# Phase 1 experimental implementation contract

Current status note (2026-09-28): this is a historical phase contract. Its dated authorization/HOLD restrictions are superseded by [current Gate A](GATE_A.md) and [original-phase acceptance](ROADMAP_ACCEPTANCE.md); technical invariants remain unless explicitly superseded.
Authorized 2026-09-26 by the owner: proceed with Phase 1 only. This is a bounded
engineering exception to [Gate A HOLD](GATE_A.md), not a research GO, practitioner
review, novelty finding, or permission to begin Phase 2. SoftwareX and the distinct
methods-paper track remain; the removed JOSS scaffold must not be restored.

## Inspectable acceptance oracle (defined before implementation)

- Seventeen named domain classes use Pydantic, forbid unknown fields and freeze
  instances. Stable logical IDs are separate from immutable revision IDs. Revision
  IDs are deterministically logical ID + positive integer version; a predecessor
  must exist, share type/logical ID, and be the immediately previous version.
- A closed package rejects duplicate IDs, dangling/wrong-type references and
  inconsistent organization, reporting period, boundary and calculation/result links.
- All numeric amounts are finite, nonnegative; zero is valid. Units use Pint through
  a bounded vocabulary, not free-form expressions. CO2e is a separate dimension,
  not ordinary mass or an implied GWP conversion. No calculation engine is supplied.
- Sources, licenses, geography, period, GWP, method, boundary, review identity/time
  and data-quality uncertainty are explicit where relevant. Synthetic claims are
  not assurance opinions or verified real factors.
- Ten hand-authored cases exercise the same schema; no per-case schema extension.
  No generated ExampleCo-GHG-001 benchmark or seeded-defect evaluation is included.
- JSON is lossless canonical exchange. RDFLib emits JSON-LD/Turtle with explicit
  typed nodes and PROV-O relationships. RDF semantic roundtrip is tested by graph
  isomorphism; this does not promise arbitrary RDF-to-domain-model import.
- Tests independently assert positive, negative, zero, nonfinite, incompatible-unit,
  revision and reference cases, schema validity and serialization roundtrips.
- Reproducible locked Python environment, CI, documentation checks, dependency/license
  review and tree/history publication scans precede publication.

## Deliberate limits
No SHACL suite, CarbonDiff attribution, benchmark generator, calculator, external
engine adapter, RO-Crate, AI, Jev, UI or calendar. Reviewed status records a supplied
claim; the package cannot authenticate a reviewer. Immutability is a validated
serialization contract, not a tamper-proof database. No licensed factor/standards
text is bundled. Consolidation, allocation, boundary comparability, biogenic
reporting, multi-driver attribution and practitioner validation remain unresolved.
