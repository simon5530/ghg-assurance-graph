# Optional deterministic evidence tools (Phase 9)

This library facade is not an agent, natural-language interpreter or AI integration. It reuses the existing five graph query templates, without provider/Jev calls or new dependencies.

## API

```python
from pathlib import Path
from ghg_assurance_graph.serialization import from_json
from ghg_assurance_graph.tools import EvidenceTools
package = from_json(Path("benchmark/generated/2025-v1/package.json").read_text())
tools = EvidenceTools([package])
answer = tools.call({"name": "explain_result",
                     "target": "urn:ghgag:acme-2025-v1-electricity-result:v1",
                     "limit": 25})
```

`QueryRequest.model_json_schema()` exposes a closed request contract. Allowed names: explain_result, results_using_factor, records_supported_by_evidence, unreviewed_results, revisions. Target requirements and kind checks are inherited from graph.query_graph. Values use bound validated revision URNs, never interpolated SPARQL. Unknown fields, arbitrary SPARQL, SERVICE, remote URLs, query-file paths and mutation requests are rejected. No user query text or graph parsing is exposed. Input evidence citations are inert literals, not instructions or fetched documents.

Construction revalidates and snapshots packages, collision-checks them, and builds a local graph. Calls return deterministic sorted rows, total_rows, truncated, evidence record copies and an explicit non-assurance authority label. Evidence records are attached only for evidence IDs in returned rows (and the evidence-target query), not invented transitive evidence. To inspect a result returned by another query, explicitly call explain_result. No matches produce an empty list; malformed targets raise errors. Result strings preserve existing graph semantics.

## Bounds and security limits

- Maximum 2,000 input records (including repeats), 2,000,000 serialized UTF-8 package bytes.
- Request limit is a strict integer 1–100; default 25.
- Maximum serialized response 200,000 bytes; excess fails rather than silently truncating evidence.
- Graph query executes over the bounded snapshot before row slicing; no wall-clock timeout or hard memory sandbox is claimed. Serialization also occurs before byte checks.
- This is an in-process API for validated local packages, not an authentication, multi-tenant or Python sandbox boundary. Callers must not mutate private attributes or bypass model validation.
- No filesystem/network execution, approvals, scheduling, storage, calculations, certification or external publication is performed.

## Evidence-linked benchmark question

The deterministic test asks: “Which asserted evidence supports the ACME 2025-v1 electricity result of 500 kg_CO2e?” The explicit explain_result request yields 500.0 kg_CO2e and the evidence/factor/method/GWP/boundary/review references, with the synthetic citation attached. This proves retrieval and linkage of supplied claims, not factual accuracy, full inventory completeness or actual assurance. It is one bounded benchmark question, not an evaluation of LLM reasoning.

Run `.venv/bin/python -m pytest -q tests/test_tools.py`. Tests cover evidence-linked retrieval with network connections blocked, deterministic output, injection/unknown requests, incorrect targets, output truncation and resource limits.

## Integration deliberately deferred

Only existing graph APIs are imported. CarbonDiff, validation and RO-Crate tool actions are not exposed, pending explicit stable contracts and permission/error semantics. There is no CLI addition, provider integration, natural-language router or autonomous approval loop.
