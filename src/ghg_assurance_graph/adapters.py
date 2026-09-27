"""Closed generic external-result interchange; no calculation or metadata inference."""

import csv
import io
import json
import math
from typing import Literal

from pydantic import Field, model_validator

from .models import (
    CalculationMethod,
    CalculationRun,
    EmissionResult,
    Entity,
    EvidencePackage,
    Frozen,
)

CSV_COLUMNS = ("schema_version", "origin", "provenance", "calculation", "result")
MAX_INPUT_BYTES = 2_000_000


class ExternalResult(Frozen):
    """One externally calculated result with a complete, caller-declared closure."""

    schema_version: Literal["external-result/1"]
    origin: Literal["externally-calculated"]
    provenance: tuple[Entity, ...] = Field(min_length=1, max_length=1000)
    calculation: CalculationRun
    result: EmissionResult

    @model_validator(mode="after")
    def complete(self):
        if any(isinstance(r, (CalculationRun, EmissionResult)) for r in self.provenance):
            raise ValueError("provenance cannot contain additional calculations or results")
        package = self.to_package()
        nodes = {r.id: r for r in package.records}
        method = nodes[self.calculation.method]
        if not isinstance(method, CalculationMethod) or method.method_type != "external-result":
            raise ValueError("method must explicitly declare external-result")
        return self

    def to_package(self) -> EvidencePackage:
        # Package integrity checks references, units, period and boundary compatibility.
        return EvidencePackage(records=(*self.provenance, self.calculation, self.result))


def _bounded(text: str) -> None:
    if (
        not isinstance(text, str)
        or len(text) > MAX_INPUT_BYTES
        or len(text.encode("utf-8")) > MAX_INPUT_BYTES
    ):
        raise ValueError("expected text within external-result input limit")


def _unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate JSON key")
        obj[key] = value
    return obj


def _json(text: str):
    def finite(value):
        number = float(value)
        if not math.isfinite(number):
            raise ValueError("nonfinite JSON number")
        return number

    try:
        value = json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_float=finite,
            parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite JSON")),
        )
        pending = [(value, 0)]
        while pending:
            item, depth = pending.pop()
            if depth > 64:
                raise ValueError("JSON nesting limit exceeded")
            if isinstance(item, dict):
                pending.extend((v, depth + 1) for v in item.values())
            elif isinstance(item, list):
                pending.extend((v, depth + 1) for v in item)
        return value
    except RecursionError as exc:
        raise ValueError("JSON nesting limit exceeded") from exc


def import_external_json(text: str) -> EvidencePackage:
    """Import JSON text, never a filename/URL; preserve supplied result without arithmetic."""
    _bounded(text)
    return ExternalResult.model_validate(_json(text)).to_package()


def import_external_csv(text: str) -> EvidencePackage:
    """Import exactly one row; three provenance-rich columns contain JSON values."""
    _bounded(text)
    reader = csv.DictReader(io.StringIO(text), strict=True)
    try:
        if reader.fieldnames is None or tuple(reader.fieldnames) != CSV_COLUMNS:
            raise ValueError("CSV header must exactly match external-result columns")
        row = next(reader, None)
        if (
            row is None
            or None in row
            or any(v is None for v in row.values())
            or next(reader, None) is not None
        ):
            raise ValueError("CSV requires exactly one complete row")
    except csv.Error as exc:
        raise ValueError("invalid external-result CSV") from exc
    for key in ("provenance", "calculation", "result"):
        row[key] = _json(row[key])
    return ExternalResult.model_validate(row).to_package()
