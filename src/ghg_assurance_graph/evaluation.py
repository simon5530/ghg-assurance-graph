"""Explicit-label evaluation, separate from all detectors and attribution code."""

import json
from dataclasses import asdict
from itertools import pairwise
from pathlib import Path

from .diff import Snapshot, compare
from .serialization import from_json
from .validation import evaluate_findings, validate_package, validate_rows


def evaluate_benchmark(root: Path, truth: Path) -> dict:
    expected = json.loads((truth / "expected_findings.json").read_text())["findings"]
    predictions = {
        path.stem: validate_rows(json.loads(path.read_text())["rows"])
        for path in sorted((root / "defects").glob("*.json"))
    }
    clean = {}
    versions = ("2025-v1", "2025-v2", "2026-v1")
    snapshots = {}
    for version in versions:
        folder = root / version
        rows = json.loads((folder / "inputs.json").read_text())
        package = from_json((folder / "package.json").read_text())
        findings = (*validate_rows(rows), *validate_package(package))
        clean[version] = len(findings)
        predictions[version] = findings
        snapshots[version] = Snapshot(
            "synthetic://exampleco-ghg-001/20250926", version, tuple(rows)
        )
    metrics = evaluate_findings(predictions, expected)
    metrics["by_rule"] = {
        rule: evaluate_findings(
            {
                case: [f for f in findings if f.rule == rule]
                for case, findings in predictions.items()
            },
            [row for row in expected if row["rule"] == rule],
        )
        for rule in sorted({r["rule"] for r in expected})
    }
    metrics["by_split"] = {}
    for split in sorted({r["split"] for r in expected}):
        labels = [r for r in expected if r["split"] == split]
        cases = {r["case_id"] for r in labels}
        metrics["by_split"][split] = evaluate_findings(
            {case: findings for case, findings in predictions.items() if case in cases}, labels
        )
    comparisons = [asdict(compare(snapshots[a], snapshots[b])) for a, b in pairwise(versions)]
    return {
        "benchmark": "0.1",
        "clean_finding_counts": clean,
        "validation": metrics,
        "carbondiff_unassisted": comparisons,
        "limits": "Public synthetic labels; no blind generalization or practitioner validation. "
        "CarbonDiff without semantic declarations leaves unsupported changes UNKNOWN.",
    }
