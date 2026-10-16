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
    import hashlib
    import json
    from fractions import Fraction

    root = Path(__file__).parents[1]
    source = (root / "paper/softwarex/MANUSCRIPT.md").read_text()
    for retired in ("UMC", "TSMC", "207 output", "144 not-assessable"):
        assert retired not in source
    assert "0.4.0a1" in source
    assert "Validation is synthetic-only" in source
    assert "scripts/run_moenv_example.py" in source
    assert "legacy CarbonDiff" in source
    table = source.split("| Source |", 1)[1].split("\n\n", 1)[0]
    cells = [line.strip("|").split("|") for line in table.splitlines()[2:]]
    assert len(cells) == 6
    literal = {
        "2023": ["27270.87138", "1493.402184", "0", "3900", "63133.2"],
        "2024": ["24710.22618", "1332.821304", "321.16176", "2600", "66265.2"],
    }
    for column, year in enumerate(("2023", "2024"), 1):
        amounts = [Fraction(row[column].strip()) for row in cells[:-1]]
        assert amounts == [Fraction(x) for x in literal[year]]
        assert sum(amounts) == Fraction(cells[-1][column].strip())
    data = json.loads((root / "paper/softwarex/figures/moenv-evaluation.json").read_text())
    summary = root / "examples/moenv_training/workflow/summary.json"
    assert data["summary_sha256"] == hashlib.sha256(summary.read_bytes()).hexdigest()
    assert data["counts"] == [120, 122, 9, 9, 2, 33]
    svg = (root / "paper/softwarex/figures/moenv-evaluation.svg").read_text()
    assert ElementTree.fromstring(svg).tag == "{http://www.w3.org/2000/svg}svg"
    assert "95,797.473564" in svg and "95,229.409244" in svg


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
