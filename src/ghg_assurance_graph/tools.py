"""Optional deterministic, local-only query facade; not an autonomous agent."""

import json
from collections.abc import Iterable
from copy import deepcopy
from typing import Annotated, Literal

from pydantic import Field

from .graph import build_graph, query_graph
from .models import EvidenceArtifact, EvidencePackage, Frozen, Ref

MAX_RECORDS = 2000
MAX_PACKAGE_BYTES = 2_000_000
MAX_RESPONSE_BYTES = 200_000


class QueryRequest(Frozen):
    name: Literal[
        "explain_result",
        "results_using_factor",
        "records_supported_by_evidence",
        "unreviewed_results",
        "revisions",
    ]
    target: Ref | None = None
    limit: Annotated[int, Field(strict=True, ge=1, le=100)] = 25


class EvidenceTools:
    """Snapshot validated packages, run only packaged queries and attach evidence claims."""

    def __init__(self, packages: Iterable[EvidencePackage]):
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
        self._evidence = {
            r.id: r.model_dump(mode="json")
            for p in validated
            for r in p.records
            if isinstance(r, EvidenceArtifact)
        }

    def call(self, request: dict | QueryRequest) -> dict:
        if isinstance(request, QueryRequest):
            request = request.model_dump()
        request = QueryRequest.model_validate(request)
        rows = query_graph(self._graph, request.name, request.target)
        selected = rows[: request.limit]
        refs = {value for row in selected for value in row.values()}
        if request.name == "records_supported_by_evidence":
            refs.add(request.target)
        answer = {
            "query": request.name,
            "target": request.target,
            "rows": selected,
            "total_rows": len(rows),
            "truncated": len(selected) < len(rows),
            "evidence": [
                deepcopy(self._evidence[ref]) for ref in sorted(refs) if ref in self._evidence
            ],
            "authority": "asserted-local-records; not an assurance opinion",
        }
        if len(json.dumps(answer).encode("utf-8")) > MAX_RESPONSE_BYTES:
            raise ValueError("response byte budget exceeded; use a smaller limit")
        return answer
