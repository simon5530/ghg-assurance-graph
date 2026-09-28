"""Historical v0.3.0a1 baseline only: reproduce pinned released assets, not current code."""

import argparse
import hashlib
import json
import os
import platform
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

REPO = "simon5530/ghg-assurance-graph"
TAG = "v0.3.0a1"
ASSETS = {
    "ghg-assurance-graph-v0.3.0a1-source.tar.gz": (
        270929,
        "5ff2de31aea494c1af95f5dcd088aaf0e8cdbafe84cbf55754cc60527107c69a",
    ),
    "ghg_assurance_graph-0.3.0a1-py3-none-any.whl": (
        47285,
        "de5d823dbf906cd47a406f950f3b7ecea5cb76d197da14e3d281a1cd5124ffb4",
    ),
    "ghgag-0.3.0a1-public-company-full-run.tar.gz": (
        50452,
        "8ac04b1f82ae2e38480f6dd9dfea7a493c98d6ce528d14701f36d92104beaa0e",
    ),
}
CASES = {
    "umc": ("umc_group_2022_2024.json", 7, 12, 41),
    "umc-parent": ("umc_parent_2022_2024.json", 9, 10, 57),
    "tsmc": ("tsmc_heldout_2023_2024.json", 8, 11, 46),
}


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree(path):
    return {
        p.relative_to(path).as_posix(): digest(p) for p in sorted(path.rglob("*")) if p.is_file()
    }


def extract(archive, destination):
    with tarfile.open(archive) as tar:
        require(
            all(m.isfile() or m.isdir() for m in tar.getmembers()),
            "Archive links/special files forbidden",
        )
        tar.extractall(destination, filter="data")


def check_metrics(data):
    require(data["benchmark"] == "0.1", "benchmark identity")
    require(
        data["clean_finding_counts"] == dict.fromkeys(("2025-v1", "2025-v2", "2026-v1"), 0),
        "clean finding counts",
    )
    metrics = data["validation"]
    for part, count in [
        (metrics, 10),
        (metrics["by_split"]["development"], 6),
        (metrics["by_split"]["holdout"], 4),
    ]:
        for key, expected in {
            "tp": count,
            "fp": 0,
            "fn": 0,
            "precision": 1,
            "recall": 1,
            "f1": 1,
        }.items():
            require(part[key] == expected, f"metric {key}: {part[key]}")
    fields = (
        "total_before",
        "total_after",
        "delta",
        "attributed_kg_co2e",
        "residual_kg_co2e",
        "absolute_unknown_kg_co2e",
    )
    rows = data["carbondiff_unassisted"]
    require(len(rows) == 2, "comparison count")
    for row, expected in zip(
        rows, [(3820, 3850, 30, 20, 10, 10), (3850, 4060, 210, -90, 300, 500)], strict=True
    ):
        require(tuple(Decimal(row[k]) for k in fields) == expected, "CarbonDiff metrics")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report-dir", type=Path, required=True)
    args = parser.parse_args()
    report_dir = args.report_dir.resolve()
    report_dir.mkdir(parents=True, exist_ok=False)
    work = Path(tempfile.mkdtemp(prefix="ghgag-release-"))
    env = os.environ.copy()
    for key in ("PYTHONPATH", "PYTHONHOME", "VIRTUAL_ENV", "UV_PROJECT_ENVIRONMENT"):
        env.pop(key, None)
    env.update(
        UV_NO_CACHE="1", PIP_NO_CACHE_DIR="1", PYTHONNOUSERSITE="1", UV_PYTHON_DOWNLOADS="never"
    )
    report = {
        "status": "running",
        "release": TAG,
        "repository": REPO,
        "started_at": datetime.now(UTC).isoformat(),
        "platform": platform.platform(),
        "python": sys.version,
        "harness_sha256": digest(Path(__file__)),
        "runner": {
            k: os.environ.get(k)
            for k in (
                "RUNNER_OS",
                "RUNNER_ARCH",
                "RUNNER_ENVIRONMENT",
                "ImageOS",
                "ImageVersion",
                "GITHUB_RUN_ID",
                "GITHUB_RUN_ATTEMPT",
                "GITHUB_SHA",
                "GITHUB_REPOSITORY",
            )
        },
        "cache": "disabled; new temporary root and separate virtual environments",
        "commands": [],
        "assets": [],
        "checks": {},
    }

    def save():
        (report_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n")

    def run(argv, cwd=work):
        argv = list(map(str, argv))
        index = len(report["commands"])
        entry = {"argv": argv, "shell_display": shlex.join(argv), "cwd": str(cwd)}
        report["commands"].append(entry)
        save()
        result = subprocess.run(argv, cwd=cwd, env=env, text=True, capture_output=True, check=False)
        (report_dir / f"command-{index:02d}.stdout").write_text(result.stdout)
        (report_dir / f"command-{index:02d}.stderr").write_text(result.stderr)
        entry["exit_code"] = result.returncode
        save()
        print(f"[{index}] {entry['shell_display']} -> {result.returncode}", flush=True)
        require(result.returncode == 0, f"command {index} failed; see archived logs")
        return result.stdout

    try:
        require(sys.version_info[:2] == (3, 12), "Python 3.12 required")
        run(["gh", "--version"])
        metadata = json.loads(run(["gh", "api", f"repos/{REPO}/releases/tags/{TAG}"]))
        (report_dir / "release.json").write_text(json.dumps(metadata, indent=2) + "\n")
        require(not metadata["draft"] and metadata["tag_name"] == TAG, "published release")
        remote = {a["name"]: a for a in metadata["assets"]}
        downloads = work / "downloads"
        downloads.mkdir()
        for name, (size, sha) in ASSETS.items():
            asset = remote[name]
            url = f"https://github.com/{REPO}/releases/download/{TAG}/{name}"
            require(
                asset["browser_download_url"] == url and asset["size"] == size,
                f"release asset identity: {name}",
            )
            require(asset.get("digest") == f"sha256:{sha}", f"remote digest: {name}")
            run(
                [
                    "gh",
                    "release",
                    "download",
                    TAG,
                    "--repo",
                    REPO,
                    "--pattern",
                    name,
                    "--dir",
                    downloads,
                ]
            )
            path = downloads / name
            require(path.stat().st_size == size and digest(path) == sha, f"download digest: {name}")
            report["assets"].append(
                {"name": name, "url": url, "asset_id": asset["id"], "bytes": size, "sha256": sha}
            )
            save()
        names = list(ASSETS)
        extract(downloads / names[0], work / "source")
        extract(downloads / names[2], work / "expected")
        source = work / "source/ghg-assurance-graph-0.3.0a1"
        expected = work / "expected/full_run"
        report["source_tree_sha256"] = tree(source)
        expected_tree = tree(expected)
        require(len(expected_tree) == 207, "published output file count")
        # Bootstrap tooling only, never the application, from the package index.
        bootstrap = work / "bootstrap"
        run([sys.executable, "-m", "venv", bootstrap])
        bootpy = bootstrap / "bin/python"
        run([bootpy, "-m", "pip", "install", "--no-cache-dir", "uv==0.12.19"])
        uv = bootstrap / "bin/uv"
        run([uv, "--version"])
        requirements = work / "requirements.txt"
        requirements.write_text(
            run(
                [
                    uv,
                    "export",
                    "--locked",
                    "--no-dev",
                    "--no-emit-project",
                    "--format",
                    "requirements-txt",
                ],
                source,
            )
        )
        shutil.copy2(requirements, report_dir / "requirements.txt")
        for mode in ("source", "wheel"):
            venv = work / f"{mode}-venv"
            run([uv, "venv", "--python", sys.executable, venv])
            python = venv / "bin/python"
            run([uv, "pip", "sync", "--python", python, "--require-hashes", requirements])
            target = source if mode == "source" else downloads / names[1]
            run([uv, "pip", "install", "--python", python, "--no-deps", target])
            identity = json.loads(
                run(
                    [
                        python,
                        "-I",
                        "-c",
                        (
                            "import json,sys,importlib.metadata as m,ghg_assurance_graph as g; "
                            "print(json.dumps(dict(version=m.version('ghg-assurance-graph'),"
                            "module=g.__file__,prefix=sys.prefix)))"
                        ),
                    ]
                )
            )
            require(identity["version"] == "0.3.0a1", "installed version")
            require(Path(identity["module"]).is_relative_to(venv), "installed import isolation")
            report["checks"][mode] = {"distribution": identity}
            freeze = run([uv, "pip", "freeze", "--python", python])
            (report_dir / f"{mode}-freeze.txt").write_text(freeze)
            if mode == "source":
                devreq = work / "dev-requirements.txt"
                devreq.write_text(
                    run(
                        [
                            uv,
                            "export",
                            "--locked",
                            "--no-emit-project",
                            "--format",
                            "requirements-txt",
                        ],
                        source,
                    )
                )
                shutil.copy2(devreq, report_dir / "dev-requirements.txt")
                run([uv, "pip", "install", "--python", python, "--require-hashes", "-r", devreq])
                run(
                    [
                        python,
                        "-I",
                        "-m",
                        "pytest",
                        "-q",
                        source / "tests",
                        f"--junitxml={report_dir / 'tests.xml'}",
                    ],
                    source,
                )
                report["checks"][mode]["tests"] = "passed"
            output = report_dir / mode
            output.mkdir()
            generated = output / "benchmark"
            metrics = json.loads(
                run(
                    [
                        venv / "bin/ghgag",
                        "benchmark",
                        "run",
                        "--out",
                        generated,
                        "--truth",
                        source / "benchmark/ground_truth",
                    ]
                )
            )
            check_metrics(metrics)
            require(
                tree(generated) == tree(source / "benchmark/generated"),
                "benchmark full tree byte identity",
            )
            (output / "benchmark-metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
            full = output / "full_run"
            for case, (filename, assertions, assessed, unavailable) in CASES.items():
                run(
                    [
                        python,
                        "-I",
                        source / "scripts/run_public_case.py",
                        source / "examples/public_companies" / filename,
                        "--out",
                        full / case,
                    ]
                )
                summary = json.loads((full / case / "summary.json").read_text())
                require(
                    summary["assertions"] == assertions
                    and summary["software"] == "0.3.0a1"
                    and summary["check_status_counts"]
                    == {"assessed": assessed, "not_assessable": unavailable}
                    and summary["validation_status"] == "not_assessable"
                    and summary["package_valid"] is True
                    and summary["causality"] == "UNKNOWN"
                    and summary["upstream_recalculation_available"] == 0,
                    f"public dataset numerical/identity contract: {case}",
                )
            actual = tree(full)
            require(actual == expected_tree, f"{mode}: all 207 output file bytes must match")
            report["checks"][mode].update(
                benchmark="passed", public_outputs="207 byte-identical files", output_sha256=actual
            )
            save()
        report["status"] = "passed"
    except BaseException as exc:
        report["status"] = "failed"
        report["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        report["finished_at"] = datetime.now(UTC).isoformat()
        save()
        # Temporary environments stay outside the archived artifact; hosted job disposes them.
        print(f"Report: {report_dir / 'report.json'}", flush=True)


if __name__ == "__main__":
    main()
