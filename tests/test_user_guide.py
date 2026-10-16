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
    assert data["profile"] == "moenv-guide/1"
    assert data["pages"] == 14
    assert data["commands"] == 33
    expected = {"2023": "95797.473564", "2024": "95229.409244"}
    for year, total in expected.items():
        assert Fraction(data["years"][year]["total_kg_co2e"]) == Fraction(total)
        assert sum(
            Fraction(v) for v in data["years"][year]["source_amounts_kg_co2e"].values()
        ) == Fraction(total)
    sample = ROOT / "examples/moenv_training/workflow"
    assert (
        data["run_manifest_sha256"]
        == hashlib.sha256((sample / "manifest.json").read_bytes()).hexdigest()
    )
    assert (
        data["summary_sha256"] == hashlib.sha256((sample / "summary.json").read_bytes()).hexdigest()
    )
    pdf = (ROOT / "docs/user-guide/GUIDE.pdf").read_bytes()
    assert pdf.startswith(b"%PDF-") and pdf.rstrip().endswith(b"%%EOF")
    assert len(pdf) < 10_000_000
    text = (ROOT / "docs/user-guide/GUIDE.html").read_text()
    assert text.count("<section>") == 14
    assert "MOENV" in text and "ExampleCo-GHG-001" not in text
    assert "not CarbonDiff" in text and "unreviewed" in text


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
