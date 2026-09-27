"""External import contracts; values and provenance remain author-supplied claims."""

import csv
import io
import json
from pathlib import Path

import pytest

from ghg_assurance_graph.adapters import (
    CSV_COLUMNS,
    ExternalResult,
    import_external_csv,
    import_external_json,
)
from ghg_assurance_graph.graph import build_graph, query_graph

ROOT = Path(__file__).parents[1]


@pytest.fixture
def document():
    return json.loads((ROOT / "examples/external_result.json").read_text())


def csv_text(document):
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=CSV_COLUMNS)
    writer.writeheader()
    writer.writerow(
        {k: json.dumps(v) if isinstance(v, (dict, list)) else v for k, v in document.items()}
    )
    return out.getvalue()


def test_json_csv_equivalence_and_lineage(document):
    package = import_external_json(json.dumps(document))
    assert package == import_external_csv(csv_text(document))
    assert package == ExternalResult.model_validate(document).to_package()
    (row,) = query_graph(build_graph([package]), "explain_result", document["result"]["id"])
    assert row["value"] == "50.0"
    assert row["unit"] == "kg_CO2e"
    assert row["factor"] == document["calculation"]["factor"]
    assert row["method"] == document["calculation"]["method"]
    assert row["factorEvidence"] == "urn:ghgag:electricity-location-evidence:v1"
    assert next(r for r in package.records if r.kind == "CalculationMethod").method_type == (
        "external-result"
    )
    assert next(r for r in package.records if r.kind == "CalculationRun").software == (
        "synthetic-external-export/1"
    )


def test_does_not_recalculate_or_invent_digest(document):
    document["result"]["quantity"]["value"] = 123.25
    package = import_external_json(json.dumps(document))
    assert next(r for r in package.records if r.kind == "EmissionResult").quantity.value == 123.25
    assert next(r for r in package.records if r.kind == "EvidenceArtifact").sha256 is None


@pytest.mark.parametrize(
    "mutation",
    [
        "unknown",
        "nested-unknown",
        "missing-provenance",
        "missing-evidence",
        "missing-factor",
        "unit",
        "physical-unit",
        "boundary",
        "method",
        "origin",
        "software",
        "negative",
        "second-result",
        "unsupported-boundary",
        "factor-source",
        "factor-unit",
    ],
)
def test_reject_incomplete_or_unsupported(document, mutation):
    by_kind = {r["kind"]: r for r in document["provenance"]}
    if mutation == "unknown":
        document["guess"] = "no"
    elif mutation == "nested-unknown":
        document["result"]["guess"] = "no"
    elif mutation == "missing-provenance":
        del document["provenance"]
    elif mutation in ("missing-evidence", "missing-factor"):
        kind = "EvidenceArtifact" if mutation == "missing-evidence" else "EmissionFactor"
        document["provenance"].remove(by_kind[kind])
    elif mutation in ("unit", "physical-unit"):
        document["result"]["quantity"]["unit"] = "tCO2e" if mutation == "unit" else "kg"
    elif mutation == "boundary":
        document["calculation"]["boundary"] = "urn:ghgag:absent:v1"
    elif mutation == "method":
        by_kind["CalculationMethod"]["method_type"] = "activity-based"
    elif mutation == "origin":
        del document["origin"]
    elif mutation == "software":
        del document["calculation"]["software"]
    elif mutation == "negative":
        document["result"]["quantity"]["value"] = -1
    elif mutation == "second-result":
        document["provenance"].append(document["result"])
    elif mutation == "unsupported-boundary":
        by_kind["BoundaryDefinition"]["consolidation"] = "cradle-to-grave"
    elif mutation == "factor-source":
        del by_kind["EmissionFactor"]["evidence"]
    else:
        by_kind["EmissionFactor"]["denominator"] = "liter"
    with pytest.raises(ValueError):
        import_external_json(json.dumps(document))
    with pytest.raises(ValueError):
        import_external_csv(csv_text(document))


@pytest.mark.parametrize(
    "text",
    [
        "{}",
        '{"origin":"a","origin":"b"}',
        "https://example.invalid/export.json",
        " " * 2_000_001,
    ],
)
def test_bad_json(text):
    with pytest.raises(ValueError):
        import_external_json(text)


@pytest.mark.parametrize("text", ["", "origin\na\n", ",".join(CSV_COLUMNS) + "\n"])
def test_bad_csv(text):
    with pytest.raises(ValueError):
        import_external_csv(text)


def test_csv_rejects_extra_rows_and_columns(document):
    valid = csv_text(document)
    with pytest.raises(ValueError):
        import_external_csv(valid + valid.splitlines()[1] + "\n")
    with pytest.raises(ValueError):
        import_external_csv(valid.replace("schema_version,", "schema_version,extra,", 1))


def test_schema_closed():
    schema = ExternalResult.model_json_schema()
    assert schema["additionalProperties"] is False
    assert {"provenance", "origin", "calculation", "result"} <= set(schema["required"])


@pytest.mark.parametrize(
    "text", ["[" * 2000 + "0" + "]" * 2000, '{"x":NaN}', '{"x":Infinity}', '{"x":1e999}', "\ud800"]
)
def test_hostile_json_is_value_error(text):
    with pytest.raises(ValueError):
        import_external_json(text)


def test_csv_parser_errors_are_value_errors():
    for row in ['"unterminated', "x" * 140_000]:
        with pytest.raises(ValueError):
            import_external_csv(",".join(CSV_COLUMNS) + "\n" + row)


@pytest.mark.parametrize("ref", ["../../secret", "file:///etc/passwd", "https://evil.invalid/x"])
def test_foreign_references_never_resolved(document, ref, monkeypatch):
    import socket

    monkeypatch.setattr(socket.socket, "connect", lambda *a: pytest.fail("network access"))
    document["calculation"]["factor"] = ref
    with pytest.raises(ValueError):
        import_external_json(json.dumps(document))
    with pytest.raises(ValueError):
        import_external_csv(csv_text(document))
