# Real public-company facts and complete run outputs

**Not synthetic data. Not reconstructed inventories or assurance opinions.**

UMC was selected before source access by a fixed SHA256 seed over TSMC/UMC/Delta/ASE.
TSMC is a lightweight held-out transfer example. See [source mapping and limitations](../../docs/PUBLIC_COMPANY_SOURCES.md).

## Read full outputs
- [UMC Group report](full_run/umc/REPORT.md), [every command](full_run/umc/commands.json), [validation](full_run/umc/validation.json), [crate](full_run/umc/crate/manifest.json)
- [UMC parent-only report](full_run/umc-parent/REPORT.md)
- [TSMC held-out report](full_run/tsmc/REPORT.md), [every command](full_run/tsmc/commands.json), [validation](full_run/tsmc/validation.json), [crate](full_run/tsmc/crate/manifest.json)

Each directory includes all canonical facts, Turtle/JSON-LD, every explanation,
per-year inputs, differences, missing-evidence actions, verified RO-Crate and Obsidian
notes. INPUT/OUTPUT in command transcripts are portable placeholders. No PDF or
licensed standards text is included. These are generated observed outputs, not
test ground truth; independent numeric oracles live in tests/test_public_company_facts.py.

## Reproduce
```sh
uv sync --locked
uv run python scripts/run_public_case.py examples/public_companies/umc_group_2022_2024.json --out artifacts/public-umc
uv run python scripts/run_public_case.py examples/public_companies/umc_parent_2022_2024.json --out artifacts/public-umc-parent
uv run python scripts/run_public_case.py examples/public_companies/tsmc_heldout_2023_2024.json --out artifacts/public-tsmc
uv run pytest -q tests/test_public_company_facts.py
```
New output directories are required. The runner blocks Python socket connections
and DNS before loading the application. This is a reproducibility guard, not an
OS sandbox. Dependency installation is separate and may need network/cache.

## Results and limits
24 assertions: 7 UMC Group, 9 UMC parent-only, 8 TSMC. All three runs are structurally
accepted, package-valid and **not_assessable** overall. Required upstream calculation
lineage is unavailable for all 24. No invented factor, activity or review fills it.
The 33 assessed checks include three schema checks and 30 metadata declarations,
not independently verified emissions checks; 144 checks remain not assessable.

Historical figures are from the 2024 report vintage, not separate vintage reports
or the latest available disclosure. UMC Scope 2 basis is unspecified. TSMC LB/MB
are separate. Scope/boundary differences and absent restatement/rounding prevent
unqualified comparisons. All causal drivers remain UNKNOWN.

## Rights
Code, original mapping and reports are project-authored MIT material. Company
reports remain their respective owners’ copyrighted works; this repository does
not relicense them. Only limited numeric facts with attribution are reproduced.
Names identify sources and imply no endorsement. Raw report redistribution is not authorized.
