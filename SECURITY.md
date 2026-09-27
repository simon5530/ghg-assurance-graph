# Security policy

This experimental Phase 1 pre-alpha provides no production security guarantee.
Only the current main-branch prototype is maintained. No credentials, corporate
inventories, personal data, live exports, or private infrastructure identifiers
belong in this repository. Future parsers and adapters must treat inputs as untrusted.

Do not file secrets or exploit details in public issues. Use [GitHub private
vulnerability reporting](https://github.com/simon5530/ghg-assurance-graph/security/advisories/new),
verified enabled on 2026-09-26 (Asia/Taipei). Never submit confidential inventory
evidence to the project; include only a minimal synthetic security reproduction.

Before publication, review every file and reachable commit for semantic privacy,
scan tree and full Git history with Gitleaks, review licenses and metadata, and run
the documented checks from an isolated checkout. A scanner pass is not a privacy
proof. Remote protection settings and anonymous access need separate verification.

The system is intended to assist evidence review, not to certify inventories,
replace competent assurance professionals, or issue legal/compliance determinations.
AI-generated explanations must never become the authority for calculations or rules.

## Phase 3 query boundary
Only packaged SELECT templates and validated URN bindings are accepted; no raw
SPARQL, SERVICE, UPDATE, RDF import, remote contexts or evidence URL fetching.
Explicit local input files remain operator-controlled, not a filesystem sandbox.
Errors omit input paths/content. Review and provenance assertions are not signatures.
