"""Collision-checked canonical graph and local, allowlisted SPARQL queries."""

import json
from collections.abc import Iterable
from importlib.resources import files

from pydantic import TypeAdapter
from rdflib import RDF, Graph, URIRef

from .models import EvidencePackage, Ref
from .serialization import GHG, to_graph

QUERIES = {
    "explain_result": "EmissionResult",
    "results_using_factor": "EmissionFactor",
    "records_supported_by_evidence": "EvidenceArtifact",
    "unreviewed_results": None,
    "revisions": "EmissionResult",
}


def build_graph(packages: Iterable[EvidencePackage]) -> Graph:
    records = {}
    for package in packages:
        package = EvidencePackage.model_validate(package.model_dump())
        for record in package.records:
            if record.id in records and records[record.id] != record:
                raise ValueError("conflicting revision identity")
            records[record.id] = record
    return to_graph(EvidencePackage(records=tuple(records.values())))


def query_graph(graph: Graph, name: str, target: str | None = None) -> list[dict[str, str]]:
    if name not in QUERIES:
        raise ValueError("unknown query template")
    kind = QUERIES[name]
    bindings = {}
    if kind:
        try:
            target = TypeAdapter(Ref).validate_python(target)
        except ValueError:
            raise ValueError("invalid revision URN") from None
        node = URIRef(target)
        if (node, RDF.type, GHG[kind]) not in graph:
            raise ValueError("target missing or wrong kind")
        bindings["target"] = node
    elif target is not None:
        raise ValueError("query takes no target")
    query = files("ghg_assurance_graph").joinpath("queries", name + ".rq").read_text()
    rows = [
        {str(key): str(value) for key, value in row.asdict().items()}
        for row in graph.query(query, initBindings=bindings)
    ]
    return sorted(rows, key=lambda row: json.dumps(row, sort_keys=True))


def deterministic_turtle(graph: Graph) -> str:
    """Sorted N-Triples subset of Turtle, no generated prefix ordering."""
    return "".join(sorted(f"{s.n3()} {p.n3()} {o.n3()} .\n" for s, p, o in graph))
