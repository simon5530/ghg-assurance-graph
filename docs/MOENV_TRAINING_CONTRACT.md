# MOENV internal-collection training contract — 2026-10-15

## Decision and workflow

Use an original fictional company with complete internal evidence, not listed-company
benchmarking. Public reports cannot supply unpublished activity logs, evidence custody,
calibration or collection forms. Do not invent those records for a real organization.

Trigger: annual collection. Inputs: boundary/source register, monthly logs, selected
parameters and evidence. Deterministic stages: validate completeness/units/hash and raw
balances → aggregate → quantify gases → project to the existing CO2e graph → inspect
quality and uncertainty → reviewer decision → export. Draft/unreviewed is the default;
missing data is a blocker, not zero. No model or external service runs the arithmetic.

The existing CSV, Pydantic, RDF/PROV and graph validation infrastructure is adequate;
no new agent system, paid platform or alternative graph architecture is introduced.
Official MOENV ODS and ODT already provide filing/reference infrastructure. We add
an internal traceability layer and original training records, not a competing filing app.

## Acceptance

- Two complete calendar years, 2023 and 2024, one fictional manufacturing plant.
- Every source has 12 monthly records per year, including documented inactive zeros.
- Original table designs map to official tables 1–11. Evidence and changes are
  project extensions 12/13, not alleged official mandates.
- Electricity meter differences, fuel-stock and refrigerant mass balances reconcile.
- Missing month, duplicate, blank amount, wrong year/unit, invalid digest, contradictory
  evidence and incorrect equipment cutoff fail before quantification.
- An independent Fraction oracle checks the Decimal calculations and literal totals.
- CO2, CH4 and N2O combustion factors and gas GWP values retain source references.
  Synthetic LHV is marked as an assumption. Historical electricity vintages are an
  explicit teaching choice, not the regulator's latest-factor selection rule.
- Workbook formulas recalculate under a changed monthly input; missing input exposes
  MISSING. Workbooks are collection views; CSV/documents require separate validation.
- Reports remain draft examples. No human signature, actual registration, uncertainty
  percentage, certification, conformity or reduction claim is fabricated.

## Boundaries

MOENV's facility/registered boundary is not interchangeable with a corporate
consolidation policy. The fictional site has no real registration; operational control
is graph metadata, not proof of a legally correct filing boundary. No ISO category
crosswalk or complete Scope 3 report is claimed. Applicability for other industries
requires replacing the source register, not applying these example omissions blindly.

Gas arithmetic lives in companion tables. Existing schema 0.1 still represents
precharacterized kgCO2e; factors are projected once and GWP is not multiplied again.
No gas-resolved core migration or unconstrained calculator is implemented.
Hashes bind file contents but do not authenticate observations or signatures.
Unknown uncertainty remains unknown, never 0%.

Historical Git objects and releases are not rewritten. Superseded company-comparison
execution is removed from the current tree; generic reported-assertion schema/tests
remain independent compatibility functionality, not evaluation against a real company.
