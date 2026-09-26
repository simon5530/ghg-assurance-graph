# Standards alignment — bounded evidence, not certification

Inspected 2026-09-26. This synthetic partial benchmark is not a conforming corporate
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
  edition 2, December 2018, confirmed 2024 (not a 2024 edition). Official-domain
  search retrieved confirmation metadata; direct fetch and
  [lawful OBP preview](https://www.iso.org/obp/ui/en/#iso:std:iso:14064:-1:ed-2:v1:en)
  returned 403. No access workaround attempted. Full clauses and Annex B were
  **not inspected**; ISO clause-level conformance remains **unverified** and needs
  licensed practitioner review. No invented clause citations.
- **Revision status:** [Official July 29, 2026 FAQ](https://ghgprotocol.org/blog/ghg-protocol-announces-key-standard-development-updates-faq-resource),
  inspected questions 1–3: joint GHG Protocol/ISO consolidated corporate standard
  planned consultation Q2 2027, publication Q4 2028. These plans and 2025/2026
  consultation proposals are **not final replacement accounting requirements**.

PDF-tool page filtering proved incomplete; full-document inspection was used for
the substantive sources above. Source inspection is evidence, not independent
professional interpretation; no verbatim standards passages are shipped.

## Requirement → implementation → test → evidence status

| Topic / source | Bounded implementation and test evidence | Status / limitation |
|---|---|---|
| Organizational consolidation C ch.3 | Canonical BoundaryDefinition names operational/financial control/equity share; ACME explicitly 100% operational control of 3 sites. Package integrity + clean oracle test | Only operational-control scenario exercised; no inferred equity percentages |
| Operational boundaries C ch.4; S3 Table5.4 | Scope/category/source fields; category coverage below and benchmark assumptions; category coverage test | Selected sources, not complete Scope1/2/3; no cross-company comparability claim |
| ISO direct vs indirect | ISO taxonomy must remain separate from GHG scopes. Direct emissions/removals and indirect imported-energy, transport, products-used, products-use, other categories are not interchangeable with scopes 1/2/3 or the 15 Scope3 categories | Conceptual orientation only, no asserted verified ISO mapping or clause coverage; no ISO-category field auto-filled |
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
of compliance with local law, CBAM, IFRS S2, CDP or SBTi is made. Licensed ISO review,
complete source screening, gas-resolved reporting, contractual evidence and human
assurance remain blockers to any stronger conformity claim.
