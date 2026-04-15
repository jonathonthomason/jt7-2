# JT_PERSONAL bot_surfaces

## Purpose
Canonical surface registry for the JT_PERSONAL tenant.

This file is the config-style source of truth for:
- surface to domain mapping
- default agent mapping
- allowed agent routing
- handoff defaults
- escalation behavior
- unified-core rules

---

## Unified Platform Rules
- one engine
- one gateway
- one shared brain
- many conversation surfaces
- no forked systems
- no duplicated logic
- no ambient cross-surface context bleed

---

## Surface Registry

### jt7_platform_bot
- bot_surface_id: jt7_platform_bot
- tenant_id: JT_PERSONAL
- provider: telegram
- bot_id: jt7_platform_bot
- bot_name: JT7 Platform Bot
- default_domain: platform
- default_agent_id: platform_agent
- allowed_agent_ids:
  - platform_agent
  - workflow_orchestrator
  - approval_router
  - audit_verifier
- escalation_agent_id: workflow_orchestrator
- handoff_mode: summary_only
- lock_state: locked
- status: active
- purpose: control plane, routing, system rules, structure, orchestration, debugging
- notes: platform owns coordination and correction, not general execution

### jt7_job_ops_bot
- bot_surface_id: jt7_job_ops_bot
- tenant_id: JT_PERSONAL
- provider: telegram
- bot_id: jt7_job_ops_bot
- bot_name: JT7 Job Ops Bot
- default_domain: job_ops
- default_agent_id: job_ops_agent
- allowed_agent_ids:
  - job_ops_agent
  - workflow_orchestrator
  - approval_router
  - audit_verifier
- escalation_agent_id: workflow_orchestrator
- handoff_mode: summary_only
- lock_state: locked
- status: active
- purpose: applications, recruiters, interviews, follow-ups, pipeline operations
- notes: job operations worker surface

### jrt7_life_bot
- bot_surface_id: jrt7_life_bot
- tenant_id: JT_PERSONAL
- provider: telegram
- bot_id: jrt7_life_bot
- bot_name: JRT7 Life Bot
- default_domain: life
- default_agent_id: life_agent
- allowed_agent_ids:
  - life_agent
  - workflow_orchestrator
  - approval_router
  - audit_verifier
- escalation_agent_id: workflow_orchestrator
- handoff_mode: summary_only
- lock_state: scoped
- status: active
- purpose: routines, habits, wellness, faith, sobriety, personal admin, life operations
- notes: dedicated life worker surface

### jt7_ta_knowledge_bot
- bot_surface_id: jt7_ta_knowledge_bot
- tenant_id: JT_PERSONAL
- provider: telegram
- bot_id: jt7_ta_knowledge_bot
- bot_name: JT7 TA Knowledge Bot
- default_domain: knowledge
- default_agent_id: knowledge_agent
- allowed_agent_ids:
  - knowledge_agent
  - workflow_orchestrator
  - approval_router
  - audit_verifier
- escalation_agent_id: workflow_orchestrator
- handoff_mode: summary_only
- lock_state: scoped
- status: active
- purpose: transcripts, synthesis, research memory, learned patterns, knowledge structuring
- notes: knowledge worker surface for TA and transcript-intelligence work

### jt7_tasks_bot
- bot_surface_id: jt7_tasks_bot
- tenant_id: JT_PERSONAL
- provider: telegram
- bot_id: jt7_tasks_bot
- bot_name: JT7 Tasks
- default_domain: tasks
- default_agent_id: tasks_agent
- allowed_agent_ids:
  - tasks_agent
  - workflow_orchestrator
  - approval_router
  - audit_verifier
- escalation_agent_id: workflow_orchestrator
- handoff_mode: summary_only
- lock_state: scoped
- status: active
- purpose: task capture, task management, follow-through tracking, execution queue control
- notes: task execution worker surface

---

## Cross-Surface Rules

### Default rule
- stay in current surface
- current surface uses its default agent unless orchestration or approval routing is required

### Allowed cross-surface actions
- handoff
- share context
- continue in other bot

### Default context transfer behavior
- handoff -> isolated
- share context -> summary_only
- continue in other bot -> summary_only
- explicit full/shared request -> shared_explicit

### Safety rules
- no silent cross-surface domain switching
- no silent context bleed
- no duplicate ownership after handoff
- no cross-tenant routing
- all cross-surface transitions must be logged
- ownership must remain explicit

---

## Surface Ownership Model

### Platform Bot owns
- routing rules
- system rules
- schemas
- workflows
- orchestration
- platform debugging
- surface contracts

### Job Ops Bot owns
- application lifecycle operations
- recruiter interactions
- interviews
- follow-ups
- pipeline-state operations

### Life Bot owns
- routines and habits support
- wellness / faith / sobriety support
- personal admin coordination
- life-area follow-through

### TA Knowledge Bot owns
- transcript ingestion and structuring
- synthesis and summarization
- reusable knowledge capture
- learning patterns and reference material
- domain knowledge retrieval support

### Tasks Bot owns
- task capture and normalization
- task status updates
- due-date and queue management
- cross-domain follow-through tracking
- actionable execution lists

---

## Activation Order
1. jt7_platform_bot
2. jt7_job_ops_bot
3. jrt7_life_bot
4. jt7_ta_knowledge_bot
5. jt7_tasks_bot

---

## Status
- state: defined
- implementation_phase: pre-runtime surface setup
