"""Executable original-phase evidence inventory, not an automatic research approval."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASES = {
    0: ("docs/GATE_A.md", "docs/RELATED_WORK.md", ".github/roadmap.json"),
    1: ("tests/test_contract.py", "examples/hand_authored.py"),
    2: (
        "tests/test_benchmark.py",
        "tests/test_worked_example.py",
        "benchmark/ground_truth",
        "examples/worked_example/README.md",
        "examples/worked_example/sample/REPORT.md",
    ),
    3: ("tests/test_graph.py", "docs/GRAPH.md"),
    4: ("tests/test_validation.py", "docs/VALIDATION.md"),
    5: ("tests/test_diff.py", "docs/CARBONDIFF.md"),
    6: ("tests/test_evidence.py", "docs/EVIDENCE.md"),
    7: ("tests/test_exporters.py", "docs/OBSIDIAN.md"),
    8: ("tests/test_adapters.py", "docs/ADAPTERS.md"),
    9: ("tests/test_tools.py", "docs/TOOLS.md"),
    10: ("docs/OPTIONAL_AI_DECISION.md",),
    11: ("docs/ARCHIVE_STATUS.md", "docs/RELEASE_PUBLICATION_0.3.0a1.md"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="execute phase 1–9 test oracles")
    args = parser.parse_args()
    rows = []
    failed = False
    for phase, paths in PHASES.items():
        missing = [p for p in paths if not (ROOT / p).exists()]
        tests = [p for p in paths if p.startswith("tests/")]
        code = None
        if args.run and tests and not missing:
            code = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", *tests], cwd=ROOT, check=False
            ).returncode
        failed |= bool(missing) or code not in (None, 0)
        rows.append(
            {
                "phase": phase,
                "evidence": paths,
                "missing": missing,
                "test_exit": code,
                "claim": "inspect evidence; file presence alone is not completion",
            }
        )
    print(
        json.dumps(
            {
                "phases": rows,
                "external_gates": [
                    "observed fresh-host release reproduction",
                    "archival identifier resolution",
                    "human manuscript declarations and submission",
                ],
                "optional_excluded": [10],
            },
            indent=2,
        )
    )
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
