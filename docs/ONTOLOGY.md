# Experimental ontology namespace 0.1

Namespace: `https://simon5530.github.io/ghg-assurance-graph/ns/0.1/`.
This is an identifier namespace controlled through this repository, not a claim of
an available dereferenceable ontology service or W3C endorsement. Breaking semantic
changes mint a new version namespace; no equivalence with PECO is asserted yet.
[Serializer](../src/ghg_assurance_graph/serialization.py) is the first graph mapping.

- Organization → prov:Agent (includes organizational reviewer identities).
- CalculationRun and ReviewDecision → prov:Activity.
- All other domain records → prov:Entity, including the supplied ChangeEvent record
  describing a change rather than asserting an executed causal activity.
- EmissionResult.calculation → prov:wasGeneratedBy.
- Record.supersedes → prov:wasRevisionOf.
- ReviewDecision.reviewer → prov:wasAssociatedWith.
- ReviewDecision.target additionally → prov:used (review did not generate result).
- Evidence links → prov:wasDerivedFrom.
- CalculationRun inputs activity/factor/method/GWP/boundary → prov:used, in addition
  to role-specific domain properties preserving which input served which role.

Other fields use the namespace and exact model field name: organization, facility,
period, boundary, source, inventory, quality, review, target, before/after and scalar
metadata. This avoids claiming a domain relation is equivalent to a PROV relation
when semantics differ. Numeric quantities use blank nodes with value/unit properties;
record revisions are URIs. Schema version is emitted on each record. Literal dates
and timestamps currently preserve ISO lexical strings, not inferred XSD temporal
semantics. Unit literals preserve the bounded Pint vocabulary, not QUDT alignment.

JSON domain roundtrip is supported. JSON-LD/Turtle semantic graph roundtrip is tested
by RDF graph isomorphism, not byte equality or domain import. No remote JSON-LD
context is fetched. Arbitrary untrusted RDF import, SHACL, RDFS/OWL inference
and general RDF assurance validation remain later work. Phase 3 extends this
serializer with a [collision-checked builder and five queries](GRAPH.md).
PROV-O relationships neither authenticate evidence nor prove its truth.
