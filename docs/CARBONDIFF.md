# CarbonDiff — experimental Phase 5 Python API

`ghg_assurance_graph.diff` compares validated ExampleCo-GHG-001 raw snapshots. It does not
compare arbitrary RDF graphs, infer corporate causality, certify inventories or
automatically harmonize base years. [Acceptance contract](PHASE5_CONTRACT.md).

## API

```python
import json
from pathlib import Path
from ghg_assurance_graph.diff import Snapshot, compare

namespace = "synthetic://exampleco-ghg-001/20250926"
def load(version):
    rows = json.loads(Path(f"benchmark/generated/{version}/inputs.json").read_text())
    return Snapshot(namespace, version, tuple(rows))

result = compare(load("2025-v2"), load("2026-v1"))
assert result.delta == 210
assert result.residual_kg_co2e == 300  # signed UNKNOWN; not a rounding error
assert result.absolute_unknown_kg_co2e == 500
```

`Snapshot(namespace, version, rows)` defensively copies immutable scalar rows and
uses the existing benchmark preflight. Stable IDs are scoped by namespace; each
row evidence URI must equal namespace/version/id. Duplicate IDs, cross-snapshot
evidence, differing namespace, reused version and changed classification context
fail closed. Explicit namespace/ID assertions are trusted inputs, not independent
proof that two physical activities are identical. An attacker rewriting both ID
and evidence cannot be detected without external identity governance. No suffix,
label, ordering or fuzzy joins. Added/removed IDs remain distinct match statuses.
No graph revision or `supersedes` edge is invented.

`compare(before, after, declarations=()) -> DiffResult` returns ordered matches,
components, both totals, delta, attributed sum, signed residual and absolute
unknown exposure. All amounts are Decimal kgCO2e; output ordering is deterministic
by stable entity, then activity/factor/allocation. Inputs are never mutated.

## Arithmetic and ambiguity

For quantity q (including fixed unit scale), unallocated factor f and share s:

- activity: (q1 - q0) × f0 × s0
- factor: q1 × (f1 - f0) × s0
- allocation: q1 × f1 × (s1 - s0)

This ordered convention assigns interaction terms to later changes. It is project
policy, not a uniquely correct causal decomposition or standards requirement.
Mechanical ACTIVITY_CHANGE and EMISSION_FACTOR_CHANGE mean changed operands, not
proven operational drivers. Zero numerical components are omitted; metadata-only
unsupported changes are retained as zero UNKNOWN components.

Any other substantive field change conservatively makes the whole row delta
UNKNOWN, unless the caller supplies a scoped declaration. Changed units/methods,
GWP bases or allocation policies cannot silently become performance improvements.
Year, factor year and snapshot-specific evidence URI are bookkeeping; URI changes
alone are not automatically DATA_SOURCE_CHANGE.

Finite nonnegative decimal operands allow at most 60 coefficient digits and
exponents +/-60, and snapshots at most 10,000 rows. Calculations use an isolated
1000-digit Decimal context, sufficient for all bounded products/aligned sums; no
rounding tolerance or float conversion. Negative changes are allowed, negative
underlying emissions are not. Exact reconciliation is asserted internally:

`attributed_kg_co2e + residual_kg_co2e == total_after - total_before`

UNKNOWN components comprise the residual; do not add them again to all components.
Absolute unknown exposure prevents positive/negative unsupported rows canceling
out and falsely suggesting full explanation. Zero residual is not proof of
causality or comparability.

## Explicit semantic evidence

`Declaration(before, after, entity, cause, fields, evidence)` accepts **no numeric
answer**. The nonempty evidence text is a caller assertion; it is not downloaded,
authenticated or interpreted by an LLM. Version pair and entity must match and
`fields` must exactly cover observed substantive changes (or `presence` for an
added/removed record). One row-level declaration overrides mechanical components
with its full computed delta; overlapping or partial declarations are rejected.
This deliberately does not support multiple semantic drivers in the same row.
Do not use declarations without evidence sufficient to justify the entire delta.

All original ChangeEvent causes are retained: ACTIVITY_CHANGE,
SUPPLIER_MIX_CHANGE, EMISSION_FACTOR_CHANGE, GWP_CHANGE, METHOD_CHANGE,
DATA_SOURCE_CHANGE, DATA_QUALITY_CHANGE, BOUNDARY_CHANGE, ORGANIZATIONAL_CHANGE,
ALLOCATION_CHANGE, CORRECTION, MISSING_DATA_RESOLVED, UNKNOWN. There is no
automatic causal precedence among semantic labels. A supplied incorrect label
can still be incorrect: evidence authenticity remains human review work.

ExampleCo-GHG-001 explanatory annotations in tests come from the published scenario README:
corrected fleet invoice; travel estimate resolution; fixed supplier technology
and changed mix; same lot with method change; characterization-only refrigerant
change; organic new source (not acquisition); allocation policy transition.
These are separate from the expected numeric truth consumed only by tests.

## Safety and scope

Existing ExampleCo-GHG-001 preflight rejects market-based electricity: MB is unavailable, not
zero. LB and MB cannot be added, including rows with distinct IDs. This API does
not yet support separate valid MB comparisons. It rejects offsets, removals and
biogenic streams rather than netting them. All factors are precharacterized CO2e;
raw-gas factors and a second GWP application are rejected. GWP declarations label
a computed difference, never perform another GWP multiplication. Allocation is
applied once in raw rows; canonical factors already embed allocation and must
not be passed as unallocated raw factors. Supported conversion is the benchmark
conversion (tonne to kg) only; currency/FX and other conversions are not inferred.

## Reproducible evaluation and limits

Run `.venv/bin/python -m pytest tests/test_diff.py -q` (or locked `uv run pytest`).
The independent hand-authored expected-change JSON supplies nine component
answers across two comparisons. Annotation-assisted results match 9/9 labels and
9/9 exact amounts: precision/recall 1.0, mean absolute component error 0 kgCO2e,
residual 0; totals +30 and +210. This is **not autonomous label accuracy**, an
unseen holdout, statistical validation or empirical assurance effectiveness.
Seven semantic row labels are supplied as assertions; electricity contributes two
mechanically derived components. Without annotations, subsequent-year UNKNOWN
is +300 signed / 500 absolute kgCO2e, explicitly tested rather than hidden.

Tests also cover the existing ten malformed fixtures, all original cause values,
identity collisions/wrong joins, renames, cancellation, malformed declarations,
zero/negative changes, precision isolation, immutable inputs and conversion once.
Broader external inventories, canonical graph matching, simultaneous semantic
decomposition, authenticated event evidence, MB characterization and empirical
expert-label validation remain gaps. The integrated CLI exposes this bounded API; no certification claim is added.

## Public aggregate comparison
The separate [reported-disclosure profile](REPORTED_CONTRACT.md) matches explicit
organization, year, scope/category and Scope 2 basis. Numeric deltas are reported
with boundary/GWP/restatement qualifications, never operational causes. Missing
years/series remain missing, not zero. Totals, category components and Scope 2
alternatives are not blindly added. Every public aggregate causal driver is UNKNOWN.
