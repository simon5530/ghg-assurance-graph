# Architecture

## Implemented workflow
Trigger: explicit local CLI/library call. Inputs are synthetic ExampleCo-GHG-001 raw rows or
canonical evidence packages; generic external-result envelopes require a caller's
explicit provenance mapping. No URL fetching or arbitrary graph/query input.

1. Pydantic and Pint check typed references, versions, contexts and dimensions.
2. RDFLib builds collision-checked RDF/PROV graphs; five bound query templates.
3. pySHACL runs packaged Core shapes; independent raw-row domain checks produce
   stable findings. The evaluator alone receives ground-truth labels.
4. CarbonDiff validates ExampleCo-GHG-001 snapshots and joins explicit namespace/stable IDs.
   Ordered Decimal decomposition reconciles; unsupported semantics remain UNKNOWN.
5. RO-Crate library builds metadata; package verification checks file sets, hashes,
   canonical payload replay and graph equivalence without external contexts.
6. Obsidian exports graph-derived notes; generic JSON/CSV import and bounded
   read-only graph tools are optional interfaces, not accounting authorities.

Storage: caller-owned local files. No server, database, credentials, scheduler or
hosted inference. Failures reject malformed inputs; no guessed factors, evidence,
zero-filled inventories or unreviewed numeric edits. Human review remains required
for source authenticity, methods, completeness and publication.

## Module boundaries
models/units/serialization → graph → validation; benchmark rows → diff;
graph/package → evidence/exporters; adapters → canonical package;
tools → allowlisted graph retrieval. evaluation consumes public labels separately.
The small benchmark calculator is fixture-only, not a general GHG engine.

See [validation](VALIDATION.md), [CarbonDiff](CARBONDIFF.md),
[evidence](EVIDENCE.md), [adapters](ADAPTERS.md), [tools](TOOLS.md) and
[acceptance matrix](ROADMAP_ACCEPTANCE.md). Gate A remains HOLD. No compliance,
causal effectiveness or full standards coverage is inferred from this architecture.

## Additive public-disclosure path (0.3.0a1)
Explicit human-mapped public numeric facts → `reported-disclosure/1` →
ReportedAssertion RDF (not EmissionResult/CalculationRun) → structural checks and
not-assessable evidence checks → per-series UNKNOWN-cause differences → bounded
RO-Crate and graph-derived inspection. No source fetch or remote JSON-LD context
resolution occurs in this path. See [contract](REPORTED_CONTRACT.md).
