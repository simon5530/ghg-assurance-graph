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
