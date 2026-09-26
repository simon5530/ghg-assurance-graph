# Canonical domain model 0.1

Status: bounded experimental Phase 1, not a calculator or assurance opinion.
[Authorization and acceptance contract](PHASE1_CONTRACT.md).

## Records and ownership
The 17 discriminated Pydantic records are Organization, Facility, ReportingPeriod,
InventoryVersion, EmissionSource, ActivityRecord, EvidenceArtifact, EmissionFactor,
GWPSet, CalculationMethod, CalculationRun, EmissionResult, BoundaryDefinition,
DataQualityAssessment, ReviewDecision, ChangeEvent and ValidationFinding.
The definitive field/type contract is [models.py](../src/ghg_assurance_graph/models.py);
JSON Schema is available from `EvidencePackage.model_json_schema()`.
Unknown fields are rejected, including per-example extensions. All nested records
are frozen and record collections are tuples. Validated model_copy updates are
revalidated; callers must not use Pydantic model_construct or Python object-level
mutation as an ingestion API. Serialize only validated packages.

## Identity, versions and migration
Logical identity uses `urn:ghgag:<lowercase-slug>`; revision identity appends
`:v<positive-integer>`. IDs never derive from mutable labels or numeric values.
Version 1 has no predecessor; later versions require the immediately preceding ID.
A closed package includes predecessors and rejects duplicate revision IDs, even
identical duplicates, and type changes under one logical ID. No auto-merge or
last-write-wins behavior. Correct a record by adding a new revision, preserving old
references until the caller explicitly supplies revised downstream records.

content_digest() is SHA256 of sorted compact UTF-8 Pydantic JSON including identity;
it detects content differences, is not the record ID or a signature, and is not a
cross-language canonical JSON standard. No persistent registry prevents a different
package reusing an ID with changed content. Store/review digests externally if needed.
Schema version is exactly 0.1.0; unknown versions fail closed. No prior schema exists
to migrate; migration must be explicit and tested before accepting a new version.

## Domain boundaries
Scope is 1/2/3; only Scope 3 has categories 1–15; only Scope 2 has a required
location/market basis. A source belongs to a facility and organization. Packages
check inventory organization/boundary and result/run/inventory consistency, factor
validity covering inventory dates (inclusive), method/GWP/boundary equality and
activity/factor dimensional compatibility. This conservative profile requires one
activity and factor per run; multi-input/gas-component/allocation models are deferred.
A supplier PCF boundary description does not establish comparability to a corporate
inventory. Geography is explicit metadata, not automated applicability validation.

Finite nonnegative numeric values only; zero is valid, booleans/strings are not amounts.
Negative removals, credits and uncertainty intervals are not supported in this profile.
Pint handles a small enumerated vocabulary: energy, mass, volume, distance, tonne-km,
USD and CO2e. CO2e has its own dimension; converting gas mass to CO2e needs a supplied
factor/GWP context, not unit conversion. USD has no exchange-rate or inflation logic.
Floats are transport values; no accounting precision/tolerance guarantee is made.

Evidence has citation/license/synthetic status and optional artifact SHA256. A citation
is not a downloaded or authenticated document; absent digest stays absent. Factor
source, reference period, geography, GWP, method and boundary are mandatory. Method
allocation and quality uncertainty are explicit text, including honest unknowns.
Review uses an organizational reviewer reference, aware timestamp and explicit status;
no personal identity, authority or approval workflow is authenticated. Inventory status
is supplied metadata, not a computed assertion that all results passed review.

## Verification and remaining questions
[Tests](../tests/test_contract.py) check schema, reference/type integrity, revisions,
units, negatives and roundtrips. [Ten cases](../examples/README.md) cover all 17 classes.
ChangeEvent and ValidationFinding are supplied records, not inferred findings or
CarbonDiff. No arithmetic is executed by domain models. Domain/practitioner review,
consolidation/allocation policy, biogenic accounting and attribution remain open.
