# Publication audit — 2026-09-26 (Asia/Taipei)

Scope: this standalone project only, original Phase 0 documentation/check scripts. No domain software, benchmark data, third-party implementation or private attachment is bundled. The historical local review below is retained; the verified public-publication addendum supersedes its remote blocker.

## Historical remote blocker — 2026-09-25 (resolved)
`gh repo view simon5530/ghg-assurance-graph --json nameWithOwner,visibility,url` failed with an untrusted api.github.com certificate. `gh auth status` also reported an invalid credential; because transport verification fails, credential invalidity is not independently established. The supported identity status sees a native account but exposes no repository mutation operation in this session. Existing-session browser connection failed because Chrome was unavailable. No TLS verification was disabled; no credential was extracted or copied; no alternate raw authenticated API was attempted.

At that historical checkpoint, no remote mutation was made. Repository existence, PUBLIC visibility, branch/SHA/file set, milestone/issue counts, hosted CI and GitHub security controls are **unverified**. Local 11/30 manifest counts must not be reported as GitHub counts. Before any future create, read existing repository/milestones/issues and reconcile exact titles/IDs; never blindly duplicate them.

## Review scope and limitations
All original scaffold text, roadmap and research draft were read. New text was reviewed for private paths/identifiers, unsupported claims and licensing. Public account handle and third-party author/repository identifiers are intentional attribution. No personal contact details, local operational endpoints, raw conversation, attachment, datasets or screenshots are intended for publication. MIT applies to original work only; cited AGPL/custom-licensed projects are not copied. No third-party runtime dependencies exist; dependency vulnerability audit is not applicable to this stdlib-only scaffold. CI action revisions are pinned; hosted execution was not verified at that historical checkpoint.

Important external sources were read via normal verified HTTPS: JOSS rules/format, Arrhen LICENSE/README, CarbonLedger drift source, TEC, yProv4DV repository/arXiv/Crossref. SoftwareX guide returned 403. Not all historical competitor links were re-fetched; no all-remote-links-pass claim. Citation release date removed because no release exists; full CITATION.cff schema validation is not performed.

## Verification results
Tools: Python 3.9.6, Apple Git 2.54.0, Gitleaks 8.30.1.

- `python3 scripts/check_docs.py`: PASS, 11 milestones / 30 issues, dependencies and relative file links (40 Markdown files).
- `python3 scripts/test_check_docs.py`: six tests passed, including five failure cases.
- Original specification comparison: all 30 issue titles exact; 11 milestones and 18 labels.
- `gitleaks dir --redact --no-banner .`: no leaks found in the precommit tree (about 121 KB scanned); final tree/history scans must also pass before any push.
- UTF-8 artifact enumeration: 49 intended text files; no bundled binaries/images/data. Targeted private-path/email/IP review found no matches.
- `git diff --check`: no errors; staged check repeated at commit.
- Before the initial commit, `git log --all` returned no commits: history was empty, not a scanner pass. Reachable-history scanner evidence is recorded after the first commit.

Reviewed content commit: `2db01bed925889d2d805596bf2196e50a6652c51`, 49 tracked files, author and committer `simon5530@users.noreply.github.com`. After this first commit, `gitleaks git --redact --no-banner --log-opts=--all .` scanned one commit and found no leaks. Final precommit tree scan found no leaks in about 122 KB. A `git clone --no-local` into an isolated temporary directory reproduced both documentation commands at that exact commit: checker PASS and six tests OK. Working tree was clean. This audit addendum is a separate evidence-only commit; final SHA is reported outside its own content to avoid a self-referential hash.

No server/authorization/persistence path exists, so service unauthorized/restart tests are not applicable. Same-machine isolated-clone documentation reproduction is distinct from a fresh-machine scientific reproduction.

## Public-publication verification — 2026-09-26 (Asia/Taipei)

The authenticated repository lookup returned 404 before authorized creation. The public repository was created at 2026-09-25T16:49:26Z: https://github.com/simon5530/ghg-assurance-graph. Verified HTTPS authentication and Git push succeeded without disabling TLS verification, extracting credentials, or bypassing the configured egress path. Host-specific trust details are deliberately not published.

Initial published content: `8bd7a57a2775f72b38c571e304de927444382c11`. All 49 remote blob paths and Git object hashes exactly matched the reviewed local tree; default branch `main`, PUBLIC visibility and MIT license were independently queried. Anonymous web retrieval returned HTTP 200 and rendered the README and repository-relative links. Only `main` existed; tags, releases and uploaded Actions artifacts were empty.

Hosted [documentation CI run 36163227750](https://github.com/simon5530/ghg-assurance-graph/actions/runs/36163227750) completed successfully at that SHA. Local checker and all six oracle tests also passed. Gitleaks 8.30.1 scanned the tree and all two reachable commits with no leaks. All tracked artifacts were text; semantic review found no private operational data, credentials, raw attachments or unauthorized third-party content. Original-work MIT licensing and stdlib-only dependency scope remain unchanged.

Verified enabled: secret scanning, push protection, dependency vulnerability alerts (GET returned HTTP 204), automated security fixes (enabled and not paused), and private vulnerability reporting. Attempts to enable non-provider secret patterns and validity checks returned successfully but readback remained disabled: these are **not claimed enabled**. Branch protection/rulesets and code-scanning analysis are not configured in this documentation-only publication.

The subsequent evidence-only commit records verified roadmap IDs and corrected status documentation; its final SHA and hosted CI outcome are reported in the publication completion record rather than self-referentially embedded here. Research Gate A remains **HOLD**. Public infrastructure does not establish domain correctness, novelty, human review, research use, journal eligibility or Phase 1 authorization. External-link, SoftwareX policy and citation-schema limitations above remain open.

Roadmap readback verified 11 exact milestones, 30 exact issues with matching milestone assignments, labels and acceptance contracts, and all 18 requested labels. GitHub retains 10 default labels, so total label count is 28. All roadmap issues remain open; none is represented as implemented or approved. Remote IDs are recorded in the manifest.


## Publication scope correction — 2026-09-26

Owner authorized public visibility with only `paper/joss` removed from the current branch. Methods and SoftwareX files are retained unchanged. No history rewrite is requested or performed; prior JOSS versions remain in Git history. README navigation, the required-file checker and the active route description are synchronized. Historical JOSS research references are retained as evidence, not a live route.

Documentation checker passes (38 Markdown files), all six checker tests pass, and `git diff --check` passes. Gitleaks 8.30.1 found no secrets in the tree or all three existing reachable commits. Tracked artifacts are text; targeted private-path/email review found only intentional GitHub noreply attribution. Methods/SoftwareX have no diff against previous HEAD. Remote has only main, no releases or uploaded Actions artifacts. License, dependency scope and previously documented scientific/external-link limitations are unchanged. Visibility restoration and final remote SHA are checked after this audit commit.

## Phase 1 publication gate — 2026-09-26

Scope: changes on baseline 8955ede9c1184327716e3c69e33e644635615097. Owner authorized
Phase 1 experimental implementation and publication; Gate A research HOLD unchanged.
Only this repository is published. JOSS scaffold remains removed; methods/SoftwareX
retained. No raw specification, private memory, credentials or real inventory data.

Observed locally: Python 3.12.14, uv 0.12.19, Ruff 0.16.9, pytest 9.1.1, Gitleaks
8.30.1, pip-audit 2.10.1. Locked runtime: Pydantic 2.13.5, Pint 0.26.1, RDFLib 7.6.0.
44 domain tests pass, seven documentation-oracle tests pass, documentation links
pass, Ruff lint/format pass, wheel and sdist build. Ten JSON-LD roundtrip tests emit
an upstream RDFLib ConjunctiveGraph deprecation warning; no warnings suppressed.
Ten hand-authored cases export 30 local artifacts. No benchmark metrics inferred.

An isolated clean publication-scope copy with a new virtual environment reproduced
locked installation, 44 tests, all exports and documentation checks. Same machine,
not an independent fresh-machine scientific replication. Runtime and full locked
development requirements independently audited: no known vulnerabilities found.
License metadata reviewed; ambiguous Pint/flexcache BSD license files inspected
and contain three clauses. No competitor source or third-party data bundled.

Gitleaks tree scan used a clean copy of all tracked plus intended nonignored files
(60 text files at that checkpoint), excluding unpublishable local environments,
caches and generated build/export artifacts by Git scope. No leaks found. Reachable
history scan used `gitleaks git --redact --no-banner --log-opts=--all .`: four
baseline commits, no leaks. Final staged tree and postcommit history are rescanned
before push. Filenames/text and diffs reviewed separately for privacy; public
repository identifiers and third-party citations are intentional. No bundled binary.

Existing PUBLIC main/MIT target verified before changes. Commit identities use
GitHub noreply metadata. Remote SHA, hosted tests and issue #5/#6 completion are
verified after push and reported externally (avoids self-referential commit hash).
Remaining issues are not bulk-closed; Phase 3 graph builder is not completed by
Phase 1 serialization. No tag, release, DOI or publication eligibility claimed.

Residual limitations: source authenticity, persistence/tamper resistance, practitioner
review, comparator execution, standards compliance, later schema migrations, external
link exhaustiveness, current SoftwareX policy/full paper access, and research novelty.
No service authentication/restart path exists. Scanner/audit passes are not guarantees.

## Phase 2 publication gate — 2026-09-26

Scope baseline 3a5c540: only bounded ACME benchmark and supporting docs/tests/CI.
84 publication-scope UTF-8 text files at review; no binary, source PDFs, licensed
ISO material, private attachment, production dataset, or personal operational data.
Original synthetic rows, factor values and ground truth are MIT; no new dependency
or borrowed implementation. Existing dependency license review remains applicable.
No paper/joss restoration; SoftwareX and methods retained. Owner publication
authorization is distinct from unchanged research Gate A HOLD.

Observed: Python 3.12.14, uv 0.12.19, pytest 9.1.1, Ruff 0.16.9, pip-audit 2.10.1,
Gitleaks 8.30.1. 86 tests, seven docs tests, 43 Markdown relative-link checks,
Ruff lint/format, wheel/sdist build and byte-identical regenerated fixture hashes
passed. Isolated clean publication copy with a new locked environment reproduced
tests/docs/generation; same machine, not independent fresh-machine reproduction.

Dependency audit: no known vulnerabilities; unpublished project itself skipped by
PyPI auditor (not represented as audited). Gitleaks clean publication tree ~765KB
and all five reachable precommit commits ~263KB: no leaks. Final staged tree and
postcommit reachable history are scanned again before push. Separate semantic
privacy review covered filenames, diff and generated synthetic evidence; no real
identifiers/endpoints or home paths intended for publication. Public repository
handle/noreply metadata and official reference URLs are intentional.

Verified before publication: PUBLIC, main, MIT; secret scanning/push protection
enabled. Other GitHub control readbacks are reported externally. Commit identity
uses GitHub noreply. Remote SHA/complete blob paths and hosted CI must be checked
after push; issue #7/#8 only may close when their exact criteria are fulfilled.

Limits: ISO metadata retrieved via official-domain search, direct ISO/OBP fetch
403; no workaround. Full licensed ISO clauses require practitioner review. GHG
PDF sections inspected through PDF tooling, no redistributed source text. No
complete inventory, assurance, legal compliance, secret holdout, or general
detector/CarbonDiff claim. Scope2 MB is unavailable, not zero. No auth/service
restart path exists. Scanner passes do not guarantee absence of semantic risk.

## Phase 3 publication gate — 2026-09-27

Scope baseline 587590e: experimental provenance graph only, owner-authorized with
ISO clause review deferred. No standards source, licensed excerpts, private paths,
production data or new dependencies. Gate A HOLD unchanged; methods/SoftwareX
retained, no JOSS scaffold. 94 publication-scope UTF-8 text files reviewed.

Observed: Python 3.12.14, uv 0.12.19, pytest 9.1.1, Ruff 0.16.9, pip-audit 2.10.1,
Gitleaks 8.30.1. Full regression: 161 tests pass (86 prior + 75 Phase 3); seven
documentation oracle tests and relative links in 45 Markdown files pass. Ruff
lint/format, wheel/sdist build, unchanged benchmark regeneration pass. Ten existing
RDFLib JSON-LD deprecation warnings remain, not suppressed.

All 45 synthetic results resolve required assertion lineage; explicit revision
chains, cross-snapshot isolation, identical deduplication/conflict rejection,
missing/wrong references, cycles, ambiguous identities, unsafe identifiers and
query names, deterministic CLI output and redacted errors tested. No SHACL or
general assurance detector added. Direct evidence support is not transitive truth.

Isolated publication copy with a new locked environment reproduced all 161 tests,
docs, generation, build and CLI. Separately installed wheel includes five query
resources and returns byte-identical explanation; wheel proof repeated with the
exact lock-exported runtime versions. Same machine, not independent replication.
Runtime and installed development dependency audits: no known vulnerabilities;
unpublished project itself is not covered by PyPI advisory lookup. No dependency
version/lock change; existing license review applies, RDFLib BSD-3-Clause, Pydantic
MIT and Pint BSD metadata rechecked.

Publication tree scanner: approximately 797 KB, no leaks. All six reachable
precommit commits: approximately 781 KB, no leaks. Final staged tree and postcommit
history are rescanned before push. Separate semantic review covered filenames,
diff, text and synthetic fixtures; no private operational context or binary
artifacts intended for publication. Build/cache/local reports remain ignored.

PUBLIC/main/MIT verified anonymously; Git transport reads the intended remote.
Authenticated GitHub CLI currently fails certificate verification; no trust
changes, TLS bypass, credentials extraction or alternative authenticated route
used. Issue #9/#10 acceptance read anonymously; no new issues created. Issue
closure/security-control authenticated readback may require parent follow-up if
the CLI blocker persists. Remote SHA/blob hashes and hosted CI are verified after
push and reported outside this self-referential audit. Noreply commit identity.

Limits: ISO 14064-1 clause review UNVERIFIED/deferred; source/review authenticity,
complete inventory coverage, research novelty, practitioner review, exhaustive
external links and independent parent review remain unverified. No release/DOI,
certification, security guarantee or Phase 4 completion claimed.

## 2026-09-28 — 0.2.0a1 deterministic continuation audit

Scope: original selected validation, ACME CarbonDiff, evidence/vault exports, generic
adapter/tools, CLI and aligned documentation; baseline dc315cf. No ISO source,
extracted text, image, private path or license metadata is included. ISO assessment
is original paraphrase and clause references with access/coverage limits.

Verification: 297 tests passed (11 upstream RDFLib deprecation warnings); Ruff lint
and format pass; 52 Markdown files pass relative-link check; 7 docs-check tests.
Wheel built from sdist and installed in an isolated Python 3.12.14 environment.
Hashed runtime requirements were obtained then installed with offline mode; an
initial missing-cache failure was correctly reported, not counted as a pass.
Installed wheel ran packaged shapes/queries, two identical benchmark generations,
two byte-identical crates, verification and vault export with socket connections
blocked, outside the repository. This is same-machine isolation, not independent
fresh-machine/practitioner reproduction.

pip-audit: no known vulnerabilities in the locked runtime set or installed
development environment; local project is not on PyPI and is not remotely audited.
Dependency metadata/licenses recorded in DEPENDENCIES.md. No vendored libraries.

Gitleaks 8.30.1 scanned tree and all seven previously reachable commits; history
clean. A tree finding was reviewed as prose about repeated JSON member names, not
a credential; wording clarified, no scanner rule disabled. Separate semantic
scan of 154 historical blobs and current intended files found no private paths,
source metadata, key material, NUL/binary artifacts or standards PDFs. Public
repository identity and attribution references are intentional. Final postcommit
history/tree scans and remote SHA verification are recorded in the handoff.

Authenticated issue access still fails normal TLS verification. No issue closure,
repository-description update, release, DOI or submission is claimed. Git push
uses the existing configured route only; no trust or credential changes.

Operational lesson: preserve historical CLI error contracts while adding commands;
a passing new pipeline alone missed four existing string-contract assertions.
Restoring backward-compatible graph errors and rerunning the full suite resolved
the regression without weakening tests.

## 2026-09-28 — independent review after 0.2.0a1

Source inspection found substantive gaps despite the 297-test baseline: ambient
Decimal context affected validation, snapshot inputs bypassed scope/type checks,
raw RDF lacked selected factor/review literal shapes, and package/adapter parsing
needed bounded reads and normalized malformed-input errors. Repairs have independent
adversarial tests, not merely new expected outputs for the same ten seeds.
The full run observed 355 passing tests and 11 upstream deprecation warnings.
Build from sdist succeeded. Four CLI actions (validate, diff, package create/verify)
passed with socket connections blocked; initial harness assumptions about main's
return value and required data-version were corrected, not counted as passes.
The original reproducible SVG has a byte-equality test. No dependency change.
Gitleaks scanned all ten reachable commits and the complete intended publication
tree (~1.01 MB), finding no secrets. Semantic diff/path review found no private
ISO source, extracts, local user paths, credentials or copyrighted standards text.
Current normal gh API issue access still fails TLS certificate verification; no
bypass or trust change. SoftwareX official guide retrieval returned HTTP 403;
its current template is explicitly unverified, not fabricated. Alpha publishing
is authorized; research/domain gates and archival/submission gates remain distinct.
Final commit/push and hosted-CI readback are reported separately to avoid a
self-referential commit hash. Published 0.2.0a1 is not retroactively changed.

## 2026-09-28 — 0.3.0a1 real public-disclosure alpha

Scope baseline43f3027: additive reported-disclosure/1, explicit CLI/evidence workflow,
UMC Group and parent-only2022–2024 plus TSMC2023–2024, complete generated outputs,
independent numeric/adversarial tests and synchronized paper/release docs. Existing
calculated schema0.1 and ACME fixtures remain byte-unchanged. No raw company report,
ISO source/extract, credentials or private user context is bundled. Company PDFs
were inspected locally; exact source SHA256 values were independently recomputed.
Only24 attributable numeric facts, original mapping/limitation notes and derived
outputs are published. Company copyrights are not relicensed under project MIT.

Observed locally: Python3.12.14, uv0.12.19, Ruff0.16.9, pytest9.1.1, Gitleaks8.30.1.
448 tests pass with11 upstream RDFLib warnings, 7 docs-oracle tests pass, relative
links in176 Markdown files pass; Ruff lint/format and diff whitespace checks pass.
Independent review reproduced3 defects (ambient Decimal exponents, missing crate
software/command metadata, raw HTML in report); all19 independent review tests now
pass after fixes. No negative oracle was weakened. Dependency audit reports no known
vulnerabilities; the unpublished project itself is outside PyPI advisory coverage.
No dependency change; prior dependency-license review remains applicable.

Wheel built from sdist and installed with29 hashed runtime dependencies in a fresh
offline local environment. Full UMC Group and held-out TSMC workflows executed
outside the source checkout with Python socket/DNS access blocked and produced
byte-identical complete trees after freezing input metadata. A separate clean
publication copy performs locked offline installation/full tests. This is same-host
reproduction, not practitioner or fresh-host proof. CI now runs all3real cases and
uploads complete artifacts using a pinned action; remote execution is not inferred.

Publication-scope helper inspected344 intended UTF-8 files and231 historical blobs;
targeted privacy scan clear. Gitleaks tree scan~1.83MB and all11reachable baseline
commits~1.06MB found no secrets. Separate semantic review covered actual facts,
source URLs, report text, filenames, scripts, generated crate/vault metadata and
commit identities. Only intentional public company/source and GitHub attribution.
No report binaries are retained. Final staged/postcommit scans and remote SHA/tag
readback are reported externally to avoid a self-referential audit hash.

Normal authenticated GitHub API probe failed certificate verification. No TLS bypass,
trust edits, credential extraction or alternate authenticated HTTP route. Existing
Git transport and anonymous repository read succeed. GitHub Release object/assets,
issue closure, description/security-control updates remain API-blocked; a pushed tag
is not those operations. No journal/DOI action attempted. Gate A HOLD and standards/
comparability limitations remain. Parent independent review remains required.


## 2026-09-28 — API recovery and verified public prerelease
Earlier API/upload-blocked observations are historical. Normal authenticated CLI
access and uploads recovered after owner-approved narrowly scoped trust
synchronization. Four assets were uploaded and independently read back with exact
name, byte-size and SHA256 equality before publishing the existing draft as a
prerelease. Anonymous release-page retrieval returned HTTP 200. No broader trust,
TLS/proxy bypass, credential extraction or tag movement was used. Description and
issues #9/#10/#24 were reconciled within their exact scope; remaining research and
archive gates stand. See [release evidence](RELEASE_PUBLICATION_0.3.0a1.md).

## Original-criteria and manuscript checkpoint — 2026-09-28
Full original specification re-read; fresh-host released-source/wheel workflow committed at 82a7ea2. Hosted runs 36382755131 (tests/build/dependency audit), 36382755158 (docs), and 36382755169 (independently fetched released assets) all completed successfully. Local 448 tests, seven docs oracles, lint/format and source/wheel build passed. Local pip-audit could not finish because the existing proxy closed a PyPI connection; hosted audit passed instead. No TLS/proxy bypass or credential extraction. Normal Git push works; local gh API still fails certificate trust. Public API readback confirms actual CI and issue state; it does not authorize an alternate authenticated mutation route.

Software Heritage request 2510390 succeeded with a full visit and snapshot/release objects resolved to the exact released code; see ARCHIVE_STATUS.md. Source preservation does not imply DOI or binary retention. Initial complete manuscript is original text with original SVG figures and generated reading PDF, not licensed standards/report/template redistribution. Human authorship/declarations remain unconfirmed. Preserve historical audits above as dated evidence, not current-state assertions.

Final original manuscript PDF was regenerated from the committed Markdown renderer: native PDFKit extracted 24,222 characters across nine pages, including new fresh-host run identifier and final reference; targeted private-path checks clear. It is the sole deliberately included original PDF, not a third-party source/standard/template. The publication scope checker flags PDFs/binaries for manual review by design; this reviewed generated reading artifact is an explicit exception, not a weakening of the checker.

## 2026-09-28 — 0.4.0a1 synthetic-only worked-example replacement

The current tree removes 213 company-example files (including 207 generated outputs),
the company source catalogue, runner and company-specific oracle. The generic
reported-disclosure API is retained; anonymous invented fixtures preserve missingness,
boundary separation, Scope 2 alternatives and unknown-causality regressions. Historical
v0.3.0a1 tags/releases and the pinned historical reproduction harness are unchanged.
Their observations are not current-release external validation.

The new runner executes 73 actual CLI actions with Python socket/DNS access blocked
before application imports (not an OS sandbox). It materializes and hash-checks 45
local synthetic source records, records seven fictional semantic declarations, checks
all 45 arithmetic results independently, and exports three verified crates and three
258-note vaults. Totals 3820/3850/4060 and deltas 30/210 agree with literal oracles.
Double-GWP and missing-factor-source controls each exit 1; nonempty output is rejected.
A new environment installed 29 locked hashed runtime dependencies offline and the
0.4.0a1 wheel without dependencies. Two complete executions produced byte-identical
1,023-file output trees. This is isolated same-host wheel proof, not external review.
Only a bounded readable sample subset is committed; the complete report is unedited.

Documentation link oracle and seven negative documentation tests, Ruff lint/format,
source/wheel build and diff whitespace checks passed. Gitleaks scanned the current
tree and all 16 reachable prior commits without findings. The targeted semantic scan
inspected 238 intended files and 479 historical blobs; its only exceptions were the
intentionally generated manuscript PDF (blanket PDF/binary policy). Its renderer,
source manuscript, PDFKit text check and nine nonempty pages establish original
project authorship; no licensed standard or company PDF is included. HTML/SVG byte
reproduction is tested; browser PDF metadata is not claimed byte-deterministic.

Normal gh API access was retried and failed x509 trust. No trust store, proxy, TLS or
credential configuration was changed. New release API publication is blocked; source
Git publication and observed current CI are tracked separately. Do not present the
old release assets as the new version or claim a new release exists without readback.

Final local suite: **458 passed**, 11 upstream RDFLib deprecation warnings; seven
documentation-oracle tests passed. The new runner regression includes actual CLI
exit checks, two different hash-seed byte-tree replays, exact component oracles,
source/declaration hashes, package/vault checks and untouched nonempty destinations.
