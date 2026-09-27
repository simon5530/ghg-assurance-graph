# Generic external-result adapter (Phase 8)

Implemented bounded JSON/CSV interchange, not an external calculation engine. Existing Pydantic records, package integrity checks and graph serialization are reused; no new dependency or vendor integration. This explicit generic interchange profile is **not** an openLCA, Brightway or PACT parser.

## Contract and workflow

Caller obtains licensed local export → explicitly maps metadata into this profile → imports text → closed schema/package checks → canonical package → existing provenance graph. No files, URLs, evidence citations or remote contexts are opened. Failure raises an exception before returning a package; there is no storage, logging service, approval or publication.

- `ExternalResult.model_json_schema()` exposes JSON Schema.
- `import_external_json(text) -> EvidencePackage` accepts one JSON object.
- `import_external_csv(text) -> EvidencePackage` accepts exactly one data row.
- `ExternalResult.to_package()` maps declared provenance, calculation and result into records for `build_graph([package])`.

The closed envelope contains schema_version (`external-result/1`), origin (`externally-calculated`), provenance (canonical record array), calculation (CalculationRun), and result (EmissionResult). Unknown fields fail at every level. The referenced method **must** declare method_type `external-result`, which survives graph conversion. Run software and performed_at describe the asserted external calculation, not import time. The checked origin envelope is not an additional RDF property.

Exact CSV header order:

    schema_version,origin,provenance,calculation,result

The last three cells contain JSON (array/object/object), quoted with ordinary CSV escaping. Use csv.DictWriter plus json.dumps, as in the tests. This avoids lossy flat mappings that invent missing factor context. JSON and CSV produce identical packages. Repeated JSON member names fail. Unknown or repeated headers, incomplete rows and additional data rows also fail. Text is limited to 2,000,000 UTF-8 bytes, provenance to 1,000 records; the normal Python CSV field limit also applies. These are input limits, not a hostile-process sandbox.

## Required provenance and limits

Supply the complete reference closure: organization/facility/source, inventory/period/boundary, activity/evidence/quality, factor with source/geography/period/GWP/method/boundary, method allocation/evidence, GWP evidence, and result review/reviewer. Optional digest remains absent if absent. No source, factor, boundary, timestamp or review is guessed or downloaded. Canonical version/status defaults remain as documented in the domain model.

One result/run and the current one-activity/one-factor model only. Provenance cannot hide additional runs/results. Multi-input LCA results without that declared structure are unsupported, not assigned dummy factors. Only canonical units/consolidation values are accepted; physical kg is not kg_CO2e. Mismatched run/inventory/factor boundaries and dimensions fail. Textual boundary equivalence, source truth and applicability are not independently proved. Explicit unknown consolidation is permitted by the canonical model, not treated as established comparability.

External numeric results are preserved even when different from activity × factor. Import does not recalculate, reconcile or certify; arithmetic verification is a separate selected validation operation. Review status is a supplied claim, not adapter approval.

## Reproduce

`examples/external_result.json` is wholly synthetic: 100 kWh, factor 0.5 kg_CO2e/kWh, result 50 kg_CO2e, unreviewed. No external engine was executed. Use different IDs if importing alongside the original hand-authored example: changed content under the same revision correctly triggers graph collision rejection.

```python
from pathlib import Path
from ghg_assurance_graph.adapters import import_external_json
from ghg_assurance_graph.graph import build_graph, query_graph
package = import_external_json(Path("examples/external_result.json").read_text())
rows = query_graph(build_graph([package]), "explain_result",
                   "urn:ghgag:electricity-location-result:v1")
```

Run `.venv/bin/python -m pytest -q tests/test_adapters.py`. Tests cover JSON/CSV agreement, lineage, unchanged external values, missing provenance, unsupported units/boundaries, unknown fields, duplicate keys and schema closure.
