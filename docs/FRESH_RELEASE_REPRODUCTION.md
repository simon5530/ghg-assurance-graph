# Independently fetched release reproduction

## Status and scope

This is an executable verification protocol, **not a claim of a completed hosted run**.
A successful run URL, head SHA, archived report and artifact digest must be recorded
after observing CI. Local helper checks or a same-machine clean environment do not
constitute fresh-host evidence. The qualified alpha remains non-assurance software;
synthetic label accuracy is not independent practitioner validation.

The workflow uses a new GitHub-hosted Ubuntu 24.04 runner, Python 3.12.14, no restored
package cache, and separate fresh source/wheel environments. Sparse checkout supplies
only the reproduction harness. Application code, tests, fixtures, uv.lock and the
public-case runner come exclusively from the published v0.3.0a1 source asset.
The independently downloaded published wheel is installed without building it from
that source. No local dist directory, development checkout or unpublished application
code can serve as a fallback. The harness itself is versioned by the workflow head SHA.

## Asset and dependency contract

Pins in [the harness](../scripts/reproduce_release.py) are copied from the
[verified publication manifest](RELEASE_PUBLICATION_0.3.0a1.md): source archive,
published wheel and complete expected public-output archive. The GitHub API name,
size, URL and digest must match; downloaded bytes are independently SHA256 checked
before extraction/install. Extraction rejects links and special files and uses the
Python data filter. Changed/replaced assets fail closed. The sdist is not tested by
this workflow; source installation means the full published source archive.

Runtime and development dependencies are exported from the fetched uv.lock and
installed with required hashes, with caches disabled. uv 0.12.19 is bootstrap tooling
obtained from the package index; the source build uses its pinned hatchling backend.
Tool bootstrap/build dependencies are not all hash-pinned, unlike the runtime/dev
lock exports. Network access is required for acquisition/install. Public-case
execution blocks Python socket connections and DNS; this is not an OS network sandbox.

## Acceptance criteria

- Source installation: entire published pytest suite succeeds; JUnit is archived.
- Both installations import version 0.3.0a1 from their own non-editable virtual
  environment, with isolated Python and no PYTHONPATH/user-site dependency.
- Both regenerate every benchmark file byte-identically to published source fixtures.
- Detection: TP 10, FP/FN 0, precision/recall/F1 1; development TP 6 and holdout TP 4.
- CarbonDiff totals 3820 → 3850 → 4060 kg CO2e; deltas 30/210, attributed 20/−90,
  residual 10/300, absolute unknown 10/500. These are bounded synthetic metrics.
- Both installations execute all CLI stages for UMC Group, UMC parent and TSMC.
  Assertions: 7/9/8; assessed checks: 12/10/11; not-assessable: 41/57/46.
  Package validity, UNKNOWN causality and zero upstream recalculation are asserted.
- Each complete 207-file public-output tree must match the independently downloaded
  expected archive by exact relative filenames and SHA256, with no normalization,
  omitted fields or exclusions. This also checks every reported numerical value.

## Run and collect proof

Once this workflow is on the default branch (or via its path-filtered push trigger):

```sh
gh workflow run released-reproduction.yml --repo simon5530/ghg-assurance-graph --ref main
gh run list --repo simon5530/ghg-assurance-graph --workflow released-reproduction.yml --limit 5 --json databaseId,headSha,status,conclusion,url
# Select the exact run matching the requested head SHA; do not assume newest is yours.
gh run watch RUN_ID --repo simon5530/ghg-assurance-graph --exit-status
gh run view RUN_ID --repo simon5530/ghg-assurance-graph --json status,conclusion,headSha,url
gh run download RUN_ID --repo simon5530/ghg-assurance-graph --dir downloaded-release-proof
gh run view RUN_ID --repo simon5530/ghg-assurance-graph --log > released-reproduction.log
```

Require conclusion=success AND report.json status=passed, both source/wheel checks,
all three asset digests and matching run/head identity. Archive upload success alone
is not a pass: failure reports are deliberately uploaded too. Record the Actions
artifact digest from upload output and retain the downloaded evidence beyond its
90-day retention. Do not conflate source/wheel reproduction with sdist reproduction.

The artifact contains report.json (machine/runner image, Python, harness digest,
run identity, fetched URLs/asset IDs/digests, exact argv/cwd/exit codes, per-file
output digests), raw API metadata, every command stdout/stderr, hashed dependency
exports, installed runtime freezes, test JUnit, numerical metrics, generated benchmark
files, and both complete public-company output trees. No environment/token dump is
performed. Temporary virtual environments/downloads are not uploaded.

Local invocation, requiring Python 3.12 and authenticated gh, is:

```sh
python3.12 -I scripts/reproduce_release.py --report-dir /tmp/new-release-proof
```

The report directory must not exist. Local results remain local evidence only.
TLS failures must be repaired through normal scoped trust/auth procedures; never
disable verification or silently substitute local archives. During implementation
the local GitHub API inspection failed certificate trust, so fresh API/download and
hosted success remain unverified until the recorded run above.
