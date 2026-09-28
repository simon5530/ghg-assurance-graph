"""Literal source-table oracles; these do not establish the truth of company disclosures."""

import hashlib
import json
from fractions import Fraction
from pathlib import Path

from ghg_assurance_graph.reported import compare_reported, load_reported, validate_reported

ROOT = Path(__file__).resolve().parents[1] / "examples" / "public_companies"


def facts(name):
    return load_reported((ROOT / name).read_text())


def test_precommitted_company_selection():
    seed = "2026-09-28-ghgag-public-company-v1"
    candidates = ["TSMC", "UMC", "Delta", "ASE"]
    assert candidates[int(hashlib.sha256(seed.encode()).hexdigest(), 16) % 4] == "UMC"


def test_umc_group_literal_table_and_missing_scope3_year():
    m = facts("umc_group_2022_2024.json")
    expected = {
        (2022, 1): "865984",
        (2022, 2): "1757833",
        (2023, 1): "509555",
        (2023, 2): "1636208",
        (2024, 1): "463670",
        (2024, 2): "1523855",
        (2024, 3): "1713507",
    }
    assert {(r.year, r.scope): r.quantity.value for r in m.assertions} == expected
    assert all(r.quantity.unit == "tCO2e" for r in m.assertions)
    assert all(r.scope2_basis == "unspecified" for r in m.assertions if r.scope == 2)
    assert all(r.rounding is None and r.restatement is None for r in m.assertions)
    assert validate_reported(m)["status"] == "not_assessable"
    before = m.model_copy(update={"assertions": tuple(r for r in m.assertions if r.year == 2023)})
    after = m.model_copy(update={"assertions": tuple(r for r in m.assertions if r.year == 2024)})
    d = compare_reported(before, after)
    deltas = {r["after"]: r["arithmetic_delta_tCO2e"] for r in d["rows"]}
    assert deltas == {
        "umc-2024-scope1": "-45885",
        "umc-2024-scope2-unspecified": "-112353",
        "umc-2024-scope3": None,
    }
    assert Fraction(463670) - Fraction(509555) == -45885
    assert Fraction(1523855) - Fraction(1636208) == -112353
    assert all(r["causality"] == "UNKNOWN" for r in d["rows"])
    assert d["aggregate_delta"] is None


def test_umc_parent_not_group_or_mislabelled_appendix_scope3():
    m = facts("umc_parent_2022_2024.json")
    expected = {
        2022: (591781, 1373914, 2064284),
        2023: (356911, 1376960, 1893167),
        2024: (287393, 1334802, 1416926),
    }
    assert len(m.assertions) == 9
    for row in m.assertions:
        assert int(row.quantity.value) == expected[row.year][row.scope - 1]
        assert "parent" in row.boundary.lower()


def test_tsmc_heldout_literal_alternatives_and_deltas():
    m = facts("tsmc_heldout_2023_2024.json")
    expected = {
        (2023, 1, None): "1596031",
        (2023, 2, "market-based"): "10187387",
        (2023, 2, "location-based"): "11466118",
        (2023, 3, None): "7616655",
        (2024, 1, None): "1825872",
        (2024, 2, "market-based"): "10957397",
        (2024, 2, "location-based"): "12674921",
        (2024, 3, None): "8223173",
    }
    assert {(r.year, r.scope, r.scope2_basis): r.quantity.value for r in m.assertions} == expected
    before = m.model_copy(update={"assertions": tuple(r for r in m.assertions if r.year == 2023)})
    after = m.model_copy(update={"assertions": tuple(r for r in m.assertions if r.year == 2024)})
    d = compare_reported(before, after)
    assert [r["arithmetic_delta_tCO2e"] for r in d["rows"]] == [
        "229841",
        "1208803",
        "770010",
        "606518",
    ]
    assert d["aggregate_delta"] is None
    assert all(r["status"] == "not_assessable" for r in d["rows"])


def test_every_fact_retains_matching_source_hash():
    sources = json.loads((ROOT / "source_manifest.json").read_text())["sources"]
    for name in (
        "umc_group_2022_2024.json",
        "umc_parent_2022_2024.json",
        "tsmc_heldout_2023_2024.json",
    ):
        m = facts(name)
        for row in m.assertions:
            key = "tsmc" if row.id.startswith("tsmc") else "umc"
            assert row.source.sha256 == sources[key]["sha256"]
            assert row.source.url == sources[key]["url"]
            assert row.source.page
