# external_action_approval_flow

## Purpose
Define the approval-gated workflow for executing high-impact external actions safely and consistently.

This workflow connects:
- request generation
- policy evaluation
- approval gating
- execution authorization
- audit logging
- post-action verification

---

## Workflow ID
- `external_action_approval_flow`

---

## Trigger Condition
Starts when a bot or agent attempts a high-impact action such as:
- send email
- submit application
- mutate external account state
- confirm/decline an external event
- move or reorganize high-impact external assets

---

## Inputs
- tenant_id
- requester_actor_id
- requester_actor_type
- source bot surface
- target integration
- action_type
- target_resource_ref
- payload_summary
- payload_ref
- risk_level

---

## Outputs
- external_action_request
- approval decision state
- execution authorization or denial
- audit log linkage
- post-action verification result

---

## Modules Involved
1. `jobboard_router` or relevant domain router
2. `external_action_guard`
3. `approval_router`
4. execution layer (future actual integration call)
5. `audit_and_verification`

---

## Sequence

### Step 1 — Action request enters workflow
A surface-specific bot requests an external action.

Examples:
- Job Ops wants to submit a LinkedIn application
- Job Ops wants to send a recruiter email
- Planning wants to create a cross-domain high-impact mutation

### Step 2 — Route and classify
The relevant router classifies:
- target platform
- action class
- risk level
- whether the action is read, organize, write, send, or mutate

### Step 3 — Guard evaluation
`external_action_guard` evaluates:
- capability policy
- tenant rules
- allowed subject ids
- approval requirement
- audit requirement

### Step 4 — Create `external_action_request`
If action is high-impact:
- create `external_action_request`
- assign pending / approval-required state as needed
- attach payload summary and refs

### Step 5 — Approval routing
If approval is required:
- `approval_router` creates and manages approval request
- workflow pauses until resolution

### Step 6 — Approval resolution
Possible results:
- approved
- denied
- expired
- canceled

### Step 7 — Execution authorization
If approved or otherwise allowed:
- workflow may proceed to execution layer
- execution remains out of scope for this current design phase, but the contract is defined here

### Step 8 — Audit and verification
After execution:
- log audit record
- verify result if possible
- mark external_action_request as executed / failed

---

## Decision States

### direct_allow
Use when:
- policy allows action
- approval not required
- risk is low enough

### approval_required
Use when:
- action class is `send` or `mutate`
- policy explicitly requires approval
- risk level is medium/high

### deny
Use when:
- capability policy disallows action
- tenant mismatch exists
- requester is out of scope
- payload is malformed or unsafe

---

## Success Condition
Workflow succeeds when:
- request is classified
- policy is evaluated
- approval is obtained if required
- action is authorized
- audit record is written
- verification result is captured

---

## Failure Condition
Workflow fails when:
- policy denies action
- approval is denied or expires
- external execution fails
- verification fails
- audit linkage cannot be written

---

## Retry Rules
Retries are allowed only for:
- transient execution failure
- transient verification failure
- temporary platform/auth/session issues

Retries are not allowed automatically for:
- denied approval
- missing permission
- unsafe payload
- tenant mismatch

---

## Ownership Model

### Platform Bot
May define and govern the workflow, but should not usually be the routine requester for external commits.

### Job Ops Bot
Primary owner for:
- jobboard submission requests
- recruiter message send requests
- external job/account workflow requests

### Planning Bot
May trigger the workflow only when coordinating or escalating, not as default execution owner.

---

## Visual Flow

```text
+-------------+
| Source Bot  |
+-------------+
       |
       v
+------------------+
| Domain Router    |
+------------------+
       |
       v
+----------------------+
| external_action_guard |
+----------------------+
       |
       +----------------------+
       |                      |
       v                      v
+-------------+         +----------------+
| Direct Allow|         | approval_router|
+-------------+         +----------------+
       |                      |
       |                      v
       |               +----------------+
       |               | approval result|
       |               +----------------+
       |                      |
       +-----------+----------+
                   |
                   v
          +-------------------+
          | execution layer   |
          +-------------------+
                   |
                   v
          +----------------------+
          | audit_and_verification|
          +----------------------+
                   |
                   v
          +-------------------+
          | final status      |
          +-------------------+
```

---

## Shared Rules

### Rule 1
All high-impact external actions must become explicit requests before execution.

### Rule 2
No send or mutate action should bypass approval logic when policy says approval is required.

### Rule 3
Execution without audit linkage is invalid.

### Rule 4
This workflow is reusable across:
- Gmail outbound actions
- jobboard submissions
- event response commits
- external account mutations

---

## Status
- state: defined
- implementation_phase: approval-gated external action workflow ready
