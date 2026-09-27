# Standards alignment — bounded evidence, not certification

GHG Protocol review: 2026-09-26. Private ISO source review: 2026-09-28.
This synthetic partial benchmark is not a conforming corporate
report, verification engagement, regulatory filing, or production factor database.
No licensed ISO text or GHG standards PDFs are redistributed. Requirements below are
paraphrases; implementation restrictions are explicitly distinguished from standards.

## Authoritative sources and status

- **C:** [Corporate Standard, revised 2004](https://ghgprotocol.org/sites/default/files/standards/ghg-protocol-revised.pdf).
  Inspected chapters 3 (printed pp.16–18), 4 (p.25), 5 (pp.35–39), 7
  (pp.50–56), 9 (pp.63–64) using PDF inspection. The
  [current official landing page](https://ghgprotocol.org/corporate-standard)
  identifies seven gases including NF3; the older PDF's six-gas wording is not a
  current seven-gas completeness exemption.
- **S2:** [Scope 2 Guidance, 2015](https://ghgprotocol.org/sites/default/files/2023-03/Scope%202%20Guidance.pdf).
  Inspected §§6.2, 6.5, 6.11, Table 6.3 (pp.43–48,54–56), §§7.1,7.4,7.5,
  Table 7.1 (pp.59–65). [Landing page](https://ghgprotocol.org/scope-2-guidance)
  confirms eight quality criteria and consultation closed 2026-01-31.
- **S3:** [Corporate Value Chain (Scope 3) Standard, 2011](https://ghgprotocol.org/sites/default/files/standards/Corporate-Value-Chain-Accounting-Reporing-Standard_041613_2.pdf).
  Inspected Table 5.4 (pp.36–39), §§6.1–6.3 (pp.61–62), §7.3/Table 7.6
  (pp.77–78), §§8.2–8.3/Table 8.1 (pp.90–93), §§9.1,9.3 (pp.102,106–108),
  §11.1 (p.121), printed edition rather than e-reader pagination.
- **T3:** [Technical Guidance for Calculating Scope 3 Emissions, 2013](https://ghgprotocol.org/sites/default/files/2023-03/Scope3_Calculation_Guidance_0%5B1%5D.pdf).
  Inspected category 1 (pp.24–25,33), 2 (pp.36–37), 4 (pp.52,57,68), 5
  (pp.72,74,77–78), 6 (pp.81–83), 7 (pp.88–90). Companion guidance, not a
  replacement for S3. [Official introduction](https://ghgprotocol.org/scope-3-calculation-guidance-2).
- **ISO:** [ISO 14064-1:2018 official metadata](https://www.iso.org/standard/66453.html),
  edition 2, December 2018, confirmed 2024 (not a 2024 edition). The earlier
  public-preview access gap was resolved by private inspection of a supplied
  licensed copy identifying itself as **ISO 14064-1:2018(E)**, second edition,
  2018-12. Its cover, foreword and internal identifiers consistently identify the
  English Part 1, not Parts 2/3 or a Chinese translation. No translation authority
  or national adoption is inferred. Source identity is internally consistent, but
  publisher authenticity and license entitlement were not independently audited.
  The image-only copy was processed with local OCR, without external upload;
  no standards text, page images or license metadata are included here. Inspected
  clause references and remaining access/interpretation limits appear below.
  **Clause inspection is not clause conformity or professional assurance.**
- **Revision status:** [Official July 29, 2026 FAQ](https://ghgprotocol.org/blog/ghg-protocol-announces-key-standard-development-updates-faq-resource),
  inspected questions 1–3: joint GHG Protocol/ISO consolidated corporate standard
  planned consultation Q2 2027, publication Q4 2028. These plans and 2025/2026
  consultation proposals are **not final replacement accounting requirements**.

For the earlier GHG Protocol review, PDF-tool page filtering proved incomplete;
full-document inspection was used for those substantive sources. Source inspection is evidence, not independent
professional interpretation; no verbatim standards passages are shipped.

## Requirement → implementation → test → evidence status

| Topic / source | Bounded implementation and test evidence | Status / limitation |
|---|---|---|
| Organizational consolidation C ch.3 | Canonical BoundaryDefinition names operational/financial control/equity share; ACME explicitly 100% operational control of 3 sites. Package integrity + clean oracle test | Only operational-control scenario exercised; no inferred equity percentages |
| Operational boundaries C ch.4; S3 Table5.4 | Scope/category/source fields; category coverage below and benchmark assumptions; category coverage test | Selected sources, not complete Scope1/2/3; no cross-company comparability claim |
| ISO direct vs indirect: ISO §5.2.4; Annex B (informative) | Six ISO categories remain separate from GHG scopes and the fifteen Scope3 categories. Scenario-specific correspondence is documented below | Source-inspected interpretation only; no ISO-category field, automatic crosswalk or ISO aggregation is implemented |
| Dual Scope2 S2 §§7.1,7.4 | Location-only partial output; market-based request rejects; test_no_gas_or_market_or_netting_fallback and missing-contract case | Not a complete dual report. Never add LB + MB; no invented contractual eligibility |
| Instrument quality S2 Table7.1 | Need emission-rate attribute, exclusive claims, tracking/retirement, vintage, market match; supplier/direct-contract provisions as applicable, residual-mix information and absence disclosure. No eligible instrument provided, so benchmark refuses MB | Standard's evidenced data hierarchy/fallback is not prohibited; this benchmark declines to manufacture missing evidence or silently use zero/grid proxy |
| Units/provenance C ch.7; S3 ch.7; T3 | Every row has evidence, factor year/geography/unit/basis, quality/uncertainty; schema + independent Fraction calculations; missing source/year/unit failures | Factors are invented, nonofficial, never production defaults. Same-year restriction is fixture policy, NOT a universal factor expiry rule |
| CO2e vs gases C ch.9/current gas list | Only precharacterized kgCO2e factors; factor GWP basis recorded and never multiplied again. GWP scenario replaces synthetic characterization factor; double-GWP and gas-factor rejection tests | No gas-resolved seven-gas reporting implemented. Synthetic A/B are NOT IPCC values; this limitation prevents full compliance claims |
| Biogenic/removals/offsets C pp.25,63–64 | Separate stream values rejected by inventory arithmetic, not netted. No biomass or removals in ACME scenario; test rejects each separate stream | Direct biogenic CO2 must be separate; non-CO2 biomass gases are not thereby excluded from scopes. No removal/offset quantification implementation |
| PCF and EEIO T3 cat1 | Explicit cradle-to-gate boundary, declared kg versus USD; same nominal year/currency, no currency conversion; unsupported PCF fails | Supplier data can contain upstream allocation; supplier-specific does NOT universally mean allocation-free |
| Capital/transport/waste/travel T3 cat2,4–7 | Capital acquired-year emissions not amortized; tonne-km freight, total passenger-km encoded as km with declared passenger interpretation; waste treatment, travel/commuting selected source boundaries | No generic distance-factor equivalence; no recycling credit or telework model |
| Allocation S3 ch.8 | Explicit mass/economic fractions, once only; independent positive allocation test | Method transition is a measurement change, not physical reduction; causal appropriateness requires domain review |
| Base-year C ch.5; S3 ch.9 | Policy in benchmark README: 2025 base year; 0.5% cumulative absolute eligible-change threshold is PROJECT choice, not mandated %. Voluntary restatement of identified corrections; pending harmonization for later method/GWP change | 2026-v1 explicitly not like-for-like performance baseline; organic new source not acquisition; no production recalculation engine |
| Traceability/quality C ch.7; S3 ch.7 | Activity→evidence/quality and result→run→factor/method/GWP/boundary/review resolvable; uncertainty explicitly unquantified | Synthetic acceptance is not human assurance. Hash = integrity hint, not source authenticity |

## ISO 14064-1:2018 — inspected references and actual coverage

References below use **printed standard pages**, not PDF viewer offsets. The review
covered §1 (p.1), §§4–10 (pp.7–16), Annex A (pp.17–18), Annex B (pp.19–24),
Annex C (pp.25–31), Annex D (p.32), Annex E (pp.33–34), the narrative/report
organization guidance in Annex F (pp.35,37), and Annex H (pp.44–45). Annexes
**D and E are normative**; A, B, C, F, G and H are informative. Informative
examples are not additional mandatory rules. Annex G agricultural/forestry
methods (pp.38–43) were not substantively assessed for this industrial fixture.
The dense illustrative table in Figure F.1 (p.36) was not reliably recoverable
through OCR and is not used as an implementation oracle. OCR can introduce
character and layout errors; this is a source-based engineering assessment, not
an authenticated transcription or an exhaustive professional interpretation.

The baseline standards review inspected the canonical model, fixed ACME benchmark
and lineage/query layer: [models](../src/ghg_assurance_graph/models.py),
[benchmark code](../src/ghg_assurance_graph/benchmark.py),
[scenario assumptions](../benchmark/README.md), and
[graph layer](../src/ghg_assurance_graph/graph.py). The subsequent engineering review
also credits selected [SHACL/raw validation](../src/ghg_assurance_graph/validation.py),
[CarbonDiff](../src/ghg_assurance_graph/diff.py) and
[portable evidence](../src/ghg_assurance_graph/evidence.py), with executable tests
in test_validation.py, test_diff.py and test_evidence.py. These extend checks,
reconciliation and integrity portability, not the normative scope of conformity.

| Inspected ISO reference | Relevant implementation / executable evidence | Coverage and residual gap |
|---|---|---|
| §§4.2–4.6; §§5.1,5.2.1; Annex A | Organization, Facility, BoundaryDefinition and InventoryVersion retain the declared consolidation context; package validation checks matching organizations/boundaries. Contract tests: test_cross_record_context; benchmark: test_clean_independent_oracle | Supports explicit context and reproducibility. Does not prove completeness, ownership/control, equity percentages or real-world accuracy. Only the declared operational-control scenario is exercised |
| §§5.2.3,6.1; Annex H §§H.2–H.5 | Fifteen-category GHG Protocol screening below; selected source IDs and exclusions in benchmark README. test_screening_and_supplier_mix checks the presence of category rows, not the adequacy of a significance decision | No documented ISO-specific significance criteria, evaluation records or completeness engine. Missing data is not by itself a sound conclusion of insignificance; material omitted sources remain a limitation |
| §5.2.4; Annex B §§B.2–B.7 | EmissionSource stores GHG scope/category and Scope2 basis. test_scope_subtotals checks those GHG groupings. Interpretive ISO correspondence below | No ISO classification field or six-category aggregation/test. GHG Scope3 category numbers must never be interpreted as ISO category numbers |
| §§6.2.1–6.2.3,6.3; Annex C §§C.2–C.6 | EvidenceArtifact, ActivityRecord, EmissionFactor, CalculationMethod and CalculationRun preserve inputs and calculation context. test_clean_independent_oracle uses literal expected values and Fraction arithmetic; test_conversion_and_allocation_once and test_unverified_fields_reject exercise bounded failures | Supports auditable synthetic arithmetic, not validated physical models, site measurements, calibrated equipment, representative factors or production data selection. Factor-period coverage and same-year fixture checks are project restrictions, not universal ISO expiry rules |
| §§5.2.2,6.3,9.3.1 | GWPSet records basis/horizon; explicit CO2e units; double-characterization and unverified gas factors fail in benchmark tests | ISO expects direct results distinguished by gas/group and appropriate GWP use, with a 100-year reporting basis; §6.3 recognizes GWP may already be embedded in factors. This model only carries precharacterized totals and invented A/B bases. It cannot produce the required gas-resolved inventory or substantiate an IPCC basis; conversion of kg to tonnes alone does not close this gap |
| §§5.2.4,6.3; normative Annex D | test_no_gas_or_market_or_netting_fallback rejects unsupported biogenic/removal streams; scenario explicitly contains none | Refusal is an honest scope boundary, not implementation of biogenic accounting. Separate anthropogenic biogenic CO2 treatment does not exclude biogenic CH4/N2O from relevant anthropogenic emissions. Natural biogenic treatment and removal quantification are unimplemented |
| §6.3; normative Annex E §§E.1–E.3; §9.3.3 | Purchased electricity has a declared location-based result; absent contractual evidence causes market-based rejection; test_no_empty_or_dual_sum. No export scenario | Annex E requires location-based imported-consumption accounting; market-based information is an additional option subject to instrument conditions, not a blanket ISO dual-reporting requirement. Synthetic grid factors do not prove grid representativeness. Annex E prefers reporting-year grid data if available, otherwise recent data. Lifecycle/loss components need separate disclosure. Exported generation is not a deduction from direct emissions; no such export control is implemented here |
| §§6.4.1–6.4.2; §9.3.1 | 2025 base year, explicit +30 restatement, change categories and non-comparability warning. test_crossperiod_reconciliation and test_activity_first_convention | CarbonDiff now checks stable identities, classification, bounded exact arithmetic,
unsupported semantic changes and independent reconciliation (test_diff.py).
Reconciles fixture deltas; not a general review/recalculation procedure. The 0.5% threshold and activity-first decomposition are project policy. Substantial methodology/factor/error/structural changes require review; ordinary production changes are not a base-year recalculation basis. Later GWP/method/allocation changes are not harmonized |
| §§8.1–8.2; Annex C §§C.3,C.4.6 | Immutable revision identities, content digests, resolvable typed references and result lineage. test_immutable_and_digest; test_revision_chain_and_missing_predecessor; test_all_45_lineages_and_queries | RO-Crate exports additionally verify a closed file set, canonical payloads, hashes
and typed provenance (test_evidence.py). Useful information-management components,
not an organizational control system. No demonstrated responsibilities/training, calibration, internal audit, archive/retention procedure or evidence authenticity. A checksum is not a signature or independent validation |
| §8.3; §9.3.1; Annex C §C.7 | DataQualityAssessment has rating/rationale/uncertainty text; fixture explicitly discloses unquantified uncertainty | No category-level uncertainty assessment or justified qualitative substitute. A text field saying “unknown” or “not statistically quantified” does not satisfy the assessment obligation. Exact test arithmetic is not measurement certainty |
| §§7.1–7.3,9.3.3 | No reduction/target claim; offset-netting fixture rejects. Changes reconcile without being described as uniquely causal reductions | No mitigation initiative, project-credit or target reporting implementation. Carbon credits are not inventory deductions; rejection of all removal arithmetic is only this benchmark's limitation, not a claim that ISO universally prohibits emission/removal aggregation |
| §§9.1–9.3,10; informative Annex F | Organization/period/boundary/method/result/review records and an explanation query provide some report ingredients. Graph tests verify links | Not a complete ISO report, dissemination/report-planning process or verification engagement. Simulated accepted review is not independent assurance. ISO 14064-3, ISO 14065, ISO 14066 and ISO 14067 were not inspected in this review; Part 1 is not a substitute for them |

### Scenario-specific ISO correspondence — documentation, not a crosswalk engine

Under the fixture's stated control and non-overlap assumptions, Annex B supports
these interpretive groupings. They do not establish completeness or automatically
map every GHG Protocol inventory:

- **ISO category 1 / B.2:** natural-gas, diesel, fleet, refrigerant and new-line
  rows describe controlled combustion or fugitive sources. No sinks are modeled.
- **ISO category 2 / B.3:** electricity describes imported grid energy. Upstream
  fuel production, grid losses and capital infrastructure are not silently included.
- **ISO category 3 / B.4:** purchased inbound transport, business travel and
  commuting describe external transport. This is not GHG Scope3 category 3.
- **ISO category 4 / B.5:** materials, supplier-pcf, method-transition and
  allocation are disjoint purchased lots; capital is a purchased asset; waste is
  an external treatment service. Explicitly excluding the separately purchased
  inbound leg from lot footprints avoids the transport overlap discussed in B.4/B.5.
- **ISO categories 5 / B.6 and 6 / B.7:** no quantified fixture coverage. Lack of
  rows is not a zero-emission or non-significance determination. Downstream use
  and end-of-life sources remain omitted as shown in the screening below.

**Do not flatten differences between standards.** The benchmark's acquired-year,
non-amortized capital treatment follows the cited GHG Protocol guidance. ISO's
informative Annex B §B.5.2 also describes an amortized alternative; therefore the
benchmark restriction is not a universal ISO prohibition. Likewise ISO Annex E's
location-based requirement plus conditional additional market-based information
must not be replaced by the GHG Protocol's applicable dual-reporting rules. Both
frameworks need their own applicable requirements and documented methodological
choices; a shared number is not proof of shared conformity.

### Verification and public-disclosure boundary

On 2026-09-28 the existing benchmark, contract and graph suites were run with
`PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_benchmark.py tests/test_contract.py tests/test_graph.py`:
**161 passed**, with 10 existing RDFLib deprecation warnings. This verifies the
encoded software contract only. No tests assert ISO clause conformity; no new
runtime capability was introduced by this documentation review.

The public deliverable contains original paraphrases, section/page references and
implementation limitations only. Private source/OCR/image files, access locations
and license details are not repository artifacts. No external upload was used.
Outstanding review needs are qualified accounting interpretation, all applicable
source/significance decisions, the unimplemented controls above and separately
licensed review of any additional standards required by an intended engagement.

## Scope 3 applicability screening (scenario policy, all fifteen categories)

This is an electronics manufacturer, not a complete company inventory. “Omitted”
is a benchmark scope limitation, **not** a justified claim that real emissions are
immaterial. A production report must assess and justify all relevant exclusions.

| Category | Applicability / benchmark coverage and rationale |
|---|---|
| 1 Purchased goods/services | Applicable; four disjoint selected material lots; other purchases omitted (data not modeled) |
| 2 Capital goods | Applicable; one current-year acquisition only |
| 3 Fuel/energy-related not S1/S2 | Applicable; upstream fuel/electricity and losses omitted, no suitable dataset modeled |
| 4 Upstream transport/distribution | Applicable; selected purchased inbound freight only; no overlap with lot PCF transport |
| 5 Waste generated | Applicable; selected third-party treatment only |
| 6 Business travel | Applicable; selected passenger travel, hotel optional boundary omitted |
| 7 Employee commuting | Applicable; selected annual passenger distance; telework not modeled |
| 8 Upstream leased assets | Not applicable under explicit scenario: no assets leased outside controlled operations |
| 9 Downstream transport | Applicable; omitted, downstream distribution not modeled |
| 10 Processing sold products | Applicable for semiconductor intermediate outputs; omitted, customer processing data absent |
| 11 Use of sold products | Applicable electronics use-phase; omitted, lifetime/use scenarios absent |
| 12 End-of-life sold products | Applicable; omitted, sales/material fate data absent |
| 13 Downstream leased assets | Not applicable: no lessor operations in scenario |
| 14 Franchises | Not applicable: no franchises in scenario |
| 15 Investments | Not applicable: no investment portfolio outside consolidation in scenario |

## Regulatory and assurance limits

GHG Protocol organizational accounting, ISO organizational inventory requirements,
ISO verification standards, ISO14067 product footprints, disclosure/target programs,
and jurisdiction-specific legal reporting are different authorities. Taiwan/Vietnam
are fictional site locations, not regulatory applicability determinations. No claim
of compliance with local law, CBAM, IFRS S2, CDP or SBTi is made. Private ISO source
inspection resolves the former text-access blocker, not the implementation gaps.
Qualified practitioner review, complete source/significance screening, gas-resolved
reporting, applicable contractual evidence, category-level uncertainty assessment
and human assurance remain necessary before any stronger conformity claim.

### Current engineering coverage addendum

The earlier 161-test result is a dated baseline, not the current total. Selected
SHACL checks now include reference cardinality/type and factor unit/version and
review status/timestamp presence. Raw-row checks independently reject ten seeded
defects and additional malformed inputs; exact rational checks avoid ambient
Decimal rounding. They do not inspect original invoices or license authenticity.
CarbonDiff semantic causes are caller declarations, not independently inferred
causes. Evidence packages prove internal consistency, not authenticity. No gas-
resolved reporting, uncertainty assessment, completeness/significance procedure,
ISO six-category report or organizational assurance controls have been added.
Private licensed sources and extracts remain outside the repository.
