"""Authoring-only Matplotlib figure sourced from actual MOENV workflow receipts."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    source = ROOT / "examples/moenv_training/workflow/summary.json"
    summary = json.loads(source.read_text())
    plt.rcParams.update({"svg.fonttype": "none", "svg.hashsalt": "moenv-training-1",
                         "font.family": "DejaVu Sans", "font.size": 10})
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.4), gridspec_kw={"width_ratios": [1.4, 1]})
    years = list(summary["years"])
    colors = {"boiler": "#207a89", "generator": "#b28743", "new-generator": "#deba73",
              "cooling": "#87b9af", "electricity": "#244a73"}
    bottom = [0.0, 0.0]
    for source_id, color in colors.items():
        values = [float(summary["years"][y]["source_amounts_kg_co2e"].get(source_id, 0)) for y in years]
        axes[0].bar(years, values, bottom=bottom, label=source_id, color=color, width=0.5)
        bottom = [a + b for a, b in zip(bottom, values, strict=True)]
    for i, value in enumerate(bottom):
        axes[0].text(i, value + 1700, f"{value:,.6f}", ha="center", fontsize=9)
    axes[0].set_ylim(0, 111000)
    axes[0].set_ylabel("kgCO2e (fictional annual inventory)")
    axes[0].set_title("Primary case: source composition")
    axes[0].legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2, fontsize=8, frameon=False)
    labels = ["Monthly rows", "Documents", "Result lineages", "Unreviewed", "Verified crates", "CLI calls"]
    rows = list(summary["years"].values())
    counts = [sum(r["activity_rows"] for r in rows), sum(r["evidence_documents"] for r in rows),
              sum(r["lineage_explanations"] for r in rows), sum(r["unreviewed_results"] for r in rows),
              sum(r["package_valid"] for r in rows), summary["commands"]]
    axes[1].barh(labels[::-1], counts[::-1], color="#207a89")
    for i, value in enumerate(counts[::-1]):
        axes[1].text(value + 2, i, str(value), va="center")
    axes[1].set_xlim(0, 143)
    axes[1].set_title("Executed evidence counts")
    axes[1].set_xlabel("Count; not accuracy or assurance")
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("MOENV-inspired 2023/2024 synthetic case", fontsize=14)
    fig.subplots_adjust(top=0.83, bottom=0.27, wspace=0.65)
    target = ROOT / "paper/softwarex/figures/moenv-evaluation.svg"
    fig.savefig(target, format="svg", metadata={"Date": None, "Creator": "GHG Assurance Graph original Matplotlib authoring script"})
    # Normalize generated XML whitespace, never PDF object offsets.
    target.write_text("\n".join(line.rstrip() for line in target.read_text().splitlines()) + "\n")
    plt.close(fig)
    target.with_suffix(".json").write_text(json.dumps({"summary_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                            "years": summary["years"], "count_labels": labels, "counts": counts,
                            "interpretation": "Executed synthetic values, not performance/causal/assurance results"}, sort_keys=True, indent=2) + "\n")


if __name__ == "__main__":
    main()
