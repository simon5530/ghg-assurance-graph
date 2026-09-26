# ACME Electronics benchmark v0.1

Original synthetic data and code: MIT. **Nonofficial factors; never production defaults.**
Clean = valid selected-source evidence, not complete GHG/ISO reporting or assurance.
[Standards alignment and all 15 Scope3 categories](../docs/STANDARDS_ALIGNMENT.md).
[Acceptance contract](../docs/PHASE2_CONTRACT.md). Gate A remains HOLD.

## Reproduce (Python 3.12, locked dependencies)

```sh
uv sync --locked
uv run python -m ghg_assurance_graph.benchmark --seed 20250926
uv run pytest -q
```

If uv is not on PATH, use the existing environment's .venv/bin/uv or
.venv/bin/python. No global install is necessary. Generator only accepts the
published seed: v0.1 uses a fixed deterministic scenario, not random scientific
sampling. Seed identifies evidence namespaces; no timestamps, network or randomness
enter outputs. An alternative output directory can be supplied with --out.

- generated/2025-v1: original, internally valid baseline with a disclosed travel estimate.
- generated/2025-v2: same-year restatement, corrected fleet invoice and travel estimate resolution.
- generated/2026-v1: subsequent-year methodological/operational changes; **not harmonized for performance comparison**.
- generated/defects: ten deliberately NONCONFORMING isolated raw mutations, never clean packages.
- ground_truth: independently hand-authored amounts, changes and expected finding labels.
- generated/manifest.json: SHA256 of all 16 payload files (manifest excludes itself).

Each snapshot has 15 source rows, 158 canonical records and 15 results. Snapshot
IDs are immutable snapshot-scoped identities; stable row id is the explicit match
key across snapshots. No canonical supersedes edge is fabricated between unrelated
snapshot identities; same-year relation is documented here and in change truth.
A general version graph/matcher remains Phase 3/5 work.

## Synthetic assumptions and arithmetic

ACME Electronics Group has Taiwan HQ, Taiwan Semiconductor Plant and Vietnam
Assembly Plant, all fully operationally controlled. These names/geographies are
fictional scenario descriptors. No actual company, invoice or supplier data used.
All numerical factors and 100-year GWP bases are invented; these are not Taiwan,
Vietnam, IPCC, EEIO database or supplier-certified values. Values deliberately
remain small for independent hand calculation.

All activities are annual and non-overlapping. Fuel factors represent combustion
only, not upstream lifecycle emissions. Refrigerant is a hypothetical nonbiogenic
HFC with precharacterized factors 1000 then 1200 kgCO2e/kg leak; gas mass never
passes as CO2e. All other factors keep basis A; basis B changes only that HFC
characterization in this synthetic set. No second GWP multiplication is allowed.
No biomass combustion, removals or offsets are modeled or netted.

Electricity is purchased grid electricity with location-based factors. No market
instrument, residual mix or demonstrated fallback evidence is supplied. MB is
therefore unavailable, not zero, and the partial LB figures cannot constitute a
complete dual report. LB and MB are alternative views, never additive.

Purchased materials, supplier-PCF, method-transition and allocation rows describe
four **different lots**. All cover cradle-to-gate production, excluding the
separately purchased inbound transport leg assigned to category4. Supplier A/B
material factors are 5 and 1 kgCO2e/kg: 75/25 shares produce 4, 50/50 produce 3.
Supplier technology is held fixed; only the purchased mix changes. The transition
lot is the same physical 50kg purchase estimated from USD200 x 0.5 in 2025,
then supplier-PCF 50kg x 1 in 2026; USD are same-year nominal values, no FX or
inflation extrapolation. This is a method change, not proven decarbonization.

Capital goods are acquired in the reporting year, not amortized. Transport is
metric tonne-km of selected purchased inbound freight. Waste is third-party
selected waste treatment lifetime emissions for waste generated in the year;
no recycling or avoided-emission credits. Travel and commuting km mean total
passenger-distance for one specified synthetic transport class, not vehicle-km;
commuting is annual return-trip distance, not one-way daily distance. No hotel,
telework or modal uncertainty is silently estimated.

Allocation lot has shared process burden 100kg x 2. Mass allocation assigns 50%,
then economic allocation assigns 25%; these are deliberately contrasting policy
choices with unchanged physical burden, not evidence of a reduction. Canonical
factor embeds share once; raw evidence retains unallocated factor and share.

New line is installed in 2026 inside the existing Vietnam site: source boundary
addition and **organic growth**, not an acquired pre-existing entity. 2025 activity
zero is an explicit structural absence assumption, never a missing-data fallback.
Travel missing primary data is represented by 100km estimate (20kgCO2e), replaced
by 150km primary observation (30kgCO2e); baseline never silently omits it.

All evidence URIs are synthetic identifiers, not downloadable records. The embedded
row JSON and its checksum are the actual reproducible evidence. Review accepted
means simulated fixture review only. Data quality is unknown; uncertainty is not
statistically quantified. Exact arithmetic is not real-world precision.

## Expected comparisons (kgCO2e, selected-source totals only)

| Version | S1 | S2 location | selected S3 | Partial total |
|---|---:|---:|---:|---:|
| 2025-v1 | 2320 | 500 | 1000 | 3820 |
| 2025-v2 | 2340 | 500 | 1010 | 3850 |
| 2026-v1 | 2770 | 480 | 810 | 4060 |

Restatement +30 = corrected invoice +20 + missing primary travel data resolved +10.
Next-year +210 = activity -100 + grid factor +80 + mix -100 + method -50 +
GWP +400 + organic source-boundary addition +30 + allocation -50.
For electricity, activity-first convention: (800−1000)×0.5 = −100;
800×(0.6−0.5) = +80. This convention is PROJECT policy, not a standard-prescribed
unique causal decomposition. No CarbonDiff algorithm or attribution accuracy claim.

Base year: 2025. Project policy uses cumulative absolute eligible restatement
changes of at least 0.5% of the original partial total (19.1kgCO2e); no standard
mandates 0.5%. +30 triggers the published 2025-v2 restatement. Eligible significant
method/GWP/accuracy/structural changes require review/recalculation before a
like-for-like performance claim. The later +400 GWP and method/allocation changes
require harmonization that is **not supplied** by these three scenario snapshots.
Organic new-line growth is not a base-year structural recalculation trigger.
No reduction claim is based on raw cross-year totals.

## Defects and leakage controls

Six development cases implement the original unit error, duplicate activity,
missing factor source, incorrect factor applicability year, unsupported PCF boundary,
and unreviewed manual override. Four public holdout cases add double GWP, missing
Scope2 contract evidence, ambiguous units and offset netting. Each ground-truth
entry names case, entity, expected error rule, severity and split. Unit-error
changes kg to tonne without changing reported amount: 400 versus 400000kgCO2e.
Duplicate electricity would overstate by 500 if blindly summed. Other invalid
inputs have no authorized corrected numeric fallback.

Expected labels are separate from raw fixtures and never read by generator.
Future detector input must exclude ground_truth and mutation source, and hide case
filenames if they reveal labels. Public “holdout” is a reproducible partition, **not
secret/unseen evaluation**. Phase2 tests preflight rejection, not SHACL precision,
recall or F1; no detector is implemented.
