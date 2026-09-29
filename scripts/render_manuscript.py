"""Local stdlib Markdown-subset renderer; optional installed Chrome PDF export."""

from __future__ import annotations

import argparse
import base64
import html
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper/softwarex"


def architecture():
    boxes = [
        (25, 35, "ExampleCo-GHG-001 / calculated", "Synthetic activity / factor / review"),
        (465, 35, "Optional reported profile", "Generic assertions; not evaluated"),
        (25, 145, "Typed records + RDF / PROV", "Required lineage; no guessed links"),
        (465, 145, "ReportedAssertion graph", "No invented calculation or factor"),
        (25, 255, "Selected checks + CarbonDiff", "Reconcile; expose UNKNOWN"),
        (465, 255, "Checks + per-series differences", "Not assessable; causes UNKNOWN"),
        (245, 365, "Portable local inspection", "JSON / RDF / RO-Crate / Markdown"),
    ]
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="880" height="505" viewBox="0 0 880 505">',
        '<rect width="880" height="505" fill="white"/><g font-family="Arial,sans-serif" fill="#152d40">',
    ]
    for x, y, title, detail in boxes:
        svg.append(
            f'<rect x="{x}" y="{y}" width="390" height="76" rx="9" fill="#eef5fa" stroke="#316784"/>'
        )
        svg.append(
            f'<text x="{x + 195}" y="{y + 29}" text-anchor="middle" font-size="19" font-weight="bold">{html.escape(title)}</text>'
        )
        svg.append(
            f'<text x="{x + 195}" y="{y + 54}" text-anchor="middle" font-size="16">{html.escape(detail)}</text>'
        )
    svg.append(
        '<path d="M220 111V145 M660 111V145 M220 221V255 M660 221V255 M220 331V349H440V365 M660 331V349H440" fill="none" stroke="#316784" stroke-width="3"/>'
    )
    svg.append(
        '<text x="440" y="481" text-anchor="middle" font-size="17">Outside software authority: authenticity / completeness / assurance</text></g></svg>'
    )
    return "".join(svg)


def inline(text):
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return re.sub(r"(https://[^\s<>]+)", r'<a href="\1">\1</a>', text)


def render(source):
    blocks, lines, i = [], source.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("~~~"):
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith("~~~"):
                code.append(lines[i])
                i += 1
            blocks.append("<pre>" + html.escape("\n".join(code)) + "</pre>")
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip("|").split("|")]
                if not all(re.fullmatch(r"[-:]+", c) for c in cells):
                    tag = "th" if not rows else "td"
                    rows.append(
                        "<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in cells) + "</tr>"
                    )
                i += 1
            blocks.append("<table>" + "".join(rows) + "</table>")
            continue
        elif line.startswith("!["):
            match = re.fullmatch(r"!\[(.*?)\]\((.*?)\)", line)
            if not match:
                raise ValueError("Unsupported image syntax")
            path = (PAPER / match[2]).resolve()
            if path.parent != (PAPER / "figures").resolve() or path.suffix != ".svg":
                raise ValueError("Only local manuscript SVG figures permitted")
            data = base64.b64encode(path.read_bytes()).decode()
            blocks.append(
                f'<figure><img alt="{html.escape(match[1])}" src="data:image/svg+xml;base64,{data}"></figure>'
            )
        elif line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            blocks.append(f"<h{level}>{inline(line[level:].strip())}</h{level}>")
        elif line.startswith("- "):
            blocks.append('<p class="bullet">• ' + inline(line[2:]) + "</p>")
        else:
            cls = ' class="caption"' if line.startswith(("**Figure", "**Table")) else ""
            blocks.append(f"<p{cls}>" + inline(line) + "</p>")
        i += 1
    return (
        """<!doctype html><html lang="en"><meta charset="utf-8">
<title>GHG Assurance Graph — initial manuscript</title><style>
@page{size:A4;margin:17mm 18mm;}body{font:11pt/1.36 Georgia,serif;color:#17212b;max-width:180mm;margin:24px auto;}
h1{font:700 22pt/1.2 Arial,sans-serif;color:#173d52;}h2{font:700 15pt/1.2 Arial,sans-serif;margin-top:1.4em;}
h3{font:700 12pt/1.2 Arial,sans-serif;margin-top:1.2em;}h1,h2,h3{break-after:avoid;}
p{orphans:3;widows:3;margin:.65em 0;}a{color:#235c7c;overflow-wrap:anywhere;text-decoration:none;}
figure{margin:1em 0 .4em;break-inside:avoid;break-after:avoid;}img{width:100%;max-height:130mm;object-fit:contain;}
.caption{font:9.5pt/1.35 Arial,sans-serif;}table{border-collapse:collapse;width:100%;font:9pt/1.3 Arial,sans-serif;margin:1em 0;}
th,td{border-bottom:1px solid #b8c4cd;padding:6px;text-align:left;overflow-wrap:anywhere;}tr{break-inside:avoid;}th{border-top:1px solid #466274;}
pre{font:8.3pt/1.4 monospace;white-space:pre-wrap;overflow-wrap:anywhere;padding:10px;background:#f2f5f7;}
.bullet{margin:.2em 0 .2em 1em;}@media print{body{margin:0;max-width:none;}}</style><main>"""
        + "".join(blocks)
        + "</main></html>"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", action="store_true")
    parser.add_argument("--chrome")
    args = parser.parse_args()
    (PAPER / "figures/architecture.svg").write_text(architecture())
    source = (PAPER / "MANUSCRIPT.md").read_text()
    output = PAPER / "MANUSCRIPT.html"
    output.write_text(render(source))
    abstract = source.split("## Abstract", 1)[1].split("**Keywords:", 1)[0]
    counted = abstract + source.split("## 1. Motivation", 1)[1].split("## References", 1)[0]
    metrics = {
        "word_count_method": "whitespace tokens; abstract plus sections 1-5, captions, table, code and declarations; excludes title, authors, metadata and references",
        "counted_words_conservative": len(counted.split()),
        "abstract_words": len(abstract.split()),
        "figures": sum(line.startswith("![") for line in source.splitlines()),
        "official_word_limit": 4000,
        "official_figure_limit": 6,
        "official_template": "Version 6, March 2026",
    }
    assert metrics["counted_words_conservative"] <= 4000
    assert metrics["abstract_words"] <= 250
    assert metrics["figures"] <= 6
    (PAPER / "MANUSCRIPT_METRICS.json").write_text(json.dumps(metrics, indent=2) + "\n")
    print(json.dumps(metrics, indent=2))
    if args.pdf:
        chrome = args.chrome or shutil.which("chromium") or shutil.which("google-chrome")
        if not chrome:
            candidate = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
            chrome = str(candidate) if candidate.is_file() else None
        if not chrome:
            raise SystemExit("HTML written; local Chrome/Chromium required for --pdf")
        with tempfile.TemporaryDirectory(prefix="ghgag-paper-") as profile:
            staged = Path(profile) / "draft.pdf"
            command = [
                chrome,
                "--headless",
                "--disable-gpu",
                "--no-first-run",
                "--disable-background-networking",
                "--disable-sync",
                "--host-resolver-rules=MAP * ~NOTFOUND",
                f"--user-data-dir={profile}",
                "--no-pdf-header-footer",
                f"--print-to-pdf={staged}",
                output.as_uri(),
            ]
            try:
                subprocess.run(command, check=True, timeout=20, capture_output=True)
            except subprocess.TimeoutExpired:
                # Some local Chrome builds finish printing but linger at shutdown.
                # subprocess.run kills/reaps this process. Accept only this run's
                # new complete PDF, never a stale destination left by an older run.
                if not staged.is_file():
                    raise
                data = staged.read_bytes()
                if not data.startswith(b"%PDF-") or not data.rstrip().endswith(b"%%EOF"):
                    raise RuntimeError("Chrome timed out without complete PDF") from None
                print("Chrome shutdown timed out; newly produced complete PDF recovered")
            data = staged.read_bytes()
            if not data.startswith(b"%PDF-") or not data.rstrip().endswith(b"%%EOF"):
                raise RuntimeError("Incomplete PDF")
            (PAPER / "MANUSCRIPT.pdf").write_bytes(data)
        pdf = PAPER / "MANUSCRIPT.pdf"
        if not pdf.read_bytes().startswith(b"%PDF-"):
            raise RuntimeError("Renderer did not produce PDF bytes")
        print(f"PDF bytes: {pdf.stat().st_size}")


if __name__ == "__main__":
    main()
