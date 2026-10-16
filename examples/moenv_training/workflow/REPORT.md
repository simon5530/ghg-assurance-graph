# MOENV 2023/2024 executed workflow

Fictional MOENV-inspired internal evidence; not statutory filing or assurance

Source documents, quantities, LHV and review roles are synthetic. Factor sources and historical electricity policy remain explicit in the repository source ledger.

| Year | kgCO2e | Results / lineages | Unreviewed | Crate verified | Vault notes |
|---|---:|---:|---:|---|---:|
| 2023 | 95797.4735640 | 4 | 4 | True | 127 |
| 2024 | 95229.4092440 | 5 | 5 | True | 140 |

## Inspect in order

1. generated/YEAR/04-activity.csv and evidence/: monthly originals and hashes.
2. generated/YEAR/05-quantification.csv: gas arithmetic; synthetic LHV and historical factor policy.
3. stages/YEAR/collection-check.json and validation.json: separate collection and graph checks.
4. stages/YEAR/explain/: actual lineage queries; unreviewed.json preserves pending review.
5. comparison.json: arithmetic delta -568.064320 kgCO2e, all causal explanations UNKNOWN; not CarbonDiff.
6. packages/YEAR/: verified canonical RO-Crates; monthly source files remain in generated/, not inside these closed-profile crates.
7. vaults/YEAR/: graph-derived Markdown, not authenticated review or tested desktop Obsidian behavior.

## Failure controls

Missing month exits 2; added crate file exits 2; unsupported ghgag diff on MOENV folders exits 2.
No fixture was rewritten to manufacture a passing comparison.

commands.json contains 33 real in-process CLI invocations and terminal exit receipts.
Copy the entire output directory, not only packages/, to preserve the monthly evidence chain.
manifest.json covers every output file except itself; retain its digest independently.
