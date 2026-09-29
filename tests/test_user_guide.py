"""Independent workbook and safe-input exercise contracts."""

import hashlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_workbook_data_matches_literal_scope_oracle():
    data = json.loads((ROOT / "docs/user-guide/figure-data.json").read_text())
    assert data["pages"] == 16
    assert data["totals"] == {"2025-v1": 3820, "2025-v2": 3850, "2026-v1": 4060}
    assert data["scopes"] == {
        "2025-v1": {"1": 2320, "2": 500, "3": 1000},
        "2025-v2": {"1": 2340, "2": 500, "3": 1010},
        "2026-v1": {"1": 2770, "2": 480, "3": 810},
    }
    sample = ROOT / "examples/worked_example/sample"
    assert (
        data["run_manifest_sha256"]
        == hashlib.sha256((sample / "full-run-manifest.json").read_bytes()).hexdigest()
    )
    for name, expected in json.loads((sample / "selected-manifest.json").read_text())[
        "sha256"
    ].items():
        assert hashlib.sha256((sample / name).read_bytes()).hexdigest() == expected
    pdf = (ROOT / "docs/user-guide/GUIDE.pdf").read_bytes()
    assert pdf.startswith(b"%PDF-") and pdf.rstrip().endswith(b"%%EOF")
    assert len(pdf) < 10_000_000
    text = (ROOT / "docs/user-guide/GUIDE.html").read_text()
    assert text.count("<section>") == 16
    assert "ACME" not in text and "not trademark" in text


def test_safe_input_exercise_regenerates_and_refuses_overwrite(tmp_path):
    out = tmp_path / "exercise"
    command = [sys.executable, str(ROOT / "scripts/modify_example.py"), "--out", str(out)]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["total_kg_co2e"] == 3870
    rows = json.loads((out / "inputs.json").read_text())
    assert (
        sum(
            Fraction(r["activity"]) * Fraction(r["factor"]) * Fraction(r["allocation_share"])
            for r in rows
        )
        == 3870
    )
    package = json.loads((out / "package.json").read_text())
    for record in package["records"]:
        if record["kind"] == "EvidenceArtifact":
            assert (
                hashlib.sha256((record["citation"] + chr(10)).encode()).hexdigest()
                == record["sha256"]
            )
    before = (out / "package.json").read_bytes()
    assert subprocess.run(command, capture_output=True, check=False).returncode == 2
    assert (out / "package.json").read_bytes() == before
