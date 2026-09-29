"""ExampleCo-GHG-001-only fixture arithmetic and generation; not a general inventory engine."""

import argparse
import hashlib
import json
from copy import deepcopy
from decimal import Decimal
from pathlib import Path

from .models import EvidencePackage
from .units import Unit

SEED = 20250926
VERSIONS = ("2025-v1", "2025-v2", "2026-v1")
# name, scope, category, site, unit, activity, factor; all factors invented.
ROWS = (
    ("electricity", 2, None, "tw-plant", "kWh", "1000", "0.5"),
    ("natural-gas", 1, None, "tw-plant", "meter ** 3", "100", "2"),
    ("diesel", 1, None, "vn-plant", "liter", "20", "3"),
    ("fleet", 1, None, "hq", "liter", "30", "2"),
    ("refrigerant", 1, None, "tw-plant", "kg", "2", "1000"),
    ("materials", 3, 1, "tw-plant", "kg", "100", "4"),
    ("capital", 3, 2, "tw-plant", "USD", "1000", "0.2"),
    ("transport", 3, 4, "vn-plant", "tonne * km", "100", "0.1"),
    ("waste", 3, 5, "tw-plant", "kg", "50", "0.2"),
    ("travel", 3, 6, "hq", "km", "100", "0.2"),
    ("commuting", 3, 7, "hq", "km", "100", "0.1"),
    ("supplier-pcf", 3, 1, "vn-plant", "kg", "50", "3"),
    ("method-transition", 3, 1, "tw-plant", "USD", "200", "0.5"),
    ("allocation", 3, 1, "tw-plant", "kg", "100", "2"),
    ("new-line", 1, None, "vn-plant", "liter", "0", "3"),
)


def dumps(value):
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def amount(row):
    """Bounded positive arithmetic. No currency conversion or inferred factors."""
    if row["factor_source"] != "ExampleCo-GHG-001 invented factor sheet v0.1; MIT":
        raise ValueError("factor provenance")
    if (
        row["factor_year"] != row["year"]
        or row["year"] not in (2025, 2026)
        or row["geography"] != {"hq": "TW", "tw-plant": "TW", "vn-plant": "VN"}[row["facility"]]
    ):
        raise ValueError("factor applicability")
    if row["review"] != "synthetic-accepted":
        raise ValueError("manual override not reviewed")
    if row["pcf_boundary"] not in ("not-pcf", "cradle-to-gate-excluding-separate-transport"):
        raise ValueError("unsupported PCF boundary")
    if row["scope2_basis"] == "market-based":
        # No verified contractual instrument is supplied by this benchmark.
        raise ValueError("market-based evidence unavailable; no fallback invented")
    if row["scope2_basis"] not in (None, "location-based"):
        raise ValueError("unknown scope2 basis")
    if (row["scope"] == 2) != (row["scope2_basis"] == "location-based"):
        raise ValueError("scope2 classification")
    if row["stream"] != "fossil-and-nonbiogenic-ghg":
        raise ValueError("separate biogenic/removal/offset stream is not inventory arithmetic")
    q, f, share = (Decimal(row[k]) for k in ("activity", "factor", "allocation_share"))
    if not all(x.is_finite() and x >= 0 for x in (q, f, share)) or share > 1:
        raise ValueError("invalid amount or allocation")
    try:
        Unit(row["unit"]), Unit(row["factor_unit"])
    except ValueError as exc:
        raise ValueError("unsupported unit conversion") from exc
    conversion = {("tonne", "kg"): Decimal(1000)}
    if row["unit"] == row["factor_unit"]:
        scale = Decimal(1)
    else:
        try:
            scale = conversion[(row["unit"], row["factor_unit"])]
        except KeyError as exc:
            raise ValueError("unsupported unit conversion") from exc
    if row["factor_basis"] != "precharacterized-kg-CO2e" or row["apply_gwp"]:
        raise ValueError("no double GWP or unverified gas characterization")
    if row["gwp_basis"] not in ("synthetic-GWP-A-100y", "synthetic-GWP-B-100y") or row[
        "allocation_method"
    ] not in ("none", "mass-share", "economic-share"):
        raise ValueError("missing accounting basis")
    if row["allocation_method"] == "none" and share != 1:
        raise ValueError("allocation share needs method")
    if row["method"] == "supplier-pcf" and row["pcf_boundary"] == "not-pcf":
        raise ValueError("unsupported PCF boundary")
    if row["method"] not in ("supplier-pcf", "spend-based", "activity-based"):
        raise ValueError("unknown method")
    if not row["evidence"].startswith("synthetic://exampleco-ghg-001/"):
        raise ValueError("activity evidence")
    return q * scale * f * share


def preflight(rows):
    if not rows:
        raise ValueError("empty inventory is not zero")
    if len({r["id"] for r in rows}) != len(rows):
        raise ValueError("duplicate activity")
    for row in rows:
        if Decimal(row["reported_kg_co2e"]) != amount(row):
            raise ValueError("reported amount mismatch")
    return rows


def inputs(version, seed=SEED):
    if version not in VERSIONS or type(seed) is not int or seed != SEED:
        raise ValueError("v0.1 supports only the published fixed seed and versions")
    year = int(version[:4])
    rows = []
    for name, scope, category, site, unit, quantity, factor in ROWS:
        row = {
            "id": name,
            "scope": scope,
            "category": category,
            "facility": site,
            "year": year,
            "activity": quantity,
            "unit": unit,
            "factor": factor,
            "factor_unit": unit,
            "factor_year": year,
            "geography": "VN" if site == "vn-plant" else "TW",
            "factor_source": "ExampleCo-GHG-001 invented factor sheet v0.1; MIT",
            "factor_basis": "precharacterized-kg-CO2e",
            "apply_gwp": False,
            "gwp_basis": "synthetic-GWP-A-100y",
            "allocation_share": "1",
            "allocation_method": "none",
            "review": "synthetic-accepted",
            "scope2_basis": "location-based" if scope == 2 else None,
            "stream": "fossil-and-nonbiogenic-ghg",
            "pcf_boundary": "cradle-to-gate-excluding-separate-transport"
            if name == "supplier-pcf"
            else "not-pcf",
            "origin": "estimated" if name == "travel" else "primary",
            "method": "spend-based"
            if unit == "USD"
            else "supplier-pcf"
            if name == "supplier-pcf"
            else "activity-based",
            "evidence": f"synthetic://exampleco-ghg-001/{seed}/{version}/{name}",
            "uncertainty": "Not statistically quantified; invented exact test inputs",
            "coverage": "selected source only",
        }
        if name == "allocation":
            row.update(allocation_share="0.5", allocation_method="mass-share")
        if version != "2025-v1":
            if name == "fleet":
                row["activity"] = "40"
            if name == "travel":
                row.update(activity="150", origin="primary")
        if version == "2026-v1":
            if name == "electricity":
                row.update(activity="800", factor="0.6")
            elif name == "materials":
                row["factor"] = "3"
            elif name == "method-transition":
                row.update(
                    activity="50",
                    unit="kg",
                    factor_unit="kg",
                    factor="1",
                    method="supplier-pcf",
                    pcf_boundary="cradle-to-gate-excluding-separate-transport",
                )
            elif name == "refrigerant":
                row.update(factor="1200", gwp_basis="synthetic-GWP-B-100y")
            elif name == "new-line":
                row["activity"] = "10"
            elif name == "allocation":
                row.update(allocation_share="0.25", allocation_method="economic-share")
        row["reported_kg_co2e"] = str(amount(row))
        rows.append(row)
    return preflight(rows)


def package(version, rows):
    """Map one complete ExampleCo-GHG-001 snapshot to existing canonical records."""
    records = []

    def ref(name):
        return f"urn:ghgag:exampleco-ghg-001-{version}-{name}:v1"

    def add(kind, name, **fields):
        records.append(
            dict(kind=kind, id=ref(name), logical_id=ref(name)[:-3], label=name, **fields)
        )

    add("Organization", "org")
    add("Organization", "reviewer")
    for site, geography in (("hq", "TW"), ("tw-plant", "TW"), ("vn-plant", "VN")):
        add("Facility", site, organization=ref("org"), geography=geography)
    year = version[:4]
    add("ReportingPeriod", "period", start=f"{year}-01-01", end=f"{year}-12-31")
    add(
        "BoundaryDefinition",
        "boundary",
        organization=ref("org"),
        consolidation="operational-control",
        description="ExampleCo-GHG-001 HQ, Taiwan Semiconductor Plant, Vietnam Assembly Plant; "
        "100% operational control. New line in 2026 is organic expansion, not acquisition.",
    )
    add(
        "InventoryVersion",
        "inventory",
        organization=ref("org"),
        period=ref("period"),
        boundary=ref("boundary"),
        status="draft",
    )
    for row in preflight(rows):
        n = row["id"]
        add(
            "EvidenceArtifact",
            n + "-evidence",
            citation=dumps(row),
            license="MIT",
            synthetic=True,
            sha256=hashlib.sha256(dumps(row).encode()).hexdigest(),
        )
        add(
            "DataQualityAssessment",
            n + "-quality",
            rating="unknown",
            rationale="Synthetic scenario; not measured data quality",
            uncertainty=row["uncertainty"],
        )
        add(
            "EmissionSource",
            n + "-source",
            facility=ref(row["facility"]),
            scope=row["scope"],
            category=row["category"],
            scope2_basis=row["scope2_basis"],
        )
        add(
            "ActivityRecord",
            n + "-activity",
            source=ref(n + "-source"),
            inventory=ref("inventory"),
            quantity={"value": float(row["activity"]), "unit": row["unit"]},
            evidence=ref(n + "-evidence"),
            quality=ref(n + "-quality"),
            data_origin=row["origin"],
        )
        add(
            "GWPSet",
            n + "-gwp",
            basis=row["gwp_basis"],
            horizon_years=100,
            evidence=ref(n + "-evidence"),
        )
        add(
            "CalculationMethod",
            n + "-method",
            method_type=row["method"],
            description="ExampleCo-GHG-001 activity x synthetic precharacterized CO2e factor; allocation "
            "embedded exactly once in canonical factor",
            allocation=row["allocation_method"],
            evidence=ref(n + "-evidence"),
        )
        add(
            "EmissionFactor",
            n + "-factor",
            value=float(Decimal(row["factor"]) * Decimal(row["allocation_share"])),
            numerator="kg_CO2e",
            denominator=row["factor_unit"],
            evidence=ref(n + "-evidence"),
            period=ref("period"),
            geography=row["geography"],
            gwp=ref(n + "-gwp"),
            boundary=ref("boundary"),
            method=ref(n + "-method"),
        )
        add(
            "CalculationRun",
            n + "-run",
            activity=ref(n + "-activity"),
            factor=ref(n + "-factor"),
            method=ref(n + "-method"),
            gwp=ref(n + "-gwp"),
            boundary=ref("boundary"),
            inventory=ref("inventory"),
            performed_at="2026-09-26T00:00:00Z",
            software="exampleco-ghg-001/0.1",
        )
        add(
            "EmissionResult",
            n + "-result",
            calculation=ref(n + "-run"),
            inventory=ref("inventory"),
            quantity={"value": float(amount(row)), "unit": "kg_CO2e"},
            review=ref(n + "-review"),
        )
        add(
            "ReviewDecision",
            n + "-review",
            target=ref(n + "-result"),
            reviewer=ref("reviewer"),
            status="accepted",
            timestamp="2026-09-26T00:00:00Z",
            rationale="Simulated benchmark acceptance only; no human assurance",
        )
    return EvidencePackage.model_validate({"records": records})


# Deliberate raw mutations, never passed off as clean canonical packages.
MUTATIONS = {
    "unit-error": ("materials", "unit", "tonne"),
    "missing-factor-source": ("natural-gas", "factor_source", ""),
    "wrong-factor-year": ("electricity", "factor_year", 2020),
    "unsupported-pcf": ("supplier-pcf", "pcf_boundary", "gate-to-gate-unknown-exclusions"),
    "manual-override": ("fleet", "review", "unreviewed"),
    "double-gwp": ("refrigerant", "apply_gwp", True),
    "missing-contract": ("electricity", "scope2_basis", "market-based"),
    "unknown-unit": ("diesel", "unit", "gallon-ambiguous"),
    "offset-netting": ("waste", "stream", "offset"),
}


def generate(out, seed=SEED):
    out = Path(out)
    hashes = {}

    def emit(name, data):
        raw = dumps(data).encode()
        path = out / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        hashes[name] = hashlib.sha256(raw).hexdigest()

    for version in VERSIONS:
        rows = inputs(version, seed)
        emit(f"{version}/inputs.json", rows)
        emit(f"{version}/package.json", package(version, rows).model_dump(mode="json"))
    for case, (entity, field, value) in MUTATIONS.items():
        rows = deepcopy(inputs("2025-v1", seed))
        next(r for r in rows if r["id"] == entity)[field] = value
        emit(f"defects/{case}.json", {"nonconforming": True, "base": "2025-v1", "rows": rows})
    rows = inputs("2025-v1", seed)
    rows.append(deepcopy(rows[0]))
    emit(
        "defects/duplicate-activity.json", {"nonconforming": True, "base": "2025-v1", "rows": rows}
    )
    emit("manifest.json", {"benchmark": "0.1", "seed": seed, "sha256": hashes})
    return hashes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("benchmark/generated"))
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    generate(args.out, args.seed)


if __name__ == "__main__":
    main()
