# Validation

Status: Phase 0 planning; domain features are not implemented.

## Planned evaluation, no results
Build an independently specified synthetic ACME Electronics benchmark with clean
cases and seeded defects. Keep seed, generator version, defect labels, expected
outcomes, and evaluation split explicit. Avoid testing only shapes' own assumptions.

Measure precision/recall per defect class with denominators and false positives;
report unmatched/unsupported cases, not only aggregate accuracy. Check graph
traceability, numeric reconciliation, deterministic repeated runs, and package
reproduction separately. Use baselines chosen after related-work review.

The current documentation checker checks scaffold structure and local links only.
It does not validate RDF, SHACL, scientific accuracy, citation semantics, remote
URLs, journal eligibility, or novelty. No benchmark values have been measured.
