"""Published figure is generated from current executable evidence."""

import importlib.util
from pathlib import Path
from xml.etree import ElementTree


def test_published_figure_is_reproducible():
    root = Path(__file__).parents[1]
    spec = importlib.util.spec_from_file_location(
        "render_figures", root / "scripts/render_figures.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    actual = module.render()
    assert actual == (root / "paper/softwarex/figures/evaluation.svg").read_text()
    assert ElementTree.fromstring(actual).tag == "{http://www.w3.org/2000/svg}svg"
    assert "TP=10, FP=0, FN=0" in actual
    assert "signed UNKNOWN 300.00" in actual


def test_manuscript_synthetic_table_and_scope():
    import json
    from decimal import Decimal

    root = Path(__file__).parents[1]
    source = (root / "paper/softwarex/MANUSCRIPT.md").read_text()
    for retired in ("UMC", "TSMC", "207 output", "144 not-assessable"):
        assert retired not in source
    assert "0.4.0a1" in source
    assert "Validation is synthetic-only" in source
    table = source.split("| Source |", 1)[1].split("\n\n", 1)[0]
    cells = [line.strip("|").split("|") for line in table.splitlines()[2:]]
    assert len(cells) == 16
    truth = json.loads((root / "benchmark/ground_truth/expected_amounts.json").read_text())
    for column, version in enumerate(("2025-v1", "2025-v2", "2026-v1"), 1):
        amounts = [Decimal(row[column].strip()) for row in cells[:-1]]
        assert amounts == truth["kg_co2e"][version]
        assert sum(amounts) == Decimal(cells[-1][column].strip())
    assert "| Partial total | 3820 | 3850 | 4060 |" in source


def test_architecture_and_html_are_reproducible():
    root = Path(__file__).parents[1]
    spec = importlib.util.spec_from_file_location(
        "render_manuscript", root / "scripts/render_manuscript.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    paper = root / "paper/softwarex"
    assert module.architecture() == (paper / "figures/architecture.svg").read_text()
    assert (
        module.render((paper / "MANUSCRIPT.md").read_text())
        == (paper / "MANUSCRIPT.html").read_text()
    )
