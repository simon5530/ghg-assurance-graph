"""Offline, explicit local inputs; no arbitrary RDF, SPARQL or network execution."""

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .graph import QUERIES, build_graph, deterministic_turtle, query_graph
from .serialization import from_json


def load_package(path):
    return from_json((path / "package.json" if path.is_dir() else path).read_text())


def output(value):
    print(json.dumps(value, sort_keys=True, indent=2, default=str))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    from .reported_cli import register

    register(commands)
    graph = commands.add_parser("graph")
    actions = graph.add_subparsers(dest="action", required=True)
    build = actions.add_parser("build")
    build.add_argument("inputs", nargs="+", type=Path)
    for action in ("explain", "query"):
        command = actions.add_parser(action)
        if action == "explain":
            command.add_argument("target")
        else:
            command.add_argument("name", choices=QUERIES)
            command.add_argument("--target")
        command.add_argument("--input", dest="inputs", required=True, nargs="+", type=Path)
    benchmark = commands.add_parser("benchmark")
    benchmark.add_argument("action", choices=("generate", "run"))
    benchmark.add_argument("--out", type=Path, default=Path("benchmark/generated"))
    benchmark.add_argument("--truth", type=Path, default=Path("benchmark/ground_truth"))
    validate = commands.add_parser("validate")
    validate.add_argument("input", type=Path)
    validate.add_argument("--format", choices=("json",), default="json")
    diff = commands.add_parser("diff")
    diff.add_argument("before", type=Path)
    diff.add_argument("after", type=Path)
    diff.add_argument("--declarations", type=Path)
    diff.add_argument("--format", choices=("json",), default="json")
    package = commands.add_parser("package")
    package_actions = package.add_subparsers(dest="action", required=True)
    create = package_actions.add_parser("create")
    create.add_argument("input", type=Path)
    create.add_argument("--out", type=Path, required=True)
    create.add_argument("--created-at", required=True)
    create.add_argument("--data-version", required=True)
    verify = package_actions.add_parser("verify")
    verify.add_argument("input", type=Path)
    export = commands.add_parser("export")
    export.add_argument("format", choices=("obsidian", "turtle", "json-ld"))
    export.add_argument("out", type=Path)
    export.add_argument("--input", type=Path, required=True)
    adapter = commands.add_parser("import")
    adapter.add_argument("format", choices=("json", "csv"))
    adapter.add_argument("input", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "reported":
            from .reported_cli import run

            run(args, output)
        elif args.command == "graph":
            graph = build_graph([load_package(p) for p in args.inputs])
            if args.action == "build":
                print(deterministic_turtle(graph), end="")
            else:
                name = "explain_result" if args.action == "explain" else args.name
                output(query_graph(graph, name, args.target))
        elif args.command == "benchmark":
            from .benchmark import generate

            generate(args.out)
            if args.action == "run":
                from .evaluation import evaluate_benchmark

                output(evaluate_benchmark(args.out, args.truth))
            else:
                output({"benchmark": "0.1", "generated": True})
        elif args.command == "validate":
            from .validation import validate_package, validate_rows

            path = args.input
            if path.is_dir():
                findings = list(validate_package(load_package(path)))
                if (path / "inputs.json").is_file():
                    findings.extend(validate_rows(json.loads((path / "inputs.json").read_text())))
            else:
                data = json.loads(path.read_text())
                findings = (
                    validate_rows(data["rows"])
                    if "rows" in data
                    else validate_package(load_package(path))
                )
            output({"conforms": not findings, "findings": [f.to_dict() for f in findings]})
            if findings:
                raise SystemExit(1)
        elif args.command == "diff":
            from .diff import Declaration, Snapshot, compare

            def snapshot(path):
                data = json.loads((path / "inputs.json").read_text())
                return Snapshot("synthetic://acme/20250926", path.name, tuple(data))

            declarations = []
            if args.declarations:
                declarations = [Declaration(**d) for d in json.loads(args.declarations.read_text())]
            output(asdict(compare(snapshot(args.before), snapshot(args.after), declarations)))
        elif args.command == "package":
            from .evidence import create_package, verify_package

            if args.action == "create":
                create_package(
                    load_package(args.input),
                    args.out,
                    created_at=args.created_at,
                    data_version=args.data_version,
                    command=["ghgag", "package", "create"],
                )
                output({"created": True})
            else:
                output(verify_package(args.input))
        elif args.command == "export":
            from .exporters import export_graph, export_obsidian

            package = load_package(args.input)
            if args.format == "obsidian":
                export_obsidian(package, args.out)
            else:
                if args.out.exists():
                    raise ValueError("output exists")
                args.out.write_text(export_graph(package, args.format))
            output({"exported": True})
        elif args.command == "import":
            from .adapters import import_external_csv, import_external_json

            importer = import_external_json if args.format == "json" else import_external_csv
            print(importer(args.input.read_text()).model_dump_json(indent=2))
    except (OSError, ValueError, KeyError, TypeError):
        message = (
            "error: invalid local package or query request\n"
            if args.command == "graph"
            else "error: invalid local input or request; no result asserted\n"
        )
        parser.exit(2, message)


if __name__ == "__main__":
    main()
