"""JSON domain roundtrip and RDF export; never fetch external contexts."""

from hashlib import sha256

from rdflib import RDF, BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import PROV

from .models import REFERENCES, EvidencePackage

GHG = Namespace("https://simon5530.github.io/ghg-assurance-graph/ns/0.1/")
RELATIONS = {
    "calculation": PROV.wasGeneratedBy,
    "supersedes": PROV.wasRevisionOf,
    "reviewer": PROV.wasAssociatedWith,
    "evidence": PROV.wasDerivedFrom,
}


def to_json(package: EvidencePackage) -> str:
    return EvidencePackage.model_validate(package.model_dump()).model_dump_json(indent=2)


def from_json(data: str) -> EvidencePackage:
    return EvidencePackage.model_validate_json(data)


def to_graph(package: EvidencePackage) -> Graph:
    package = EvidencePackage.model_validate(package.model_dump())
    graph = Graph()
    graph.bind("ghg", GHG)
    graph.bind("prov", PROV)
    for record in package.records:
        subject = URIRef(record.id)
        prov_type = (
            PROV.Agent
            if record.kind == "Organization"
            else PROV.Activity
            if record.kind in ("CalculationRun", "ReviewDecision")
            else PROV.Entity
        )
        graph.add((subject, RDF.type, GHG[record.kind]))
        graph.add((subject, RDF.type, prov_type))
        for field, value in record.model_dump(mode="json").items():
            if value is None or field in ("id", "kind"):
                continue
            predicate = RELATIONS.get(field, GHG[field])
            if field in REFERENCES:
                obj = URIRef(value)
            elif isinstance(value, dict):
                obj = BNode(sha256(f"{record.id}/{field}".encode()).hexdigest())
                for key, nested in value.items():
                    graph.add((obj, GHG[key], Literal(nested)))
            else:
                obj = Literal(value)
            graph.add((subject, predicate, obj))
            if record.kind == "CalculationRun" and field in (
                "activity",
                "factor",
                "method",
                "gwp",
                "boundary",
            ):
                graph.add((subject, PROV.used, obj))
        if record.kind == "ReviewDecision":
            graph.add((subject, PROV.used, URIRef(record.target)))
        graph.add((subject, GHG.schemaVersion, Literal(package.schema_version)))
    return graph


def to_rdf(package: EvidencePackage, format: str = "turtle") -> str:
    if format not in ("turtle", "json-ld"):
        raise ValueError("only turtle and json-ld are supported")
    return to_graph(package).serialize(format=format)
