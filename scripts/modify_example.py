"""Safe, isolated electricity exercise; regenerate canonical evidence, never patch results."""

import argparse
from fractions import Fraction
from pathlib import Path

from ghg_assurance_graph.benchmark import amount, dumps, inputs, package, preflight
from ghg_assurance_graph.validation import validate_package, validate_rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        parser.error("output must be new; refusing to overwrite")
    rows = inputs("2025-v1")
    row = next(r for r in rows if r["id"] == "electricity")
    row["activity"] = "1100"
    row["reported_kg_co2e"] = str(amount(row))
    preflight(rows)
    model = package("2025-v1", rows)
    assert not validate_rows(rows)
    assert not validate_package(model)
    total = sum(
        Fraction(r["activity"]) * Fraction(r["factor"]) * Fraction(r["allocation_share"])
        for r in rows
    )
    assert total == 3870
    args.out.mkdir(parents=True)
    (args.out / "inputs.json").write_text(dumps(rows))
    (args.out / "package.json").write_text(model.model_dump_json(indent=2) + chr(10))
    print(
        dumps(
            {
                "electricity_kg_co2e": 550,
                "total_kg_co2e": int(total),
                "delta_kg_co2e": 50,
                "exercise_only": True,
            }
        )
    )


if __name__ == "__main__":
    main()
