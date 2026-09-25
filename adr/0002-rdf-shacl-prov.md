# ADR 0002: RDF, SHACL, and PROV-O

Status: proposed; implementation and final library selection deferred.

Context: evidence relationships and inspectable constraints need portable semantics.
Decision proposed: RDF/PROV-O representation with SHACL validation; evaluate RDFLib
and pySHACL before committing to versions or dependencies.

Alternatives: relational tables with foreign keys; JSON Schema plus explicit lineage;
property graphs. Compare usability, interoperability, constraint expressiveness,
performance, and reproducibility on the same synthetic cases.

Consequences: graph complexity and ontology governance are real costs. SHACL
conformance is not financial or GHG assurance. Record missing-evidence semantics
and validation profiles. No RDF or SHACL artifact exists in Phase 0.
