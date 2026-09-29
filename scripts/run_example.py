"""Reproduce the bounded synthetic ExampleCo-GHG-001 workflow offline using the installed CLI.

Usage: python scripts/run_example.py --python .venv/bin/python --out /tmp/exampleco-ghg-001
No installation or network retrieval occurs. Output must be absent or empty.
"""

import argparse
import contextlib
import hashlib
import io
import json
import os
import platform
import re
import socket
import subprocess
from fractions import Fraction
from importlib.metadata import version
from itertools import pairwise
from pathlib import Path

VERSIONS = ("2025-v1", "2025-v2", "2026-v1")
CREATED_AT = "2026-09-28T00:00:00Z"
# Scenario assertions, not numerical answers or inferred causal explanations.
SCENARIOS = (
    (
        "fleet",
        "CORRECTION",
        "activity",
        "Corrected synthetic fleet invoice replaces 30 with 40 liters.",
    ),
    (
        "travel",
        "MISSING_DATA_RESOLVED",
        "activity origin",
        "Synthetic primary travel log replaces the 100 km estimate with 150 km.",
    ),
    (
        "materials",
        "SUPPLIER_MIX_CHANGE",
        "factor",
        "Invented supplier mix changes from 75/25 to 50/50; technology factors stay 5 and 1.",
    ),
    (
        "refrigerant",
        "GWP_CHANGE",
        "factor gwp_basis",
        "Invented characterization basis changes from A to B, not a physical gas reduction.",
    ),
    (
        "new-line",
        "BOUNDARY_CHANGE",
        "activity",
        "Organic source expansion adds a line using 10 liters; not an acquisition.",
    ),
    (
        "allocation",
        "ALLOCATION_CHANGE",
        "allocation_method allocation_share",
        "Synthetic allocation policy changes from 50% mass share to 25% economic share.",
    ),
    (
        "method-transition",
        "METHOD_CHANGE",
        "activity unit factor_unit factor method pcf_boundary",
        "Same synthetic lot changes from spend-based estimation to supplier PCF; not abatement.",
    ),
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def block_network():
    """Process-local guard, not an OS sandbox; installed dependencies are trusted."""

    def blocked(*args, **kwargs):
        raise RuntimeError("Network disabled during ExampleCo-GHG-001 reproduction")

    for name in ("connect", "connect_ex", "sendto", "sendmsg"):
        if hasattr(socket.socket, name):
            setattr(socket.socket, name, blocked)
    for name in (
        "create_connection",
        "getaddrinfo",
        "gethostbyname",
        "gethostbyname_ex",
        "gethostbyaddr",
    ):
        setattr(socket, name, blocked)
    # Verify the guards without attempting DNS or opening an external connection.
    for action in (
        lambda: socket.getaddrinfo("example.invalid", 443),
        lambda: socket.create_connection(("127.0.0.1", 9)),
    ):
        try:
            action()
        except RuntimeError:
            continue
        raise RuntimeError("network guard did not reject probe")


def reproduce(out):
    block_network()  # Before any application/dependency import.
    from ghg_assurance_graph.cli import main as cli

    require(not out.is_symlink(), "output must not be a symlink")
    require(
        not out.exists() or (out.is_dir() and not any(out.iterdir())),
        "output must be absent or empty; refusing to overwrite",
    )
    out.mkdir(parents=True, exist_ok=True)
    previous = Path.cwd()
    os.chdir(out)
    receipts = []

    def run(argv, artifact, expected=0):
        stdout, stderr = io.StringIO(), io.StringIO()
        code = 0
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                cli(argv)
            except SystemExit as exc:
                code = exc.code or 0
        path = Path(artifact)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(stdout.getvalue(), encoding="utf-8")
        error_path = path.with_suffix(path.suffix + ".stderr.txt")
        error_path.write_text(stderr.getvalue(), encoding="utf-8")
        receipts.append(
            {
                "argv": ["ghgag", *argv],
                "cwd": "OUTPUT",
                "exit_code": code,
                "expected_exit_code": expected,
                "stdout": artifact,
                "stdout_sha256": digest(path),
                "stderr": error_path.as_posix(),
                "stderr_sha256": digest(error_path),
            }
        )
        dump(Path("commands.json"), receipts)
        require(code == expected, f"unexpected CLI exit {code}: {argv}")
        return json.loads(stdout.getvalue()) if artifact.endswith(".json") else stdout.getvalue()

    try:
        run(["benchmark", "generate", "--out", "generated"], "benchmark-generate.json")
        provenance, totals, checks, packages, vaults = [], {}, {}, {}, {}
        calculations = {}
        for snapshot in VERSIONS:
            source = f"generated/{snapshot}"
            rows = json.loads(Path(source, "inputs.json").read_text())
            model = json.loads(Path(source, "package.json").read_text())
            # Benchmark hashes dumps(row), including its terminal newline. The model
            # strips citation whitespace: restore that newline, then prove the hash.
            # These are synthetic source records, never purported invoices or public PDFs.
            for record in model["records"]:
                if record["kind"] != "EvidenceArtifact":
                    continue
                path = Path("sources", snapshot, record["label"] + ".json")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((record["citation"] + "\n").encode())
                require(digest(path) == record["sha256"], "citation digest mismatch")
                provenance.append(
                    {
                        "artifact_id": record["id"],
                        "path": path.as_posix(),
                        "sha256": digest(path),
                        "synthetic": True,
                        "license": "MIT",
                    }
                )
            # Independent Fraction oracle: no benchmark.amount or expected-answer files.
            amounts = [
                Fraction(r["activity"]) * Fraction(r["factor"]) * Fraction(r["allocation_share"])
                for r in rows
            ]
            require(
                all(r["unit"] == r["factor_unit"] for r in rows),
                "oracle only covers these same-unit fixtures",
            )
            results = {
                r["label"]: Fraction(str(r["quantity"]["value"]))
                for r in model["records"]
                if r["kind"] == "EmissionResult"
            }
            require(
                all(
                    results[r["id"] + "-result"] == amount == Fraction(r["reported_kg_co2e"])
                    for r, amount in zip(rows, amounts, strict=True)
                ),
                "numeric mismatch",
            )
            calculations[snapshot] = [
                {
                    "source": row["id"],
                    "activity": row["activity"],
                    "unit": row["unit"],
                    "factor": row["factor"],
                    "factor_denominator": row["factor_unit"],
                    "allocation_share": row["allocation_share"],
                    "kg_co2e": str(value),
                }
                for row, value in zip(rows, amounts, strict=True)
            ]
            dump(Path("calculations", snapshot + ".json"), calculations[snapshot])
            total = sum(amounts)
            require(total.denominator == 1, "noninteger ExampleCo-GHG-001 total")
            totals[snapshot] = int(total)
            base = f"stages/{snapshot}"
            checks[snapshot] = run(["validate", source], f"{base}/validation.json")
            require(checks[snapshot]["conforms"], "validation failed")
            # Explicit package-only validation is the SHACL stage; directory validation also
            # checks raw-row policy. Both invoke the actual installed CLI.
            shacl = run(["validate", f"{source}/package.json"], f"{base}/shacl.json")
            require(shacl["conforms"], "SHACL failed")
            run(["graph", "build", source], f"{base}/graph.ttl")
            for row in rows:
                explained = run(
                    [
                        "graph",
                        "explain",
                        f"urn:ghgag:exampleco-ghg-001-{snapshot}-{row['id']}-result:v1",
                        "--input",
                        source,
                    ],
                    f"{base}/explain/{row['id']}.json",
                )
                require(bool(explained), "empty lineage explanation")
            run(
                ["export", "json-ld", f"{base}/graph.jsonld", "--input", source],
                f"{base}/export-jsonld.json",
            )
            crate = f"packages/{snapshot}"
            run(
                [
                    "package",
                    "create",
                    source,
                    "--out",
                    crate,
                    "--created-at",
                    CREATED_AT,
                    "--data-version",
                    f"exampleco-ghg-001-0.1-{snapshot}",
                ],
                f"{base}/package-create.json",
            )
            packages[snapshot] = run(["package", "verify", crate], f"{base}/package-verify.json")
            require(packages[snapshot]["valid"], "package verification failed")
            vault = f"vaults/{snapshot}"
            run(["export", "obsidian", vault, "--input", source], f"{base}/obsidian.json")
            notes = list(Path(vault).glob("*.md"))
            for note in notes:
                for target in re.findall(r"\[\[([^]\n]+)\]\]", note.read_text()):
                    require(Path(vault, target + ".md").is_file(), "broken vault wikilink")
            vaults[snapshot] = len(notes)
        require(list(totals.values()) == [3820, 3850, 4060], "literal total oracle failed")
        dump(
            Path("input-provenance.json"),
            {
                "sources": provenance,
                "generated_manifest_sha256": digest(Path("generated/manifest.json")),
                "scope": "Generated synthetic citation records, not external authenticated evidence",
            },
        )
        diffs = {}
        for index, (before, after) in enumerate(pairwise(VERSIONS)):
            pair = f"{before}--{after}"
            declarations = []
            for entity, cause, fields, text in SCENARIOS[:2] if index == 0 else SCENARIOS[2:]:
                path = Path("sources/scenarios", pair, entity + ".md")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    "# Synthetic scenario declaration\n\n"
                    + text
                    + "\n\nInvented assertion; not independently authenticated. MIT.\n"
                )
                declarations.append(
                    {
                        "before": before,
                        "after": after,
                        "entity": entity,
                        "cause": cause,
                        "fields": fields.split(),
                        "evidence": f"{path.as_posix()}#sha256={digest(path)}",
                    }
                )
            declaration_path = f"declarations/{pair}.json"
            dump(Path(declaration_path), declarations)
            diffs[pair] = {}
            for mode in ("unassisted", "assisted"):
                argv = ["diff", f"generated/{before}", f"generated/{after}"]
                if mode == "assisted":
                    argv += ["--declarations", declaration_path]
                result = run(argv, f"diffs/{pair}/{mode}.json")
                delta = Fraction(result["delta"])
                require(
                    delta == [30, 210][index] == totals[after] - totals[before],
                    "delta oracle failed",
                )
                require(
                    sum(Fraction(c["kg_co2e"]) for c in result["components"]) == delta,
                    "components do not reconcile",
                )
                if mode == "assisted":
                    require(
                        Fraction(result["absolute_unknown_kg_co2e"]) == 0,
                        "assisted unknown exposure",
                    )
                diffs[pair][mode] = result
        negative = run(
            ["validate", "generated/defects/double-gwp.json"],
            "negative-validation.json",
            expected=1,
        )
        require(not negative["conforms"] and negative["findings"], "negative control passed")
        missing = run(
            ["validate", "generated/defects/missing-factor-source.json"],
            "missing-evidence-validation.json",
            expected=1,
        )
        require(not missing["conforms"] and missing["findings"], "missing evidence control passed")
        summary = {
            "software": {
                name: version(name)
                for name in ("ghg-assurance-graph", "pydantic", "rdflib", "pyshacl", "rocrate")
            },
            "python": platform.python_version(),
            "created_at": CREATED_AT,
            "totals_kg_co2e": totals,
            "oracle": "Fraction products plus literal totals/deltas",
            "network": "Python socket connections, DNS and datagram sends blocked; not an OS sandbox",
            "source_records": len(provenance),
            "commands": len(receipts),
            "package_valid": {k: v["valid"] for k, v in packages.items()},
            "vault_note_counts": vaults,
            "negative_expected_exit": 1,
        }
        dump(Path("summary.json"), summary)
        lines = [
            "# ExampleCo-GHG-001 synthetic worked example",
            "",
            "Generated by the installed CLI; selected sources only, not a complete corporate inventory.",
            "Invented factors, GWP bases and review decisions; no assurance opinion or causal inference.",
            "Integrity checks are not evidence authentication. No market-based fallback, offsets or removals.",
            "",
            "## Execution",
            "",
            f"Software: {summary['software']}; Python {summary['python']}.",
            summary["network"] + ". No downloads or installation occur in this runner.",
            f"{len(receipts)} CLI receipts: [commands.json](commands.json). Paths are relative to OUTPUT.",
            "",
            "## Partial totals and validation",
            "",
            "| Snapshot | kg CO2e | Conforms (SHACL + raw rows) | Crate valid | Vault notes |",
            "|---|---:|---|---|---:|",
        ]
        for snapshot in VERSIONS:
            lines.append(
                f"| {snapshot} | {totals[snapshot]} | {checks[snapshot]['conforms']} | "
                f"{packages[snapshot]['valid']} | {vaults[snapshot]} |"
            )
        lines += [
            "",
            "## Per-result calculation trail",
            "",
            "Factors are invented kgCO2e per activity unit; allocation is applied once.",
            "The exact rational oracle independently checks each reported result.",
        ]
        for snapshot, rows in calculations.items():
            lines += [
                "",
                "### " + snapshot,
                "",
                "| Source | Activity | Unit | Factor | Share | kgCO2e |",
                "|---|---:|---|---:|---:|---:|",
            ]
            lines += [
                f"| {r['source']} | {r['activity']} | {r['unit']} | {r['factor']} | "
                f"{r['allocation_share']} | {r['kg_co2e']} |"
                for r in rows
            ]
        lines += [
            "",
            "Independent Fraction arithmetic agrees with every result and literal totals 3820/3850/4060.",
            "",
            "## Changes: mechanical versus declaration-assisted",
            "",
            "Assisted labels are supplied synthetic interpretations, not discovered causes.",
            "Convention: activity-first, factor-second, allocation-last; semantic row override.",
            "Absolute UNKNOWN exposure is retained because signed residuals can cancel.",
            "",
        ]
        for pair, modes in diffs.items():
            lines += [f"### {pair}", ""]
            for mode, result in modes.items():
                lines += [
                    (
                        f"**{mode}**: delta {result['delta']} kg CO2e; attributed "
                        f"{result['attributed_kg_co2e']}; signed residual {result['residual_kg_co2e']}; "
                        f"absolute UNKNOWN {result['absolute_unknown_kg_co2e']}."
                    )
                ]
                lines += [
                    f"- {c['entity']}: {c['cause']} = {c['kg_co2e']} kg CO2e"
                    for c in result["components"]
                ]
                lines.append("")
        lines += [
            "## Evidence and negative control",
            "",
            f"{len(provenance)} local synthetic citation documents match existing EvidenceArtifact hashes.",
            "See input-provenance.json, sources/, declarations/, generated/, stages/, packages/ and vaults/.",
            "The benchmark inputs and canonical packages are unmodified generator output.",
            "Sources remain outside the closed-profile crates; the run-level manifest covers both.",
            f"Deliberate double-GWP input exited 1 with {len(negative['findings'])} findings:",
        ]
        lines += [f"- {f['target']}: {f['rule']}" for f in negative["findings"]]
        lines += ["", "Missing factor source also exited 1, without fabricating provenance:"]
        lines += [f"- {f['target']}: {f['rule']}" for f in missing["findings"]]
        lines += [
            "",
            "manifest.json hashes all run files except itself; no authenticity claim is made.",
            "",
        ]
        Path("REPORT.md").write_text("\n".join(lines), encoding="utf-8")
        dump(
            Path("manifest.json"),
            {
                "sha256": {
                    p.as_posix(): digest(p)
                    for p in sorted(Path(".").rglob("*"))
                    if p.is_file() and p != Path("manifest.json")
                }
            },
        )
        return summary
    finally:
        os.chdir(previous)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--python", help="Installed Python executable (e.g. fresh wheel venv)")
    args = parser.parse_args()
    if args.python:
        # Do not inject checkout src or PYTHONPATH into the selected installed environment.
        env = dict(os.environ)
        env.pop("PYTHONPATH", None)
        command = [
            args.python,
            "-I",
            str(Path(__file__).resolve()),
            "--out",
            str(args.out.absolute()),
        ]
        raise SystemExit(subprocess.run(command, env=env, check=False).returncode)
    try:
        print(json.dumps(reproduce(args.out.absolute()), sort_keys=True, indent=2))
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(2, f"ExampleCo-GHG-001 reproduction failed: {exc}\n")


if __name__ == "__main__":
    main()
