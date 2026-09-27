"""Bounded ACME CarbonDiff: exact attribution, explicit identity and evidence."""

from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal, localcontext
from enum import StrEnum
from types import MappingProxyType

from .benchmark import preflight


class Cause(StrEnum):
    ACTIVITY_CHANGE = "ACTIVITY_CHANGE"
    SUPPLIER_MIX_CHANGE = "SUPPLIER_MIX_CHANGE"
    EMISSION_FACTOR_CHANGE = "EMISSION_FACTOR_CHANGE"
    GWP_CHANGE = "GWP_CHANGE"
    METHOD_CHANGE = "METHOD_CHANGE"
    DATA_SOURCE_CHANGE = "DATA_SOURCE_CHANGE"
    DATA_QUALITY_CHANGE = "DATA_QUALITY_CHANGE"
    BOUNDARY_CHANGE = "BOUNDARY_CHANGE"
    ORGANIZATIONAL_CHANGE = "ORGANIZATIONAL_CHANGE"
    ALLOCATION_CHANGE = "ALLOCATION_CHANGE"
    CORRECTION = "CORRECTION"
    MISSING_DATA_RESOLVED = "MISSING_DATA_RESOLVED"
    UNKNOWN = "UNKNOWN"


# Versioned evidence URI/year are bookkeeping, not inferred data-source changes.
CONTEXT = frozenset({"scope", "category", "facility", "geography", "scope2_basis", "stream"})
IGNORED = frozenset({"id", "evidence", "year", "factor_year", "reported_kg_co2e"})
NUMBERS = ("activity", "factor", "allocation_share", "reported_kg_co2e")
MECHANICAL = frozenset({"activity", "factor", "allocation_share"})
ZERO = Decimal(0)


def _number(value):
    if not isinstance(value, (str, Decimal, int)) or isinstance(value, bool):
        raise ValueError(  # noqa: TRY004 - public validation errors use ValueError
            "decimal inputs must be strings, integers or Decimal, not floats"
        )
    number = Decimal(value)
    if not number.is_finite() or number < 0:
        raise ValueError("finite nonnegative input required")
    if len(number.as_tuple().digits) > 60 or abs(number.as_tuple().exponent) > 60:
        raise ValueError("decimal exceeds bounded precision contract")
    return number


@dataclass(frozen=True)
class Snapshot:
    namespace: str
    version: str
    rows: tuple[Mapping, ...]

    def __post_init__(self):
        if not isinstance(self.namespace, str) or not self.namespace.strip():
            raise ValueError("explicit namespace required")
        if not isinstance(self.version, str) or not self.version.strip():
            raise ValueError("explicit version required")
        if not self.rows or len(self.rows) > 10000:
            raise ValueError("snapshot requires 1..10000 rows")
        copied = []
        for supplied in self.rows:
            row = dict(supplied)
            if any(not isinstance(v, (str, int, bool, Decimal, type(None))) for v in row.values()):
                raise ValueError("only scalar row fields supported")
            identity = row.get("id")
            if not isinstance(identity, str) or not identity or "/" in identity:
                raise ValueError("invalid stable identity")
            if row.get("evidence") != f"{self.namespace}/{self.version}/{identity}":
                raise ValueError("wrong snapshot evidence binding")
            for name in NUMBERS:
                row[name] = str(_number(row[name]))
            copied.append(row)
        with localcontext() as ctx:
            ctx.prec = 1000
            preflight(copied)
        object.__setattr__(self, "rows", tuple(MappingProxyType(r) for r in copied))


@dataclass(frozen=True)
class Declaration:
    """Evidence-supported row-level interpretation; never accepts numeric answers.

    fields must cover every substantive observed change for this entity. This
    intentionally disallows overlapping partial semantic allocations.
    """

    before: str
    after: str
    entity: str
    cause: Cause
    fields: frozenset[str]
    evidence: str

    def __post_init__(self):
        object.__setattr__(self, "cause", Cause(self.cause))
        object.__setattr__(self, "fields", frozenset(self.fields))
        if not isinstance(self.evidence, str) or not self.evidence.strip():
            raise ValueError("declaration needs explanatory evidence")
        if not self.fields:
            raise ValueError("declaration needs observed fields")


@dataclass(frozen=True)
class Component:
    entity: str
    cause: Cause
    kg_co2e: Decimal
    evidence: str | None = None


@dataclass(frozen=True)
class Match:
    entity: str
    status: str
    changed_fields: tuple[str, ...]


@dataclass(frozen=True)
class DiffResult:
    before: str
    after: str
    total_before: Decimal
    total_after: Decimal
    delta: Decimal
    components: tuple[Component, ...]
    matches: tuple[Match, ...]
    attributed_kg_co2e: Decimal
    residual_kg_co2e: Decimal
    absolute_unknown_kg_co2e: Decimal
    convention: str = "activity-first; factor-second; allocation-last; semantic row override"


def compare(before: Snapshot, after: Snapshot, declarations=()) -> DiffResult:
    """Compare explicit stable IDs; fail closed, with UNKNOWN for unsupported causes.

    Caller declarations are assertions, not independently authenticated evidence.
    No labels, ground truth, filesystem, graph heuristics or LLM are consulted.
    """
    if before.namespace != after.namespace:
        raise ValueError("namespace mismatch")
    if before.version == after.version:
        raise ValueError("distinct snapshot versions required")
    old = {r["id"]: r for r in before.rows}
    new = {r["id"]: r for r in after.rows}
    declared = {}
    for item in declarations:
        if (item.before, item.after) != (before.version, after.version):
            raise ValueError("declaration wrong version pair")
        if item.entity in declared:
            raise ValueError("overlapping declarations")
        if item.entity not in old.keys() | new.keys():
            raise ValueError("declaration unknown entity")
        declared[item.entity] = item
    with localcontext() as ctx:
        # Four operands, each <=60 digits and exponent +/-60, <=10000 rows.
        # 1000 significant digits cover all products, alignments and sums exactly.
        ctx.prec = 1000
        components, matches = [], []
        for identity in sorted(old.keys() | new.keys()):
            a, b = old.get(identity), new.get(identity)
            av = Decimal(a["reported_kg_co2e"]) if a is not None else ZERO
            bv = Decimal(b["reported_kg_co2e"]) if b is not None else ZERO
            delta = bv - av
            if a is None or b is None:
                status = "added" if a is None else "removed"
                fields = frozenset({"presence"})
            else:
                if any(a.get(k) != b.get(k) for k in CONTEXT):
                    raise ValueError("stable identity classification mismatch")
                status = "matched"
                fields = frozenset(
                    k for k in a.keys() | b.keys() if k not in IGNORED and a.get(k) != b.get(k)
                )
            matches.append(Match(identity, status, tuple(sorted(fields))))
            claim = declared.get(identity)
            if claim is not None:
                if claim.fields != fields:
                    raise ValueError("declaration fields do not match observed changes")
                components.append(Component(identity, claim.cause, delta, claim.evidence))
            elif status != "matched" or fields - MECHANICAL:
                components.append(Component(identity, Cause.UNKNOWN, delta))
            elif fields:
                q0, f0, s0 = (Decimal(a[k]) for k in NUMBERS[:3])
                q1, f1, s1 = (Decimal(b[k]) for k in NUMBERS[:3])
                scale = Decimal(1000) if a["unit"] == "tonne" and a["factor_unit"] == "kg" else 1
                for cause, value in (
                    (Cause.ACTIVITY_CHANGE, (q1 - q0) * scale * f0 * s0),
                    (Cause.EMISSION_FACTOR_CHANGE, q1 * scale * (f1 - f0) * s0),
                    (Cause.ALLOCATION_CHANGE, q1 * scale * f1 * (s1 - s0)),
                ):
                    if value:
                        components.append(Component(identity, cause, value))
        total_before = sum((Decimal(r["reported_kg_co2e"]) for r in before.rows), ZERO)
        total_after = sum((Decimal(r["reported_kg_co2e"]) for r in after.rows), ZERO)
        attributed = sum((c.kg_co2e for c in components if c.cause != Cause.UNKNOWN), ZERO)
        residual = sum((c.kg_co2e for c in components if c.cause == Cause.UNKNOWN), ZERO)
        exposure = sum((abs(c.kg_co2e) for c in components if c.cause == Cause.UNKNOWN), ZERO)
        if attributed + residual != total_after - total_before:
            raise ValueError("internal reconciliation failure")
        return DiffResult(
            before.version,
            after.version,
            total_before,
            total_after,
            total_after - total_before,
            tuple(components),
            tuple(matches),
            attributed,
            residual,
            exposure,
        )
