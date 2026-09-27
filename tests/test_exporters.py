"""Serialization and filesystem/link oracles independent of exporter implementation."""

import json
import re
from pathlib import Path

import pytest
from rdflib import BNode, Graph, Literal, URIRef
from rdflib.compare import isomorphic

from ghg_assurance_graph.exporters import canonical_json, export_graph, export_obsidian
from ghg_assurance_graph.models import EvidencePackage
from ghg_assurance_graph.serialization import to_graph


@pytest.fixture
def package():
    return EvidencePackage.model_validate_json(
        (Path(__file__).parents[1] / "benchmark/generated/2025-v1/package.json").read_text()
    )


def test_canonical_json(package):
    assert canonical_json(package) == canonical_json(
        package.model_copy(update={"records": tuple(reversed(package.records))})
    )
    assert EvidencePackage.model_validate_json(canonical_json(package))
    with pytest.raises(ValueError):
        canonical_json({"bad": float("nan")})


@pytest.mark.parametrize("format", ["turtle", "json-ld"])
def test_roundtrip_and_order(package, format):
    graph = to_graph(package)
    reverse = Graph()
    for triple in reversed(list(graph)):
        reverse.add(triple)
    data = export_graph(graph, format)
    assert data == export_graph(reverse, format)
    assert isomorphic(graph, Graph().parse(data=data, format=format))
    if format == "json-ld":
        assert "@context" not in data
        assert isinstance(json.loads(data), list)


def test_blank_node_identity_independent():
    graphs = []
    for name in ("one", "two"):
        graph = Graph()
        graph.add((URIRef("urn:s"), URIRef("urn:p"), BNode(name)))
        graph.add((BNode(name), URIRef("urn:p"), Literal("x")))
        graphs.append(graph)
    for format in ("turtle", "json-ld"):
        assert export_graph(graphs[0], format) == export_graph(graphs[1], format)


def test_vault_no_dangling_deterministic_safe(package, tmp_path):
    graph = to_graph(package)
    graph.add((URIRef("urn:../../bad"), URIRef("urn:p"), Literal("[[missing]] <script>x</script>")))
    one = export_obsidian(graph, tmp_path / "one")
    two = export_obsidian(graph, tmp_path / "two")
    expected = {p.name for p in one.iterdir()}
    assert expected == {p.name for p in two.iterdir()}
    links = []
    for p in one.iterdir():
        assert p.name == "index.md" or re.fullmatch(r"node-[0-9a-f]{64}\.md", p.name)
        text = p.read_text()
        assert text.startswith("---\n")
        assert text == (two / p.name).read_text()
        assert "<script>" not in text and "[[missing]]" not in text
        links.extend(re.findall(r"\[\[([^\]]+)\]\]", text))
    assert links and all(link + ".md" in expected for link in links)
    assert len(re.findall(r"\[\[", (one / "index.md").read_text())) == len(expected) - 1
    with pytest.raises(FileExistsError):
        export_obsidian(graph, one)
    link = tmp_path / "link"
    link.symlink_to(one, target_is_directory=True)
    with pytest.raises(ValueError):
        export_obsidian(graph, link / "child")


def test_unsupported_format(package):
    with pytest.raises(ValueError):
        export_graph(package, "xml")
