# Reproducibility

Status: Phase 0 planning; domain features are not implemented.

## Current reproducible operation
Use Python 3.9+ and run `python3 scripts/check_docs.py` from a clean checkout.
No network, third-party package, dataset, private configuration, or credentials are
required. This reproduces documentation checks, not scientific results.

## Deferred to implementation
Choose and pin dependencies with a lockfile once domain code exists. Record OS,
Python, library, ontology, benchmark, input digest, configuration, and commit versions.
Plan an offline replay path and compare semantic outputs with documented tolerances.
RO-Crate export and fresh-machine scientific reproduction are not implemented.
Do not commit generated private data or call a same-machine clone a fresh-machine test.

The checker also has six standard-library tests: `python3 scripts/test_check_docs.py`.
They exercise the valid tree, missing required file, broken link, escaping link,
dependency cycle and missing issue contract. They are documentation-oracle tests,
not GHG domain tests.
