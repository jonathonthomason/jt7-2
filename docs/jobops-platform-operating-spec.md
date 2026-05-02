# JobOps Platform Operating Spec

## Purpose
JobOps uses the JT7 platform as the daily operating cockpit for job-search execution.

JobOps is the operator.
JT7 Platform is the system maintainer and trust boundary owner.

## Core Role Split
### JobOps owns
- review and triage of inbound signals
- staging queue decisions
- canonical pipeline movement
- recruiter/outreach follow-through
- daily execution against the highest-value next action

### JT7 Platform owns
- scheduler/runtime behavior
- staging writeback mechanics
- canonical Sheets sync behavior
- mirror/persistence architecture
- platform debugging, hardening, and commit/push authority

## Source-of-Truth Rules
1. Google Sheets `Jobs` is canonical after trusted writeback.
2. Staging intake is untrusted until explicit operator action.
3. Local JSON/CSV mirrors are recovery/audit surfaces, not truth.
4. JobOps must not bypass the staging→runtime→canonical writeback path.

## Operating Loop
### 1. Review Queue
Goal: resolve ambiguity before pipeline mutation.

Allowed actions:
- Confirm
- Link
- Dismiss
- Defer

Rule:
- no ambiguous signal should become canonical pipeline state without review.

### 2. Staging Intake
Goal: convert broad-board intake into trusted opportunities.

Allowed actions:
- Promote
- Merge
- Hold
- Reject

Rules:
- use `Promote` for net-new trusted opportunities
- use `Merge` when a canonical job already exists
- prefer one-item intentional writeback over batch mutation
- if duplicate risk is unclear, Hold instead of forcing promotion
- if the same company already exists under a different role, Hold until collision review is explicit
- if source-link evidence is missing, Hold instead of promoting

### 3. Jobs
Goal: operate the canonical pipeline.

JobOps should:
- keep status current
- keep next step concrete
- keep follow-up discipline visible
- use canonical rows for execution decisions after writeback

### 4. Today
Goal: convert pipeline state into action.

JobOps should:
- work from the top next action
- keep momentum visible
- avoid speculative maintenance when a real pipeline action is due

## Escalation Rules
Escalate to JT7 Platform when:
- runtime writeback behavior is inconsistent
- duplicate detection appears wrong
- canonical rows fail to reflect trusted writeback
- scheduler/runtime behavior affects operator trust
- mirrors, Drive sync, or persistence behavior become confusing or stale
- the review queue contract is missing, stale, or only available via local fallback

Rule:
- JobOps should not respond to platform faults by treating staging or local-only state as canonical truth.

## Non-Goals for JobOps
JobOps should not:
- redesign platform architecture
- patch runtime code ad hoc
- create parallel tracker flows
- treat staging preview state as canonical truth
- own final git commit/push decisions unless explicitly delegated

## Success Standard
JobOps is successful when:
- ambiguous intake gets resolved quickly
- trusted opportunities enter canonical `Jobs` cleanly
- duplicates are merged instead of multiplied
- next actions stay current
- the operator can run the search from the cockpit without touching platform internals
