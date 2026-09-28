# Phase 2 acceptance contract — 2026-09-26

Current status note (2026-09-28): this is a historical phase contract. Its dated authorization/HOLD restrictions are superseded by [current Gate A](GATE_A.md) and [original-phase acceptance](ROADMAP_ACCEPTANCE.md); technical invariants remain unless explicitly superseded.
Defined before implementation. Owner authorizes only bounded synthetic benchmark
implementation/publication. Gate A remains HOLD; Gate B needs independent domain
review. No general graph builder, SHACL detector, CarbonDiff algorithm or AI.

1. Fixed seed 20250926 generates ACME HQ/Taiwan semiconductor/Vietnam assembly
   fixtures for 2025-v1, 2025-v2 and 2026-v1; all clean packages validate and JSON
   roundtrip. Identical command yields byte-identical files and SHA256 manifest.
2. Original twelve representative source types and all fifteen specified changes/
   defects are documented. Independent hand-authored expected amounts and causes
   are never imported by generator/calculation code. Cross-period sums reconcile.
3. Clean means internally valid partial synthetic inventory, not complete or assured.
   All 15 Scope 3 categories have applicability and explicit coverage limitations.
4. Scope 2 bases never sum; contractual evidence absence blocks market-based output.
   Factor units, geography, temporal applicability, provenance and CO2e/GWP basis
   are explicit. No guessed normative fields, silent zero, or silent fallback.
5. Nonconforming mutations live only under defects; catalog has rule/entity/severity
   and leakage-aware public development/holdout labels. Public holdout is not secret.
6. Independent expected values test arithmetic, changes, unit conversion, exclusions,
   gas characterization once, allocations, and non-additivity; adversarial mutations
   must fail the bounded benchmark preflight or existing schema. No detection metrics.
7. Standards alignment cites actually inspected official sources; ISO full-clause
   coverage is unverified without licensed review. No blanket compliance claim.
8. Full tests/docs/lint, isolated locked installation/build, dependency audit, tree/
   reachable-history secret scans and privacy/license review precede commit/push.
   Remote SHA/CI/files and only fulfilled Phase 2 issues are verified afterward.
