# Ontology

Status: Phase 0 planning; domain features are not implemented.

## Proposed reuse
Use RDF for interoperable graph representation, PROV-O for entities/activities/agents,
and SHACL for explicit graph constraints. Reuse existing vocabularies after a
licensing and semantic-fit review; do not mint a competing ontology unnecessarily.

Candidate mappings: evidence and inventory versions → prov:Entity;
calculation/import/review → prov:Activity; accountable organizations/reviewers →
prov:Agent. These are proposals, not approved ontology axioms.

Define namespace governance, vocabulary versions, identifier policy, units, temporal
semantics, validation profiles, and migrations before publishing any ontology.
RDFLib and pySHACL are candidate implementations, not installed dependencies.
PROV-O provenance is not itself proof that evidence is true.
