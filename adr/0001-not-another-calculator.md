# ADR 0001: Not another calculator

Status: proposed research boundary, pending gate review.

Context: accounting engines already calculate emissions; rebuilding them would not
establish an assurance-evidence contribution.

Decision proposed: focus on evidence lineage, explicit constraints, version-change
explanations, and reproducible packaging. Reuse external calculation engines.

Alternatives: another calculator; a spreadsheet-only workflow; extend an existing
provenance tool. Related-work review must determine whether a new toolkit is warranted.

Consequences: numerical correctness still needs tests, but engine completeness is
out of scope. PIVOT to an existing project if no distinct gap remains.
