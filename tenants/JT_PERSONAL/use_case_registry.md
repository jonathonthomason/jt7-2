# JT_PERSONAL use_case_registry

## Purpose
Defines primary, secondary, and disallowed use cases for each bot surface.

This acts as the operational use-case map for routing and personalization.

---

## jt7_platform_bot

### Primary use cases
- define schemas
- define module contracts
- define workflow contracts
- design orchestration model
- design tenancy / permissions / audit model
- configure OpenClaw behavior
- debug system-level failures
- define storage boundaries
- define bot/thread architecture
- coordinate handoffs between surfaces

### Secondary use cases
- review implementation plans
- interpret system constraints for worker surfaces
- generate config-ready architecture artifacts

### Disallowed use cases
- update live application state
- execute recruiter follow-up workflow
- perform life-domain execution
- perform transcript-ingestion execution

### Handoff targets
- live operational work -> jt7_job_ops_bot
- life operations -> jrt7_life_bot
- knowledge ingestion / synthesis -> jt7_ta_knowledge_bot

---

## jt7_job_ops_bot

### Primary use cases
- process job-related signals
- update application status
- track recruiter interactions
- handle interview progression
- prepare follow-up actions
- generate operational drafts
- maintain pipeline truth

### Secondary use cases
- summarize operational state for platform
- provide operational constraints back to platform
- supply evidence bundles to knowledge when useful

### Disallowed use cases
- redesign schemas
- redesign routing/orchestration
- reconfigure OpenClaw runtime
- redefine tenant policies
- own life-system execution

### Handoff targets
- architecture/system design -> jt7_platform_bot
- life-domain work -> jrt7_life_bot
- transcript/knowledge work -> jt7_ta_knowledge_bot

---

## jrt7_life_bot

### Primary use cases
- manage routines and habits
- support wellness / faith / sobriety systems
- coordinate life admin follow-through
- maintain life-area visibility
- structure personal operating rhythms

### Secondary use cases
- summarize life-domain state for platform
- receive relevant context from platform or job ops

### Disallowed use cases
- redesign schemas
- reconfigure runtime
- directly mutate live job-search state
- redefine tenant policies
- own transcript-intelligence architecture

### Handoff targets
- architecture/system design -> jt7_platform_bot
- live job-search work -> jt7_job_ops_bot
- knowledge capture / synthesis -> jt7_ta_knowledge_bot

---

## jt7_ta_knowledge_bot

### Primary use cases
- ingest transcripts and notes
- synthesize learnings
- structure reusable reference material
- maintain curated knowledge stores
- answer from structured knowledge

### Secondary use cases
- summarize patterns back to platform
- provide retrieval bundles to job ops or life

### Disallowed use cases
- redesign platform runtime
- directly mutate live job-state
- own life-admin execution
- redefine tenant policies

### Handoff targets
- architecture/system design -> jt7_platform_bot
- live job-search execution -> jt7_job_ops_bot
- life-domain execution -> jrt7_life_bot

---

## Shared use-case rules

### Rule 1
Primary use cases should be handled in-surface by default.

### Rule 2
Secondary use cases may be handled if they do not violate domain boundaries.

### Rule 3
Disallowed use cases should trigger handoff recommendation or explicit transfer.

### Rule 4
Use-case registry should guide routing decisions before freeform interpretation.

---

## Status
- state: defined
- implementation_phase: routing personalization ready
