# Carbondiff

Status: Phase 0 planning; domain features are not implemented.

## Planned deterministic comparison
Compare two explicit inventory versions. Proposed categories: activity change,
factor change, methodology change, boundary change, correction, and added/removed
records. Classification rules and overlap precedence are not yet defined.

Match stable identities first; report ambiguous/unmatched records. Never silently
use an LLM to decide identity, reason, or numeric attribution. Specify decimal
precision, units, GWP basis, missingness, and rounding before calculations.

For multiplicative inputs, cross-terms require an explicit ordered or symmetric
attribution convention; a narrative label alone is not a causal explanation.
Require sum(attributions) + explicit residual = total delta under a documented
tolerance. Boundary/method changes may require comparable restatement rather than
naive subtraction. Test zero, negative, missing, duplicate, and reordered inputs.

No algorithm, numeric attribution, or reconciliation test is implemented.
