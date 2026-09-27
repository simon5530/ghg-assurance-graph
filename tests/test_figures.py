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
