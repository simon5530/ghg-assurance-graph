"""Adversarial independent contract tests; synthetic assertions, no real-source claims."""

import json
import socket
import subprocess
import sys
from decimal import localcontext
from pathlib import Path

import pytest
from rdflib import RDF, Literal

from ghg_assurance_graph.reported import (
    REP,
    ReportedDisclosure,
    ReportedEvidenceTools,
    ReportedQuantity,
    compare_reported,
    create_reported_package,
    explain_reported,
    reported_graph,
    validate_reported,
    verify_reported_package,
)


def assertion(**changes):
    data = {
        "id": "a",
        "year": 2020,
        "scope": 1,
        "category": None,
        "scope2_basis": None,
        "quantity": {"value": "100", "unit": "tCO2e"},
        "source": {
            "url": "https://example.org/report",
            "sha256": "a" * 64,
            "page": "1",
            "retrieved_at": "2026-09-28T00:00:00Z",
            "title": "Source states independently assured",
        },
        "boundary": "group",
        "gwp_basis": "AR5",
        "restatement": "original",
        "rounding": "1",
    }
    data.update(changes)
    return data


def document(*rows):
    return {
        "profile": "reported-disclosure/1",
        "organization": "Synthetic review",
        "assertions": list(rows or [assertion()]),
    }


def model(*rows):
    return ReportedDisclosure.model_validate(document(*rows))


def total_check(*rows):
    return next(
        c
        for c in validate_reported(document(*rows))["checks"]
        if c["rule"] == "reported_total_reconciliation"
    )


def total_rows(**changes):
    return [
        assertion(),
        assertion(id="b", scope=2, scope2_basis="location-based"),
        assertion(
            id="total",
            scope=None,
            total_scopes=[1, 2],
            scope2_basis="location-based",
            quantity={"value": "200", "unit": "tCO2e"},
            **changes,
        ),
    ]


@pytest.fixture(autouse=True)
def block_network(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Network attempted")

    for name in ("create_connection", "getaddrinfo"):
        monkeypatch.setattr(socket, name, forbidden)
    monkeypatch.setattr(socket.socket, "connect", forbidden)
    monkeypatch.setattr(socket.socket, "connect_ex", forbidden)


@pytest.mark.parametrize("field", ["boundary", "gwp_basis", "restatement"])
@pytest.mark.parametrize("value", [None, "incompatible"])
def test_total_rejects_unknown_or_different_basis(field, value):
    rows = total_rows()
    rows[0][field] = value
    assert total_check(*rows)["status"] == "not_assessable"


def test_unknown_rounding_never_asserts_mismatch():
    rows = total_rows(rounding=None)
    rows[2]["quantity"]["value"] = "999"
    assert total_check(*rows)["status"] == "not_assessable"


def test_overlaps_do_not_inflate_total():
    rows = total_rows()
    rows += [
        assertion(id="mb", scope=2, scope2_basis="market-based"),
        assertion(id="cat", scope=3, category=1),
        assertion(
            id="other-total",
            scope=None,
            total_scopes=[1, 3],
            quantity={"value": "200", "unit": "tCO2e"},
        ),
    ]
    assert total_check(*rows)["delta_tCO2e"] == "0"


def test_crossyear_gaps_and_basis_changes_are_not_abatement():
    result = compare_reported(model(), model(assertion(id="later", year=2025, gwp_basis="AR6")))
    assert result["before_year"] == 2020 and result["after_year"] == 2025
    assert result["rows"][0]["status"] == "not_assessable"
    assert result["rows"][0]["arithmetic_delta_tCO2e"] == "0"
    assert result["aggregate_delta"] is None and result["causality"] == "UNKNOWN"


def test_source_assurance_label_is_not_own_assurance_or_factor():
    m = model()
    graph = reported_graph(m)
    assert set(graph.objects(None, RDF.type)) == {REP.ReportedAssertion, REP.SourceCitation}
    assert all(isinstance(url, Literal) for url in graph.objects(None, REP.url))
    checks = explain_reported(m, "a")["checks"]
    for rule in ("independent_assurance", "activity_factor_recalculation", "source_authenticity"):
        assert next(c for c in checks if c["rule"] == rule)["status"] == "not_assessable"


def test_identity_stable_for_reordering_and_subsets():
    a, b = assertion(), assertion(id="b", year=2021)
    assert explain_reported(model(a, b), "a")["node"] == explain_reported(model(b, a), "a")["node"]
    assert explain_reported(model(a), "a")["node"] == explain_reported(model(a, b), "a")["node"]
    assert validate_reported(document(a, assertion(id="duplicate")))["status"] == "invalid"


def test_profile_separation_and_context_rejected():
    for extra in (
        {"schema_version": "0.1"},
        {"@context": "https://example.org/context"},
        {"profile": "0.1"},
    ):
        data = document()
        data.update(extra)
        assert validate_reported(data)["status"] == "invalid"


def test_decimal_precision_independent_of_low_precision():
    with localcontext() as ctx:
        ctx.prec = 2
        value = ReportedQuantity(
            value="123456789012345678901234567890.123456789012", unit="ktCO2e"
        ).tonnes()
        assert str(value) == "123456789012345678901234567890123.456789012000"
        assert total_check(*total_rows())["delta_tCO2e"] == "0"


def test_decimal_context_exponent_must_not_change_valid_result():
    with localcontext() as ctx:
        ctx.Emax = 2
        ctx.Emin = -2
        assert str(ReportedQuantity(value="1000", unit="ktCO2e").tonnes()) == "1000000"


def make_crate(tmp_path):
    root = tmp_path / "crate"
    assert create_reported_package(model(), root, created_at="2026-09-28T00:00:00Z")["valid"]
    return root


def test_package_records_software_and_command_provenance(tmp_path):
    root = make_crate(tmp_path)
    manifest = json.loads((root / "manifest.json").read_text())
    assert manifest.get("software", {}).get("ghg-assurance-graph")
    assert manifest.get("command")


@pytest.mark.parametrize("payload", ["graph.jsonld", "ro-crate-metadata.json"])
def test_context_tamper_never_fetches_even_with_rehashed_manifest(tmp_path, payload):
    from hashlib import sha256

    from ghg_assurance_graph.exporters import canonical_json

    root = make_crate(tmp_path)
    data = b'{"@context":"https://example.org/remote"}'
    (root / payload).write_bytes(data)
    manifest = json.loads((root / "manifest.json").read_text())
    manifest["files"][payload] = {"sha256": sha256(data).hexdigest(), "bytes": len(data)}
    (root / "manifest.json").write_text(canonical_json(manifest))
    assert not verify_reported_package(root)["valid"]


def test_crate_and_vault_ancestor_symlinks_rejected(tmp_path):
    root = make_crate(tmp_path)
    link = tmp_path / "link"
    link.symlink_to(tmp_path, target_is_directory=True)
    assert not verify_reported_package(link / root.name)["valid"]
    with pytest.raises(ValueError):
        ReportedEvidenceTools(model()).obsidian(link / "vault")


def test_public_runner_escapes_untrusted_organization(tmp_path):
    data = document()
    data["organization"] = '<script>alert("untrusted")</script>'
    source = tmp_path / "input.json"
    source.write_text(json.dumps(data))
    out = tmp_path / "out"
    runner = Path(__file__).resolve().parents[1] / "scripts" / "run_public_case.py"
    completed = subprocess.run(
        [sys.executable, str(runner), str(source), "--out", str(out)],
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert completed.returncode == 0, completed.stderr
    assert "<script>" not in (out / "REPORT.md").read_text()
