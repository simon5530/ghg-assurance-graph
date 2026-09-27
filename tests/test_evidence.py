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
