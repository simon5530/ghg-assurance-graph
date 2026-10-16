# Manuscript claim and source ledger

Bibliographic verification began 2026-09-28; primary-case reconciliation 2026-10-16. References cite primary sources, not model-generated bibliography. No invented DOI, author, affiliation or approval. Primary standards remain outside Git; company reports are not evaluation sources.

## Bibliography verification

1–3: official GHG Protocol editions and inspected chapter/page coverage are recorded in [standards alignment](../../docs/STANDARDS_ALIGNMENT.md), reviewed 2026-09-26. Corporate revised 2004, Scope 2 2015, Scope 3 2011 remain distinct; revisions/consultations are not adopted as final requirements. Scope 3 exact inspected PDF: https://ghgprotocol.org/sites/default/files/standards/Corporate-Value-Chain-Accounting-Reporing-Standard_041613_2.pdf .

4: W3C PROV-O official HTML retrieved with normal HTTPS on 2026-09-28; document header confirms Recommendation 30 April 2013. Initial web-fetch 403 was not evidence of unavailable content: system HTTPS retrieval succeeded without disabling verification.

5: W3C SHACL official HTML similarly retrieved 2026-09-28; header confirms Recommendation 20 July 2017. Cite this implemented Core standard, not an unverified later draft.

6: official RO-Crate 1.2 page retrieved 2026-09-28; identifies Metadata Specification 1.2, published 2025-06-04, Recommendation. The implemented closed directory profile is described in [evidence contract](../../docs/EVIDENCE.md); not a universal RO-Crate verifier.

7–8: primary website, repository docs and source-code snapshots inspected 2026-09-24, with exact commits and capability qualifiers in [related work](../../docs/RELATED_WORK.md). TEC provenance/validation and CarbonLedger factor-vintage restatement are prior art, not rerun comparator experiments.

9: official ISO metadata and bounded licensed-source review are recorded in standards alignment. ISO 14064-1:2018 second edition; inspection is not conformity. No licensed text redistributed.

Publisher guide/template verified independently for this draft: [journal check](JOURNAL_GUIDE_CHECK.md). Template SHA256 9fcf40ede96a2f188ee4ef77134e0596d01e1b65fd9db63f2874d29f2ecb916d (44,823 bytes).

## Current primary quantitative claims — 2026-10-16

| Claim | Executable source / oracle | Meaning |
|---|---|---|
| 2023/2024; 120 rows / 122 documents | moenv_example.py; test_moenv_example.py; workflow summary | Fictional internal collection, not real-company observations |
| 95797.473564 / 95229.409244 kgCO2e | Gas CSV, independent Fraction and literal oracles | Primary annual totals |
| 9 lineages, all unreviewed | Executed graph explain/query receipts; workflow tests | Explicit graph state, not human acceptance |
| 33 calls; 30 success / 3 exit2 controls | commands.json and referenced output hashes | Actual CLI parser invocations, not a performance metric |
| Two valid crates; 127/140 notes | Executed verification and link checks | Bounded integrity / export, not source authenticity |
| -568.064320 delta; all causes UNKNOWN | comparison.json and exact rational reconciliation | Arithmetic only; legacy CarbonDiff unsupported |

Reference10 is the [inspected MOENV file ledger](../../examples/moenv_training/official-sources.json)
and [source/parameter policy](../../examples/moenv_training/SOURCES.md). Five
2024/2026 official downloads were inspected and hashed15October2026; bytes remain
outside Git. Current editing reused that source evidence; no new legal conformity
or latest-factor determination is implied. Official coefficients, synthetic LHV,
historical electricity vintages and unquantified uncertainty remain separate.

## Separate regression evidence

The legacy ExampleCo benchmark's45lineages,10authoreddefects,nineassistedcomponents,
3820/3850/4060totals and +300/500UNKNOWN quantities are not observations from the
primary MOENV case. Bibliographic sources1–9 support definitions and prior-art
context, not measured comparative superiority. No listed-company dataset is used.

## Reproduction

- `uv sync --locked`; `uv run python scripts/run_moenv_example.py --out NEW_OUTPUT`.
- Open REPORT.md, commands.json, summary.json; [reference subset](../../examples/moenv_training/workflow/REPORT.md).
- Authoring-only: `python scripts/render_moenv_figures.py` with Matplotlib3.10.7;
  `python scripts/render_user_guide.py --run NEW_OUTPUT` with ReportLab4.4.10;
  `python scripts/render_manuscript.py --pdf` with a local Chrome.
- Primary figures/guide data bind to the same summary and manifest; regression
  SVG remains a separate source fixture, not the manuscript evaluation figure.

This is a working-source0.4.0a1alpha draft, not a minted release, DOI, practitioner
review, conformity claim or journal submission. Actual authors must review and
approve metadata and declarations; no approval is inferred from repository ownership.
