# Validation API and reproducibility

Experimental, offline, selected-source validation. **Gate A is scoped GO; no conformity claim.**

Dependency: pyshacl==0.31.0 (also initially tested with 0.30.1). Dependency
metadata and lock are committed. Turtle resource lives at
src/ghg_assurance_graph/shapes/core.ttl and is loaded with importlib.resources.

## API (ghg_assurance_graph.validation)

- Finding(target: str, rule: str, severity="error", message=""): frozen ordered
  dataclass; .id is a SHA256-derived URN; .to_dict() includes id and all fields.
- validate_rows(rows: Iterable[Mapping]) -> tuple[Finding, ...]: ACME policy and
  independent numeric rules, accepts only row payloads, no filenames or truth.
- validate_graph(graph: rdflib.Graph) -> tuple[Finding, ...]: real pySHACL Core;
  caller graph is data, never shapes. Does not mutate the graph.
- validate_package(package: EvidencePackage) -> tuple[Finding, ...]: canonical
  model revalidation and SHACL. Invalid canonical input raises model errors;
  rejected raw fixtures should use validate_rows instead.
- evaluate_findings(predicted: Mapping[str, Iterable[Finding]],
  truth: Iterable[Mapping]) -> dict: keys tp, fp, fn, precision, recall, f1,
  false_positives, false_negatives. Truth rows need case_id/entity/rule/severity.

Precision = TP/(TP+FP); recall = TP/(TP+FN); F1 = 2TP/(2TP+FP+FN).
Undefined ratios return 0, including empty prediction/truth sets. Matching is exact
set matching; repeated reports do not inflate true positives. Extra predicted cases
are false positives; absent predicted cases are false negatives. No true-negative
population or accuracy is invented. For split metrics filter both cases and labels.

Run from repository root after installing dependencies:

~~~sh
.venv/bin/python -m pytest tests/test_validation.py -q
.venv/bin/ruff check src/ghg_assurance_graph/validation.py tests/test_validation.py
~~~

Measured fixture results: development TP=6 FP=0 FN=0; public holdout TP=4 FP=0
FN=0; combined TP=10 FP=0 FN=0, precision=recall=F1=1.0. Three clean snapshots
produce no raw or SHACL findings. This is regression evidence, not population
performance or independent blind evaluation. See PHASE4_CONTRACT.md for limits.

## Separation and numeric policy

The detector does not import the benchmark generator or read truth. The tests
load committed raw fixtures and give only rows to the detector. Truth is loaded
separately by the evaluator. Decimal strings are converted to exact rational arithmetic, independent of the
ambient Decimal context, with no undocumented rounding tolerance; supported conversions are tonne/kg and kWh/MJ plus identity.
Allocation applies exactly once. Unknown conversions and invalid quantities do
not produce a guessed corrected result. Canonical quantities remain float-based
under the existing model; raw domain arithmetic uses source decimal strings (at most 60 digits and exponent
magnitude 60). Raw-graph checks also require factor version/units and review
status/timestamp presence and lexical form; calendar validity remains a canonical
model check.

## Security and assurance boundary

No validation API accepts a URL, arbitrary query, custom shapes or remote ontology.
The packaged shapes contain no SPARQL. pySHACL imports, advanced rules, JS and
inference are disabled. Callers are responsible for safe local RDF parsing before
validate_graph; it is not a sandbox for hostile RDF store implementations or an
unbounded denial-of-service defense. Simulated review status is not human review.
Standards edition/clause authority review is handled separately; no certification,
full reporting conformity or assurance readiness follows from passing these checks.
