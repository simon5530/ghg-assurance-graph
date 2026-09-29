"""Build a vector PDF and editable HTML workbook from an executed example run.
Authoring-only dependency: reportlab==4.4.10; no network or runtime dependency.
"""

import argparse
import hashlib
import html
import json
import textwrap
from collections import defaultdict
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
BLUE, TEAL, ORANGE = "#17658a", "#357c70", "#b56d23"
NL = chr(10)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=ROOT / "docs/user-guide")
    args = parser.parse_args()
    run, out = args.run, args.out
    out.mkdir(parents=True, exist_ok=True)

    def read(name):
        return json.loads((run / name).read_text())

    summary = read("summary.json")
    totals = summary["totals_kg_co2e"]
    versions = list(totals)
    rows = {v: read(f"generated/{v}/inputs.json") for v in versions}
    assert list(totals.values()) == [3820, 3850, 4060]
    assert len(read("commands.json")) == 73
    pages = []

    def page(title, action, blocks, interpret, next_step):
        pages.append((title, action, blocks, interpret, next_step))

    def t(s):
        return ("text", s)

    def code(*lines):
        return ("code", NL.join(lines))

    def table(rows):
        return ("table", rows)

    def chart(data):
        return ("chart", data)

    page(
        "From input to inspectable evidence",
        "A practical workbook for ExampleCo-GHG-001",
        [
            t("GHG Assurance Graph | 0.4.0a1 source revision | 29 September 2026"),
            chart([(v, totals[v], BLUE) for v in versions]),
            t(
                "Three selected-source inventories, 45 calculations and 73 recorded CLI actions. Figures are derived from executed JSON outputs, not a simulated application interface."
            ),
            t(
                "Read sequentially: prepare (2-3), inspect (4-7), investigate (8-10), preserve and share (11-13), experiment (14), close (15-16)."
            ),
        ],
        "All organizations, source documents, factors and review labels are invented. This is not a complete inventory or human assurance.",
        "Prepare a local locked Python environment.",
    )
    page(
        "01 / Prepare a locked environment",
        "Run these commands in your terminal.",
        [
            t(
                "Prerequisites: Git, uv and Python 3.12. The package requires >=3.12,<3.13; this run used 3.12.14. Installation may download dependencies. No API key or paid service is required."
            ),
            code(
                "git clone https://github.com/simon5530/ghg-assurance-graph.git",
                "cd ghg-assurance-graph",
                "git checkout main",
                "uv sync --locked",
                "git rev-parse HEAD",
            ),
            t(
                "Use the source commit accompanying this guide, not an older release tag. Record the printed SHA for exact reproduction. uv.lock pins dependencies; do not substitute an unpinned installation."
            ),
            table(
                [
                    ["Check", "Expected"],
                    ["Python", "3.12.x"],
                    ["Environment", ".venv created by uv sync"],
                    ["Working directory", "Repository root"],
                    ["Run network", "Process-local socket guard"],
                ]
            ),
        ],
        "The run is offline after installation. The guard is not an OS sandbox; installed dependencies are trusted.",
        "Choose a new or empty output folder.",
    )
    page(
        "02 / Execute the complete workflow",
        "One command creates the evidence tree.",
        [
            code(
                "uv run --locked python scripts/run_example.py", "  --out artifacts/worked-example"
            ),
            t(
                "The two lines above are one command: join with a space. Open artifacts/worked-example/REPORT.md first. In this guide OUTPUT means that output folder."
            ),
            table(
                [
                    ["Stage", "Saved evidence"],
                    ["Generate / calculate", "generated/ and calculations/"],
                    ["Trace / validate", "stages/<snapshot>/"],
                    ["Compare / declare", "diffs/ and declarations/"],
                    ["Package / verify", "packages/ and package-verify.json"],
                    ["Export / inspect", "vaults/ and REPORT.md"],
                ]
            ),
            code(
                json.dumps(
                    {k: summary[k] for k in ("commands", "source_records", "totals_kg_co2e")},
                    indent=2,
                )
            ),
        ],
        "Actual summary.json excerpt. Success checks 45 Fraction products, literal totals, expected failures, package integrity and vault links.",
        "If the destination exists, choose a new name instead of deleting evidence.",
    )
    r = rows["2025-v1"][0]
    page(
        "03 / Map the input fields",
        "Open OUTPUT/generated/2025-v1/inputs.json.",
        [
            table(
                [
                    ["Field / role", "Actual electricity input"],
                    ["id / matching key", r["id"]],
                    ["activity + unit", r["activity"] + " " + r["unit"]],
                    ["factor + denominator", r["factor"] + " kgCO2e / " + r["factor_unit"]],
                    ["allocation share", r["allocation_share"]],
                    ["scope / basis", "2 / " + r["scope2_basis"]],
                    ["year / geography", str(r["year"]) + " / " + r["geography"]],
                    ["factor basis", r["factor_basis"]],
                    ["apply_gwp", str(r["apply_gwp"]).lower()],
                    ["origin / review", r["origin"] + " / " + r["review"]],
                ]
            ),
            t(
                "Also inspect factor_source, factor_year, evidence, method, gwp_basis, uncertainty and coverage. reported_kg_co2e is an independently checked result, not an extra operand."
            ),
        ],
        "1000 kWh x 0.5 kgCO2e/kWh x 1 = 500 kgCO2e. Precharacterized factors already include GWP: do not multiply by GWP again.",
        "Compare snapshots without calling their difference verified abatement.",
    )
    scopes = {}
    for v in versions:
        s = defaultdict(float)
        for r in rows[v]:
            s[r["scope"]] += float(r["reported_kg_co2e"])
        scopes[v] = s
    page(
        "04 / Read totals and composition",
        "Compare actual selected-source results, in kgCO2e.",
        [
            table(
                [["Snapshot", "Scope 1", "S2 LB", "Scope 3", "Total"]]
                + [[v, *[f"{scopes[v][s]:g}" for s in (1, 2, 3)], str(totals[v])] for v in versions]
            ),
            chart(
                [
                    (f"{v} / S{s}", scopes[v][s], [TEAL, BLUE, ORANGE][s - 1])
                    for v in versions
                    for s in (1, 2, 3)
                ]
            ),
            t(
                "Labels, not color alone, identify scopes. Scope 2 is location-based only; market-based results are alternatives, not additive totals."
            ),
        ],
        "2025-v2 restates 2025-v1 (+30). 2026-v1 is a changed-basis scenario (+210), not a harmonized performance claim. Scope 3 is partial.",
        "Trace a 500 kgCO2e result before trusting an aggregate.",
    )
    lineage = read("stages/2025-v1/explain/electricity.json")[0]
    page(
        "05 / Follow a typed lineage",
        "Open OUTPUT/stages/2025-v1/explain/electricity.json.",
        [
            table(
                [
                    ["Typed node", "Local ID suffix / role"],
                    ["EmissionResult", "electricity-result:v1 / 500 kgCO2e"],
                    ["CalculationRun", "electricity-run:v1"],
                    ["ActivityRecord", "electricity-activity:v1 / 1000 kWh"],
                    ["EmissionFactor", "electricity-factor:v1 / 0.5"],
                    ["CalculationMethod", "electricity-method:v1"],
                    ["GWPSet", "electricity-gwp:v1"],
                    ["EvidenceArtifact", "electricity-evidence:v1"],
                    ["ReviewDecision", "electricity-review:v1 / accepted"],
                ]
            ),
            t(
                "Reference direction: result.calculation -> run; run.activity -> activity; run.factor -> factor. Both operands reference synthetic evidence. Run also references method, GWP, boundary and inventory."
            ),
            code(
                "Shared ID prefix:",
                "urn:ghgag:exampleco-ghg-001-2025-v1-",
                "Actual explain value: " + lineage["value"] + " " + lineage["unit"],
            ),
            t(
                "The same row JSON supports activity and factor evidence here: reproducible provenance, not independent corroboration."
            ),
        ],
        "Accepted is a simulated status, not authenticated reviewer authority. Snapshot IDs are not cross-year revision edges.",
        "Inspect clean and failing validation reports.",
    )
    neg = read("negative-validation.json")["findings"][0]
    missing = read("missing-evidence-validation.json")["findings"][0]
    page(
        "06 / Validate, including failures",
        "Do not interpret exit 0 as assurance.",
        [
            code(json.dumps(read("stages/2025-v1/validation.json"), indent=2)),
            table(
                [
                    ["Control / expected exit", "Finding and target"],
                    ["Clean / 0", "conforms=true; no selected findings"],
                    ["Double GWP / 1", neg["target"] + ": " + neg["rule"]],
                    ["Missing source / 1", missing["target"] + ": " + missing["rule"]],
                ]
            ),
            t(
                "Double GWP: for a precharacterized factor set apply_gwp=false on the source row, then regenerate and revalidate. Do not delete the finding."
            ),
            t(
                "Missing source: restore a legitimate factor_source citation. In this fixture, regenerate the invented source record. In real use, stop until evidence is available."
            ),
            code("Full finding IDs:", neg["id"], missing["id"]),
        ],
        "Two exit-1 controls are expected. Ten defects exist; the full tests evaluate all. Clean means only that encoded checks passed.",
        "Keep failure receipts and separate restatement from annual change.",
    )
    a = read("diffs/2025-v1--2025-v2/assisted.json")
    u = read("diffs/2025-v1--2025-v2/unassisted.json")
    page(
        "07 / Read a same-year restatement",
        "Open both 2025-v1--2025-v2 diff files.",
        [
            chart(
                [
                    (c["entity"] + " / " + c["cause"], float(c["kg_co2e"]), BLUE)
                    for c in a["components"]
                ]
            ),
            table(
                [
                    ["Mode", "Delta", "Signed UNKNOWN", "Absolute UNKNOWN"],
                    [
                        "Unassisted",
                        u["delta"],
                        u["residual_kg_co2e"],
                        u["absolute_unknown_kg_co2e"],
                    ],
                    ["Assisted", a["delta"], a["residual_kg_co2e"], a["absolute_unknown_kg_co2e"]],
                ]
            ),
            t(
                "Fleet: 30 -> 40 liters at factor 2 gives +20. Travel: 100 -> 150 km at factor 0.2 gives +10. Total 3820 -> 3850."
            ),
            t(
                "Declarations supply CORRECTION and MISSING_DATA_RESOLVED interpretations. The unassisted algorithm does not discover these business reasons."
            ),
        ],
        "Zero assisted UNKNOWN reflects supplied assertions, not independently proven causes.",
        "Read the annual comparison using its declared decomposition convention.",
    )
    a = read("diffs/2025-v2--2026-v1/assisted.json")
    u = read("diffs/2025-v2--2026-v1/unassisted.json")
    page(
        "08 / Reconcile the +210 change",
        "Assisted waterfall: 3850 -> 4060 kgCO2e.",
        [
            (
                "waterfall",
                [
                    (
                        c["entity"] + " / " + c["cause"].replace("_CHANGE", ""),
                        float(c["kg_co2e"]),
                        BLUE,
                    )
                    for c in a["components"]
                ],
            ),
            t(
                "Electricity: (800-1000) x 0.5 = -100 activity; 800 x (0.6-0.5) = +80 factor. Net -20. Activity-first, factor-second, allocation-last is the selected convention."
            ),
            t(
                "Other components: supplier mix -100, method -50, refrigerant GWP +400, boundary +30 and allocation -50. These include methodological changes, not only physical changes."
            ),
        ],
        "Bars bridge cumulative values in report order. Components sum to +210; another convention can distribute interactions differently.",
        "Inspect UNKNOWN before accepting a narrative.",
    )
    page(
        "09 / Keep uncertainty visible",
        "Compare unassisted and declaration-assisted outputs.",
        [
            table(
                [
                    ["2025-v2 -> 2026-v1", "Unassisted", "Assisted"],
                    ["Delta", u["delta"], a["delta"]],
                    ["Attributed", u["attributed_kg_co2e"], a["attributed_kg_co2e"]],
                    ["Signed UNKNOWN", u["residual_kg_co2e"], a["residual_kg_co2e"]],
                    [
                        "Absolute UNKNOWN",
                        u["absolute_unknown_kg_co2e"],
                        a["absolute_unknown_kg_co2e"],
                    ],
                ]
            ),
            t(
                "Signed UNKNOWN can cancel: +400 and -100 yield +300 signed but 500 absolute exposure. Absolute exposure is not an extra emission total."
            ),
            code(
                "OUTPUT/declarations/2025-v2--2026-v1.json",
                "OUTPUT/sources/scenarios/2025-v2--2026-v1/",
                "OUTPUT/diffs/2025-v2--2026-v1/assisted.json",
            ),
            t(
                "Read each rationale and its evidence path#sha256 reference. The runner checks the referenced scenario bytes. It does not authenticate a real-world cause."
            ),
        ],
        "Never replace UNKNOWN with a plausible story. Assisted labels remain supplied interpretations.",
        "Preserve the complete run and verify its package.",
    )
    proof = read("stages/2025-v1/package-verify.json")
    page(
        "10 / Verify the evidence package",
        "Read the actual package verification result.",
        [
            code(
                "uv run --locked ghgag package verify",
                "  artifacts/worked-example/packages/2025-v1",
            ),
            code(
                json.dumps(
                    {k: proof[k] for k in ("valid", "record_count", "manifest_sha256")}, indent=2
                )
            ),
            table(
                [
                    ["Location", "What it preserves"],
                    ["packages/2025-v1/", "JSON, graph, schema, ontology, manifest"],
                    ["sources/2025-v1/", "15 synthetic source JSON documents"],
                    ["input-provenance.json", "45 paths and SHA-256 digests"],
                    ["manifest.json", "Full run hashes, except itself"],
                    ["commands.json", "73 argv / exit / stdout / stderr receipts"],
                ]
            ),
            t(
                "Join command lines with a space. Sources remain outside the closed-profile crates. Preserve the whole tree for source documents, comparisons and receipts."
            ),
        ],
        "Hashes detect changed bytes, not truth or authenticity. A substituted file plus substituted manifest can still agree.",
        "Use REPORT.md as an index and JSON for independent checks.",
    )
    excerpt = NL.join((run / "REPORT.md").read_text().splitlines()[:16])
    page(
        "11 / Read the generated report",
        "Actual REPORT.md excerpt, typeset here; not an app screenshot.",
        [
            code(excerpt),
            table(
                [
                    ["Annotation", "How to read it"],
                    ["Profile / warning", "Synthetic and completeness limits"],
                    ["Totals", "Reconcile summary.json and 45 rows"],
                    ["Checks", "Selected validation and package results"],
                    ["Later sections", "Every formula, both diff modes, failures"],
                ]
            ),
            t(
                "The full report has 15 calculations per snapshot. calculations/<snapshot>.json preserves operands; stages/<snapshot>/explain/ has every result lineage."
            ),
        ],
        "A concise report is an evidence index, not a replacement. This guide does not print all 73 receipts or all 45 formulas.",
        "Inspect portable notes without assuming a desktop UI was tested.",
    )
    page(
        "12 / Inspect linked notes",
        "Open OUTPUT/vaults/2025-v1/index.md in a Markdown reader.",
        [
            code(
                "uv run --locked ghgag export obsidian",
                "  artifacts/exercise-vault",
                "  --input artifacts/worked-example/generated/2025-v1",
            ),
            table(
                [
                    ["Portable export", "Inspection route"],
                    ["Markdown", "Start at index.md; follow [[note]] links"],
                    ["Turtle / JSON-LD", "Graph exports and package artifacts"],
                    ["Canonical JSON", "generated/<snapshot>/package.json"],
                ]
            ),
            t(
                "Join command lines with spaces. Optionally open the exported folder as an Obsidian vault, then select index. No plugins or cloud sync are required. Desktop UI behavior is not live-verified; no application screenshots are fabricated."
            ),
            t(
                "The runner verifies every generated wikilink target exists. This proves on-disk resolution, not rendering or interoperability in every editor."
            ),
        ],
        "An evidence graph is not an assurance opinion. Share only authorized files; this example is fictional.",
        "Try a controlled input change in an isolated directory.",
    )
    page(
        "13 / Change one input safely",
        "Predict first, then regenerate dependent evidence.",
        [
            code(
                "uv run --locked python scripts/modify_example.py",
                "  --out artifacts/electricity-exercise",
                "uv run --locked ghgag validate artifacts/electricity-exercise",
            ),
            chart([("Original electricity", 500, BLUE), ("Changed electricity", 550, TEAL)]),
            t(
                "Join the first two lines. The exercise changes 2025-v1 electricity from 1000 to 1100 kWh. Prediction: +100 x 0.5 = +50 kgCO2e; electricity 550; total 3870. It regenerates reported amount, canonical records and embedded evidence hashes, then checks Fraction arithmetic and validators."
            ),
            t(
                "This isolated teaching branch reuses the fixture namespace: never merge it with the original package. For export or packaging, use the new input directory and fresh destinations."
            ),
            t(
                "Do not edit derived results or hashes. benchmark generate restores the fixed baseline, not your exercise. Old crates and reports must not be reused for changed inputs."
            ),
        ],
        "Expected: conforms=true and findings=[]. The script refuses existing output and leaves committed fixtures unchanged.",
        "Run troubleshooting checks before sharing.",
    )
    page(
        "14 / Troubleshoot transparently",
        "Find the cheapest discriminating check.",
        [
            table(
                [
                    ["Symptom", "Check / safe recovery"],
                    ["uv not found", "Install uv or use existing .venv/bin/uv"],
                    ["Wrong Python", "Select 3.12 and sync the lock"],
                    ["Output refused", "Choose a new or empty folder"],
                    ["Unexpected exit 1", "Read rule, target and stderr receipt"],
                    ["Digest mismatch", "Regenerate; never patch the manifest"],
                    ["UNKNOWN remains", "Retain it; require explicit evidence"],
                    ["Wrong total", "Check unit, share, precharacterization"],
                    ["Broken note link", "Regenerate export from matching input"],
                ]
            ),
            t(
                "Do not suppress negative controls: two intentional exit-1 reports prove rejection paths execute. An unexpected failure is not successful reproduction."
            ),
            t(
                "Unsupported: physical-gas characterization, market-factor eligibility proof, complete Scope 3 screening, uncertainty quantification, source authentication and human assurance. No full ISO 14064-1 conformity or certification is claimed."
            ),
        ],
        "Passing a bounded contract cannot establish facts that were never encoded or supplied.",
        "Finish with a second reviewer and preserve the source revision.",
    )
    page(
        "15 / Review, preserve, hand off",
        "Use this checklist before sharing the evidence.",
        [
            table(
                [
                    ["Check", "Expected evidence"],
                    ["Revision + lock", "Git SHA, uv.lock, Python version"],
                    ["Totals", "3820 / 3850 / 4060 kgCO2e"],
                    ["Formulas", "45 independent Fraction products"],
                    ["Receipts", "73 actions; two expected exit-1 controls"],
                    ["Sources", "45 matching source digests"],
                    ["Changes", "+30 and +210; UNKNOWN disclosed"],
                    ["Packages", "158 records per snapshot"],
                    ["Limits", "Fictional / partial / no human assurance"],
                ]
            ),
            t(
                "Glossary: lineage = typed operand/evidence links; snapshot = one fixture version; CO2e = precharacterized equivalent emissions; UNKNOWN = unattributed change; declaration = supplied interpretation; SHA-256 = byte digest; RO-Crate = portable packaging."
            ),
            t(
                "Name choice: CompanyX is a real cyber-insurance business (KHIPU Networks partnership, 14 August 2025). Exact-label search on 29 September 2026 found no results for ExampleCo-GHG-001. This is a fictional identifier, not trademark or global-availability clearance."
            ),
            t("Source: https://www.khipu-networks.com/news/companyx-partnership/"),
        ],
        "Historical releases retain original names and hashes. Current regenerated fixtures use ExampleCo-GHG-001; arithmetic and schema are unchanged.",
        "See examples/worked_example/README.md for the full field dictionary and commands.",
    )
    pages[0][2].append(("flow", ["Input rows", "Typed graph", "Checks / diff", "Crate / notes"]))
    pages[5][2].insert(0, ("flow", ["Result", "CalculationRun", "Activity / Factor", "Evidence"]))
    render(pages, out)
    (out / "figure-data.json").write_text(
        json.dumps(
            {
                "totals": totals,
                "scopes": scopes,
                "run_manifest_sha256": hashlib.sha256(
                    (run / "manifest.json").read_bytes()
                ).hexdigest(),
                "pages": len(pages),
            },
            indent=2,
        )
        + NL
    )


def render(pages, out):
    c = canvas.Canvas(str(out / "GUIDE.pdf"), pagesize=(595.28, 841.89), invariant=1)
    c.setTitle("ExampleCo-GHG-001 | Step-by-step evidence workbook")
    c.setAuthor("GHG Assurance Graph contributors")
    body = ParagraphStyle(
        "body",
        fontName="Helvetica",
        fontSize=11.3,
        leading=16,
        textColor=colors.HexColor("#233747"),
    )
    small = ParagraphStyle("small", parent=body, fontSize=9.4, leading=13)
    html_pages = []
    for n, (title, action, blocks, interpret, next_step) in enumerate(pages, 1):
        y = 779
        c.setFillColor(colors.HexColor(BLUE))
        c.rect(40, 805, 515, 4, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(40, y, title)
        y -= 30

        def para(s, style=body):
            nonlocal y
            p = Paragraph(html.escape(s).replace(NL, "<br/>"), style)
            _, h = p.wrap(515, 700)
            p.drawOn(c, 40, y - h)
            y -= h + 13

        para(action)
        hblocks = []
        for kind, value in blocks:
            if kind == "text":
                para(value)
                hblocks.append("<p>" + html.escape(value) + "</p>")
            elif kind == "code":
                lines = []
                for line in value.splitlines():
                    lines.extend(
                        textwrap.wrap(line, 86, replace_whitespace=False, drop_whitespace=False)
                        or [""]
                    )
                height = len(lines) * 11 + 18
                c.setFillColor(colors.HexColor("#edf3f6"))
                c.rect(40, y - height, 515, height, fill=1, stroke=0)
                c.setFillColor(colors.HexColor("#233747"))
                c.setFont("Courier", 9)
                for i, line in enumerate(lines):
                    c.drawString(49, y - 15 - 11 * i, line)
                y -= height + 14
                hblocks.append("<pre>" + html.escape(value) + "</pre>")
            elif kind == "flow":
                svg = []
                for j, label in enumerate(value):
                    x = 40 + j * 132
                    c.setStrokeColor(colors.HexColor(BLUE))
                    c.setFillColor(colors.HexColor("#edf3f6"))
                    c.roundRect(x, y - 38, 119, 35, 4, fill=1, stroke=1)
                    c.setFillColor(colors.HexColor(BLUE))
                    c.setFont("Helvetica-Bold", 9)
                    c.drawCentredString(x + 59.5, y - 24, label)
                    if j < 3:
                        c.drawString(x + 121, y - 24, ">")
                    svg.append(
                        f'<rect x="{j * 132}" y="3" width="119" height="35" fill="#edf3f6" stroke="{BLUE}"/><text x="{j * 132 + 10}" y="25">{html.escape(label)}</text>'
                    )
                hblocks.append(
                    '<svg viewBox="0 0 530 55" xmlns="http://www.w3.org/2000/svg">'
                    + "".join(svg)
                    + "</svg>"
                )
                y -= 55
            elif kind == "table":
                cols = len(value[0])
                widths = [165, 350] if cols == 2 else [515 / cols] * cols
                for i, row in enumerate(value):
                    ps = [Paragraph(html.escape(str(v)), small) for v in row]
                    hs = [p.wrap(widths[j] - 14, 600)[1] for j, p in enumerate(ps)]
                    height = max(hs) + 14
                    c.setFillColor(
                        colors.HexColor(
                            "#e5eff4" if i == 0 else ("#f4f7f8" if i % 2 else "#ffffff")
                        )
                    )
                    c.rect(40, y - height, 515, height, fill=1, stroke=0)
                    x = 40
                    for j, p in enumerate(ps):
                        p.drawOn(c, x + 7, y - 7 - hs[j])
                        x += widths[j]
                    y -= height
                y -= 14
                hblocks.append(
                    "<table>"
                    + "".join(
                        "<tr>"
                        + "".join("<td>" + html.escape(str(v)) + "</td>" for v in row)
                        + "</tr>"
                        for row in value
                    )
                    + "</table>"
                )
            else:
                data = value
                svg = []
                height = 35 * len(data) + 22
                if kind == "waterfall":
                    current = 3850
                    lo = 3500
                    hi = 4250
                    for i, (label, v, color) in enumerate(data):
                        start, end = current, current + v
                        current = end
                        x = 285 + (min(start, end) - lo) / (hi - lo) * 210
                        width = abs(v) / (hi - lo) * 210
                        yy = y - 18 - i * 35
                        c.setFillColor(colors.HexColor("#233747"))
                        c.setFont("Helvetica", 9)
                        c.drawString(40, yy, label)
                        c.setFillColor(colors.HexColor(TEAL if v < 0 else ORANGE))
                        c.rect(x, yy - 5, max(width, 1), 14, fill=1, stroke=0)
                        c.setFillColor(colors.HexColor("#233747"))
                        c.drawString(510, yy, f"{v:+g}")
                        svg.append(
                            f'<text x="0" y="{20 + i * 35}">{html.escape(label)} {v:+g}</text><rect x="{x - 40}" y="{8 + i * 35}" width="{max(width, 1)}" height="14" fill="{TEAL if v < 0 else ORANGE}"/>'
                        )
                    assert current == 4060
                else:
                    maximum = max(abs(v) for _, v, _ in data) or 1
                    for i, (label, v, color) in enumerate(data):
                        yy = y - 18 - i * 35
                        width = abs(v) / maximum * 195
                        c.setFillColor(colors.HexColor("#233747"))
                        c.setFont("Helvetica", 9)
                        c.drawString(40, yy, label)
                        c.setFillColor(colors.HexColor(color))
                        c.rect(305, yy - 4, width, 14, fill=1, stroke=0)
                        c.setFillColor(colors.HexColor("#233747"))
                        c.drawString(507, yy, f"{v:g}")
                        svg.append(
                            f'<text x="0" y="{20 + i * 35}">{html.escape(label)}</text><rect x="265" y="{8 + i * 35}" width="{width}" height="14" fill="{color}"/><text x="470" y="{20 + i * 35}">{v:g}</text>'
                        )
                y -= height
                hblocks.append(
                    f'<svg viewBox="0 0 530 {height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Executed result chart">'
                    + "".join(svg)
                    + "</svg>"
                )
        para("INTERPRET / " + interpret, small)
        para("NEXT / " + next_step, small)
        if y < 58:
            raise ValueError(f"Page {n} overflow: {y}")
        c.setStrokeColor(colors.HexColor("#ccd7de"))
        c.line(40, 46, 555, 46)
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.HexColor("#536675"))
        c.drawString(40, 31, "ExampleCo-GHG-001 | Synthetic evidence, not assurance")
        c.drawRightString(555, 31, f"{n:02d} / {len(pages):02d}")
        c.showPage()
        html_pages.append(
            "<section><h1>"
            + html.escape(title)
            + "</h1><h2>"
            + html.escape(action)
            + "</h2>"
            + "".join(hblocks)
            + "<aside><b>Interpret:</b> "
            + html.escape(interpret)
            + "</aside><p><b>Next:</b> "
            + html.escape(next_step)
            + f"</p><footer>ExampleCo-GHG-001 | Synthetic, not assurance | {n}/{len(pages)}</footer></section>"
        )
    c.save()
    css = "body{font:17px/1.5 system-ui;color:#233747;background:#e5eaf0;margin:0}section{background:white;max-width:850px;padding:45px;margin:24px auto;page-break-after:always}h1{font-size:29px;color:#17658a}h2{font-size:19px}table{border-collapse:collapse;width:100%;font-size:15px}td{padding:9px;border-bottom:1px solid #ccd7de}tr:first-child,pre,aside{background:#edf3f6}pre{white-space:pre-wrap;overflow-wrap:anywhere;padding:18px;font-size:14px}svg{width:100%;font:12px sans-serif}aside{padding:16px}footer{font-size:12px;border-top:1px solid #ccd7de;margin-top:30px}@media print{body{background:white}section{margin:0;padding:20px}}"
    (out / "GUIDE.html").write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8"><title>ExampleCo-GHG-001 workbook</title><style>'
        + css
        + "</style>"
        + "".join(html_pages)
        + "</html>"
    )
    print(f"{len(pages)} pages; {(out / 'GUIDE.pdf').stat().st_size} bytes")


if __name__ == "__main__":
    main()
