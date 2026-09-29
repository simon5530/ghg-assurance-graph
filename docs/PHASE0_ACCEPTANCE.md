# Phase 0 acceptance against the original specification

Historical record, 2026-09-25: all 2159 lines of the original project-plan attachment were read. The attachment itself is not redistributed; this is a public-safe traceability summary.

| Specification | Artifact / result |
|---|---|
| Sections 10–11, 25: public pre-alpha scaffold, MIT, governance | Public MIT scaffold verified on 2026-09-26 (Asia/Taipei); anonymous access, matching remote files and hosted documentation CI passed. |
| Sections 4, 11, 25: minimum competitors and feature matrix | [Related work](RELATED_WORK.md), including seven required ecosystems and additional near-neighbors. Prior report provenance and independent spot checks distinguished. |
| Sections 4.4, 12–14: precedent and publication plan | [Precedent](SOFTWAREX_PRECEDENTS.md), [policy review](PUBLICATION_STRATEGY.md), paper templates. SoftwareX official policy inaccessible; gap recorded. |
| Sections 1–3, 11: problem, requirements, two ADRs | Local documents and proposed ADRs present; [Gate A scoped GO, reassessed 2026-09-28](GATE_A.md). |
| Sections 16–17: 11 milestone titles, 18 labels, 30 exact issue titles | Machine-readable [.github/roadmap.json](../.github/roadmap.json), with AC/dependencies/scope/non-goals/oracles. All 11 milestones, 18 roadmap labels and 30 exact issue titles verified remotely; IDs recorded in manifest. GitHub also retains 10 default labels (28 total). |
| Sections 21–24: security, AI disclosure, checks, scoped commit | [Publication audit](PUBLICATION_AUDIT.md); no domain tests/results claimed. |
| Section 25: learning log | [Learning log](LEARNING_LOG.md), not a substitute for later runnable domain examples. |

## Historical Phase 0 deviations (2026-09-25 snapshot)
The recommended root in section 10 includes pyproject.toml, uv.lock, .python-version and test/lint/benchmark CI. These are deliberately deferred: Phase 0 has no domain package or selected dependencies, and fake empty test/benchmark workflows would misrepresent implementation. Only the real standard-library documentation checker and its CI are supplied. ADRs are in root `adr/` rather than `docs/adr/`; links resolve. These differences are disclosed, not exact-layout acceptance claims.

At that historical Phase 0 snapshot no domain implementation existed. This is no longer the current state.

## Current reassessment — 2026-09-28

The complete original plan was reread. [Gate A](GATE_A.md) is now **scoped GO** for an organizational assurance/interoperability overlay, supported by refreshed primary-source interfaces and the same ExampleCo-GHG-001 case compared against CarbonLedger, Arrhen and TEC/PECO + SHACL + RO-Crate. This is not universal absence proof or algorithmic novelty. The earlier practitioner prerequisite was analyst-added, not part of original Gate A or Phase 11.

The repository now contains the typed package, graph/shapes, benchmark, CarbonDiff and evidence package implementation. Selected graph/validation/diff/evidence tests rerun here: **196 passed**. See [related work](RELATED_WORK.md) for exact command, revision, case output and limits. This updates stale Phase 0 statements; it does not certify all later phase acceptance criteria.

Public repository/backlog checks above are retained as dated 2026-09-26 evidence, not reverified in this documentation pass. Human/domain review remains unperformed and is transparently recorded in the [owner questionnaire](DOMAIN_REVIEW.md); no external endorsement or assurance opinion is inferred. Release/archive, fresh-machine reproduction, actual quantitative evaluation and official submission requirements remain separate original gates.
