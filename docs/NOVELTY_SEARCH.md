# Bounded novelty search log

Access dates: 2026-09-24 (prior report) and 2026-09-25 (completion review). Search results are discovery leads, not absence proofs or verified implementation claims. Primary-source matrix: [RELATED_WORK.md](RELATED_WORK.md).

| Source / exact query | Outcome and limitation |
|---|---|
| GitHub repository search, 2026-09-24: `carbon SHACL`, `emissions provenance`, `GHG restatement`, `carbon assurance graph` | Prior report records 0/9/0/0 metadata hits; not exhaustive code search. TEC, AutoMatCE and OpenDPP followed to primary sources. |
| Web, 2026-09-25: `"GHG provenance graph" "GHG assurance knowledge graph"` | No clear exact matches reported; ESGlass/KG4ESG preprints and IBM methodology surfaced. Unreviewed leads, not established equivalence. |
| Web: `"carbon inventory" SHACL "carbon evidence ontology"` | Provider error; no valid negative result. |
| Web restricted to arXiv: `site:arxiv.org carbon provenance emissions attribution` | Electricity/carbon-aware-computing attribution papers surfaced, not organizational version bridges; discovery only. |
| Web restricted to JOSS: `site:joss.theoj.org greenhouse gas provenance` | bonsai_ipcc, carbonr, Emiproc, dtrackr surfaced; search does not establish their full capabilities. |
| Web restricted to SoftwareX: `site:sciencedirect.com SoftwareX greenhouse gas provenance` | ChamberFlux, yProv4ML and SAMbA-RaP surfaced; discovery only. |
| Google Scholar: `GHG restatement change attribution` | Public results accessed; broad/noisy, including Widespread revisions of self-reported emissions by major US corporations (Nature Climate Change). No full-text result or algorithm claim adopted. |
| Scopus / Web of Science | No authenticated database search available or performed. No exhaustive or indexed-systematic-review claim. |
| yProv4DV / SoftwareX DOI | Crossref record, repository, arXiv abstract and accessible HTML inspected; see precedent record. |

## Material follow-up rather than search expansion
[TEC](https://tec-toolkit.github.io/) is direct carbon-provenance prior art. [CarbonLedger](https://github.com/jackson-marcus/Carbon-Ledger) is direct numerical factor-restatement prior art. [ESGlass](https://www.preprints.org/manuscript/202603.2187) and [KG4ESG](https://www.preprints.org/manuscript/202602.1970/v1) remain unreviewed preprint leads; [corporate emissions revisions](https://www.nature.com/articles/s41558-025-02494-9) is a problem/method lead, not evidence of an open-source full-combination tool.

Stop condition: enough overlap and uncertainty exist to select HOLD. Further search is not needed to justify stopping before implementation. A future GO requires focused primary-source/full-text and comparative-workflow evidence, not more zero-hit searches. Commercial/private products and non-English literature are not comprehensively covered.
