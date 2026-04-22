# JT7 Four-Bot Activation Checklist

## Purpose
This checklist prepares the JT7 four-bot model for live activation in OpenClaw.

It focuses on:
- Telegram prerequisites
- OpenClaw connection setup
- bot identity mapping
- runtime validation
- handoff/shared-context smoke tests

---

## 1. Activation Goal

Bring these four bot surfaces live:
- JRT7 Life Bot
- JT7 Platform Bot
- JT7 Job Ops Bot
- JT7 Planning Bot

using:
- one shared JT7 core
- one tenant (`JT_PERSONAL`)
- explicit handoff behavior
- explicit shared context behavior

---

## 2. Telegram Prerequisites

### Create bots
- [ ] Create `JRT7 Life Bot`
- [ ] Create `JT7 Platform Bot`
- [ ] Create `JT7 Job Ops Bot`
- [ ] Create `JT7 Planning Bot`

### Capture bot metadata
For each bot, record:
- [ ] bot username
- [ ] bot token
- [ ] visible display name
- [ ] intended domain

### Naming recommendation
- JRT7 Life
- JT7 Platform
- JT7 Job Ops
- JT7 Planning

### Bot descriptions should reflect domain
- Platform -> architecture / system / orchestration
- Job Ops -> recruiter/application/job operations
- Planning -> priorities / reviews / sequencing

---

## 3. OpenClaw Connection Setup

### Runtime prerequisites
- [ ] OpenClaw gateway is healthy
- [ ] Telegram channel support is active
- [ ] each bot token is connected/configured
- [ ] inbound messages from each bot can reach OpenClaw

### Identity resolution requirements
For each bot surface, confirm OpenClaw can distinguish:
- [ ] provider
- [ ] bot/account identity
- [ ] chat/session identity
- [ ] stable targetable session or label

---

## 4. Config Readiness

### Tenant config files present
- [ ] `tenants/JT_PERSONAL/bot_surfaces.md`
- [ ] `tenants/JT_PERSONAL/surface_policies.md`
- [ ] `tenants/JT_PERSONAL/archetypes.md`
- [ ] `tenants/JT_PERSONAL/bot_capabilities.md`
- [ ] `tenants/JT_PERSONAL/data_repos.md`
- [ ] `tenants/JT_PERSONAL/use_case_registry.md`
- [ ] `tenants/JT_PERSONAL/bot_runtime_profile.md`

### Docs present
- [ ] `docs/three-bot-surface-model.md`
- [ ] `docs/three-bot-openclaw-implementation-plan.md`
- [ ] `docs/openclaw-thread-routing-config-spec.md`
- [ ] `docs/multi-agent-thread-implementation-spec.md`
- [ ] `docs/multi-agent-thread-rollout-plan.md`

---

## 5. Bot Identity Mapping

### Life bot
- [ ] map to `jrt7_life_bot`
- [ ] default domain = `life`
- [ ] default agent = `life_agent`

### Platform bot
- [ ] map to `jt7_platform_bot`
- [ ] default domain = `platform`
- [ ] default agent = `platform_agent`

### Job Ops bot
- [ ] map to `jt7_job_ops_bot`
- [ ] default domain = `job_ops`
- [ ] default agent = `job_ops_agent`

### Planning bot
- [ ] map to `jt7_planning_bot`
- [ ] default domain = `planning`
- [ ] default agent = `planning_agent`

### Shared core rules
- [ ] tenant_id resolves to `JT_PERSONAL`
- [ ] same user identity resolves across all bots
- [ ] cross-bot actions remain tenant-scoped

---

## 6. Scope Enforcement Validation

### Platform bot tests
- [ ] architecture request stays in-bot
- [ ] live job ops request triggers handoff recommendation
- [ ] planning request triggers handoff recommendation or summary sharing

### Job Ops bot tests
- [ ] operational job task stays in-bot
- [ ] platform architecture request triggers handoff recommendation
- [ ] planning-style prioritization request triggers planning handoff recommendation

### Planning bot tests
- [ ] daily/weekly planning request stays in-bot
- [ ] direct architecture mutation request routes to Platform
- [ ] direct live job-state mutation request routes to Job Ops

### Life bot tests
- [ ] life/routine request stays in-bot
- [ ] platform architecture request routes to Platform
- [ ] live job-state request routes to Job Ops
- [ ] broad prioritization request routes to Planning when needed

---

## 7. Handoff Command Smoke Tests

### `handoff`
- [ ] Life -> Planning handoff works
- [ ] Life -> Platform handoff works
- [ ] Platform -> Job Ops handoff works
- [ ] Job Ops -> Platform handoff works
- [ ] Planning -> Platform handoff works
- [ ] Planning -> Job Ops handoff works

### Expected behavior
- [ ] handoff record created
- [ ] target bot receives scoped task
- [ ] source bot no longer owns transferred execution

---

## 8. Shared Context Smoke Tests

### `share context`
- [ ] Life -> Planning summary sharing works
- [ ] Planning -> Life summary sharing works
- [ ] Platform -> Job Ops summary sharing works
- [ ] Platform -> Planning summary sharing works
- [ ] Job Ops -> Planning summary sharing works
- [ ] Planning -> Platform summary sharing works

### Expected behavior
- [ ] shared context bundle created
- [ ] source bot retains ownership
- [ ] target bot receives scoped context only
- [ ] no raw history dump occurs

---

## 9. Continue-in-Other-Bot Smoke Tests

### `continue in other bot`
- [ ] Life -> Planning continuity transfer works
- [ ] Platform -> Planning continuity transfer works
- [ ] Platform -> Job Ops continuity transfer works
- [ ] Job Ops -> Planning continuity transfer works

### Expected behavior
- [ ] handoff record created
- [ ] shared context bundle created
- [ ] target bot becomes active owner
- [ ] source bot records handed_off state

---

## 10. Full-Context Request Validation

### `shared_explicit`
- [ ] explicit “with full context” request upgrades context mode correctly
- [ ] bundle remains scoped and relevant
- [ ] no unrelated context is included

---

## 11. Audit and Safety Validation

- [ ] handoff actions are logged
- [ ] shared context bundles are logged
- [ ] ownership state is explicit after every transfer
- [ ] no cross-tenant movement is possible
- [ ] no silent cross-bot drift occurs

---

## 12. Minimum Live Activation Criteria

Mark the 4-bot system live only when all are true:

- [ ] all 4 bots are reachable in Telegram
- [ ] all 4 bots are distinguishable by OpenClaw
- [ ] each bot maps to the correct bot surface
- [ ] each bot respects domain scope
- [ ] handoff works
- [ ] share context works
- [ ] continue in other bot works
- [ ] audit records exist for cross-bot actions

---

## 13. Recommended Activation Order

### Step 1
Bring `JRT7 Life Bot` live

### Step 2
Bring `JT7 Platform Bot` live

### Step 3
Bring `JT7 Job Ops Bot` live

### Step 4
Validate Life <-> Planning and Platform <-> Job Ops handoff and shared context

### Step 5
Bring `JT7 Planning Bot` live

### Step 6
Validate Planning <-> Platform, Planning <-> Job Ops, and Life <-> Planning interactions

---

## 14. Go/No-Go Decision

## Go
Proceed if:
- bot identity mapping is stable
- domain scope is enforced
- handoff/shared-context behavior is predictable

## No-Go
Pause if:
- bots cannot be distinguished reliably
- scope drift still occurs
- handoff target resolution is ambiguous
- shared context is bleeding too broadly

---

## 15. Bottom Line

The system is ready for activation when:
- the four bot surfaces are reachable
- the four bot surfaces are correctly mapped
- domain boundaries hold
- cross-bot movement is explicit
- context sharing is controlled
- auditability is intact
