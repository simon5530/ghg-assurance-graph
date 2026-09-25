# Domain Model

Status: Phase 0 planning; domain features are not implemented.

## Candidate entities (not an implemented schema)
Organization, facility, organizational boundary, reporting period, inventory version,
activity record, emission factor/version, calculation run, result, evidence artifact,
methodology decision, review action, and change explanation.

Specify units, gases, GWP basis, scopes/categories, geography, time validity,
source licensing, uncertainty, and transformation lineage before implementation.
Keep source observation separate from normalized value and derived result.
Identifiers must distinguish enduring record identity, immutable version identity,
and content digest. Corrections must not overwrite prior provenance.

Open questions: consolidation approach, scope/category boundaries, recalculation
policy, allocation, biogenic reporting, missing-data semantics, and reviewer roles.
No standard-conformance claim is made.
