# SoftwareX precedent: yProv4DV

Accessed 2026-09-25.

- Published title: **yProv4DV: Filling the visualization gap in reproducible research workflows**.
- Journal: SoftwareX, volume 35, 2026, article 102821.
- DOI: [10.1016/j.softx.2026.102821](https://doi.org/10.1016/j.softx.2026.102821); [publisher-deposited Crossref metadata](https://api.crossref.org/works/10.1016/j.softx.2026.102821) independently read, not inferred from a badge.
- [Repository](https://github.com/HPCI-Lab/yProv4DV), [preprint abstract](https://arxiv.org/abs/2603.20437), [preprint HTML](https://arxiv.org/html/2603.20437v1). The preprint title is *Reproducible Data Visualization Scripts Out of the Box*, submitted 2026-03-20. Do not conflate its title/date or evaluation text with the final publisher version, which was not retrieved.

## Observed contribution and example
Repository documentation and accessible preprint describe a lightweight Python instrumentation layer collecting visualization source, inputs, outputs and execution context, creating W3C PROV records and RO-Crate archives. Standard file operations and selected scientific-library reads are tracked; unsupported inputs may need manual registration. File-size exclusions and subsets make capture completeness an explicit configuration concern. These are documented capabilities, not results rerun by this project.

The inspected preprint illustrates architecture, start/log/end directives, a Python visualization script, and an RO-Crate descriptor connecting CSV inputs, a PNG output, source and requirements. Evaluation evidence inspected here is demonstrative artifact/workflow evidence. No comparative performance result or numerical speedup is adopted; no code was installed or executed. The final paper’s complete evaluation needs review before using it as an evaluation template.

## Lessons and limits
A narrow workflow gap and low-friction integration can motivate a software contribution without inventing a new provenance standard. Show one complete reproducible case with concrete artifacts and limitations, not a decorative graph. Reuse PROV/RO-Crate; do not claim their combination is new. For GHG assurance this precedent does not replace seeded-defect precision/recall, multi-driver attribution reconciliation, or domain review. It is not a corporate GHG assurance engine and does not establish that our remaining gap is publishable.

Other search leads (not primary-reviewed precedents): yProv4ML and SAMbA-RaP; see [search log](NOVELTY_SEARCH.md). No fabricated DOI or evaluation is assigned to them.
