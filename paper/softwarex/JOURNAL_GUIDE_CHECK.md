# Official SoftwareX guide and template check

Accessed 2026-09-28. Supersedes the earlier access-blocked planning assumption, not submission readiness.

- Official guide: https://www.sciencedirect.com/journal/softwarex/publish/guide-for-authors
- Direct web fetch returned 403. Ordinary managed-browser navigation succeeded without login or challenge bypass; journal-specific instructions and submission checklist were read.
- Official linked Word template: https://legacyfileshare.elsevier.com/promis_misc/softwarex-osp-template.docx
- Normal verified HTTPS download succeeded; DOCX ZIP/XML inspected locally. Identifies **Version 6 (March 2026)**. Third-party template bytes are not redistributed.

## Verified requirements

Current limit: **4,000 words**, not the specification's older approximately 3,000 assumption. Excludes title, authors, affiliations, references and metadata tables; includes abstract, running text, captions and footnotes. Maximum **six figures**. Template asks for about 100 abstract words, maximum six keywords and five main sections: motivation/significance, software description, illustrative examples, impact, conclusions. Generic guide permits a 250-word abstract and 1–7 keywords; draft follows stricter template preference (about 100; six keywords).

Template suggests maximum six main-text pages excluding metadata/tables/figures/references, prioritizing word limit. Reading PDF is not in official layout; total page count is not a submission-format claim.

C1–C8 are in MANUSCRIPT.md. C8 requests a support email, not merely issues URL. Author identities, affiliations, addresses, corresponding-author contact and consent remain owner items. Guide specifies README.md and LICENSE.txt, while template says Licence.txt; repository has LICENSE. Resolve filename expectation during publication preparation without inventing a license.

Official Word or LaTeX template is mandatory; Word figures must be embedded. Editable sources are required: generated PDF is a reading copy only. References use sequential bracketed numbers. Highlights are encouraged: 3–5 bullets, at most 85 characters each. Research-data deposit/citation and availability statement are required (Option C); assess archival deposit beyond GitHub. No DOI invented.

Guide requires AI disclosure and human accountability, permits explanatory diagrams and reproducible visualizations with disclosure, and prohibits fabricated observational imagery. Captions disclose AI-assisted deterministic code. Funding, conflicts and CRediT require human confirmation. APC/waiver eligibility and payment are not verified or authorized.

## Rendering

Run: python scripts/render_manuscript.py --pdf with existing local Chrome/Chromium. HTML/SVG use Python standard library only; no paid service or installation. No references fetched; Chrome background networking/DNS disabled. MANUSCRIPT_METRICS.json conservatively counts table/code/declaration text too.

Before submission transfer human-reviewed content into current official template without altering format. Unknown human declarations remain pending, not fabricated. Guide retrieval does not supply human review, impact or submission approval. Current-release hosted reproduction and archival links remain pending; historical v0.3 records are not carried forward.


## Observed render verification

Local Chrome produced a complete PDF but lingered during shutdown. Renderer now
uses a fresh staging destination, kills/reaps its own timed-out process, and accepts
only a newly generated PDF with header and EOF markers; never a stale prior PDF.
Current PDF verification is recorded in RESULTS_LEDGER.md; historical PDF byte/page counts do not apply to this revision. HTML/PDF are reading copies.
