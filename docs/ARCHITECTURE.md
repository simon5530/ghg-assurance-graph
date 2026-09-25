# Architecture

Status: Phase 0 planning; domain features are not implemented.

## Proposed workflow (not implemented)
Trigger: explicit local import of a versioned synthetic inventory.
Inputs: activity records, factor references, evidence, boundaries, and decisions.
Sources: licensed local artifacts; external engines remain separate.
Deterministic steps: parse → validate canonical model → construct RDF/PROV-O →
run SHACL → compare inventory versions → package evidence.
Reasoning: optional narrative assistance, isolated from numerical and rule authority.
Validation: schema constraints, seeded ground truth, reconciliation, reproducibility.
Approval: human review before accepting decisions or publishing evidence.
Outputs: provenance explanations, validation reports, CarbonDiff, RO-Crate.
Storage: versioned local artifacts and portable graph files; no service yet.
Logging: planned structured run metadata without secrets or source data leakage.
Failure: reject malformed inputs; report incomplete/ambiguous evidence; never invent it.

Prefer established RDF, SHACL, PROV-O and RO-Crate infrastructure; library and
version choices await the research gate. One deterministic pipeline is the default;
agents are an optional later interface, not the core architecture.
