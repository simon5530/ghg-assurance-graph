# Manuscript claim and source ledger

Initial manuscript, 2026-09-28. References cite primary sources, not model-generated bibliography. No invented DOI, author, affiliation or approval. Primary standards remain outside Git; company reports are not evaluation sources.

## Bibliography verification

1–3: official GHG Protocol editions and inspected chapter/page coverage are recorded in [standards alignment](../../docs/STANDARDS_ALIGNMENT.md), reviewed 2026-09-26. Corporate revised 2004, Scope 2 2015, Scope 3 2011 remain distinct; revisions/consultations are not adopted as final requirements. Scope 3 exact inspected PDF: https://ghgprotocol.org/sites/default/files/standards/Corporate-Value-Chain-Accounting-Reporing-Standard_041613_2.pdf .

4: W3C PROV-O official HTML retrieved with normal HTTPS on 2026-09-28; document header confirms Recommendation 30 April 2013. Initial web-fetch 403 was not evidence of unavailable content: system HTTPS retrieval succeeded without disabling verification.

5: W3C SHACL official HTML similarly retrieved 2026-09-28; header confirms Recommendation 20 July 2017. Cite this implemented Core standard, not an unverified later draft.

6: official RO-Crate 1.2 page retrieved 2026-09-28; identifies Metadata Specification 1.2, published 2025-06-04, Recommendation. The implemented closed directory profile is described in [evidence contract](../../docs/EVIDENCE.md); not a universal RO-Crate verifier.

7–8: primary website, repository docs and source-code snapshots inspected 2026-09-24, with exact commits and capability qualifiers in [related work](../../docs/RELATED_WORK.md). TEC provenance/validation and CarbonLedger factor-vintage restatement are prior art, not rerun comparator experiments.

9: official ISO metadata and bounded licensed-source review are recorded in standards alignment. ISO 14064-1:2018 second edition; inspection is not conformity. No licensed text redistributed.

Publisher guide/template verified independently for this draft: [journal check](JOURNAL_GUIDE_CHECK.md). Template SHA256 9fcf40ede96a2f188ee4ef77134e0596d01e1b65fd9db63f2874d29f2ecb916d (44,823 bytes).

## Quantitative claim mapping

| Claim | Executable evidence | Meaning |
|---|---|---|
| 45/45 lineages | tests/test_graph.py | Stored relationships only |
| 10 TP, 0 FP/FN; 6/4 split | benchmark evaluator; expected_findings.json | Nonblind synthetic regression |
| Nine assisted components | tests/test_diff.py; expected_change_attribution.json | Seven supplied labels, two mechanical components |
| 3820/3850/4060; +30/+210 | Raw rows, evaluator, literal/Fraction oracle | Partial synthetic kgCO2e |
| +300 signed, 500 absolute UNKNOWN | Unassisted evaluator | Unsupported changes, not uncertainty intervals |

## Reproduction entry points

- uv sync --locked; uv run ghgag benchmark run; uv run pytest -q.
- Detailed workflow: scripts/run_acme_example.py (see --help).
- uv run python scripts/render_figures.py; uv run python scripts/render_manuscript.py --pdf.
- tests/test_figures.py checks generated SVG equality and manuscript scope/table contracts.
- Current version 0.4.0a1; immutable release and archival links pending.

## Review boundaries

Only fictional ACME data support this manuscript's evaluation. No current external
validation, real-company transfer, adoption, DOI, human approval or journal submission
is claimed. Historical v0.3 reproduction and archive records are not current evidence.
Bibliographic sources are prior verified records; this scope edit did not repeat
source retrieval or introduce new external research.
