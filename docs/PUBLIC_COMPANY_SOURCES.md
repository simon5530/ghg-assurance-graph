# Public-company reported-disclosure evidence

Retrieved 2026-09-28. These are public **reported assertions**, not reconstructed inventories, assurance conclusions, or invented activities/factors. Raw original PDFs and extraction/rendering artifacts remain outside Git in a local temporary source directory. Only small attributable numerical facts and original research notes are distributed.

## Precommitted selection

Candidates in order: TSMC, UMC, Delta, ASE. UTF-8 seed `2026-09-28-ghgag-public-company-v1`; SHA256 `570d0d908b7db57fd461b0ca03a4d4e737a9a73288b56d60b3cb71ed3a5c7e01`. Integer digest modulo four = 1, selecting **UMC**. Selection was retained despite initial access failures. TSMC is a lightweight held-out transfer example, not a blinded or representative benchmark. See selection.json.

## Exact official sources

- [UMC 2024 Sustainability Report, English](https://www.umc.com/upload/media/07_Sustainability/72_Reports_and_Results/1_Corporate_Sustainability_Reports/CSR_Reports/CS_Report_English_pdf/2024_CSR_report_eng/UMC-2024-EN-elink.pdf). SHA256: d66619bea5b4ca327ef128c7d31adb8559386a328ee974657ad28129698a8b4d. Publication July 2025 (p.4); report year 2024. Official discovery: https://www.umc.com/en/Download/corporate_sustainability_reports.
- [TSMC 2024 Sustainability Report, English](https://esg.tsmc.com/file/public/2024-TSMC-Sustainability-Report-e.pdf). SHA256: 68c093548001a5b90222997590089fac3378bc3611dff63d65b4460e36e6ff41. P.253 plans publication August 2025; actual publication date not independently established. Official discovery: https://esg.tsmc.com/en-US/ESG-data-hub/reports-and-documents.

Hashes identify exact inspected PDF bytes, not publisher authenticity or future URL contents. PDF page numbers equal printed page numbers for the cited tables. Both reports contain several historical years; these are **2024-report-vintage** values, not separate annual-vintage comparisons. Later reports were visible in catalogues, but this bounded case study uses the 2024 vintage; no claim to latest inventory data.

## Extracted values (tCO2e)

UMC Group, p.99, charts headed Direct GHG Emissions / Indirect GHG Emissions from Purchased Energy:

| Year | Scope 1 | Scope 2 (basis unspecified) |
|---|---:|---:|
| 2022 | 865,984 | 1,757,833 |
| 2023 | 509,555 | 1,636,208 |
| 2024 | 463,670 | 1,523,855 |

UMC 2024 Scope 3 aggregate: **1,713,507**, p.100, Total Amount. Its boundary is UMC and all subsidiaries, not the narrower Scope 1/2 disclosure. Earlier group Scope 3 totals were not selected because they were not found in the inspected group table.

UMC **parent-only** supplementary series, p.209, Appendix 7 ESG Data Summary explicitly headed Scope: UMC:

| Year | Scope 1 | Scope 2 (basis unspecified) | Scope 3 |
|---|---:|---:|---:|
| 2022 | 591,781 | 1,373,914 | 2,064,284 |
| 2023 | 356,911 | 1,376,960 | 1,893,167 |
| 2024 | 287,393 | 1,334,802 | 1,416,926 |

These are separate fixtures: parent and group values must **never be added** or treated as interchangeable.

TSMC held-out, p.266, ESG Performance Summary / Climate and Energy:

| Year | Scope 1 | Scope 2 market-based | Scope 2 location-based | Scope 3 |
|---|---:|---:|---:|---:|
| 2023 | 1,596,031 | 10,187,387 | 11,466,118 | 7,616,655 |
| 2024 | 1,825,872 | 10,957,397 | 12,674,921 | 8,223,173 |

## Boundaries, methods, limitations

**UMC:** pp.4/99 describe operational control, Taiwan and Singapore fabs and foundry subsidiaries HJ, USCXM, Wavetek, USJC. Other non-foundry subsidiaries are excluded from Scope 1/2 disclosure under the report's less-than-5% emissions materiality criterion; this is a company choice, not a project assurance rule. P.99 cites IPCC AR5 (2014) for direct emissions; p.100 cites AR5 for Scope 3. Prior-year continuity was not independently established. Scope 2 has no explicit LB/MB label in the inspected report: retained as unspecified, despite grid-factor and renewable-electricity discussions. No fabricated LB alternative or MB inference. P.100 Scope 3 refers to GHG Protocol value-chain guidance and ISO14064-1:2018 and factors from Taiwan environmental authorities, suppliers and SimaPro; no source activities or factors are reconstructed.

**TSMC:** p.115 note 1 says parent and all subsidiaries for Scopes 1/2; note 2 specifies business-control approach, AR5 GWP100 and the 2019 Refinement to 2006 IPCC Guidelines for 2020-2024 Scope 1. P.260 note 3 lists 2024 boundary additions (Fab20 Phase1, Advanced Backend Fab6 Phase2, Taichung Zero Waste Manufacturing Center, Japan 3DIC R&D Center), preventing an unqualified like-for-like trend claim. **Scope 3 boundary conflict remains unresolved:** p.266 note6 lists Taiwan, Washington, China, Nanjing, VisEra; p.115 note3 additionally names JASM and Japan 3DIC R&D Center and Taiwan R&D/Zero Waste centers. Values are preserved, not silently corrected. Pp.113-114 discuss carbon-neutral natural gas; gross/net treatment is not independently reconciled. Disclosed offsets are not deducted by this dataset. LB/MB are alternative accounting results, never additive.

**Restatement and rounding:** no row-specific restatement status or explicit rounding increment was identified for these selected series. JSON retains null, not a claim that no restatement occurred. Displayed integer values are exact transcriptions, not proof of measurement precision. Missing metadata must lead to not-assessable checks, not fabricated defaults. No between-company performance ranking is justified by these fixtures.

## Assurance evidence is not this project's assurance

UMC p.208 describes 2023/2024 parent/subsidiary inventory verification, DNV/SGS providers, ISO14064-3 reasonable assurance and unmodified opinions. Pp.212-213 contain report-level SGS assurance (signed June25,2025). P.214's DNV TCFD engagement expressly excludes Scope1/2/3 because covered by a separate engagement. Do not cite TCFD assurance as direct emissions verification. A suspicious p.208 column labelled Scope3 numerically equals Scope1+2; it was deliberately **not** used as a Scope3 source (p.100/209 used instead).

TSMC p.260 lists reasonable assurance for parent/most subsidiaries, while Washington's 2023 row is limited (2024 reasonable). P.276's report-level DNV limited assurance excludes fresh GHG verification and references separate verification C736454-2024-AG-TWN-DNV (May13,2025); it is signed June27,2025 and states verification used the Chinese report. Those statements do not constitute an independent review by this project.

## Verification and reproducibility

1. Retain source bytes locally and run SHA256 before interpreting any download; HTML error pages are not PDF evidence.
2. Manually transcribe exact numeric table values and compare with rendered source pages (UMC99/209; TSMC266); textual extraction alone can scramble chart order.
3. All three assertion JSON files were loaded successfully using the reported-disclosure/1 implementation: 7 group, 9 parent-only and 8 held-out assertions. Schema checks passed; validation appropriately returned not_assessable for incomplete metadata, not assurance. selection.json and source_manifest.json are metadata, not disclosure inputs.
4. Repeat retrieval only when needed; compare hashes before reusing page citations. No copyrighted report prose or full report is committed.

Access observations: configured web search returned provider_error; initial guessed old paths returned 403/404. Official catalogue navigation in the managed browser revealed working URLs. UMC direct PDF download succeeded. TSMC command-line retrieval returned403 while normal browser fetch returned200; original bytes were downloaded through the browser and copied to the local raw directory. No login, paywall bypass, credential handling, or unresolved source-access blocker was required. Remaining blockers are interpretive comparability limitations above.
