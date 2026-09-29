# Illustrated workbook

- [16-page PDF](GUIDE.pdf): printable, vector charts and actual output excerpts.
- [Editable standalone HTML](GUIDE.html): no external assets.
- [Full reference guide](../../examples/worked_example/README.md) and [sample report](../../examples/worked_example/sample/REPORT.md).
- [Figure data](figure-data.json) records totals, scopes and the complete run manifest digest.

From the repository root, after `uv sync --locked`:

```sh
uv run --locked python scripts/run_example.py --out artifacts/worked-example
uv run --locked python scripts/modify_example.py --out artifacts/electricity-exercise
uv run --locked ghgag validate artifacts/electricity-exercise
```

To regenerate the PDF/HTML, use a separate authoring environment with ReportLab 4.4.10 (MIT-compatible BSD license), then run:

```sh
python scripts/render_user_guide.py --run artifacts/worked-example
```

The renderer reads completed JSON and report artifacts, performs numeric assertions and rejects page overflow. No private data or hosted rendering service is used. PyMuPDF is optional local visual QA tooling, not a redistributed application dependency. All 16 pages were rendered and inspected; text bounds and extracted numeric values were checked. Desktop Obsidian behavior is explicitly unverified.

## Naming migration, 2026-09-29

Current fictional organization: **ExampleCo-GHG-001**. CompanyX is already used by a real cyber-insurance business; see the [KHIPU Networks announcement](https://www.khipu-networks.com/news/companyx-partnership/) dated 2025-08-14, checked 2026-09-29. An exact-label web search for the chosen identifier returned no results that day. This is not legal, trademark or global-availability clearance.

The former ACME fixture namespace and runner were renamed: use `scripts/run_example.py` and `examples/worked_example/`. No old namespace alias is emitted: mixing old and new identities would misrepresent continuity. Regenerate all dependent evidence, manifests, figures and exports. Old URLs into the source tree may require the historical commit; historical tags/releases and their hashes are untouched. This is a source/documentation update within 0.4.0a1, not a newly minted release. Schema 0.1.0, all 45 products, totals 3820/3850/4060 and deltas 30/210 are unchanged. Historical changelog/audit entries preserve their genuine former labels.
