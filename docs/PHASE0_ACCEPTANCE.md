# Phase 0 acceptance against the original specification

2026-09-25: all 2159 lines of the original project-plan attachment were read. The attachment itself is not redistributed; this is a public-safe traceability summary.

| Specification | Artifact / result |
|---|---|
| Sections 10–11, 25: public pre-alpha scaffold, MIT, governance | Public MIT scaffold verified on 2026-09-26 (Asia/Taipei); anonymous access, matching remote files and hosted documentation CI passed. |
| Sections 4, 11, 25: minimum competitors and feature matrix | [Related work](RELATED_WORK.md), including seven required ecosystems and additional near-neighbors. Prior report provenance and independent spot checks distinguished. |
| Sections 4.4, 12–14: precedent and publication plan | [Precedent](SOFTWAREX_PRECEDENTS.md), [policy review](PUBLICATION_STRATEGY.md), paper templates. SoftwareX official policy inaccessible; gap recorded. |
| Sections 1–3, 11: problem, requirements, two ADRs | Local documents and proposed ADRs present; [Gate A HOLD](GATE_A.md). |
| Sections 16–17: 11 milestone titles, 18 labels, 30 exact issue titles | Machine-readable [.github/roadmap.json](../.github/roadmap.json), with AC/dependencies/scope/non-goals/oracles. All 11 milestones, 18 roadmap labels and 30 exact issue titles verified remotely; IDs recorded in manifest. GitHub also retains 10 default labels (28 total). |
| Sections 21–24: security, AI disclosure, checks, scoped commit | [Publication audit](PUBLICATION_AUDIT.md); no domain tests/results claimed. |
| Section 25: learning log | [Learning log](LEARNING_LOG.md), not a substitute for later runnable domain examples. |

## Explicit deviations and deferred items
The recommended root in section 10 includes pyproject.toml, uv.lock, .python-version and test/lint/benchmark CI. These are deliberately deferred: Phase 0 has no domain package or selected dependencies, and fake empty test/benchmark workflows would misrepresent implementation. Only the real standard-library documentation checker and its CI are supplied. ADRs are in root `adr/` rather than `docs/adr/`; links resolve. These differences are disclosed, not exact-layout acceptance claims.

No Phase 1 Pydantic classes, ontology, example records, serializers or domain tests were implemented. Later CLI commands, benchmark, agents and Jev are planned only. Publication infrastructure is complete: public repository, GitHub roadmap and remote checks are verified. Research Gate A remains HOLD; domain review, comparative evidence and explicit authorization are still required before Phase 1.
