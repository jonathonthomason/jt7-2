# JT_PERSONAL channel_surfaces

## Purpose
Canonical live bot-to-surface mapping for the JT7 system.

This file defines the live surface registry for one shared JT7 platform.
It is the canonical mapping layer between bot identities and tenant-scoped conversation surfaces.

---

## Platform Rules
- one shared engine
- one shared gateway
- one shared brain
- no separate bot engines
- all bots are surfaces under one platform
- `jt7_platform_bot` is the control plane
- all other bots are domain worker surfaces
- shared global context is available across all surfaces through explicit platform rules
- thread-local state remains surface-local unless handed off or shared explicitly

---

## Primary Inbound Platform Entry
- primary_surface_id: jt7_platform_bot
- primary_bot_name: JT7 Platform Bot
- primary_bot_username: jt7_platform_bot
- role: control_plane
- notes: primary inbound platform entry for routing, structure, orchestration, and correction

---

## Surface Registry

### Surface 1
- bot_surface_id: jt7_platform_bot
- bot_name: JT7 Platform Bot
- bot_username: jt7_platform_bot
- domain: platform
- default_agent: platform_agent
- surface_role: control_plane
- allowed_handoff_targets:
  - jt7_job_ops_bot
  - jrt7_life_bot
  - jt7_ta_knowledge_bot
  - jt7_tasks_bot
- shares_global_context: yes
- runtime_status: defined
- notes: control plane and primary platform entry

### Surface 2
- bot_surface_id: jt7_job_ops_bot
- bot_name: JT7 Job Ops Bot
- bot_username: jt7_job_ops_bot
- domain: job_ops
- default_agent: job_ops_agent
- surface_role: domain_worker
- allowed_handoff_targets:
  - jt7_platform_bot
  - jrt7_life_bot
  - jt7_ta_knowledge_bot
  - jt7_tasks_bot
- shares_global_context: yes
- runtime_status: defined
- notes: domain worker for job-search and recruiter operations

### Surface 3
- bot_surface_id: jrt7_life_bot
- bot_name: JRT7 Life Bot
- bot_username: jrt7_life_bot
- domain: life
- default_agent: life_agent
- surface_role: domain_worker
- allowed_handoff_targets:
  - jt7_platform_bot
  - jt7_job_ops_bot
  - jt7_ta_knowledge_bot
  - jt7_tasks_bot
- shares_global_context: yes
- runtime_status: defined
- notes: domain worker for routines, life systems, and personal admin

### Surface 4
- bot_surface_id: jt7_ta_knowledge_bot
- bot_name: JT7 TA Knowledge Bot
- bot_username: jt7_ta_knowledge_bot
- domain: knowledge
- default_agent: knowledge_agent
- surface_role: domain_worker
- allowed_handoff_targets:
  - jt7_platform_bot
  - jt7_job_ops_bot
  - jrt7_life_bot
  - jt7_tasks_bot
- shares_global_context: yes
- runtime_status: defined
- notes: domain worker for transcript intelligence, synthesis, and structured knowledge

### Surface 5
- bot_surface_id: jt7_tasks_bot
- bot_name: JT7 Tasks
- bot_username: jt7_tasks_bot
- domain: tasks
- default_agent: tasks_agent
- surface_role: domain_worker
- allowed_handoff_targets:
  - jt7_platform_bot
  - jt7_job_ops_bot
  - jrt7_life_bot
  - jt7_ta_knowledge_bot
- shares_global_context: yes
- runtime_status: defined
- notes: domain worker for task capture, follow-through, and queue control

---

## Explicit Handoff Expectations
- wrong-surface requests must not silently blend
- out-of-scope work must route through explicit handoff or explicit shared-context transfer
- handoffs must preserve tenant identity, source surface, target surface, and reason
- shared global context may be used across surfaces, but thread-local context must only move explicitly

---

## Runtime Mapping Status
- current_state: defined_not_live
- live_mapping_verified: no
- runtime_config_bound: no
- notes: file is canonical for live bot-to-surface mapping, but runtime binding is not yet verified
