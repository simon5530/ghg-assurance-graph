# GHG Assurance Graph

**v0.4.0a1 — research prototype, not an assurance opinion or certification.**

An offline Python toolkit that turns declared organizational greenhouse-gas
evidence into a queryable RDF/PROV graph, checks selected evidence constraints,
compares inventory versions and public reported aggregates, and exports portable evidence. It is not a
production factor database, complete inventory calculator or compliance service.

## Implemented and bounded

- Additive [reported-disclosure profile](docs/REPORTED_CONTRACT.md): public totals
  remain ReportedAssertions, not invented activity/factor calculations. Missing
  upstream evidence is not assessable; numeric differences are not causal reductions.

- 17 canonical record types, explicit units/versions and five safe graph queries.
- [ACME benchmark](benchmark/README.md): three snapshots, independent numeric truth
  and ten defective fixtures; all factors are invented and nonproduction.
- [SHACL and domain validation](docs/VALIDATION.md): packaged pySHACL shapes plus
  independent raw-row rules; ten true positives, zero false positives/negatives on
  the public synthetic fixture set—not a blind generalization result.
- [CarbonDiff](docs/CARBONDIFF.md): exact Decimal reconciliation, stable-ID matching,
  explicit semantic declarations and visible UNKNOWN residuals. Seven supplied
  semantic labels plus two mechanical components match nine expected components;
  this is not autonomous causal inference.
- [RO-Crate packages](docs/EVIDENCE.md), [Obsidian notes](docs/OBSIDIAN.md),
  [generic external JSON/CSV adapter](docs/ADAPTERS.md) and
  [bounded read-only tools](docs/TOOLS.md).

**Gate A: scoped GO for the compositional evidence overlay**, not a novelty or
assurance claim. [Exact original-phase matrix](docs/ROADMAP_ACCEPTANCE.md).
The previous v0.3.0a1 release has [historical fresh-host reproduction](docs/FRESH_RELEASE_REPRODUCTION.md)
and [source preservation](docs/ARCHIVE_STATUS.md). Those records do not certify this revision.
This remains a qualified alpha, not a stable v1.0 or journal submission.
[Full initial SoftwareX manuscript](paper/softwarex/MANUSCRIPT.md) is available for
human review. Authorship/declarations and official submission formatting remain
owner decisions. PACT/openLCA/Brightway integrations and Jev remain optional;
[adapter assessment](docs/ADAPTER_FEASIBILITY.md) and [AI decision](docs/OPTIONAL_AI_DECISION.md).

[ISO review](docs/STANDARDS_ALIGNMENT.md) inspected English ISO 14064-1:2018
privately, including normative Annexes D/E. Only paraphrases and references are
published. Gas-resolved reporting, completeness/significance, uncertainty and
organizational controls remain gaps; no full conformity claim.

## Complete fictional worked example

Start with the [ACME step-by-step guide](examples/acme_worked_example/README.md)
and [complete sample report](examples/acme_worked_example/sample/REPORT.md).
One command executes the selected-source inventory through calculation evidence,
graphs, validation, explanation, unassisted/annotation-assisted differences,
verified evidence packages and Obsidian notes, with offline command receipts.
All activities, factors and source documents are explicitly fictional; simulated
reviews are not human assurance. The [ten hand-authored cases](examples/README.md)
remain small schema examples, distinct from the three-snapshot ACME workflow.
Public-company demonstration inputs/outputs have been removed from the current tree:
missing upstream records cannot be repaired by invented data. Historical tags and
release assets remain unchanged; the generic reported-disclosure API is retained.

## Reproduce locally

Python 3.12.14 and uv; no API key or cloud model.

```sh
uv sync --locked
uv run python scripts/run_acme_example.py --out artifacts/acme-worked
uv run ghgag benchmark run
uv run ghgag graph build benchmark/generated/2026-v1
uv run ghgag validate benchmark/generated/2026-v1
uv run ghgag diff benchmark/generated/2025-v2 benchmark/generated/2026-v1
uv run ghgag package create benchmark/generated/2026-v1 --out artifacts/acme-crate --created-at 2026-09-28T00:00:00Z --data-version acme-0.1-2026-v1
uv run ghgag package verify artifacts/acme-crate
uv run ghgag export obsidian artifacts/acme-vault --input benchmark/generated/2026-v1
uv run pytest -q
```

Output directories must be new. The example timestamp is a declared reproducibility
input, not a claim about when a user runs it. Default diff leaves unsupported
semantic changes UNKNOWN: +210 kgCO2e delta, +300 signed residual, 500 absolute
unknown exposure for 2025-v2→2026-v1. Location/market-based totals are never added.
Validation exit codes: 0 clean selected checks, 1 findings, 2 invalid request.

## Documentation and publication

- [Architecture](docs/ARCHITECTURE.md), [requirements](docs/REQUIREMENTS.md),
  [domain model](docs/DOMAIN_MODEL.md), [ontology](docs/ONTOLOGY.md)
- [Reproducibility](docs/REPRODUCIBILITY.md), [dependencies](docs/DEPENDENCIES.md),
  [security](SECURITY.md), [audit](docs/PUBLICATION_AUDIT.md)
- [Related work](docs/RELATED_WORK.md), [research decision](docs/GATE_A.md),
  [publication strategy](docs/PUBLICATION_STRATEGY.md), [roadmap](.github/roadmap.json)
- [SoftwareX highlights](paper/softwarex/HIGHLIGHTS.md),
  [SoftwareX full initial manuscript](paper/softwarex/MANUSCRIPT.md),
  [results ledger](paper/softwarex/RESULTS_LEDGER.md),
  [distinct methods research](paper/methods/FUTURE_PAPER.md)
- [AI disclosure](docs/AI_USAGE_LOG.md), [contributing](CONTRIBUTING.md),
  [changelog](CHANGELOG.md), [citation](CITATION.cff), [MIT license](LICENSE)

No journal submission, DOI, independent assurance or empirical adoption is claimed.
