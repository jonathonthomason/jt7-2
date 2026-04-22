# JT_PERSONAL jobboard_access_matrix

## Purpose
Defines access classes, permissions, and risk posture for job-board and recruiting platforms.

---

## Access Classes

### Class A — Read / Ingest
Capabilities:
- read listings
- search roles
- normalize role metadata
- dedupe opportunities
- score or rank opportunities

### Class B — Authenticated Read / Apply Assist
Capabilities:
- authenticated dashboard read
- saved jobs read
- application-status read
- profile-aware autofill assistance
- draft preparation

### Class C — External Commit / Mutation
Capabilities:
- submit application
- send recruiter message
- update external account state
- save or unsave external platform state

---

## LinkedIn
- platform: linkedin
- class_a: allowed
- class_b: allowed_with_approval
- class_c: approval_required
- preferred_bot: jt7_job_ops_bot
- notes: use for discovery, status reading, and application-assist before any direct commit

## Indeed
- platform: indeed
- class_a: allowed
- class_b: allowed_with_approval
- class_c: approval_required
- preferred_bot: jt7_job_ops_bot
- notes: allow listing ingestion and dashboard/status support before submission actions

## Workday
- platform: workday
- class_a: limited
- class_b: allowed_with_approval
- class_c: approval_required
- preferred_bot: jt7_job_ops_bot
- notes: authenticated workflow likely needed; treat submit actions as high risk

## Built In
- platform: builtin
- class_a: allowed
- class_b: limited
- class_c: approval_required
- preferred_bot: jt7_job_ops_bot
- notes: prioritize listing ingestion and role normalization

## Otta
- platform: otta
- class_a: allowed
- class_b: allowed_with_approval
- class_c: approval_required
- preferred_bot: jt7_job_ops_bot
- notes: status/dashboard read may be useful before direct mutation

## Creative Circle
- platform: creative_circle
- class_a: allowed
- class_b: allowed_with_approval
- class_c: approval_required
- preferred_bot: jt7_job_ops_bot
- notes: recruiter/staffing workflows may require portal-aware handling

---

## Shared Jobboard Rules

### Rule 1
All jobboard reads and ingestion should route through Job Ops by default.

### Rule 2
Authenticated read should be approval-aware because it depends on account/session context.

### Rule 3
Application submission and external account mutation require approval and audit.

### Rule 4
If a platform lacks stable API support, browser automation should still honor the same permission classes.

---

## Status
- state: defined
- implementation_phase: jobboard permission matrix ready
