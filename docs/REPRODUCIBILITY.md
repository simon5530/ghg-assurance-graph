# Reproducibility: primary MOENV 2023/2024 workflow

The primary documented run is `scripts/run_moenv_example.py`, not the old
regression runner. [Usage](USAGE.zh-TW.md) and [reference receipts](../examples/moenv_training/workflow/REPORT.md)
show the complete data → graph → validation → exports path.

```sh
uv sync --locked
uv run python scripts/run_moenv_example.py --out artifacts/moenv-worked
```

The output must not exist. Installation may use networking; the runner blocks
Python sockets/DNS before application imports (not an OS sandbox). No model or
credentials are needed. The recorded run uses Python 3.12.14 and the repository
uv.lock. `--python INSTALLED_PYTHON` runs with `-I` and no injected PYTHONPATH.

The run writes 33 actual CLI receipts with stdout/stderr hashes and exact exits,
120 monthly rows, 122 fictional source documents, annual gas calculations,
nine result explanations and nine unreviewed states. Literal/Fraction totals are
95797.473564 and 95229.409244 kgCO2e; all causes in the arithmetic difference
remain UNKNOWN. Legacy CarbonDiff is explicitly unsupported for these folders.
Both canonical crates verify; exported notes number127/140 with no broken links.
The full output, including external monthly documents, is needed for handoff.

`manifest.json` hashes every run file except itself. Two independent PYTHONHASHSEED
runs compare complete relative file/byte maps; do not replace this with a total-only
check. Source generation uses stable sorted Turtle. The committed workflow folder
is a selected reference subset with its own manifest, not the full output tree.

## Rendered reading artifacts

The PDF/HTML guide and primary manuscript examples use this same summary.
ReportLab (guide) and Matplotlib (figure) are authoring-only; they are not runtime
requirements. The manuscript HTML uses inline local SVG; optional local Chrome
prints its PDF. PDF metadata/browser output is not a cross-platform byte-replay
contract. Visual review and numeric/text extraction are separate checks.

## Separate legacy regression and historical releases

ExampleCo's 2025-v1/v2/2026-v1 and benchmark/ground_truth remain a software-regression
population, not the user or paper's primary MOENV example. Its independent runner
and tests retain their original arithmetic and declared semantic bounds. They do
not prove primary-case CarbonDiff support.

[Historical fresh-host release evidence](FRESH_RELEASE_REPRODUCTION.md) and
[source preservation](ARCHIVE_STATUS.md) identify earlier source/release objects,
not an immutable release of this updated working tree. No journal submission or
current-source DOI/archival identifier is claimed. CI receipts for the current
reconciliation are recorded in the results ledger and publication audit.
