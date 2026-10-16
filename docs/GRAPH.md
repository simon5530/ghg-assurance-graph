# Phase 3 local provenance graph

Experimental owner-authorized implementation; [contract](PHASE3_CONTRACT.md).
Gate A is scoped GO; current licensed-review scope and limitations are in STANDARDS_ALIGNMENT.md.

## Reproduce

From the repository with Python 3.12 and locked uv environment:

~~~sh
uv sync --locked
uv run python scripts/run_moenv_example.py --out artifacts/moenv-worked
uv run ghgag graph build artifacts/moenv-worked/generated/2024/package.json
uv run ghgag graph explain urn:ghgag:moenv-demo-2024-electricity-result:v1 --input artifacts/moenv-worked/generated/2024/package.json
uv run ghgag graph query results_using_factor --target urn:ghgag:moenv-demo-2024-electricity-factor:v1 --input artifacts/moenv-worked/generated/2024/package.json
uv run ghgag graph query records_supported_by_evidence --target urn:ghgag:moenv-demo-2024-electricity-activity-evidence:v1 --input artifacts/moenv-worked/generated/2024/package.json
uv run ghgag graph query unreviewed_results --input artifacts/moenv-worked/generated/2024/package.json
~~~

Build accepts canonical package files or folders. It emits sorted Turtle to stdout;
explain/query rebuild from the explicit package, not from the Turtle output.
The 2024 electricity result explains to 66265.2 kg_CO2e and status unreviewed.
All nine MOENV result lineages resolve; the years retain four/five unreviewed results.
Monthly source files remain external to the canonical graph/crate; use the collection
checker as well. See [operating instructions](USAGE.zh-TW.md).

No arbitrary SPARQL file execution or hidden graph exists. Missing/wrong-kind IDs
fail nonzero. A legitimate query with no matches returns an empty JSON list.

## Semantics and boundaries

- build_graph revalidates every package, deduplicates identical revision records,
  rejects conflicting content at the same revision URI, then reuses to_graph.
- Deterministic quantity blank nodes are keyed by record URI and field, avoiding
  random labels and cross-inventory quantity merging. JSON-LD/Turtle export remains
  in the existing serializer; CLI Turtle is a stable sorted-triple presentation.
- Results prov:wasGeneratedBy calculations; calculations prov:used their inputs.
  Reviews prov:used the target and were associated with the reviewer agent.
  A retrospective review does not generate the emissions result.
- explain_result resolves role-specific lineage, not a complete source-document
  dump. records_supported_by_evidence returns directly derived records (activity,
  factor, method, GWP here), not an inferred transitive assurance relationship.
- unreviewed_results means explicit status unreviewed, not every non-accepted
  decision. needs-review and rejected are distinct states. Missing review nodes
  are malformed packages and rejected before querying.
- revisions follows explicit revision edges both ways and includes the selected
  result. Benchmark snapshots have distinct logical IDs, not revision edges: the
  result is a singleton even when all three snapshots are loaded. Tests separately
  exercise a genuine v1→v2→v3 result chain. Do not infer revisions from row labels.
- Queries are package-owned SELECT text with RDFLib initBindings, no interpolation.
  No user-supplied query, SERVICE, UPDATE, remote RDF/context or evidence citation
  dereferencing is exposed. Canonical input and output paths are explicitly chosen
  by the local operator; this is not a sandbox for hostile filesystem access.
- The library query API expects an unmodified graph produced by build_graph; arbitrary
  caller-mutated RDF graphs are not integrity-validated at query time. No SHACL or
  general RDF assurance validator is implemented in this phase.

The older benchmark separately traces 45 synthetic results; those counts are not the nine-result MOENV case. This is not evidence
that an underlying document is true, the review actually occurred, the inventory
is complete, or an organization is certified. No new dependency, remote service,
licensed standard, factor database or source PDF is included. Later phases stopped.
