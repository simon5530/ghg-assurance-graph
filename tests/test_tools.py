"""Evidence-linked deterministic benchmark questions; no AI interpretation."""

import socket
from pathlib import Path

import pytest

from ghg_assurance_graph.serialization import from_json
from ghg_assurance_graph.tools import EvidenceTools, QueryRequest

ROOT = Path(__file__).parents[1]
RESULT = "urn:ghgag:exampleco-ghg-001-2025-v1-electricity-result:v1"


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
        {"name": "explain_result", "target": "urn:ghgag:exampleco-ghg-001-2025-v1-org:v1"},
    ],
)
def test_reject_unsafe_or_unsupported_requests(tools, payload):
    with pytest.raises(ValueError):
        tools.call(payload)


def test_truncation_and_evidence_lookup(tools):
    evidence = "urn:ghgag:exampleco-ghg-001-2025-v1-electricity-evidence:v1"
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


@pytest.fixture
def offline(monkeypatch):
    def blocked(*args, **kwargs):
        raise AssertionError("network access forbidden")

    monkeypatch.setattr(socket.socket, "connect", blocked)
    monkeypatch.setattr(socket, "create_connection", blocked)


def test_question_set_factor_graph_and_digest_gaps(package, offline):
    from ghg_assurance_graph.models import EvidencePackage

    records = tuple(
        r.model_copy(update={"sha256": None}) if r.kind == "EvidenceArtifact" else r
        for r in package.records
    )
    tools = EvidenceTools([EvidencePackage(records=records)])
    factor = "urn:ghgag:exampleco-ghg-001-2025-v1-electricity-factor:v1"
    answer = tools.call({"name": "find_results_using_factor", "target": factor})
    assert [r["result"] for r in answer["rows"]] == [RESULT]
    assert tools.call({"name": "query_graph", "query": "explain_result", "target": RESULT}) == (
        tools.explain_result(RESULT)
    )
    answer = tools.call({"name": "find_missing_evidence", "limit": 100})
    assert answer["total_rows"] == 60
    assert len([r for r in answer["rows"] if r["result"] == RESULT]) == 4
    assert all(r["gap"] == "artifact digest absent" for r in answer["rows"])
    assert answer["evidence"] and "no real-world" in answer["scope"]


def test_question_set_validation_distinguishes_assertions(package, offline):
    from ghg_assurance_graph.models import EvidencePackage, ValidationFinding

    finding = ValidationFinding(
        id="urn:ghgag:test-finding:v1",
        logical_id="urn:ghgag:test-finding",
        label="test",
        target=RESULT,
        severity="warning",
        rule="test-rule",
        message="asserted only",
    )
    tools = EvidenceTools([EvidencePackage(records=(*package.records, finding))])
    answer = tools.call({"name": "get_validation_findings", "target": RESULT})
    assert len(answer["rows"]) == 1
    assert answer["rows"][0]["origin"] == "asserted-record"
    assert answer["rows"][0]["id"] == finding.id
    assert tools.get_validation_findings() == tools.get_validation_findings()


def comparison_tools():
    import json

    from ghg_assurance_graph.diff import Snapshot

    packages, snapshots = [], {}
    for version in ("2025-v1", "2025-v2"):
        base = ROOT / "benchmark/generated" / version
        packages.append(from_json((base / "package.json").read_text()))
        inventory = f"urn:ghgag:exampleco-ghg-001-{version}-inventory:v1"
        snapshots[inventory] = Snapshot(
            "synthetic://exampleco-ghg-001/20250926",
            version,
            tuple(json.loads((base / "inputs.json").read_text())),
        )
    return EvidenceTools(packages, snapshots=snapshots), packages, snapshots


def test_question_set_compare_exact_totals_and_evidence(offline):
    from decimal import Decimal

    tools, _, snapshots = comparison_tools()
    before, after = snapshots
    answer = tools.call({"name": "compare_inventory_versions", "before": before, "after": after})
    assert answer == tools.compare_inventory_versions(before, after)
    # Published independent oracle: 3850 - 3820, fleet +20 and travel +10.
    assert Decimal(answer["totals"]["delta"]) == 30
    assert Decimal(answer["totals"]["total_before"]) == 3820
    assert Decimal(answer["totals"]["total_after"]) == 3850
    assert Decimal(answer["totals"]["delta"]) == (
        Decimal(answer["totals"]["attributed_kg_co2e"])
        + Decimal(answer["totals"]["residual_kg_co2e"])
    )
    assert answer["evidence"]
    assert all(r["before_citation"] and r["after_citation"] for r in answer["rows"])
    short = tools.compare_inventory_versions(before, after, limit=1)
    assert short["truncated"] and short["totals"] == answer["totals"]
    snapshots.clear()
    assert tools.compare_inventory_versions(before, after) == answer


def test_snapshot_binding_fails_closed(package):
    tools, packages, snapshots = comparison_tools()
    before, after = snapshots
    with pytest.raises(ValueError, match="explicitly bound"):
        EvidenceTools(packages).compare_inventory_versions(before, after)
    with pytest.raises(ValueError, match="evidence absent"):
        EvidenceTools([package], snapshots={before: snapshots[after]})
    with pytest.raises(ValueError):
        tools.compare_inventory_versions(before, before)


def test_question_set_export_permission_integrity_and_snapshot(tools, tmp_path, offline):
    from ghg_assurance_graph.evidence import verify_package

    destination = tmp_path / "crate"
    kwargs = {"created_at": "2026-09-28T00:00:00+08:00", "command": ["test-export"]}
    with pytest.raises(PermissionError):
        tools.create_evidence_package(destination, **kwargs)
    assert not destination.exists()
    with pytest.raises(ValueError):
        tools.call({"name": "create_evidence_package", "destination": str(destination)})
    assert not destination.exists()
    answer = tools.explain_result(RESULT)
    answer["evidence"][0]["citation"] = "mutated caller copy"
    exported = tools.create_evidence_package(destination, allow_write=True, **kwargs)
    assert exported["valid"]
    assert verify_package(destination, expected_manifest_sha256=exported["manifest_sha256"])[
        "valid"
    ]
    assert tools.explain_result(RESULT)["evidence"][0]["citation"] != "mutated caller copy"
    with pytest.raises(FileExistsError):
        tools.create_evidence_package(destination, allow_write=True, **kwargs)
    link = tmp_path / "link"
    link.symlink_to(tmp_path, target_is_directory=True)
    with pytest.raises(ValueError, match="symlink"):
        tools.create_evidence_package(link / "other", allow_write=True, **kwargs)


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "query_graph"},
        {"name": "query_graph", "query": "SERVICE <https://example.invalid>"},
        {"name": "find_missing_evidence", "target": RESULT},
        {"name": "get_validation_findings", "before": RESULT},
        {"name": "compare_inventory_versions", "before": RESULT, "after": RESULT},
        {"name": "get_validation_findings", "destination": "../escape"},
        {"name": "find_missing_evidence", "limit": True},
    ],
)
def test_new_action_contracts_fail_closed(tools, payload):
    with pytest.raises(ValueError):
        tools.call(payload)
