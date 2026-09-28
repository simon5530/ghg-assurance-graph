# Bounded domain review — owner questionnaire

Prepared 2026-09-28. **Status: unanswered; no human/domain or independent assurance review claimed.** This is a method-design review aid, not an invented mandatory Gate A/Phase 11 sign-off. Human authors remain responsible for benchmark ground truth and manuscript claims. Record actual answers, reviewer role/date, evidence and resulting changes; never prefill approval.

## Review materials and assumptions

Read [CarbonDiff](CARBONDIFF.md), [validation](VALIDATION.md), [evidence packaging](EVIDENCE.md) and the same-case [comparison](RELATED_WORK.md). ACME is selected-source synthetic data, not a complete organizational inventory. Factors/GWP labels are invented test inputs, not production datasets. Standards coverage and licensed-clause limits remain in [standards alignment](STANDARDS_ALIGNMENT.md).

For each question answer **accept for research / revise / unsure**, give a reason and a public-safe counterexample. Do not upload client evidence or licensed standards text.

1. **Boundary:** Does selected-source ACME support a meaningful assurance/change example without implying inventory completeness? Identify one excluded applicable source and how its exclusion should be disclosed. Confirm location-based electricity and market-based electricity are alternatives, never additive; the current raw-snapshot profile rejects market-based cases rather than inventing zero.
2. **Interaction convention:** Electricity 1,000 kWh×0.5=500 becomes 800×0.6=480 kgCO2e. Activity-first gives −100/+80; factor-first gives +100/−120. Is the disclosed activity-first ordering adequate for this software demonstration? What sensitivity display is needed? Neither bridge alone means 20 kg of operational decarbonization.
3. **Correction versus activity:** A corrected invoice changes fleet quantity without any physical operational change. What evidence distinguishes CORRECTION from a bare ACTIVITY_CHANGE operand? Current API accepts a caller declaration covering all changed fields; it does not authenticate that statement. Is that limitation clear enough?
4. **Method transition:** For the same purchased lot, EEIO spend estimate 100 currency units×2=200 kgCO2e changes to supplier PCF 50 kg product×3=150. Treat −50 as a method/data difference, not an efficiency improvement. Which declared unit, lifecycle boundary, allocation and reference-period fields are necessary before comparison? No unsupported currency/unit conversion or silent boundary harmonization is permitted.
5. **GWP and allocation:** A precharacterized CO2e factor is multiplied once, never by GWP again. For q=100, f=2, allocation 0.5→0.25, results 100→50; current arithmetic gives −50 allocation. If allocation method changes too, it stays UNKNOWN unless one whole-row declaration is supplied. Are these conservative rules acceptable? Identify a case needing multiple semantic drivers, currently unsupported.
6. **Unknown exposure:** Existing unannotated next-year benchmark has signed UNKNOWN +300 and absolute UNKNOWN 500 kgCO2e (including −50 allocation, −50 method and +400 GWP rows); total inventory delta +210. Is reporting both signed residual and absolute exposure sufficient to prevent cancellation from looking like certainty?
7. **Executable checks:** Missing factor source, duplicate record, invalid unit or unreviewed override should yield explicit findings. Which check is domain-required versus project policy? Supply an authoritative reference or mark unresolved; a shape passing cannot establish authentic evidence or a complete assurance opinion.
8. **Portable evidence:** Current crate contains typed records, RDF and integrity/version metadata, but external invoice artifacts are only cited, not bundled. Would a reviewer need actual documents, access controls or signatures? Distinguish inspectable/recomputable software records from source authenticity and independent audit evidence.
9. **Practical differentiation:** Against CarbonLedger fixed-activity restatement, Arrhen report lineage and TEC + SHACL + RO-Crate composition, which joined output saves real review work? Give a concrete task; “graph looks useful” is not adoption evidence. “No practical benefit” is a valid answer and may motivate narrowing/upstream work.

## Answer record (not approval)

- Reviewer and role: not supplied.
- Date and artifacts/version reviewed: not supplied.
- Answers/counterexamples: pending.
- Changes requested and verification: pending.
- Independent review or assurance opinion: **none**.

Owner review can improve examples and interpretation. It cannot be relabeled external validation, empirical accuracy, regulatory compliance or an independent assurance engagement. If answers expose material method defects, narrow claims and repair/test them regardless of gate labels.
