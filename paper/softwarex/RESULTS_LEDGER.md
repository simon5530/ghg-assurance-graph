# Results ledger

No scientific experiments or domain measurements have been run. Documentation check
results belong in the publication audit, not in a scientific performance table.

## Entry template (copy only after an actual run)

- Date and research question:
- Commit / software / benchmark / ontology versions:
- Exact command and configuration:
- Input and output artifact digests:
- Observed results, denominators, and uncertainty:
- Baseline and comparison:
- Interpretation and claims supported:
- Unsupported claims and limitations:
- Reproduction status and reviewer:


## 2026-09-26 — Phase 1 representation experiment
- Question: can ten representative authored cases share a closed typed schema?
- Software 0.1.0a1; schema/namespace 0.1.0/0.1; no benchmark version. Content commit
  is the Phase 1 implementation commit in Git history; no self-referential SHA.
- Commands: `uv run pytest -q`, `uv run python examples/hand_authored.py`, Ruff check
  and format, documentation checker and oracle tests; locked Python 3.12.14.
- Observed: 44 domain/serialization test cases pass; all ten cases validate and
  export JSON/JSON-LD/Turtle (30 files). All 17 classes are exercised. Seven
  documentation oracle tests pass. Ten upstream RDFLib JSON-LD deprecation warnings.
- Independent checks: JSON Schema validation, explicit known conversion constants,
  hand-authored expected values, RDF isomorphism and negative identity/reference
  mutations. No baseline comparison, precision/recall or change attribution measured.
- Interpretation: this bounded representation works for these cases. It does not
  establish accounting validity, novelty, practitioner need or standard compliance.
- Reproduction: isolated same-machine clean-copy install recorded in audit; human
  review pending. SoftwareX submission policy and research HOLD remain unresolved.

## 2026-09-26 — Phase 2 ACME benchmark v0.1

Question: can standards-bounded synthetic inventory changes and defects be reproduced
without an AI or circular numerical oracle? Software 0.1.0a1; benchmark 0.1;
canonical schema 0.1.0 unchanged; baseline commit 3a5c540. Final reviewed SHA is
reported by the publication completion record, not self-referentially here.

Method: `uv run python -m ghg_assurance_graph.benchmark --seed 20250926`;
`uv run pytest -q`; docs checker and seven checker tests; Ruff lint/format; uv build.
Three snapshots, 158 canonical records and 15 results each; ten separate raw defect
fixtures. Six development/four publicly visible holdout labels. 86 tests passed
(44 existing, 42 benchmark), seven docs tests passed. JSON roundtrips, duplicate
generation byte/hash equivalence, independent Fraction and literal numerical oracle,
per-source and per-scope reconciliation passed. Partial totals 3820/3850/4060 kgCO2e;
same-year +30, next-year +210; explicit activity-first components, zero residual
under the authored scenario. Ten existing upstream RDFLib warnings not suppressed.

An isolated publication-file copy/new locked virtualenv reproduced 86 tests and
both docs commands on the same machine. Wheel/sdist built. No fresh-machine claim.
No SHACL detector, inferred change taxonomy, performance/precision/recall/F1,
production compliance or research novelty is measured. Figure candidate: future
scenario/evidence table, not yet a quantitative assurance evaluation figure.
ISO full-clause review remains unverified; see standards alignment. Gate A HOLD.

## 2026-09-27 — Phase 3 provenance
Question: can each clean synthetic result resolve its asserted lineage?
Method: tests/test_graph.py independently checks 45 result chains across three
snapshots, five query answer sets, explicit revisions, collisions and failure paths.
Observed: 45/45 traceable required chains; no inferred cross-snapshot revisions.
Version: software 0.1.0a1, benchmark 0.1, ontology 0.1; exact published commit is
reported after publication. Reproduce with [graph guide](../../docs/GRAPH.md).
Interpretation: stored-assertion traceability only, not source authenticity, full
inventory coverage, assurance evaluation or certification. ISO review UNVERIFIED;
Gate A HOLD. Parent/practitioner review pending. Potential lineage figure, no
comparative performance claim.
