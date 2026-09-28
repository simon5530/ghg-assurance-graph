# ADR 0002: RDF, SHACL, and PROV-O

Status: accepted for bounded implementation, reviewed against executed code and tests 2026-09-28. Human/domain endorsement is not implied.

Context: evidence relationships and inspectable constraints need portable semantics. Decision: reuse RDFLib/PROV-O representation with pySHACL Core rather than invent provenance syntax or a validation engine. Locked versions and licenses are in docs/DEPENDENCIES.md; MIT original code does not relicense dependencies.

Alternatives: relational foreign keys provide efficient local integrity but do not by themselves supply interoperable PROV identities and graph exports; JSON Schema checks closed records but not the complete graph relationship contract; property graphs add runtime/storage dependencies and need their own exchange mapping. For current small offline fixtures, RDFLib + packaged queries avoids a graph server. No benchmark establishes performance superiority over these alternatives.

Implementation evidence: tests/test_graph.py checks identity collisions, reference integrity and five queries; tests/test_validation.py executes real packaged SHACL shapes against clean and defective fixtures. Closed Pydantic validation complements, rather than replaces, graph checks. No remote contexts, SERVICE queries, JavaScript, inferred standards opinion or automatic evidence download.

Missingness: calculated-profile missing required provenance fails closed. Public totals use reported-disclosure/1, never fabricated calculation closure; unavailable checks remain not_assessable. SHACL conformance only means selected encoded constraints hold, not source truth, full accounting conformity or assurance.

Consequences: ontology governance and graph complexity are real costs. Scope remains bounded in-memory snapshots; broader scale, alternative query engines and PECO/ECFO alignment require evaluation. Production guarantees, authenticated review and universal ontology interoperability are not established.
