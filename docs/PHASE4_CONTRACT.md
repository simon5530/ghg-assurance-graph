# Phase 4 validation acceptance contract

Current status note (2026-09-28): this is a historical phase contract. Its dated authorization/HOLD restrictions are superseded by [current Gate A](GATE_A.md) and [original-phase acceptance](ROADMAP_ACCEPTANCE.md); technical invariants remain unless explicitly superseded.
Status: engineering implementation; **Gate A remains HOLD**. Owner authorization
permits engineering, not standards-conformity claims. Licensed ISO clause review
and practitioner review are separate, unresolved gates; no ISO clauses are invented here.

## Workflow and acceptance

1. Input: local canonical EvidencePackage/in-memory RDF, or ACME raw row mappings.
   Detector never receives case filenames, truth labels, mutation metadata or network data.
2. Canonical packages retain existing Pydantic integrity validation. Packaged Turtle
   Core SHACL runs through pySHACL with no caller shapes, arbitrary SPARQL, imports,
   JS, advanced rules or inference. It validates required typed single-valued
   provenance/context edges and evidence citation/license presence.
3. Raw domain detector independently checks published ACME policy and Decimal
   arithmetic, not benchmark.amount/preflight. It reports all applicable rules.
4. Findings have stable sorted ordering and content-derived identifiers for stable
   entity IDs. No input is repaired or silently replaced with zero.
5. Separate evaluator compares exact (case, entity, rule, severity) sets against
   hand-authored benchmark/ground_truth/expected_findings.json. Report TP/FP/FN,
   precision, recall and F1; test the evaluator with deliberate FP/FN.
6. Acceptance oracle: 3 clean snapshots produce zero findings; all 10 seeded
   defects match exactly; development and public holdout scored separately;
   provenance removal/wrong class/dangling/multiple values fail actual SHACL;
   missing fields, conflicting duplicate rows and numeric adversaries fail.

## Rule coverage

- reported amount mismatch: independent activity × unit scale × factor × share;
- duplicate activity: repeated raw identity, even conflicting content;
- factor provenance: exact synthetic factor citation policy (not merely nonempty);
- factor applicability: year, facility and geography policy;
- unsupported PCF boundary: explicit supported cradle-to-gate exclusion contract;
- manual override not reviewed: fixture simulated-review status;
- no double GWP: precharacterized factors cannot request characterization again;
- market-based evidence unavailable: no verified contractual evidence in this dataset;
- unsupported unit conversion: explicit physical/currency vocabulary and conversion allowlist;
- separate biogenic/removal/offset: prohibited netting into selected inventory arithmetic.

Additional checks cover finite nonnegative quantities, share range, classification,
activity evidence row binding, accounting basis and method/allocation vocabulary.
These are project/benchmark rules, not a claim of exhaustive GHG or ISO requirements.

## Limits and failure behavior

SHACL is a structural subset, not a replacement for the canonical model. An empty
or unrelated RDF graph has no target nodes and vacuously conforms; it is not a
complete inventory. Arbitrary raw RDF numeric/domain validation is not supplied.
RDF set semantics cannot identify repeated identical triples: detect duplicate
raw records before graph construction. Valid-class but semantically wrong evidence
links require source-content/identity review beyond structural SHACL.

The public holdout is not unseen data. Perfect scores establish only these ten
known fixtures. The same developer inspected public truth; no scientific blind
validation is claimed. No external source authenticity, completeness, statistical
uncertainty, market-instrument eligibility or assurance conclusion is established.
