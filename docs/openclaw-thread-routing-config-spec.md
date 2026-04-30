# OpenClaw Thread Routing Config Spec

## Purpose
This document defines the configuration-level requirements for supporting JT7 multi-surface routing inside OpenClaw.

It separates:
- what belongs in OpenClaw platform/runtime configuration
- what belongs in JT7 orchestration logic
- what belongs in tenant/domain policy

---

## 1. Goal

Enable multiple thread or bot surfaces such that:
- each surface maps to a domain
- each surface maps to a default agent
- scope is preserved by default
- context sharing is explicit
- handoffs are structured
- orchestration remains centralized
- all surfaces run through one platform core

Important clarification:
- one user-facing bot can technically front multiple internal agents
- but each bot surface should still map to one primary domain/default agent for user-facing clarity

---

## 2. Routing Layers

## Layer A — OpenClaw runtime routing
Responsibility:
- receive inbound messages
- expose stable thread/channel identifiers
- preserve provider metadata
- support cross-session/thread messaging
- support session labeling and targeting

## Layer B — JT7 routing logic
Responsibility:
- interpret inbound surface as `channel_surface`
- resolve domain and default agent
- enforce scope policy
- create handoffs and bundles
- call orchestrator when needed

## Layer C — Tenant/domain policy
Responsibility:
- define which surfaces exist
- define allowed agents
- define lock rules
- define approval rules

---

## 3. Required OpenClaw Capabilities

## Capability 1 — Stable surface identity
OpenClaw must expose enough metadata to identify:
- provider
- chat_id
- bot identity or thread identity
- label/name if available

### Required outcome
JT7 can construct a stable `channel_id` like:
- `telegram:jt7_platform_bot`
- `telegram:jt7_job_ops_bot`
- `telegram:jrt7_life_bot`
- `telegram:jt7_ta_knowledge_bot`

---

## Capability 2 — Session targeting
OpenClaw must support routing work to a specific visible session/thread.

### Required outcome
JT7 can:
- send work to another surface/session
- resume structured work there
- avoid freeform manual copy/paste

### Current likely mechanism
- `sessions_send`
- session labels / session keys

---

## Capability 3 — Session labeling
Each surface/session should have a stable logical label.

### Required labels
- `JT7 Platform Bot`
- `JT7 Job Ops Bot`
- `JRT7 Life Bot`
- `JT7 TA Knowledge Bot`

---

## Capability 4 — Cross-session messaging
OpenClaw must support sending structured handoff/context messages across surfaces.

### Required outcome
JT7 can issue:
- handoff payload
- shared context bundle payload
- continue-in-other-bot payload

without pretending the message itself is the full audit model.

---

## Capability 5 — Delegated execution visibility
If one surface delegates work to another, OpenClaw should preserve enough run/session visibility to:
- confirm target exists
- send work to target
- retrieve response or completion state

---

## 4. What OpenClaw Should Own vs What JT7 Should Own

## OpenClaw should own
- provider messaging transport
- session/thread visibility
- session targeting
- execution/session lifecycle
- session metadata exposure

## JT7 should own
- channel surface mapping
- domain routing
- scope enforcement
- handoff semantics
- shared context bundle logic
- audit semantics
- tenant-aware behavior

## Tenant config should own
- which surfaces exist
- default domains
- default agents
- allowed agents per surface
- approval and escalation rules

---

## 5. Suggested Configuration Model

## Surface registry input
JT7 needs a config source that maps runtime surfaces to logical channel surfaces.

Example logical mapping:

```yaml
channel_surfaces:
  - channel_id: telegram:jt7_platform_bot
    provider: telegram
    label_hint: JT7 Platform Bot
    default_domain: platform
    default_agent: platform_agent

  - channel_id: telegram:jt7_job_ops_bot
    provider: telegram
    label_hint: JT7 Job Ops Bot
    default_domain: job_ops
    default_agent: job_ops_agent

  - channel_id: telegram:jrt7_life_bot
    provider: telegram
    label_hint: JRT7 Life Bot
    default_domain: life
    default_agent: life_agent

  - channel_id: telegram:jt7_ta_knowledge_bot
    provider: telegram
    label_hint: JT7 TA Knowledge Bot
    default_domain: knowledge
    default_agent: knowledge_agent
```

### Handoff target resolution
JT7 should resolve targets in this order:
1. explicit session key
2. explicit label
3. channel_surface mapping
4. fail closed

---

## 6. JT7 Routing Decision Flow

```text
Inbound Message
   ↓
OpenClaw Metadata
   ↓
channel_router
   ↓
channel_surface lookup
   ↓
conversation_context lookup/create
   ↓
context_scope_manager
   ↓
[ in scope ] -> default agent handles
[ out of scope ] -> explicit handoff / shared context / orchestrated split
```

---

## 7. Handoff Config Rules

## Rule 1
Cross-surface work should use session-to-session messaging, not ad hoc user forwarding.

## Rule 2
The target session must be known via:
- label
- session key
- or registry mapping

## Rule 3
A handoff message should contain:
- tenant_id
- source conversation id
- source domain
- target domain
- handoff reason
- context mode
- compact structured payload

## Rule 4
The target surface should treat a handoff as structured input, not as normal conversational drift.

---

## 8. Shared Context Config Rules

## Default
No automatic full shared state across sessions.

## Allowed modes
- `isolated`
- `summary_only`
- `shared_explicit`

## Required JT7 behavior
- `summary_only` is default for context sharing
- `shared_explicit` only on explicit request
- bundles should be compact and structured
- shared context and thread-local state must remain separate

---

## 9. Scope Locking Rules

## Platform surface
Lock to:
- architecture
- modules
- schemas
- orchestration
- infrastructure
- system debugging

## Job Ops surface
Lock to:
- live job operations
- recruiter/application tracking
- follow-ups
- interviews
- drafts

## Life surface
Lock to:
- routines
- habits
- wellness / sobriety / faith support
- personal admin

## TA Knowledge surface
Lock to:
- transcripts
- synthesis
- learning capture
- reference material
- knowledge retrieval

## Enforcement location
- JT7 layer, not raw OpenClaw transport layer

---

## 10. Minimal OpenClaw Implementation Path

## Phase 1
Use existing sessions as surface containers.

Requirements:
- stable labels
- ability to target by label or session key
- ability to inspect visible sessions

## Phase 2
Introduce surface registry in JT7 config/docs.

Requirements:
- logical mapping from OpenClaw session to JT7 surface domain

## Phase 3
Use `sessions_send` for explicit handoff / shared context transfer.

Requirements:
- structured handoff messages
- target resolution by label/sessionKey

## Phase 4
Add orchestrator-mediated cross-surface workflows.

Requirements:
- routing envelope
- run linkage
- audit logging

---

## 11. Bottom Line
OpenClaw owns transport and session visibility.
JT7 owns platform behavior.
The platform remains unified even when surfaces multiply.
