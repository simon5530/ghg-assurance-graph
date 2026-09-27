# Portable evidence packages (Phase 6)

The Python API creates a deterministic, closed-profile RO-Crate 1.2 **directory**.
It reuses maintained `rocrate` Python entities, root datasets, file registration,
and metadata generation; it does not imitate the library behind a label.
The supported dependency is `rocrate>=0.15.1,<0.16`.

## API

```python
from ghg_assurance_graph.evidence import create_package, verify_package

report = create_package(
    package, "output/evidence",
    created_at="2026-01-01T00:00:00Z",
    command=["ghgag", "evidence", "create", "..."],
    data_version="synthetic-benchmark-v1",
)
verified = verify_package("output/evidence",
                          expected_manifest_sha256=report["manifest_sha256"])
```

The destination must not exist. Timestamp and command are explicit recorded
provenance, never generated from the current clock or executed. Avoid secrets
in command arguments. All input models are revalidated.

## Closed manifest

Exactly seven regular files are permitted:

- `package.json`: complete typed records, sorted by revision ID, canonical JSON.
- `graph.ttl`: deterministic Turtle using sorted triple statements.
- `graph.jsonld`: expanded JSON-LD, without an external context.
- `schema.json`: complete local Pydantic JSON Schema.
- `ontology.json`: experimental vocabulary ID/version descriptor (not an imported ontology).
- `ro-crate-metadata.json`: library-generated metadata with an inline context.
- `manifest.json`: SHA-256 and byte counts of every other file, software versions
  (application, RO-Crate, RDFLib, Pydantic), schema/data/ontology versions,
  factor/method/GWP/evidence revision IDs, fixed creation timestamp and command.

The manifest does not hash itself; the returned external manifest SHA-256 closes
that integrity boundary. Preserve that digest independently. Canonical JSON is
this project's sorted compact UTF-8 encoding, **not RFC 8785**. Determinism assumes
the same recorded provenance, dependency versions, schema, and input records;
input record order and RDF blank-node labels do not affect exports.

## Offline verification and limits

Verification requires only the copied directory and installed application, not
its source dataset, repository checkout, original path, network, or source files.
It checks file membership, hashes, provenance shape, domain validation, identities,
canonical exports, schema and metadata consistency. It never parses untrusted RDF
or follows manifest paths; it regenerates and compares expected payloads instead.
Unknown manifest keys, extra/missing files, directories, symbolic links (including
path ancestors), absolute/traversal manifest paths, duplicate JSON keys and remote
or nested JSON-LD contexts fail closed. URLs inside evidence citations are inert
literals and are not dereferenced. Tests block socket connections.

This is a strict application profile, not a verifier for arbitrary third-party
RO-Crates. Verification may reject crates made with incompatible future schemas or
serialization dependencies. It assumes a quiescent local directory, not an attacker
racing filesystem changes. No archive extraction is implemented. Creation refuses
overwrite, but an interrupted write may leave a partial directory that verification
rejects; remove it deliberately before retrying.

Hashes are not signatures. An attacker can rewrite the whole package and its
manifest consistently; without an independently trusted digest that is not
detectable. Evidence citations and optional artifact checksums are retained, but
external artifacts are not fetched or claimed to be bundled. No ISO licensed text,
normative data, assurance opinion, or compliance certification is included.

## Verification

```sh
python -m pytest -q tests/test_evidence.py tests/test_exporters.py
```

Tests cover relocated verification, RO-Crate library loading, deterministic bytes,
RDF roundtrip isomorphism, recomputed-checksum semantic tampering, remote contexts,
missing/extra files, symlinks, traversal and external manifest digest mismatch.
