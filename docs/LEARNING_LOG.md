# Learning Log

Status: Phase 0 planning; domain features are not implemented.

## 2026-09-24 — Separate a scaffold from research evidence
A working documentation check demonstrates repository consistency, not scientific
validity. Keep implementation, evaluation, novelty, and publication gates independent.
A local isolated checkout demonstrates portability of the docs check, not a
fresh-machine scientific reproduction. Preserve these distinctions in later PRs.

Future entries should record question → evidence → decision → limitation, linking
versioned artifacts rather than copying operational logs or private context.

## 2026-09-25 — publication evidence chain
Symptom: prior status conflated local files with published artifacts. Cause: no
remote-state oracle. Cheapest check: query repository visibility, remote SHA and
issue/milestone counts before reporting public completion. Safe recovery: complete
local review, preserve HOLD and report authentication/transport blockers. Completion
proof requires matching reviewed SHA/file set plus anonymous visibility and counts.
A README badge is not publication evidence; use publisher/DOI records.

## 2026-09-26 — Verify writes with independent readback
A completed API mutation is not its acceptance oracle. Read back exact titles, IDs,
labels, milestone assignments and issue contracts; compare remote blob hashes with
the reviewed tree and verify anonymous access and the CI head SHA. Nullable API
fields need value checks: an issue with `pull_request: null` is not a pull request.
An initial count assertion used field presence and excluded valid issues; read-only
inspection identified this, and reconciliation completed without duplicate writes.
Optional security flags returned successful mutation responses but remained disabled
on readback; retain that limitation instead of declaring every control enabled.
