"""Installed-style offline CLI workflow and rejection behavior."""

import json
from pathlib import Path

import pytest

from ghg_assurance_graph.cli import main

ROOT = Path(__file__).resolve().parents[1]


def test_pipeline(tmp_path, capsys):
    generated = tmp_path / "generated"
    main(
        [
            "benchmark",
            "run",
            "--out",
            str(generated),
            "--truth",
            str(ROOT / "benchmark/ground_truth"),
        ]
    )
    metrics = json.loads(capsys.readouterr().out)
    assert metrics["validation"]["tp"] == 10
    assert metrics["validation"]["fp"] == metrics["validation"]["fn"] == 0
    assert list(metrics["clean_finding_counts"].values()) == [0, 0, 0]
    latest = generated / "2026-v1"
    main(["graph", "build", str(latest)])
    assert "wasGeneratedBy" in capsys.readouterr().out
    main(["validate", str(latest)])
    assert json.loads(capsys.readouterr().out)["conforms"]
    main(["diff", str(generated / "2025-v2"), str(latest)])
    report = json.loads(capsys.readouterr().out)
    assert report["delta"] == "210.00"
    assert report["residual_kg_co2e"] == "300.00"
    crate = tmp_path / "crate"
    main(
        [
            "package",
            "create",
            str(latest),
            "--out",
            str(crate),
            "--created-at",
            "2026-09-28T00:00:00Z",
            "--data-version",
            "acme-0.1-2026-v1",
        ]
    )
    capsys.readouterr()
    main(["package", "verify", str(crate)])
    capsys.readouterr()
    main(["export", "obsidian", str(tmp_path / "vault"), "--input", str(latest)])
    assert (tmp_path / "vault" / "index.md").exists() or (tmp_path / "vault" / "Index.md").exists()
    capsys.readouterr()
    with pytest.raises(SystemExit) as error:
        main(["validate", str(generated / "defects/double-gwp.json")])
    assert error.value.code == 1
    assert not json.loads(capsys.readouterr().out)["conforms"]


def test_private_paths_not_logged(capsys):
    with pytest.raises(SystemExit) as error:
        main(["validate", "/private-example/not-present.json"])
    assert error.value.code == 2
    assert "private-example" not in capsys.readouterr().err
