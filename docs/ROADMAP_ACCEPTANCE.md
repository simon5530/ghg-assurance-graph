# Original-plan acceptance matrix

2026-09-28. The complete 2,159-line original specification was read, including original exit criteria and definition of done. The owner authorizes all remaining engineering phases and an initial full SoftwareX manuscript. Optional experiments are not silently made mandatory.

Run `python scripts/check_phase_acceptance.py --run` in the locked environment for an executable phase-to-file/test inventory. It reports missing evidence and actual test exit codes; file presence does not prove scientific approval. Full baseline: 448 tests passed, seven documentation-oracle tests, lint/format and wheel/sdist build passed. The hosted released-artifact run is tracked separately below.

| Phase | Original exit criterion | Evidence and bounded status |
|---|---|---|
| 0 | Defensible gap; no inspected mature tool covers full combination | Current comparative decision in [Gate A](GATE_A.md), primary-source [comparison](RELATED_WORK.md), original 30-issue backlog. Not a universal novelty proof. |
| 1 | Representative examples without per-example ad hoc fields | Complete bounded model: 17 types, ten hand-authored examples, JSON/JSON-LD/Turtle, schema/unit/identity tests in `test_contract.py`. |
| 2 | Cases understandable and reproducible with separate ground truth | Complete synthetic benchmark: fixed seed, three versions, twelve source types, documented fifteen change/defect cases, independent Fraction/literal oracle, public development/holdout split. Domain realism is a limitation, not fabricated practitioner approval. |
| 3 | Every clean result traces to source/factor/method/version/review | Complete bounded graph builder and five queries; `test_graph.py`; collision/reference/lineage failures explicit. |
| 4 | Defects detected or scoped out, FP characterized, automatic metrics | Complete selected checks: real pySHACL plus raw-row rules; 10 TP, 0 FP/FN on public synthetic fixtures; class/split metrics. Not standards conformity. |
| 5 | Reconciliation, cause evaluation, explicit unresolved cases | Complete ACME deterministic convention, nine annotation-assisted components, exact Decimal reconciliation and unknown residual. General RDF matching and causal inference not claimed. |
| 6 | Fresh clone verifies package without original directory | Complete bounded RO-Crate directory profile, versions/digests/commands, JSON-LD/Turtle, isolated verification and tamper tests; no authenticity guarantee. |
| 7 | Usable graph-derived vault, no manual edits | Complete generated notes/frontmatter/index/wikilinks with link tests; no fabricated Obsidian application screenshot. Optional for v1. |
| 8 | At least one external result format mapped | Complete generic JSON/CSV external-result profile and fixtures/tests. Vendor engines are optional and not executed. Public aggregates have a separate missingness-preserving profile. |
| 9 | Evidence-linked question set and measurable grounding | Complete deterministic seven-action facade and executable evidence/arithmetic/permission questions. No natural-language router or model-performance study. Optional for v1. |
| 10 | Publish Jev only for meaningful reproducible comparison; otherwise exclude | [Capability reassessed; optional experiment excluded](OPTIONAL_AI_DECISION.md). Full non-Jev baseline evaluated; no invented credential blocker or model metrics. |
| 11 | Mandatory software scope, tests/CI, tagged archive, licenses, fresh-machine reproduction | Published qualified v0.3.0a1 source/wheel/output assets; [Software Heritage source archive verified](ARCHIVE_STATUS.md). Fresh-runner source AND wheel reproduction [protocol and observed status](FRESH_RELEASE_REPRODUCTION.md). Hosted run 36382755169 passed. Stable v1.0 freeze is not claimed; local proof download and release-readiness reconciliation remain distinct. |

## Research gates versus engineering and submission

Gate A is decided against the original bounded comparative gap, not an invented requirement for an independent interview. Gate B asks whether cases represent meaningful assurance/change problems: method transitions, boundary additions, missing evidence and allocation are present, beyond toy multiplication, but external representativeness remains untested. Gate C permits paper preparation because SHACL/detection and CarbonDiff have quantitative outputs; semantic labels are supplied, not autonomously discovered.

A hosted clean GitHub runner **does** qualify as fresh-machine software reproduction. It does not qualify as human practitioner review. Phase 11 asks for Zenodo **or equivalent**, and DOI **if available**; verified Software Heritage content-addressed source preservation is an equivalent source archive, not a DOI or promise to preserve release binaries. Actions evidence expires on its configured retention; retain downloaded proof separately.

Gate D before journal submission remains separate: exact official template, human-approved authorship/affiliations/CRediT/funding/conflicts, verified article claims and release freeze. The initial manuscript is not submission. No journal action, account creation, spending or invented human approval is authorized. Methods-paper #30 is distinct future research, not an additional software phase. JOSS #24 was superseded/not planned by the chosen SoftwareX + methods route.

## Invariants and breadth

Location/market electricity are alternative series, never additive. Precharacterized CO2e is not characterized again. Invalid units/identities/lineage fail closed. All synthetic factors are nonproduction. Private ISO text stays outside the repository; published original clause paraphrases do not establish full conformity. Public UMC/TSMC runs contain 24 explicitly mapped assertions across three datasets, 33 assessed metadata checks and 144 not assessable; no upstream recalculation or causal reduction inference. This is not arbitrary-PDF support.

## Remote reconciliation

The v0.3.0a1 release is **public**, not a draft; four assets were verified. Earlier API/upload-TLS blocker statements in old snapshots are historical, not release status. Current normal local gh access regressed on 2026-09-28; Git push and anonymous public API reads work. Remote issue mutations must wait for supported authenticated access and exact readback, without TLS bypass. #9/#10 were previously closed against graph tests, #24 as not planned. Individual issue contracts can be stricter than original phase exits: #13 explicitly requests domain-reviewed examples and remains open until actual review. No blanket closure of research, v1.0, submission or methods work.
