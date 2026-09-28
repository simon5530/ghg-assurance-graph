# Original-plan acceptance matrix

2026-09-28: owner authorizes engineering through all remaining phases. This
supersedes earlier phase-only authorization, **not** research GO or external review.
The complete original 2,159-line plan was read. Current implementation status is
tracked below; phase completion requires code, tests, reproducible commands, honest
docs, limitations, publication evidence and a scoped commit, not merely files.

| Original phase | Inspectable acceptance | Current evidence status | Stop gate / optionality |
|---|---|---|---|
| 0 Gap verification | Comparative workflow evidence, original backlog, explicit gap decision | Scaffold/research evidence exists; Gate A HOLD | Independent practitioner/prior-art comparison missing; owner engineering exception is not GO |
| 1 Canonical model | 17 record types, 10 examples, identity/unit/RDF schema tests | Implemented, prior verified baseline | Contract/schema 0.1 retained |
| 2 Benchmark | Three fixed-seed versions, separate truth, documented defects and assumptions | Implemented, prior verified baseline | Gate B domain representativeness remains unreviewed |
| 3 Graph | Five queries, collision-safe graph, complete clean provenance | Implemented, prior verified baseline | Only allowlisted local queries |
| 4 SHACL | Packaged Turtle shapes, pySHACL, stable findings, class-wise precision/recall/F1 | Implemented and locally tested; scope limits below | Synthetic defect coverage is not standards conformity |
| 5 CarbonDiff | Stable matching, typed causes, numeric attribution, residual, independent reconciliation | Implemented and locally tested; scope limits below | Gate C requires quantitative results; no causal decarbonization claim |
| 6 Evidence | Manifest, versions, digests, JSON-LD/Turtle, RO-Crate, isolated verification | Implemented and locally tested; scope limits below | No source-directory dependence; tampering fails closed |
| 7 Obsidian | Graph-derived notes, frontmatter, stable links/index, link tests | Implemented and locally tested; scope limits below | Nonblocking for v1; screenshot only if real interface inspected |
| 8 Adapters | At least one external result format mapped with provenance | Implemented and locally tested; scope limits below | Generic adapter prioritized; PACT/openLCA/Brightway individually optional |
| 9 Agent tools | Bounded deterministic tools, evidence-linked questions, grounding measured | Seven deterministic actions and evidence-linked question tests implemented; no LLM study | Optional for v1; no hosted LLM required |
| 10 Jev | Opt-in baseline comparison, probabilities/cost/privacy logs, meaningful result | Deferred | Optional; no spend/model credentials authorized, exclude from paper results |
| 11 SoftwareX v1.0 | All mandatory software features, quantitative evaluation, CI, tagged archive, licenses, fresh-machine reproduction | Not met | Fresh-machine reproduction and archive remain unproven; reasonable GitHub prerelease publication is authorized |
| SoftwareX manuscript/submission | Current official template, authorship/disclosures, current related work, Gate D | Draft only | Submission and archival DOI publication not authorized here |
| Methods extension | Distinct research question, baselines/sensitivity/new results | Research plan only | No fabricated study, novelty, external use or journal acceptance |

Original Gate E / JOSS is superseded by the owner's chosen SoftwareX + distinct
methods route. Keep issue 24 as historical superseded work, not a new JOSS scaffold.

## Invariants and verification

- Location/market-based electricity are alternative series, never additive totals.
- Precharacterized CO2e is never multiplied by GWP again; raw gases require a basis.
- Duplicate identities, cross-version joins, missing/wrong provenance fail closed.
- Synthetic factors remain explicitly nonproduction; no licensed standards text.
- Schema/benchmark 0.1 and baseline fixture history remain available; API evolution
  must not silently relabel earlier benchmark or validation results.
- Fresh local virtual environments and remote CI are evidence, not a claim that an
  independent practitioner reproduced the system on a fresh machine.

See [research HOLD](GATE_A.md), [standards coverage](STANDARDS_ALIGNMENT.md),
[publication strategy](PUBLICATION_STRATEGY.md) and [roadmap](../.github/roadmap.json).

## Verified engineering scope and unresolved breadth
The published 0.2.0a1 baseline had 297 tests; the subsequent independent audit
adds adversarial tests and facade coverage (see results ledger for the current run).
Phase 4 detects all ten seeded defects with zero FP/FN; clean graphs pass real SHACL.
Phase 5 calculated attribution is ACME raw-row matching, not general RDF version matching.
The additive 0.3.0a1 reported-disclosure profile compares public aggregate series
with UNKNOWN causes and explicit basis qualifications; it does not extend causal attribution. Semantic cause
accuracy is annotation-assisted; no automatic causal attribution. Phase 6 is a
bounded directory RO-Crate profile, not signed evidence or fetched source documents.
Phase 7 emits tested notes/links; no Obsidian application screenshot was fabricated.
Phase 8 maps a defined generic external-result format, not an executed vendor engine.
An additive public-aggregate profile avoids fictitious external calculation lineage;
manual attributable numeric fact mapping is required, not arbitrary PDF ingestion.
Phase 9 implements the seven planned deterministic actions with explicit host-only
export consent and evidence-linked questions. No natural-language router or AI
grounding study is claimed; those optional experiments are not prerequisites for
the deterministic facade. Remaining Phase 11 gates are not waived.

## GitHub reconciliation blocker
On 2026-09-28 authenticated `gh api` issue listing failed certificate verification.
No TLS bypass, credential extraction, trust changes or alternative authenticated
HTTP route was attempted. No issue mutation or repository-description edit is claimed.
The manifest records local evidence, not remote issue closure. After normal access
recovers, read current issues before updating; do not recreate the original 30.
Close #9/#10 only against graph evidence, then individually assess #11/#12/#14–#19/#22;
#13 still requires domain-reviewed examples. #24 should close as superseded/not planned,
not completed. #25–#27/#30 remain open; #20/#21/#29 are optional deferred; #28 deterministic scope implemented.
Desired repository description: Offline experimental GHG provenance, selected checks,
change attribution and portable evidence; not certification.

## Exact original final-gate interpretation

Phase 11 explicitly requires a fresh-machine reproduction and an archive in Zenodo
or equivalent; it lists a release DOI **if available**. Gate D, before journal
submission, separately requires release DOI/archive and the populated official
template. A same-machine virtual environment is not a fresh machine. Hosted CI
is a fresh runner but does not constitute practitioner review or research impact.
The original Phase 11 list does not require independent practitioner approval;
that remains the project's research/domain evidence limitation under Gates A/B,
not an invented requirement for publishing a clearly qualified alpha release.
The owner has authorized reasonable GitHub release publication. Remaining GitHub
API certificate failures are technical blockers, not missing release permission.
Journal submission, DOI account operations and paid services remain separate.
