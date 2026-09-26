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
