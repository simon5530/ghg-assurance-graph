# ADR 0001: Not another calculator

Status: accepted bounded research boundary, 2026-09-28; see [same-case comparison](../docs/RELATED_WORK.md) and [scoped GO](../docs/GATE_A.md). Not a claim of novelty or practitioner approval.

Context: accounting engines already calculate emissions; rebuilding them would not
establish an assurance-evidence contribution.

Decision: focus on evidence lineage, explicit constraints, version-change
explanations, and reproducible packaging. Reuse external calculation engines.

Alternatives: another calculator; a spreadsheet-only workflow; extend an existing
provenance tool. Source-grounded comparison identifies the organizational version/evidence integration contract as remaining work; mature generic infrastructure is reused, not replaced.

Consequences: numerical correctness still needs tests, but engine completeness is
out of scope. PIVOT to an existing project if no distinct gap remains.
