"""Independent literal numeric oracles for the reported-only profile (synthetic facts)."""

import json
from copy import deepcopy
from decimal import Decimal

import pytest
from rdflib import RDF

from ghg_assurance_graph.cli import main
from ghg_assurance_graph.reported import (
    REP,
    ReportedDisclosure,
    ReportedEvidenceTools,
    ReportedQuantity,
    compare_reported,
    create_reported_package,
    explain_reported,
    load_reported,
    reported_graph,
    validate_reported,
    verify_reported_package,
)


def row(**changes):
    result = {
        "id": "s1",
        "year": 2023,
        "scope": 1,
        "category": None,
        "scope2_basis": None,
        "quantity": {"value": "100", "unit": "tCO2e"},
        "source": {
            "url": "https://example.org/report.pdf",
            "sha256": "a" * 64,
            "page": "42",
            "retrieved_at": "2026-09-28T00:00:00Z",
            "title": "Synthetic test",
        },
        "boundary": "group",
        "gwp_basis": "AR5",
        "restatement": "none disclosed",
        "rounding": "1",
    }
    result.update(changes)
    return result


def disclosure(*rows):
    return {
        "profile": "reported-disclosure/1",
        "organization": "Synthetic",
        "assertions": list(rows or [row()]),
    }


def model(*rows):
    return ReportedDisclosure.model_validate(disclosure(*rows))


@pytest.mark.parametrize(
    "value", [None, 2, 2.0, True, "NaN", "Infinity", "-1", "1e3", "01", " 1", "1.", "9" * 31]
)
def test_strict_decimal(value):
    assert (
        validate_reported(disclosure(row(quantity={"value": value, "unit": "tCO2e"})))["status"]
        == "invalid"
    )


@pytest.mark.parametrize("unit", [None, "tonne", "t CO2e", "kgCO2", "MTCO2e", "tco2e"])
def test_exact_units(unit):
    assert (
        validate_reported(disclosure(row(quantity={"value": "1", "unit": unit})))["status"]
        == "invalid"
    )


@pytest.mark.parametrize(
    "changes",
    [
        {"scope": "1"},
        {"scope": True},
        {"scope": None},
        {"category": 1},
        {"scope2_basis": "market-based"},
        {"scope": 2},
        {"scope": 2, "scope2_basis": "both"},
        {"scope": 3, "category": 16},
        {"year": None},
        {"year": "2024"},
        {"rounding": "0"},
        {"rounding": "3"},
        {"boundary": " "},
        {"total_scopes": [1, 2]},
        {"id": "../unsafe"},
        {"scope": None, "total_scopes": [1, 1]},
        {"scope": None, "total_scopes": [2, 1], "scope2_basis": "location-based"},
    ],
)
def test_classification(changes):
    assert validate_reported(disclosure(row(**changes)))["status"] == "invalid"


@pytest.mark.parametrize(
    "field",
    ["year", "boundary", "gwp_basis", "restatement", "rounding", "category", "scope2_basis"],
)
def test_required_explicit_missingness(field):
    r = row()
    del r[field]
    assert validate_reported(disclosure(r))["status"] == "invalid"


@pytest.mark.parametrize(
    "url",
    [
        "file:///etc/passwd",
        "http://example.org",
        "https://localhost/x",
        "https://127.0.0.1/x",
        "https://[::1]/x",
        "https://a.local/x",
        "https://user:pw@example.org/x",
        "https://example.org:444/x",
        "https://example.org/\n",
        "https://127.1/x",
        "https://example.org\\@localhost/x",
    ],
)
def test_unsafe_citation(url):
    r = row()
    r["source"]["url"] = url
    assert validate_reported(disclosure(r))["status"] == "invalid"


def test_source_provenance_required():
    for field in row()["source"]:
        r = row()
        del r["source"][field]
        assert validate_reported(disclosure(r))["status"] == "invalid"
    for field, value in [("sha256", "z" * 64), ("retrieved_at", "2024-01-01"), ("page", "")]:
        r = row()
        r["source"][field] = value
        assert validate_reported(disclosure(r))["status"] == "invalid"


def test_exact_conversion_and_long_precision():
    assert ReportedQuantity(value="1000", unit="kgCO2e").tonnes() == Decimal(1)
    assert ReportedQuantity(value="1.25", unit="ktCO2e").tonnes() == Decimal(1250)
    assert ReportedQuantity(
        value="123456789012345678901234567890.123456789012", unit="ktCO2e"
    ).tonnes() == Decimal("123456789012345678901234567890123.456789012000")


def test_duplicate_identity_and_copy():
    assert validate_reported(disclosure(row(), row(id="other")))["status"] == "invalid"
    assert validate_reported(disclosure(row(), row(year=2024)))["status"] == "invalid"
    with pytest.raises(ValueError):
        model().assertions[0].model_copy(update={"year": None})


def test_graph_no_fabricated_calculation():
    m = model(row(boundary=None, gwp_basis=None, restatement=None, rounding=None))
    graph = reported_graph(m)
    assert set(graph.objects(None, RDF.type)) == {REP.ReportedAssertion, REP.SourceCitation}
    assert len(list(graph.triples((None, REP.missingField, None)))) >= 4
    assert explain_reported(m, "s1")["causality"] == "UNKNOWN"
    assert validate_reported(m)["status"] == "not_assessable"
    with pytest.raises(ValueError):
        explain_reported(m, "missing")


def total_model(total="300", rounding="1", basis="location-based"):
    return model(
        row(),
        row(
            id="s2-lb",
            scope=2,
            scope2_basis="location-based",
            quantity={"value": "200", "unit": "tCO2e"},
        ),
        row(
            id="s2-mb",
            scope=2,
            scope2_basis="market-based",
            quantity={"value": "150", "unit": "tCO2e"},
        ),
        row(
            id="total",
            scope=None,
            total_scopes=[1, 2],
            scope2_basis=basis,
            quantity={"value": total, "unit": "tCO2e"},
            rounding=rounding,
        ),
    )


def reconciliation(m):
    return next(
        c for c in validate_reported(m)["checks"] if c["rule"] == "reported_total_reconciliation"
    )


def test_scope2_alternatives_and_total_overlap():
    assert reconciliation(total_model())["delta_tCO2e"] == "0"
    assert reconciliation(total_model("250", basis="market-based"))["delta_tCO2e"] == "0"
    assert reconciliation(total_model("450"))["status"] == "invalid"
    assert reconciliation(total_model("301"))["status"] == "assessed"
    assert reconciliation(total_model("302"))["status"] == "invalid"
    assert reconciliation(total_model(rounding=None))["status"] == "not_assessable"
    assert reconciliation(total_model(basis="unspecified"))["status"] == "not_assessable"


def test_categories_are_not_scopes_or_extra_components():
    m = total_model()
    m = m.model_copy(update={"assertions": (*m.assertions, row(id="cat1", scope=3, category=1))})
    assert reconciliation(m)["delta_tCO2e"] == "0"


def test_crossyear_unknown_causality_and_missing_rows():
    diff = compare_reported(
        model(),
        model(row(year=2024, quantity={"value": "0.09", "unit": "ktCO2e"}, rounding="0.01")),
    )
    assert diff["rows"][0]["arithmetic_delta_tCO2e"] == "-10.00"
    assert diff["rows"][0]["status"] == "assessed"
    assert diff["causality"] == "UNKNOWN" and diff["aggregate_delta"] is None
    changed = compare_reported(model(), model(row(year=2024, boundary=None)))
    assert changed["rows"][0]["status"] == "not_assessable"
    missing = compare_reported(model(), model(row(id="s3", year=2024, scope=3)))
    assert all(r["arithmetic_delta_tCO2e"] is None for r in missing["rows"])
    with pytest.raises(ValueError):
        compare_reported(model(), model())
    with pytest.raises(ValueError):
        compare_reported(
            model(), model(row(year=2024)).model_copy(update={"organization": "Other"})
        )
    with pytest.raises(ValueError):
        compare_reported(model(row(), row(id="next", year=2024)), model(row(year=2025)))


def test_json_closed_no_context_duplicate_keys():
    with pytest.raises(ValueError):
        load_reported('{"organization":"x","organization":"y"}')
    data = disclosure()
    data["@context"] = "https://example.org/context"
    with pytest.raises(ValueError):
        load_reported(json.dumps(data))
    assert load_reported(json.dumps(disclosure())) == model()


def test_stable_graph_identity_and_unknown_restatement():
    single = model()
    combined = model(row(), row(id="next", year=2024))
    assert explain_reported(single, "s1")["node"] == explain_reported(combined, "s1")["node"]
    total = total_model()
    changed = total.model_copy(
        update={
            "assertions": tuple(
                r.model_copy(update={"restatement": None}) if r.id == "total" else r
                for r in total.assertions
            )
        }
    )
    assert reconciliation(changed)["status"] == "not_assessable"
    for field, value in (("retrieved_at", 1234), ("page", " "), ("title", " ")):
        data = disclosure()
        data["assertions"][0]["source"][field] = value
        assert validate_reported(data)["status"] == "invalid"


def test_evidence_package_and_tamper(tmp_path):
    root = tmp_path / "crate"
    result = create_reported_package(model(), root, created_at="2026-09-28T00:00:00Z")
    assert result["valid"]
    assert verify_reported_package(root, expected_manifest_sha256=result["manifest_sha256"])[
        "valid"
    ]
    assert not verify_reported_package(root, expected_manifest_sha256="a" * 64)["valid"]
    metadata = json.loads((root / "ro-crate-metadata.json").read_text())
    assert isinstance(metadata["@context"], dict)
    (root / "graph.ttl").write_text("malicious")
    assert not verify_reported_package(root)["valid"]


@pytest.mark.parametrize("attack", ["context", "manifest_path", "extra", "symlink"])
def test_crate_unsafe_payloads(tmp_path, attack):
    root = tmp_path / "crate"
    create_reported_package(model(), root, created_at="2026-09-28T00:00:00Z")
    if attack == "context":
        (root / "graph.jsonld").write_text('{"@context":"https://evil.example/context"}')
    elif attack == "manifest_path":
        data = json.loads((root / "manifest.json").read_text())
        data["files"]["../outside"] = data["files"].pop("package.json")
        (root / "manifest.json").write_text(json.dumps(data))
    elif attack == "extra":
        (root / "extra").write_text("x")
    else:
        (root / "graph.ttl").unlink()
        (root / "graph.ttl").symlink_to(tmp_path / "outside")
    assert not verify_reported_package(root)["valid"]


def test_tools_obsidian_and_paths(tmp_path):
    tools = ReportedEvidenceTools(model(row(note="[[evil]] <script>bad</script>")))
    assert tools.missing_evidence()
    assert tools.explain("s1")["tonnesCO2e"] == "100"
    tools.obsidian(tmp_path / "vault")
    notes = "".join(p.read_text() for p in (tmp_path / "vault").glob("*.md"))
    assert "<script>" not in notes and "[[evil]]" not in notes
    with pytest.raises(ValueError):
        tools.obsidian(tmp_path / ".." / "outside")
    link = tmp_path / "link"
    link.symlink_to(tmp_path, target_is_directory=True)
    with pytest.raises(ValueError):
        tools.package(link / "crate", created_at="2026-09-28T00:00:00Z")


def test_cli_end_to_end(tmp_path, capsys):
    source = tmp_path / "facts.json"
    source.write_text(json.dumps(disclosure()))
    for action in ("ingest", "validate", "graph", "explain"):
        main(["reported", action, str(source)] + (["s1"] if action == "explain" else []))
        assert capsys.readouterr().out
    after = tmp_path / "after.json"
    after.write_text(json.dumps(disclosure(row(year=2024))))
    main(["reported", "diff", str(source), str(after)])
    assert json.loads(capsys.readouterr().out)["causality"] == "UNKNOWN"
    root = tmp_path / "crate"
    main(
        [
            "reported",
            "package",
            str(source),
            "--out",
            str(root),
            "--created-at",
            "2026-09-28T00:00:00Z",
        ]
    )
    assert json.loads(capsys.readouterr().out)["valid"]
    main(["reported", "verify", str(root)])
    assert json.loads(capsys.readouterr().out)["valid"]
    main(["reported", "obsidian", str(source), "--out", str(tmp_path / "vault")])
    assert json.loads(capsys.readouterr().out)["exported"]
    data = deepcopy(disclosure())
    data["assertions"][0]["year"] = None
    source.write_text(json.dumps(data))
    with pytest.raises(SystemExit) as exc:
        main(["reported", "validate", str(source)])
    assert exc.value.code == 1
    assert json.loads(capsys.readouterr().out)["status"] == "invalid"
