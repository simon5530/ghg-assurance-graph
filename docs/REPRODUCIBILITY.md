# Phase 1 reproducibility

Python 3.12.14 is pinned in .python-version; uv.lock pins transitive dependencies.
Install uv through its documented trusted distribution, then from the repository:

~~~sh
uv sync --locked
uv run pytest -q
uv run ruff check src/ghg_assurance_graph tests examples
uv run ruff format --check src/ghg_assurance_graph tests examples
uv run python examples/hand_authored.py
uv run python scripts/check_docs.py
uv run python scripts/test_check_docs.py
~~~

The core needs no credential, cloud model, confidential file or service. Initial
package installation needs network access or a populated cache. Generated examples
are ignored artifacts; no benchmark command exists. A same-machine isolated clean
copy is a reproducibility check, not a fresh-machine scientific reproduction.
See [publication audit](PUBLICATION_AUDIT.md) for observed versions/results and limits.

JSON Schema is generated from EvidencePackage.model_json_schema(). Read JSON through
EvidencePackage.model_validate_json or serialization.from_json. to_rdf supports only
turtle and json-ld. RDF roundtrip means graph isomorphism, not arbitrary domain import.
No calculation, benchmark evaluation, SHACL or CarbonDiff results are reproduced.
