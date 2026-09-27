# Obsidian graph export (Phase 7)

`export_obsidian(graph_or_package, destination)` in
`ghg_assurance_graph.exporters` creates a new plain-Markdown vault. Open its
folder with Obsidian and start at `index.md`. No Obsidian installation, plugin,
network access, or executable configuration is required to generate it.

Every subject, predicate, and resource-valued object has a note, including
external vocabulary IRIs; none of these IRIs is fetched. Notes have JSON-quoted
YAML frontmatter (`id`, `type`), outgoing relations, incoming relations, and
local wikilinks. The index links every note. This deliberately includes vocabulary
notes to avoid dangling links. The export represents the graph, not hand-authored
interpretations or an assurance opinion.

## Safety and determinism

- Filenames are `node-` plus a full SHA-256 of a resource identity, never a label
  or user-provided path. URI and blank-node namespaces are disambiguated.
- RDFLib canonicalizes blank nodes before exports. Identical graphs therefore
  produce identical note names and content independent of insertion order.
- Literal brackets and HTML are escaped, preventing accidental wikilinks and
  HTML from evidence text. Literal language/datatype annotations remain visible.
- Existing destinations and symlink destinations/ancestors are rejected.
- All notes and links are generated together; this is not a merge/update tool.
  Keep personal annotations in a separate vault or regenerate to a fresh folder.
- Blank-node filenames can change when graph structure changes; named revision
  resource filenames remain stable. Hash filenames favor safety over readability.

The destination is assumed to be a quiescent local filesystem; concurrent hostile
filesystem mutation is outside the contract. An interrupted write can leave a
partial vault; generate anew into a fresh directory.

## Other exports

`canonical_json(package)` returns sorted compact UTF-8-compatible JSON, with
records sorted by ID (project canonicalization, not RFC 8785).
`export_graph(graph_or_package, format="turtle")` supports `turtle`/`ttl` and
`json-ld`/`jsonld`; the JSON-LD is expanded and contains no remote context.

Run `python -m pytest -q tests/test_exporters.py`. Tests independently parse RDF
for graph isomorphism, compare repeated output, check safe filenames/frontmatter,
and resolve every wikilink against the actual generated note set.
