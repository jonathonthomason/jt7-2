# JT7 Four-Surface OpenClaw Implementation Plan

## Purpose
This document maps the JT7 four-surface model into an OpenClaw implementation plan.

It focuses on:
- OpenClaw representation of conversation surfaces
- routing assumptions
- config vs logic boundaries
- implementation order
- validation steps

---

## 1. Objective

Implement four separate domain surfaces:
- JT7 Platform Bot
- JT7 Job Ops Bot
- JRT7 Life Bot
- JT7 TA Knowledge Bot

while preserving:
- one shared JT7 core
- one tenant model
- one orchestration model
- one audit model
- one gateway/runtime path

---

## 2. Desired Runtime Shape

```text
Telegram Bot: JT7 Platform      --->
Telegram Bot: JT7 Job Ops       --->
Telegram Bot: JRT7 Life         --->  OpenClaw Runtime  ---> JT7 Shared Core
Telegram Bot: JT7 TA Knowledge  --->
```

JT7 Shared Core contains:
- surface resolver
- routing logic
- scope enforcement
- handoff logic
- shared context bundle logic
- orchestrator
- audit layer

---

## 3. OpenClaw Representation Model

## Surface = inbound channel surface
Each Telegram bot becomes a distinct inbound surface.

Each surface must resolve to:
- `tenant_id`
- `bot_surface_id`
- `default_domain`
- `default_agent_id`
- `allowed_agent_ids`

### Required logical mappings
- `telegram:jt7_platform_bot`
- `telegram:jt7_job_ops_bot`
- `telegram:jrt7_life_bot`
- `telegram:jt7_ta_knowledge_bot`

---

## 4. What Must Be Configured in OpenClaw

## A. Separate Telegram bot connections
OpenClaw must be able to receive inbound messages from 4 Telegram bot identities.

### Required
- separate bot tokens
- separate inbound surface identities
- stable mapping from bot identity to logical bot surface id

---

## B. Surface identity resolution
JT7 needs enough inbound metadata to distinguish which bot received the message.

### Required metadata
- provider = telegram
- bot/account identity
- chat_id
- sender_id
- thread/surface identity if applicable

### Outcome
JT7 can resolve:
- which bot surface is active
- which default domain to use
- which agent should own the message by default

---

## C. Cross-session / cross-surface messaging
OpenClaw must support structured routing from one visible surface/session to another.

### Required capability
- send from current session into target surface session
- target by stable label or session key
- preserve enough metadata for handoff records

### Likely mechanism
- `sessions_send`
- session labels
- session visibility discovery

---

## 5. What Must Be Implemented in JT7 Logic

## A. Surface resolver
JT7 must map inbound bot identity to a configured bot surface.

### Inputs
- inbound metadata
- tenant config

### Outputs
- bot surface record
- tenant id
- default domain
- default agent

---

## B. Scope enforcement
JT7 must decide whether work is:
- in-scope
- out-of-scope
- requires handoff
- requires shared context bundle

---

## C. Cross-surface handoff
JT7 must support:
- `handoff`
- `share context`
- `continue in other bot`

using structured records and bundles.

---

## D. Shared context bundle generation
JT7 must create compact explicit bundles rather than relying on ambient thread memory.

---

## 6. What Stays in Tenant Config

Tenant config owns:
- surface definitions
- default domain per surface
- default agent per surface
- allowed agents per surface
- handoff defaults
- escalation behavior

Primary file:
- `tenants/JT_PERSONAL/bot_surfaces.md`

---

## 7. Implementation Breakdown

## Phase 1 — Surface connectivity

### Tasks
- create 4 Telegram bots
- connect all 4 to OpenClaw
- verify inbound routing works independently

### Success criteria
- each bot can receive and send messages independently
- OpenClaw can distinguish the surfaces reliably

---

## Phase 2 — Surface mapping

### Tasks
- define logical surface registry
- map each Telegram bot to one `bot_surface_id`
- assign default domain and default agent

### Success criteria
- inbound message can be resolved to the correct surface automatically

---

## Phase 3 — Scope enforcement

### Tasks
- implement or encode surface policy rules
- lock Platform to platform domain
- lock Job Ops to job_ops domain
- scope Life to life domain
- scope TA Knowledge to knowledge domain

### Success criteria
- out-of-scope work is not silently handled in the wrong surface

---

## Phase 4 — Cross-surface handoff

### Tasks
- implement handoff records
- implement shared context bundles
- implement continue-in-other-bot behavior
- implement target surface resolution

### Success criteria
- user can explicitly move work between surfaces
- target surface receives structured payload
- source surface records transfer cleanly

---

## Phase 5 — Shared context control

### Tasks
- support `summary_only` as default bundle mode
- support `shared_explicit` on explicit request
- ensure no silent context bleed
- separate shared context from thread-local state

### Success criteria
- user can share context intentionally without losing clean boundaries

---

## 8. Recommended Session / Surface Labeling
- `JT7 Platform Bot`
- `JT7 Job Ops Bot`
- `JRT7 Life Bot`
- `JT7 TA Knowledge Bot`

---

## 9. Cross-Surface Routing Rules

## Default rule
Stay in current surface.

## If request is out of scope
Recommend:
- handoff
- share context
- continue in other bot

## If user explicitly requests movement
Use the requested command semantics.

## If request spans multiple domains
Use orchestrator logic to:
- split into domain-specific work
- route to proper surfaces
- preserve audit trail

---

## 10. Failure Modes

## Failure 1 — wrong surface mapping
### Mitigation
- explicit surface registry
- stable labels
- fail closed if ambiguous

## Failure 2 — silent domain drift
### Mitigation
- surface policy enforcement
- lock/scoped behavior

## Failure 3 — broken cross-surface targeting
### Mitigation
- stable labels
- session discovery rules
- explicit fail state on ambiguity

## Failure 4 — excessive context bleed
### Mitigation
- default `summary_only`
- explicit `shared_explicit` only by request
- hard separation between shared and thread-local context

---

## 11. Bottom Line
The goal is not four assistants.
The goal is one platform with four disciplined surfaces.
