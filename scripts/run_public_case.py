#!/usr/bin/env python3
"""Execute the full reported CLI pipeline with Python socket network access blocked."""

import argparse
import contextlib
import io
import json
import socket
from collections import Counter
from html import escape
from itertools import pairwise
from pathlib import Path


def blocked(*args, **kwargs):
    raise RuntimeError("Network disabled during public-case reproduction")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    # Block before importing the application; source URLs remain inert citations.
    socket.socket.connect = blocked
    socket.socket.connect_ex = blocked
    socket.create_connection = blocked
    socket.getaddrinfo = blocked
    from ghg_assurance_graph import __version__
    from ghg_assurance_graph.cli import main as cli
    from ghg_assurance_graph.reported import ReportedEvidenceTools, load_reported

    out = args.out
    out.mkdir(parents=True, exist_ok=False)
    model = load_reported(args.input.read_text())
    transcript = []

    def run(argv, filename):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            try:
                cli(argv)
            except SystemExit as exc:
                if exc.code not in (None, 0):
                    raise
        text = stream.getvalue()
        (out / filename).write_text(text)
        # Portable command transcript, no local private input/output paths.
        portable = [
            str(a).replace(str(out), "OUTPUT").replace(str(args.input), "INPUT") for a in argv
        ]
        transcript.append({"argv": ["ghgag", *portable], "output": filename, "exit": 0})
        return text

    input_path = str(args.input)
    run(["reported", "ingest", input_path], "canonical.json")
    validation = json.loads(run(["reported", "validate", input_path], "validation.json"))
    run(["reported", "graph", input_path], "graph.ttl")
    run(["reported", "graph", input_path, "--format", "json-ld"], "graph.jsonld")
    for row in model.assertions:
        run(["reported", "explain", input_path, row.id], "explain-" + row.id + ".json")
    years = sorted({r.year for r in model.assertions})
    for year in years:
        data = model.model_dump(mode="json")
        data["assertions"] = [r for r in data["assertions"] if r["year"] == year]
        (out / f"year-{year}.json").write_text(json.dumps(data, indent=2) + "\n")
    diffs = []
    for before, after in pairwise(years):
        diffs.append(
            json.loads(
                run(
                    [
                        "reported",
                        "diff",
                        str(out / f"year-{before}.json"),
                        str(out / f"year-{after}.json"),
                    ],
                    f"diff-{before}-{after}.json",
                )
            )
        )
    run(
        [
            "reported",
            "package",
            input_path,
            "--out",
            str(out / "crate"),
            "--created-at",
            "2026-09-28T00:00:00Z",
        ],
        "package-create.json",
    )
    verification = json.loads(
        run(["reported", "verify", str(out / "crate")], "package-verify.json")
    )
    if not verification["valid"]:
        raise AssertionError("package verification failed")
    run(["reported", "obsidian", input_path, "--out", str(out / "vault")], "obsidian.json")
    tools = ReportedEvidenceTools(model)
    missing = tools.missing_evidence()
    (out / "missing-evidence.json").write_text(json.dumps(missing, indent=2) + "\n")
    counts = dict(Counter(c["status"] for c in validation["checks"]))
    summary = {
        "software": __version__,
        "organization": model.organization,
        "years": years,
        "assertions": len(model.assertions),
        "validation_status": validation["status"],
        "check_status_counts": counts,
        "network": "Python socket connections and DNS blocked",
        "package_valid": True,
        "causality": "UNKNOWN",
        "upstream_recalculation_available": 0,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out / "commands.json").write_text(json.dumps(transcript, indent=2) + "\n")
    lines = [
        "# Full public-disclosure run",
        "",
        f"Organization: {escape(model.organization).replace(chr(10), ' &#10; ').replace(chr(13), ' &#13; ').replace('[', '&#91;').replace(']', '&#93;')}",
        f"Software: {__version__}",
        "",
        "Reported assertions, not reconstructed calculations or an assurance opinion.",
        "Python socket networking and DNS blocked for the complete run.",
        "",
        "## Imported numeric facts",
        "",
        "| Year | Scope/category/basis | Original value | Unit |",
        "|---|---|---|---|",
    ]
    for r in model.assertions:
        label = f"{r.scope if r.scope else 'total'} / {r.category or '-'} / {r.scope2_basis or '-'}"
        lines.append(f"| {r.year} | {label} | {r.quantity.value} | {r.quantity.unit} |")
    lines += [
        "",
        "## Validation and missingness",
        "",
        f"Overall: **{validation['status']}**. Check statuses: {counts}.",
        "Zero assertions have supplied activity/factor reconstruction or independently verified assurance.",
        "Declared metadata is not verified metadata. Missing fields are not zero or invalid numeric totals.",
        "",
        "## Cross-year differences",
        "",
    ]
    for d in diffs:
        lines.append(f"### {d['before_year']} → {d['after_year']}")
        for r in d["rows"]:
            lines.append(
                f"- {r['before']} → {r['after']}: {r['arithmetic_delta_tCO2e']} tCO2e; {r['status']}; cause UNKNOWN."
            )
    lines += [
        "",
        "No total is formed by adding alternatives, totals and components. A decrease is not proof of abatement.",
        "",
        "## Evidence",
        "",
        "Crate verification: valid (internal integrity only). See commands.json for every CLI action,",
        "canonical.json and graph exports, explanation files, validation.json, missing-evidence.json,",
        "diff files, crate/ and vault/. Source URLs/hashes are in the canonical assertion records.",
        "Raw reports are deliberately not redistributed. No arbitrary PDF parser is claimed.",
        "",
    ]
    (out / "REPORT.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
