"""Offline SHACL structure checks and bounded ACME domain checks.

No benchmark generator, mutation metadata or ground truth is imported by detectors.
"""

from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from hashlib import sha256
from importlib.resources import files

from pyshacl import validate
from rdflib import RDF, Graph
from rdflib.namespace import SH

from .models import EvidencePackage
from .serialization import to_graph


@dataclass(frozen=True, order=True)
class Finding:
    target: str
    rule: str
    severity: str = "error"
    message: str = ""

    @property
    def id(self) -> str:
        raw = f"{self.target}\0{self.rule}\0{self.severity}\0{self.message}"
        return "urn:ghgag:finding-" + sha256(raw.encode()).hexdigest() + ":v1"

    def to_dict(self) -> dict:
        return {"id": self.id, **asdict(self)}


def validate_graph(graph: Graph) -> tuple[Finding, ...]:
    """Validate an in-memory RDF graph against packaged Core shapes only.

    Caller graphs are data, never shapes. Imports, JS, rules and inference disabled.
    No URLs, caller-supplied SHACL/SPARQL or ontology graphs are accepted.
    """
    if not isinstance(graph, Graph):
        raise TypeError("expected an in-memory rdflib Graph")
    shapes = Graph().parse(
        data=files("ghg_assurance_graph").joinpath("shapes/core.ttl").read_text(),
        format="turtle",
    )
    _, report, _ = validate(
        graph,
        shacl_graph=shapes,
        inference="none",
        advanced=False,
        js=False,
        do_owl_imports=False,
        inplace=False,
        abort_on_first=False,
    )
    findings = set()
    for result in report.subjects(RDF.type, SH.ValidationResult):
        focus = report.value(result, SH.focusNode)
        shape = report.value(result, SH.sourceShape)
        # Named property shapes give stable rules independent of report blank nodes.
        rule = "shacl:" + str(shape).rsplit("/", 1)[-1]
        message = str(report.value(result, SH.resultMessage) or "SHACL constraint violated")
        findings.add(Finding(str(focus), rule, message=message))
    return tuple(sorted(findings))


def validate_package(package: EvidencePackage) -> tuple[Finding, ...]:
    """Recheck canonical model integrity, then run RDF structural validation."""
    return validate_graph(to_graph(package))


def _decimal(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise TypeError("not a number")
    number = Decimal(str(value))
    if not number.is_finite() or number < 0:
        raise ValueError("not finite/nonnegative")
    if len(number.as_tuple().digits) > 60 or abs(number.as_tuple().exponent) > 60:
        raise ValueError("decimal exceeds bounded precision contract")
    return number


# Explicit benchmark policy, not real emission factors or normative standard clauses.
_UNITS = {"kWh", "MJ", "kg", "tonne", "liter", "meter ** 3", "km", "tonne * km", "USD"}
_SCALES = {
    ("tonne", "kg"): Fraction(1000),
    ("kg", "tonne"): Fraction(1, 1000),
    ("kWh", "MJ"): Fraction(18, 5),
    ("MJ", "kWh"): Fraction(5, 18),
}


def validate_rows(rows: Iterable[Mapping]) -> tuple[Finding, ...]:
    """Detect all applicable ACME raw-row errors without reading labels or filenames.

    Decimal arithmetic and explicit conversions are independent of benchmark.amount.
    Findings are set-valued by entity/rule. Duplicate identity is an error even if
    the repeated rows disagree. Invalid numeric inputs never receive a fallback.
    """
    rows = list(rows)
    findings = set()

    def add(target, rule):
        findings.add(Finding(target, rule, message=rule))

    if not rows:
        add("inventory", "empty inventory")
    counts = Counter(
        r.get("id") for r in rows if isinstance(r, Mapping) and isinstance(r.get("id"), str)
    )
    for identity, count in counts.items():
        if count > 1:
            add(identity, "duplicate activity")
    for index, row in enumerate(rows):
        if not isinstance(row, Mapping):
            add(f"row-{index}", "invalid row")
            continue
        target = row.get("id")
        if not isinstance(target, str) or not target.strip():
            target = f"row-{index}"
            add(target, "missing activity identity")
        if row.get("factor_source") != "ACME invented factor sheet v0.1; MIT":
            add(target, "factor provenance")
        if (
            type(row.get("year")) is not int
            or row.get("year") not in (2025, 2026)
            or type(row.get("factor_year")) is not int
            or row.get("factor_year") != row.get("year")
            or row.get("facility") not in ("hq", "tw-plant", "vn-plant")
            or row.get("geography")
            != {"hq": "TW", "tw-plant": "TW", "vn-plant": "VN"}.get(
                row.get("facility") if isinstance(row.get("facility"), str) else None
            )
        ):
            add(target, "factor applicability")
        if row.get("review") != "synthetic-accepted":
            add(target, "manual override not reviewed")
        if row.get("pcf_boundary") not in (
            "not-pcf",
            "cradle-to-gate-excluding-separate-transport",
        ) or (row.get("method") == "supplier-pcf" and row.get("pcf_boundary") == "not-pcf"):
            add(target, "unsupported PCF boundary")
        if row.get("scope2_basis") == "market-based":
            add(target, "market-based evidence unavailable")
        elif (row.get("scope") == 2) != (row.get("scope2_basis") == "location-based") or row.get(
            "scope2_basis"
        ) not in (None, "location-based"):
            add(target, "scope2 classification")
        if (
            type(row.get("scope")) is not int
            or row.get("scope") not in (1, 2, 3)
            or (
                row.get("scope") == 3
                and (type(row.get("category")) is not int or not 1 <= row["category"] <= 15)
            )
            or (row.get("scope") != 3 and row.get("category") is not None)
        ):
            add(target, "scope classification")
        if row.get("stream") != "fossil-and-nonbiogenic-ghg":
            add(target, "separate biogenic/removal/offset")
        if row.get("apply_gwp") is not False:
            add(target, "no double GWP")
        if row.get("factor_basis") != "precharacterized-kg-CO2e":
            add(target, "unsupported factor basis")
        if row.get("gwp_basis") not in ("synthetic-GWP-A-100y", "synthetic-GWP-B-100y"):
            add(target, "missing accounting basis")
        if row.get("method") not in ("supplier-pcf", "spend-based", "activity-based"):
            add(target, "unknown method")
        evidence = row.get("evidence")
        # Evidence identity binds to this row, not merely an arbitrary URI prefix.
        if (
            not isinstance(evidence, str)
            or not evidence.startswith("synthetic://acme/")
            or evidence.rsplit("/", 1)[-1] != target
        ):
            add(target, "activity evidence")
        try:
            unit, denominator = row.get("unit"), row.get("factor_unit")
            if unit not in _UNITS or denominator not in _UNITS:
                raise ValueError
            scale = Fraction(1) if unit == denominator else _SCALES[(unit, denominator)]
        except (KeyError, ValueError, TypeError):
            add(target, "unsupported unit conversion")
            scale = None
        try:
            activity, factor, share, reported = (
                _decimal(row.get(key))
                for key in ("activity", "factor", "allocation_share", "reported_kg_co2e")
            )
            if share > 1:
                raise ValueError
        except (TypeError, ValueError, InvalidOperation):
            add(target, "invalid amount or allocation")
            continue
        method = row.get("allocation_method")
        if method not in ("none", "mass-share", "economic-share") or (
            method == "none" and share != 1
        ):
            add(target, "allocation method")
        if scale is not None and (
            Fraction(activity) * scale * Fraction(factor) * Fraction(share) != Fraction(reported)
        ):
            add(target, "reported amount mismatch")
    return tuple(sorted(findings))


def evaluate_findings(predicted: Mapping[str, Iterable[Finding]], truth: Iterable[Mapping]) -> dict:
    """Exact (case, entity, rule, severity) set matching; labels enter evaluator only.

    Extra cases are false positives. Missing cases are false negatives. Metrics use
    zero for an undefined denominator. No true-negative count is fabricated.
    """
    expected = {(r["case_id"], r["entity"], r["rule"], r["severity"]) for r in truth}
    actual = {
        (case, f.target, f.rule, f.severity)
        for case, findings in predicted.items()
        for f in findings
    }
    tp, fp, fn = len(actual & expected), len(actual - expected), len(expected - actual)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0,
        "false_positives": sorted(actual - expected),
        "false_negatives": sorted(expected - actual),
    }
