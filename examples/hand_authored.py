"""Ten manually specified cases share one explicit record template, not a benchmark generator.

Run: uv run python examples/hand_authored.py
"""

import json
from pathlib import Path

from ghg_assurance_graph.models import EvidencePackage
from ghg_assurance_graph.serialization import to_json, to_rdf

CASES = json.loads(Path(__file__).with_name("cases.json").read_text())


def example(case):
    def ref(name):
        return f"urn:ghgag:{case['name']}-{name}:v1"

    def record(kind, name, **fields):
        return dict(kind=kind, id=ref(name), logical_id=ref(name)[:-3], label=name, **fields)

    records = [
        record("Organization", "org"),
        record("Organization", "reviewer"),
        record("Facility", "site", organization=ref("org"), geography="synthetic-region"),
        record("ReportingPeriod", "period", start="2025-01-01", end="2025-12-31"),
        record(
            "BoundaryDefinition",
            "boundary",
            organization=ref("org"),
            consolidation="unknown",
            description="Synthetic example boundary; not approved",
        ),
        record(
            "InventoryVersion",
            "inventory",
            organization=ref("org"),
            period=ref("period"),
            boundary=ref("boundary"),
        ),
        record(
            "EmissionSource",
            "source",
            facility=ref("site"),
            scope=case["scope"],
            category=case.get("category"),
            scope2_basis=case.get("scope2_basis"),
        ),
        record(
            "EvidenceArtifact",
            "evidence",
            citation=case["description"],
            license="MIT",
            synthetic=True,
        ),
        record(
            "DataQualityAssessment",
            "quality",
            rating="unknown",
            rationale="Hand-authored illustrative values",
            uncertainty="Not quantified",
        ),
        record(
            "ActivityRecord",
            "activity",
            source=ref("source"),
            inventory=ref("inventory"),
            quantity={"value": case["amount"], "unit": case["unit"]},
            evidence=ref("evidence"),
            quality=ref("quality"),
            data_origin=case["origin"],
        ),
        record(
            "GWPSet",
            "gwp",
            basis="Synthetic illustrative CO2e basis, not IPCC",
            horizon_years=100,
            evidence=ref("evidence"),
        ),
        record(
            "CalculationMethod",
            "method",
            method_type=case["method"],
            description="Supplied illustrative amount times factor; not executed by library",
            allocation="No allocation in this synthetic single-source case",
            evidence=ref("evidence"),
        ),
        record(
            "EmissionFactor",
            "factor",
            value=case["factor"],
            numerator="kg_CO2e",
            denominator=case["unit"],
            evidence=ref("evidence"),
            period=ref("period"),
            geography="synthetic-region",
            gwp=ref("gwp"),
            boundary=ref("boundary"),
            method=ref("method"),
        ),
        record(
            "CalculationRun",
            "run",
            activity=ref("activity"),
            factor=ref("factor"),
            method=ref("method"),
            gwp=ref("gwp"),
            boundary=ref("boundary"),
            inventory=ref("inventory"),
            performed_at="2026-09-26T00:00:00Z",
            software="hand-authored-example/1",
        ),
        record(
            "EmissionResult",
            "result",
            calculation=ref("run"),
            inventory=ref("inventory"),
            quantity={"value": case["result"], "unit": "kg_CO2e"},
            review=ref("review"),
        ),
        record(
            "ReviewDecision",
            "review",
            target=ref("result"),
            reviewer=ref("reviewer"),
            status="unreviewed",
            timestamp="2026-09-26T00:00:00Z",
            rationale="No practitioner assurance performed",
        ),
        record(
            "ValidationFinding",
            "finding",
            target=ref("result"),
            severity="info",
            rule="illustration-only",
            message="Authored finding, not an executed assurance rule",
        ),
    ]
    # One explicit correction demonstrates version identity without attribution logic.
    if case["name"] == "fleet-fuel":
        old = next(r for r in records if r["kind"] == "ActivityRecord")
        revised = dict(
            old,
            id=old["logical_id"] + ":v2",
            version=2,
            supersedes=old["id"],
            quantity={"value": 21, "unit": "liter"},
        )
        records += [
            revised,
            record(
                "ChangeEvent",
                "change",
                before=old["id"],
                after=revised["id"],
                cause="CORRECTION",
                rationale="Illustrative corrected observation",
            ),
        ]
    return EvidencePackage.model_validate({"records": records})


if __name__ == "__main__":
    out = Path("artifacts/examples")
    out.mkdir(parents=True, exist_ok=True)
    for case in CASES:
        package = example(case)
        (out / (case["name"] + ".json")).write_text(to_json(package))
        for format, suffix in (("turtle", ".ttl"), ("json-ld", ".jsonld")):
            (out / (case["name"] + suffix)).write_text(to_rdf(package, format))
    print("Exported ten authored examples in JSON, JSON-LD and Turtle")
