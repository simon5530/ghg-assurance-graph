# GHG Assurance Graph

**v0.4.0a1 — research prototype, not an assurance opinion or certification.**

An offline Python toolkit that turns declared organizational greenhouse-gas
evidence into a queryable RDF/PROV graph, checks selected evidence constraints,
compares inventory versions, and exports portable evidence. It is not a
production factor database, complete inventory calculator or compliance service.

## Implemented and bounded

- 17 canonical record types, explicit units/versions and five safe graph queries.
- [ExampleCo-GHG-001 benchmark](benchmark/README.md): three snapshots, independent numeric truth
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

## MOENV-guided internal collection (primary worked case)

**2023 and 2024, entirely fictional single manufacturing plant.** Original collection
forms map to MOENV inventory tables 1–11 and the all-industry report chapters.
120 monthly records and 122 synthetic evidence documents preserve meter readings,
fuel-stock balances and refrigerant mass balances. Includes blank CSV/XLSX templates,
filled XLSX workbooks, annual reports, gas-level arithmetic and canonical graphs.

- [Start / download workbooks](examples/moenv_training/README.md)
- [Official source/version evidence](examples/moenv_training/SOURCES.md)
- [Field mapping and evidence workflow](examples/moenv_training/FIELD_MAP.md)
- [Scope and acceptance contract](docs/MOENV_TRAINING_CONTRACT.md)

```sh
uv run python -m ghg_assurance_graph.moenv_example --out artifacts/moenv-training
uv run ghgag validate artifacts/moenv-training/2024/package.json
```

Historical electricity factor vintages are replayed for teaching; synthetic fuel
LHV/activity and unquantified uncertainty mean this is not a current statutory
filing or assurance opinion. Canonical CO2e projection is explicit; gas-resolved
companion tables do not add a gas schema to the core.

## Earlier synthetic software-regression example

Start with the [illustrated PDF workbook](docs/user-guide/GUIDE.pdf) ([HTML](docs/user-guide/GUIDE.html)), then the [ExampleCo-GHG-001 step-by-step guide](examples/worked_example/README.md)
and [complete sample report](examples/worked_example/sample/REPORT.md).
One command executes the selected-source inventory through calculation evidence,
graphs, validation, explanation, unassisted/annotation-assisted differences,
verified evidence packages and Obsidian notes, with offline command receipts.
All activities, factors and source documents are explicitly fictional; simulated
reviews are not human assurance. The [ten hand-authored cases](examples/README.md)
remain small schema examples, distinct from the three-snapshot ExampleCo-GHG-001 workflow.
The primary collection workflow is now the [MOENV-guided two-year internal training case](examples/moenv_training/README.md).
The older ExampleCo benchmark remains a software regression suite, not an industry
reference, company comparison or substitute for MOENV collection design.
The optional reported-assertion API is retained only as a bounded interoperability
feature; it is not the project evaluation dataset.

## Reproduce locally

Python 3.12.14 and uv; no API key or cloud model.

```sh
uv sync --locked
uv run python scripts/run_example.py --out artifacts/exampleco-ghg-001-worked
uv run ghgag benchmark run
uv run ghgag graph build benchmark/generated/2026-v1
uv run ghgag validate benchmark/generated/2026-v1
uv run ghgag diff benchmark/generated/2025-v2 benchmark/generated/2026-v1
uv run ghgag package create benchmark/generated/2026-v1 --out artifacts/exampleco-ghg-001-crate --created-at 2026-09-28T00:00:00Z --data-version exampleco-ghg-001-0.1-2026-v1
uv run ghgag package verify artifacts/exampleco-ghg-001-crate
uv run ghgag export obsidian artifacts/exampleco-ghg-001-vault --input benchmark/generated/2026-v1
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
