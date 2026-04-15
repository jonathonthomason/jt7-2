# JT7 Multi-Surface Implementation Spec

## Purpose
This document defines the implementation-ready spec for JT7 multi-surface routing, scoped conversations, explicit context portability, and cross-surface handoff behavior.

It is designed for:
- clean domain separation
- explicit shared context
- low operational ambiguity
- tenant-safe orchestration
- future productization

---

## 1. Design Decision

### Chosen model
**Scoped conversation surfaces with explicit context portability**

### Core behavior
- each surface owns a domain
- each surface has a default agent
- work stays in-surface by default
- cross-surface movement is explicit
- shared context is explicit
- all handoffs are auditable
- all surfaces run through one unified platform core

### Default tenant
- `JT_PERSONAL`

---

## 2. Surface Model

### Platform Agent
**Domain:** `platform`

Scope:
- system architecture
- schemas
- workflows
- orchestration
- infrastructure
- OpenClaw configuration
- platform debugging
- routing and handoff control

### Job Ops Agent
**Domain:** `job_ops`

Scope:
- application tracking
- recruiter interactions
- follow-ups
- interviews
- drafts
- daily job operations

### Life Agent
**Domain:** `life`

Scope:
- routines and habits
- wellness / faith / sobriety support
- personal admin
- life operating support

### TA Knowledge Agent
**Domain:** `knowledge`

Scope:
- transcript ingestion
- synthesis
- learning capture
- reference material
- structured retrieval

---

## 3. Canonical Schemas

## `channel_surface`
Required fields:
- `channel_id`
- `tenant_id`
- `provider`
- `surface_type`
- `surface_name`
- `default_domain`
- `default_agent_id`
- `allowed_agent_ids`
- `handoff_mode`
- `status`

Optional fields:
- `escalation_agent_id`
- `approval_policy_id`
- `notes`

---

## `conversation_context`
Required fields:
- `conversation_id`
- `channel_id`
- `tenant_id`
- `active_domain`
- `active_agent_id`
- `context_scope`
- `lock_state`
- `status`

Optional fields:
- `handoff_state`
- `last_run_id`
- `notes`

---

## `handoff_record`
Required fields:
- `handoff_id`
- `tenant_id`
- `source_conversation_id`
- `source_agent_id`
- `target_agent_id`
- `source_domain`
- `target_domain`
- `handoff_reason`
- `context_mode`
- `status`
- `created_at`

Optional fields:
- `target_conversation_id`
- `context_ref`
- `notes`

---

## `shared_context_bundle`
Required fields:
- `bundle_id`
- `tenant_id`
- `source_conversation_id`
- `source_agent_id`
- `context_mode`
- `included_domains`
- `summary`
- `created_at`

Optional fields:
- `target_conversation_id`
- `target_agent_id`
- `included_decisions`
- `included_state`
- `included_constraints`
- `included_artifacts`
- `expires_at`
- `notes`

---

## 4. Core Modules

## `channel_router`
Purpose:
Map inbound message/thread to tenant, domain, and agent defaults.

Outputs:
- resolved `channel_surface`
- normalized routing envelope
- target domain
- target default agent

## `context_scope_manager`
Purpose:
Ensure surface stays in scope unless an explicit handoff/share request exists.

Outputs:
- `allow`
- `deny`
- `handoff_recommended`
- `handoff_required`

## `conversation_handoff`
Purpose:
Transfer work between surfaces cleanly.

Outputs:
- `handoff_record`
- optional `shared_context_bundle`
- updated source/target surface state

## `surface_policy_enforcer`
Purpose:
Apply per-surface operating rules.

## `workflow_orchestrator`
Purpose:
Coordinate multi-domain requests without breaking explicit ownership.

---

## 5. Routing Rules
- identify current surface domain
- check whether request belongs there
- if yes, execute normally
- if no, create explicit handoff
- do not silently switch domains

### Platform-specific rule
Platform is the control plane.
It owns routing and correction, but does not become the worker by default.

---

## 6. Context Rules

### Shared context
Global across all surfaces:
- user goals
- system rules
- major decisions
- identity and priorities

### Thread-local context
Local to one surface:
- active tasks
- recent actions
- domain-specific state

### Rule
Thread-local context moves only via explicit handoff or shared context bundle.

---

## 7. Handoff Rules
A handoff must:
- state that handoff is happening
- explain why
- identify target surface
- package context cleanly
- preserve traceability
- avoid duplicate ownership

---

## 8. Success Condition
The system behaves like one coordinated product platform with:
- focused surfaces
- reusable logic
- explicit routing
- explicit context movement
- shared memory without uncontrolled bleed
