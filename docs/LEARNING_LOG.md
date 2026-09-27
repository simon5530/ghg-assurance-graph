# Learning Log

Status: Phase 0 planning; domain features are not implemented.

## 2026-09-24 — Separate a scaffold from research evidence
A working documentation check demonstrates repository consistency, not scientific
validity. Keep implementation, evaluation, novelty, and publication gates independent.
A local isolated checkout demonstrates portability of the docs check, not a
fresh-machine scientific reproduction. Preserve these distinctions in later PRs.

Future entries should record question → evidence → decision → limitation, linking
versioned artifacts rather than copying operational logs or private context.

## 2026-09-25 — publication evidence chain
Symptom: prior status conflated local files with published artifacts. Cause: no
remote-state oracle. Cheapest check: query repository visibility, remote SHA and
issue/milestone counts before reporting public completion. Safe recovery: complete
local review, preserve HOLD and report authentication/transport blockers. Completion
proof requires matching reviewed SHA/file set plus anonymous visibility and counts.
A README badge is not publication evidence; use publisher/DOI records.

## 2026-09-26 — Verify writes with independent readback
A completed API mutation is not its acceptance oracle. Read back exact titles, IDs,
labels, milestone assignments and issue contracts; compare remote blob hashes with
the reviewed tree and verify anonymous access and the CI head SHA. Nullable API
fields need value checks: an issue with `pull_request: null` is not a pull request.
An initial count assertion used field presence and excluded valid issues; read-only
inspection identified this, and reconciliation completed without duplicate writes.
Optional security flags returned successful mutation responses but remained disabled
on readback; retain that limitation instead of declaring every control enabled.

## Phase 1 — representation is not assurance
Pydantic constrains record shape; package checks constrain cross-record identity.
Pint proves dimensional compatibility, not factor applicability. PROV-O states
lineage, not source truth. RDF graph isomorphism checks meaning despite different
blank-node labels; byte snapshots would be the wrong oracle. Run the ten examples
and tests in [reproducibility](REPRODUCIBILITY.md). Explain why ordinary kg cannot
convert into kg CO2e, and why a correction keeps old result references unchanged.

Operating lesson: initial lint found style issues after domain tests passed; test
success is not all-checks success. Run native lint/format and all contract tests
separately before publication. No configuration rules were disabled to pass.

Documentation checker failure after installing dependencies came from scanning
vendored .venv README links, not broken project links. Exclude only local environment/
build artifacts and retain a negative test proving real project links still fail.
Cross-record checks now validate all edges before multi-hop dereference; reversing
record order and introducing a dangling facility confirms a validation error rather
than a KeyError. These are scope/isolation lessons, not research results.

## Phase 2 — Oracle verification is also necessary
Initial manually added subtotals were transcribed incorrectly while every line
answer was correct. Independent sum and cross-period reconciliation tests failed.
Re-summing the unchanged literal lines gave 3820, 3850, 4060 and deltas 30/210;
only the erroneous subtotal annotations were corrected. Never weaken a failing
constraint or regenerate expected answers from production output to obtain green.
Also: a valid partial fixture is not a standards-compliant complete inventory.
Runnable example: `uv run pytest tests/test_benchmark.py -q`. Explain why LB/MB
are alternatives, why organic growth differs from acquisition, and why a factor
change cannot alone establish real-world abatement.

## Phase 3 — identity, joins and provenance (2026-09-27)
A revision URI is an identity contract, not a merge hint: unequal content at one
URI must fail before union. A repeated row label across inventories is not a
revision edge. Reuse RDFLib/PROV-O instead of a parallel graph stack.

Observed failure → redundant type and generic-used joins expanded intermediate
SPARQL matches despite a small result set. Discriminating check → inspect RDFLib
algebra and compare a role-specific query on the same canonical graph. Recovery →
query role-specific edges, leave reference/type/PROV integrity to independently
asserted canonical tests, and bind target directly. Proof → all 45 exact answer
sets and subprocess timeouts pass. This is a query design lesson, not a speed
benchmark or permission to skip validation. [Runnable example](GRAPH.md).

Explain why a review uses a result rather than generates it; why a graph claim is
not source truth; and why an allowlisted template is safer than regex filtering
arbitrary SPARQL. Interrupted source writes are inspected and syntax-tested before
resuming; saved files are not evidence of a completed implementation.

## Independent-oracle lesson: arithmetic context and malformed inputs
A clean ten-case score missed ambient Decimal rounding in validation and missing
classification checks in snapshots. The cheapest discriminating test is a literal
3.6 MJ / 3.6 kWh conversion under precision=2 plus missing/invalid metadata, not
another run of the seed catalog. Exact Fraction arithmetic over bounded decimal
inputs and complete preflight findings fix the cause. Adversarial tests, original
fixtures and a full-suite run prove the encoded recovery; they do not prove
standards conformity. SHACL also needs direct raw-graph mutation tests: canonical
model validation can otherwise mask absent shape constraints.
