"""MOENV-inspired training case, not a statutory filing or general inventory engine.

Decimal CSV inputs are authoritative; the existing graph receives declared
precharacterized CO2e factors only after gas-level arithmetic is checked.
"""

import argparse
import csv
import hashlib
import io
import json
from decimal import Decimal
from pathlib import Path

from .models import EvidencePackage

YEARS = (2023, 2024)
STAMP = "2026-10-15T00:00:00Z"
SOURCES = {
    "boiler": ("天然氣鍋爐", "meter ** 3", 1, "固定燃燒", "天然氣", "CO2;CH4;N2O"),
    "generator": ("柴油備援發電機", "liter", 1, "固定燃燒", "柴油", "CO2;CH4;N2O"),
    "new-generator": ("新增柴油備援發電機", "liter", 1, "固定燃燒", "柴油", "CO2;CH4;N2O"),
    "cooling": ("HFC-134a空調系統", "kg", 1, "逸散", "HFC-134a", "HFCs"),
    "electricity": ("外購電力總表", "kWh", 2, "外購電力", "電力", "CO2e"),
}
GWP = {"CO2": "1", "CH4": "28", "N2O": "265", "HFC-134a": "1300", "CO2e": "1"}
# Official kg gas/TJ (fixed combustion); LHV below is deliberately synthetic.
COMBUSTION = {
    "boiler": {"CO2": "56100", "CH4": "1", "N2O": "0.1"},
    "generator": {"CO2": "74100", "CH4": "3", "N2O": "0.6"},
    "new-generator": {"CO2": "74100", "CH4": "3", "N2O": "0.6"},
}
LHV = {"boiler": "38", "generator": "36", "new-generator": "36"}  # MJ/unit
ELECTRICITY = {2023: "0.494", 2024: "0.474"}  # inspected ODS Annex 1; vintage replay

# Internal collection design, not a byte-for-byte copy of the filing workbook.
FORMS = {
    "01-entity": (
        "year",
        "organization",
        "facility_id",
        "registration_id",
        "industry",
        "owner_role",
        "contact_role",
        "assurance_status",
        "synthetic",
    ),
    "02-boundary": (
        "year",
        "facility_id",
        "boundary",
        "site_plan_evidence",
        "exclusions",
        "reason",
        "synthetic",
    ),
    "03-sources": (
        "year",
        "source_id",
        "source_name",
        "process_id",
        "equipment_id",
        "material",
        "direct_or_energy_indirect",
        "emission_type",
        "gases",
        "biomass",
        "cogeneration",
        "status",
        "start_date",
        "end_date",
        "evidence_id",
    ),
    "04-activity": (
        "year",
        "month",
        "source_id",
        "quantity",
        "unit",
        "data_status",
        "evidence_id",
        "evidence_sha256",
        "custodian",
        "measurement_frequency",
        "instrument",
        "calibration",
        "allocation_share",
        "method",
        "synthetic",
    ),
    "05-quantification": (
        "year",
        "source_id",
        "gas",
        "activity",
        "unit",
        "lhv_mj_per_unit",
        "factor",
        "factor_unit",
        "factor_source_id",
        "gwp",
        "gwp_basis",
        "gas_kg",
        "kg_co2e",
        "synthetic",
    ),
    "06-quality": (
        "year",
        "source_id",
        "activity_quality",
        "factor_quality",
        "calibration_evidence",
        "custodian",
        "review_status",
        "limitation",
    ),
    "07-uncertainty": (
        "year",
        "source_id",
        "activity_uncertainty_pct",
        "factor_uncertainty_pct",
        "confidence_level",
        "distribution",
        "correlation",
        "status",
        "reason",
    ),
    "08-summary": (
        "year",
        "direct_kg_co2e",
        "energy_indirect_kg_co2e",
        "total_kg_co2e",
        "total_t_co2e",
        "boundary",
        "status",
    ),
    "09-energy": (
        "year",
        "purchased_kwh",
        "self_generated_kwh",
        "sold_kwh",
        "purchased_steam_t",
        "generated_steam_t",
        "sold_steam_t",
        "evidence_id",
        "note",
    ),
    "10-production": (
        "year",
        "process_id",
        "product",
        "production",
        "unit",
        "operating_days",
        "hours_per_day",
        "evidence_id",
    ),
    "11-tests": (
        "year",
        "source_id",
        "parameter",
        "value",
        "unit",
        "test_method",
        "test_date",
        "laboratory",
        "qualification",
        "evidence_id",
        "status",
    ),
    "12-evidence": (
        "evidence_id",
        "path",
        "sha256",
        "year",
        "month",
        "source_id",
        "custodian",
        "synthetic",
        "license",
    ),
    "13-changes": (
        "change_id",
        "source_id",
        "effective_date",
        "change_type",
        "before",
        "after",
        "evidence_id",
        "comparability",
        "review_status",
    ),
}


def encode(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def csv_bytes(columns, rows):
    text = io.StringIO(newline="")
    writer = csv.DictWriter(text, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return text.getvalue().encode("utf-8")


def monthly(year, source, month):
    if source == "boiler":
        return str((1000 if year == 2023 else 900) + month * 10)
    if source == "generator":
        return str((40 if year == 2023 else 35) + month)
    if source == "new-generator":
        return "0" if year == 2023 or month < 7 else "20"
    if source == "cooling":
        return ("3" if year == 2023 else "2") if month == 8 else "0"
    return str((10000 if year == 2023 else 11000) + month * 100)


def activity_rows(year):
    rows, docs = [], {}
    for source, (_, unit, *_) in SOURCES.items():
        for month in range(1, 13):
            eid = f"{year}-{source}-{month:02}"
            inactive = source == "new-generator" and (year == 2023 or month < 7)
            doc = {
                "synthetic": True,
                "license": "MIT",
                "evidence_id": eid,
                "year": year,
                "month": month,
                "source_id": source,
                "quantity": monthly(year, source, month),
                "unit": unit,
                "document_type": "synthetic maintenance/meter/consumption record",
                "status": "not-operating" if inactive else "recorded",
                "note": "Cooling quantity is documented leaked gas mass from a closed synthetic service balance, not equipment charge or purchased refrigerant. Fuel quantity is consumption after stock reconciliation, not purchases. No actual invoice or human approval.",
            }
            quantity = Decimal(doc["quantity"])
            if source in ("boiler", "electricity"):
                opening = Decimal(100000) + sum(
                    Decimal(monthly(year, source, m)) for m in range(1, month)
                )
                doc["raw_data"] = {
                    "basis": "meter-difference",
                    "opening": str(opening),
                    "closing": str(opening + quantity),
                    "multiplier": "1",
                }
            elif source in ("generator", "new-generator"):
                doc["raw_data"] = {
                    "basis": "fuel-stock-balance",
                    "opening": "100",
                    "purchased": str(quantity),
                    "closing": "100",
                }
            else:
                doc["raw_data"] = {
                    "basis": "refrigerant-mass-balance",
                    "opening": "10",
                    "added": str(quantity),
                    "recovered": "0",
                    "closing": "10",
                }
            raw = encode(doc)
            docs[eid] = raw
            rows.append(
                {
                    "year": year,
                    "month": month,
                    "source_id": source,
                    "quantity": doc["quantity"],
                    "unit": unit,
                    "data_status": doc["status"],
                    "evidence_id": eid,
                    "evidence_sha256": hashlib.sha256(raw).hexdigest(),
                    "custodian": "simulated-facilities-team",
                    "measurement_frequency": "monthly",
                    "instrument": "synthetic-log",
                    "calibration": "not-established",
                    "allocation_share": "1",
                    "method": "documented-consumption-or-leakage",
                    "synthetic": True,
                }
            )
    return rows, docs


def validate_activity(rows, docs, year):
    """Reject gaps and corruption; zero needs evidence and is not a missing value."""
    expected = {(source, month) for source in SOURCES for month in range(1, 13)}
    seen = set()
    for row in rows:
        key = (row["source_id"], int(row["month"]))
        if key in seen or key not in expected or int(row["year"]) != year:
            raise ValueError("duplicate, unknown source/month or wrong reporting period")
        seen.add(key)
        if row["unit"] != SOURCES[key[0]][1] or str(row["allocation_share"]) != "1":
            raise ValueError("unit or allocation mismatch")
        if not isinstance(row["quantity"], str) or not row["quantity"].strip():
            raise ValueError("blank quantity is not zero")
        value = Decimal(row["quantity"])
        if not value.is_finite() or value < 0:
            raise ValueError("invalid quantity")
        raw = docs.get(row["evidence_id"])
        if raw is None or hashlib.sha256(raw).hexdigest() != row["evidence_sha256"]:
            raise ValueError("missing evidence or digest mismatch")
        doc = json.loads(raw)
        if any(
            str(doc[k]) != str(row[k]) for k in ("year", "month", "source_id", "quantity", "unit")
        ):
            raise ValueError("evidence and activity disagree")
        if doc["synthetic"] is not True or row["data_status"] != doc["status"]:
            raise ValueError("synthetic/status mismatch")
        original = doc["raw_data"]
        if original["basis"] == "meter-difference":
            derived = (Decimal(original["closing"]) - Decimal(original["opening"])) * Decimal(
                original["multiplier"]
            )
        elif original["basis"] == "fuel-stock-balance":
            derived = (
                Decimal(original["opening"])
                + Decimal(original["purchased"])
                - Decimal(original["closing"])
            )
        elif original["basis"] == "refrigerant-mass-balance":
            derived = (
                Decimal(original["opening"])
                + Decimal(original["added"])
                - Decimal(original["recovered"])
                - Decimal(original["closing"])
            )
        else:
            raise ValueError("unsupported raw-data method")
        if derived != value:
            raise ValueError("raw evidence does not reconcile to activity")
        inactive = key[0] == "new-generator" and (year == 2023 or key[1] < 7)
        if inactive != (row["data_status"] == "not-operating") or (inactive and value != 0):
            raise ValueError("equipment operation cutoff mismatch")
    if seen != expected:
        raise ValueError("missing source/month; do not impute zero")


def quantify(rows, docs, year):
    validate_activity(rows, docs, year)
    result = []
    for source, (_, unit, *_rest) in SOURCES.items():
        if source == "new-generator" and year == 2023:
            continue
        activity = sum(Decimal(r["quantity"]) for r in rows if r["source_id"] == source)
        gases = COMBUSTION.get(
            source, {"HFC-134a": "1"} if source == "cooling" else {"CO2e": ELECTRICITY[year]}
        )
        for gas, factor in gases.items():
            lhv = LHV.get(source)
            gas_kg = activity * Decimal(factor)
            if lhv:
                gas_kg *= Decimal(lhv) / Decimal(1000000)  # MJ -> TJ exactly once
            co2e = gas_kg * Decimal(GWP[gas])
            result.append(
                {
                    "year": year,
                    "source_id": source,
                    "gas": gas,
                    "activity": str(activity),
                    "unit": unit,
                    "lhv_mj_per_unit": lhv or "not-applicable",
                    "factor": factor,
                    "factor_unit": "kg-gas/TJ"
                    if lhv
                    else ("kg-gas/kg-leaked" if source == "cooling" else "kg-CO2e/kWh"),
                    "factor_source_id": "official-factors"
                    if lhv or source == "cooling"
                    else "official-inventory-annex1",
                    "gwp": GWP[gas],
                    "gwp_basis": "MOENV-113-AR5-100y"
                    if gas != "CO2e"
                    else "precharacterized-no-second-GWP",
                    "gas_kg": str(gas_kg) if gas != "CO2e" else "not-gas-resolved",
                    "kg_co2e": str(co2e),
                    "synthetic": True,
                }
            )
    return result


def totals(rows):
    direct = sum(Decimal(r["kg_co2e"]) for r in rows if SOURCES[r["source_id"]][2] == 1)
    indirect = sum(Decimal(r["kg_co2e"]) for r in rows if SOURCES[r["source_id"]][2] == 2)
    return direct, indirect, direct + indirect


def canonical(year, activities, docs, gas_rows):
    records = []

    def ref(name):
        return f"urn:ghgag:moenv-demo-{year}-{name}:v1"

    def add(kind, name, **values):
        records.append(
            dict(kind=kind, id=ref(name), logical_id=ref(name)[:-3], label=name, **values)
        )

    add("Organization", "organization")
    add("Organization", "simulated-review-role")
    add("Facility", "plant", organization=ref("organization"), geography="TW")
    add("ReportingPeriod", "period", start=f"{year}-01-01", end=f"{year}-12-31")
    add(
        "BoundaryDefinition",
        "boundary",
        organization=ref("organization"),
        consolidation="operational-control",
        description="Fictional single registered manufacturing site; one plant, no subsidiaries; no claim of legal registration. Direct and purchased-energy sources only; no Scope 3 conformity claim.",
    )
    add(
        "InventoryVersion",
        "inventory",
        organization=ref("organization"),
        period=ref("period"),
        boundary=ref("boundary"),
        status="draft",
    )
    for source, (_, unit, scope, *_rest) in SOURCES.items():
        components = [r for r in gas_rows if r["source_id"] == source]
        if not components:
            continue
        source_rows = [r for r in activities if r["source_id"] == source]
        # A canonical artifact cites an annual evidence bundle. Monthly files and
        # hashes remain independently checkable in the companion collection pack.
        bundle = {
            "synthetic": True,
            "monthly_evidence": [
                {
                    "id": r["evidence_id"],
                    "sha256": hashlib.sha256(docs[r["evidence_id"]]).hexdigest(),
                }
                for r in source_rows
            ],
        }
        for suffix, body in (
            ("activity-evidence", bundle),
            (
                "factor-evidence",
                {
                    "synthetic_case": True,
                    "components": components,
                    "warning": "LHV is synthetic. Electricity factor vintages replay inspected historical ODS rows, not latest-factor regulatory compliance.",
                },
            ),
        ):
            add(
                "EvidenceArtifact",
                source + "-" + suffix,
                citation=encode(body).decode().strip(),
                license="MIT (original synthetic bundle; official citations are external)",
                synthetic=True,
                sha256=hashlib.sha256(encode(body)).hexdigest(),
            )
        add(
            "DataQualityAssessment",
            source + "-quality",
            rating="unknown",
            rationale="Synthetic exercise; not independently assessed",
            uncertainty="not quantified; see form 07",
        )
        add(
            "EmissionSource",
            source + "-source",
            facility=ref("plant"),
            scope=scope,
            category=None,
            scope2_basis="location-based" if scope == 2 else None,
        )
        activity = Decimal(components[0]["activity"])
        amount = sum(Decimal(r["kg_co2e"]) for r in components)
        add(
            "ActivityRecord",
            source + "-activity",
            source=ref(source + "-source"),
            inventory=ref("inventory"),
            quantity={"value": float(activity), "unit": unit},
            evidence=ref(source + "-activity-evidence"),
            quality=ref(source + "-quality"),
            data_origin="primary",
        )
        add(
            "GWPSet",
            source + "-gwp",
            basis="MOENV-113-AR5-100y; precharacterized gas sum (do not apply twice)",
            horizon_years=100,
            evidence=ref(source + "-factor-evidence"),
        )
        add(
            "CalculationMethod",
            source + "-method",
            method_type="activity-based",
            description="Gas-resolved Decimal companion calculation projected to an explicit precharacterized CO2e factor; not a gas-resolved core schema",
            allocation="none",
            evidence=ref(source + "-factor-evidence"),
        )
        add(
            "EmissionFactor",
            source + "-factor",
            value=float(amount / activity),
            numerator="kg_CO2e",
            denominator=unit,
            evidence=ref(source + "-factor-evidence"),
            period=ref("period"),
            geography="TW",
            gwp=ref(source + "-gwp"),
            boundary=ref("boundary"),
            method=ref(source + "-method"),
        )
        add(
            "CalculationRun",
            source + "-run",
            activity=ref(source + "-activity"),
            factor=ref(source + "-factor"),
            method=ref(source + "-method"),
            gwp=ref(source + "-gwp"),
            boundary=ref("boundary"),
            inventory=ref("inventory"),
            performed_at=STAMP,
            software="moenv-training/1",
        )
        add(
            "EmissionResult",
            source + "-result",
            calculation=ref(source + "-run"),
            inventory=ref("inventory"),
            quantity={"value": float(amount), "unit": "kg_CO2e"},
            review=ref(source + "-review"),
        )
        add(
            "ReviewDecision",
            source + "-review",
            target=ref(source + "-result"),
            reviewer=ref("simulated-review-role"),
            status="unreviewed",
            timestamp=STAMP,
            rationale="Training fixture only; no human approval or assurance performed",
        )
    return EvidencePackage.model_validate({"records": records})


def build(out):
    out = Path(out)
    if out.exists():
        raise ValueError("output must not exist; refusing to overwrite")
    out.mkdir(parents=True)
    all_totals = {}

    def emit(path, raw):
        target = out / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)

    for form, columns in FORMS.items():
        emit(f"templates/{form}.csv", csv_bytes(columns, []))
    for year in YEARS:
        rows, docs = activity_rows(year)
        gas = quantify(rows, docs, year)
        direct, indirect, total = totals(gas)
        all_totals[str(year)] = {
            "direct_kg_co2e": str(direct),
            "energy_indirect_kg_co2e": str(indirect),
            "total_kg_co2e": str(total),
        }
        tables = {f: [] for f in FORMS}
        tables["01-entity"] = [
            {
                "year": year,
                "organization": "示範製造廠（完全虛構）",
                "facility_id": "demo-plant",
                "registration_id": "NOT-A-REAL-REGISTRATION",
                "industry": "generic-manufacturing-training",
                "owner_role": "simulated-manager",
                "contact_role": "simulated-coordinator",
                "assurance_status": "not-assured",
                "synthetic": True,
            }
        ]
        tables["02-boundary"] = [
            {
                "year": year,
                "facility_id": "demo-plant",
                "boundary": "single fictional plant under operational control",
                "site_plan_evidence": "scenario",
                "exclusions": "onsite process gas; SF6/PFC/NF3; onsite wastewater; purchased steam; biomass",
                "reason": "scenario has no relevant process/equipment; sanitary wastewater discharged to public sewer with no onsite anaerobic treatment; verify in any real application",
                "synthetic": True,
            }
        ]
        for source, (name, _unit, scope, typ, material, gases) in SOURCES.items():
            tables["03-sources"].append(
                {
                    "year": year,
                    "source_id": source,
                    "source_name": name,
                    "process_id": "demo-utilities",
                    "equipment_id": source,
                    "material": material,
                    "direct_or_energy_indirect": "direct" if scope == 1 else "energy-indirect",
                    "emission_type": typ,
                    "gases": gases,
                    "biomass": False,
                    "cogeneration": False,
                    "status": "not-installed"
                    if source == "new-generator" and year == 2023
                    else "included",
                    "start_date": "2024-07-01" if source == "new-generator" else "before-2023",
                    "end_date": "ongoing",
                    "evidence_id": "scenario",
                }
            )
            tables["06-quality"].append(
                {
                    "year": year,
                    "source_id": source,
                    "activity_quality": "synthetic-not-rated",
                    "factor_quality": "official-values-plus-synthetic-LHV",
                    "calibration_evidence": "not-established",
                    "custodian": "simulated-facilities-team",
                    "review_status": "not-human-reviewed",
                    "limitation": "hashes prove consistency only, not source authenticity",
                }
            )
            tables["07-uncertainty"].append(
                {
                    "year": year,
                    "source_id": source,
                    "activity_uncertainty_pct": "",
                    "factor_uncertainty_pct": "",
                    "confidence_level": "",
                    "distribution": "",
                    "correlation": "unknown",
                    "status": "not-assessed",
                    "reason": "no actual instrument calibration, distribution or confidence evidence; blank is not zero",
                }
            )
            if source in LHV:
                tables["11-tests"].append(
                    {
                        "year": year,
                        "source_id": source,
                        "parameter": "lower-heating-value",
                        "value": LHV[source],
                        "unit": "MJ/activity-unit",
                        "test_method": "synthetic-assumption-not-laboratory",
                        "test_date": "not-performed",
                        "laboratory": "none",
                        "qualification": "not-established",
                        "evidence_id": "scenario",
                        "status": "synthetic-not-measured",
                    }
                )
        tables["04-activity"] = rows
        tables["05-quantification"] = gas
        tables["08-summary"] = [
            dict(
                year=year,
                **all_totals[str(year)],
                total_t_co2e=str(total / 1000),
                boundary="demo-plant; direct + purchased energy",
                status="synthetic-not-assured",
            )
        ]
        purchased = sum(Decimal(r["quantity"]) for r in rows if r["source_id"] == "electricity")
        tables["09-energy"] = [
            {
                "year": year,
                "purchased_kwh": str(purchased),
                "self_generated_kwh": "1200" if year == 2023 else "1440",
                "sold_kwh": "0",
                "purchased_steam_t": "0",
                "generated_steam_t": "0",
                "sold_steam_t": "0",
                "evidence_id": "scenario",
                "note": "synthetic generator electricity used onsite; do not add it again as purchased electricity; boiler produces hot water, not steam",
            }
        ]
        tables["10-production"] = [
            {
                "year": year,
                "process_id": "demo-production",
                "product": "fictional metal components",
                "production": "12000" if year == 2023 else "13200",
                "unit": "pieces",
                "operating_days": "250",
                "hours_per_day": "8",
                "evidence_id": "scenario",
            }
        ]
        for r in rows:
            eid = r["evidence_id"]
            emit(f"{year}/evidence/{eid}.json", docs[eid])
            tables["12-evidence"].append(
                {
                    "evidence_id": eid,
                    "path": f"evidence/{eid}.json",
                    "sha256": r["evidence_sha256"],
                    "year": year,
                    "month": r["month"],
                    "source_id": r["source_id"],
                    "custodian": r["custodian"],
                    "synthetic": True,
                    "license": "MIT",
                }
            )
        scenario = {
            "synthetic": True,
            "license": "MIT",
            "boundary": tables["02-boundary"],
            "source_register": tables["03-sources"],
            "energy": tables["09-energy"],
            "production": tables["10-production"],
            "tests": tables["11-tests"],
            "event": "new-generator installed 2024-07-01; no organizational acquisition",
            "LHV": LHV,
            "GWP": GWP,
            "electricity_factor_policy": "historical-vintage replay, not latest-factor compliance",
        }
        emit(f"{year}/evidence/scenario.json", encode(scenario))
        tables["12-evidence"].append(
            {
                "evidence_id": "scenario",
                "path": "evidence/scenario.json",
                "sha256": hashlib.sha256(encode(scenario)).hexdigest(),
                "year": year,
                "month": "annual",
                "source_id": "all",
                "custodian": "simulated-coordinator",
                "synthetic": True,
                "license": "MIT",
            }
        )
        if year == 2024:
            tables["13-changes"] = [
                {
                    "change_id": "new-equipment-2024",
                    "source_id": "new-generator",
                    "effective_date": "2024-07-01",
                    "change_type": "organic-equipment-addition",
                    "before": "not installed",
                    "after": "installed; six months consumption",
                    "evidence_id": "scenario",
                    "comparability": "same plant boundary, source composition changed; not acquisition",
                    "review_status": "synthetic-not-human-reviewed",
                },
                {
                    "change_id": "electricity-vintage-2024",
                    "source_id": "electricity",
                    "effective_date": "2024-01-01",
                    "change_type": "factor-vintage-change",
                    "before": "0.494 kgCO2e/kWh",
                    "after": "0.474 kgCO2e/kWh",
                    "evidence_id": "scenario",
                    "comparability": "activity-first/factor-second convention; not uniquely causal abatement",
                    "review_status": "synthetic-not-human-reviewed",
                },
            ]
        for form, values in tables.items():
            emit(f"{year}/{form}.csv", csv_bytes(FORMS[form], values))
        package = canonical(year, rows, docs, gas)
        emit(f"{year}/package.json", encode(package.model_dump(mode="json")))
        from .graph import build_graph

        turtle = build_graph([package]).serialize(format="turtle").rstrip() + "\n"
        emit(f"{year}/graph.ttl", turtle.encode())
        report = f"# {year} 年示範盤查報告（合成資料，非查驗聲明）\n\n"
        sections = [
            "公司基本資料",
            "盤查邊界設定",
            "排放源鑑別",
            "排放量計算",
            "數據品質管理",
            "其他事項及減量措施",
        ]
        texts = [
            "完全虛構的單一製造廠。詳表一；不使用真實統編、地址或人名。",
            "單一虛構廠場；詳表二及 scenario.json。無真實法定邊界證書。",
            "詳表三及變更表；製程：原料→電動加工→組裝→成品，廠務提供熱水/備援電力/空調。",
            f"直接排放 {direct} kgCO2e；能源間接 {indirect} kgCO2e；合計 {total / 1000} tCO2e。逐月資料→氣體計算→圖譜見表四、五、八。",
            "品質及不確定性尚未實測或量化；詳表六、七、十一。未填不是零。",
            "跨期變動不是已證實減量；新設備與係數變動見表十三。無抵換、移除或市場基礎聲明。",
        ]
        for i, (heading, text) in enumerate(zip(sections, texts, strict=True), 1):
            report += f"## 第{i}章 {heading}\n\n{text}\n\n"
        report += "官方參考章節結構經原創改寫；不是官方申報檔，亦不宣稱符合全部法規或 ISO。\n"
        emit(f"{year}/REPORT.zh-TW.md", report.encode())
    emit(
        "summary.json",
        encode(
            {
                "profile": "moenv-training/1",
                "synthetic": True,
                "years": all_totals,
                "limitations": "historical electricity vintages; synthetic LHV/activity; no independent assurance or quantified uncertainty",
            }
        ),
    )
    hashes = {
        p.relative_to(out).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(out.rglob("*"))
        if p.is_file()
    }
    emit("manifest.json", encode({"profile": "moenv-training/1", "sha256": hashes}))
    return all_totals


def check_collection(folder):
    """Check collected CSV against actual monthly documents and declared gas results.

    This checks the training profile only; it never certifies arbitrary inventory
    methods or silently repairs altered input.
    """
    folder = Path(folder)
    with (folder / "04-activity.csv").open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != FORMS["04-activity"]:
            raise ValueError("activity header does not match training profile")
        rows = list(reader)
    if not rows:
        raise ValueError("empty collection is not a zero inventory")
    year = int(rows[0]["year"])
    if year not in YEARS:
        raise ValueError("training profile supports only the declared example years")
    docs = {}
    for row in rows:
        eid = row["evidence_id"]
        if not eid or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in eid):
            raise ValueError("unsafe evidence identifier")
        target = folder / "evidence" / (eid + ".json")
        if target.is_symlink():
            raise ValueError("evidence symlink is not permitted")
        docs[eid] = target.read_bytes()
    gas = quantify(rows, docs, year)
    if (folder / "05-quantification.csv").read_bytes() != csv_bytes(
        FORMS["05-quantification"], gas
    ):
        raise ValueError("gas calculation does not match collected inputs")
    direct, indirect, total = totals(gas)
    with (folder / "08-summary.csv").open(newline="", encoding="utf-8") as stream:
        summary = list(csv.DictReader(stream))
    if len(summary) != 1 or any(
        Decimal(summary[0][key]) != value
        for key, value in (
            ("direct_kg_co2e", direct),
            ("energy_indirect_kg_co2e", indirect),
            ("total_kg_co2e", total),
            ("total_t_co2e", total / 1000),
        )
    ):
        raise ValueError("annual summary disagrees with gas-level calculation")
    return {
        "year": year,
        "activity_rows": len(rows),
        "checked_monthly_documents": len(docs),
        "total_kg_co2e": str(total),
        "status": "selected-training-checks-pass-not-assurance",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--out", type=Path)
    group.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = check_collection(args.check) if args.check else build(args.out)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
