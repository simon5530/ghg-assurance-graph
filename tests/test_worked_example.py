"""End-to-end runner regressions: literal oracle, real CLI receipts and byte trees."""

import hashlib
import importlib.util
import json
import os
import re
import socket
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/run_acme_example.py"
VERSIONS = ("2025-v1", "2025-v2", "2026-v1")


def read(path):
    return json.loads(path.read_text())


def tree(root):
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def invoke(out, *, seed="1", python=None):
    env = dict(os.environ, PYTHONHASHSEED=seed)
    return subprocess.run(
        [sys.executable, str(RUNNER), "--python", python or sys.executable, "--out", str(out)],
        cwd=out.parent,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
    )


@pytest.fixture(scope="module")
def completed(tmp_path_factory):
    root = tmp_path_factory.mktemp("worked-example")
    a, b = root / "a", root / "b"
    b.mkdir()  # An explicitly empty destination is allowed.
    for out, seed in ((a, "1"), (b, "999")):
        result = invoke(out, seed=seed)
        assert result.returncode == 0, result.stdout + result.stderr
    return a, b


def test_two_complete_trees_are_byte_identical(completed):
    a, b = completed
    assert tree(a) == tree(b)
    manifest = read(a / "manifest.json")["sha256"]
    assert manifest == {k: v for k, v in tree(a).items() if k != "manifest.json"}
    assert len(manifest) > 500


def test_independent_literal_totals_and_deltas(completed):
    a, _ = completed
    assert read(a / "summary.json")["totals_kg_co2e"] == dict(zip(VERSIONS, (3820, 3850, 4060)))
    for snapshot, expected in zip(VERSIONS, (3820, 3850, 4060), strict=True):
        rows = read(a / "generated" / snapshot / "inputs.json")
        products = [
            Fraction(r["activity"]) * Fraction(r["factor"]) * Fraction(r["allocation_share"])
            for r in rows
        ]
        assert sum(products) == expected
        assert len(products) == 15
        for name in ("validation.json", "shacl.json"):
            assert read(a / "stages" / snapshot / name) == {"conforms": True, "findings": []}
        assert len(list((a / "stages" / snapshot / "explain").glob("*.json"))) == 15
        for path in (a / "stages" / snapshot / "explain").glob("*.json"):
            assert read(path)
    for before, after, delta, residual, exposure in (
        ("2025-v1", "2025-v2", 30, 10, 10),
        ("2025-v2", "2026-v1", 210, 300, 500),
    ):
        for mode in ("unassisted", "assisted"):
            data = read(a / "diffs" / f"{before}--{after}" / f"{mode}.json")
            assert Fraction(data["delta"]) == delta
            assert sum(Fraction(c["kg_co2e"]) for c in data["components"]) == delta
            assert Fraction(data["residual_kg_co2e"]) == (residual if mode == "unassisted" else 0)
            assert Fraction(data["absolute_unknown_kg_co2e"]) == (
                exposure if mode == "unassisted" else 0
            )
    latest = read(a / "diffs/2025-v2--2026-v1/assisted.json")
    assert {(c["entity"], c["cause"]): Fraction(c["kg_co2e"]) for c in latest["components"]} == {
        ("electricity", "ACTIVITY_CHANGE"): -100,
        ("electricity", "EMISSION_FACTOR_CHANGE"): 80,
        ("materials", "SUPPLIER_MIX_CHANGE"): -100,
        ("method-transition", "METHOD_CHANGE"): -50,
        ("refrigerant", "GWP_CHANGE"): 400,
        ("new-line", "BOUNDARY_CHANGE"): 30,
        ("allocation", "ALLOCATION_CHANGE"): -50,
    }


def test_receipts_provenance_and_negative_exit(completed):
    a, _ = completed
    receipts = read(a / "commands.json")
    assert len(receipts) == read(a / "summary.json")["commands"]
    assert len(receipts) == 73
    for receipt in receipts:
        assert receipt["exit_code"] == receipt["expected_exit_code"]
        assert receipt["argv"][0] == "ghgag"
        assert receipt["cwd"] == "OUTPUT"
        assert str(a.parent) not in json.dumps(receipt)
        for stream in ("stdout", "stderr"):
            assert (
                hashlib.sha256((a / receipt[stream]).read_bytes()).hexdigest()
                == receipt[stream + "_sha256"]
            )
    failed = [r for r in receipts if r["exit_code"]]
    assert len(failed) == 2 and all(r["exit_code"] == 1 for r in failed)
    missing = read(a / "missing-evidence-validation.json")
    assert missing["conforms"] is False and missing["findings"]
    negative = read(a / "negative-validation.json")
    assert negative["conforms"] is False
    assert any("GWP" in f["rule"] for f in negative["findings"])
    sources = read(a / "input-provenance.json")["sources"]
    assert len(sources) == 45
    for source in sources:
        assert source["synthetic"] is True
        assert hashlib.sha256((a / source["path"]).read_bytes()).hexdigest() == source["sha256"]
    # Preserve the existing generator byte contract; don't silently rewrite benchmark hashes.
    for name, digest in read(ROOT / "benchmark/generated/manifest.json")["sha256"].items():
        assert hashlib.sha256((a / "generated" / name).read_bytes()).hexdigest() == digest
    for path in (a / "declarations").glob("*.json"):
        for declaration in read(path):
            source, digest = declaration["evidence"].split("#sha256=")
            assert hashlib.sha256((a / source).read_bytes()).hexdigest() == digest
            assert "kg_co2e" not in declaration


def test_packages_vaults_and_real_report(completed):
    a, _ = completed
    report = (a / "REPORT.md").read_text()
    assert "not a complete corporate inventory" in report
    assert "not discovered causes" in report
    for snapshot in VERSIONS:
        proof = read(a / "stages" / snapshot / "package-verify.json")
        assert proof["valid"] is True and proof["record_count"] == 158
        assert (
            proof["manifest_sha256"]
            == hashlib.sha256(
                (a / "packages" / snapshot / "manifest.json").read_bytes()
            ).hexdigest()
        )
        vault = a / "vaults" / snapshot
        assert (vault / "index.md").is_file()
        for note in vault.glob("*.md"):
            for target in re.findall(r"\[\[([^]\n]+)\]\]", note.read_text()):
                assert (vault / (target + ".md")).is_file()
    for pair in ("2025-v1--2025-v2", "2025-v2--2026-v1"):
        for mode in ("unassisted", "assisted"):
            data = read(a / "diffs" / pair / f"{mode}.json")
            assert f"delta {data['delta']} kg CO2e" in report
            for c in data["components"]:
                assert f"{c['entity']}: {c['cause']} = {c['kg_co2e']} kg CO2e" in report


def test_nonempty_destination_is_untouched(completed):
    a, _ = completed
    before = tree(a)
    result = invoke(a)
    assert result.returncode == 2
    assert "refusing to overwrite" in result.stderr
    assert tree(a) == before


def test_network_guard_blocks_before_application_import(monkeypatch):
    spec = importlib.util.spec_from_file_location("acme_runner", RUNNER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Keep guard installation local to this test process.
    for name in ("connect", "connect_ex", "sendto", "sendmsg"):
        if hasattr(socket.socket, name):
            monkeypatch.setattr(socket.socket, name, getattr(socket.socket, name))
    for name in (
        "create_connection",
        "getaddrinfo",
        "gethostbyname",
        "gethostbyname_ex",
        "gethostbyaddr",
    ):
        monkeypatch.setattr(socket, name, getattr(socket, name))
    module.block_network()
    with pytest.raises(RuntimeError, match="Network disabled"):
        socket.getaddrinfo("example.invalid", 443)
    with socket.socket() as sock, pytest.raises(RuntimeError, match="Network disabled"):
        sock.connect(("127.0.0.1", 9))


def test_selected_python_is_used(tmp_path):
    # A missing executable must fail, never fall back to the checkout environment.
    result = invoke(tmp_path / "out", python=str(tmp_path / "missing-python"))
    assert result.returncode != 0
    assert not (tmp_path / "out").exists()
