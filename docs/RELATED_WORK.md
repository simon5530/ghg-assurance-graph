# GHG Assurance Graph — Phase 0 competitor evidence

**Access date: 2026-09-24 (Asia/Taipei).** Research only; public HTTP reads of primary repositories/documentation. No repositories cloned, dependencies installed, competitor code executed, or remote resources modified. This is a bounded prior-art/alternative assessment, not proof that no competing tool exists, a security audit, or a standards-conformance assessment.

## Decision summary

**Gate A: scoped GO, reassessed 2026-09-28.** This supersedes the 2026-09-25 HOLD; see [the recorded gate decision](GATE_A.md) and the same-case comparison below. Corporate carbon accounting, factor-version restatement, numerical factor-change attribution, machine-readable carbon provenance, executable graph validation, and evidence exports each already exist. The strongest near-neighbor discovered beyond the requested list is **TEC Toolkit**: actual PROV-extending carbon ontologies, machine-readable calculation traces, and executable Datalog validation. CarbonLedger already implements factor-vintage change attribution. AutoMatCE and OpenDPP already provide carbon-related RDF/JSON-LD with SHACL.

A potentially defensible contribution is an **organizational-inventory assurance case joining versioned source evidence, RDF/PROV calculation dependencies, executable inventory-specific constraints, and reconciled numerical attribution of changes across approved inventory versions, with a portable reviewer evidence package**. The inspected evidence does not establish one existing project delivering that full combination. That is an integration/use-case gap hypothesis, not algorithmic novelty or a market-exclusivity claim. AI is neither necessary nor a novelty differentiator.

The focused comparison below now assesses **CarbonLedger + TEC/PECO/ECFO + SHACL/RO-Crate**, and adapting Arrhen. Its decision is to proceed as an interoperability/assurance overlay, reusing the components rather than replacing them. Do not start a replacement LCA engine or generic Scope 1/2/3 dashboard on novelty grounds.

## Method and interpretation

- **Code** means relevant source text was inspected, not executed or independently tested. **Docs** means a primary README/specification claim. **NE** means not evidenced within this bounded inspection, **not absent**. **Different** means the demonstrated capability has a different purpose or scope.
- A graph UI is not RDF; mentioning PROV is not a PROV-O implementation; JSON-LD is not automatically a PROV trace; ordinary validation is not SHACL; a hash chain is not semantic provenance; an assurance metadata field is not an assurance procedure; a version identifier or scenario comparison is not a reconciled attribution of version changes.
- “Executable assurance” here means executable data/control checks useful to assurance, **not an automated independent assurance opinion**. Neither SHACL conformance nor balanced ledger entries establish truthful source evidence, correct boundaries, or GHG Protocol compliance.
- Metadata below is the default-branch HEAD returned by GitHub's API at access time. Commit date is the committer timestamp, not a release or effective date. Branch files were read during the same session; commit URLs supply reproducible snapshot references. No release was installed or tested. Maturity assessments are interpretation, not deployment certification.
- A Python HTTPS certificate-store error was resolved by using system `curl` with normal certificate verification; no TLS verification was disabled. One web-search query timed out; two other web searches and direct GitHub repository searches completed. Repository search indexes names/descriptions and is not exhaustive code search.

## Repository snapshots, licensing, and maturity

| Project | Inspected HEAD / commit date (UTC) | License evidence | Maturity assessment |
|---|---|---|---|
| [CarbonLedger](https://github.com/jackson-marcus/Carbon-Ledger) | [ce9f16ed1d987753555d366ceae94e23c81c32b7](https://github.com/jackson-marcus/Carbon-Ledger/commit/ce9f16ed1d987753555d366ceae94e23c81c32b7), 2026-08-30 | README says MIT; GitHub API license is null and inspected 45-file tree has no LICENSE file. **Do not treat reuse permission as settled.** | Created 2026-08-18; 0 stars/0 forks at access. Demo factors/data; README explicitly says in-memory, single-process, no persistence/concurrency/signing-key management. Tests and CI files exist; not run. |
| [Arrhen](https://github.com/kunleowolabi/arrhen) | [d007950adc0507621702831aaad77e4edeb5e508](https://github.com/kunleowolabi/arrhen/commit/d007950adc0507621702831aaad77e4edeb5e508), 2026-07-13 | AGPL-3.0, LICENSE and API classification | Created 2026-05-20; 0 stars/0 forks. 105-file full-stack repository with migrations/tests. README live demo is “deployment in progress”; JOSS badge uses a placeholder, not evidence of publication or peer-review acceptance. |
| [Hyperledger blockchain-carbon-accounting](https://github.com/hyperledger-labs/blockchain-carbon-accounting) | [a53185cf7a2f0956e108a7b875142e86106e61c9](https://github.com/hyperledger-labs/blockchain-carbon-accounting/commit/a53185cf7a2f0956e108a7b875142e86106e61c9), 2025-11-13 | Apache-2.0 | **Archived** per GitHub API; created 2020-08-13, 220 stars/109 forks, 898 files. Substantial multi-component research/application history, but not an actively maintained default choice. Last push 2025-12-05 is distinct from HEAD date. |
| [Battery Carbon Evidence Graph](https://github.com/Alexbohua/battery-carbon-evidence-graph) | [181fb1c47f38ea48f7e77ca9755f05adf43a581d](https://github.com/Alexbohua/battery-carbon-evidence-graph/commit/181fb1c47f38ea48f7e77ca9755f05adf43a581d), 2026-08-11 | MIT code/original docs; external standards and source material separately governed | Created 2026-08-11; 15 files, 0 stars/0 forks. Explicit research prototype, no real annual factory activity data, source thesis not redistributed. |
| [openLCA app](https://github.com/GreenDelta/olca-app) | [c96fddaa2fc995fcd2af7762b2a1993173e65608](https://github.com/GreenDelta/olca-app/commit/c96fddaa2fc995fcd2af7762b2a1993173e65608), 2026-09-19 | MPL-2.0 for app repository; databases/data licenses separate | Long-lived desktop LCA application, repo created 2013, active HEAD, 1,789 files, 264 stars/67 forks. Strong existing calculation/export option; not evidence of organizational assurance equivalence. |
| [Brightway calculation engine](https://github.com/brightway-lca/brightway2-calc) | [4e0682a413247359c006027ff079b990793b8bf5](https://github.com/brightway-lca/brightway2-calc/commit/4e0682a413247359c006027ff079b990793b8bf5), 2026-08-05 | BSD-3-Clause | Maintained LCA framework component with tests and package distribution. Older brightway2 metapackage HEAD is e3d585a663697a368b0e5d037c69ddaba358e080 (2025-04-10); **do not infer ecosystem inactivity from that wrapper**. |
| [WBCSD PACT data-exchange protocol](https://github.com/wbcsd/data-exchange-protocol) | [cf4ebedb18d42f3453bcc868e01159321297c09a](https://github.com/wbcsd/data-exchange-protocol/commit/cf4ebedb18d42f3453bcc868e01159321297c09a), 2025-12-11 | Custom WBCSD LICENSE.md; API says NOASSERTION, **not MIT/Apache** | Specification and implementation contract, not an inventory application. README identifies 3.0.0 as current focus and also lists 2.3.0/1.0.1. Published spec artifacts/OpenAPI exist. |

Metadata sources: GitHub repository endpoints `https://api.github.com/repos/{owner}/{repo}`, `/commits?per_page=1`, and `/git/trees/{default_branch}?recursive=1` for the linked repositories. Stars/file counts are contextual snapshots, not evidence of correctness, adoption, or release readiness.

## Capability comparison

| Project | Organizational GHG | RDF / PROV semantic graph | Executable checks / SHACL | Numeric version-change attribution | Evidence/export | AI |
|---|---|---|---|---|---|---|
| CarbonLedger | Docs + calculation/restatement code for Scope 1/2/3 activities | Provenance metadata/hash-chain claimed; RDF/PROV NE | Python conformance gate inspected; SHACL NE | **Code: fixed activity submission recomputed under two factor vintages, per-activity delta and gross/net drift** | README API returns stages/journal; portable source-evidence bundle NE | No AI workflow evidenced; README explicitly deterministic |
| Arrhen | Docs + relational records/reports inspected | Relational lineage/factor links; RDF/PROV NE | Defensive validation described, tests present; SHACL NE | Version/GWP stamps evidenced; attribution bridge NE | **Code: JSON lineage/factor metadata and PDF generation** | NE |
| Hyperledger | Docs company/supply-chain emissions; selected units/data code inspected | Distributed ledger is different; RDF/PROV NE | Chaincode/contracts and tests exist; SHACL NE | NE | Docs audits/tokenization; upload metadata code; portable assurance bundle NE | NE |
| Battery graph | Scope concepts; annual values explicitly missing | Typed Cytoscape graph; PROV conceptual mapping in docs, executable RDF serialization NE | “Deterministic validation” displayed as workflow/data; SHACL NE | Static academic scenario results, not inventory-version attribution | **Code: visible graph JSON download**, not complete source-evidence package | AI roles/boundaries illustrated in static workflow; live extraction/inference NE |
| openLCA | Different: process/product LCA; no turnkey corporate-inventory assurance workflow established | JSON-LD dataset export code; PROV assurance trace NE | Docs database validation; SHACL NE | Scenario/contribution analysis differs; approved-version attribution NE | **Code: JSON-LD ZIP dataset export**; docs reports/contribution tree | AI assurance workflow NE |
| Brightway | Different: programmable LCA framework | Process/matrix graph differs; RDF/PROV assurance graph NE | Calculation tests present; SHACL NE | Recalculation primitives, not inspected automatic version-change explanation | Code `to_dataframe`; full reviewer bundle NE | Docs AI-powered documentation search only, not accounting AI |
| PACT | Different: product carbon-footprint exchange | JSON/OpenAPI specification; PROV trace NE | Schema/validation tooling in tree; SHACL NE | Version, predecessor and descriptive change fields, **not computed attribution** | PCF and assurance metadata interchange; not underlying full evidence | NE |

### CarbonLedger — most direct numerical-restatement overlap

Primary README: [snapshot](https://github.com/jackson-marcus/Carbon-Ledger/blob/ce9f16ed1d987753555d366ceae94e23c81c32b7/README.md).

Inspected implementation:
- [recompute.py](https://github.com/jackson-marcus/Carbon-Ledger/blob/ce9f16ed1d987753555d366ceae94e23c81c32b7/src/carbonledger/restatement/stages/recompute.py) calls the same calculation engine on the same accepted activities using baseline/candidate factor libraries and aggregates by activity/scope.
- [drift.py](https://github.com/jackson-marcus/Carbon-Ledger/blob/ce9f16ed1d987753555d366ceae94e23c81c32b7/src/carbonledger/restatement/stages/drift.py) computes `candidate - baseline`, sum of absolute changes, net change and largest-single percentage, and emits before/after factors and delta tonnes.
- [conformance.py](https://github.com/jackson-marcus/Carbon-Ledger/blob/ce9f16ed1d987753555d366ceae94e23c81c32b7/src/carbonledger/restatement/stages/conformance.py) checks unknown factors, negative/nonfinite amounts and duplicate activity keys before posting.

This is genuine prior art for **factor-update numerical attribution**, not merely a README promise. It does not establish decomposition of simultaneously changed activity data, boundaries, allocations, GWP and factors, or an RDF assurance graph. Its gross-drift materiality preference is a project policy, **not independently established as a mandated GHG Protocol rule**. Synthetic README results (8.31% gross / +1.57% net) were not rerun. README admits each restatement creates a fresh journal and posting is aggregated rather than source-line level. A future claim of “first auditable factor-version restatement tool” is untenable from this evidence.

### Arrhen — serious reuse candidate, with report-quality caveats

[README](https://github.com/kunleowolabi/arrhen/blob/d007950adc0507621702831aaad77e4edeb5e508/README.md) claims Scope 1/2/3, AR5/AR6, per-compound GWP, CSV/Kobo ingestion, dual Scope 2, multi-tenancy and PDF/JSON reports. These are claims except where specifically inspected below; row-level-security correctness was not audited.

[Emission models](https://github.com/kunleowolabi/arrhen/blob/d007950adc0507621702831aaad77e4edeb5e508/backend/models/emission.py) have factor source/version/validity dates, gas quantities, GWP version, fallback flags and relational links. `activity_record_id` is unique on emission records: the inspected schema does not demonstrate a many-version immutable result history.

[Report generator](https://github.com/kunleowolabi/arrhen/blob/d007950adc0507621702831aaad77e4edeb5e508/backend/core/reporting/report_generator.py) constructs inventory JSON by joining activity, emission, factor and site and generates PDF bytes. Caution: generic methodology text hard-codes AR6/DEFRA 2023/IEA 2022 while individual emission rows retain their own GWP version. This is a **static-review risk** of mismatch, not a reproduced runtime defect. The inspected JSON record explicitly lists CO2/CH4/N2O/HFC/SF6 components while the model also contains PFC/NF3; completeness of a reconstructable gas-level export needs testing. “Audit-ready” remains the author's characterization; the PDF itself disclaims third-party verification.

AGPL network-copyleft obligations require review before reuse in a differently licensed hosted product.

### Hyperledger — ledger/audit workflow, not automatically semantic assurance

[README](https://github.com/hyperledger-labs/blockchain-carbon-accounting/blob/a53185cf7a2f0956e108a7b875142e86106e61c9/README.md) describes permissioned energy data, tokenized emissions audits/credits/certificates, and DAO climate-project voting. Company and supply-chain calculations are explicit use cases. The repository contains Fabric chaincode, Solidity/Hardhat, data models and applications.

Inspected [unit/date helper code](https://github.com/hyperledger-labs/blockchain-carbon-accounting/blob/a53185cf7a2f0956e108a7b875142e86106e61c9/fabric/chaincode/emissionscontract/typescript/src/lib/emissions_data/src/emissions-calc.ts) and [uploaded-file model](https://github.com/hyperledger-labs/blockchain-carbon-accounting/blob/a53185cf7a2f0956e108a7b875142e86106e61c9/data/src/models/uploadedFile.ts) establish implementation artifacts, but do not prove complete evidence export or end-to-end correct accounting. A blockchain's tamper-evidence does not validate input truth. Archived status is a material adoption concern. The large tree was only selectively inspected; NE judgments here are particularly weak negatives.

### Battery Carbon Evidence Graph — closest conceptual presentation, not verified backend

[README](https://github.com/Alexbohua/battery-carbon-evidence-graph/blob/181fb1c47f38ea48f7e77ca9755f05adf43a581d/README.md) explicitly says prototype, separates a 1 kWh NMC111 product model from factory Scope contexts, and leaves real annual factory values missing. [DATA_MODEL.md](https://github.com/Alexbohua/battery-carbon-evidence-graph/blob/181fb1c47f38ea48f7e77ca9755f05adf43a581d/DATA_MODEL.md) maps `provenance` to PROV Entity/Activity/Agent conceptually, says numeric records “should eventually include” extensive metadata, and places stable identifiers/versioned PCF envelopes in the next increment.

Inspected [data.cjs](https://github.com/Alexbohua/battery-carbon-evidence-graph/blob/181fb1c47f38ea48f7e77ca9755f05adf43a581d/src/data.cjs) contains graph/audit records and AI-extraction → validation → human-approval → engine nodes. These workflow nodes are not proof those services execute. [app.cjs](https://github.com/Alexbohua/battery-carbon-evidence-graph/blob/181fb1c47f38ea48f7e77ca9755f05adf43a581d/src/app.cjs) renders React/Cytoscape; `exportGraph` downloads JSON with timestamp, view, boundary notice and **visible projected node/relationship data**. It is not an evidenced RDF/PROV export or full underlying evidence record archive. No SHACL artifact was visible in the 15-file tree. Live AI inference and approval-state persistence remain unverified.

Do not claim novelty for combining product/factory/supplier/evidence concepts, human approval and constrained AI on a graph: this prototype already presents that combination.

### openLCA and Brightway — use existing LCA engines, do not confuse contribution with restatement

openLCA official [2.0 feature announcement](https://www.openlca.org/openlca-2-0-is-now-available-for-download/) documents model graphs, EPDs, contribution-tree export, scenario parameters, collaboration and database validation. This is a historical feature source, **not a claim that 2.0 is the latest release in 2026**; page publication date was not exposed in fetched text. Current repository maintenance is separately dated above.

Inspected [JsonExportWizard.java](https://github.com/GreenDelta/olca-app/blob/c96fddaa2fc995fcd2af7762b2a1993173e65608/olca-app/src/org/openlca/app/wizards/io/JsonExportWizard.java) uses `org.openlca.jsonld.output.JsonExport` with a ZIP store and optional provider/library links. This is real structured model export. It does not by itself establish W3C PROV assurance traces or source-document evidence completeness.

[Brightway official docs](https://docs.brightway.dev/en/latest/) describe a Python LCA framework and academic/industry users (author claim); its AI search announcement concerns documentation search. [Calculation README](https://github.com/brightway-lca/brightway2-calc/blob/4e0682a413247359c006027ff079b990793b8bf5/README.md) describes linear systems, graph traversal and Monte Carlo. Inspected [lca.py](https://github.com/brightway-lca/brightway2-calc/blob/4e0682a413247359c006027ff079b990793b8bf5/src/bw2calc/lca.py) implements inventory/characterization matrix calculations and `to_dataframe`. Recalculation/scenarios/contribution analysis should not be relabeled as an already-implemented accounting change bridge; conversely, they make a bespoke LCA kernel unnecessary.

### PACT — interoperability baseline, not a competing assurance engine

[README](https://github.com/wbcsd/data-exchange-protocol/blob/cf4ebedb18d42f3453bcc868e01159321297c09a/README.md) distinguishes PCF data/API specifications from calculation methodology. Inspected [v3 data model](https://github.com/wbcsd/data-exchange-protocol/blob/cf4ebedb18d42f3453bcc868e01159321297c09a/spec/v3/data-model.md) includes `version`, `precedingPfIds`, descriptive reasons for change, characterization-factor references, factor-database version, quality indicators and an `Assurance` object with coverage/level/provider/completion/standard fields. These are meaningful interchange requirements but not a computed cause-by-cause change attribution or proof of assurance.

[LICENSE.md](https://github.com/wbcsd/data-exchange-protocol/blob/cf4ebedb18d42f3453bcc868e01159321297c09a/LICENSE.md) is custom: it distinguishes noncommercial sharing of reproductions from sharing Separate Derivatives, including commercially, with attribution/disclaimer obligations. Do not copy the specification into a permissively licensed project without reviewing these terms. Implementation can align with PACT while organizational GHG accounting remains a separate reporting boundary. Draft/source consistency and normative published version must be checked before making conformance claims; inspecting markdown is not certification.

## Broader search: material alternatives found

Searches on 2026-09-24:
- Web: `github greenhouse gas emissions restatement provenance numerical attribution`; `github carbon footprint knowledge graph SHACL`. A separate `github carbon accounting RDF PROV SHACL assurance` request timed out.
- GitHub repository search API: `carbon SHACL` (0 results), `emissions provenance` (9), `GHG restatement` (0), `carbon assurance graph` (0). These narrow metadata queries miss repositories whose relevant features appear only in code/README; **zero results are not absence evidence**.
- Followed primary sources for TEC Toolkit, AutoMatCE and OpenDPP; these materially weaken a broad novelty claim. Another repository, [jagrav-alt/Provenance-Verified-Emissions-Monitoring](https://github.com/jagrav-alt/Provenance-Verified-Emissions-Monitoring), had only a title in the inspected README; HEAD 8492aee072835285d300193769a27de1833358cf dated 2026-08-16 and no API-recognized license. Capability is unknown; title similarity is not feature evidence.

### TEC Toolkit — mandatory prior art and reuse assessment

[Official site](https://tec-toolkit.github.io/) identifies a 2023 ISWC publication (DOI [10.1007/978-3-031-47243-5_5](https://doi.org/10.1007/978-3-031-47243-5_5)), ECFO emission-factor ontology/KG, PECO carbon-calculation provenance and a semantic calculation application. The site claims over 42,400 conversion factors; no count was independently recomputed. The site licenses ontologies CC-BY 4.0, software MIT, KG/mappings Apache-2.0.

- [PECO](https://github.com/TEC-Toolkit/PECO): HEAD [059ac8bac868d35eb8498206b3c85aee0244dc74](https://github.com/TEC-Toolkit/PECO/commit/059ac8bac868d35eb8498206b3c85aee0244dc74), 2024-10-09. README explicitly extends PROV and offers RDF/XML, Turtle, JSON-LD and N-Triples; CC-BY 4.0 claimed in README (API classifies license as Other). Inspected [development/peco.ttl](https://github.com/TEC-Toolkit/PECO/blob/059ac8bac868d35eb8498206b3c85aee0244dc74/development/peco.ttl) contains PROV subclass relations, including EmissionGenerationActivity as PROV Activity. This is actual semantic ontology code, not a graph illustration.
- [Data-Validation](https://github.com/TEC-Toolkit/Data-Validation): HEAD [711b51f2e9c865bdf1c869a77cc5c3d1a5531074](https://github.com/TEC-Toolkit/Data-Validation/commit/711b51f2e9c865bdf1c869a77cc5c3d1a5531074), 2023-05-26; MIT. README and inspected [Datalog rules](https://github.com/TEC-Toolkit/Data-Validation/blob/711b51f2e9c865bdf1c869a77cc5c3d1a5531074/scripts/check-kg_CO2e-rules.dlog) establish executable RDF factor-consistency checks with aggregation/comparison. **Datalog, not SHACL.** Runtime requires RDFox; README says commercial product with trial/research licenses, so this is not a cost-free production-runtime assumption.
- [Semantic Machine Learning Impact Calculator](https://github.com/TEC-Toolkit/Semantic_Machine_Learning_Impact_Calculator): HEAD [c692a2b359390bfb9c53cb7e8c7a701ddff8e193](https://github.com/TEC-Toolkit/Semantic_Machine_Learning_Impact_Calculator/commit/c692a2b359390bfb9c53cb7e8c7a701ddff8e193), 2024-10-14; MIT. README claims machine-readable PECO-aligned operations/calculations and factor applicability provenance. This application README/tree were inspected, not its entire backend. It calculates **emissions from ML workloads**; that does not mean AI generates accounting evidence.

Maturity: academic toolkit with publication, ontology serializations, code and rules; sampled components have older HEAD dates. It is not established as a comprehensive corporate inventory product, SHACL implementation, or numerical restatement-attribution engine. Nonetheless “first carbon-provenance knowledge graph with executable validation” would be misleading.

### AutoMatCE — carbon RDF plus actual SHACL

[materialdigital/automatce](https://github.com/materialdigital/automatce), HEAD [3c77c1dd3f068a81199cc5bc5aa3a5567ddfd900](https://github.com/materialdigital/automatce/commit/3c77c1dd3f068a81199cc5bc5aa3a5567ddfd900), 2026-06-19; CC-BY-4.0. README describes automotive circular-economy ontology, release serializations, patterns and validation. Inspected [lifecycle-footprint/shape.ttl](https://github.com/materialdigital/automatce/blob/3c77c1dd3f068a81199cc5bc5aa3a5567ddfd900/src/patterns/lifecycle-footprint/shape.ttl) requires one numeric greenhouse-gas amount, constrains optional unit to an IRI and requires an about-entity link. This is actual SHACL, but not full organizational inventory assurance or source-truth verification. No numeric approved-version attribution was established. Maturity: ontology/pattern project with CI artifacts; runtime validation not executed.

### OpenDPP — JSON-LD/SHACL boundary kit, private product backend

[OpenDPP/opendpp-interop](https://github.com/OpenDPP/opendpp-interop), HEAD [20211ecc2b63eb7664c571a8d629aeeed364491e](https://github.com/OpenDPP/opendpp-interop/commit/20211ecc2b63eb7664c571a8d629aeeed364491e), 2026-09-18; Apache-2.0. README explicitly identifies a generated interoperability mirror with a separate **private backend**, not a fully open-source product. Public assets include schemas, battery passport samples, shapes and conformance tooling.

Inspected [validate/shacl.mjs](https://github.com/OpenDPP/opendpp-interop/blob/20211ecc2b63eb7664c571a8d629aeeed364491e/validate/shacl.mjs) converts JSON-LD to RDF, loads Turtle shapes and invokes `rdf-validate-shacl`, returning conformance and violations. The code explicitly calls its shapes **non-normative**, not an EU/CIRPASS conformance oracle. Organizational accounting, PROV calculation provenance, numerical restatement attribution and AI evidence processing remain NE. This is useful adjacent interoperability prior art; private backend unknowns cannot be scored as absent.

A web search also surfaced [openepcis/openepcis-dpp-ready](https://github.com/openepcis/openepcis-dpp-ready) and battery carbon declarations. It was **not source-inspected** in this bounded pass; do not promote it to a verified capability row. Revisit if product/battery passport scope becomes central.

## What is known, inferred, and unresolved

**Known from inspected source:** CarbonLedger factor-change deltas and checks; Arrhen relational provenance and report generation; battery graph visualization/export projection; openLCA JSON-LD ZIP export; Brightway calculation/dataframe primitives; PACT version/change/assurance fields; PECO PROV semantics; TEC Datalog; AutoMatCE SHACL; OpenDPP executable RDF/SHACL validation.

**Inferred:** a small assurance/interoperability layer may be more useful than another accounting/LCA application. The integrated corporate-inventory change-explanation case may remain differentiated. Source age and repository architecture suggest different maintenance/adoption risks, not proven defects.

**Unresolved:** actual deployment/adoption; full test status; compliance; security; source-document authenticity and access control; reproducibility of complete exports; immutable approval history; simultaneous multi-driver attribution; commercial/private alternatives; other languages/repos not found by these searches. No exhaustive ecosystem or commercial product audit was performed.

### Historical proposed criteria (superseded on 2026-09-28)

The following were analyst-added criteria, not the original Gate A contract. They are historical, not active restrictions; the current decision below supersedes them.

1. **GO only if** a reviewer demonstrably needs the joined workflow and a bounded test can prove: correct organizational boundary/context; immutable approved-version identity; deterministic recalculation; a specified interaction/allocation policy for change attribution; a change bridge that reconciles to total delta; queryable evidence dependencies; failing constraints with actionable violations; and a portable package another reviewer can inspect/recompute.
2. **HOLD novelty marketing** until TEC/PECO/ECFO reuse and CarbonLedger overlap are acknowledged and at least one practitioner compares the proposed output against current tools. Avoid “first,” “unique,” “certified,” “automatic assurance,” or “standards-compliant” claims from this report.
3. **PIVOT to overlay/adapters** if existing engines and provenance vocabularies meet arithmetic/semantic needs. Choose SHACL because it provides useful interoperable validation, not merely to distinguish from TEC's Datalog. Support PACT at the product exchange boundary without conflating it with corporate totals.
4. Keep AI optional and review-gated. Extracted candidate data must not silently change approved factors, units, boundaries or results; a model-generated explanation is not the numeric attribution oracle.

All source links were accessed on 2026-09-24 unless explicitly described as an uninspected search lead. No practical equivalence or absence claim is based solely on a README badge, repository title, zero search results, or star count.

## Independent verification on 2026-09-25

The completion review re-read Arrhen LICENSE and README at the pinned commit: AGPL-3.0 and a literal JOSS `papers/placeholder/status.svg` badge are confirmed. Earlier MIT/JOSS-published descriptions are incorrect. No publication acceptance is established. CarbonLedger pinned `drift.py` was re-read: candidate-minus-baseline per-activity deltas and gross/net drift are implemented; no runtime results were reproduced. TEC official site confirms PECO/ECFO, carbon provenance and Datalog validation. Other detailed code observations above are retained as dated prior research reports, not independently rerun verification. See [search log](NOVELTY_SEARCH.md) and [publication precedent](SOFTWAREX_PRECEDENTS.md).

## 2026-09-28 focused reassessment: one case, three alternatives

**Scope:** an organizational-inventory overlay, not a new accounting engine. Original sections 11/23 ask whether an existing mature open-source project supplies the full combination, not whether every ingredient is new. This bounded review cannot prove universal absence; it identifies concrete missing integration work in the strongest inspected alternatives. Practitioner review is valuable utility evidence, not an original Gate A or Phase 11 prerequisite.

### Common case and acceptance outputs

Existing ACME selected-source electricity row, same Taiwan facility and explicit stable identity, location-based Scope 2 only: 2025-v2 **1,000 kWh × 0.5 kgCO2e/kWh = 500 kgCO2e** versus 2026-v1 **800 × 0.6 = 480 kgCO2e**. Factors are invented, precharacterized CO2e, allocation 1, no second GWP multiplication. Synthetic evidence/review states are not authentic invoices or human approvals.

Required workflow: retain two identified snapshots; query result → calculation → activity/evidence/factor/method/review; flag missing provenance; produce a declared two-driver bridge; export records, graph, versions and integrity metadata for another installation. Activity-first gives (800−1000)×0.5 = **−100**, then 800×(0.6−0.5) = **+80**, total **−20 kgCO2e**, residual 0. Factor-first instead gives +100/−120. Neither ordering proves causation or uniquely correct attribution.

| Alternative | Actual primary evidence applied to this case | Missing work / decision |
|---|---|---|
| Extend CarbonLedger | Re-read pinned recompute.py and drift.py: one accepted activity table is recomputed under two factor libraries. Fixed 1,000 kWh would give 500→600 (+100); fixed 800 gives 400→480 (+80). These are analytical consequences of source, **not competitor runtime measurements**. The stage does not accept two independent activity snapshots. | Add snapshot matching and interaction convention to explain 500→480; add RDF/PROV, inventory shapes and portable evidence profile. Factor-restatement arithmetic is prior art. README MIT without a license file leaves copying permission unresolved. Prefer an adapter/specification contribution over copying. |
| Adapt Arrhen | Re-read generate_json_report: joins organization/site/activity/emission/factor by reporting year; exports quantity/unit, factor source/version, GWP/results. This supplies much of the two input records. The shown factor export does not provide a full numerical-factor reconstruction contract. | Need immutable revisions, snapshot bridge, semantic mapping, shapes and packaging profile. AGPL-3.0 permits reuse with obligations, not silent MIT relicensing. Full-stack/database deployment is broader than the local-library request. A report adapter is plausible, not implemented/benchmarked here. |
| Compose TEC/PECO/ECFO + pySHACL + ro-crate-py | PECO extends PROV with versioned ontology URIs and RDF serializations. Inspected TEC Datalog sums related non-CO2e gas factors and flags sums exceeding a CO2e value. pySHACL validates supplied RDF/shapes; ro-crate-py creates/consumes research packages. | Still author corporate snapshot identity, evidence/review contracts, inventory shapes, comparability, attribution convention and verification profile. No inspected component automatically implements the 500→480 organizational bridge. Composition is the **chosen architectural strategy**, not a mature turnkey competitor or reason to rebuild libraries; PECO/ECFO alignment remains a reuse assessment, not an already implemented dependency. TEC validation needs commercial RDFox (trial/research licenses described); SHACL is an engineering choice, not novelty. |

**Evidence level:** competitor source inspection + exact arithmetic mapping; no competitor installed/executed, no timed usability comparison, no deployment/adoption claim. Missing behavior means not evidenced in inspected interfaces, not impossible elsewhere. Hyperledger, Battery graph, openLCA, Brightway, PACT, AutoMatCE and OpenDPP rows above remain dated 2026-09-24/25 evidence, not falsely refreshed audits.

### Current primary refresh and licensing

On 2026-09-28 GitHub repository/HEAD APIs returned unchanged pinned commits for CarbonLedger, Arrhen, PECO, TEC Data-Validation and the semantic ML calculator (snapshot table above); all five were unarchived. Relevant CarbonLedger stages, Arrhen report source, PECO README and TEC rule/README were retrieved again at those commits. CarbonLedger API still returns null license; Arrhen AGPL-3.0; PECO API NOASSERTION but README explicitly CC BY 4.0; Data-Validation MIT. Prototype/academic maturity cautions remain; unarchived is not deployment evidence.

- [pySHACL README](https://github.com/RDFLib/pySHACL/blob/469cca7a22a078b36c167c1e8dadecf5e5ec6c75/README.md): Apache-2.0, HEAD 2026-07-28; RDFLib-based validator, CLI and distinct conformance/error exits. Reuse validator, author domain shapes.
- [ro-crate-py README](https://github.com/ResearchObject/ro-crate-py/blob/05effe591443934e48e3fe59c53d7bc01a3334e0/README.md): Apache-2.0, HEAD 2026-07-10; supports RO-Crate 1.2/1.1/1.0 and file/contextual entities. [RO-Crate 1.2](https://www.researchobject.org/ro-crate/specification/1.2/) is a community Recommendation published 2025-06-04, not an assurance standard.
- W3C SHACL refresh returned HTTP 403: no new normative interpretation from that failed fetch.
- Python HTTPS failed local certificate validation; system curl succeeded normally for metadata. No TLS verification disabled; not a repository defect.

### Current implementation versus proposed scope

At local revision 25231a6a5078d2d6f452a7c1136e91e2776184bd, read diff.py, tests/test_diff.py and CARBONDIFF/EVIDENCE contracts. Reproduced the electricity row using Snapshot/compare: 500→480, −100/+80, −20 total, residual 0. Ran:

    .venv/bin/python -m pytest -q tests/test_diff.py tests/test_evidence.py tests/test_graph.py tests/test_validation.py

**196 passed in 12.04 s.** Literal/Fraction-based test oracles, not model self-review, check arithmetic. This establishes bounded feasibility, not independent domain acceptance or the whole intended workflow. Comparator uses raw ACME snapshots, not arbitrary RDF matching; semantic declarations are unauthenticated caller assertions, with one whole-row label rather than simultaneous semantic decomposition. Packages retain citations but do **not** fetch/bundle invoices; hashes are not signatures. Review fields do not implement immutable human approval. Preserve these limitations in release/manuscript claims.

### Decision and stop condition

**Scoped GO:** no mature ready-to-use project was established among required/strongest inspected alternatives supplying the entire organizational snapshot → semantic checks → declared numerical attribution → reproducible export combination. The positive justification is the concrete domain glue still needed on the same case even when existing components are composed, not zero search hits. Proceed with the small overlay and reusable profiles/tests. No claims of new provenance standards, decomposition algorithms, automatic assurance, superiority, universal absence, adoption or publishability. Reopen if a maintained full-combination implementation is identified; prefer extension/upstream then. Primary evidence now covers this scoped decision; further broad searches are unlikely to change it.
