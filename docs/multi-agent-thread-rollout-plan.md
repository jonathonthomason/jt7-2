# JT7 Multi-Surface Rollout Plan

## Purpose
This document defines the rollout sequence for implementing JT7 multi-surface routing in OpenClaw.

It focuses on:
- implementation order
- configuration touchpoints
- operational safety
- failure modes
- testing

---

## 1. Rollout Goal

Move from:
- one generalized thread
- implicit domain switching
- unclear cross-thread ownership

To:
- explicit domain surfaces
- scoped surface behavior
- structured handoff
- explicit shared context
- audit-safe orchestration
- one unified platform core

---

## 2. Rollout Principles
1. keep one orchestration core
2. define surfaces before adding more workers
3. isolate by default
4. share context only explicitly
5. log all cross-surface transitions
6. keep human-visible behavior predictable

---

## 3. Implementation Order

## Phase 1 — Configuration foundation
### Deliverables
- surface registry
- conversation context model
- domain-to-surface mapping
- default tenant mapping

### Exit criteria
- every inbound surface can be mapped to one domain and one default agent

---

## Phase 2 — Scope enforcement
### Deliverables
- context scope manager
- surface policy enforcer
- out-of-scope detection

### Exit criteria
- platform stays platform-scoped
- job ops stays job-ops-scoped
- life stays life-scoped
- knowledge stays knowledge-scoped
- system recommends handoff instead of drifting silently

---

## Phase 3 — Handoff and shared context
### Deliverables
- handoff record model
- shared context bundle model
- conversation handoff module
- share-context workflow
- continue-in-other-bot workflow

### Exit criteria
- user can explicitly handoff work
- user can explicitly share context
- user can continue work in another surface with continuity

---

## Phase 4 — Orchestrator integration
### Deliverables
- routing decision schema
- agent run schema
- agent selector
- result merger
- orchestrator state machine
- permission/approval enforcement

### Exit criteria
- multi-domain requests can be split intentionally
- cross-surface movement is orchestrated and auditable

---

## Phase 5 — Runtime hardening
### Deliverables
- failure handling rules
- retry policy per workflow
- audit verification rules
- operator-visible recovery paths

### Exit criteria
- failures are predictable, bounded, and reviewable

---

## 4. Initial Surface Setup Sequence

### Surface 1 — Platform
Purpose:
- architecture
- orchestration
- infra/config
- debugging

### Surface 2 — Job Ops
Purpose:
- live job operations

### Surface 3 — Life
Purpose:
- life systems and personal admin

### Surface 4 — TA Knowledge
Purpose:
- transcript intelligence and knowledge retrieval

---

## 5. OpenClaw Configuration Touchpoints
- inbound metadata resolution
- session labeling
- session routing
- cross-session messaging
- audit persistence

---

## 6. Key Failure Modes
- silent surface drift
- wrong surface mapping
- broken handoff targeting
- excessive context bleed
- duplicated ownership after transfer

---

## 7. Bottom Line
Roll out surfaces as disciplined entry points into one JT7 platform, not as separate assistants.
