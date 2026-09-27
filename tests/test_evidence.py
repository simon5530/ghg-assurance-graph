"""Offline package contract and adversarial tests."""

import json
import shutil
import socket
from hashlib import sha256
from pathlib import Path

import pytest
from rocrate.rocrate import ROCrate

from ghg_assurance_graph.evidence import FILES, create_package, verify_package
from ghg_assurance_graph.exporters import canonical_json
from ghg_assurance_graph.models import EvidencePackage

ROOT = Path(__file__).parents[1]


@pytest.fixture
def package():
    return EvidencePackage.model_validate_json(
        (ROOT / "benchmark/generated/2025-v1/package.json").read_text()
    )


@pytest.fixture
def crate(tmp_path, package):
    path = tmp_path / "crate"
    create_package(
        package,
        path,
        created_at="2026-01-01T00:00:00Z",
        command=["ghgag", "evidence", "create"],
        data_version="fixture-v1",
    )
    return path


def rehash(crate, name):
    manifest = json.loads((crate / "manifest.json").read_text())
    data = (crate / name).read_bytes()
    manifest["files"][name] = {"sha256": sha256(data).hexdigest(), "bytes": len(data)}
    (crate / "manifest.json").write_text(canonical_json(manifest))


def test_portable_deterministic_and_library(crate, package, tmp_path, monkeypatch):
    def blocked(*args, **kwargs):
        raise AssertionError("network attempted")

    monkeypatch.setattr(socket.socket, "connect", blocked)
    other = tmp_path / "other"
    reverse = package.model_copy(update={"records": tuple(reversed(package.records))})
    create_package(
        reverse,
        other,
        created_at="2026-01-01T00:00:00Z",
        command=["ghgag", "evidence", "create"],
        data_version="fixture-v1",
    )
    assert {p.name for p in crate.iterdir()} == FILES
    for name in FILES:
        assert (crate / name).read_bytes() == (other / name).read_bytes()
    loaded = ROCrate(crate)
    assert loaded.root_dataset["datePublished"] == "2026-01-01T00:00:00Z"
    assert loaded.get("package.json") is not None
    moved = tmp_path / "unrelated-location"
    shutil.copytree(crate, moved)
    result = verify_package(moved)
    assert result["record_count"] == len(package.records)
    assert verify_package(moved, expected_manifest_sha256=result["manifest_sha256"])["valid"]
    assert len(result["manifest"]["identities"]["EmissionFactor"]) == 15
    with pytest.raises(ValueError):
        verify_package(moved, expected_manifest_sha256="0" * 64)


@pytest.mark.parametrize(
    "attack",
    [
        "tamper",
        "missing",
        "extra",
        "directory",
        "symlink",
        "traversal",
        "absolute",
        "manifest",
        "duplicate",
    ],
)
def test_fail_closed(crate, tmp_path, attack):
    payload = crate / "graph.ttl"
    if attack == "tamper":
        payload.write_text("tampered")
    elif attack == "missing":
        payload.unlink()
    elif attack == "extra":
        (crate / "extra").write_text("x")
    elif attack == "directory":
        payload.unlink()
        payload.mkdir()
    elif attack == "symlink":
        elsewhere = tmp_path / "elsewhere"
        elsewhere.write_bytes(payload.read_bytes())
        payload.unlink()
        payload.symlink_to(elsewhere)
    elif attack in ("traversal", "absolute"):
        manifest = json.loads((crate / "manifest.json").read_text())
        name = "../outside" if attack == "traversal" else "/etc/passwd"
        manifest["files"][name] = manifest["files"].pop("graph.ttl")
        (crate / "manifest.json").write_text(canonical_json(manifest))
    elif attack == "manifest":
        (crate / "manifest.json").write_text("[]")
    else:
        (crate / "manifest.json").write_text('{"format":1,"format":2}')
    with pytest.raises(ValueError):
        verify_package(crate)


@pytest.mark.parametrize("name", ["graph.jsonld", "ro-crate-metadata.json"])
def test_remote_context_even_with_rehashed_manifest(crate, name, monkeypatch):
    monkeypatch.setattr(socket.socket, "connect", lambda *args: pytest.fail("network access"))
    data = json.loads((crate / name).read_text())
    if isinstance(data, list):
        data[0]["@context"] = "https://example.invalid/context"
    else:
        data["@context"] = "https://example.invalid/context"
    (crate / name).write_text(canonical_json(data))
    rehash(crate, name)
    with pytest.raises(ValueError, match="context"):
        verify_package(crate)


def test_semantic_tampering_rehashed(crate):
    (crate / "graph.ttl").write_text("<urn:bad> <urn:bad> <urn:bad> .\n")
    rehash(crate, "graph.ttl")
    with pytest.raises(ValueError, match="inconsistent"):
        verify_package(crate)


def test_provenance_and_no_overwrite(crate, package, tmp_path):
    with pytest.raises(FileExistsError):
        create_package(package, crate, created_at="2026-01-01T00:00:00Z", command=["test"])
    for timestamp in ("2026-01-01", "nonsense"):
        with pytest.raises(ValueError):
            create_package(package, tmp_path / "new", created_at=timestamp, command=["test"])
    link = tmp_path / "link"
    link.symlink_to(crate, target_is_directory=True)
    with pytest.raises(ValueError):
        verify_package(link)
    with pytest.raises(ValueError):
        create_package(package, link / "child", created_at="2026-01-01T00:00:00Z", command=["t"])


@pytest.mark.parametrize(
    "data", [b"\xff", b"[" * 2000 + b"0" + b"]" * 2000, b'{"x":1e999}', b"null", b"42"]
)
def test_malformed_manifest_is_value_error(crate, data):
    (crate / "manifest.json").write_bytes(data)
    with pytest.raises(ValueError):
        verify_package(crate)


def test_resource_limits(crate, monkeypatch):
    from ghg_assurance_graph import evidence

    monkeypatch.setattr(evidence, "MAX_FILE_BYTES", 100)
    with pytest.raises(ValueError, match="size limit"):
        verify_package(crate)
    monkeypatch.setattr(evidence, "MAX_FILE_BYTES", 16_000_000)
    monkeypatch.setattr(evidence, "MAX_PACKAGE_BYTES", 100)
    with pytest.raises(ValueError, match="size limit"):
        verify_package(crate)


@pytest.mark.parametrize("replacement", ["symlink", "fifo"])
def test_replacement_at_open_fails_closed(crate, tmp_path, monkeypatch, replacement):
    import os

    from ghg_assurance_graph import evidence

    original = os.open
    target = crate / "graph.ttl"
    outside = tmp_path / "outside"
    outside.write_bytes(target.read_bytes())

    def swapped(path, flags, *args, **kwargs):
        if path == "graph.ttl":
            target.unlink()
            if replacement == "symlink":
                target.symlink_to(outside)
            else:
                os.mkfifo(target)
        return original(path, flags, *args, **kwargs)

    monkeypatch.setattr(evidence.os, "open", swapped)
    with pytest.raises(ValueError):
        verify_package(crate)


@pytest.mark.parametrize("ref", ["../../private", "file:///etc/passwd", "https://evil.invalid/x"])
def test_foreign_rocrate_entity_rehashed(crate, monkeypatch, ref):
    monkeypatch.setattr(socket.socket, "connect", lambda *a: pytest.fail("network access"))
    path = crate / "ro-crate-metadata.json"
    metadata = json.loads(path.read_text())
    metadata["@graph"].append({"@id": ref, "@type": "File"})
    path.write_text(canonical_json(metadata))
    rehash(crate, path.name)
    with pytest.raises(ValueError, match="inconsistent"):
        verify_package(crate)
