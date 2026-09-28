# Reported disclosure contract (additive; schema 0.1 unchanged)

Implementation module: ghg_assurance_graph.reported. Profile: reported-disclosure/1.
A ReportedDisclosure has profile (default), organization (nonempty string), assertions (array).
Each ReportedAssertion has:
- id: safe slug [a-z][a-z0-9-]*, unique within disclosure
- year: integer 1900..2100 (required)
- scope: integer 1,2,3 or null (null only for a total)
- category: integer 1..15 or null (only scope 3; null means scope aggregate)
- scope2_basis: location-based | market-based | unspecified | null (required non-null for scope 2; also required when total includes scope 2)
- quantity: {value: decimal STRING, unit: kgCO2e | tCO2e | ktCO2e}; no float/null/negative/nonfinite
- source: {url: public HTTPS URL, sha256: 64 lowercase hex, page: nonempty string, retrieved_at: timezone-aware ISO timestamp, title: nonempty string}
- boundary, gwp_basis, restatement: nonempty strings or null (explicit required keys; null = not disclosed, never inferred)
- rounding: decimal STRING or null, in original quantity unit (required; disclosed rounding increment, not invented tolerance)
- total_scopes: array of distinct integers 1..3 (default empty; only when scope=null; at least two)
- note: nonempty string or null (default null)

Source SHA256 identifies locally inspected source bytes, not authenticity. Every source remains a citation, never an implicit calculation input. Numeric facts are public reported assertions; no ActivityRecord, factor, CalculationRun or review is synthesized. Missing basis/boundary/GWP/restatement/rounding yields not_assessable checks, not invented defaults. Totals and components coexist but are never summed together. Scope 2 alternatives never added. Duplicate semantic row (year, scope, category, scope2_basis, total_scopes) is invalid even with different id.

APIs: load_reported(JSON str), reported_graph(model), validate_reported(model or dict), explain_reported(model,id), compare_reported(before,after), create_reported_package(model,path,created_at=...), verify_reported_package(path), ReportedEvidenceTools(model).
CLI:

Examples (all local/offline):

```sh
ghgag reported ingest facts.json
ghgag reported validate facts.json
ghgag reported graph facts.json --format turtle
ghgag reported explain facts.json assertion-id
ghgag reported diff year-before.json year-after.json
ghgag reported package facts.json --out new-crate --created-at 2026-09-28T00:00:00Z
ghgag reported verify new-crate
ghgag reported obsidian facts.json --out new-vault
```

Validation exits 1 only for invalid; not_assessable is an explicit bounded result, not a failure or assurance pass. Syntax/input failures exit 2. Individual checks distinguish assessed, not_assessable, invalid. Report-wide status remains not_assessable because source authenticity, upstream recalculation and independent assurance cannot be established from reported facts alone.

Total reconciliation requires every scope aggregate exactly once, matching declared boundary/GWP/restatement, known scope2 basis and positive disclosed rounding increments. Tolerance is half the total increment plus half each component increment after exact unit conversion. This is an explicit arithmetic policy, not materiality or a GHG standard clause. Missing categories are never zero. Category completeness and inventory completeness are not assessed. Decimal strings permit up to 30 integer and 12 fractional digits (no exponent).

Diff requires one year per snapshot, same organization and increasing years. It reports per-row arithmetic deltas independently of comparability; unknown/changed declarations yield not_assessable. All causal attribution remains UNKNOWN; no aggregate delta combines overlapping totals, categories or scope2 alternatives. ReportedEvidenceTools exposes explain, validation, missing_evidence, compare, graph, package, obsidian. No arbitrary SPARQL or remote source/context loader.

RO-Crate contains canonical facts, graphs, JSON Schema, vocabulary descriptor, inline-context metadata and closed manifest with software version and canonical creation command. Replay verification requires the recorded application version; use that tagged environment for older artifacts. The dependency environment is pinned by the repository uv.lock, not bundled as source documents. Verification reconstructs exports without parsing attacker RDF; rejects symlinks, extra files, unsafe manifests and inconsistent payloads. Optional expected_manifest_sha256 anchors the manifest to a separately trusted digest. Source document bytes are not bundled or rehashed; citation hashes must be checked independently. Package integrity is not source authenticity.

Identity lesson: graph node identity hashes organization plus canonical assertion, rather than whole disclosure, so splitting years or sorting rows preserves assertion nodes while changed facts produce new identities. Existing schema 0.1 calculated models and contracts remain untouched.
