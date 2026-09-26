#!/usr/bin/env python3
"""Check scaffold structure, roadmap dependencies, and relative Markdown file links.

Standard library only. This is not a domain or scientific validation suite.
"""
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MILESTONES = [
    "M0 Research Gate", "M1 Domain Model", "M2 Benchmark", "M3 Provenance Graph",
    "M4 Assurance Rules", "M5 CarbonDiff", "M6 Reproducibility", "M7 Integrations",
    "M8 Agent / Jev Experimental", "M9 v1.0", "M10 SoftwareX Submission",
]
REQUIRED = [
    "README.md", "LICENSE", "CITATION.cff", "CHANGELOG.md", "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md", "SECURITY.md", "GOVERNANCE.md", ".gitignore",
    ".github/roadmap.json", ".github/workflows/docs.yml",
    ".github/PULL_REQUEST_TEMPLATE.md", ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/research_proposal.md",
    "adr/0001-not-another-calculator.md", "adr/0002-rdf-shacl-prov.md",
    "paper/methods/FUTURE_PAPER.md",
]
REQUIRED += ["docs/" + name + ".md" for name in (
    "PROBLEM REQUIREMENTS ARCHITECTURE DOMAIN_MODEL ONTOLOGY CARBONDIFF VALIDATION "
    "REPRODUCIBILITY PUBLICATION_STRATEGY AI_BOUNDARY AI_USAGE_LOG LEARNING_LOG RELATED_WORK SOFTWAREX_PRECEDENTS NOVELTY_SEARCH GATE_A PHASE0_ACCEPTANCE PUBLICATION_AUDIT"
).split()]
REQUIRED += ["paper/softwarex/" + name for name in (
    "OUTLINE.md METADATA.md FIGURE_PLAN.md RESULTS_LEDGER.md REFERENCES.bib"
).split()]
REQUIRED += [name + "/README.md" for name in ("src", "tests", "benchmark", "examples")]


def check(root):
    errors = []
    for name in REQUIRED:
        path = root / name
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            errors.append("Missing or empty required file: " + name)
    try:
        data = json.loads((root / ".github/roadmap.json").read_text(encoding="utf-8"))
        milestones = data["milestones"]
        issues = data["issues"]
        if [m["title"] for m in milestones] != MILESTONES:
            errors.append("Roadmap must preserve all 11 ordered milestone titles")
        if len(issues) != 30 or {i["id"] for i in issues} != set(range(1, 31)):
            errors.append("Roadmap must contain exactly 30 uniquely numbered issues")
        if len({i["title"] for i in issues}) != len(issues):
            errors.append("Issue titles must be unique")
        for item in issues:
            for field in ("scope", "non_goals", "verification", "evidence_paths", "labels"):
                if not item.get(field):
                    errors.append("Missing issue field: " + field)
            if any(label not in data["labels"] for label in item["labels"]):
                errors.append("Unknown issue label")
            for evidence in item["evidence_paths"]:
                if not (root / evidence).is_file():
                    errors.append("Missing issue evidence path")
            if not item["title"].strip() or item["milestone"] not in MILESTONES:
                errors.append("Invalid issue title or milestone")
            if not item["acceptance_criteria"] or not all(item["acceptance_criteria"]):
                errors.append("Missing issue acceptance criteria")
            if any(d not in range(1, 31) or d == item["id"] for d in item["depends_on"]):
                errors.append("Invalid issue dependency")
        for item in milestones:
            if not item["acceptance_criteria"] or any(d not in MILESTONES for d in item["depends_on"]):
                errors.append("Invalid milestone contract")
        for graph in (
            {i["id"]: i["depends_on"] for i in issues},
            {m["title"]: m["depends_on"] for m in milestones},
        ):
            visited, active = set(), set()

            def visit(node):
                if node in active:
                    raise ValueError("Cyclic roadmap dependencies")
                if node in visited:
                    return
                active.add(node)
                for child in graph[node]:
                    visit(child)
                active.remove(node)
                visited.add(node)

            for node in graph:
                visit(node)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append("Invalid roadmap: " + str(exc))
    markdown = [p for p in root.rglob("*.md") if ".git" not in p.relative_to(root).parts]
    for path in markdown:
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            target = target.split(' "', 1)[0].strip("<>")
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            resolved = (path.parent / unquote(url.path)).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                errors.append(str(path.relative_to(root)) + ": link escapes repository")
                continue
            if not resolved.exists():
                errors.append(str(path.relative_to(root)) + ": broken link " + target)
    return errors, len(markdown)


if __name__ == "__main__":
    failures, count = check(ROOT)
    if failures:
        print("\n".join(failures), file=sys.stderr)
        sys.exit(1)
    print("PASS: required scaffold, 11 milestones, 30 issues, acyclic dependencies, "
          "and relative file links in {} Markdown files".format(count))
    print("Not checked: remote URLs, Markdown anchors, domain semantics, citation schema, or novelty.")
