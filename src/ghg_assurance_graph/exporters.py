"""Deterministic offline graph exports and a plain-Markdown graph vault."""

import json
from hashlib import sha256
from pathlib import Path

from rdflib import BNode, Graph, Literal, URIRef
from rdflib.compare import to_canonical_graph

from .models import EvidencePackage
from .serialization import to_graph


def canonical_json(value) -> str:
    """Project canonical JSON (not RFC 8785); records are ordered by revision ID."""
    if isinstance(value, EvidencePackage):
        value = EvidencePackage.model_validate(value.model_dump()).model_dump(mode="json")
        value["records"].sort(key=lambda record: record["id"])
    return (
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
        )
        + "\n"
    )


def export_graph(graph: Graph | EvidencePackage, format: str = "turtle") -> str:
    """Canonical blank-node labels; expanded JSON-LD has no remote context."""
    graph = to_canonical_graph(to_graph(graph) if isinstance(graph, EvidencePackage) else graph)
    if format in ("turtle", "ttl"):
        return "".join(sorted(f"{s.n3()} {p.n3()} {o.n3()} .\n" for s, p, o in graph))
    if format not in ("json-ld", "jsonld"):
        raise ValueError("unsupported graph format")
    nodes = {}

    def identifier(node):
        return "_:" + str(node) if isinstance(node, BNode) else str(node)

    for subject, predicate, obj in graph:
        node = nodes.setdefault(identifier(subject), {"@id": identifier(subject)})
        if isinstance(obj, (URIRef, BNode)):
            value = {"@id": identifier(obj)}
        else:
            value = {"@value": str(obj)}
            if obj.language:
                value["@language"] = obj.language
            elif obj.datatype:
                value["@type"] = str(obj.datatype)
        node.setdefault(str(predicate), []).append(value)
    for node in nodes.values():
        for key, values in node.items():
            if key != "@id":
                values.sort(key=canonical_json)
    return canonical_json([nodes[key] for key in sorted(nodes)])


def note_name(node) -> str:
    """Never derive filesystem paths or wikilink syntax from untrusted labels."""
    tag = "blank:" if isinstance(node, BNode) else "iri:"
    return "node-" + sha256((tag + str(node)).encode()).hexdigest()


def _safe_text(value) -> str:
    # HTML escape brackets as well: literals must never create unintended wikilinks.
    import html

    return html.escape(str(value)).replace("[", "&#91;").replace("]", "&#93;")


def export_obsidian(graph: Graph | EvidencePackage, destination: str | Path) -> Path:
    """Create a new vault, with a note for every resource (including external IRIs)."""
    graph = to_canonical_graph(to_graph(graph) if isinstance(graph, EvidencePackage) else graph)
    destination = Path(destination)
    if any(p.is_symlink() for p in (destination, *destination.parents)):
        raise ValueError("symlink destination")
    destination.mkdir(parents=True, exist_ok=False)
    resources = {node for triple in graph for node in triple if isinstance(node, (URIRef, BNode))}
    names = {node: note_name(node) for node in resources}
    if len(set(names.values())) != len(names):
        raise ValueError("filename collision")
    for node in sorted(resources, key=lambda n: names[n]):
        title = _safe_text(node)
        frontmatter = "---\n" + "id: " + json.dumps(str(node)) + "\n"
        frontmatter += "type: " + json.dumps("blank-node" if isinstance(node, BNode) else "iri")
        frontmatter += "\n---\n\n# " + title + "\n\n## Outgoing\n\n"
        lines = []
        for _, predicate, obj in sorted(
            graph.triples((node, None, None)), key=lambda t: tuple(n.n3() for n in t)
        ):
            target = f"[[{names[obj]}]]" if obj in names else _safe_text(obj)
            if isinstance(obj, Literal):
                target += " (" + _safe_text(obj.language or obj.datatype or "literal") + ")"
            lines.append(f"- [[{names[predicate]}]]: {target}\n")
        lines.append("\n## Incoming\n\n")
        for subject, predicate, _ in sorted(
            graph.triples((None, None, node)), key=lambda t: tuple(n.n3() for n in t)
        ):
            lines.append(f"- [[{names[subject]}]] via [[{names[predicate]}]]\n")
        (destination / (names[node] + ".md")).write_text(
            (frontmatter + "".join(lines)).rstrip() + "\n", encoding="utf-8"
        )
    index = "---\ntype: graph-index\n---\n\n# Evidence graph\n\n"
    index += "Experimental evidence navigation; not an assurance opinion.\n\n"
    index += "".join(f"- [[{name}]]\n" for name in sorted(names.values()))
    (destination / "index.md").write_text(index, encoding="utf-8")
    return destination
