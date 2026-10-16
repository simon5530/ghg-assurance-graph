# GHG Assurance Graph

**v0.4.0a1 — research prototype, not an assurance opinion or certification.**

An offline Python toolkit that turns declared organizational greenhouse-gas
evidence into a queryable RDF/PROV graph, checks selected evidence constraints,
compares inventory versions, and exports portable evidence. It is not a
production factor database, complete inventory calculator or compliance service.

## Implemented and bounded

- 17 canonical record types, explicit units/versions and five safe graph queries.
- Separate regression only: [ExampleCo-GHG-001 benchmark](benchmark/README.md): three snapshots, independent numeric truth
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
[Reconciled SoftwareX manuscript](paper/softwarex/MANUSCRIPT.md) is available for
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

Use the [ExampleCo-GHG-001 regression guide](examples/worked_example/README.md) only for that separate software test population
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

Python 3.12.14 and uv; no API key or cloud model. Use the primary MOENV case:

```sh
uv sync --locked
uv run python scripts/run_moenv_example.py --out artifacts/moenv-worked
uv run python -m ghg_assurance_graph.moenv_example --check artifacts/moenv-worked/generated/2024
uv run ghgag graph explain urn:ghgag:moenv-demo-2024-electricity-result:v1 --input artifacts/moenv-worked/generated/2024/package.json
uv run ghgag graph query unreviewed_results --input artifacts/moenv-worked/generated/2024/package.json
uv run ghgag package verify artifacts/moenv-worked/packages/2024
uv run pytest -q
```

Open `artifacts/moenv-worked/REPORT.md` first. This executed 33-command workflow
checks both collections and canonical packages, traces all nine results, preserves
unreviewed statuses, verifies two crates and exports two Markdown vaults. The
[Chinese operating guide](docs/USAGE.zh-TW.md), [PDF](docs/user-guide/GUIDE.pdf),
[editable HTML](docs/user-guide/GUIDE.html) and [reference receipts](examples/moenv_training/workflow/REPORT.md)
use the same 2023/2024 baseline as the [revised SoftwareX draft](paper/softwarex/MANUSCRIPT.md).

Output directories must be new. The timestamp is an explicit replay input, not a
review date. `comparison.json` reports -568.064320 kgCO2e with causal explanations
UNKNOWN; **legacy `ghgag diff` does not accept these MOENV folders**. Its independent
ExampleCo regression is not evidence of primary-case change attribution.
The canonical crate alone excludes external monthly documents: preserve the whole
output directory and manifest. Collection checking and canonical checking are
separate. Workbook edits do not automatically update CSV, evidence or graphs.

The optional old regression commands remain documented only in
[the regression guide](examples/worked_example/README.md). Validation exits:
0 selected checks clean, 1 findings, 2 invalid/unsupported request.

## Documentation and publication

- [Architecture](docs/ARCHITECTURE.md), [requirements](docs/REQUIREMENTS.md),
  [domain model](docs/DOMAIN_MODEL.md), [ontology](docs/ONTOLOGY.md)
- [Reproducibility](docs/REPRODUCIBILITY.md), [dependencies](docs/DEPENDENCIES.md),
  [security](SECURITY.md), [audit](docs/PUBLICATION_AUDIT.md)
- [Related work](docs/RELATED_WORK.md), [research decision](docs/GATE_A.md),
  [publication strategy](docs/PUBLICATION_STRATEGY.md), [roadmap](.github/roadmap.json)
- [SoftwareX highlights](paper/softwarex/HIGHLIGHTS.md),
  [SoftwareX reconciled content draft](paper/softwarex/MANUSCRIPT.md),
  [results ledger](paper/softwarex/RESULTS_LEDGER.md),
  [distinct methods research](paper/methods/FUTURE_PAPER.md)
- [AI disclosure](docs/AI_USAGE_LOG.md), [contributing](CONTRIBUTING.md),
  [changelog](CHANGELOG.md), [citation](CITATION.cff), [MIT license](LICENSE)

No journal submission, DOI, independent assurance or empirical adoption is claimed.
