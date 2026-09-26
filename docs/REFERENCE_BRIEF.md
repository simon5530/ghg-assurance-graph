# Reference brief: reuse, overlap and uncertainty

Prepared 2026-09-26 from the dated Phase 0 primary-source inspection, not a new
exhaustive literature review. Precise pinned source links and evidence distinctions
are in [RELATED_WORK](RELATED_WORK.md); search limitations in [NOVELTY_SEARCH](NOVELTY_SEARCH.md).
[Gate A remains HOLD](GATE_A.md); Phase 1 is only a bounded engineering experiment.

| Reference | What matters here | Reuse / distinction and uncertainty |
|---|---|---|
| [CarbonLedger](https://github.com/jackson-marcus/Carbon-Ledger) | Inspected code computes factor-vintage restatement deltas and gross/net drift. | Do not claim first provenance/restatement. Compare an overlay before replacing it. README says MIT but inspected tree lacked LICENSE: copying permission unresolved. Not executed. |
| [Arrhen](https://github.com/kunleowolabi/arrhen) | Organizational Scope 1/2/3, source/factor/GWP lineage and report code. | AGPL-3.0, not MIT; network-copyleft review before hosted reuse. Placeholder JOSS badge is not publication. No runtime evaluation. |
| [TEC Toolkit](https://tec-toolkit.github.io/) / [PECO](https://github.com/TEC-Toolkit/PECO) | Existing carbon PROV ontology, factors and executable Datalog checks. | Mandatory prior art, not new carbon semantics here. Assess PECO mapping later; ontology CC-BY, software MIT, KG/mappings Apache per site. RDFox runtime licensing constrains free deployment. Paper DOI [10.1007/978-3-031-47243-5_5](https://doi.org/10.1007/978-3-031-47243-5_5). |
| [AutoMatCE](https://github.com/materialdigital/automatce) | Carbon lifecycle RDF with inspected SHACL shape. | Reuse semantic lessons; CC-BY-4.0 attribution if copied. Not evidence of complete organizational assurance or change attribution. |
| [OpenDPP](https://github.com/OpenDPP/opendpp-interop) | JSON-LD → RDF → SHACL implementation at a product-passport boundary. | Apache-2.0 public interop mirror; backend private. Non-normative shapes are not regulatory certification. |
| [openLCA](https://github.com/GreenDelta/olca-app) | Existing LCA engine and JSON-LD ZIP export. | Optional later IPC adapter; no new LCA engine. App MPL-2.0; databases separately licensed. Contribution analysis is not approved-inventory restatement attribution. |
| [Brightway](https://github.com/brightway-lca/brightway2-calc) | Python LCA matrices, recalculation and dataframe output. | Later optional adapter; calculation component BSD-3-Clause. Do not infer ecosystem inactivity from an older wrapper repository. |
| [PACT](https://github.com/wbcsd/data-exchange-protocol) | PCF exchange, version/predecessor/change descriptions and assurance metadata. | Later boundary mapping, not a new PACT API or corporate-accounting standard. Custom WBCSD terms; metadata is not evidence of actual assurance. |
| [yProv4DV](https://github.com/HPCI-Lab/yProv4DV) | Python visualization instrumentation, PROV and RO-Crate research artifacts. | Reuse provenance/package concepts, not novelty claims. SoftwareX 35 (2026), 102821: [10.1016/j.softx.2026.102821](https://doi.org/10.1016/j.softx.2026.102821). Final metadata verified through Crossref; final full evaluation not read. |

[yProv4DV precedent details](SOFTWAREX_PRECEDENTS.md) distinguish the published title
*Filling the visualization gap in reproducible research workflows* from its differently
titled preprint. No performance numbers or equivalence claims are borrowed.

## Direct Phase 1 dependencies
Pydantic provides typed validation/schema; Pint provides dimensional conversion;
RDFLib provides RDF/JSON-LD/Turtle. All are mature reusable infrastructure, not our
novel contribution. [Dependency/license record](DEPENDENCIES.md). PROV-O is reused;
SHACL/pySHACL and RO-Crate are deferred rather than prematurely installed.

## Decision and remaining work
Known: individual capabilities substantially overlap with existing projects. Inferred:
an organizational evidence/interoperability overlay might be useful. Unknown:
practitioner need, complete comparative reproduction, simultaneous-driver attribution
conventions, boundary comparability, final SoftwareX policy access and publishability.
Next research decision remains a concrete practitioner-reviewed case against composed
existing tools, not more broad “first” claims. Phase 1 validates representation only.
