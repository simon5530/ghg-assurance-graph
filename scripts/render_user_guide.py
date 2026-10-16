"""Render the primary MOENV guide from executed CLI receipts, not invented UI."""

import argparse
import hashlib
import html
import json
import textwrap
from fractions import Fraction
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
    summary = json.loads((run / "summary.json").read_text())
    if summary["profile"] != "moenv-workflow/1" or summary["commands"] != 33:
        raise ValueError("guide requires the executed primary workflow")
    years = summary["years"]
    for year, expected in (("2023", "95797.473564"), ("2024", "95229.409244")):
        assert Fraction(years[year]["total_kg_co2e"]) == Fraction(expected)
    pages = []
    text = lambda value: ("text", value)
    code = lambda *lines: ("code", "\n".join(lines))
    table = lambda rows: ("table", rows)

    def page(title, action, blocks, interpretation, next_step):
        pages.append((title, action, blocks, interpretation, next_step))

    page("MOENV evidence: 2023 and 2024", "Primary worked case | 16 October 2026",
         [text("A fully fictional single-site manufacturing case, mapped to inspected Taiwan MOENV collection guidance. This is an evidence workflow, not a filing or assurance opinion."),
          ("flow", ["Monthly records", "Gas calculation", "Typed graph", "Crate / notes"]),
          ("chart", [(year, float(row["total_kg_co2e"]), BLUE) for year, row in years.items()]),
          table([["Executed evidence", "Observed"], ["Monthly rows / documents", "120 / 122"], ["Result lineages", "4 in 2023; 5 in 2024"], ["CLI calls", "33 (30 success, 3 expected rejection)"]])],
         "All nine results remain unreviewed. Historical electricity vintages and synthetic fuel LHV are explicit limitations.", "Install the locked environment.")
    page("01 / Prepare and execute", "Run from the repository root.",
         [text("Prerequisites: Git, uv, Python 3.12; tested with 3.12.14. Installation may download packages. Runtime needs no model, API key or paid service."),
          code("git clone https://github.com/simon5530/ghg-assurance-graph.git", "cd ghg-assurance-graph", "git rev-parse HEAD", "uv sync --locked", "uv run python scripts/run_moenv_example.py --out artifacts/moenv-worked"),
          text("OUTPUT below means artifacts/moenv-worked. The destination must not exist. Open OUTPUT/REPORT.md, commands.json and summary.json. Repeat into a new folder, not over saved evidence.")],
         "The runner invokes real CLI parsers and records stdout, stderr and exit codes. Its Python socket guard is not an OS sandbox.", "Follow the collection-to-evidence folders.")
    page("02 / Map the collection forms", "Use original internal forms, not company disclosure totals.",
         [table([["Forms", "Purpose"], ["01-03", "Entity, facility boundary, source/equipment register"], ["04-05", "Monthly activity and gas-level quantification"], ["06-08", "Quality, uncertainty, annual totals"], ["09-11", "Energy, production, tests and test dates"], ["12-13", "Project extensions: evidence index and change records"]]),
          text("Read examples/moenv_training/FIELD_MAP.md and SOURCES.md. Official inputs span a 113-year guideline/template and a June-2026 workbook update; they are not one publication date."),
          text("The registration is deliberately non-real. A facility/registered boundary is not interchangeable with corporate operational-control metadata. Omitted sources follow this fictional equipment scenario only.")],
         "Tables 12/13 are project traceability extensions, not official mandates. Unknown calibration and uncertainty are not fabricated pass scores.", "Inspect the monthly original documents.")
    page("03 / Inspect original monthly balances", "Open generated/2023/04-activity.csv and evidence/.",
         [table([["Source", "How quantity is derived"], ["Gas / electricity", "(Closing meter - opening meter) x multiplier"], ["Diesel", "Opening stock + purchases - closing stock"], ["HFC-134a", "Opening mass + added - recovered - closing mass"], ["New generator", "Not installed in 2023; starts July 2024"]]),
          text("The January-2023 boiler row is 1010 m3; its synthetic meter starts at 100000 and closes at 101010. Quantity, period, unit and source must match the referenced file and SHA256."),
          text("A documented inactive zero is not a missing record. Refrigerant charge or purchases alone do not establish leaked mass. Real observations and calibration cannot be authenticated by synthetic examples.")],
         "Monthly documents are originals of the training scenario, not real invoices. Preserve them alongside the CSV and source index.", "Run the collection-specific checker.")
    page("04 / Check inputs before the graph", "The two checks have different contracts.",
         [code("uv run python -m ghg_assurance_graph.moenv_example --check artifacts/moenv-worked/generated/2024", "uv run ghgag validate artifacts/moenv-worked/generated/2024/package.json"),
          table([["Check", "Expected output"], ["Collection", "60 monthly rows and 60 document checks"], ["Raw balances", "Meter / fuel / refrigerant quantities reconcile"], ["Canonical package", "conforms: true; findings: []"], ["Meaning", "Selected rules only, not source truth"]]),
          text("Collection checking rejects gaps, duplicates, blank values, wrong units/years, corrupted evidence and altered results. ghgag validate alone does not read the monthly CSV/documents.")],
         "Never replace unknown quantities with zero to satisfy the checker. Both successful checks are needed for the documented workflow.", "Trace the gas calculation and its projection.")
    page("05 / Understand gas arithmetic", "Read generated/2023/05-quantification.csv.",
         [code("2023 boiler: 12780 m3 x 38 MJ/m3 / 1000000", "x (56100 + 1 x 28 + 0.1 x 265)", "= 27270.87138 kgCO2e"),
          table([["Parameter", "Status"], ["kg gas / TJ coefficients", "Transcribed official stationary-fuel values"], ["GWP", "CO2=1, CH4=28, N2O=265, HFC-134a=1300"], ["LHV 38 / 36 MJ per unit", "Synthetic, not tested or official defaults"], ["Electricity 0.494 / 0.474", "Historical example-workbook vintage replay"]]),
          text("The graph receives an explicit composite kgCO2e/unit factor. Do not multiply GWP again. Companion gas tables do not implement a gas-resolved core schema or prove applicable filing-factor selection.")],
         "Official factors, synthetic LHV and historical-vintage policy remain distinct. Fuel category is stationary backup generation, not a vehicle factor.", "Check the annual source results.")
    source_names=[("boiler","Natural-gas boiler"),("generator","Existing diesel generator"),("new-generator","New diesel generator"),("cooling","HFC-134a leakage"),("electricity","Purchased electricity")]
    source_table=[["Source (kgCO2e)","2023","2024"]]
    for source,label in source_names:
        source_table.append([label,*[years[y]["source_amounts_kg_co2e"].get(source,"0 (not installed)") for y in years]])
    source_table.append(["Total",*[years[y]["total_kg_co2e"] for y in years]])
    page("06 / Read the annual totals", "Compare the same declared fictional site.",
         [table(source_table),text("The 2024 new generator contributes 321.16176 kgCO2e. The site boundary is unchanged; equipment composition changes. Purchased electricity rises while boiler, existing generator and refrigerant quantities decline.")],
         "The annual decrease is -568.064320 kgCO2e. It is not independently established abatement or a complete corporate inventory.", "Inspect actual graph explanations.")
    page("07 / Explain an emissions result", "Use the exact revision URN and explicit package path.",
         [("flow",["EmissionResult","CalculationRun","Activity / Factor","Evidence"]),
          code("uv run ghgag graph explain urn:ghgag:moenv-demo-2024-electricity-result:v1 --input artifacts/moenv-worked/generated/2024/package.json"),
          table([["Returned field", "Observed value / meaning"],["value / unit","66265.2 / kg_CO2e"],["status","unreviewed"],["activity / factor","Declared annual activity and coefficient records"],["evidence / factorEvidence","Different synthetic evidence bundles"],["period / boundary / review","Explicit references, not inferred acceptance"]]),
          text("All 9 primary-case lineages resolve. Annual activity bundles contain 12 monthly evidence IDs and hashes; the actual documents are in generated/YEAR/evidence.")],
         "A linked citation is not a downloaded or authenticated document. A retrospective review is not the calculation itself.", "Query factor usage and pending reviews.")
    page("08 / Keep review state visible", "A clean graph must not become fictional acceptance.",
         [code("uv run ghgag graph query unreviewed_results --input artifacts/moenv-worked/generated/2024/package.json", "uv run ghgag graph query results_using_factor --target urn:ghgag:moenv-demo-2024-electricity-factor:v1 --input artifacts/moenv-worked/generated/2024/package.json"),
          table([["Observed", "Meaning"],["4 unreviewed / 2023","Every primary result still lacks human acceptance"],["5 unreviewed / 2024","New generator adds one result"],["50 / 61 canonical records","Typed record counts, not document counts"],["One electricity factor match","Exact-ID use, not arbitrary semantic search"]])],
         "The approved query templates do not authenticate reviewers, run arbitrary SPARQL, or certify inventory completeness.", "Read the labelled arithmetic comparison.")
    deltas=[["Source","Delta kgCO2e"]]+[[r["source"],f"{float(Fraction(r['delta'])):.6f}"] for r in summary["comparison"]["sources"]]
    page("09 / Compare without causal claims", "Open OUTPUT/comparison.json.",
         [table(deltas),text("The source changes sum to -568.064320 kgCO2e. Every causal explanation stays UNKNOWN. A zero predecessor is justified only for the explicitly uninstalled new generator."),
          text("Do not call ghgag diff on these MOENV folders as a supported main step. The legacy raw-snapshot contract is different and the negative control observes exit 2. Old benchmark component scores are not primary-case results.")],
         "This is an arithmetic series comparison, explicitly not CarbonDiff or a measured emissions-reduction decomposition.", "Preserve canonical packages and original documents together.")
    page("10 / Package and verify", "One-click output already contains verified packages/2023 and packages/2024.",
         [code("uv run ghgag package verify artifacts/moenv-worked/packages/2024"),
          table([["Inside closed canonical crate","Outside, preserve with it"],["Canonical package and RDF exports","generated/YEAR/04-activity.csv"],["Schema / ontology / metadata","generated/YEAR/evidence/*"],["Manifest and software versions","Source ledger and collection forms"]]),
          text("Both package verifications return valid: true. Use a new destination when creating another package. Creation timestamp 2026-10-16T00:00:00Z is an explicit replay input, not an authenticated review date."),
          text("Copy the complete OUTPUT directory to preserve the monthly chain; the seven-file canonical crate alone is not the complete source collection.")],
         "Digests prove bounded consistency, not document authenticity. Keep the manifest digest independently; verification must not fetch citation URLs.", "Inspect graph-derived Markdown if useful.")
    page("11 / Export and inspect notes", "No Obsidian installation is required for generation.",
         [code("uv run ghgag export obsidian artifacts/moenv-2024-vault --input artifacts/moenv-worked/generated/2024/package.json"),
          table([["Year","Actual note count"],["2023",str(years['2023']['vault_notes'])],["2024",str(years['2024']['vault_notes'])]]),
          text("The example command needs a new destination. In the one-click output, start at vaults/YEAR/index.md. All generated wikilinks resolve as files; desktop Obsidian interaction remains untested."),
          text("Keep personal annotations separately. Exports are regenerated views, not an approval workflow, editable source of truth or general database.")],
         "Textual notes expose the supplied graph; they do not establish an actual meter observation or performed human review.", "Verify the expected failure receipts.")
    page("12 / Inspect intentional failures", "The runner records expected rejections, not false passes.",
         [table([["Separate negative control","Observed exit"],["Missing monthly activity row","2: collection request rejected"],["Extra file in canonical crate","2: invalid closed package request"],["Legacy ghgag diff on MOENV folders","2: unsupported input contract"]]),
          text("Read negative/*.stderr.txt with commands.json. Unexpected failures stop the run and do not produce a success report. Valid source collections and packages stay untouched."),
          text("If a digest differs, investigate version/source changes. Do not patch only the manifest to claim true observations. If output exists, choose a new folder; do not overwrite evidence.")],
         "The controls demonstrate selected software boundaries; three failures are not a defect-detection benchmark or a security certification.", "Understand how edits and handoff are bounded.")
    page("13 / Edit carefully and hand off", "The workbook is not an automatic Excel-to-graph importer.",
         [text("You may edit blue monthly cells in the filled XLSX examples to observe formula recalculation. Fixed source/month blocks must not move. Edits do not rewrite CSV, originals, hashes, canonical results or graphs."),
          text("--out regenerates the fixed training scenario; it does not read your edited workbook. --check reads this profile's saved CSV and rejects inconsistent documents or calculations. Arbitrary real-company ingestion requires an explicit mapping, not fictional evidence."),
          table([["Handoff item","Check"],["Source commit / uv.lock","Record exact revision and dependency set"],["Two totals","95797.473564 / 95229.409244 kgCO2e"],["Receipts / lineages / originals","33 calls / 9 lineages / 122 synthetic documents"],["Review / uncertainty","Unreviewed / not quantified"],["Primary guide and paper","MOENV case, not old regression metrics"]])],
         "No source truth, statutory conformity, independent assurance, complete Scope 3 coverage or causal abatement is claimed.", "Use docs/USAGE.zh-TW.md and the MOENV field/source ledgers for detailed commands.")
    render(pages, out)
    (out / "figure-data.json").write_text(json.dumps({"profile":"moenv-guide/1","pages":len(pages),"years":years,"commands":summary["commands"],"delta_kg_co2e":summary["comparison"]["delta_kg_co2e"],"summary_sha256":hashlib.sha256((run/'summary.json').read_bytes()).hexdigest(),"run_manifest_sha256":hashlib.sha256((run/'manifest.json').read_bytes()).hexdigest()},sort_keys=True,indent=2)+"\n")


def render(pages, out):
    c = canvas.Canvas(str(out / "GUIDE.pdf"), pagesize=(595.28, 841.89), invariant=1)
    c.setTitle("MOENV 2023/2024 | Step-by-step evidence workbook")
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
                    c.drawRightString(550, yy, f"{v:,.6f}".rstrip("0").rstrip("."))
                    svg.append(
                        f'<text x="0" y="{20 + i * 35}">{html.escape(label)}</text><rect x="265" y="{8 + i * 35}" width="{width}" height="14" fill="{color}"/><text x="470" y="{20 + i * 35}">{v:,.3f}</text>'
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
        c.drawString(40, 31, "MOENV 2023/2024 | Synthetic evidence, not assurance")
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
            + f"</p><footer>MOENV 2023/2024 | Synthetic, not assurance | {n}/{len(pages)}</footer></section>"
        )
    c.save()
    css = "body{font:17px/1.5 system-ui;color:#233747;background:#e5eaf0;margin:0}section{background:white;max-width:850px;padding:45px;margin:24px auto;page-break-after:always}h1{font-size:29px;color:#17658a}h2{font-size:19px}table{border-collapse:collapse;width:100%;font-size:15px}td{padding:9px;border-bottom:1px solid #ccd7de}tr:first-child,pre,aside{background:#edf3f6}pre{white-space:pre-wrap;overflow-wrap:anywhere;padding:18px;font-size:14px}svg{width:100%;font:12px sans-serif}aside{padding:16px}footer{font-size:12px;border-top:1px solid #ccd7de;margin-top:30px}@media print{body{background:white}section{margin:0;padding:20px}}"
    (out / "GUIDE.html").write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8"><title>MOENV 2023/2024 workbook</title><style>'
        + css
        + "</style>"
        + "".join(html_pages)
        + "</html>"
    )
    print(f"{len(pages)} pages; {(out / 'GUIDE.pdf').stat().st_size} bytes")


if __name__ == "__main__":
    main()
