# Optional ecosystem adapter assessment

Primary sources inspected 2026-09-28. Decision: keep the tested generic JSON/CSV profile; defer vendor parsers without claiming vendor execution. This completes an assessment, not an implementation.

## PACT (roadmap #20)
The [official repository](https://github.com/wbcsd/data-exchange-protocol) describes a PCF data model and exchange API, explicitly separating exchange from calculation methodology. Its current README focuses on 3.0.0. Product footprint per declared unit is not an organizational annual inventory total. Mapping a PCF requires declared unit, lifecycle boundary, reporting/reference period, geography, assurance/data-quality declarations, characterization basis and treatment of biogenic/fossil components. Missing organizational scope/category, purchaser quantities and consolidation cannot be inferred from a PCF alone. A PCF may later support a purchased-goods calculation, but the importer must not allocate twice or fabricate factor/activity lineage.

The current [LICENSE.md](https://github.com/wbcsd/data-exchange-protocol/blob/main/LICENSE.md) is a custom WBCSD license, not assumed MIT. No specification text/schema/code is copied. An implementation would need exact pinned schema/version validation, custom-license review and mapping-loss fixtures. Existing one-activity/one-factor generic profile cannot losslessly represent every PCF field. Proceed with explicit generic mapping only where its full closure exists; otherwise preserve a reported assertion. Defer a PACT-conformance claim and direct parser.

## openLCA (roadmap #21)
[olca-ipc.py README](https://github.com/GreenDelta/olca-ipc.py) implements unified JSON-RPC/REST communication with openLCA; its tests require a running configured server. Data-only openLCA 2 interchange can use olca-schema. The inspected [client LICENSE](https://github.com/GreenDelta/olca-ipc.py/blob/master/LICENSE) is MPL-2.0; this does not license third-party databases or imply the entire ecosystem has the same license. No client code, engine or licensed database is bundled.

Feasible future adapter: obtain authorized external calculation output, retain engine/database/method versions, functional unit, allocation, system boundary and characterized impact category, then map supported provenance without recalculating LCA. Multi-input lifecycle results do not satisfy the current one-activity/one-factor calculation profile. A generic reported aggregate is not an LCA provenance reconstruction. Direct engine validation requires an installed server and a tiny openly licensed system fixture; neither is claimed executed. Defer the optional vendor adapter rather than introducing dummy factors.

Brightway likewise remains optional; no Brightway runtime/database is installed or executed by this release. The original Phase 8 exit asks for at least one external result format, which the tested engine-neutral profile provides, not all listed ecosystem integrations.
