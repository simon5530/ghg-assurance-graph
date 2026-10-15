"""Independent numeric and failure-path oracles for the MOENV training case."""

import csv
import hashlib
import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path

import pytest

from ghg_assurance_graph.moenv_example import (
    FORMS,
    activity_rows,
    build,
    canonical,
    check_collection,
    quantify,
    totals,
    validate_activity,
)

ROOT = Path(__file__).parents[1] / "examples/moenv_training/sample"


@pytest.mark.parametrize("year,expected", [(2023, "95797.473564"), (2024, "95229.409244")])
def test_literal_totals_and_independent_gas_arithmetic(year, expected):
    rows, docs = activity_rows(year)
    gases = quantify(rows, docs, year)
    # Independent rational oracle, literal factors/LHV/GWP, not production tables.
    factors = {
        "boiler": Fraction(38, 1000000) * (56100 + 28 + Fraction(1, 10) * 265),
        "generator": Fraction(36, 1000000) * (74100 + 3 * 28 + Fraction(6, 10) * 265),
        "new-generator": Fraction(36, 1000000) * (74100 + 3 * 28 + Fraction(6, 10) * 265),
        "cooling": Fraction(1300),
        "electricity": Fraction("0.494" if year == 2023 else "0.474"),
    }
    oracle = sum(Fraction(r["quantity"]) * factors[r["source_id"]] for r in rows)
    assert oracle == Fraction(expected) == Fraction(totals(gases)[2])
    assert len(rows) == 60 and len(docs) == 60
    package = canonical(year, rows, docs, gases)
    results = [r for r in package.records if r.kind == "EmissionResult"]
    assert len(results) == (4 if year == 2023 else 5)
    assert sum(Fraction(str(r.quantity.value)) for r in results) == oracle
    assert all(r.status == "unreviewed" for r in package.records if r.kind == "ReviewDecision")


@pytest.mark.parametrize(
    "mutation",
    [
        "blank",
        "missing-row",
        "duplicate",
        "unit",
        "period",
        "hash",
        "source-doc",
        "cutoff",
        "negative",
        "nonfinite",
        "missing-evidence",
    ],
)
def test_fail_closed_activity_contract(mutation):
    rows, docs = activity_rows(2024)
    rows, docs = deepcopy(rows), deepcopy(docs)
    if mutation == "blank":
        rows[0]["quantity"] = ""
    elif mutation == "missing-row":
        rows.pop()
    elif mutation == "duplicate":
        rows.append(deepcopy(rows[0]))
    elif mutation == "unit":
        rows[0]["unit"] = "liter"
    elif mutation == "period":
        rows[0]["year"] = 2023
    elif mutation == "hash":
        rows[0]["evidence_sha256"] = "0" * 64
    elif mutation == "source-doc":
        eid = rows[0]["evidence_id"]
        docs[eid] = docs[eid].replace(b'"quantity": "910"', b'"quantity": "911"')
        rows[0]["evidence_sha256"] = hashlib.sha256(docs[eid]).hexdigest()
    elif mutation == "cutoff":
        row = next(r for r in rows if r["source_id"] == "new-generator")
        row["data_status"] = "recorded"
    elif mutation == "negative":
        rows[0]["quantity"] = "-1"
    elif mutation == "nonfinite":
        rows[0]["quantity"] = "NaN"
    else:
        del docs[rows[0]["evidence_id"]]
    with pytest.raises(ValueError):
        validate_activity(rows, docs, 2024)


def test_replay_committed_tree_and_no_overwrite(tmp_path):
    out = tmp_path / "case"
    build(out)
    # Turtle blank-node serialization is not a byte-identity contract. Compare
    # graph isomorphism separately; structured input/output files are byte stable.
    from rdflib import Graph
    from rdflib.compare import isomorphic

    for path in ROOT.rglob("*"):
        if not path.is_file() or path.name in ("manifest.json",) or path.suffix == ".xlsx":
            continue
        replay = out / path.relative_to(ROOT)
        if path.suffix == ".ttl":
            assert isomorphic(Graph().parse(path), Graph().parse(replay))
        else:
            assert replay.read_bytes() == path.read_bytes(), path
    before = (out / "summary.json").read_bytes()
    with pytest.raises(ValueError, match="refusing to overwrite"):
        build(out)
    assert before == (out / "summary.json").read_bytes()
    for year in (2023, 2024):
        checked = check_collection(ROOT / str(year))
        assert checked["checked_monthly_documents"] == 60
        index = list(csv.DictReader((ROOT / str(year) / "12-evidence.csv").open()))
        assert len(index) == 61
        for item in index:
            raw = (ROOT / str(year) / item["path"]).read_bytes()
            assert hashlib.sha256(raw).hexdigest() == item["sha256"]
        assert all((ROOT / str(year) / (form + ".csv")).is_file() for form in FORMS)
        assert len(list(csv.DictReader((ROOT / str(year) / "07-uncertainty.csv").open()))) == 5
    manifest = json.loads((ROOT / "manifest.json").read_text())
    for name, digest in manifest["sha256"].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest


def test_changed_saved_inputs_do_not_silently_pass(tmp_path):
    out = tmp_path / "case"
    build(out)
    folder = out / "2024"
    path = folder / "04-activity.csv"
    original = path.read_text()
    path.write_text(original.replace(",boiler,910,", ",boiler,911,", 1))
    with pytest.raises(ValueError, match="disagree"):
        check_collection(folder)
    path.write_text(original)
    result = folder / "05-quantification.csv"
    result.write_text(result.read_text().replace("24761.244", "24761.245", 1))
    # Explicitly change a known gas result, not an unrelated metadata string.
    with result.open() as stream:
        rows = list(csv.DictReader(stream))
    rows[0]["kg_co2e"] = "1"
    with result.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError, match="gas calculation"):
        check_collection(folder)
