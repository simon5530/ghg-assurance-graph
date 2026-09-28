# Manuscript claim and source ledger

Initial manuscript, 2026-09-28. References cite primary sources, not model-generated bibliography. No invented DOI, author, affiliation or approval. Primary standards and company reports remain outside Git.

## Bibliography verification

1–3: official GHG Protocol editions and inspected chapter/page coverage are recorded in [standards alignment](../../docs/STANDARDS_ALIGNMENT.md), reviewed 2026-09-26. Corporate revised 2004, Scope 2 2015, Scope 3 2011 remain distinct; revisions/consultations are not adopted as final requirements. Scope 3 exact inspected PDF: https://ghgprotocol.org/sites/default/files/standards/Corporate-Value-Chain-Accounting-Reporing-Standard_041613_2.pdf .

4: W3C PROV-O official HTML retrieved with normal HTTPS on 2026-09-28; document header confirms Recommendation 30 April 2013. Initial web-fetch 403 was not evidence of unavailable content: system HTTPS retrieval succeeded without disabling verification.

5: W3C SHACL official HTML similarly retrieved 2026-09-28; header confirms Recommendation 20 July 2017. Cite this implemented Core standard, not an unverified later draft.

6: official RO-Crate 1.2 page retrieved 2026-09-28; identifies Metadata Specification 1.2, published 2025-06-04, Recommendation. The implemented closed directory profile is described in [evidence contract](../../docs/EVIDENCE.md); not a universal RO-Crate verifier.

7–8: primary website, repository docs and source-code snapshots inspected 2026-09-24, with exact commits and capability qualifiers in [related work](../../docs/RELATED_WORK.md). TEC provenance/validation and CarbonLedger factor-vintage restatement are prior art, not rerun comparator experiments.

9–10: official report bytes, rendered-page transcription checks and original fact extraction recorded in [public sources](../../docs/PUBLIC_COMPANY_SOURCES.md). UMC SHA256 d66619bea5b4ca327ef128c7d31adb8559386a328ee974657ad28129698a8b4d; TSMC SHA256 68c093548001a5b90222997590089fac3378bc3611dff63d65b4460e36e6ff41. UMC July 2025 publication; TSMC actual publication date not established. 2024-report historical series, not latest reports or annual-vintage restatements. No source PDFs redistributed.

11: official ISO metadata and bounded private licensed-source inspection are recorded in standards alignment. ISO 14064-1:2018 second edition, not 2024 edition. Clause inspection is not conformity; no licensed content or local access identifiers reproduced.

Publisher guide/template verified independently for this draft: [journal check](JOURNAL_GUIDE_CHECK.md). Template SHA256 9fcf40ede96a2f188ee4ef77134e0596d01e1b65fd9db63f2874d29f2ecb916d (44,823 bytes).

## Quantitative claim mapping

| Claim | Executable/source evidence | Meaning |
|---|---|---|
| 448 tests, 11 warnings | Full pytest rerun 2026-09-28, 16.10 s | Engineering regression only |
| 45/45 lineages | tests/test_graph.py; three ACME snapshots | Asserted relationships resolve |
| 10 TP, 0 FP/FN; 6/4 split | ghgag benchmark run rerun; expected_findings.json | Nonblind public fixture checks |
| Nine assisted components | expected_change_attribution.json; tests/test_diff.py in passing full suite | Seven supplied semantic labels, two mechanical components |
| 3820/3850/4060; +30/+210 | Benchmark evaluator rerun; independent Fraction/literal test oracles | Partial synthetic kgCO2e |
| +300 signed, 500 absolute UNKNOWN | Unassisted evaluator rerun | Unsupported delta exposure, not statistical uncertainty |
| 24 assertions; 33 assessed; 144 not assessable | Three committed full_run/*/summary.json inspected | Presence/schema checks, not truth checks |
| 207 outputs | Recursive file count of examples/public_companies/full_run | Artifact count, not sample size |
| All public statuses not_assessable; all causes UNKNOWN | Three summaries and diff contracts | No upstream reconstruction or causal inference |
| UMC/TSMC deltas | Public source table; committed differences; tests/test_public_company_facts.py | tCO2e, independent series only |

UMC Group checks: 12 assessed / 41 not assessable. Parent: 10 / 57. TSMC: 11 / 46. All packages internally valid. Schema accounts for 3 of 33 assessed checks; other 30 are metadata-presence declarations. Upstream recalculation 0/24.

## Reproduction entry points

- ACME: uv sync --locked; uv run ghgag benchmark run; uv run pytest -q.
- Public cases: all three explicit commands in [public example README](../../examples/public_companies/README.md); new output directories required.
- Figure 1 + reading HTML/PDF: python scripts/render_manuscript.py --pdf.
- Figure 2: python scripts/render_figures.py; existing byte-equality test verifies its source-driven regeneration.
- Frozen code: b0de4b8a9373eee24d631cad14265e37bffcc75d, v0.3.0a1. Manuscript is a later working-tree content draft, not part of that frozen release.

## Review boundaries

No human domain sign-off, independent external adoption, DOI, submission, fee approval or causal accuracy inferred. Fresh hosted-runner source/wheel reproduction is observed in run 36382755169; source preservation resolves the released tag in Software Heritage (see docs/FRESH_RELEASE_REPRODUCTION.md and docs/ARCHIVE_STATUS.md). Bibliography uses corporate/group sources when appropriate and does not fabricate individual authors. Final journal style and author-approved source interpretation remain review work.
