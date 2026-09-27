"""Independent published answers plus literal adversarial arithmetic."""

import inspect
import json
from dataclasses import replace
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import get_args

import pytest

from ghg_assurance_graph import diff
from ghg_assurance_graph.diff import Cause, Declaration, Snapshot, compare
from ghg_assurance_graph.models import ChangeEvent

ROOT = Path(__file__).resolve().parents[1]
NS = "synthetic://acme/20250926"


def rows(version):
    return json.loads((ROOT / f"benchmark/generated/{version}/inputs.json").read_text())


def snapshot(version, data=None):
    return Snapshot(NS, version, tuple(rows(version) if data is None else data))


def declaration(before, after, entity, cause, fields, evidence="controlled scenario evidence"):
    return Declaration(before, after, entity, Cause(cause), frozenset(fields.split()), evidence)


def annotations(before, after):
    # Independent scenario inputs from benchmark README, NOT expected amount/label JSON.
    # These are supplied semantic assertions: evaluation is annotation-assisted.
    if before == "2025-v1":
        specs = [
            ("fleet", "CORRECTION", "activity", "corrected invoice"),
            ("travel", "MISSING_DATA_RESOLVED", "activity origin", "estimate replaced by primary"),
        ]
    else:
        specs = [
            ("materials", "SUPPLIER_MIX_CHANGE", "factor", "75/25 to 50/50; technologies fixed"),
            ("refrigerant", "GWP_CHANGE", "factor gwp_basis", "only characterization changes"),
            ("new-line", "BOUNDARY_CHANGE", "activity", "organic source addition, not acquisition"),
            ("allocation", "ALLOCATION_CHANGE", "allocation_method allocation_share", "policy"),
            (
                "method-transition",
                "METHOD_CHANGE",
                "activity unit factor_unit factor method pcf_boundary",
                "same lot; method transition",
            ),
        ]
    return tuple(declaration(before, after, *spec) for spec in specs)


@pytest.mark.parametrize("before,after", [("2025-v1", "2025-v2"), ("2025-v2", "2026-v1")])
def test_independent_quantitative_oracle(before, after):
    truth = json.loads(
        (ROOT / "benchmark/ground_truth/expected_change_attribution.json").read_text()
    )
    amounts = json.loads((ROOT / "benchmark/ground_truth/expected_amounts.json").read_text())
    result = compare(snapshot(before), snapshot(after), annotations(before, after))
    expected = {
        (c["entity"], c["cause"]): Fraction(c["kg_co2e"])
        for c in truth["changes"]
        if (c["before"], c["after"]) == (before, after)
    }
    actual = {(c.entity, c.cause.value): Fraction(c.kg_co2e) for c in result.components}
    # Label precision=recall=1; exact amount agreement=1; MAE=0 on public scenarios.
    assert actual.keys() == expected.keys()
    assert sum(abs(actual[k] - expected[k]) for k in expected) / len(expected) == 0
    assert result.total_before == amounts["partial_totals"][before]
    assert result.total_after == amounts["partial_totals"][after]
    assert result.delta == result.attributed_kg_co2e + result.residual_kg_co2e
    assert result.residual_kg_co2e == result.absolute_unknown_kg_co2e == 0
    assert len(result.matches) == 15


def test_original_taxonomy_exactly_preserved():
    assert {c.value for c in Cause} == set(get_args(ChangeEvent.model_fields["cause"].annotation))


def test_order_independent_and_no_truth_input():
    a, b = "2025-v2", "2026-v1"
    assert compare(snapshot(a), snapshot(b)) == compare(
        snapshot(a, list(reversed(rows(a)))), snapshot(b, list(reversed(rows(b))))
    )
    assert "ground_truth" not in inspect.getsource(diff)


def test_unannotated_semantics_remain_unknown():
    result = compare(snapshot("2025-v2"), snapshot("2026-v1"))
    unknown = {c.entity: c.kg_co2e for c in result.components if c.cause == Cause.UNKNOWN}
    assert unknown == {"allocation": -50, "method-transition": -50, "refrigerant": 400}
    assert result.residual_kg_co2e == 300
    assert result.absolute_unknown_kg_co2e == 500
    # Bare activity/factor deltas are mechanical, not claims about corrections or mix.
    assert result.delta == 210


@pytest.mark.parametrize("cause", list(Cause))
def test_all_causes_explicitly_representable(cause):
    a, b = "2025-v1", "2025-v2"
    result = compare(snapshot(a), snapshot(b), [declaration(a, b, "fleet", cause, "activity")])
    assert next(c for c in result.components if c.entity == "fleet").cause == cause


def test_duplicate_wrong_snapshot_and_wrong_join_reject():
    data = rows("2025-v1")
    with pytest.raises(ValueError, match="duplicate"):
        snapshot("2025-v1", data + [data[0]])
    with pytest.raises(ValueError, match="snapshot"):
        snapshot("2025-v2", data)
    with pytest.raises(ValueError, match="distinct"):
        compare(snapshot("2025-v1"), snapshot("2025-v1"))
    data = rows("2025-v2")
    data[0]["facility"] = "hq"
    with pytest.raises(ValueError, match="classification"):
        compare(snapshot("2025-v1"), snapshot("2025-v2", data))
    other = [dict(r, evidence=r["evidence"].replace("20250926", "other")) for r in rows("2025-v2")]
    with pytest.raises(ValueError, match="namespace"):
        compare(snapshot("2025-v1"), Snapshot("synthetic://acme/other", "2025-v2", tuple(other)))


def test_added_removed_not_fuzzy_joined_or_assumed_acquisition():
    data = rows("2025-v2")
    data[0].update(id="electricity-renamed", evidence=f"{NS}/2025-v2/electricity-renamed")
    result = compare(snapshot("2025-v1"), snapshot("2025-v2", data))
    assert {(m.entity, m.status) for m in result.matches if m.status != "matched"} == {
        ("electricity", "removed"),
        ("electricity-renamed", "added"),
    }
    assert result.absolute_unknown_kg_co2e == 1010  # travel ambiguity plus +/-500
    assert result.residual_kg_co2e == 10


@pytest.mark.parametrize("fault", ["pair", "entity", "fields", "overlap", "empty-evidence"])
def test_malformed_declarations_fail_closed(fault):
    a, b = "2025-v1", "2025-v2"
    item = declaration(a, b, "fleet", "CORRECTION", "activity")
    with pytest.raises(ValueError):
        if fault == "pair":
            item = replace(item, before="wrong")
        elif fault == "entity":
            item = replace(item, entity="missing")
        elif fault == "fields":
            item = replace(item, fields=frozenset({"factor"}))
        elif fault == "empty-evidence":
            item = replace(item, evidence=" ")
        compare(snapshot(a), snapshot(b), [item, item] if fault == "overlap" else [item])


@pytest.mark.parametrize(
    "path", sorted((ROOT / "benchmark/generated/defects").glob("*.json")), ids=lambda p: p.stem
)
def test_existing_adversarial_catalog(path):
    with pytest.raises(ValueError):
        snapshot("2025-v1", json.loads(path.read_text())["rows"])


@pytest.mark.parametrize("value", ["NaN", "Infinity", "-1", "1e61", 0.1])
def test_invalid_decimal(value):
    data = rows("2025-v1")
    data[0]["activity"] = value
    with pytest.raises(ValueError):
        snapshot("2025-v1", data)


def test_empty_and_raw_gas_reject():
    with pytest.raises(ValueError, match="1..10000"):
        snapshot("2025-v1", [])
    data = rows("2025-v1")
    data[4]["factor_basis"] = "kg-HFC"
    with pytest.raises(ValueError, match="GWP"):
        snapshot("2025-v1", data)


def test_cross_terms_allocation_decimal_context_and_negative_delta():
    a, b = rows("2025-v1")[13], rows("2025-v2")[13]
    a.update(activity="3", factor="2", allocation_share="0.5", reported_kg_co2e="3")
    b.update(activity="2", factor="3", allocation_share="0.25", reported_kg_co2e="1.5")
    with localcontext() as ctx:
        ctx.prec = 2
        result = compare(snapshot("2025-v1", [a]), snapshot("2025-v2", [b]))
    assert [(c.cause, c.kg_co2e) for c in result.components] == [
        (Cause.ACTIVITY_CHANGE, -1),
        (Cause.EMISSION_FACTOR_CHANGE, 1),
        (Cause.ALLOCATION_CHANGE, Decimal("-1.5")),
    ]
    assert result.delta == Decimal("-1.5")
    a.update(
        activity="0.123456789123456789",
        factor="2",
        allocation_share="0.5",
        reported_kg_co2e="0.123456789123456789",
    )
    b.update(
        activity="0.123456789123456788",
        factor="2",
        allocation_share="0.5",
        reported_kg_co2e="0.123456789123456788",
    )
    with localcontext() as ctx:
        ctx.prec = 2
        result = compare(snapshot("2025-v1", [a]), snapshot("2025-v2", [b]))
    assert result.delta == Decimal("-0.000000000000000001")


def test_unknown_zero_metadata_and_snapshot_copied():
    a, b = rows("2025-v1")[0], rows("2025-v2")[0]
    b["uncertainty"] = "changed quality assessment"
    old = snapshot("2025-v1", [a])
    a["activity"] = "999"
    result = compare(old, snapshot("2025-v2", [b]))
    assert result.components[0].cause == Cause.UNKNOWN
    assert result.components[0].kg_co2e == result.delta == 0
    with pytest.raises(TypeError):
        old.rows[0]["activity"] = "2"


def test_unit_conversion_once():
    a, b = rows("2025-v1")[5], rows("2025-v2")[5]
    a.update(activity="0.1", unit="tonne")
    b.update(activity="0.2", unit="tonne", reported_kg_co2e="800")
    result = compare(snapshot("2025-v1", [a]), snapshot("2025-v2", [b]))
    assert result.delta == 400
    assert result.components[0].kg_co2e == 400
