"""Execute the MOENV 2023/2024 CLI workflow, saving real command receipts offline."""

import argparse
import contextlib
import hashlib
import io
import json
import os
import platform
import re
import shutil
import socket
import subprocess
from fractions import Fraction
from importlib.metadata import version
from pathlib import Path

STAMP = "2026-10-16T00:00:00Z"


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def block_network():
    def blocked(*args, **kwargs):
        raise RuntimeError("MOENV example run does not allow socket networking")

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


def reproduce(out):
    block_network()  # Process-local guard, not an OS sandbox.
    from ghg_assurance_graph.cli import main as cli
    from ghg_assurance_graph.moenv_example import main as collection_cli

    if out.exists() or out.is_symlink():
        raise ValueError("output must not exist; choose a new directory")
    out.mkdir(parents=True)
    previous = Path.cwd()
    receipts = []

    def run(argv, artifact, *, collection=False, expected=0):
        stdout, stderr = io.StringIO(), io.StringIO()
        code = 0
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                (collection_cli if collection else cli)(argv)
            except SystemExit as exc:
                code = exc.code or 0
        path = Path(artifact)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(stdout.getvalue())
        error = path.with_suffix(path.suffix + ".stderr.txt")
        error.write_text(stderr.getvalue())
        command = ["python", "-m", "ghg_assurance_graph.moenv_example"] if collection else ["ghgag"]
        receipts.append(
            {
                "argv": command + argv,
                "cwd": "OUTPUT",
                "exit_code": code,
                "expected_exit_code": expected,
                "stdout": artifact,
                "stdout_sha256": digest(path),
                "stderr": error.as_posix(),
                "stderr_sha256": digest(error),
            }
        )
        dump(Path("commands.json"), receipts)
        if code != expected:
            raise ValueError(f"unexpected exit {code}: {command + argv}")
        return (
            json.loads(stdout.getvalue())
            if artifact.endswith(".json") and stdout.getvalue()
            else None
        )

    try:
        os.chdir(out)
        run(["--out", "generated"], "stages/generation.json", collection=True)
        summary = {
            "profile": "moenv-workflow/1",
            "python": platform.python_version(),
            "software": version("ghg-assurance-graph"),
            "created_at": STAMP,
            "network": "Python socket guard; not an OS sandbox",
            "years": {},
            "scope": "Fictional MOENV-inspired internal evidence; not statutory filing or assurance",
        }
        for year in (2023, 2024):
            source = f"generated/{year}"
            base = f"stages/{year}"
            checked = run(["--check", source], f"{base}/collection-check.json", collection=True)
            validation = run(["validate", source + "/package.json"], f"{base}/validation.json")
            if not validation["conforms"] or checked["activity_rows"] != 60:
                raise ValueError("MOENV input/graph validation did not pass")
            run(["graph", "build", source], f"{base}/graph.ttl")
            package = json.loads(Path(source, "package.json").read_text())
            results = [r for r in package["records"] if r["kind"] == "EmissionResult"]
            for result in results:
                name = result["label"].removesuffix("-result")
                explained = run(
                    ["graph", "explain", result["id"], "--input", source],
                    f"{base}/explain/{name}.json",
                )
                if not explained:
                    raise ValueError("lineage explanation is empty")
            unreviewed = run(
                ["graph", "query", "unreviewed_results", "--input", source],
                f"{base}/unreviewed.json",
            )
            if len(unreviewed) != len(results):
                raise ValueError("unreviewed result count mismatch")
            prefix = f"urn:ghgag:moenv-demo-{year}-electricity"
            run(
                [
                    "graph",
                    "query",
                    "results_using_factor",
                    "--target",
                    prefix + "-factor:v1",
                    "--input",
                    source,
                ],
                f"{base}/factor-use.json",
            )
            run(
                [
                    "graph",
                    "query",
                    "records_supported_by_evidence",
                    "--target",
                    prefix + "-activity-evidence:v1",
                    "--input",
                    source,
                ],
                f"{base}/evidence-use.json",
            )
            run(
                ["export", "json-ld", f"{base}/graph.jsonld", "--input", source],
                f"{base}/export-jsonld.json",
            )
            crate = f"packages/{year}"
            run(
                [
                    "package",
                    "create",
                    source,
                    "--out",
                    crate,
                    "--created-at",
                    STAMP,
                    "--data-version",
                    f"moenv-training-1-{year}",
                ],
                f"{base}/package-create.json",
            )
            verified = run(["package", "verify", crate], f"{base}/package-verify.json")
            if not verified["valid"]:
                raise ValueError("crate verification failed")
            vault = f"vaults/{year}"
            run(["export", "obsidian", vault, "--input", source], f"{base}/obsidian.json")
            notes = list(Path(vault).glob("*.md"))
            for note in notes:
                for target in re.findall(r"\[\[([^]\n]+)\]\]", note.read_text()):
                    if not Path(vault, target + ".md").is_file():
                        raise ValueError("broken generated wikilink")
            amounts = {
                r["label"].removesuffix("-result"): str(r["quantity"]["value"]) for r in results
            }
            total = sum(Fraction(v) for v in amounts.values())
            expected = Fraction("95797.473564" if year == 2023 else "95229.409244")
            if total != expected or total != Fraction(checked["total_kg_co2e"]):
                raise ValueError("independent literal total oracle failed")
            summary["years"][str(year)] = {
                "total_kg_co2e": checked["total_kg_co2e"],
                "source_amounts_kg_co2e": amounts,
                "results": len(results),
                "activity_rows": checked["activity_rows"],
                "monthly_documents": 60,
                "evidence_documents": len(list(Path(source, "evidence").glob("*.json"))),
                "canonical_records": len(package["records"]),
                "unreviewed_results": len(unreviewed),
                "lineage_explanations": len(results),
                "package_valid": verified["valid"],
                "vault_notes": len(notes),
            }
        before, after = summary["years"]["2023"], summary["years"]["2024"]
        comparison = {
            "profile": "moenv-arithmetic-comparison/1",
            "causality": "UNKNOWN",
            "not_carbon_diff": True,
            "delta_kg_co2e": "-568.0643200",
            "sources": [],
        }
        for source in sorted(
            set(before["source_amounts_kg_co2e"]) | set(after["source_amounts_kg_co2e"])
        ):
            # A zero predecessor is permitted only for the explicitly declared new
            # generator. Missing arbitrary sources are not silently zero-filled.
            if source not in before["source_amounts_kg_co2e"] and source != "new-generator":
                raise ValueError("unexplained missing source")
            a = Fraction(before["source_amounts_kg_co2e"].get(source, "0"))
            b = Fraction(after["source_amounts_kg_co2e"][source])
            comparison["sources"].append(
                {
                    "source": source,
                    "before": str(a),
                    "after": str(b),
                    "delta": str(b - a),
                    "causality": "UNKNOWN",
                }
            )
        if sum(Fraction(r["delta"]) for r in comparison["sources"]) != Fraction(
            comparison["delta_kg_co2e"]
        ):
            raise ValueError("comparison does not reconcile")
        dump(Path("comparison.json"), comparison)
        # Three deliberate failure paths, separated from valid packages and inputs.
        negative = Path("negative/missing-month")
        shutil.copytree("generated/2024", negative)
        activity = negative / "04-activity.csv"
        lines = activity.read_text().splitlines(keepends=True)
        activity.write_text("".join(lines[:1] + lines[2:]))
        run(
            ["--check", str(negative)],
            "negative/missing-month-check.json",
            collection=True,
            expected=2,
        )
        shutil.copytree("packages/2024", "negative/tampered-crate")
        Path("negative/tampered-crate/extra.txt").write_text("synthetic tampering control\n")
        run(
            ["package", "verify", "negative/tampered-crate"],
            "negative/tampered-crate-check.json",
            expected=2,
        )
        run(
            ["diff", "generated/2023", "generated/2024"],
            "negative/unsupported-carbondiff.json",
            expected=2,
        )
        summary["commands"] = len(receipts)
        summary["negative_controls"] = {
            "missing_month": 2,
            "tampered_crate": 2,
            "unsupported_carbon_diff": 2,
        }
        summary["comparison"] = comparison
        dump(Path("summary.json"), summary)
        lines = [
            "# MOENV 2023/2024 executed workflow",
            "",
            summary["scope"],
            "",
            "Source documents, quantities, LHV and review roles are synthetic. Factor sources and historical electricity policy remain explicit in the repository source ledger.",
            "",
            "| Year | kgCO2e | Results / lineages | Unreviewed | Crate verified | Vault notes |",
            "|---|---:|---:|---:|---|---:|",
        ]
        for year, row in summary["years"].items():
            lines.append(
                f"| {year} | {row['total_kg_co2e']} | {row['results']} | {row['unreviewed_results']} | {row['package_valid']} | {row['vault_notes']} |"
            )
        lines += [
            "",
            "## Inspect in order",
            "",
            "1. generated/YEAR/04-activity.csv and evidence/: monthly originals and hashes.",
            "2. generated/YEAR/05-quantification.csv: gas arithmetic; synthetic LHV and historical factor policy.",
            "3. stages/YEAR/collection-check.json and validation.json: separate collection and graph checks.",
            "4. stages/YEAR/explain/: actual lineage queries; unreviewed.json preserves pending review.",
            "5. comparison.json: arithmetic delta -568.064320 kgCO2e, all causal explanations UNKNOWN; not CarbonDiff.",
            "6. packages/YEAR/: verified canonical RO-Crates; monthly source files remain in generated/, not inside these closed-profile crates.",
            "7. vaults/YEAR/: graph-derived Markdown, not authenticated review or tested desktop Obsidian behavior.",
            "",
            "## Failure controls",
            "",
            "Missing month exits 2; added crate file exits 2; unsupported ghgag diff on MOENV folders exits 2.",
            "No fixture was rewritten to manufacture a passing comparison.",
            "",
            f"commands.json contains {len(receipts)} real in-process CLI invocations and terminal exit receipts.",
            "Copy the entire output directory, not only packages/, to preserve the monthly evidence chain.",
            "manifest.json covers every output file except itself; retain its digest independently.",
            "",
        ]
        Path("REPORT.md").write_text("\n".join(lines))
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
    parser.add_argument(
        "--python", help="Use a separate installed Python without checkout path injection"
    )
    args = parser.parse_args()
    if args.python:
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
        parser.exit(2, f"MOENV workflow failed: {exc}\n")


if __name__ == "__main__":
    main()
