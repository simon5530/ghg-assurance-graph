# GHG Assurance Graph

**v0.1.0a1 — Research prototype / pre-alpha. Experimental Phase 1 model.**

A proposed research toolkit for organizational greenhouse-gas evidence provenance,
inspectable assurance constraints, deterministic inventory change explanations, and
reproducible evidence packages. This is **not another emissions calculator** and is
not an assurance opinion, certification, or regulatory compliance service.

## Current status

Implemented: 17 typed canonical records, version/reference integrity, bounded Pint
units, first RDF/PROV mapping, JSON/JSON-LD/Turtle serialization, ten hand-authored
examples, schema/domain tests, locked packaging and CI.

Not implemented: full provenance query workflow, SHACL assurance, CarbonDiff,
RO-Crate, generated benchmark, adapters or AI. No practitioner validation, measured
benchmark evaluation, release archive, DOI or journal acceptance is claimed.

**Research gate: HOLD.** [Decision and conditions](docs/GATE_A.md).
[Related-work evidence](docs/RELATED_WORK.md) supports only a narrow gap hypothesis.
The public repository, 11 milestones, 18 roadmap labels and 30 issues are verified; see the
[acceptance record](docs/PHASE0_ACCEPTANCE.md) and [audit](docs/PUBLICATION_AUDIT.md).
The owner authorized a [bounded Phase 1 exception](docs/PHASE1_CONTRACT.md) on
2026-09-26. This does not change HOLD to GO or authorize Phase 2.

## Reproduce Phase 1

Python 3.12.14 and uv; no API key or cloud model:

```sh
uv sync --locked
uv run pytest -q
uv run python examples/hand_authored.py
uv run python scripts/check_docs.py
uv run python scripts/test_check_docs.py
```

See [ten examples](examples/README.md), [reference brief](docs/REFERENCE_BRIEF.md),
[dependency licenses](docs/DEPENDENCIES.md) and [reproducibility](docs/REPRODUCIBILITY.md).

## Start here

- [Problem and research questions](docs/PROBLEM.md)
- [Requirements and phase gate](docs/REQUIREMENTS.md)
- [Architecture](docs/ARCHITECTURE.md) and [domain model](docs/DOMAIN_MODEL.md)
- [Ontology](docs/ONTOLOGY.md), [CarbonDiff](docs/CARBONDIFF.md), [validation](docs/VALIDATION.md)
- [Reproducibility](docs/REPRODUCIBILITY.md) and [publication strategy](docs/PUBLICATION_STRATEGY.md)
- [AI boundary](docs/AI_BOUNDARY.md) and [AI usage log](docs/AI_USAGE_LOG.md)
- [Roadmap manifest](.github/roadmap.json)
- [SoftwareX outline](paper/softwarex/OUTLINE.md), [Future methods paper](paper/methods/FUTURE_PAPER.md)
- [Contribution guide](CONTRIBUTING.md), [governance](GOVERNANCE.md), [security](SECURITY.md)
- [Changelog](CHANGELOG.md), [citation metadata](CITATION.cff), [MIT license](LICENSE)

Use synthetic data only in public examples. Research outputs require domain review.
