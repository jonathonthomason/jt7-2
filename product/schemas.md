# product/schemas.md

## File Role
- **Purpose:** define canonical data schemas for JT7 core entities
- **Roadmap step:** JT7-R2.3.1
- **Status:** active

> Consolidation note: this schema file reflects an earlier, richer JT7 modeling pass. JT7's current consolidated MVP operating model now uses a simpler shared schema for live tracker flow (`company`, `role`, `status`, `last_activity`, `next_step`, `contact`, `source`, `thread_id`, `notes`) and a stricter single status model. Until rewritten, treat this file as valuable reference material but partially legacy relative to the current MVP governance model.

## Schema Design Rules
- each schema must be UI-renderable
- each schema must be file-compatible
- each schema must support durable state and derived state
- each schema should separate raw fields from interpretation
- each schema should support IDs, status, timestamps, and notes where useful

---

## Schema: opportunity
### Purpose
Represent a job opportunity, target role, or active application.

### Fields
- **id:** unique string identifier
- **company_name:** string
- **role_title:** string
- **priority:** low | medium | high
- **status:** researching | targeting | applied | outreach | interviewing | follow_up_due | on_hold | closed
- **source:** linkedin | referral | recruiter | direct | indeed | builtin | other
- **last_action_at:** ISO date or datetime
- **last_action_summary:** string
- **next_action_at:** ISO date or datetime | null
- **next_action_summary:** string
- **blockers:** array[string]
- **fit_score:** number 0-10 | null
- **fit_notes:** string
- **location_mode:** remote | hybrid | onsite | unknown
- **comp_range:** string | null
- **owner:** Jonathon | JT7
- **notes:** array[string]

### Example
```yaml
id: opp_figma_principal_pd
company_name: Figma
role_title: Principal Product Designer
priority: high
status: targeting
source: linkedin
last_action_at: 2026-04-02
last_action_summary: Added role to pipeline and marked high priority
next_action_at: 2026-04-03
next_action_summary: Review job description and tailor positioning notes
blockers: []
fit_score: 9
fit_notes: Strong match on systems thinking and strategic scope
location_mode: remote
comp_range: null
owner: JT7
notes:
  - Design strategy and product influence appear central to the role
```

### File Mapping
- **Primary file:** `career/pipeline.md`
- **Supporting file:** `career/strategy.md`

### Future UI Mapping
- Pipeline table row
- Opportunity detail panel
- Follow-up queue item

---

## Schema: recruiter_contact
### Purpose
Represent a recruiter, hiring manager, referrer, or other career-relevant contact.

### Fields
- **id:** unique string identifier
- **name:** string
- **company_name:** string
- **role:** recruiter | hiring_manager | referrer | founder | peer | other
- **relationship_strength:** weak | medium | strong | unknown
- **contact_channel:** linkedin | email | phone | other
- **contact_value:** low | medium | high
- **last_contact_at:** ISO date or datetime | null
- **last_contact_summary:** string | null
- **next_action_at:** ISO date or datetime | null
- **next_action_summary:** string | null
- **associated_opportunity_ids:** array[string]
- **status:** active | waiting | dormant | closed
- **notes:** array[string]

### Example
```yaml
id: contact_figma_recruiter_01
name: Alex Doe
company_name: Figma
role: recruiter
relationship_strength: weak
contact_channel: linkedin
contact_value: high
last_contact_at: null
last_contact_summary: null
next_action_at: 2026-04-04
next_action_summary: Draft outreach message tied to principal design role
associated_opportunity_ids:
  - opp_figma_principal_pd
status: active
notes:
  - No prior conversation recorded
```

### File Mapping
- **Future primary file:** `career/contacts.md`
- **Current relationship anchor:** `career/pipeline.md`

### Future UI Mapping
- Contact list
- Relationship timeline
- Outreach action queue

---

## Schema: decision
### Purpose
Represent a meaningful system, career, or product decision.

### Fields
- **id:** unique string identifier
- **title:** string
- **domain:** career | product | execution | system
- **status:** proposed | active | reversed | superseded
- **decision_date:** ISO date
- **owner:** Jonathon | JT7 | shared
- **summary:** string
- **why:** string
- **implications:** array[string]
- **related_files:** array[string]
- **related_entity_ids:** array[string]
- **next_review_at:** ISO date | null

### Example
```yaml
id: decision_career_first_priority_order
title: Career remains the top system priority
domain: system
status: active
decision_date: 2026-04-02
owner: shared
summary: JT7 should prioritize career outcomes ahead of product and execution work
why: Career transition has the highest immediate leverage and urgency
implications:
  - Product work should support, not displace, the search
  - Execution systems should reduce drag on career movement
related_files:
  - MISSION.md
  - AGENTS.md
  - CURRENT.md
related_entity_ids: []
next_review_at: null
```

### File Mapping
- **Primary file:** `DECISIONS.md`
- **Supporting files:** `CURRENT.md`, workstream files as needed

### Future UI Mapping
- Decision log
- Timeline event
- Dependency and rationale view

---

## Schema: focus_item
### Purpose
Represent a current priority, active task, blocker, or next action.

### Fields
- **id:** unique string identifier
- **title:** string
- **type:** priority | task | blocker | next_action | anti_focus
- **domain:** career | product | execution | system
- **status:** active | blocked | done | deferred
- **priority_rank:** number | null
- **summary:** string
- **related_files:** array[string]
- **related_entity_ids:** array[string]
- **owner:** Jonathon | JT7 | shared
- **due_at:** ISO date or datetime | null
- **notes:** array[string]

### Example
```yaml
id: focus_add_first_pipeline_targets
title: Add first real pipeline targets
type: next_action
domain: career
status: active
priority_rank: 1
summary: Populate the pipeline with the first real set of companies and roles
related_files:
  - career/pipeline.md
  - ops/focus.md
related_entity_ids: []
owner: shared
due_at: null
notes:
  - Highest-leverage next move for career activation
```

### File Mapping
- **Primary file:** `ops/focus.md`
- **Supporting files:** `CURRENT.md`, workstream files

### Future UI Mapping
- Now view cards
- Action queue
- Blocker list

---

## Schema: current_state
### Purpose
Represent the compressed cross-system state of JT7 right now.

### Fields
- **id:** unique string identifier
- **updated_at:** ISO date or datetime
- **system_phase:** string
- **current_step:** roadmap label
- **top_priorities:** array[string]
- **active_risks:** array[string]
- **open_questions:** array[string]
- **required_next_moves:** array[string]
- **state_summary:** string
- **confidence_level:** low | medium | high
- **related_files:** array[string]

### Example
```yaml
id: current_state_2026_04_02
updated_at: 2026-04-02T08:10:00-05:00
system_phase: Canonical Data Layer
current_step: JT7-R2.3.1
top_priorities:
  - Activate the career engine
  - Stabilize the JT7 operating system
  - Reduce execution drag
active_risks:
  - No live opportunities are recorded yet
  - Asset inventory is still missing
open_questions:
  - What real companies should enter the pipeline first?
  - What portfolio and resume assets already exist?
required_next_moves:
  - Define canonical schemas
  - Align files to schemas
state_summary: The system foundation exists, but the career engine is not yet populated with live data
confidence_level: medium
related_files:
  - CURRENT.md
  - ROADMAP.md
  - ops/focus.md
```

### File Mapping
- **Primary file:** `CURRENT.md`
- **Supporting files:** `ROADMAP.md`, `ops/focus.md`

### Future UI Mapping
- Now dashboard header
- State summary panel
- Risk and questions widgets

---

## Schema: heartbeat_alert
### Purpose
Represent a proactive alert emitted by the heartbeat system.

### Fields
- **id:** unique string identifier
- **type:** priority | blocker | career | decision | drift | memory
- **severity:** low | medium | high
- **detected_at:** ISO date or datetime
- **issue:** string
- **why_it_matters:** string
- **next_move:** string
- **source_files:** array[string]
- **related_entity_ids:** array[string]
- **status:** open | acknowledged | resolved | suppressed

### Example
```yaml
id: hb_alert_pipeline_empty
type: career
severity: high
detected_at: 2026-04-02T08:11:00-05:00
issue: Career remains the top priority, but no live opportunities are recorded in the pipeline
why_it_matters: Without visible pipeline state, career movement is likely to stay fragmented and hard to manage
next_move: Add the first real target companies and roles to career/pipeline.md
source_files:
  - career/pipeline.md
  - ops/focus.md
  - HEARTBEAT.md
related_entity_ids: []
status: open
```

### File Mapping
- **Primary logic file:** `HEARTBEAT.md`
- **Future storage file:** `ops/alerts.md` or derived state layer

### Future UI Mapping
- Alert banner
- Attention feed
- Notification center entry

---

## Schema-to-File Summary
| Schema | Current Primary File | Future Supporting / Storage File | UI Surface |
|---|---|---|---|
| opportunity | `career/pipeline.md` | `career/opportunities.md` or derived store | Pipeline tab |
| recruiter_contact | future `career/contacts.md` | contact store / CRM layer | Contacts / Outreach tab |
| decision | `DECISIONS.md` | decision index / derived state | Decision log |
| focus_item | `ops/focus.md` | action queue / derived state | Now / Actions tab |
| current_state | `CURRENT.md` | state snapshot layer | Now dashboard |
| heartbeat_alert | `HEARTBEAT.md` logic | `ops/alerts.md` / alert feed | Alerts / Notification center |
