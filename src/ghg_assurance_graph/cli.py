"""Explicit local canonical inputs; no arbitrary RDF or SPARQL execution."""

import argparse
import json
from pathlib import Path

from .graph import QUERIES, build_graph, deterministic_turtle, query_graph
from .serialization import from_json


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
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
    args = parser.parse_args(argv)
    try:
        packages = [
            from_json((p / "package.json" if p.is_dir() else p).read_text(encoding="utf-8"))
            for p in args.inputs
        ]
        result = build_graph(packages)
        if args.action == "build":
            print(deterministic_turtle(result), end="")
        else:
            name = "explain_result" if args.action == "explain" else args.name
            rows = query_graph(result, name, args.target)
            print(json.dumps(rows, sort_keys=True, indent=2))
    except (OSError, ValueError):
        # Do not leak input paths, data, or validation excerpts in public logs.
        parser.exit(2, "error: invalid local package or query request\n")


if __name__ == "__main__":
    main()
