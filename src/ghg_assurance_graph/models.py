"""Closed, immutable experimental domain records with package-level integrity."""

import json
from datetime import date
from hashlib import sha256
from typing import Annotated, Literal

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

from .units import Unit, convert

Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
LogicalID = Annotated[str, StringConstraints(pattern=r"^urn:ghgag:[a-z][a-z0-9-]*$")]
Ref = Annotated[str, StringConstraints(pattern=r"^urn:ghgag:[a-z][a-z0-9-]*:v[1-9][0-9]*$")]
Amount = Annotated[float, Field(ge=0, allow_inf_nan=False, strict=True)]
Version = Annotated[int, Field(ge=1, strict=True)]


class Frozen(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, validate_default=True)

    def model_copy(self, *, update=None, deep=False):
        # Pydantic's default update bypasses validation, unsuitable for this public API.
        data = self.model_dump(mode="python")
        data.update(update or {})
        return type(self).model_validate(data)


class Quantity(Frozen):
    value: Amount
    unit: Unit


class Record(Frozen):
    logical_id: LogicalID
    version: Version = 1
    id: Ref
    label: Text
    supersedes: Ref | None = None

    @model_validator(mode="after")
    def identity(self):
        if self.id != f"{self.logical_id}:v{self.version}":
            raise ValueError("revision ID must match logical ID and version")
        expected = f"{self.logical_id}:v{self.version - 1}" if self.version > 1 else None
        if self.supersedes != expected:
            raise ValueError("revision requires immediate predecessor; v1 has none")
        return self

    def content_digest(self) -> str:
        """SHA256 of sorted compact JSON; integrity hint, not signature or identity."""
        raw = json.dumps(self.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))
        return sha256(raw.encode()).hexdigest()


class Organization(Record):
    kind: Literal["Organization"] = "Organization"


class Facility(Record):
    kind: Literal["Facility"] = "Facility"
    organization: Ref
    geography: Text


class ReportingPeriod(Record):
    kind: Literal["ReportingPeriod"] = "ReportingPeriod"
    start: date
    end: date

    @model_validator(mode="after")
    def ordered(self):
        if self.start > self.end:
            raise ValueError("period start after end")
        return self


class BoundaryDefinition(Record):
    kind: Literal["BoundaryDefinition"] = "BoundaryDefinition"
    organization: Ref
    consolidation: Literal["operational-control", "financial-control", "equity-share", "unknown"]
    description: Text


class InventoryVersion(Record):
    kind: Literal["InventoryVersion"] = "InventoryVersion"
    organization: Ref
    period: Ref
    boundary: Ref
    status: Literal["draft", "reviewed"] = "draft"


class EmissionSource(Record):
    kind: Literal["EmissionSource"] = "EmissionSource"
    facility: Ref
    scope: Literal[1, 2, 3]
    category: Annotated[int, Field(ge=1, le=15, strict=True)] | None = None
    scope2_basis: Literal["location-based", "market-based"] | None = None

    @field_validator("scope", mode="before")
    @classmethod
    def integer_scope(cls, value):
        if type(value) is not int:
            raise ValueError("scope must be integer")
        return value

    @model_validator(mode="after")
    def classification(self):
        if (self.scope == 3) != (self.category is not None):
            raise ValueError("category required only for scope 3")
        if (self.scope == 2) != (self.scope2_basis is not None):
            raise ValueError("scope2 basis required only for scope 2")
        return self


class EvidenceArtifact(Record):
    kind: Literal["EvidenceArtifact"] = "EvidenceArtifact"
    citation: Text
    license: Text
    sha256: Annotated[str, StringConstraints(pattern=r"^[a-f0-9]{64}$")] | None = None
    synthetic: bool


class ActivityRecord(Record):
    kind: Literal["ActivityRecord"] = "ActivityRecord"
    source: Ref
    inventory: Ref
    quantity: Quantity
    evidence: Ref
    quality: Ref
    data_origin: Literal["primary", "secondary", "estimated", "supplier-specific", "unknown"]


class GWPSet(Record):
    kind: Literal["GWPSet"] = "GWPSet"
    basis: Text
    horizon_years: Annotated[int, Field(gt=0, strict=True)]
    evidence: Ref


class EmissionFactor(Record):
    kind: Literal["EmissionFactor"] = "EmissionFactor"
    value: Amount
    numerator: Literal[Unit.KG_CO2E, Unit.T_CO2E]
    denominator: Unit
    evidence: Ref
    period: Ref
    geography: Text
    gwp: Ref
    boundary: Ref
    method: Ref


class CalculationMethod(Record):
    kind: Literal["CalculationMethod"] = "CalculationMethod"
    method_type: Literal["activity-based", "spend-based", "supplier-pcf", "external-result"]
    description: Text
    allocation: Text
    evidence: Ref


class CalculationRun(Record):
    kind: Literal["CalculationRun"] = "CalculationRun"
    activity: Ref
    factor: Ref
    method: Ref
    gwp: Ref
    boundary: Ref
    inventory: Ref
    performed_at: AwareDatetime
    software: Text


class EmissionResult(Record):
    kind: Literal["EmissionResult"] = "EmissionResult"
    calculation: Ref
    inventory: Ref
    quantity: Quantity
    review: Ref

    @model_validator(mode="after")
    def equivalent(self):
        if self.quantity.unit not in (Unit.KG_CO2E, Unit.T_CO2E):
            raise ValueError("result must use explicit CO2e units")
        return self


class DataQualityAssessment(Record):
    kind: Literal["DataQualityAssessment"] = "DataQualityAssessment"
    rating: Literal["high", "medium", "low", "unknown"]
    rationale: Text
    uncertainty: Text


class ReviewDecision(Record):
    kind: Literal["ReviewDecision"] = "ReviewDecision"
    target: Ref
    reviewer: Ref
    status: Literal["unreviewed", "accepted", "rejected", "needs-review"]
    timestamp: AwareDatetime
    rationale: Text


class ChangeEvent(Record):
    kind: Literal["ChangeEvent"] = "ChangeEvent"
    before: Ref
    after: Ref
    cause: Literal[
        "ACTIVITY_CHANGE",
        "SUPPLIER_MIX_CHANGE",
        "EMISSION_FACTOR_CHANGE",
        "GWP_CHANGE",
        "METHOD_CHANGE",
        "DATA_SOURCE_CHANGE",
        "DATA_QUALITY_CHANGE",
        "BOUNDARY_CHANGE",
        "ORGANIZATIONAL_CHANGE",
        "ALLOCATION_CHANGE",
        "CORRECTION",
        "MISSING_DATA_RESOLVED",
        "UNKNOWN",
    ]
    rationale: Text


class ValidationFinding(Record):
    kind: Literal["ValidationFinding"] = "ValidationFinding"
    target: Ref
    severity: Literal["info", "warning", "error"]
    rule: Text
    message: Text


Entity = Annotated[
    Organization
    | Facility
    | ReportingPeriod
    | InventoryVersion
    | EmissionSource
    | ActivityRecord
    | EvidenceArtifact
    | EmissionFactor
    | GWPSet
    | CalculationMethod
    | CalculationRun
    | EmissionResult
    | BoundaryDefinition
    | DataQualityAssessment
    | ReviewDecision
    | ChangeEvent
    | ValidationFinding,
    Field(discriminator="kind"),
]

# Inspectable relation contract also consumed by the RDF serializer.
REFERENCES = {
    "organization": (Organization,),
    "facility": (Facility,),
    "period": (ReportingPeriod,),
    "boundary": (BoundaryDefinition,),
    "source": (EmissionSource,),
    "inventory": (InventoryVersion,),
    "evidence": (EvidenceArtifact,),
    "quality": (DataQualityAssessment,),
    "gwp": (GWPSet,),
    "method": (CalculationMethod,),
    "activity": (ActivityRecord,),
    "factor": (EmissionFactor,),
    "calculation": (CalculationRun,),
    "review": (ReviewDecision,),
    "reviewer": (Organization,),
    "target": (Record,),
    "before": (Record,),
    "after": (Record,),
    "supersedes": (Record,),
}


class EvidencePackage(Frozen):
    schema_version: Literal["0.1.0"] = "0.1.0"
    records: tuple[Entity, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def integrity(self):
        nodes = {r.id: r for r in self.records}
        if len(nodes) != len(self.records):
            raise ValueError("duplicate revision ID")
        logical_types = {}
        for r in self.records:
            if logical_types.setdefault(r.logical_id, type(r)) is not type(r):
                raise ValueError("logical identity cannot change entity type")
            for field, types in REFERENCES.items():
                ref = getattr(r, field, None)
                if ref is not None and (ref not in nodes or not isinstance(nodes[ref], types)):
                    raise ValueError(f"invalid reference {r.id}.{field}")
        # Validate every edge before dereferencing multi-hop context; record order is arbitrary.
        for r in self.records:
            if r.supersedes and type(nodes[r.supersedes]) is not type(r):
                raise ValueError("revision type mismatch")
            if isinstance(r, InventoryVersion) and nodes[r.boundary].organization != r.organization:
                raise ValueError("inventory boundary organization mismatch")
            if isinstance(r, ActivityRecord):
                facility = nodes[nodes[r.source].facility]
                if facility.organization != nodes[r.inventory].organization:
                    raise ValueError("activity organization mismatch")
                if r.quantity.unit in (Unit.KG_CO2E, Unit.T_CO2E):
                    raise ValueError("activity cannot be a CO2e result")
            if isinstance(r, EmissionFactor) and r.denominator in (Unit.KG_CO2E, Unit.T_CO2E):
                raise ValueError("factor denominator cannot be CO2e")
            if isinstance(r, CalculationRun):
                activity, factor, inventory = nodes[r.activity], nodes[r.factor], nodes[r.inventory]
                if activity.inventory != r.inventory or inventory.boundary != r.boundary:
                    raise ValueError("calculation inventory/boundary mismatch")
                if (factor.method, factor.gwp, factor.boundary) != (r.method, r.gwp, r.boundary):
                    raise ValueError("factor calculation context mismatch")
                period, valid = nodes[inventory.period], nodes[factor.period]
                if not (valid.start <= period.start <= period.end <= valid.end):
                    raise ValueError("factor period does not cover inventory")
                try:
                    convert(activity.quantity.value, activity.quantity.unit, factor.denominator)
                except Exception as exc:
                    raise ValueError("activity and factor units incompatible") from exc
            if isinstance(r, EmissionResult) and (
                nodes[r.calculation].inventory != r.inventory or nodes[r.review].target != r.id
            ):
                raise ValueError("result inventory/review target mismatch")
            if isinstance(r, ChangeEvent):
                before, after = nodes[r.before], nodes[r.after]
                if before.logical_id != after.logical_id or after.version <= before.version:
                    raise ValueError("change requires ordered revisions of same logical record")
        return self
