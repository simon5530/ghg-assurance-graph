"""Seven deterministic local evidence actions; no agent or natural-language routing."""

import json
from collections.abc import Iterable, Mapping
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field, TypeAdapter

from .diff import Snapshot, compare
from .evidence import create_package
from .graph import build_graph, query_graph
from .models import EvidenceArtifact, EvidencePackage, Frozen, Ref
from .validation import validate_graph

MAX_RECORDS = 2000
MAX_PACKAGE_BYTES = 2_000_000
MAX_RESPONSE_BYTES = 200_000
AUTHORITY = "asserted-local-records; not an assurance opinion"
Limit = Annotated[int, Field(strict=True, ge=1, le=100)]
QueryName = Literal[
    "explain_result",
    "results_using_factor",
    "records_supported_by_evidence",
    "unreviewed_results",
    "revisions",
]


class QueryRequest(Frozen):
    """Original five-template contract, retained unchanged."""

    name: QueryName
    target: Ref | None = None
    limit: Limit = 25


class ToolRequest(Frozen):
    """Read-only action contract. Export deliberately has no request route."""

    name: Literal[
        "find_missing_evidence",
        "find_results_using_factor",
        "compare_inventory_versions",
        "get_validation_findings",
        "query_graph",
    ]
    target: Ref | None = None
    before: Ref | None = None
    after: Ref | None = None
    query: QueryName | None = None
    limit: Limit = 25


class EvidenceTools:
    """Own validated snapshots, bounded queries and an explicit opt-in export method.

    CarbonDiff inputs must be explicitly bound to inventory URNs at construction;
    no identity matching or input reconstruction from graph labels is attempted.
    """

    def __init__(
        self,
        packages: Iterable[EvidencePackage],
        *,
        snapshots: Mapping[str, Snapshot] | None = None,
    ):
        validated = []
        count = size = 0
        for package in packages:
            count += len(package.records)
            if count > MAX_RECORDS:
                raise ValueError("record budget exceeded")
            raw = package.model_dump_json()
            size += len(raw.encode("utf-8"))
            if size > MAX_PACKAGE_BYTES:
                raise ValueError("package byte budget exceeded")
            validated.append(EvidencePackage.model_validate_json(raw))
        self._graph = build_graph(validated)
        self._records = {r.id: r for p in validated for r in p.records}
        self._package = EvidencePackage(
            records=tuple(self._records[key] for key in sorted(self._records))
        )
        self._evidence = {
            r.id: r.model_dump(mode="json")
            for r in self._records.values()
            if isinstance(r, EvidenceArtifact)
        }
        self._snapshots = {}
        for inventory, snapshot in (snapshots or {}).items():
            self._target(inventory, "InventoryVersion")
            count += len(snapshot.rows)
            if count > MAX_RECORDS:
                raise ValueError("record budget exceeded")
            copied = Snapshot(snapshot.namespace, snapshot.version, snapshot.rows)
            size += len(json.dumps([dict(r) for r in copied.rows]).encode("utf-8"))
            if size > MAX_PACKAGE_BYTES:
                raise ValueError("package byte budget exceeded")
            # Bind every source citation to a supplied artifact; never fetch its URI.
            if any(not self._snapshot_evidence(row) for row in copied.rows):
                raise ValueError("snapshot evidence absent from package")
            self._snapshots[inventory] = copied

    def _snapshot_evidence(self, row):
        """Match literal URI citations or exact embedded benchmark row assertions."""
        refs = []
        for ref, artifact in self._evidence.items():
            citation = artifact["citation"]
            if citation == row["evidence"]:
                refs.append(ref)
                continue
            try:
                embedded = json.loads(citation)
            except (ValueError, TypeError):
                continue
            if embedded == dict(row):
                refs.append(ref)
        return refs

    def _target(self, target, kind=None):
        target = TypeAdapter(Ref).validate_python(target)
        record = self._records.get(target)
        if record is None or (kind is not None and record.kind != kind):
            raise ValueError("target missing or wrong kind")
        return record

    def _answer(self, name, target, rows, limit, *, refs=(), **extra):
        selected = rows[:limit]
        ids = set(refs)
        ids.update(value for row in selected for value in row.values() if isinstance(value, str))
        answer = {
            "query": name,
            "target": target,
            "rows": selected,
            "total_rows": len(rows),
            "truncated": len(selected) < len(rows),
            "evidence": [
                deepcopy(self._evidence[ref]) for ref in sorted(ids) if ref in self._evidence
            ],
            "authority": AUTHORITY,
            **extra,
        }
        if len(json.dumps(answer).encode("utf-8")) > MAX_RESPONSE_BYTES:
            raise ValueError("response byte budget exceeded; use a smaller limit")
        return answer

    def call(self, request: dict | QueryRequest | ToolRequest) -> dict:
        if isinstance(request, (QueryRequest, ToolRequest)):
            request = request.model_dump(exclude_unset=True)
        if isinstance(request, dict) and request.get("name") in (
            "find_missing_evidence",
            "find_results_using_factor",
            "compare_inventory_versions",
            "get_validation_findings",
            "query_graph",
        ):
            action = ToolRequest.model_validate(request)
            allowed = {
                "compare_inventory_versions": {"before", "after"},
                "query_graph": {"query", "target"},
            }.get(action.name, {"target"})
            if action.model_fields_set - allowed - {"name", "limit"}:
                raise ValueError("unexpected action arguments")
            if action.name == "query_graph":
                if action.query is None:
                    raise ValueError("query template required")
                return self.query_graph(action.query, action.target, limit=action.limit)
            if action.name == "compare_inventory_versions":
                return self.compare_inventory_versions(
                    action.before, action.after, limit=action.limit
                )
            return getattr(self, action.name)(action.target, limit=action.limit)
        request = QueryRequest.model_validate(request)
        return self.query_graph(request.name, request.target, limit=request.limit)

    def query_graph(self, name: QueryName, target: str | None = None, *, limit: int = 25):
        request = QueryRequest(name=name, target=target, limit=limit)
        rows = query_graph(self._graph, request.name, request.target)
        refs = [target] if name == "records_supported_by_evidence" else []
        return self._answer(name, target, rows, request.limit, refs=refs)

    def explain_result(self, target: str, *, limit: int = 25):
        return self.query_graph("explain_result", target, limit=limit)

    def find_results_using_factor(self, target: str, *, limit: int = 25):
        request = QueryRequest(name="results_using_factor", target=target, limit=limit)
        rows = query_graph(self._graph, request.name, request.target)
        return self._answer("find_results_using_factor", target, rows, request.limit)

    def find_missing_evidence(self, target: str | None = None, *, limit: int = 25):
        limit = TypeAdapter(Limit).validate_python(limit)
        if target is not None:
            self._target(target, "InventoryVersion")
        rows = []
        for result in self._records.values():
            if result.kind != "EmissionResult" or (target and result.inventory != target):
                continue
            calculation = self._records[result.calculation]
            explanation = {
                "evidence": self._records[calculation.activity].evidence,
                "factorEvidence": self._records[calculation.factor].evidence,
                "methodEvidence": self._records[calculation.method].evidence,
                "gwpEvidence": self._records[calculation.gwp].evidence,
            }
            for field in ("evidence", "factorEvidence", "methodEvidence", "gwpEvidence"):
                evidence = self._evidence[explanation[field]]
                if evidence["sha256"] is None:
                    rows.append(
                        {
                            "result": result.id,
                            "relation": field,
                            "evidence": evidence["id"],
                            "gap": "artifact digest absent",
                        }
                    )
        rows.sort(key=lambda row: json.dumps(row, sort_keys=True))
        return self._answer(
            "find_missing_evidence",
            target,
            rows,
            limit,
            scope="linked artifact digests only; required links already model-validated; "
            "no real-world inventory completeness or source availability test",
        )

    def get_validation_findings(self, target: str | None = None, *, limit: int = 25):
        limit = TypeAdapter(Limit).validate_python(limit)
        if target is not None:
            self._target(target)
        rows = [dict(f.to_dict(), origin="computed-shacl") for f in validate_graph(self._graph)]
        rows.extend(
            {
                "id": r.id,
                "target": r.target,
                "rule": r.rule,
                "severity": r.severity,
                "message": r.message,
                "origin": "asserted-record",
            }
            for r in self._records.values()
            if r.kind == "ValidationFinding"
        )
        rows = sorted(
            (r for r in rows if target is None or r["target"] == target),
            key=lambda row: json.dumps(row, sort_keys=True),
        )
        return self._answer(
            "get_validation_findings",
            target,
            rows,
            limit,
            scope="packaged Core SHACL and asserted findings; not raw-row validation",
        )

    def compare_inventory_versions(self, before: str, after: str, *, limit: int = 25):
        limit = TypeAdapter(Limit).validate_python(limit)
        self._target(before, "InventoryVersion")
        self._target(after, "InventoryVersion")
        if before not in self._snapshots or after not in self._snapshots:
            raise ValueError("comparison requires explicitly bound CarbonDiff snapshots")
        a, b = self._snapshots[before], self._snapshots[after]
        result = compare(a, b)
        rows = [
            {**asdict(c), "cause": c.cause.value, "kg_co2e": str(c.kg_co2e)}
            for c in result.components
        ]
        sources = {(s.version, r["id"]): r["evidence"] for s in (a, b) for r in s.rows}
        by_citation = {}
        for snapshot in (a, b):
            for source in snapshot.rows:
                by_citation.setdefault(source["evidence"], []).extend(
                    self._snapshot_evidence(source)
                )
        refs = set()
        for row in rows[:limit]:
            for side, snapshot in (("before", a), ("after", b)):
                citation = sources.get((snapshot.version, row["entity"]))
                row[side + "_citation"] = citation
                refs.update(by_citation.get(citation, ()))
        totals = {
            key: str(getattr(result, key))
            for key in (
                "total_before",
                "total_after",
                "delta",
                "attributed_kg_co2e",
                "residual_kg_co2e",
                "absolute_unknown_kg_co2e",
            )
        }
        return self._answer(
            "compare_inventory_versions",
            None,
            rows,
            limit,
            refs=refs,
            before=before,
            after=after,
            totals=totals,
            convention=result.convention,
            scope="caller-bound snapshots; no inferred semantic declarations",
        )

    def create_evidence_package(
        self,
        destination: str | Path,
        *,
        allow_write: bool = False,
        created_at: str,
        command: list[str] | tuple[str, ...],
        data_version: str = "unspecified",
    ) -> dict:
        """Explicit trusted-host write, never reachable through call(request).

        Writes the complete collision-checked snapshot to a NEW directory. The
        host owns destination authorization; allow_write is consent, not a sandbox.
        """
        if allow_write is not True:
            raise PermissionError("package export requires explicit allow_write=True")
        return create_package(
            self._package,
            destination,
            created_at=created_at,
            command=command,
            data_version=data_version,
        )
