"""Evidence-linked deterministic benchmark questions; no AI interpretation."""

import socket
from pathlib import Path

import pytest

from ghg_assurance_graph.serialization import from_json
from ghg_assurance_graph.tools import EvidenceTools, QueryRequest

ROOT = Path(__file__).parents[1]
RESULT = "urn:ghgag:acme-2025-v1-electricity-result:v1"


@pytest.fixture
def package():
    return from_json((ROOT / "benchmark/generated/2025-v1/package.json").read_text())


@pytest.fixture
def tools(package):
    return EvidenceTools([package])


def test_benchmark_question_what_supports_500_kg(tools, monkeypatch):
    def no_network(*args, **kwargs):
        raise AssertionError("network access forbidden")

    monkeypatch.setattr(socket.socket, "connect", no_network)
    monkeypatch.setattr(socket, "create_connection", no_network)
    request = {"name": "explain_result", "target": RESULT}
    answer = tools.call(request)
    assert answer == tools.call(request)
    (row,) = answer["rows"]
    assert row["value"] == "500.0" and row["unit"] == "kg_CO2e"
    (evidence,) = answer["evidence"]
    assert evidence["id"] == row["evidence"] == row["factorEvidence"]
    assert evidence["citation"] and evidence["synthetic"] is True
    assert "not an assurance opinion" in answer["authority"]
    assert answer["total_rows"] == 1 and answer["truncated"] is False


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "SELECT * WHERE { SERVICE <https://example.invalid> {?s ?p ?o}}"},
        {"name": "../explain_result"},
        {"name": "explain_result", "target": "https://example.invalid"},
        {"name": "explain_result", "target": RESULT + "> SERVICE <https://example.invalid>"},
        {"name": "unreviewed_results", "sparql": "DROP ALL"},
        {"name": "unreviewed_results", "limit": 101},
        {"name": "unreviewed_results", "limit": True},
        {"name": "unreviewed_results", "limit": 0},
        {"name": "unreviewed_results", "target": RESULT},
        {"name": "explain_result"},
        {"name": "explain_result", "target": "urn:ghgag:absent:v1"},
        {"name": "explain_result", "target": "urn:ghgag:acme-2025-v1-org:v1"},
    ],
)
def test_reject_unsafe_or_unsupported_requests(tools, payload):
    with pytest.raises(ValueError):
        tools.call(payload)


def test_truncation_and_evidence_lookup(tools):
    evidence = "urn:ghgag:acme-2025-v1-electricity-evidence:v1"
    answer = tools.call(
        QueryRequest(name="records_supported_by_evidence", target=evidence, limit=1)
    )
    assert len(answer["rows"]) == 1
    assert answer["total_rows"] == 4 and answer["truncated"]
    assert answer["evidence"][0]["id"] == evidence
    assert tools.call({"name": "unreviewed_results"})["rows"] == []


def test_budgets(package, tools, monkeypatch):
    import ghg_assurance_graph.tools as module

    monkeypatch.setattr(module, "MAX_RECORDS", 1)
    with pytest.raises(ValueError, match="record budget"):
        EvidenceTools([package])
    monkeypatch.setattr(module, "MAX_RECORDS", 2000)
    monkeypatch.setattr(module, "MAX_PACKAGE_BYTES", 1)
    with pytest.raises(ValueError, match="byte budget"):
        EvidenceTools([package])
    monkeypatch.setattr(module, "MAX_RESPONSE_BYTES", 1)
    with pytest.raises(ValueError, match="response byte budget"):
        tools.call({"name": "explain_result", "target": RESULT})


def test_request_schema_closed():
    assert QueryRequest.model_json_schema()["additionalProperties"] is False
