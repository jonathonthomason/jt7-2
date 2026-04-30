# JT7 Four-Surface Model

## Purpose
This document defines the production multi-surface model for JT7.

It assumes:
- one shared JT7/OpenClaw core
- one tenant: `JT_PERSONAL`
- four separate conversation surfaces
- strict surface contracts
- explicit handoff and shared context
- no forked logic

---

## 1. Core Model
- one engine
- one gateway
- one shared brain
- many conversation surfaces
- platform is the control plane
- domain surfaces are workers

Surfaces are different entry points into one platform.
They are not separate systems.

A single bot surface may still use internal delegation or subagents, but each user-facing bot should keep one primary role and domain contract.

---

## 2. Surface Set

## Surface 1 — JT7 Platform Bot
- bot_id: `jt7_platform_bot`
- default_domain: `platform`
- default_agent: `platform_agent`
- role: control plane

### Scope
- system architecture
- schemas
- module contracts
- workflow design
- routing logic
- infra/config
- system debugging
- orchestration and handoff rules

### Out of Scope
- live job application tracking
- recruiter follow-ups
- life-admin execution
- transcript-ingestion execution

---

## Surface 2 — JT7 Job Ops Bot
- bot_id: `jt7_job_ops_bot`
- default_domain: `job_ops`
- default_agent: `job_ops_agent`
- role: worker

### Scope
- application tracking
- recruiter interactions
- interviews
- follow-ups
- drafts
- pipeline operations

### Out of Scope
- platform architecture
- infra/config decisions
- life operations
- knowledge architecture

---

## Surface 3 — JRT7 Life Bot
- bot_id: `jrt7_life_bot`
- default_domain: `life`
- default_agent: `life_agent`
- role: worker

### Scope
- routines and habits
- wellness / faith / sobriety support
- personal admin coordination
- life operating system support

### Out of Scope
- platform architecture
- live job pipeline mutation
- knowledge architecture
- tenant/runtime redesign

---

## Surface 4 — JT7 TA Knowledge Bot
- bot_id: `jt7_ta_knowledge_bot`
- default_domain: `knowledge`
- default_agent: `knowledge_agent`
- role: worker

### Scope
- transcripts
- synthesis
- learning capture
- reference material
- reusable knowledge retrieval

### Out of Scope
- direct platform redesign
- direct live job-state mutation
- life-admin execution
- runtime reconfiguration

---

## 3. Shared Context vs Thread-Local Context

### Shared context
Global across all surfaces:
- user goals
- system rules
- major decisions
- identity
- priorities

### Thread-local context
Owned by each surface:
- active tasks
- recent actions
- domain-specific state
- local conversation progress

### Rule
Never mix these blindly.
Thread-local context must only move through explicit handoff or shared-context packaging.

---

## 4. Routing Rule

For every inbound request:
1. resolve current surface
2. resolve current domain
3. test whether request belongs in that domain
4. if yes, execute normally in-surface
5. if no, create explicit handoff or shared-context recommendation

### Prohibitions
- no silent domain switching
- no implicit worker substitution
- no general-assistant fallback

---

## 5. Handoff Rule

When work needs to move:
- state that a handoff is happening
- explain why
- package context cleanly
- direct it to the correct surface/domain
- preserve traceability
- avoid duplicate ownership

### Supported modes
- `handoff` -> isolated transfer
- `share context` -> summary-only context share
- `continue in other bot` -> transfer with continuity
- `shared_explicit` -> only on explicit request

---

## 6. Ownership Model

### Platform owns
- routing
- orchestration
- system rules
- contracts
- control-plane decisions

### Job Ops owns
- live job-search execution
- recruiter/application state
- follow-up operations

### Life owns
- life operations
- habits/routines
- personal admin

### TA Knowledge owns
- transcript intelligence
- synthesis
- knowledge structuring
- retrieval support

---

## 7. Bottom Line

This 4-surface model gives JT7:
- one coordinated platform
- focused domain threads
- explicit handoffs
- reusable logic
- shared memory without uncontrolled bleed
- a clean path to additional worker surfaces later
