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
