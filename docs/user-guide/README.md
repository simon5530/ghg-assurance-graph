# Primary illustrated user guide — MOENV 2023/2024

- [14-page PDF](GUIDE.pdf), [editable standalone HTML](GUIDE.html).
- [Chinese operating instructions](../USAGE.zh-TW.md).
- [Collection/source mapping](../../examples/moenv_training/README.md).
- [Actual 33-command reference report](../../examples/moenv_training/workflow/REPORT.md).
- [Figure data](figure-data.json) binds both annual totals and all guide counts to the executed summary/manifest.

```sh
uv sync --locked
uv run python scripts/run_moenv_example.py --out artifacts/moenv-worked
```

The guide's primary case is 2023/2024, not the legacy ExampleCo regression.
It covers raw balances, collection checking, gas-to-CO2e projection, graph queries,
unreviewed results, arithmetic comparison, canonical packages, Markdown exports,
expected failure controls and safe handoff. Legacy CarbonDiff does not accept
these folders; no old benchmark score is presented as a MOENV observation.

Authoring only: a separate environment with ReportLab 4.4.10 (BSD) can run
`python scripts/render_user_guide.py --run artifacts/moenv-worked`.
The main software's locked dependencies do not include PDF authoring libraries.
All pages are rendered for visual review and checked for text overflow; charts
use saved real execution results, not application screenshots. Native Excel,
desktop Obsidian, source authentication and human assurance remain unverified.
