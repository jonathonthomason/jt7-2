# JT_PERSONAL data_repos

## Purpose
Defines primary and secondary data repositories used by each bot surface.

This keeps repo ownership explicit and reduces cross-surface confusion.

---

## Shared core repos

### Core platform repos
- `/docs`
- `/schemas`
- `/modules`
- `/workflows`
- `/tenants`
- `/audit`

### Shared system stores
- handoff records
- shared context bundles
- routing decisions
- workflow runs
- audit logs

---

## jt7_platform_bot

### Primary repos
- `/docs`
- `/schemas`
- `/modules`
- `/workflows`
- `/tenants`
- `/audit`

### Secondary repos
- GitHub architecture/docs repo
- Notion architecture workspace
- system configuration references

### Repo role
- source of truth for platform design, routing rules, contracts, and system policies

---

## jt7_job_ops_bot

### Primary repos
- Google Sheets tracker
- Gmail evidence store
- Calendar events
- Google Docs application/support docs

### Secondary repos
- local markdown audit outputs
- Notion operational dashboard if retained
- recruiter/application export artifacts

### Repo role
- source of truth for live operational job state and supporting evidence

---

## jrt7_life_bot

### Primary repos
- Notion life workspace
- goals/projects/tasks/habits databases
- wellness / faith / sobriety records
- calendar and task views

### Secondary repos
- markdown life planning artifacts
- shared context bundles from other surfaces
- personal admin reference docs

### Repo role
- source of truth for life operations, routines, personal systems, and follow-through support

---

## jt7_ta_knowledge_bot

### Primary repos
- transcript exports and thread archives
- Notion knowledge workspace
- structured reference docs
- curated synthesis artifacts

### Secondary repos
- shared context bundles from platform, job ops, or life
- markdown research notes
- source document mirrors

### Repo role
- source of truth for transcript intelligence, reusable synthesis, and structured knowledge retrieval

---

## Shared repo rules

### Rule 1
Each bot has primary repos it should prefer by default.

### Rule 2
Cross-repo reads may occur through shared context or orchestrator flows.

### Rule 3
Cross-repo writes should respect bot domain ownership and approval policy.

### Rule 4
Platform docs should not silently become live operational truth unless explicitly designated.

---

## Status
- state: defined
- implementation_phase: repo ownership ready
