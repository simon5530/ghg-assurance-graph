# Phase 5 CarbonDiff acceptance contract

Current status note (2026-09-28): this is a historical phase contract. Its dated authorization/HOLD restrictions are superseded by [current Gate A](GATE_A.md) and [original-phase acceptance](ROADMAP_ACCEPTANCE.md); technical invariants remain unless explicitly superseded.
Experimental deterministic comparison, not causal inference or assurance. ISO
licensed-clause review and Gate A status are unchanged.

1. Compare two explicit ACME raw snapshots using supplied namespace, version and
   stable row IDs. Never match by position, labels, suffixes or fuzzy similarity.
   Reject duplicate IDs, mixed snapshot evidence, namespace mismatch and reused
   version IDs. Classification context changes under one ID fail closed.
2. Validate inputs before arithmetic. Only selected-source fossil/nonbiogenic
   precharacterized CO2e, location-based Scope 2 and benchmark unit conversions
   are supported. Never sum LB and MB; never multiply precharacterized factors
   by GWP again. Raw-gas characterization remains unsupported.
3. All original ChangeEvent causes remain expressible. Mechanical decomposition
   uses activity first, factor second, allocation last. A changed GWP basis alone
   does not prove that its entire factor delta is GWP-caused. Ambiguous semantic
   changes become UNKNOWN unless explicit scoped explanatory evidence is given.
4. Semantic declarations are caller-supplied assertions with nonempty evidence,
   exact before/after snapshot binding, stable entity and observed changed fields.
   They are not inferred from entity names, dates or evaluation truth. No supplied
   attribution amount is accepted. Overlapping declarations fail closed.
5. Finite bounded Decimal operands, exact arithmetic independent of ambient
   Decimal precision; no rounding tolerance. Signed components plus signed UNKNOWN
   residual equal total delta exactly. Also report absolute unknown exposure to
   avoid cancellation concealing unsupported changes.
6. Added/removed records are explicit match statuses, not automatic acquisitions
   or corrections; without evidence their signed delta is UNKNOWN. Metadata-only
   changes remain visible with zero amount. Empty inventories are not zero.
7. Tests consume independent hand-authored expected changes and amounts, never
   production code. Quantify labels, component amounts and residual reconciliation;
   disclose public fixture/annotation limitations. Test negative/zero deltas, order,
   duplicates, wrong joins, unsupported changes, decimal precision and double GWP.

Scope: bounded Python API and integrated CLI; no general graph matcher, automatic
restatement policy, inventory completeness or decarbonization claims.
