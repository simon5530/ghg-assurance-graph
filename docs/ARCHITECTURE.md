# Architecture

Status: experimental Phase 1–3 implemented; later workflow remains planned.

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

Prefer established RDF, SHACL, PROV-O and RO-Crate infrastructure. Implemented
library versions are locked; research Gate A remains HOLD. One deterministic pipeline is the default;
agents are an optional later interface, not the core architecture.

## Implemented Phase 1 slice — 2026-09-26
Explicit local JSON/authored records → Pydantic package validation → Pint dimensional
checks → RDFLib export. Storage is caller-owned local files; no service, database,
authentication or agent. Inputs remain supplied claims. Validation failure raises
Pydantic errors before serialization. Source modules: models.py, units.py and
serialization.py. At that checkpoint, downstream steps remained future work.
[Contract](PHASE1_CONTRACT.md). Phase 3 extension is described below.

## Implemented Phase 3 slice — 2026-09-27
Validated local packages → collision-checked union → existing RDFLib serializer →
allowlisted bound SPARQL SELECT → sorted JSON/Turtle stdout. No network, database,
RDF import, remote context, AI or SHACL. See [graph guide](GRAPH.md).
