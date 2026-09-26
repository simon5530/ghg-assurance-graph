"""Independent assertions of the declared contract, not assurance evaluation."""

import importlib.util
import json
from pathlib import Path

import jsonschema
import pint
import pytest
from pydantic import ValidationError
from rdflib import RDF, Graph, URIRef
from rdflib.compare import isomorphic
from rdflib.namespace import PROV

from ghg_assurance_graph.models import EvidencePackage, Quantity
from ghg_assurance_graph.serialization import GHG, from_json, to_graph, to_json, to_rdf
from ghg_assurance_graph.units import Unit, convert

spec = importlib.util.spec_from_file_location(
    "examples", Path(__file__).parents[1] / "examples/hand_authored.py"
)
examples = importlib.util.module_from_spec(spec)
spec.loader.exec_module(examples)


@pytest.fixture
def data():
    return examples.example(examples.CASES[0]).model_dump(mode="json")


def node(data, kind):
    return next(r for r in data["records"] if r["kind"] == kind)


@pytest.mark.parametrize("case", examples.CASES, ids=lambda c: c["name"])
def test_examples_schema_and_roundtrip(case):
    package = examples.example(case)
    jsonschema.Draft202012Validator(EvidencePackage.model_json_schema()).validate(
        json.loads(to_json(package))
    )
    assert from_json(to_json(package)) == package
    # Hand-authored expected totals, not computed by production code.
    result = next(r for r in package.records if r.kind == "EmissionResult")
    assert result.quantity.value == case["result"]
    assert case["amount"] * case["factor"] == pytest.approx(case["result"])
    graph = to_graph(package)
    for format in ("turtle", "json-ld"):
        parsed = Graph().parse(data=to_rdf(package, format), format=format)
        assert isomorphic(graph, parsed)
    run = next(r for r in package.records if r.kind == "CalculationRun")
    assert (URIRef(result.id), PROV.wasGeneratedBy, URIRef(run.id)) in graph
    assert (URIRef(run.id), PROV.used, URIRef(run.factor)) in graph
    assert (URIRef(result.id), RDF.type, GHG.EmissionResult) in graph


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), -1, True, "1"])
def test_reject_bad_amount(value):
    with pytest.raises(ValidationError):
        Quantity(value=value, unit="kg")


def test_zero_and_units():
    assert Quantity(value=0, unit="kg").value == 0
    assert convert(1000, Unit.KG, Unit.TONNE) == 1
    assert convert(1, Unit.KWH, Unit.MJ) == pytest.approx(3.6)
    assert convert(1, Unit.T_CO2E, Unit.KG_CO2E) == 1000
    with pytest.raises(pint.DimensionalityError):
        convert(1, Unit.KG, Unit.KG_CO2E)
    for unit in ("unknown", "kg / second", "EUR"):
        with pytest.raises(ValidationError):
            Quantity(value=1, unit=unit)
    with pytest.raises(ValueError):
        convert(float("inf"), Unit.KG, Unit.KG)


@pytest.mark.parametrize(
    "kind,field,value",
    [
        ("ActivityRecord", "evidence", "urn:ghgag:missing:v1"),
        ("ActivityRecord", "evidence", "urn:ghgag:electricity-location-org:v1"),
        ("Organization", "id", "urn:ghgag:wrong:v1"),
        ("Organization", "version", True),
        ("Organization", "supersedes", "urn:ghgag:electricity-location-org:v1"),
        ("ReportingPeriod", "start", "2026-01-01"),
        ("EmissionSource", "scope", True),
        ("EmissionSource", "category", 1),
        ("EmissionSource", "scope2_basis", None),
        ("ReviewDecision", "timestamp", "2026-09-26T00:00:00"),
        ("EvidenceArtifact", "citation", "  "),
        ("EvidenceArtifact", "sha256", "pretend-hash"),
        ("EmissionFactor", "denominator", "kg"),
        ("EmissionFactor", "value", -1),
        ("EmissionResult", "quantity", {"value": 1, "unit": "kg"}),
        ("ActivityRecord", "quantity", {"value": 1, "unit": "kg_CO2e"}),
        ("ReviewDecision", "target", "urn:ghgag:electricity-location-org:v1"),
    ],
)
def test_invalid_fields(data, kind, field, value):
    node(data, kind)[field] = value
    with pytest.raises(ValidationError):
        EvidencePackage.model_validate(data)


def test_closed_schema_duplicate_and_schema_version(data):
    bad = json.loads(json.dumps(data))
    node(bad, "Organization")["bespoke"] = "not allowed"
    with pytest.raises(ValidationError):
        EvidencePackage.model_validate(bad)
    bad = dict(data, schema_version="0.2.0")
    with pytest.raises(ValidationError):
        EvidencePackage.model_validate(bad)
    data["records"].append(data["records"][0])
    with pytest.raises(ValidationError):
        EvidencePackage.model_validate(data)


def test_immutable_and_digest(data):
    package = EvidencePackage.model_validate(data)
    organization = package.records[0]
    with pytest.raises(ValidationError):
        organization.label = "changed"
    with pytest.raises(ValidationError):
        organization.model_copy(update={"version": 2})
    assert isinstance(package.records, tuple)
    assert organization.content_digest() == from_json(to_json(package)).records[0].content_digest()
    assert (
        organization.content_digest()
        != organization.model_copy(update={"label": "new"}).content_digest()
    )


def test_revision_chain_and_missing_predecessor():
    package = examples.example(examples.CASES[4])
    data = package.model_dump(mode="json")
    revisions = [r for r in data["records"] if r["kind"] == "ActivityRecord"]
    assert len(revisions) == 2
    assert revisions[1]["supersedes"] == revisions[0]["id"]
    data["records"].remove(revisions[0])
    with pytest.raises(ValidationError):
        EvidencePackage.model_validate(data)


@pytest.mark.parametrize(
    "mutation", ["boundary-org", "activity-org", "period", "method", "result-inventory"]
)
def test_cross_record_context(data, mutation):
    if mutation == "boundary-org":
        node(data, "BoundaryDefinition")["organization"] = node(data, "ReviewDecision")["reviewer"]
    elif mutation == "activity-org":
        node(data, "Facility")["organization"] = node(data, "ReviewDecision")["reviewer"]
    elif mutation == "period":
        old = node(data, "ReportingPeriod")
        new = dict(old, logical_id="urn:ghgag:short", id="urn:ghgag:short:v1", end="2025-06-30")
        data["records"].append(new)
        node(data, "EmissionFactor")["period"] = new["id"]
    elif mutation == "method":
        old = node(data, "CalculationMethod")
        new = dict(old, logical_id="urn:ghgag:other", id="urn:ghgag:other:v1")
        data["records"].append(new)
        node(data, "CalculationRun")["method"] = new["id"]
    else:
        old = node(data, "InventoryVersion")
        new = dict(old, logical_id="urn:ghgag:other", id="urn:ghgag:other:v1")
        data["records"].append(new)
        node(data, "EmissionResult")["inventory"] = new["id"]
    with pytest.raises(ValidationError):
        EvidencePackage.model_validate(data)


def test_all_classes_covered_and_no_unsupported_export():
    packages = [examples.example(case) for case in examples.CASES]
    assert len({r.kind for p in packages for r in p.records}) == 17
    assert len(examples.CASES) == 10
    with pytest.raises(ValueError):
        to_rdf(packages[0], "xml")


def test_reference_validation_is_order_independent(data):
    data["records"].reverse()
    assert EvidencePackage.model_validate(data)
    node(data, "EmissionSource")["facility"] = "urn:ghgag:missing:v1"
    with pytest.raises(ValidationError):
        EvidencePackage.model_validate(data)
