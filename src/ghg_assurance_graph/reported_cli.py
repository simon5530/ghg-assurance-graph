"""Explicit reported-profile CLI routes, independent of calculated schema 0.1."""

from pathlib import Path

from .adapters import _bounded, _json
from .exporters import export_graph
from .reported import (
    ReportedEvidenceTools,
    compare_reported,
    load_reported,
    validate_reported,
    verify_reported_package,
)


def register(commands):
    parser = commands.add_parser("reported")
    actions = parser.add_subparsers(dest="action", required=True)
    for name in ("ingest", "validate", "graph", "explain", "diff", "package", "verify", "obsidian"):
        action = actions.add_parser(name)
        action.add_argument("input", type=Path)
        if name == "explain":
            action.add_argument("target")
        if name == "diff":
            action.add_argument("after", type=Path)
        if name in ("package", "obsidian"):
            action.add_argument("--out", type=Path, required=True)
        if name == "package":
            action.add_argument("--created-at", required=True)
        if name == "graph":
            action.add_argument("--format", choices=("turtle", "json-ld"), default="turtle")


def run(args, output):
    if args.action == "verify":
        result = verify_reported_package(args.input)
        output(result)
        if not result["valid"]:
            raise SystemExit(1)
        return
    text = args.input.read_text()
    if args.action == "validate":
        _bounded(text)
        result = validate_reported(_json(text))
        output(result)
        if result["status"] == "invalid":
            raise SystemExit(1)
        return
    model = load_reported(text)
    tools = ReportedEvidenceTools(model)
    if args.action == "ingest":
        output(model.model_dump(mode="json"))
    elif args.action == "graph":
        print(export_graph(tools.graph(), args.format), end="")
    elif args.action == "explain":
        output(tools.explain(args.target))
    elif args.action == "diff":
        output(compare_reported(model, load_reported(args.after.read_text())))
    elif args.action == "package":
        output(tools.package(args.out, created_at=args.created_at))
    elif args.action == "obsidian":
        tools.obsidian(args.out)
        output({"exported": True, "profile": model.profile})
