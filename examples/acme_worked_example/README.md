# ACME: inputs → evidence graph → checks → change explanation

This is the canonical worked-example guide for the **synthetic calculated-evidence profile**, not the separate public-company reported-assertion profile. Its objective is to make every operand, lineage edge, check and change explanation inspectable. **ACME, its invoices, suppliers and reviews are fictional. All factors are invented, nonproduction values.** This is not human assurance, certification, a complete inventory or whole-ISO conformity.

## 1. Locked installation and one-command run

Prerequisites: a checkout containing this guide and runner, Python **3.12** (release reproduction used 3.12.14), and uv. Run from the repository root. Installation may download locked dependencies; execution is offline and needs no API key, cloud model, paid service or factor database.

```sh
uv sync --locked
uv run --locked python scripts/run_acme_example.py --out artifacts/acme-worked
```

`--out OUTPUT` is the runner convention: choose a **new or empty** output directory, not a source directory; a nonempty destination is refused. The runner orchestrates generation, graph/explanation, validation, unassisted and declaration-assisted comparisons, packaging/verification and exports. Open `OUTPUT/REPORT.md` first. A successful process is not an assurance pass. For repeat runs use another destination. The individually executable stages below use a separate `artifacts/acme-manual` directory.

Runner output map:

- `REPORT.md`, `summary.json`: human-readable results and machine-readable totals, installed versions, checks and execution scope.
- `commands.json`: actual CLI arguments, relative working directory, expected/observed exit codes and stdout/stderr artifact paths.
- `generated/`: all three raw/canonical snapshots, ten defects and generator manifest.
- `sources/<snapshot>/`: 45 local synthetic citation JSON documents reconstructed from embedded evidence; `input-provenance.json` maps their IDs, paths and digests. These are not recovered real invoices.
- `sources/scenarios/` and `declarations/`: supplied scenario assertions and explicit diff declarations, separate from numeric expected answers.
- `stages/<snapshot>/`: combined validation, package-only SHACL report, Turtle/JSON-LD graph, explanations for every result, package verification and export receipts.
- `diffs/<before>--<after>/unassisted.json` and `assisted.json`: both comparison modes with components and residuals.
- `packages/<snapshot>/`, `vaults/<snapshot>/`: verified closed-profile crates and generated linked notes. Source documents remain outside those crates.
- `negative-validation.json`: deliberate double-GWP rejection, expected CLI exit 1; the runner itself succeeds only when this expected failure is observed.
- `manifest.json`: run-file digests excluding itself; internal integrity, not authenticity.

The runner checks Fraction products independently of the benchmark calculator, compares literal totals/deltas, and verifies source-document digests and vault links. Its process-local socket guard is not an OS sandbox. It generates all ten defects but executes one negative control; `benchmark run` and tests below evaluate the full public defect set. An absent `uv` on PATH is an environment issue: if already installed locally, use `.venv/bin/uv` for locked commands or `.venv/bin/python scripts/run_acme_example.py --out OUTPUT` after syncing. Do not silently replace the locked install with unpinned dependencies.

The [complete generated sample report](sample/REPORT.md) includes all 45 per-result calculations.
Only [selected readable artifacts](sample/README.md) are committed; regenerate the full
1,023-file tree rather than duplicating all graph, package and vault exports in Git.
The runner executes 73 CLI actions, including separate double-GWP and missing-factor-source
negative controls (both expected exit 1), and records exact receipts and hashes.

## 2. Three different fixture collections

- **Ten hand-authored canonical examples**: [cases.json](../cases.json) supplies numbers; [hand_authored.py](../hand_authored.py) maps them into the model. These illustrate all 17 record classes collectively. They are not ACME snapshots or defect cases.
- **ACME three snapshots**: [benchmark generator](../../src/ghg_assurance_graph/benchmark.py), fixed seed `20250926`, produces `2025-v1`, `2025-v2`, `2026-v1`. Each contains 15 activity rows, 15 results and 158 canonical records. `2025-v2` is a same-year restatement; `2026-v1` is a subsequent-year scenario, not a harmonized performance comparison.
- **Ten defective ACME fixtures**: isolated raw-row mutations of `2025-v1`, explicitly nonconforming, not canonical packages. Independent expected amounts, changes and findings live in [ground_truth](../../benchmark/ground_truth/expected_amounts.json). These public labels are evaluation inputs, not detector inputs or a blind holdout.

### The ten hand-authored cases

All use year 2025, `synthetic-region`, an **unknown/unapproved** consolidation boundary, a synthetic non-IPCC 100-year CO2e basis, no allocation, unknown quality and unquantified uncertainty. Factors below are kgCO2e per listed activity unit. Results are supplied illustrative values, not calculations executed by the domain model.

| Case | Classification | Activity × factor = kgCO2e | Method; origin |
|---|---|---|---|
| electricity-location | S2 location-based | 100 kWh × 0.5 = 50 | activity-based; primary |
| electricity-market | S2 market-based | 100 kWh × 0.2 = 20 | activity-based; secondary |
| natural-gas | S1 | 10 m³ × 2 = 20 | activity-based; primary |
| diesel-generator | S1 | 10 L × 3 = 30 | activity-based; primary |
| fleet-fuel | S1 | 20 L × 2.5 = 50 | activity-based; estimated |
| refrigerant | S1 | 1 kg × 100 = 100 | activity-based; estimated |
| purchased-material | S3 category 1 | 100 kg × 2 = 200 | activity-based; secondary |
| capital-spend | S3 category 2 | USD 100 × 0.1 = 10 | spend-based; secondary |
| upstream-transport | S3 category 4 | 100 tonne-km × 0.05 = 5 | activity-based; estimated |
| supplier-pcf | S3 category 1 | 50 kg × 4 = 200 | supplier-pcf; supplier-specific |

The market-based case demonstrates representation only, not contractual eligibility; do not add it to location-based electricity. All reviews are `unreviewed`; each authored `ValidationFinding` says illustration-only, not an executed finding. Fleet adds activity revision v2 = 21 L and a supplied `CORRECTION` event, but its original run/result still reference v1: revisions do **not** automatically recalculate downstream records. The fleet description mentions low quality, but the actual template assigns `rating=unknown`; inspect fields rather than interpreting prose as structured data.

```sh
uv run --locked python examples/hand_authored.py
```

This writes ten JSON, ten JSON-LD and ten Turtle files under `artifacts/examples`. It can replace prior example exports; it does not run the ACME pipeline.

## 3. Canonical record dictionary: all 17 types

The authoritative schema is [models.py](../../src/ghg_assurance_graph/models.py). An `EvidencePackage` has `schema_version: "0.1.0"` and a nonempty `records` collection. Unknown fields, duplicate revision IDs, broken or wrong-type references are rejected.

**Every record** has `kind` (type discriminator), `logical_id` (stable `urn:ghgag:<lowercase-slug>`), `version` (positive integer, default 1), `id` (logical ID plus `:vN`), `label` (nonempty display text), and `supersedes` (null for v1; immediate predecessor for later revisions). The predecessor must be included. Labels and values are not identity keys. `Quantity` contains finite nonnegative numeric `value` and an explicit `unit`; booleans, NaN and negative amounts are invalid. Canonical quantities are numeric transport values; raw ACME operands are decimal strings.

| Record | Additional fields and meaning |
|---|---|
| Organization | No extra fields; identifies reporting organization or simulated reviewer organization. |
| Facility | `organization`: owning organization reference; `geography`: declared region. |
| ReportingPeriod | `start`, `end`: inclusive dates; start cannot follow end. |
| BoundaryDefinition | `organization`; `consolidation`: operational-control, financial-control, equity-share or unknown; `description`: included operations and policy. |
| InventoryVersion | `organization`, `period`, `boundary`: inventory context; `status`: draft or reviewed, supplied metadata rather than computed assurance. |
| EmissionSource | `facility`; `scope`: integer 1/2/3; `category`: 1–15 required only for S3; `scope2_basis`: location-based/market-based required only for S2. |
| EvidenceArtifact | `citation`: source description (ACME embeds row JSON); `license`: reuse terms; `sha256`: optional artifact digest; `synthetic`: explicit fictional status. Citation/digest is not authentication. |
| ActivityRecord | `source`, `inventory`; `quantity`: observed/estimated activity, not CO2e; `evidence`, `quality`: provenance/assessment references; `data_origin`: primary, secondary, estimated, supplier-specific or unknown. |
| GWPSet | `basis`: characterization basis description; `horizon_years`: positive integer; `evidence`. No gas-specific GWP table or characterization engine is implied. |
| EmissionFactor | `value`; `numerator`: kg_CO2e or t_CO2e; `denominator`: activity unit; `evidence`, `period`, `geography`, `gwp`, `boundary`, `method`: applicability and provenance. |
| CalculationMethod | `method_type`: activity-based, spend-based, supplier-pcf or external-result; `description`; `allocation`: explicit policy text; `evidence`. |
| CalculationRun | `activity`, `factor`, `method`, `gwp`, `boundary`, `inventory`: one-activity/one-factor lineage; `performed_at`: timezone-aware timestamp; `software`: declared implementation. |
| EmissionResult | `calculation`, `inventory`; `quantity`: explicit CO2e; `review`: decision targeting this result. A model-valid supplied result is not automatically an arithmetic proof. |
| DataQualityAssessment | `rating`: high/medium/low/unknown; `rationale`; `uncertainty`: explicit description, including honest unknowns. |
| ReviewDecision | `target`; `reviewer`: Organization reference; `status`: unreviewed/accepted/rejected/needs-review; aware `timestamp`; `rationale`. No reviewer authority is authenticated. |
| ChangeEvent | `before`, `after`: ordered revisions of the same logical record; `cause`: supplied taxonomy label; `rationale`. Not automatic change detection. |
| ValidationFinding | `target`; `severity`: info/warning/error; `rule`; `message`. A canonical authored record is distinct from runtime validator finding objects. |

Change causes are `ACTIVITY_CHANGE`, `SUPPLIER_MIX_CHANGE`, `EMISSION_FACTOR_CHANGE`, `GWP_CHANGE`, `METHOD_CHANGE`, `DATA_SOURCE_CHANGE`, `DATA_QUALITY_CHANGE`, `BOUNDARY_CHANGE`, `ORGANIZATIONAL_CHANGE`, `ALLOCATION_CHANGE`, `CORRECTION`, `MISSING_DATA_RESOLVED`, `UNKNOWN`.

The package checks organization consistency, reference types, run/result context, factor period coverage, method/GWP/boundary agreement and dimensional compatibility. It does not establish source truth, completeness, significance or uncertainty adequacy. Canonical geography is declared metadata; ACME raw rules additionally enforce the fixture's site/geography policy. ACME uses snapshot-scoped IDs such as `urn:ghgag:acme-2026-v1-electricity-result:v1`; its cross-snapshot matching key is raw row `id=electricity`, not a fabricated canonical `supersedes` edge. ACME clean packages have neither authored ChangeEvents nor ValidationFindings: the ten earlier examples provide those types.

## 4. ACME inputs and accounting assumptions

**Organization:** Taiwan HQ (`hq`, TW), Taiwan semiconductor plant (`tw-plant`, TW), Vietnam assembly plant (`vn-plant`, VN), all 100% operationally controlled. Geography codes do not make factors official national values. Reporting periods are calendar years. All rows are annual, selected and non-overlapping; this is not a completeness/significance assessment of every Scope 3 category.

**Row fields:** `id` is the stable source key; `scope`, `category`, `facility` classify it; `year` is reporting year; `activity`/`unit` and `factor`/`factor_unit` are operands (factor_unit is its denominator). `factor_year`, `geography`, `factor_source` specify applicability; `factor_basis`, `apply_gwp`, `gwp_basis` state characterization. `allocation_share` and `allocation_method` specify allocation. `review` records simulated acceptance; `scope2_basis`, `stream`, `pcf_boundary` constrain accounting boundaries. `origin`, `method`, `evidence`, `uncertainty`, `coverage` preserve evidence limitations. `reported_kg_co2e` is the supplied result checked independently, not an extra operand.

The arithmetic is **activity × unit scale × unallocated factor × allocation share**. All factors are precharacterized kgCO2e, `apply_gwp=false`; GWP A/B are invented 100-year bases, not IPCC factors. Raw-gas characterization and second GWP multiplication are unsupported. `factor_year=year` is an ACME policy, not a universal standard requiring factor publication and inventory years to match. USD means same-year nominal synthetic USD: no FX, inflation or EEIO database is inferred.

Canonical unit spellings are `kWh`, `MJ`, `kg`, `tonne`, `liter`, `meter ** 3`, `km`, `tonne * km`, `USD`, `kg_CO2e`, `t_CO2e`. CO2e is not physical gas mass. The ACME arithmetic/diff accepts identical units and tonne→kg conversion only; broader Pint dimensional conversions in the canonical model do not broaden this calculator. No density, calorific conversion or currency conversion is guessed.

All activity origins are `primary` except travel in 2025-v1 (`estimated`), even the ACME supplier-PCF row: method and origin are separate fields. These are **scenario labels**, not real measurements. Quality stays unknown; uncertainty is not statistically quantified. Review `synthetic-accepted` maps to canonical `accepted` with an explicitly simulated rationale, while inventory status remains `draft`. Synthetic evidence URIs are identifiers, not downloadable invoices. Embedded row JSON supplies reproducible fixture evidence, not independent evidence of a real emission.

### Every source and number

Factors in the formula column are kgCO2e per displayed unit; share defaults to 1. The last three columns are kgCO2e.

| Row (site; scope/category) | 2025-v1 formula | 2025-v1 | 2025-v2 | 2026-v1 |
|---|---|---:|---:|---:|
| electricity (TW plant; S2 LB) | 1000 kWh × 0.5 | 500 | 500 | 480 |
| natural-gas (TW plant; S1) | 100 m³ × 2 | 200 | 200 | 200 |
| diesel (VN plant; S1) | 20 L × 3 | 60 | 60 | 60 |
| fleet (HQ; S1) | 30 L × 2 | 60 | 80 | 80 |
| refrigerant (TW plant; S1) | 2 kg × 1000 | 2000 | 2000 | 2400 |
| materials (TW plant; S3/1) | 100 kg × 4 | 400 | 400 | 300 |
| capital (TW plant; S3/2) | USD 1000 × 0.2 | 200 | 200 | 200 |
| transport (VN plant; S3/4) | 100 tonne-km × 0.1 | 10 | 10 | 10 |
| waste (TW plant; S3/5) | 50 kg × 0.2 | 10 | 10 | 10 |
| travel (HQ; S3/6) | 100 passenger-km × 0.2 | 20 | 30 | 30 |
| commuting (HQ; S3/7) | 100 passenger-km × 0.1 | 10 | 10 | 10 |
| supplier-pcf (VN plant; S3/1) | 50 kg × 3 | 150 | 150 | 150 |
| method-transition (TW plant; S3/1) | USD 200 × 0.5 | 100 | 100 | 50 |
| allocation (TW plant; S3/1) | 100 kg × 2 × 0.5 | 100 | 100 | 50 |
| new-line (VN plant; S1) | 0 L × 3 | 0 | 0 | 30 |
| **Selected-source total** | | **3820** | **3850** | **4060** |

| Breakdown | 2025-v1 | 2025-v2 | 2026-v1 |
|---|---:|---:|---:|
| Scope 1 | 2320 | 2340 | 2770 |
| Scope 2 location-based | 500 | 500 | 480 |
| Selected Scope 3 | 1000 | 1010 | 810 |

Specific assumptions prevent misleading interpretation:

- Fuels represent combustion only, not upstream fuel lifecycle emissions. Refrigerant is a hypothetical nonbiogenic HFC leak; 2026 changes its characterization to 1200, not its 2 kg mass. Only this row changes from synthetic GWP A to B.
- Electricity is purchased grid electricity. No contractual instrument, residual mix or verified fallback is supplied: **market-based is unavailable, not zero**. Location/market alternatives are never added; this is not a complete dual report.
- Materials, supplier-PCF, method-transition and allocation are **four distinct lots**. Cradle-to-gate production excludes separately purchased inbound freight (category 4), preventing an assumed double count. This is not PACT conformance or externally verified PCF compatibility.
- Materials supplier A/B factors stay 5/1. Mix 75%/25% gives 4; 50%/50% gives 3 in 2026. Supplier technology is held fixed; the semantic mix explanation is supplied.
- The transition lot is the same physical 50 kg purchase: USD 200 × 0.5 estimates 100 in 2025; supplier PCF 50 kg × 1 gives 50 in 2026. This method change is not evidence of decarbonization.
- Capital goods are acquired during the year, not amortized. Freight uses metric tonne-km. Waste covers selected third-party treatment lifetime emissions for waste generated during the year; no avoided-emissions credit.
- Travel/commuting use passenger-distance for one synthetic transport class, not vehicle-km. Commuting is annual return-trip distance; hotels, telework and modal uncertainty are not invented. Travel's 100 km estimate is replaced by 150 km primary observation in the restatement. Missing primary data was represented by an estimate, not zero.
- Allocation keeps physical burden 100 kg × 2 = 200: mass-share 50% gives 100; economic-share 25% gives 50 in 2026. This is a policy change, not an operational reduction. **Canonical factors embed the share once** (1 then 0.5); raw factors stay 2. Do not apply allocation twice.
- The new line starts in 2026 at the existing VN site, 10 L × 3 = 30: organic source-boundary expansion, **not acquisition**. Earlier zero is a declared structural absence, not a missing-data fallback.
- Offsets, removals and biogenic streams are unsupported and never netted against these totals.

## 5. Exact stages and inspectable outputs

The following shell commands make a standalone manual run. Paths are relative to the repository root. The first command refuses an existing destination; do not run it against the runner's output.

```sh
mkdir artifacts/acme-manual
uv run --locked ghgag benchmark run --out artifacts/acme-manual/generated > artifacts/acme-manual/benchmark-report.json
uv run --locked ghgag graph build artifacts/acme-manual/generated/2026-v1 > artifacts/acme-manual/graph.ttl
uv run --locked ghgag graph explain urn:ghgag:acme-2026-v1-electricity-result:v1 --input artifacts/acme-manual/generated/2026-v1 > artifacts/acme-manual/explain-electricity.json
uv run --locked ghgag graph query unreviewed_results --input artifacts/acme-manual/generated/2026-v1 > artifacts/acme-manual/unreviewed.json
uv run --locked ghgag validate artifacts/acme-manual/generated/2026-v1 > artifacts/acme-manual/validation.json
uv run --locked ghgag diff artifacts/acme-manual/generated/2025-v1 artifacts/acme-manual/generated/2025-v2 > artifacts/acme-manual/diff-restatement-unassisted.json
uv run --locked ghgag diff artifacts/acme-manual/generated/2025-v2 artifacts/acme-manual/generated/2026-v1 > artifacts/acme-manual/diff-year-unassisted.json
uv run --locked ghgag package create artifacts/acme-manual/generated/2026-v1 --out artifacts/acme-manual/crate --created-at 2026-09-28T00:00:00Z --data-version acme-0.1-2026-v1
uv run --locked ghgag package verify artifacts/acme-manual/crate > artifacts/acme-manual/verification.json
uv run --locked ghgag export obsidian artifacts/acme-manual/vault --input artifacts/acme-manual/generated/2026-v1
uv run --locked ghgag export json-ld artifacts/acme-manual/graph.jsonld --input artifacts/acme-manual/generated/2026-v1
uv run --locked pytest -q
```

`benchmark run` generates three `inputs.json`/`package.json` pairs, ten raw defect JSON files and a manifest, then evaluates the selected rules against public expected labels. Expect clean finding counts of zero for all three snapshots; 10 TP, 0 FP, 0 FN on these fixtures (not a generalization estimate). It also reports **unassisted** CarbonDiff results. It does not by itself evaluate all annotation-assisted causes. Independent arithmetic/change checks are exercised by tests and the worked runner.

`graph.ttl` is the canonical RDF/PROV representation; `explain-electricity.json` traces 480 kgCO2e to activity 800 kWh, factor 0.6, evidence, method, period, boundary and simulated review. `unreviewed.json` is empty because all ACME results carry simulated accepted decisions, **not because an independent reviewer approved them**. Other allowlisted queries are `results_using_factor`, `records_supported_by_evidence`, `revisions` and `explain_result`; target types are enforced. No arbitrary SPARQL or network fetch is executed.

`validation.json` should have `conforms: true` and empty findings. Directory validation checks the canonical package (including packaged SHACL shapes) and adjacent raw inputs. Validating only `package.json` does not run the raw-row checks; model/SHACL structure is not proof of arithmetic, evidence authenticity or accounting completeness.

The crate contains `package.json`, `graph.ttl`, `graph.jsonld`, `schema.json`, `ontology.json`, `ro-crate-metadata.json`, `manifest.json`. Verification checks internal consistency/integrity; an attacker able to replace payloads and manifest can create a different internally consistent package. A digest is not a signature or assurance opinion. The declared creation timestamp is a reproducibility input, not a claim about when you executed the command. No particular hash value is promised here. The vault contains generated notes/index/links for local inspection, not proof of Obsidian application behavior.

## 6. Change explanation: numbers versus supplied semantics

The convention is **activity-first; factor-second; allocation-last; semantic row override**. For activity q, factor f, share s, with fixed unit scale included in q:

- Activity component: (q1 − q0) × f0 × s0.
- Factor component: q1 × (f1 − f0) × s0.
- Allocation component: q1 × f1 × (s1 − s0).

Interaction terms go to later steps. This is project policy, **not a standard-prescribed unique causal decomposition**. Electricity in 2026 is 800 × 0.6 = 480: activity (800−1000) × 0.5 = **−100**, factor 800 × (0.6−0.5) = **+80**, net **−20**. Mechanical labels describe operands, not independently established operational causes.

### Expected reports

| Comparison/mode | Delta | Attributed | Signed UNKNOWN residual | Absolute UNKNOWN exposure |
|---|---:|---:|---:|---:|
| 2025-v1 → 2025-v2, unassisted | +30 | +20 | +10 | 10 |
| 2025-v1 → 2025-v2, assisted | +30 | +30 | 0 | 0 |
| 2025-v2 → 2026-v1, unassisted | +210 | −90 | +300 | 500 |
| 2025-v2 → 2026-v1, assisted | +210 | +210 | 0 | 0 |

Unassisted restatement: fleet +20 is mechanical ACTIVITY_CHANGE; travel +10 is UNKNOWN because `origin` changes as well as activity. Unassisted subsequent year: electricity −100/+80, materials −100 factor change, and new-line +30 activity change are mechanical; allocation −50, method-transition −50 and refrigerant +400 are UNKNOWN. Their signed sum is +300 but absolute exposure is 50+50+400=500. Opposite unknowns must not cancel away uncertainty.

Assisted restatement: **+30 = CORRECTION +20 + MISSING_DATA_RESOLVED +10**. Assisted subsequent year: **+210 = −100 activity +80 factor −100 supplier mix −50 method +400 GWP +30 boundary −50 allocation**. These seven semantic row labels are **supplied scenario assertions**, not autonomous discovery; electricity's two components are mechanical. All nine expected components across the comparisons match the published controlled scenario, not unseen causal ground truth.

To reproduce assisted CLI output, create declarations separately from expected numeric answers:

```sh
uv run --locked python - <<'PY'
import json
from pathlib import Path
root = Path('artifacts/acme-manual')
pairs = [
    ('2025-v1', '2025-v2', 'restatement', [
        ('fleet', 'CORRECTION', 'activity', 'Scenario: corrected fleet invoice'),
        ('travel', 'MISSING_DATA_RESOLVED', 'activity origin', 'Scenario: estimate replaced by primary observation'),
    ]),
    ('2025-v2', '2026-v1', 'year', [
        ('materials', 'SUPPLIER_MIX_CHANGE', 'factor', 'Scenario: supplier mix changes; technology fixed'),
        ('refrigerant', 'GWP_CHANGE', 'factor gwp_basis', 'Scenario: characterization only'),
        ('new-line', 'BOUNDARY_CHANGE', 'activity', 'Scenario: organic source addition, not acquisition'),
        ('allocation', 'ALLOCATION_CHANGE', 'allocation_method allocation_share', 'Scenario: allocation policy changes'),
        ('method-transition', 'METHOD_CHANGE', 'activity unit factor_unit factor method pcf_boundary', 'Scenario: same physical lot, changed method'),
    ]),
]
for before, after, name, specs in pairs:
    declarations = [dict(before=before, after=after, entity=entity, cause=cause,
                         fields=fields.split(), evidence=evidence)
                    for entity, cause, fields, evidence in specs]
    (root / f'declarations-{name}.json').write_text(json.dumps(declarations, indent=2) + '\n')
PY
uv run --locked ghgag diff artifacts/acme-manual/generated/2025-v1 artifacts/acme-manual/generated/2025-v2 --declarations artifacts/acme-manual/declarations-restatement.json > artifacts/acme-manual/diff-restatement-assisted.json
uv run --locked ghgag diff artifacts/acme-manual/generated/2025-v2 artifacts/acme-manual/generated/2026-v1 --declarations artifacts/acme-manual/declarations-year.json > artifacts/acme-manual/diff-year-assisted.json
```

Declarations contain version pair, entity, cause, exact changed `fields`, and nonempty explanatory `evidence`, **never a numeric answer**. The code recomputes the full row delta. Text is not downloaded, authenticated or interpreted by an AI. One declaration must cover every substantive changed field for the row; partial/overlapping claims are rejected. Evidence URI/year bookkeeping is excluded from substantive changes. A wrong but structurally valid semantic assertion can still be wrong.

CarbonDiff uses exact bounded Decimal arithmetic and asserts `attributed + residual == total_after − total_before`. Residual is the sum of UNKNOWN components; do not add it again to the sum of all components. Zero residual does not prove causal truth or cross-year comparability.

**Restatement policy:** base year 2025; this scenario chooses cumulative absolute eligible changes ≥0.5% of 3820 = 19.1 kgCO2e. The +30 restatement exceeds it. This is a documented project policy, not a standard-mandated threshold or a general automated materiality engine. Later GWP/method/allocation changes require review and base-year harmonization before a performance claim; no harmonized base year is supplied. Organic new-line growth is not an acquisition or a base-year structural-recalculation trigger.

## 7. Negative cases, missing inputs and exit codes

For the CLI, **0** means the requested selected operation completed (validation: no selected findings), **1** means validation emitted findings, and **2** means invalid input/request with no result asserted. A missing file is not a zero inventory. Canonical malformed records may be rejected at load time with exit 2 before a findings report can be produced. A raw row with missing/negative numeric operands yields an `invalid amount or allocation` finding (exit 1 when using the raw wrapper); no substitute amount is authorized. An empty raw list gives `empty inventory`, not total zero.

| Defect file under generated/defects | Intended finding | Why |
|---|---|---|
| unit-error.json | reported amount mismatch | Materials unit changed kg→tonne without updating reported 400; converted amount would be 400000. |
| missing-factor-source.json | factor provenance | Required synthetic factor source absent. |
| wrong-factor-year.json | factor applicability | Electricity factor year 2020 violates ACME same-year rule. |
| unsupported-pcf.json | unsupported PCF boundary | Gate-to-gate/unknown exclusions cannot stand in for declared boundary. |
| manual-override.json | manual override not reviewed | Fleet review changed to unreviewed. |
| duplicate-activity.json | duplicate activity | Repeated electricity would add an invalid extra 500 if blindly summed. |
| double-gwp.json | no double GWP | Precharacterized refrigerant incorrectly asks for another GWP multiplication. |
| missing-contract.json | market-based evidence unavailable | No supported MB instrument or fallback. |
| unknown-unit.json | unsupported unit conversion | Ambiguous gallon is not guessed. |
| offset-netting.json | separate biogenic/removal/offset | Offset cannot be netted into this emissions stream. |

The first six are public development cases; the last four are public holdout-labelled cases, not unseen tests. To inspect rejection while preserving the expected nonzero exit:

```sh
uv run --locked ghgag validate artifacts/acme-manual/generated/defects/unit-error.json > artifacts/acme-manual/negative-unit.json
# Immediately after the command, in the same shell:
printf 'exit=%s\n' "$?"
```

Expect exit 1, `conforms: false`, and a finding identifying `materials`, rule, error severity and message. In a shell with `set -e`, run expected-failure cases in an explicit conditional; do not silently ignore arbitrary failures. Other invalid fixtures have no authorized corrected fallback. Canonical missing references, mismatched inventory contexts, invalid periods, duplicate identities, unsupported units and negative amounts fail closed. Diff also rejects inconsistent classification for the same ID, invalid evidence binding and malformed declarations rather than guessing a join.

## 8. Change an input and follow propagation

Work on a copy, never overwrite the independent ground truth to make a changed scenario pass. The generator only accepts the published seed and three version names; editing generated files then rerunning generation will replace those edits. For experiments, load/copy rows and call the explicit Python API. For example, change 2026 electricity from 800 to 900 kWh:

```sh
uv run --locked python - <<'PY'
import json
from pathlib import Path
from ghg_assurance_graph.benchmark import amount, package
root = Path('artifacts/acme-manual')
rows = json.loads((root / 'generated/2026-v1/inputs.json').read_text())
row = next(r for r in rows if r['id'] == 'electricity')
row['activity'] = '900'
row['reported_kg_co2e'] = str(amount(row))
out = root / 'experiment/2026-v1'
out.mkdir(parents=True, exist_ok=False)
(out / 'inputs.json').write_text(json.dumps(rows, indent=2) + '\n')
(out / 'package.json').write_text(package('2026-v1', rows).model_dump_json(indent=2) + '\n')
PY
uv run --locked ghgag validate artifacts/acme-manual/experiment/2026-v1
uv run --locked ghgag graph explain urn:ghgag:acme-2026-v1-electricity-result:v1 --input artifacts/acme-manual/experiment/2026-v1
uv run --locked ghgag diff artifacts/acme-manual/generated/2025-v2 artifacts/acme-manual/experiment/2026-v1
```

Expected electricity 540, partial total 4120, cross-year delta +270. Activity-first electricity components become −50 and +90, net +40; unassisted UNKNOWN residual remains +300/absolute 500 because other rows are unchanged. The +60 total change follows 100 extra kWh × 0.6. Leaving the old reported value 480 intentionally causes rejection, not automatic silent repair.

The experiment keeps the original snapshot name so the fixed ACME CLI evidence binding remains valid; it is an **alternative scratch dataset**, not a new immutable published revision. Do not merge its graph with the original: identical canonical IDs with changed content conflict. For real revision work, mint explicit logical/revision identities, preserve predecessors and update dependent activity/factor/run/result/review references. The example generator is not that general revision manager.

Propagation is explicit: raw row → embedded EvidenceArtifact and digest, ActivityRecord, factor/method/GWP context → CalculationRun → EmissionResult → graph/explanation, validation, diff, exported package/vault. Changing source files does not refresh already exported crates or notes. Regenerate into fresh destinations and verify again. If allocation changes, preserve the raw unallocated factor and embed the share only once when constructing the canonical factor. If units/method/GWP policy change, expect UNKNOWN until a complete supported declaration is supplied. If physical identity/classification changes, do not force an old stable ID to hide it.

## 9. Scope and further reading

This guide follows the original phase sequence: canonical representation, benchmark, graph, selected validation, change attribution, portable package and optional notes. The [original-plan acceptance matrix](../../docs/ROADMAP_ACCEPTANCE.md) distinguishes engineering evidence from research/submission gates. The [domain model](../../docs/DOMAIN_MODEL.md), [validation contract](../../docs/VALIDATION.md), [CarbonDiff contract](../../docs/CARBONDIFF.md), [evidence packaging](../../docs/EVIDENCE.md) and [standards alignment](../../docs/STANDARDS_ALIGNMENT.md) document narrower implementation boundaries. Historical phase-only status statements in older documents should not be mistaken for current whole-project status.

Tests validate encoded contracts, not every accounting requirement. Selected-source totals cannot establish organizational completeness, all-gas ISO reporting, uncertainty adequacy, evidence authenticity, reviewer independence or standards conformity. Public reported totals with unavailable upstream activity/factor evidence belong in the [reported-disclosure profile](../../docs/REPORTED_CONTRACT.md), not invented ACME-style calculations.
