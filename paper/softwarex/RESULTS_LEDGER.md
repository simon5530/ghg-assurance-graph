# Results ledger

Current scope is synthetic-only ExampleCo-GHG-001 validation (0.4.0a1). Earlier entries below
are explicitly historical engineering records, not current-release validation. Documentation checks are not scientific
performance measurements.

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

## 2026-09-26 — Phase 2 ExampleCo-GHG-001 benchmark v0.1

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

## 2026-09-28 — deterministic continuation, 0.2.0a1

Question: can selected synthetic provenance checks, attribution and portable
exports be executed without an AI authority? Baseline schema/benchmark 0.1 retained.

Method: `uv run ghgag benchmark run`; `uv run pytest -q`; separate literal/Fraction
truth for arithmetic and annotations declared separately from numeric answers.

Observed: 297 tests pass; 10 seeded defects TP=10, FP=0, FN=0, precision/recall/F1=1;
development 6/6 and publicly visible holdout 4/4. Three clean snapshots have zero
findings. Annotation-assisted CarbonDiff matches 9/9 expected component labels and
amounts, MAE=0, residual=0, total deltas +30 and +210 kgCO2e. Seven semantic labels
are caller assertions, not model predictions. Unassisted next-year residual +300,
absolute UNKNOWN exposure 500; no silent causal claims. CLI end-to-end crate/vault
workflow passes. Eleven RDFLib deprecation warnings remain.

Interpretation: encoded public synthetic contracts work; not blind accuracy,
standards conformity, causal identification or empirical assurance performance.
Independent practitioner/fresh-machine/archive gates remain open.

Figure candidates: constraint coverage, assisted versus unassisted decomposition,
portable evidence structure. Source data/standards are not embedded in figures.

## 2026-09-28 — independent source review and completion repair

Version: working source after published 0.2.0a1 / 61e0d34; benchmark/schema 0.1.
Question: do mandatory operations hold outside the ten seeded cases?
Method: raw-graph mutation, malformed inputs, exact conversion under Decimal
precision=2, digest/symlink/JSON adversarial tests, seven deterministic action
questions, full pytest, docs/link checks, lint, build and socket-blocked CLI.
Observed full run: 355 tests passed (11 upstream RDFLib deprecation warnings);
selected validation remains TP=10 FP=0 FN=0. Decimal-context rounding and missing
snapshot classification checks were found and repaired, demonstrating why the
seed score alone is insufficient. SHACL factor/review literals now have direct
raw-graph tests; package reads reject race-time symlinks and bound sizes.
Seven evidence actions are tested without natural-language/model inference.
Original figure: [evaluation](figures/evaluation.svg), regenerated by
`python scripts/render_figures.py` from the evaluator (byte-equality test).
No blind generalization, external practitioner review, conformity, AI evaluation,
DOI, journal submission or fresh-machine reproduction is inferred.


## Historical v0.3 scope retirement

The earlier real-company workflow and release-reproduction entries are superseded
for this manuscript; their original records remain in Git history. No external
validation, output counts, hosted-run status or archival identifiers from that
release are carried forward as current evidence.

## 2026-09-28 — 0.4.0a1 synthetic-only full manuscript

The complete initial draft retains all five SoftwareX sections, metadata,
limitations, declarations and nine references. Official template remains Version 6
(March 2026), maximum 4,000 words and six figures. Human author fields remain pending.
The detailed example shows all 15 source amounts and activity-first electricity
decomposition. Current verification results are recorded below after execution.

Executed verification (local Python 3.12 environment):
- ".venv/bin/python -m pytest -q tests/test_figures.py tests/test_diff.py tests/test_graph.py tests/test_benchmark.py": 173 passed in 5.28 s.
- Direct evaluate_benchmark call: TP=10, FP=0, FN=0; precision/recall/F1=1.0;
  all three clean finding counts zero. Totals 3820.0, 3850.0, 4060.00;
  deltas 30.0 and 210.00. Unassisted signed/absolute UNKNOWN: 10/10 and 300/500.
- Table oracle tests compare all 45 manuscript row values with independent
  expected amounts and recompute each total. Assisted component and lineage
  tests are included in the 173-test selection. No full-suite count is asserted here.
- Figure and HTML byte-equality tests passed; Ruff lint/format and git diff --check
  passed for the owned sources. Both figure generators executed.
- Renderer: 2,694 conservative words, 96-word abstract, two figures; below the
  official 4,000-word/six-figure limits. Chrome generated a new complete 372,630-byte
  PDF, recovered after its bounded shutdown timeout. Native PDFKit independently
  opened all nine nonempty pages and extracted 23,406 characters; current version,
  synthetic-only wording and exact runner command are present, retired company
  names absent. No full visual-proofreading or byte-identical PDF claim: browser
  PDF metadata may vary between renders; HTML/SVG content is deterministic.
- Runner --help inspected: --out required; --python optional; absent/empty output
  directory required. The runner's end-to-end execution is owned by the parallel
  implementation task, not counted as executed in this paper-only verification.

Scope-correction lesson: replacing an evaluation population requires updating
abstract, example, bibliography, metadata, ledgers and regenerated reading artifacts
alongside the prose; old release reproduction must not become current evidence.
The table and scope regression tests guard this contract.
