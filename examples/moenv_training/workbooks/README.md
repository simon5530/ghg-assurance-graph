# Collection workbooks

Three XLSX files are original collection views, not official MOENV filing files.
Each contains Overview, eleven mapped collection tables and two provenance extensions.
The blank template has no invented factors or calculated totals. Filled examples
are formula-linked, but assume fixed five-source/month blocks; do not reorder rows.
Monthly edits do not update CSV, source evidence or hashes automatically.

[Formula mutation receipts](formula-checks.json) cover both years: changing one
boiler month by 10 m³ changes the annual total by 21.33871 kgCO2e; blanking it
exposes MISSING. All 42 sheets were rendered for visual review. This used the
artifact-tool calculation engine, not native Microsoft Excel; no native Excel
execution or automatic source-authentication claim is made.

The optional [XLSX renderer](../../../scripts/render_moenv_workbooks.mjs) reads
committed CSV via Python's standard CSV parser and uses `@oai/artifact-tool`.
It is authoring tooling, not a runtime dependency or requirement to validate the
CSV/graph case. In an authoring environment providing that package, run
`node scripts/render_moenv_workbooks.mjs`; set `GHG_PREVIEW_DIR` to a new local
preview directory for rendered sheets and mutation receipts. PDF/ODF official
sources are not embedded or redistributed. Numeric source IDs resolve through
[the source ledger](../SOURCES.md) and [download hashes](../official-sources.json).
