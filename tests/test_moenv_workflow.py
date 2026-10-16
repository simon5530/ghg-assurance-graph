"""Execute documented primary CLI workflow independently of committed receipts."""

import hashlib
import json
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).parents[1]


def file_map(root):
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in root.rglob("*")
        if p.is_file()
    }


def test_primary_workflow_replay_and_no_overwrite(tmp_path):
    runner = ROOT / "scripts/run_moenv_example.py"
    outputs = []
    for seed in ("11", "73"):
        output = tmp_path / seed
        env = {**os.environ, "PYTHONHASHSEED": seed}
        result = subprocess.run(
            [sys.executable, str(runner), "--out", str(output)],
            env=env,
            check=False,
            capture_output=True,
            text=True,
            timeout=90,
        )
        assert result.returncode == 0, result.stderr
        summary = json.loads(result.stdout)
        assert summary["commands"] == 33
        assert summary["years"]["2023"]["canonical_records"] == 50
        assert summary["years"]["2024"]["canonical_records"] == 61
        assert Fraction(summary["years"]["2023"]["total_kg_co2e"]) == Fraction("95797.473564")
        assert Fraction(summary["years"]["2024"]["total_kg_co2e"]) == Fraction("95229.409244")
        assert [row["unreviewed_results"] for row in summary["years"].values()] == [4, 5]
        calls = json.loads((output / "commands.json").read_text())
        assert sum(c["exit_code"] == 0 for c in calls) == 30
        assert sum(c["exit_code"] == 2 for c in calls) == 3
        for c in calls:
            assert c["exit_code"] == c["expected_exit_code"]
            assert (
                hashlib.sha256((output / c["stdout"]).read_bytes()).hexdigest()
                == c["stdout_sha256"]
            )
            assert (
                hashlib.sha256((output / c["stderr"]).read_bytes()).hexdigest()
                == c["stderr_sha256"]
            )
        for year in ("2023", "2024"):
            assert json.loads((output / f"stages/{year}/package-verify.json").read_text())["valid"]
            assert len(list((output / f"generated/{year}/evidence").glob("*.json"))) == 61
        outputs.append(output)
    assert file_map(outputs[0]) == file_map(outputs[1])
    before = file_map(outputs[0])
    again = subprocess.run(
        [sys.executable, str(runner), "--out", str(outputs[0])], capture_output=True, check=False
    )
    assert again.returncode == 2
    assert file_map(outputs[0]) == before


def test_reference_receipts_and_primary_scope():
    reference = ROOT / "examples/moenv_training/workflow"
    selected = json.loads((reference / "selected-manifest.json").read_text())
    for name, digest in selected["sha256"].items():
        assert hashlib.sha256((reference / name).read_bytes()).hexdigest() == digest
    summary = json.loads((reference / "summary.json").read_text())
    compare = summary["comparison"]
    assert compare["not_carbon_diff"] is True
    assert {r["causality"] for r in compare["sources"]} == {"UNKNOWN"}
    assert sum(Fraction(r["delta"]) for r in compare["sources"]) == Fraction("-568.064320")
    readme = (ROOT / "README.md").read_text()
    primary = readme.split("## Reproduce locally", 1)[1].split("## Documentation", 1)[0]
    assert "scripts/run_moenv_example.py" in primary
    assert "benchmark/generated/2026" not in primary
