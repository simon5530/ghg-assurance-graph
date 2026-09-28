# Results ledger

Historical entries below distinguish executed synthetic regression and public assertion
workflows from independent scientific validation. Documentation checks are not scientific
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

## 2026-09-28 — public Taiwanese company assertions, 0.3.0a1

Question: can real aggregate disclosures be ingested and inspected without faking
activity/factor lineage? Precommitted seeded selection chose UMC; TSMC is a lightweight
held-out transfer, not a blinded statistical evaluation. Original official 2024 reports
supply historical years. Exact sources/locators/hashes are in PUBLIC_COMPANY_SOURCES.

Method: `uv run python scripts/run_public_case.py` with each of three inputs listed
in [full reproduction](../../examples/public_companies/README.md); Python socket
connections and DNS blocked. Literal table values plus Fraction deltas form the
independent oracle. No LLM inference or source fetch occurs in reproduction.

Observed: 24 assertions (UMC Group7, parent9, TSMC8), 3 internally verified crates,
33 assessed checks (3 schema +30 metadata-presence declarations), 144 not-assessable
checks, zero invalid findings on the selected inputs. Upstream activity/factor
reconstruction available: 0/24. All causal drivers UNKNOWN. These counts measure
encoded checks/missingness, not accuracy of reported emissions or assurance.

UMC Group2023→2024 Scope1 −45,885 tCO2e; unspecified-basis Scope2 −112,353.
Group Scope3 2024 1,713,507 has no matched earlier year in the selected evidence.
TSMC2023→2024 Scope1 +229,841; Scope2 LB +1,208,803; MB +770,010; Scope3 +606,518.
No mixed-basis aggregate is produced. Boundary conflicts, expansion, unknown
restatement and rounding prevent unqualified like-for-like comparisons.

Full graph/explain/validate/diff/package/vault outputs are committed for inspection.
Same-machine isolated wheel reproduction is byte-identical for UMC Group and TSMC
with frozen inputs. Hosted CI and final publication status are separately verified.


## 2026-09-28 — full initial manuscript verification

Full pytest rerun: 448 passed, 11 upstream RDFLib warnings, 16.10 seconds.
Benchmark evaluator rerun: 10 TP / 0 FP / 0 FN; clean findings zero;
unassisted next-year residual +300 and absolute UNKNOWN 500 kgCO2e.
Public committed summaries inspected: 24 assertions, 33 assessed checks,
144 not assessable; 207 output files counted. All three statuses not_assessable,
all causes UNKNOWN; no new external assurance or causal experiment claimed.
Full manuscript and two original figures drafted; current official SoftwareX
4,000-word/six-figure guide and Version 6 March 2026 template inspected.
See SOURCE_LEDGER.md and MANUSCRIPT_METRICS.json. Owner approval pending.

## 2026-09-28 — independently fetched release and source preservation
Harness commit 82a7ea2c697af158619581bf6f960670a6c61e35, application 0.3.0a1. Hosted Ubuntu run 36382755169 passed after fetching published source, wheel and expected outputs with exact digest pins. Both installations regenerate every benchmark fixture and all 207 public-company output files identically; source regression suite passes. Artifact 10952658541, SHA256 24ddbb3249a70fcec097663a27c354738fd6e65edd76f2b91fb071d11078e40f, 531924 bytes. Local artifact download remains blocked by gh TLS, not a failed hosted run. Software Heritage full visit archives release object cbd30c9cc797de3bcff750ece70c01167ea2bb23 targeting original code b0de4b8a9373eee24d631cad14265e37bffcc75d; no DOI. Updated reading manuscript conservatively counts 2636 words, 98-word abstract, two figures. These are software verification/preservation results, not practitioner assurance.
