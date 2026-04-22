# jobboard_router

## Purpose
Resolve jobboard-related requests into the correct access path, permission class, and execution model.

This module separates:
- listing ingestion
- authenticated dashboard reads
- apply-assist flows
- external submission/mutation flows

---

## Inputs
- tenant_id
- requester_actor_id
- requester surface or bot
- target platform
- requested action
- account/session context
- payload or search query

---

## Outputs
- platform classification
- access class
- execution path
- approval requirement
- target downstream module or integration path

---

## Dependencies
- `tenants/JT_PERSONAL/jobboard_access_matrix.md`
- `tenants/JT_PERSONAL/integration_permissions.md`
- `schemas/integration_capability.md`
- `schemas/external_action_request.md`
- `modules/external_action_guard.md`

---

## Side Effects
- may route search/read to ingestion workflows
- may route authenticated status lookups to approval-aware path
- may create external action request for commit actions
- may emit audit record

---

## Access Classes

### Class A — Read / Ingest
Examples:
- search roles
- ingest listings
- normalize metadata
- dedupe roles
- score roles

Execution path:
- direct or orchestrated read pipeline

### Class B — Authenticated Read / Apply Assist
Examples:
- read saved jobs
- read application dashboards
- prepare autofill assistance
- extract status from authenticated portals

Execution path:
- approval-aware authenticated path
- browser/session-sensitive route if needed

### Class C — External Commit / Mutation
Examples:
- submit application
- send recruiter message via platform
- mutate external account/application state

Execution path:
- must pass through `external_action_guard`
- approval required by default

---

## Platform Resolution Rules

### LinkedIn
- discovery and listing ingestion allowed
- authenticated dashboard/support actions are approval-aware
- direct apply or mutation requires approval

### Indeed
- discovery and ingestion allowed
- authenticated workflows are approval-aware
- submission requires approval

### Workday
- often requires authenticated portal flow
- status read is approval-aware
- submission is approval-required

### Built In
- prioritize listing ingestion and normalization
- commit actions remain approval-gated

### Otta
- listing + dashboard support allowed through approval-aware path
- commit actions require approval

### Creative Circle
- recruiter/staffing workflows may mix read and portal actions
- commit actions require approval

---

## Decision Logic

### Step 1
Resolve target platform.

### Step 2
Map requested action to access class:
- Class A
- Class B
- Class C

### Step 3
Check jobboard access matrix and capability policy.

### Step 4
Route to appropriate path:
- ingestion/read workflow
- authenticated read/apply-assist path
- external_action_guard

### Step 5
Return structured execution decision.

---

## Success Condition
The requested jobboard action is routed to the correct execution path with the correct approval and audit posture.

---

## Status
- state: defined
- implementation_phase: jobboard execution boundary ready
