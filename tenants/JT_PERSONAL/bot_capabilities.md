# JT_PERSONAL bot_capabilities

## Purpose
Defines bot-specific capability profiles for APIs, webhooks, skills, tools, and approval posture.

This file controls what each bot surface is expected to use.

---

## jt7_platform_bot

### Allowed APIs / integrations
- OpenClaw runtime/session layer
- GitHub
- Notion
- local workspace/docs repos

### Allowed webhooks / signals
- system health or runtime status signals
- config / deployment signals
- workflow orchestration events
- cross-surface routing events

### Preferred skills / tools
- github
- skill-creator
- clawhub
- coding-agent
- notion
- healthcheck

### Approval posture
- approval required for configuration mutations with external/runtime effect
- approval required for policy changes affecting multiple surfaces

### Disallowed default capability focus
- live recruiter/application operations
- life admin execution
- transcript-processing execution at scale
- task queue execution by default

---

## jt7_job_ops_bot

### Allowed APIs / integrations
- Gmail
- Calendar
- Google Sheets
- Google Docs
- job ingestion/search sources
- Telegram control surface

### Allowed webhooks / signals
- Gmail message events
- Calendar event updates
- tracker write/verify events
- job ingestion results

### Preferred skills / tools
- gog
- notion
- job-search wrapper / related search layer

### Approval posture
- approval required for high-risk external sending
- approval required for low-confidence destructive or ambiguous operational mutations

### Disallowed default capability focus
- platform schema redesign
- tenant/policy redesign
- OpenClaw configuration changes
- generalized task-system ownership

---

## jrt7_life_bot

### Allowed APIs / integrations
- Notion life system
- Google Calendar
- Google Tasks
- Gmail read for life/admin-relevant signals
- Telegram control surface

### Allowed webhooks / signals
- routine reminder signals
- calendar/life-event updates
- life-admin inbox signals
- periodic life review triggers

### Preferred skills / tools
- notion
- gog

### Approval posture
- approval required for high-impact external sends or sensitive life-domain mutations
- approval required for ambiguous actions affecting another locked domain

### Disallowed default capability focus
- platform schema redesign
- live job pipeline execution
- tenant/policy redesign
- generalized task-system ownership

---

## jt7_ta_knowledge_bot

### Allowed APIs / integrations
- transcript exports
- local docs and markdown repos
- Notion knowledge workspace
- Google Drive read
- Telegram control surface

### Allowed webhooks / signals
- transcript import events
- document updates
- summary requests
- knowledge refresh triggers

### Preferred skills / tools
- notion
- github

### Approval posture
- approval required for bulk overwrite of trusted knowledge stores
- approval required for ambiguous source consolidation with destructive consequences

### Disallowed default capability focus
- runtime reconfiguration
- direct job pipeline mutation
- life-domain execution
- generalized task-system ownership

---

## jt7_tasks_bot

### Allowed APIs / integrations
- Notion task system
- Google Tasks
- Calendar read
- Gmail read for actionable follow-ups
- Telegram control surface

### Allowed webhooks / signals
- task capture events
- due-date reminders
- follow-through updates
- cross-surface action requests

### Preferred skills / tools
- notion
- gog

### Approval posture
- approval required for destructive bulk task changes
- approval required for high-impact external actions initiated from task flows

### Disallowed default capability focus
- platform redesign
- direct job pipeline ownership
- transcript-intelligence ownership
- life-domain ownership

---

## Shared rules

### Rule 1
All bots inherit shared-core capabilities only through orchestrator-safe routing.

### Rule 2
A capability being technically available does not mean it is in-scope for every bot.

### Rule 3
Capability access should align with domain ownership, not convenience.

---

## Status
- state: defined
- implementation_phase: capability policy ready
