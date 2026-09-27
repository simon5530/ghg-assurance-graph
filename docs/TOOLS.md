# Deterministic evidence tools (Phase 9)

EvidenceTools exposes the seven planned actions using the existing graph, Core
SHACL, CarbonDiff and RO-Crate implementations. It is not an agent, AI integration,
natural-language interpreter, certification service or assurance opinion. No LLM,
provider, network fetch, arbitrary query execution or new dependency is used.

## Seven actions and their bounded meaning

| Action | Inputs | Result / limits |
| --- | --- | --- |
| explain_result | result revision URN | Existing evidence/factor/method/GWP/boundary/review explanation |
| find_missing_evidence | optional inventory revision URN | Linked activity/factor/method/GWP artifacts lacking optional SHA256; not a claim that the artifact is absent |
| find_results_using_factor | factor revision URN | Results referencing that exact factor revision |
| compare_inventory_versions | before/after inventory revision URNs | Exact CarbonDiff components, full totals and residuals from explicitly bound snapshots |
| get_validation_findings | optional exact finding-target revision URN | Computed packaged Core SHACL findings plus separately labeled asserted ValidationFinding records |
| query_graph | allowlisted template and optional target | Original five deterministic graph templates, not arbitrary SPARQL |
| create_evidence_package | trusted destination, explicit write consent and provenance | New verified offline RO-Crate directory containing the complete package snapshot |

Missing mandatory evidence links, unknown references and invalid packages fail
construction rather than becoming gap rows. Digest gaps do **not** establish
real-world inventory completeness, source availability, authenticity or accuracy.
Validation does not run raw-row domain checks or infer a standards opinion.

## Read API and compatibility

Default limit is 25; strict integer range 1–100 (booleans rejected).

```python
tools.call({"name": "explain_result", "target": result_urn})
tools.call({"name": "find_results_using_factor", "target": factor_urn})
tools.call({"name": "find_missing_evidence", "target": inventory_urn})
tools.call({"name": "get_validation_findings"})
tools.call({"name": "query_graph", "query": "explain_result", "target": result_urn})
tools.call({"name": "compare_inventory_versions", "before": old_urn, "after": new_urn})
```

The same named methods are available directly. The original QueryRequest schema
and call dictionaries remain supported unchanged: explain_result,
results_using_factor, records_supported_by_evidence, unreviewed_results, revisions.
ToolRequest describes additional read actions; irrelevant action arguments fail
closed, as do unknown fields and malformed/wrong-kind targets. query_graph wraps
the original allowlist and preserves the original query name in its response.
No query text, SERVICE clause, remote URL or file path is accepted as a query.
Citation strings are inert data, never instructions or documents to fetch.

Read answers contain deterministic rows, total_rows, truncated, copied evidence
records, and an explicit non-assurance authority label. Evidence attaches only
when identified in selected rows, explicitly queried as an evidence target, or
bound to comparison source rows. Factor search does not invent transitive evidence;
call explain_result for returned results. Findings distinguish computed-shacl from
asserted-record. A target filter selects the exact target, not all descendants.

## Explicit CarbonDiff snapshot binding

Construct with EvidenceTools(packages, snapshots={inventory_urn: snapshot, ...}),
where each value is a diff.Snapshot. The inventory must exist with the right kind.
The constructor revalidates and copies snapshots, including source rows, and
requires every row to have supplied artifact support: a literal matching evidence
URI citation or a JSON citation exactly equal to the normalized snapshot row.
The benchmark's embedded JSON citations work without network access. The binding
between a snapshot and inventory is an explicit **caller assertion**, not inferred
from labels, and does not prove graph result amounts agree with source rows.

Comparisons fail without bound snapshots; CarbonDiff requires a common namespace,
distinct versions, stable identity and valid arithmetic. This facade supplies no
semantic declarations: unsupported causes remain UNKNOWN. Numeric outputs are
exact decimal strings; full totals are not recomputed from truncated components.
Selected components carry before/after citations and matching artifact records.
No ground-truth files are read by implementation code.

## Export permission boundary

Export is intentionally **not reachable through call(request)**, including when a
request supplies allow_write. Trusted application code must authorize its chosen
destination and call the separate method:

```python
tools.create_evidence_package(
    destination,
    allow_write=True,
    created_at="2026-09-28T00:00:00+08:00",
    command=["my-application", "export"],
    data_version="review-input-v1",
)
```

Omitting consent raises PermissionError before filesystem mutation. Export uses
the complete deduplicated, collision-checked, sorted package snapshot, not a
possibly incomplete query slice. It delegates provenance validation, existing-path
refusal, symlink-path rejection, closed-file-set creation and verification to
create_package. Returned manifest_sha256 can be retained independently. Integrity
is not authenticity. command is recorded provenance, **never executed**. CarbonDiff
snapshots are comparison inputs, not additional exported files.

allow_write is explicit host consent, not authentication or a filesystem sandbox.
The host must enforce destination authorization and prevent concurrent path races.
A filesystem error after directory creation may leave a partial directory; no
atomic transaction or automatic destructive cleanup is promised.

## Bounds and verification

- Maximum 2,000 records, counting package repeats and supplied snapshot rows.
- Maximum 2,000,000 serialized UTF-8 bytes across packages and normalized snapshot rows.
- Maximum 200,000 serialized bytes per read response; excess fails, without silently dropping evidence.
- Graph queries and validation execute over bounded snapshots before row slicing.
  Serialization occurs before byte checks; no hard memory sandbox or timeout is claimed.
- Constructor snapshot isolation and returned copies prevent ordinary caller mutation.
  Private attribute tampering/model-validation bypass is outside this in-process contract.
- Only explicitly authorized package export writes files. No scheduling or publication occurs.

Run .venv/bin/python -m pytest -q tests/test_tools.py and
.venv/bin/ruff check src/ghg_assurance_graph/tools.py tests/test_tools.py.

The deterministic question set checks: support for the 500 kg_CO2e electricity
result; exact factor usage; four digest-gap relations; allowlisted graph retrieval;
asserted-versus-computed finding provenance; 3820 to 3850 kg_CO2e comparison
(+30, reconciled to attribution plus residual); and authorized, independently
verified export. Network connections are blocked for these action tests. Additional
tests cover compatibility, injection/unknown requests, strict limits, truncation,
resource budgets, snapshot binding, response mutation, denied export, existing
destinations and symlinks. This is executable retrieval/arithmetic/permission
verification, not an evaluation of AI reasoning or real assurance performance.
