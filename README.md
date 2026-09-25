# GHG Assurance Graph

**v0.0.1 — Research prototype / pre-alpha. Phase 0 documentation scaffold only.**

A proposed research toolkit for organizational greenhouse-gas evidence provenance,
inspectable assurance constraints, deterministic inventory change explanations, and
reproducible evidence packages. This is **not another emissions calculator** and is
not an assurance opinion, certification, or regulatory compliance service.

## Current status

Implemented: project documentation, paper planning templates, a machine-readable
roadmap, and a standard-library documentation checker with its CI workflow.

Not implemented: canonical domain schema, RDF graph builder, SHACL shapes,
CarbonDiff, RO-Crate export, benchmark generator, adapters, or agent tools.
No domain tests, measured benchmark results, release archive, DOI, or journal
acceptance are claimed. CI configuration is present; a hosted CI run is not yet evidence.

**Research gate: HOLD.** [Decision and conditions](docs/GATE_A.md).
[Related-work evidence](docs/RELATED_WORK.md) supports only a narrow gap hypothesis.
Publication and GitHub provisioning remain blocked/unverified; see the
[acceptance record](docs/PHASE0_ACCEPTANCE.md) and [audit](docs/PUBLICATION_AUDIT.md).
Even a positive gate requires an explicit decision before implementation begins.

## Check the scaffold

Requires Python 3.9+; no third-party dependencies:

```sh
python3 scripts/check_docs.py
python3 scripts/test_check_docs.py
```

Packaging, Python dependency choices and a lockfile are deferred to Phase 1 because
there is no domain software to package yet. Do not install an empty package.

## Start here

- [Problem and research questions](docs/PROBLEM.md)
- [Requirements and phase gate](docs/REQUIREMENTS.md)
- [Architecture](docs/ARCHITECTURE.md) and [domain model](docs/DOMAIN_MODEL.md)
- [Ontology](docs/ONTOLOGY.md), [CarbonDiff](docs/CARBONDIFF.md), [validation](docs/VALIDATION.md)
- [Reproducibility](docs/REPRODUCIBILITY.md) and [publication strategy](docs/PUBLICATION_STRATEGY.md)
- [AI boundary](docs/AI_BOUNDARY.md) and [AI usage log](docs/AI_USAGE_LOG.md)
- [Roadmap manifest](.github/roadmap.json)
- [SoftwareX outline](paper/softwarex/OUTLINE.md), [JOSS readiness](paper/joss/READINESS.md)
- [Contribution guide](CONTRIBUTING.md), [governance](GOVERNANCE.md), [security](SECURITY.md)
- [Changelog](CHANGELOG.md), [citation metadata](CITATION.cff), [MIT license](LICENSE)

Use synthetic data only in public examples. Research outputs require domain review.
