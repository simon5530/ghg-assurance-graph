# Examples

**Start here:** [complete ExampleCo-GHG-001 worked example](worked_example/README.md),
with [generated sample report](worked_example/sample/REPORT.md).
This is a fictional selected-source inventory, not a complete organizational inventory.

## Ten hand-authored representative cases

The ten entries in [cases.json](cases.json) are manually authored synthetic examples,
not generated benchmark data, real factors, regulatory values or measured results.
[hand_authored.py](hand_authored.py) expands a shared explicit record template; no
random generation, seeded defects or per-case schema extensions are used.

| Case | Context | Activity × illustrative factor = kg CO2e |
|---|---|---|
| electricity-location | Scope 2 location-based | 100 kWh × 0.5 = 50 |
| electricity-market | Scope 2 market-based; contract quality not assessed | 100 kWh × 0.2 = 20 |
| natural-gas | Scope 1 stationary combustion | 10 m³ × 2 = 20 |
| diesel-generator | Scope 1 generator | 10 L × 3 = 30 |
| fleet-fuel | Scope 1 estimated fleet observation | 20 L × 2.5 = 50 |
| refrigerant | Scope 1 synthetic characterization, not actual GWP | 1 kg × 100 = 100 |
| purchased-material | Scope 3 category 1 | 100 kg × 2 = 200 |
| capital-spend | Scope 3 category 2, synthetic USD basis | 100 USD × 0.1 = 10 |
| upstream-transport | Scope 3 category 4 | 100 tonne-km × 0.05 = 5 |
| supplier-pcf | Scope 3 category 1, illustrative supplier boundary | 50 kg × 4 = 200 |

Every case has organization, reviewer organization, facility, reporting period,
boundary, inventory, source, evidence, quality, activity, GWP, method, factor, run,
result, review and authored finding. Quality is explicitly unknown, uncertainty not
quantified, consolidation unknown, review unreviewed. All evidence is synthetic and
original MIT-licensed fixture text. No source files or digest claims are fabricated.
Fleet additionally records an activity correction to 21 L as version 2 and a supplied
ChangeEvent; its existing result still references v1. No recalculation or attribution
is implied. All 17 domain classes occur across the cases.

Run `uv run python examples/hand_authored.py` to write 30 ignored artifacts under
artifacts/examples (JSON, JSON-LD, Turtle). These artifacts can be opened locally;
JSON reload and RDF isomorphism are covered by tests. The production library stores
supplied results; only test arithmetic checks the illustrative numbers independently.
