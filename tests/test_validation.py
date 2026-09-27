"""Independent published fixtures + adversarial validation oracles."""

import json
from copy import deepcopy
from importlib.resources import files
from pathlib import Path

import pytest
from rdflib import RDF, Graph, Literal, URIRef
from rdflib.namespace import OWL, PROV, SH

from ghg_assurance_graph.models import EvidencePackage
from ghg_assurance_graph.serialization import to_graph
from ghg_assurance_graph.validation import (
    Finding,
    evaluate_findings,
    validate_graph,
    validate_package,
    validate_rows,
)

ROOT = Path(__file__).resolve().parents[1] / "benchmark"


def load(path):
    return json.loads((ROOT / path).read_text())


@pytest.mark.parametrize("version", ["2025-v1", "2025-v2", "2026-v1"])
def test_clean(version):
    assert validate_rows(load(f"generated/{version}/inputs.json")) == ()
    package = EvidencePackage.model_validate(load(f"generated/{version}/package.json"))
    assert validate_package(package) == ()


def test_independent_truth_metrics():
    # Only row payloads enter detector; truth and revealing case paths remain in evaluator.
    predictions = {
        path.stem: validate_rows(json.loads(path.read_text())["rows"])
        for path in sorted((ROOT / "generated/defects").glob("*.json"))
    }
    truth = load("ground_truth/expected_findings.json")["findings"]
    result = evaluate_findings(predictions, truth)
    assert (result["tp"], result["fp"], result["fn"]) == (10, 0, 0)
    assert (result["precision"], result["recall"], result["f1"]) == (1, 1, 1)
    for split, count in (("development", 6), ("holdout", 4)):
        labels = [r for r in truth if r["split"] == split]
        cases = {r["case_id"] for r in labels}
        metrics = evaluate_findings({k: v for k, v in predictions.items() if k in cases}, labels)
        assert (metrics["tp"], metrics["fp"], metrics["fn"], metrics["f1"]) == (count, 0, 0, 1)


def test_metric_oracle_penalizes_wrong_entity_rule_severity_and_missing():
    truth = [
        {"case_id": "c", "entity": "e", "rule": "r", "severity": "error"},
        {"case_id": "c", "entity": "f", "rule": "r", "severity": "error"},
    ]
    result = evaluate_findings({"c": [Finding("e", "r"), Finding("other", "r")]}, truth)
    assert (result["tp"], result["fp"], result["fn"]) == (1, 1, 1)
    assert result["precision"] == result["recall"] == result["f1"] == 0.5
    for finding in (Finding("wrong", "r"), Finding("e", "wrong"), Finding("e", "r", "warning")):
        assert evaluate_findings({"c": [finding]}, truth)["tp"] == 0
    assert evaluate_findings({}, truth)["fn"] == 2
    assert evaluate_findings({}, [])["f1"] == 0


@pytest.mark.parametrize(
    "field,value,rule",
    [
        ("factor_source", "plausible but wrong source", "factor provenance"),
        ("evidence", "synthetic://acme/20250926/2025-v1/other", "activity evidence"),
        ("activity", "NaN", "invalid amount or allocation"),
        ("activity", "Infinity", "invalid amount or allocation"),
        ("activity", "-1", "invalid amount or allocation"),
        ("activity", True, "invalid amount or allocation"),
        ("allocation_share", "1.1", "invalid amount or allocation"),
        ("factor_unit", "USD", "unsupported unit conversion"),
        ("apply_gwp", "false", "no double GWP"),
        ("reported_kg_co2e", "499.999999999", "reported amount mismatch"),
    ],
)
def test_adversarial_rows(field, value, rule):
    row = load("generated/2025-v1/inputs.json")[0]
    row[field] = value
    assert rule in {f.rule for f in validate_rows([row])}


@pytest.mark.parametrize("field", ["factor_source", "activity", "evidence", "unit", "review"])
def test_missing_fields(field):
    row = load("generated/2025-v1/inputs.json")[0]
    del row[field]
    assert validate_rows([row])


def test_numeric_conversion_allocation_and_duplicate_identity():
    row = next(r for r in load("generated/2025-v1/inputs.json") if r["id"] == "materials")
    row.update(unit="tonne", activity="0.1")
    assert validate_rows([row]) == ()  # 0.1 tonne * 1000 kg/t * 4 = 400
    row.update(allocation_share="0.25", allocation_method="mass-share", reported_kg_co2e="100")
    assert validate_rows([row]) == ()
    row["reported_kg_co2e"] = "25"  # forbidden second allocation
    assert "reported amount mismatch" in {f.rule for f in validate_rows([row])}
    other = deepcopy(row)
    other["activity"] = "0.2"
    assert "duplicate activity" in {f.rule for f in validate_rows([row, other])}
    assert validate_rows([])


@pytest.mark.parametrize("mutation", ["missing", "wrong-type", "duplicate", "dangling"])
def test_real_shacl_provenance(mutation):
    package = EvidencePackage.model_validate(load("generated/2025-v1/package.json"))
    graph = to_graph(package)
    factor = URIRef("urn:ghgag:acme-2025-v1-electricity-factor:v1")
    original = graph.value(factor, PROV.wasDerivedFrom)
    if mutation != "duplicate":
        graph.remove((factor, PROV.wasDerivedFrom, original))
    replacement = {
        "wrong-type": URIRef("urn:ghgag:acme-2025-v1-org:v1"),
        "duplicate": URIRef("urn:ghgag:acme-2025-v1-fleet-evidence:v1"),
        "dangling": URIRef("urn:ghgag:missing:v1"),
    }.get(mutation)
    if replacement:
        graph.add((factor, PROV.wasDerivedFrom, replacement))
    before = set(graph)
    findings = validate_graph(graph)
    assert any(
        f.target == str(factor) and f.rule == "shacl:EmissionFactor-wasDerivedFrom"
        for f in findings
    )
    assert findings == validate_graph(graph)
    assert [f.id for f in findings] == [f.id for f in validate_graph(graph)]
    assert set(graph) == before


def test_offline_shapes_not_data_supplied_code(monkeypatch):
    import socket

    def forbidden(*args, **kwargs):
        raise AssertionError("network access")

    monkeypatch.setattr(socket, "create_connection", forbidden)
    graph = Graph()
    node = URIRef("urn:untrusted")
    graph.add((node, OWL.imports, URIRef("https://example.invalid/ontology")))
    graph.add((node, SH.sparql, Literal("SERVICE <https://example.invalid/> {}")))
    assert validate_graph(graph) == ()
    with pytest.raises(TypeError):
        validate_graph("https://example.invalid/data")
    shapes = Graph().parse(
        data=files("ghg_assurance_graph").joinpath("shapes/core.ttl").read_text(), format="turtle"
    )
    assert list(shapes.subjects(RDF.type, SH.NodeShape))
    assert not list(shapes.triples((None, SH.sparql, None)))


def test_stable_row_findings_and_serialization():
    rows = load("generated/defects/wrong-factor-year.json")["rows"]
    assert validate_rows(rows) == validate_rows(reversed(rows))
    finding = validate_rows(rows)[0]
    assert finding.to_dict()["id"] == finding.id
    assert finding.id.startswith("urn:ghgag:finding-")


def test_exact_conversion_independent_of_decimal_context():
    from decimal import localcontext

    row = load("generated/2025-v1/inputs.json")[0]
    row.update(unit="MJ", factor_unit="kWh", activity="3.6", factor="1", reported_kg_co2e="1")
    with localcontext() as ctx:
        ctx.prec = 2
        assert validate_rows([row]) == ()
        row.update(
            unit="kWh", activity="0.123456789123456789", reported_kg_co2e="0.123456789123456789"
        )
        assert validate_rows([row]) == ()
        row["reported_kg_co2e"] = "0.12"
        assert "reported amount mismatch" in {f.rule for f in validate_rows([row])}


@pytest.mark.parametrize("value", [None, [], {}, True, "1e999999", "9" * 61])
def test_unseen_malformed_numeric_inputs(value):
    row = load("generated/2025-v1/inputs.json")[0]
    row["factor"] = value
    assert "invalid amount or allocation" in {f.rule for f in validate_rows([row])}


@pytest.mark.parametrize("value", [None, [], {}, True])
def test_arbitrary_malformed_metadata_is_a_finding(value):
    row = load("generated/2025-v1/inputs.json")[0]
    for field in ("facility", "unit", "scope", "factor_year", "method", "id"):
        changed = dict(row, **{field: value})
        assert validate_rows([changed])


@pytest.mark.parametrize(
    "kind,field",
    [
        ("factor", "version"),
        ("factor", "numerator"),
        ("factor", "denominator"),
        ("review", "status"),
        ("review", "timestamp"),
    ],
)
def test_raw_graph_required_literals_not_only_model_validation(kind, field):
    from ghg_assurance_graph.serialization import GHG

    package = EvidencePackage.model_validate(load("generated/2025-v1/package.json"))
    graph = to_graph(package)
    node = URIRef(f"urn:ghgag:acme-2025-v1-electricity-{kind}:v1")
    assert graph.value(node, GHG[field]) is not None
    graph.remove((node, GHG[field], None))
    assert any(f.target == str(node) for f in validate_graph(graph))
