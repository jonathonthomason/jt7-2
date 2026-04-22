# external_action_guard

## Purpose
Enforce approval, audit, and policy boundaries before any high-impact external action is executed.

This module exists to prevent unsafe or ambiguous external commits.

---

## Inputs
- tenant_id
- requester_actor_id
- requester_actor_type
- target_integration
- action_type
- target_resource_ref
- payload_summary
- payload_ref
- risk_level
- applicable capability policy

---

## Outputs
- allow
- deny
- approval_required
- external_action_request
- approval_request linkage if needed
- audit trigger

---

## Dependencies
- `schemas/external_action_request.md`
- `schemas/approval_request.md`
- `schemas/permission_policy.md`
- `schemas/integration_capability.md`
- `tenants/JT_PERSONAL/integration_permissions.md`
- `tenants/JT_PERSONAL/jobboard_access_matrix.md`

---

## Side Effects
- creates `external_action_request` for send/mutate actions
- may create approval request
- emits audit event before and after execution
- blocks execution if policy is not satisfied

---

## Evaluation Logic

### Step 1 — Resolve capability class
Determine whether the requested action is:
- read
- organize
- draft
- write
- send
- mutate

### Step 2 — Resolve tenant policy
Load capability and approval posture for:
- integration domain
- action class
- requesting bot/agent

### Step 3 — Determine execution path
Possible paths:
- direct_allow
- allow_with_audit
- require_approval
- deny

### Step 4 — Create request object if needed
If action class is `send` or `mutate`:
- create `external_action_request`
- attach payload summary and refs
- mark status as pending if approval is required

### Step 5 — Gate execution
- deny if policy disallows
- pause if approval required
- allow only when policy and approval conditions are satisfied

---

## Default Rules

### Allowed without approval by default
- read
- some low-risk draft actions

### Approval-aware by default
- organize
- write
- authenticated browser reads

### Approval-required by default
- send
- mutate
- jobboard submission
- recruiter message send
- external account state change

---

## Failure Modes
- missing capability policy
- tenant mismatch
- requester not allowed
- high-risk action without approval
- malformed payload summary or target resource

---

## Success Condition
External action proceeds only when:
- tenant policy allows it
- requester is authorized
- approval is satisfied if required
- audit path exists

---

## Status
- state: defined
- implementation_phase: execution boundary ready
