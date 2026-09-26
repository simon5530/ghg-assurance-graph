"""Independent literal/Fraction oracle: never regenerate expected answers."""

import hashlib
import json
from collections import defaultdict
from copy import deepcopy
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import pytest

from ghg_assurance_graph.benchmark import amount, generate, inputs, package, preflight
from ghg_assurance_graph.models import EvidencePackage
from ghg_assurance_graph.serialization import from_json, to_json

ROOT = Path(__file__).resolve().parents[1] / "benchmark"
TRUTH = json.loads((ROOT / "ground_truth/expected_amounts.json").read_text())
FINDINGS = json.loads((ROOT / "ground_truth/expected_findings.json").read_text())["findings"]
CHANGES = json.loads((ROOT / "ground_truth/expected_change_attribution.json").read_text())[
    "changes"
]


@pytest.mark.parametrize("version", TRUTH["kg_co2e"])
def test_clean_independent_oracle(version):
    rows = inputs(version)
    assert [r["id"] for r in rows] == TRUTH["order"]
    expected = TRUTH["kg_co2e"][version]
    assert [amount(r) for r in rows] == expected
    # Different numeric implementation, plus literal expected answers above.
    assert [
        Fraction(r["activity"]) * Fraction(r["factor"]) * Fraction(r["allocation_share"])
        for r in rows
    ] == expected
    assert sum(expected) == TRUTH["partial_totals"][version]
    p = package(version, rows)
    assert from_json(to_json(p)) == p
    assert len(p.records) == 158
    assert [r.quantity.value for r in p.records if r.kind == "EmissionResult"] == expected
    nodes = {r.id: r for r in p.records}
    for r in p.records:
        if r.kind == "EmissionResult":
            run = nodes[r.calculation]
            a, f = nodes[run.activity], nodes[run.factor]
            assert Fraction(str(a.quantity.value)) * Fraction(str(f.value)) == Fraction(
                str(r.quantity.value)
            )
    stored = EvidencePackage.model_validate_json(
        (ROOT / "generated" / version / "package.json").read_text()
    )
    assert stored == p


@pytest.mark.parametrize("before,after", [("2025-v1", "2025-v2"), ("2025-v2", "2026-v1")])
def test_crossperiod_reconciliation(before, after):
    old, new = inputs(before), inputs(after)
    components = defaultdict(int)
    for c in CHANGES:
        if (c["before"], c["after"]) == (before, after):
            components[c["entity"]] += c["kg_co2e"]
    for a, b in zip(old, new, strict=True):
        assert a["id"] == b["id"]
        assert amount(b) - amount(a) == components[a["id"]]
    assert (
        sum(components.values()) == TRUTH["partial_totals"][after] - TRUTH["partial_totals"][before]
    )


def test_activity_first_convention():
    # Independent counterfactual: (800-1000)*.5=-100; 800*(.6-.5)=80.
    assert (800 - 1000) * Fraction(1, 2) == -100
    assert 800 * (Fraction(3, 5) - Fraction(1, 2)) == 80
    assert [c["kg_co2e"] for c in CHANGES if c["entity"] == "electricity"] == [-100, 80]


@pytest.mark.parametrize("finding", FINDINGS, ids=lambda f: f["case_id"])
def test_adversarial_catalog(finding):
    fixture = json.loads((ROOT / "generated/defects" / (finding["case_id"] + ".json")).read_text())
    assert fixture["nonconforming"] is True
    assert finding["entity"] in {r["id"] for r in fixture["rows"]}
    with pytest.raises(ValueError, match=finding["rule"]):
        preflight(fixture["rows"])


def test_reproduction_hashes(tmp_path):
    generate(tmp_path / "a")
    generate(tmp_path / "b")
    expected = json.loads((ROOT / "generated/manifest.json").read_text())
    for name, digest in expected["sha256"].items():
        a = (tmp_path / "a" / name).read_bytes()
        assert a == (tmp_path / "b" / name).read_bytes() == (ROOT / "generated" / name).read_bytes()
        assert hashlib.sha256(a).hexdigest() == digest
    assert (tmp_path / "a/manifest.json").read_bytes() == (
        ROOT / "generated/manifest.json"
    ).read_bytes()


@pytest.mark.parametrize(
    "field",
    [
        "factor_source",
        "factor_year",
        "gwp_basis",
        "factor_basis",
        "allocation_method",
        "scope2_basis",
    ],
)
def test_missing_normative_fields_fail_closed(field):
    row = deepcopy(inputs("2025-v1")[0])
    del row[field]
    with pytest.raises((KeyError, ValueError)):
        amount(row)


@pytest.mark.parametrize("bad", ["-1", "NaN", "Infinity"])
def test_invalid_numbers(bad):
    row = inputs("2025-v1")[0]
    row["activity"] = bad
    with pytest.raises(ValueError):
        amount(row)


def test_conversion_and_allocation_once():
    row = inputs("2025-v1")[5]
    row.update(activity="0.1", unit="tonne")
    assert amount(row) == 400
    assert amount(inputs("2025-v1")[13]) == 100
    assert amount(inputs("2026-v1")[13]) == 50


def test_no_gas_or_market_or_netting_fallback():
    row = inputs("2025-v1")[4]
    row["factor_basis"] = "kg-HFC"
    with pytest.raises(ValueError, match="GWP"):
        amount(row)
    for stream in ("biogenic-CO2", "removal", "offset"):
        row = inputs("2025-v1")[0]
        row["stream"] = stream
        with pytest.raises(ValueError, match="separate"):
            amount(row)


def test_seed_is_versioned_not_uncontrolled():
    with pytest.raises(ValueError):
        inputs("2025-v1", seed=42)


def test_oracle_is_not_generator_input():
    import inspect

    import ghg_assurance_graph.benchmark as module

    assert "ground_truth" not in inspect.getsource(module)
    assert Decimal(3850) - Decimal(3820) == 30


@pytest.mark.parametrize(
    "version,expected",
    [("2025-v1", [2320, 500, 1000]), ("2025-v2", [2340, 500, 1010]), ("2026-v1", [2770, 480, 810])],
)
def test_scope_subtotals(version, expected):
    rows = inputs(version)
    assert [sum(amount(r) for r in rows if r["scope"] == scope) for scope in (1, 2, 3)] == expected
    assert {r["category"] for r in rows if r["scope"] == 3} == {1, 2, 4, 5, 6, 7}


def test_screening_and_supplier_mix():
    text = (ROOT.parent / "docs/STANDARDS_ALIGNMENT.md").read_text()
    for category in range(1, 16):
        assert f"| {category} " in text
    assert Fraction(3, 4) * 5 + Fraction(1, 4) * 1 == 4
    assert Fraction(1, 2) * 5 + Fraction(1, 2) * 1 == 3
    assert Fraction(3820, 200) == Fraction(191, 10) < 30


@pytest.mark.parametrize(
    "patch",
    [
        {"geography": "VN"},
        {"gwp_basis": "unknown"},
        {"scope2_basis": None},
        {"allocation_method": "unknown"},
        {"unit": "unknown", "factor_unit": "unknown"},
        {"evidence": ""},
        {"allocation_share": "0.5"},
    ],
)
def test_unverified_fields_reject(patch):
    row = inputs("2025-v1")[0]
    row.update(patch)
    with pytest.raises(ValueError):
        amount(row)


def test_no_empty_or_dual_sum():
    with pytest.raises(ValueError, match="empty"):
        preflight([])
    rows = inputs("2025-v1")
    mb = deepcopy(rows[0])
    mb.update(id="electricity-mb", scope2_basis="market-based")
    rows.append(mb)
    with pytest.raises(ValueError, match="market-based"):
        preflight(rows)
