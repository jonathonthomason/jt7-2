# JT_PERSONAL surface_policies

## Purpose
Canonical policy definitions for each active bot surface in the JT_PERSONAL tenant.

This file defines:
- in-scope intents
- out-of-scope intents
- handoff triggers
- approval triggers
- shared-context rules
- enforcement posture

---

## Global Unified-Core Policy
- one shared platform core serves all surfaces
- surfaces are entry points, not separate systems
- each surface must stay in its domain unless explicitly redirected
- out-of-scope work must trigger explicit handoff behavior
- shared context and thread-local context must stay distinct

---

## Policy: jt7_platform_bot

### Surface
- bot_surface_id: jt7_platform_bot
- default_domain: platform
- lock_state: locked
- enforcement_mode: strict

### In-scope intents
- define_schema
- define_module_contract
- define_workflow
- define_routing_model
- define_tenancy_model
- define_permissions_model
- define_audit_model
- configure_openclaw
- diagnose_system_issue
- debug_platform_behavior
- define_storage_architecture
- define_agent_architecture
- define_surface_model
- coordinate_cross_surface_handoff

### Out-of-scope intents
- update_application_state
- log_recruiter_interaction
- draft_candidate_follow_up
- process_live_pipeline_work
- manage_routines
- coordinate_personal_admin
- ingest_transcript_knowledge
- summarize_ta_learnings

### Handoff triggers
- request is live job-search operational work
- request is life-operations work
- request is knowledge ingestion or transcript synthesis work

### Approval triggers
- platform config mutation with external effect
- cross-surface rule changes
- permission or policy changes affecting multiple surfaces
- tenant-level configuration changes

### Shared-context rules
- may send summary bundles to any worker surface
- must default to `summary_only`
- may use `shared_explicit` only on explicit user request

### Enforcement behavior
- reject silent domain drift
- route to the correct worker surface when work is not platform-owned

---

## Policy: jt7_job_ops_bot

### Surface
- bot_surface_id: jt7_job_ops_bot
- default_domain: job_ops
- lock_state: locked
- enforcement_mode: strict

### In-scope intents
- update_application_state
- track_recruiter_interaction
- log_interview_state
- create_follow_up_action
- review_pipeline_item
- update_job_tracking_record
- handle_job_signal
- prepare_candidate_draft
- manage_live_job_ops

### Out-of-scope intents
- redefine_platform_architecture
- configure_openclaw_runtime
- redesign_tenant_policy
- manage_routines
- support_wellness_tracking
- ingest_transcript_knowledge
- build_knowledge_base

### Handoff triggers
- request becomes architectural or configuration-heavy
- request belongs to life domain
- request belongs to knowledge domain

### Approval triggers
- externally risky write actions
- low-confidence workflow state mutation
- ambiguous contact/application match with meaningful consequences

### Shared-context rules
- may receive architecture constraints from platform
- may send operational summaries to platform, life, or knowledge when relevant
- should default to `summary_only`

### Enforcement behavior
- do not perform architecture, life, or knowledge work in-thread
- route instead of drifting

---

## Policy: jrt7_life_bot

### Surface
- bot_surface_id: jrt7_life_bot
- default_domain: life
- lock_state: scoped
- enforcement_mode: guided

### In-scope intents
- manage_routines
- manage_habits
- support_wellness_tracking
- support_faith_and_sobriety_structure
- coordinate_personal_admin
- shape_life_area_follow_through
- review_life_os_state

### Out-of-scope intents
- redefine_platform_architecture
- update_live_application_state
- reconfigure_openclaw_runtime
- redesign_tenant_policy
- ingest_transcript_knowledge
- build_ta_reference_system

### Handoff triggers
- request becomes architectural or runtime-config heavy
- request becomes live job-search operational work
- request becomes transcript, learning, or TA knowledge work

### Approval triggers
- life-domain action would trigger high-impact external mutation
- request attempts to override another locked surface domain

### Shared-context rules
- may receive summaries from platform, job ops, or knowledge
- may share scoped life context with other surfaces
- default transfer mode is `summary_only`
- explicit full-context requests may use `shared_explicit`

### Enforcement behavior
- act as a dedicated life operations surface
- do not silently absorb platform, job ops, or knowledge ownership

---

## Policy: jt7_ta_knowledge_bot

### Surface
- bot_surface_id: jt7_ta_knowledge_bot
- default_domain: knowledge
- lock_state: scoped
- enforcement_mode: guided

### In-scope intents
- ingest_transcript_knowledge
- summarize_ta_learnings
- structure_reference_material
- capture_reusable_patterns
- curate_domain_memory
- answer_from_curated_knowledge
- review_knowledge_base_state

### Out-of-scope intents
- redefine_platform_architecture
- update_live_application_state
- reconfigure_openclaw_runtime
- redesign_tenant_policy
- manage_routines
- own_job_pipeline_execution

### Handoff triggers
- request becomes platform architecture or routing design
- request becomes live job-search operational work
- request becomes life operations execution

### Approval triggers
- knowledge action would overwrite trusted source material at scale
- request attempts to operate outside explicit knowledge scope

### Shared-context rules
- may receive summaries and evidence from platform, job ops, or life
- may share structured knowledge bundles back to other surfaces
- default transfer mode is `summary_only`
- explicit full-context requests may use `shared_explicit`

### Enforcement behavior
- act as a dedicated knowledge surface
- do not silently become a general strategist or platform owner

---

## Global Cross-Surface Policy

### Allowed commands
- handoff
- share context
- continue in other bot

### Default transfer modes
- handoff -> isolated
- share context -> summary_only
- continue in other bot -> summary_only
- explicit full/shared request -> shared_explicit

### Global prohibitions
- no silent cross-bot context bleed
- no cross-tenant transfer
- no duplicate ownership after handoff
- no specialist bot claiming another surface’s domain by default

### Global requirements
- every cross-surface move must produce a handoff record or shared context bundle
- every transfer must preserve tenant_id
- every transfer must preserve explicit ownership state
- thread-local state must not be treated as shared context unless packaged explicitly

---

## Escalation Defaults
- platform -> workflow_orchestrator
- job_ops -> workflow_orchestrator
- life -> workflow_orchestrator
- knowledge -> workflow_orchestrator

---

## Status
- state: defined
- implementation_phase: policy foundation ready
