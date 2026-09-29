"""Deterministic original SVG figures from executed synthetic-only ExampleCo-GHG-001 evaluation."""

from html import escape
from pathlib import Path

from ghg_assurance_graph.evaluation import evaluate_benchmark

ROOT = Path(__file__).resolve().parents[1]


def render():
    result = evaluate_benchmark(ROOT / "benchmark/generated", ROOT / "benchmark/ground_truth")
    validation = result["validation"]
    rows = [
        "ExampleCo-GHG-001 synthetic-only regression — no external validation",
        f"Seeded findings: TP={validation['tp']}, FP={validation['fp']}, FN={validation['fn']}",
        f"Precision={validation['precision']:.2f}; recall={validation['recall']:.2f}; F1={validation['f1']:.2f}",
        "Partial totals (kg CO2e): "
        + " → ".join(
            str(value)
            for value in (
                result["carbondiff_unassisted"][0]["total_before"],
                result["carbondiff_unassisted"][0]["total_after"],
                result["carbondiff_unassisted"][1]["total_after"],
            )
        ),
        "Unassisted CarbonDiff (kg CO2e):",
    ]
    for item in result["carbondiff_unassisted"]:
        rows.append(
            f"{item['before']} → {item['after']}: delta {item['delta']}; signed UNKNOWN {item['residual_kg_co2e']}; absolute UNKNOWN {item['absolute_unknown_kg_co2e']}"
        )
    rows.append("UNKNOWN can cancel in the signed residual; absolute exposure is shown separately.")
    text = "".join(
        f'<text x="24" y="{40 + 34 * i}">{escape(row)}</text>' for i, row in enumerate(rows)
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="320" viewBox="0 0 1080 320"><title>Observed ExampleCo-GHG-001 regression results</title><rect width="1080" height="290" fill="white"/><g font-family="sans-serif" font-size="16" fill="#172b4d">'
        + text
        + "</g></svg>\n"
    )


if __name__ == "__main__":
    target = ROOT / "paper/softwarex/figures/evaluation.svg"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render())
