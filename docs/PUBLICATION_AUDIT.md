# Publication audit — 2026-09-25

Scope: this standalone project only, original Phase 0 documentation/check scripts. No domain software, benchmark data, third-party implementation or private attachment is bundled. Final local verification evidence will be recorded below; remote publication is blocked.

## Remote blocker
`gh repo view simon5530/ghg-assurance-graph --json nameWithOwner,visibility,url` failed with an untrusted api.github.com certificate. `gh auth status` also reported an invalid credential; because transport verification fails, credential invalidity is not independently established. The supported identity status sees a native account but exposes no repository mutation operation in this session. Existing-session browser connection failed because Chrome was unavailable. No TLS verification was disabled; no credential was extracted or copied; no alternate raw authenticated API was attempted.

No remote mutation was made. Repository existence, PUBLIC visibility, branch/SHA/file set, milestone/issue counts, hosted CI and GitHub security controls are **unverified**. Local 11/30 manifest counts must not be reported as GitHub counts. Before any future create, read existing repository/milestones/issues and reconcile exact titles/IDs; never blindly duplicate them.

## Review scope and limitations
All original scaffold text, roadmap and research draft were read. New text was reviewed for private paths/identifiers, unsupported claims and licensing. Public account handle and third-party author/repository identifiers are intentional attribution. No personal contact details, local operational endpoints, raw conversation, attachment, datasets or screenshots are intended for publication. MIT applies to original work only; cited AGPL/custom-licensed projects are not copied. No third-party runtime dependencies exist; dependency vulnerability audit is not applicable to this stdlib-only scaffold. CI action revisions are pinned; hosted execution is not verified.

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

No server/authorization/persistence path exists, so service unauthorized/restart tests are not applicable. Same-machine isolated-clone documentation reproduction is distinct from a fresh-machine scientific reproduction.
