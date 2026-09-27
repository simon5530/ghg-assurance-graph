"""Portable, offline, closed-profile RO-Crate evidence directories.

Integrity is not authenticity: retain the returned manifest digest independently.
"""

import os
import re
import stat
from datetime import datetime
from hashlib import sha256
from importlib.metadata import version
from pathlib import Path

from rocrate.rocrate import ROCrate

from .adapters import _json
from .exporters import canonical_json, export_graph
from .models import EvidencePackage
from .serialization import GHG

CONTEXT = {
    "@vocab": "http://schema.org/",
    "File": "http://schema.org/MediaObject",
    "conformsTo": "http://purl.org/dc/terms/conformsTo",
    "sha256": "https://w3id.org/ro/terms/sha256",
}
PAYLOADS = {"package.json", "graph.ttl", "graph.jsonld", "schema.json", "ontology.json"}
FILES = PAYLOADS | {"ro-crate-metadata.json", "manifest.json"}
MAX_FILE_BYTES = 16_000_000
MAX_PACKAGE_BYTES = 48_000_000


def _read_payloads(root):
    # Anchor every lookup to opened directories, including ancestors. O_NOFOLLOW
    # closes the check/open symlink race; O_NONBLOCK prevents FIFO replacement hangs.
    absolute = Path(os.path.abspath(root))
    fd = os.open(absolute.anchor, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in absolute.parts[1:]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        with os.scandir(fd) as entries:
            names = set()
            for entry in entries:
                if entry.name not in FILES:
                    raise ValueError("unexpected package entry")
                names.add(entry.name)
        if names != FILES:
            raise ValueError("missing package entry")
        raw = {}
        total = 0
        for name in sorted(FILES):
            child = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
            with os.fdopen(child, "rb") as stream:
                info = os.fstat(stream.fileno())
                if not stat.S_ISREG(info.st_mode):
                    raise ValueError("nonregular package entry")
                limit = min(MAX_FILE_BYTES, MAX_PACKAGE_BYTES - total)
                if info.st_size > limit:
                    raise ValueError("evidence package size limit exceeded")
                data = stream.read(limit + 1)
                if len(data) > limit:
                    raise ValueError("evidence package size limit exceeded")
                total += len(data)
                raw[name] = data
        return raw
    finally:
        os.close(fd)


def _digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def _validate_provenance(created_at, command):
    if not isinstance(created_at, str):
        raise TypeError("explicit creation timestamp required")
    try:
        timestamp = datetime.fromisoformat(created_at)
    except ValueError:
        raise ValueError("invalid creation timestamp") from None
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("timezone required")
    if (
        not isinstance(command, (list, tuple))
        or not command
        or any(not isinstance(arg, str) or not arg or "\x00" in arg for arg in command)
    ):
        raise ValueError("record the nonempty command argument vector")


def _metadata(payloads, created_at):
    # The maintained library owns RO-Crate entity/root/descriptor construction.
    crate = ROCrate(version="1.2")
    crate.root_dataset["datePublished"] = created_at
    crate.root_dataset["name"] = "Experimental GHG evidence package"
    crate.root_dataset["description"] = "Evidence lineage, not an assurance opinion"
    crate.root_dataset["license"] = "License statements are recorded per evidence artifact"
    for name, data in sorted(payloads.items()):
        crate.add_file(
            dest_path=name, properties={"sha256": _digest(data), "contentSize": str(len(data))}
        )
    metadata = crate.metadata.generate()
    # Inline the small explicit profile: no JSON-LD loader needs a network context.
    metadata["@context"] = CONTEXT
    metadata["@graph"].sort(key=lambda entity: entity["@id"])
    return canonical_json(metadata).encode()


def _payloads(package):
    ontology = {
        "id": str(GHG),
        "version": "0.1",
        "status": "experimental",
        "description": "Project vocabulary; no ISO normative content",
        "schema_version": package.schema_version,
    }
    return {
        "package.json": canonical_json(package).encode(),
        "graph.ttl": export_graph(package, "turtle").encode(),
        "graph.jsonld": export_graph(package, "json-ld").encode(),
        "schema.json": canonical_json(EvidencePackage.model_json_schema()).encode(),
        "ontology.json": canonical_json(ontology).encode(),
    }


def _identities(package):
    return {
        kind: sorted(record.id for record in package.records if record.kind == kind)
        for kind in ("EmissionFactor", "CalculationMethod", "GWPSet", "EvidenceArtifact")
    }


def create_package(
    package: EvidencePackage,
    destination: str | Path,
    *,
    created_at: str,
    command: list[str] | tuple[str, ...],
    data_version: str = "unspecified",
) -> dict:
    """Create a new directory. Caller supplies reproducible provenance; no source copying."""
    package = EvidencePackage.model_validate(package.model_dump())
    _validate_provenance(created_at, command)
    if not isinstance(data_version, str) or not data_version.strip():
        raise ValueError("data version required")
    destination = Path(destination)
    if any(p.is_symlink() for p in (destination, *destination.parents)):
        raise ValueError("symlink path")
    payloads = _payloads(package)
    payloads["ro-crate-metadata.json"] = _metadata(payloads, created_at)
    manifest = {
        "format": "ghgag-evidence-1",
        "created_at": created_at,
        "command": list(command),
        "software": {
            name: version(name) for name in ("ghg-assurance-graph", "rocrate", "rdflib", "pydantic")
        },
        "schema_version": package.schema_version,
        "data_version": data_version,
        "ontology": str(GHG),
        "identities": _identities(package),
        "files": {
            name: {"sha256": _digest(data), "bytes": len(data)}
            for name, data in sorted(payloads.items())
        },
    }
    payloads["manifest.json"] = canonical_json(manifest).encode()
    destination.mkdir(parents=True, exist_ok=False)
    for name, data in payloads.items():
        (destination / name).write_bytes(data)
    return verify_package(destination)


def _load(data):
    return _json(data)


def _no_context(value):
    if isinstance(value, dict):
        if "@context" in value or "@import" in value:
            raise ValueError("unexpected JSON-LD context")
        for item in value.values():
            _no_context(item)
    elif isinstance(value, list):
        for item in value:
            _no_context(item)


def verify_package(directory: str | Path, *, expected_manifest_sha256: str | None = None) -> dict:
    """Verify closed file set, hashes, model and derived exports entirely offline.

    Never follows paths supplied by a manifest or parses attacker-controlled RDF.
    Optional external manifest digest authenticates only against that trusted digest.
    """
    root = Path(directory)
    try:
        if any(p.is_symlink() for p in (root, *root.parents)) or not root.is_dir():
            raise ValueError("not a regular package directory")
        raw = _read_payloads(root)
        manifest_digest = _digest(raw["manifest.json"])
        if expected_manifest_sha256 is not None and manifest_digest != expected_manifest_sha256:
            raise ValueError("manifest digest mismatch")
        manifest = _load(raw["manifest.json"])
        expected_keys = {
            "format",
            "created_at",
            "command",
            "software",
            "schema_version",
            "data_version",
            "ontology",
            "identities",
            "files",
        }
        if (
            not isinstance(manifest, dict)
            or set(manifest) != expected_keys
            or manifest["format"] != "ghgag-evidence-1"
        ):
            raise ValueError("unsupported manifest")
        _validate_provenance(manifest["created_at"], manifest["command"])
        if not isinstance(manifest["data_version"], str) or not manifest["data_version"].strip():
            raise ValueError("invalid data version")
        software = manifest["software"]
        if set(software) != {"ghg-assurance-graph", "rocrate", "rdflib", "pydantic"} or any(
            not isinstance(v, str) or not v for v in software.values()
        ):
            raise ValueError("invalid software provenance")
        if set(manifest["files"]) != FILES - {"manifest.json"}:
            raise ValueError("unsafe or incomplete manifest paths")
        for name, entry in manifest["files"].items():
            if set(entry) != {"sha256", "bytes"} or type(entry["bytes"]) is not int:
                raise ValueError("invalid checksum entry")
            if not re.fullmatch(r"[a-f0-9]{64}", entry["sha256"]):
                raise ValueError("invalid digest")
            if entry != {"sha256": _digest(raw[name]), "bytes": len(raw[name])}:
                raise ValueError("payload checksum mismatch")
        package = EvidencePackage.model_validate(_load(raw["package.json"]))
        if (
            manifest["schema_version"] != package.schema_version
            or manifest["ontology"] != str(GHG)
            or manifest["identities"] != _identities(package)
        ):
            raise ValueError("manifest model mismatch")
        _no_context(_load(raw["graph.jsonld"]))
        metadata = _load(raw["ro-crate-metadata.json"])
        if metadata.get("@context") != CONTEXT:
            raise ValueError("nonlocal or unsupported RO-Crate context")
        _no_context(metadata.get("@graph"))
        expected = _payloads(package)
        if any(raw[name] != data for name, data in expected.items()):
            raise ValueError("noncanonical or inconsistent payload")
        if raw["ro-crate-metadata.json"] != _metadata(expected, manifest["created_at"]):
            raise ValueError("inconsistent RO-Crate metadata")
        if raw["manifest.json"] != canonical_json(manifest).encode():
            raise ValueError("noncanonical manifest")
        return {
            "valid": True,
            "manifest_sha256": manifest_digest,
            "record_count": len(package.records),
            "manifest": manifest,
        }
    except (OSError, TypeError, KeyError, AttributeError, RecursionError, UnicodeError) as exc:
        raise ValueError("invalid evidence package") from exc
