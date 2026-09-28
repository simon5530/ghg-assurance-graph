"""Closed offline reported-disclosure/1 profile; never a calculated inventory."""

import ipaddress
import re
from decimal import Context, Decimal, localcontext
from hashlib import sha256
from pathlib import Path
from typing import Annotated, Literal
from urllib.parse import urlsplit

from pydantic import AwareDatetime, Field, StringConstraints, field_validator, model_validator
from rdflib import RDF, XSD, Graph, Namespace, URIRef
from rdflib import Literal as RDFLiteral

from . import __version__
from .adapters import _bounded, _json
from .exporters import canonical_json, export_graph, export_obsidian
from .models import Frozen

PROFILE = "reported-disclosure/1"
REP = Namespace("https://w3id.org/ghgag/reported/1/")
Text = Annotated[str, StringConstraints(strict=True, min_length=1, max_length=4000)]
Slug = Annotated[str, StringConstraints(strict=True, pattern=r"^[a-z][a-z0-9-]{0,99}$")]
Scope = Annotated[int, Field(strict=True, ge=1, le=3)]
SCALES = {"kgCO2e": Decimal("0.001"), "tCO2e": Decimal(1), "ktCO2e": Decimal(1000)}
LIMITATION = (
    "Reported assertions only; no source authenticity, inventory completeness or assurance opinion."
)


def decimal_string(value):
    if not isinstance(value, str) or not re.fullmatch(
        r"(?:0|[1-9][0-9]{0,29})(?:\.[0-9]{1,12})?", value
    ):
        raise ValueError("bounded nonnegative decimal string required")
    return value


def decimal_text(value):
    return format(value, "f")


class ReportedQuantity(Frozen):
    value: str
    unit: Literal["kgCO2e", "tCO2e", "ktCO2e"]

    _value = field_validator("value", mode="before")(decimal_string)

    def tonnes(self):
        with localcontext(Context(prec=80, Emin=-999999, Emax=999999)) as ctx:
            ctx.prec = 80
            return Decimal(self.value) * SCALES[self.unit]


class ReportedSource(Frozen):
    url: Text
    sha256: Annotated[str, StringConstraints(strict=True, pattern=r"^[a-f0-9]{64}$")]
    page: Text
    retrieved_at: AwareDatetime
    title: Text

    @field_validator("page", "title")
    @classmethod
    def citation_text(cls, value):
        if not value.strip():
            raise ValueError("nonblank citation required")
        return value

    @field_validator("retrieved_at", mode="before")
    @classmethod
    def timestamp_type(cls, value):
        from datetime import datetime

        if not isinstance(value, (str, datetime)):
            raise ValueError("ISO timestamp required, not epoch coercion")  # noqa: TRY004
        return value

    @field_validator("url")
    @classmethod
    def safe_url(cls, value):
        if any(ord(c) <= 32 for c in value) or "\\" in value:
            raise ValueError("unsafe citation URL")
        parts = urlsplit(value)
        host = parts.hostname or ""
        if (
            parts.scheme != "https"
            or parts.username
            or parts.password
            or parts.port not in (None, 443)
            or not re.fullmatch(r"[A-Za-z0-9.-]+", host)
            or "." not in host
            or host.endswith((".local", ".localhost", ".internal", "."))
        ):
            raise ValueError("public HTTPS citation required")
        try:
            ipaddress.ip_address(host)
        except ValueError:
            if all(c.isdigit() or c == "." for c in host):
                raise ValueError("numeric citation host prohibited") from None
        else:
            raise ValueError("IP citation hosts prohibited")
        return value


class ReportedAssertion(Frozen):
    id: Slug
    year: Annotated[int, Field(strict=True, ge=1900, le=2100)]
    scope: Scope | None
    category: Annotated[int, Field(strict=True, ge=1, le=15)] | None
    scope2_basis: Literal["location-based", "market-based", "unspecified"] | None
    quantity: ReportedQuantity
    source: ReportedSource
    boundary: Text | None
    gwp_basis: Text | None
    restatement: Text | None
    rounding: str | None
    total_scopes: tuple[Scope, ...] = ()
    note: Text | None = None

    @field_validator("boundary", "gwp_basis", "restatement", "note")
    @classmethod
    def nonblank(cls, value):
        if value is not None and not value.strip():
            raise ValueError("blank is not explicit missingness")
        return value

    @field_validator("rounding", mode="before")
    @classmethod
    def rounding_value(cls, value):
        if value is not None:
            decimal_string(value)
            if Decimal(value) <= 0:
                raise ValueError("rounding increment must be positive; use null if unknown")
        return value

    @model_validator(mode="after")
    def classify(self):
        if self.category is not None and self.scope != 3:
            raise ValueError("category belongs only to scope 3")
        if self.scope is None:
            if (
                len(self.total_scopes) < 2
                or tuple(sorted(set(self.total_scopes))) != self.total_scopes
            ):
                raise ValueError(
                    "total scopes must be sorted, distinct, and contain at least two scopes"
                )
        elif self.total_scopes:
            raise ValueError("scope row cannot also be a total")
        includes2 = self.scope == 2 or 2 in self.total_scopes
        if includes2 != (self.scope2_basis is not None):
            raise ValueError("scope2 basis required exactly when scope 2 included")
        if self.rounding is not None:
            with localcontext(Context(prec=80, Emin=-999999, Emax=999999)) as ctx:
                ctx.prec = 80
                if Decimal(self.quantity.value) % Decimal(self.rounding):
                    raise ValueError("value inconsistent with disclosed rounding increment")
        return self

    def key(self, *, year=True):
        return ((self.year,) if year else ()) + (
            self.scope,
            self.category,
            self.scope2_basis,
            self.total_scopes,
        )


class ReportedDisclosure(Frozen):
    profile: Literal["reported-disclosure/1"] = PROFILE
    organization: Text
    assertions: tuple[ReportedAssertion, ...] = Field(min_length=1, max_length=2000)

    @model_validator(mode="after")
    def identity(self):
        if not self.organization.strip():
            raise ValueError("organization required")
        if len({r.id for r in self.assertions}) != len(self.assertions):
            raise ValueError("duplicate assertion id")
        if len({r.key() for r in self.assertions}) != len(self.assertions):
            raise ValueError("duplicate semantic row identity")
        return self


def load_reported(text: str) -> ReportedDisclosure:
    _bounded(text)
    return ReportedDisclosure.model_validate(_json(text))


def _checked(model):
    return ReportedDisclosure.model_validate(
        model.model_dump() if isinstance(model, ReportedDisclosure) else model
    )


def _node(model, row):
    # Content-addressed assertion identity is stable across sorting and year subsets.
    identity = {"organization": model.organization, "assertion": row.model_dump(mode="json")}
    digest = sha256(canonical_json(identity).encode()).hexdigest()
    return URIRef(f"urn:ghgag:reported:{digest}:{row.id}")


def reported_graph(model) -> Graph:
    model = _checked(model)
    graph = Graph()
    for row in model.assertions:
        node = _node(model, row)
        graph.add((node, RDF.type, REP.ReportedAssertion))
        graph.add((node, REP.organization, RDFLiteral(model.organization)))
        graph.add((node, REP.profile, RDFLiteral(PROFILE)))
        graph.add(
            (node, REP.value, RDFLiteral(row.quantity.value, datatype=XSD.decimal, normalize=False))
        )
        graph.add((node, REP.unit, RDFLiteral(row.quantity.unit)))
        graph.add(
            (
                node,
                REP.tonnesCO2e,
                RDFLiteral(decimal_text(row.quantity.tonnes()), datatype=XSD.decimal),
            )
        )
        for key in (
            "id",
            "year",
            "scope",
            "category",
            "scope2_basis",
            "boundary",
            "gwp_basis",
            "restatement",
            "rounding",
            "note",
        ):
            value = getattr(row, key)
            graph.add(
                (
                    node,
                    REP[key if value is not None else "missingField"],
                    RDFLiteral(value if value is not None else key),
                )
            )
        for scope in row.total_scopes:
            graph.add((node, REP.totalScope, RDFLiteral(scope)))
        source = URIRef(str(node) + ":source")
        graph.add((node, REP.source, source))
        graph.add((source, RDF.type, REP.SourceCitation))
        for key, value in row.source.model_dump(mode="json").items():
            # URL is deliberately a literal; no remote graph or context dereference.
            graph.add((source, REP[key], RDFLiteral(value)))
    return graph


def validate_reported(model) -> dict:
    try:
        model = _checked(model)
    except (ValueError, TypeError):
        return {
            "profile": PROFILE,
            "status": "invalid",
            "checks": [{"rule": "schema", "status": "invalid"}],
            "limitation": LIMITATION,
        }
    checks = [{"rule": "schema", "status": "assessed", "outcome": "pass"}]
    for row in model.assertions:
        for field in ("boundary", "gwp_basis", "restatement", "rounding"):
            checks.append(
                {
                    "target": row.id,
                    "rule": field,
                    "status": "not_assessable" if getattr(row, field) is None else "assessed",
                    "outcome": "missing"
                    if getattr(row, field) is None
                    else "declared_not_verified",
                }
            )
        if row.scope2_basis == "unspecified":
            checks.append({"target": row.id, "rule": "scope2_basis", "status": "not_assessable"})
        for rule in (
            "source_authenticity",
            "activity_factor_recalculation",
            "independent_assurance",
        ):
            checks.append({"target": row.id, "rule": rule, "status": "not_assessable"})
        if row.total_scopes:
            components = [
                r
                for r in model.assertions
                if r.year == row.year
                and r.scope in row.total_scopes
                and r.category is None
                and (r.scope != 2 or r.scope2_basis == row.scope2_basis)
            ]
            assessable = (
                len(components) == len(row.total_scopes)
                and row.scope2_basis != "unspecified"
                and all(r.rounding is not None for r in [row, *components])
                and row.boundary is not None
                and row.gwp_basis is not None
                and row.restatement is not None
                and all(
                    (r.boundary, r.gwp_basis, r.restatement)
                    == (row.boundary, row.gwp_basis, row.restatement)
                    for r in components
                )
            )
            check = {
                "target": row.id,
                "rule": "reported_total_reconciliation",
                "status": "not_assessable",
            }
            if assessable:
                with localcontext(Context(prec=80, Emin=-999999, Emax=999999)) as ctx:
                    ctx.prec = 80
                    delta = row.quantity.tonnes() - sum(
                        (r.quantity.tonnes() for r in components), Decimal(0)
                    )
                    tolerance = sum(
                        (
                            Decimal(r.rounding) * SCALES[r.quantity.unit] / 2
                            for r in [row, *components]
                        ),
                        Decimal(0),
                    )
                    check.update(
                        status="assessed" if abs(delta) <= tolerance else "invalid",
                        delta_tCO2e=decimal_text(delta),
                        tolerance_tCO2e=decimal_text(tolerance),
                        outcome="within_rounding" if abs(delta) <= tolerance else "mismatch",
                    )
            checks.append(check)
    status = (
        "invalid"
        if any(c["status"] == "invalid" for c in checks)
        else "not_assessable"
        if any(c["status"] == "not_assessable" for c in checks)
        else "assessed"
    )
    return {"profile": PROFILE, "status": status, "checks": checks, "limitation": LIMITATION}


def explain_reported(model, target):
    model = _checked(model)
    row = next((r for r in model.assertions if r.id == target), None)
    if row is None:
        raise ValueError("unknown reported assertion")
    return {
        "assertion": row.model_dump(mode="json"),
        "node": str(_node(model, row)),
        "tonnesCO2e": decimal_text(row.quantity.tonnes()),
        "checks": [c for c in validate_reported(model)["checks"] if c.get("target") == target],
        "causality": "UNKNOWN",
        "limitation": LIMITATION,
    }


def compare_reported(before, after):
    before, after = _checked(before), _checked(after)
    if before.organization != after.organization:
        raise ValueError("cross-organization comparison prohibited")
    years = [{r.year for r in m.assertions} for m in (before, after)]
    if any(len(y) != 1 for y in years) or next(iter(years[0])) >= next(iter(years[1])):
        raise ValueError("one explicit, chronologically increasing year per snapshot required")
    left, right = ({r.key(year=False): r for r in m.assertions} for m in (before, after))
    rows = []
    for key in sorted(left.keys() | right.keys(), key=str):
        a, b = left.get(key), right.get(key)
        comparable = (
            a is not None
            and b is not None
            and all(
                getattr(a, f) is not None and getattr(a, f) == getattr(b, f)
                for f in ("boundary", "gwp_basis", "restatement")
            )
            and a.scope2_basis != "unspecified"
        )
        with localcontext(Context(prec=80, Emin=-999999, Emax=999999)) as ctx:
            ctx.prec = 80
            delta = decimal_text(b.quantity.tonnes() - a.quantity.tonnes()) if a and b else None
        rows.append(
            {
                "before": a.id if a else None,
                "after": b.id if b else None,
                "status": "assessed" if comparable else "not_assessable",
                "arithmetic_delta_tCO2e": delta,
                "causality": "UNKNOWN",
                "reason": "declared basis equal; attribution unavailable"
                if comparable
                else "missing row or unknown/changed reporting basis",
            }
        )
    return {
        "profile": PROFILE,
        "organization": before.organization,
        "before_year": next(iter(years[0])),
        "after_year": next(iter(years[1])),
        "rows": rows,
        "causality": "UNKNOWN",
        "aggregate_delta": None,
        "limitation": "Row deltas only: alternatives, categories and totals are not additive; no causal attribution.",
    }


def _payloads(model):
    return {
        "package.json": canonical_json(model.model_dump(mode="json")).encode(),
        "graph.ttl": export_graph(reported_graph(model)).encode(),
        "graph.jsonld": export_graph(reported_graph(model), "json-ld").encode(),
        "schema.json": canonical_json(ReportedDisclosure.model_json_schema()).encode(),
        "ontology.json": canonical_json(
            {"id": str(REP), "profile": PROFILE, "limitation": LIMITATION}
        ).encode(),
    }


def create_reported_package(model, destination, *, created_at):
    from .evidence import _metadata, _validate_provenance

    model = _checked(model)
    _validate_provenance(created_at, ["ghgag", "reported", "package"])
    destination = Path(destination)
    if ".." in destination.parts or any(
        p.is_symlink() for p in (destination, *destination.parents)
    ):
        raise ValueError("unsafe destination")
    payloads = _payloads(model)
    payloads["ro-crate-metadata.json"] = _metadata(payloads, created_at)
    manifest = {
        "profile": PROFILE,
        "created_at": created_at,
        "software": {"ghg-assurance-graph": __version__},
        "command": ["ghgag", "reported", "package"],
        "files": {
            name: {"sha256": sha256(data).hexdigest(), "bytes": len(data)}
            for name, data in sorted(payloads.items())
        },
    }
    payloads["manifest.json"] = canonical_json(manifest).encode()
    destination.mkdir(parents=True, exist_ok=False)
    for name, data in payloads.items():
        (destination / name).write_bytes(data)
    return verify_reported_package(destination)


def verify_reported_package(directory, *, expected_manifest_sha256=None):
    from .evidence import _metadata, _read_payloads, _validate_provenance

    try:
        if ".." in Path(directory).parts:
            raise ValueError("unsafe path")
        raw = _read_payloads(directory)
        digest = sha256(raw["manifest.json"]).hexdigest()
        if expected_manifest_sha256 is not None and digest != expected_manifest_sha256:
            raise ValueError("manifest mismatch")
        manifest = _json(raw["manifest.json"])
        if (
            set(manifest) != {"profile", "created_at", "software", "command", "files"}
            or manifest["profile"] != PROFILE
        ):
            raise ValueError("invalid manifest")
        _validate_provenance(manifest["created_at"], manifest["command"])
        if manifest["software"] != {"ghg-assurance-graph": __version__} or manifest["command"] != [
            "ghgag",
            "reported",
            "package",
        ]:
            raise ValueError("unsupported software replay version or command")
        model = load_reported(raw["package.json"].decode())
        expected = _payloads(model)
        expected["ro-crate-metadata.json"] = _metadata(expected, manifest["created_at"])
        hashes = {
            name: {"sha256": sha256(data).hexdigest(), "bytes": len(data)}
            for name, data in sorted(expected.items())
        }
        if (
            canonical_json(manifest["files"]) != canonical_json(hashes)
            or any(raw[name] != data for name, data in expected.items())
            or raw["manifest.json"] != canonical_json(manifest).encode()
        ):
            raise ValueError("package integrity mismatch")
        return {
            "valid": True,
            "profile": PROFILE,
            "manifest_sha256": digest,
            "limitation": "Integrity only, not source authenticity or assurance.",
        }
    except (ValueError, TypeError, OSError, KeyError, UnicodeError):
        return {
            "valid": False,
            "profile": PROFILE,
            "error": "invalid local reported evidence package",
        }


class ReportedEvidenceTools:
    """Separate additive local evidence facade; no arbitrary query or network route."""

    def __init__(self, model):
        self.model = load_reported(canonical_json(_checked(model).model_dump(mode="json")))

    def explain(self, target):
        return explain_reported(self.model, target)

    def validation(self):
        return validate_reported(self.model)

    def missing_evidence(self):
        return [c for c in self.validation()["checks"] if c["status"] == "not_assessable"]

    def compare(self, after):
        return compare_reported(self.model, after)

    def graph(self):
        return reported_graph(self.model)

    def package(self, destination, *, created_at):
        return create_reported_package(self.model, destination, created_at=created_at)

    def obsidian(self, destination):
        if ".." in Path(destination).parts:
            raise ValueError("unsafe destination")
        return export_obsidian(self.graph(), destination)
