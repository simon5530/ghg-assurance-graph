"""Independent literal oracles for invented data, not company disclosures.

The fixtures deliberately retain missing years, parent/group separation, and
alternative Scope 2 rows. Citation hashes are synthetic placeholders only.
"""

from pathlib import Path

import pytest

from ghg_assurance_graph.reported import compare_reported, load_reported, validate_reported

ROOT = Path(__file__).parent / "fixtures" / "reported"


def facts(name):
    return load_reported((ROOT / f"{name}.json").read_text())


def year(model, value):
    return model.model_copy(
        update={"assertions": tuple(r for r in model.assertions if r.year == value)}
    )


def test_group_literal_table_and_missing_scope3_year():
    m = facts("group")
    assert {(r.year, r.scope): r.quantity.value for r in m.assertions} == {
        (2022, 1): "900",
        (2022, 2): "1800",
        (2023, 1): "600",
        (2023, 2): "1700",
        (2024, 1): "550",
        (2024, 2): "1550",
        (2024, 3): "2000",
    }
    assert all(r.quantity.unit == "tCO2e" for r in m.assertions)
    assert all(r.scope2_basis == "unspecified" for r in m.assertions if r.scope == 2)
    assert all(r.rounding is None and r.restatement is None for r in m.assertions)
    assert validate_reported(m)["status"] == "not_assessable"
    d = compare_reported(year(m, 2023), year(m, 2024))
    assert {r["after"]: r["arithmetic_delta_tCO2e"] for r in d["rows"]} == {
        "group-2024-scope1": "-50",
        "group-2024-scope2-unspecified": "-150",
        "group-2024-scope3": None,
    }
    assert all(r["causality"] == "UNKNOWN" for r in d["rows"])
    assert d["aggregate_delta"] is None


def test_parent_literal_table_and_boundary_separation():
    m = facts("parent")
    expected = {
        2022: (500, 1200, 1600),
        2023: (350, 1100, 1500),
        2024: (250, 1000, 1300),
    }
    assert len(m.assertions) == 9
    for row in m.assertions:
        assert int(row.quantity.value) == expected[row.year][row.scope - 1]
        assert row.boundary == "synthetic parent only"
    assert all(r.boundary == "synthetic group" for r in facts("group").assertions)
    with pytest.raises(ValueError):
        compare_reported(year(m, 2023), year(facts("group"), 2024))


def test_literal_scope2_alternatives_and_deltas():
    m = facts("alternatives")
    assert {(r.year, r.scope, r.scope2_basis): r.quantity.value for r in m.assertions} == {
        (2023, 1, None): "1200",
        (2023, 2, "market-based"): "8000",
        (2023, 2, "location-based"): "9500",
        (2023, 3, None): "6000",
        (2024, 1, None): "1350",
        (2024, 2, "market-based"): "8500",
        (2024, 2, "location-based"): "10200",
        (2024, 3, None): "6400",
    }
    d = compare_reported(year(m, 2023), year(m, 2024))
    assert [r["arithmetic_delta_tCO2e"] for r in d["rows"]] == ["150", "700", "500", "400"]
    assert d["aggregate_delta"] is None
    assert all(r["status"] == "not_assessable" for r in d["rows"])
    assert all(r["causality"] == "UNKNOWN" for r in d["rows"])


@pytest.mark.parametrize("name,digest", [("group", "a"), ("parent", "b"), ("alternatives", "c")])
def test_every_fact_retains_synthetic_citation(name, digest):
    m = facts(name)
    for row in m.assertions:
        assert row.source.sha256 == digest * 64
        assert row.source.url == f"https://example.org/synthetic-{name}.txt"
        assert row.source.page == "1"
        assert "Synthetic" in row.source.title
