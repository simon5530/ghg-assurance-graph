"""Independent Phase 3 lineage/query expectations; no generator as oracle."""

import json
import subprocess
import sys
from pathlib import Path

import pytest
from rdflib import RDF, Graph, Literal, URIRef
from rdflib.compare import isomorphic
from rdflib.namespace import PROV

from ghg_assurance_graph.graph import build_graph, deterministic_turtle, query_graph
from ghg_assurance_graph.models import EvidencePackage
from ghg_assurance_graph.serialization import GHG, from_json

ROOT = Path(__file__).parents[1]
VERSIONS = ("2025-v1", "2025-v2", "2026-v1")
ROWS = [
    "electricity",
    "natural-gas",
    "diesel",
    "fleet",
    "refrigerant",
    "materials",
    "capital",
    "transport",
    "waste",
    "travel",
    "commuting",
    "supplier-pcf",
    "method-transition",
    "allocation",
    "new-line",
]


def ref(version, name):
    return f"urn:ghgag:exampleco-ghg-001-{version}-{name}:v1"


@pytest.fixture(scope="module")
def packages():
    return [
        from_json((ROOT / "benchmark/generated" / v / "package.json").read_text()) for v in VERSIONS
    ]


@pytest.fixture(scope="module")
def graph(packages):
    return build_graph(packages)


@pytest.mark.parametrize("version", VERSIONS)
@pytest.mark.parametrize("name", ROWS)
def test_all_45_lineages_and_queries(graph, version, name):
    r = lambda suffix: ref(version, name + "-" + suffix)
    result, run = URIRef(r("result")), URIRef(r("run"))
    assert (result, PROV.wasGeneratedBy, run) in graph
    assert (result, RDF.type, GHG.EmissionResult) in graph
    for field in ("activity", "factor", "method", "gwp"):
        assert (run, GHG[field], URIRef(r(field))) in graph
        assert (run, PROV.used, URIRef(r(field))) in graph
    assert (run, PROV.used, URIRef(ref(version, "boundary"))) in graph
    review = URIRef(r("review"))
    assert (review, PROV.used, result) in graph
    assert (result, PROV.wasGeneratedBy, review) not in graph
    assert (URIRef(r("activity")), PROV.wasDerivedFrom, URIRef(r("evidence"))) in graph
    expected = {
        field: r(suffix)
        for field, suffix in {
            "result": "result",
            "calculation": "run",
            "activity": "activity",
            "source": "source",
            "evidence": "evidence",
            "factor": "factor",
            "method": "method",
            "gwp": "gwp",
            "review": "review",
            "factorEvidence": "evidence",
            "methodEvidence": "evidence",
            "gwpEvidence": "evidence",
        }.items()
    }
    expected.update(
        {field: ref(version, field) for field in ("inventory", "period", "boundary", "reviewer")}
    )
    expected.update(
        factorVersion="1",
        methodVersion="1",
        inventoryVersion="1",
        status="accepted",
        unit="kg_CO2e",
    )
    answers = query_graph(graph, "explain_result", str(result))
    assert len(answers) == 1
    assert {k: v for k, v in answers[0].items() if k != "value"} == expected
    assert query_graph(graph, "results_using_factor", r("factor")) == [{"result": str(result)}]
    supported = query_graph(graph, "records_supported_by_evidence", r("evidence"))
    assert {x["record"] for x in supported} == {
        r(x) for x in ("activity", "factor", "method", "gwp")
    }
    assert query_graph(graph, "revisions", str(result)) == [{"result": str(result), "version": "1"}]


def test_exact_count_and_unreviewed(graph, packages):
    assert len(set(graph.subjects(RDF.type, GHG.EmissionResult))) == 45
    assert query_graph(graph, "unreviewed_results") == []
    data = packages[0].model_dump(mode="json")
    statuses = ["unreviewed", "needs-review", "rejected"]
    for record, status in zip(
        [r for r in data["records"] if r["kind"] == "ReviewDecision"], statuses
    ):
        record["status"] = status
    changed = build_graph([EvidencePackage.model_validate(data)])
    assert query_graph(changed, "unreviewed_results") == [
        {
            "result": ref("2025-v1", "electricity-result"),
            "review": ref("2025-v1", "electricity-review"),
        }
    ]


def test_collisions_and_determinism(packages, graph):
    assert isomorphic(graph, build_graph([*reversed(packages), packages[0]]))
    assert deterministic_turtle(graph) == deterministic_turtle(build_graph(reversed(packages)))
    assert isomorphic(graph, Graph().parse(data=deterministic_turtle(graph), format="turtle"))
    data = packages[0].model_dump(mode="json")
    data["records"][0]["label"] = "conflicting shared identity"
    with pytest.raises(ValueError, match="conflicting revision identity"):
        build_graph([packages[0], EvidencePackage.model_validate(data)])
    with pytest.raises(ValueError):
        build_graph([])


@pytest.mark.parametrize(
    "mutation", ["missing", "wrong-kind", "duplicate", "unsafe-id", "wrong-inventory"]
)
def test_builder_revalidates_unsafe_construct(packages, mutation):
    data = packages[0].model_dump(mode="json")
    activity = next(r for r in data["records"] if r["kind"] == "ActivityRecord")
    if mutation == "missing":
        activity["evidence"] = "urn:ghgag:absent:v1"
    elif mutation == "wrong-kind":
        activity["evidence"] = ref("2025-v1", "org")
    elif mutation == "duplicate":
        data["records"].append(data["records"][0])
    elif mutation == "unsafe-id":
        data["records"][0]["id"] = "https://example.invalid/remote"
    else:
        activity["inventory"] = ref("2026-v1", "inventory")
    # Bypass construction deliberately; builder must not trust model_construct.
    records = []
    for raw in data["records"]:
        original = next(r for r in packages[0].records if r.logical_id == raw["logical_id"])
        values = dict(original.__dict__)
        values.update(
            {
                key: value
                for key, value in raw.items()
                if value != original.model_dump(mode="json").get(key)
            }
        )
        records.append(type(original).model_construct(**values))
    bad = EvidencePackage.model_construct(records=tuple(records))
    with pytest.raises(ValueError):
        build_graph([bad])


def test_explicit_revision_chain(packages):
    data = packages[0].model_dump(mode="json")
    old = next(r for r in data["records"] if r["id"] == ref("2025-v1", "electricity-result"))
    for version in (2, 3):
        new = dict(
            old,
            id=old["logical_id"] + f":v{version}",
            version=version,
            supersedes=old["logical_id"] + f":v{version - 1}",
            review=f"urn:ghgag:review-revision-{version}:v1",
        )
        review = next(r for r in data["records"] if r["id"] == old["review"])
        data["records"].extend(
            [
                new,
                dict(
                    review,
                    id=new["review"],
                    logical_id=f"urn:ghgag:review-revision-{version}",
                    target=new["id"],
                ),
            ]
        )
    graph = build_graph([EvidencePackage.model_validate(data)])
    expected = [{"result": old["logical_id"] + f":v{i}", "version": str(i)} for i in (1, 2, 3)]
    for i in (1, 2, 3):
        assert query_graph(graph, "revisions", old["logical_id"] + f":v{i}") == expected


@pytest.mark.parametrize(
    "target",
    [
        None,
        "file:///etc/passwd",
        "https://example.invalid/",
        "urn:ghgag:x:v1> } SERVICE <https://example.invalid/> { ?s ?p ?o } #",
        "urn:ghgag:absent:v1",
        "urn:ghgag:exampleco-ghg-001-2025-v1-org:v1",
    ],
)
def test_bad_targets(graph, target):
    with pytest.raises(ValueError):
        query_graph(graph, "explain_result", target)


@pytest.mark.parametrize(
    "name", ["../explain_result", "SELECT * WHERE {?s ?p ?o}", "LOAD file:///x", "x.rq"]
)
def test_no_arbitrary_query(graph, name):
    with pytest.raises(ValueError, match="unknown query"):
        query_graph(graph, name)


def test_no_unused_binding(graph):
    with pytest.raises(ValueError):
        query_graph(graph, "unreviewed_results", ref("2025-v1", "electricity-result"))


def cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "ghg_assurance_graph.cli", "graph", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )


@pytest.mark.parametrize(
    "args",
    [
        ("build", "benchmark/generated/2025-v1"),
        (
            "explain",
            "urn:ghgag:exampleco-ghg-001-2025-v1-electricity-result:v1",
            "--input",
            "benchmark/generated/2025-v1",
        ),
        ("query", "unreviewed_results", "--input", "benchmark/generated/2025-v1"),
    ],
)
def test_cli_repeated(args):
    first, second = cli(*args), cli(*args)
    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout
    assert first.stderr == second.stderr == ""
    if args[0] == "explain":
        assert json.loads(first.stdout)[0]["value"] == "500.0"


@pytest.mark.parametrize(
    "args",
    [
        ("build", "absent-private-file.json"),
        ("build", "benchmark/generated/defects/manual-override.json"),
        ("explain", "urn:ghgag:absent:v1", "--input", "benchmark/generated/2025-v1"),
        (
            "query",
            "unreviewed_results",
            "--target",
            "urn:ghgag:x:v1",
            "--input",
            "benchmark/generated/2025-v1",
        ),
    ],
)
def test_cli_failure_is_redacted(args):
    out = cli(*args)
    assert out.returncode == 2 and not out.stdout
    assert out.stderr == "error: invalid local package or query request\n"


def test_evidence_literals_are_not_loaded(packages, monkeypatch):
    import socket

    def blocked(*args, **kwargs):
        raise AssertionError("network not permitted")

    monkeypatch.setattr(socket, "create_connection", blocked)
    data = packages[0].model_dump(mode="json")
    next(r for r in data["records"] if r["kind"] == "EvidenceArtifact")["citation"] = (
        "file:///nonexistent"
    )
    graph = build_graph([EvidencePackage.model_validate(data)])
    assert (
        URIRef(ref("2025-v1", "electricity-evidence")),
        GHG.citation,
        Literal("file:///nonexistent"),
    ) in graph
    assert query_graph(graph, "explain_result", ref("2025-v1", "electricity-result"))


@pytest.mark.parametrize("mutation", ["cycle", "ambiguous", "missing-review"])
def test_lineage_rejects_cycles_ambiguity_missing_review(packages, mutation):
    records = list(packages[0].records)
    result = next(r for r in records if r.kind == "EmissionResult")
    if mutation == "cycle":
        values = dict(result.__dict__, supersedes=result.id)
        records[records.index(result)] = type(result).model_construct(**values)
    elif mutation == "ambiguous":
        records.append(result.model_copy(update={"label": "second competing result"}))
    else:
        records = [r for r in records if r.id != result.review]
    bad = EvidencePackage.model_construct(records=tuple(records))
    with pytest.raises(ValueError):
        build_graph([bad])
