# product/derived-state.md

## File Role
- **Purpose:** define the derived-state layer for JT7
- **Roadmap step:** JT7-R2.3.3
- **Status:** active specification
- **Implementation status:** spec only; no code

> Consolidation note: this file reflects an earlier broader derived-state/UI-support model. JT7's current consolidated MVP focus is narrower: prove one Gmail/Calendar/manual → Processing → Google Sheets loop and keep Google Sheets as live operational truth. Derived objects remain useful for later UI support, but they are not the current source of operational reality and should not compete with the consolidated runtime model.

## Derived-State Design Rules
- derived objects are computed from canonical files
- derived objects must not become the source of truth
- derived objects should reduce cognitive load, not duplicate raw state blindly
- derived objects should make action, change, and attention more visible
- derived objects should be UI-ready and safe to regenerate

---

## Derived Object: decision_state
### Purpose
Provide a compressed view of the current decision environment.

Use it to answer:
- what active decisions shape the system right now?
- which decisions matter most to current execution?
- are there unresolved, conflicting, or stale decision conditions?

### Required Inputs
- `DECISIONS.md`
- `CURRENT.md`
- `ops/focus.md`
- optional later input: `ROADMAP.md`

### Output Fields
- **id:** unique derived object id
- **generated_at:** ISO date or datetime
- **active_decision_ids:** array[string]
- **decision_count_active:** number
- **decision_count_proposed:** number
- **decision_count_reversed:** number
- **priority_shaping_decision_ids:** array[string]
- **execution_relevant_decision_ids:** array[string]
- **stale_decision_ids:** array[string]
- **missing_decision_signals:** array[string]
- **decision_summary:** string
- **source_files:** array[string]

### Output Logic
- `active_decision_ids` = all canonical decisions with `status: active`
- `priority_shaping_decision_ids` = active decisions directly affecting priority order, roadmap direction, or workstream emphasis
- `execution_relevant_decision_ids` = active decisions referenced by current focus items or current-state required moves
- `stale_decision_ids` = decisions with `next_review_at` in the past or decisions whose implications no longer match current files
- `missing_decision_signals` = inferred areas where current state or focus implies a decision but no canonical decision exists
- `decision_summary` = one-sentence synthesized state of the decision layer

### Example Output
```yaml
id: derived_decision_state_2026_04_02T10_05_00_05_00
generated_at: 2026-04-02T10:05:00-05:00
active_decision_ids:
  - decision_adopt_jt7_identity
  - decision_priority_order_career_product_execution
  - decision_rebuild_scaffold_into_operating_system
  - decision_introduce_foundation_files
  - decision_do_not_pretend_unverified_workspace_state
decision_count_active: 5
decision_count_proposed: 0
decision_count_reversed: 0
priority_shaping_decision_ids:
  - decision_priority_order_career_product_execution
  - decision_rebuild_scaffold_into_operating_system
execution_relevant_decision_ids:
  - decision_priority_order_career_product_execution
  - decision_do_not_pretend_unverified_workspace_state
stale_decision_ids: []
missing_decision_signals:
  - No explicit decision yet defines how live opportunities should be ranked once pipeline data exists
decision_summary: The decision layer is stable and active, but future execution decisions will be needed once live career data enters the system
source_files:
  - DECISIONS.md
  - CURRENT.md
  - ops/focus.md
```

### File Dependencies
- **Primary:** `DECISIONS.md`
- **Supporting:** `CURRENT.md`, `ops/focus.md`

### Future UI Support
- decision summary card on the Now view
- decision health module in a system panel
- stale or missing decision warnings in an attention feed

---

## Derived Object: today_actions
### Purpose
Provide the shortest useful list of actions that should happen today.

Use it to answer:
- what are the highest-leverage moves right now?
- which current tasks are most urgent or blocked?
- what should appear in the Now or Actions tab?

### Required Inputs
- `ops/focus.md`
- `CURRENT.md`
- `career/pipeline.md`
- `DECISIONS.md`

### Output Fields
- **id:** unique derived object id
- **generated_at:** ISO date or datetime
- **action_ids:** array[string]
- **top_action_id:** string | null
- **blocked_action_ids:** array[string]
- **deferred_action_ids:** array[string]
- **career_action_ids:** array[string]
- **product_action_ids:** array[string]
- **execution_action_ids:** array[string]
- **action_count_total:** number
- **action_count_blocked:** number
- **today_summary:** string
- **source_files:** array[string]

### Output Logic
- `action_ids` = focus items of type `next_action` or `priority` with `status: active`
- `top_action_id` = highest-ranked active item, weighted by domain priority and `priority_rank`
- `blocked_action_ids` = focus items with `status: blocked` or actions blocked by unresolved blockers in the same domain
- `deferred_action_ids` = active items intentionally suppressed by anti-focus or future scheduling logic
- `career_action_ids`, `product_action_ids`, `execution_action_ids` = grouped action ids by domain
- `today_summary` = one-sentence summary of the highest-value action posture today

### Example Output
```yaml
id: derived_today_actions_2026_04_02T10_06_00_05_00
generated_at: 2026-04-02T10:06:00-05:00
action_ids:
  - focus_enter_first_pipeline_roles
  - focus_capture_job_search_assets
  - focus_refine_positioning_statement
  - focus_activate_career_engine
  - focus_stabilize_jt7_operating_system
  - focus_reduce_execution_drag
top_action_id: focus_enter_first_pipeline_roles
blocked_action_ids:
  - focus_no_live_pipeline_data
  - focus_missing_asset_inventory
deferred_action_ids: []
career_action_ids:
  - focus_enter_first_pipeline_roles
  - focus_capture_job_search_assets
  - focus_refine_positioning_statement
  - focus_activate_career_engine
product_action_ids:
  - focus_stabilize_jt7_operating_system
execution_action_ids:
  - focus_reduce_execution_drag
action_count_total: 6
action_count_blocked: 2
today_summary: The highest-leverage action today is populating the career pipeline so the top priority becomes operationally visible
source_files:
  - ops/focus.md
  - CURRENT.md
  - career/pipeline.md
  - DECISIONS.md
```

### File Dependencies
- **Primary:** `ops/focus.md`
- **Supporting:** `CURRENT.md`, `career/pipeline.md`, `DECISIONS.md`

### Future UI Support
- Now tab action stack
- Today view shortlist
- blocked-vs-active action split panel
- suggested-first-action card

---

## Derived Object: session_delta
### Purpose
Summarize what changed during the current session or since the last checkpoint.

Use it to answer:
- what files changed?
- what decisions or state changed?
- what should the user know when returning after a break?

### Required Inputs
- `CURRENT.md`
- `ops/focus.md`
- `career/pipeline.md`
- `DECISIONS.md`
- optional later input: `ROADMAP.md`
- optional later input: daily memory file

### Output Fields
- **id:** unique derived object id
- **generated_at:** ISO date or datetime
- **changed_files:** array[string]
- **new_decision_ids:** array[string]
- **updated_focus_item_ids:** array[string]
- **updated_opportunity_ids:** array[string]
- **state_changes:** array[string]
- **roadmap_step_before:** string | null
- **roadmap_step_after:** string | null
- **resume_point:** string | null
- **session_summary:** string
- **source_files:** array[string]

### Output Logic
- `changed_files` = files touched during the session or after the last stored checkpoint
- `new_decision_ids` = decision ids added since the checkpoint
- `updated_focus_item_ids` = focus items added or materially changed since the checkpoint
- `updated_opportunity_ids` = opportunity ids added or materially changed since the checkpoint
- `state_changes` = normalized list of meaningful changes in system state
- `roadmap_step_before` / `roadmap_step_after` = step transition, if any
- `resume_point` = next step or exact place to continue
- `session_summary` = one-sentence summary of what changed and what should happen next

### Example Output
```yaml
id: derived_session_delta_2026_04_02T10_07_00_05_00
generated_at: 2026-04-02T10:07:00-05:00
changed_files:
  - CURRENT.md
  - ops/focus.md
  - career/pipeline.md
  - DECISIONS.md
new_decision_ids: []
updated_focus_item_ids:
  - focus_activate_career_engine
  - focus_enter_first_pipeline_roles
  - focus_no_live_pipeline_data
updated_opportunity_ids:
  - opp_pipeline_initial_placeholder
state_changes:
  - CURRENT.md aligned to canonical current_state structure
  - ops/focus.md aligned to canonical focus_item structure
  - career/pipeline.md aligned to canonical opportunity structure
  - DECISIONS.md aligned to canonical decision structure
roadmap_step_before: JT7-R2.3.2
roadmap_step_after: JT7-R2.3.3
resume_point: JT7-R2.4.1
session_summary: Canonical file alignment is complete and the next phase begins with integrations
source_files:
  - CURRENT.md
  - ops/focus.md
  - career/pipeline.md
  - DECISIONS.md
```

### File Dependencies
- **Primary:** `CURRENT.md`, `ops/focus.md`, `career/pipeline.md`, `DECISIONS.md`
- **Supporting later:** `ROADMAP.md`, `memory/YYYY-MM-DD.md`

### Future UI Support
- session recap panel
- return-to-work banner
- change log timeline
- resume card after breaks or restarts

---

## Dependency Summary
| Derived Object | Primary Inputs | Output Focus | UI Panel |
|---|---|---|---|
| decision_state | `DECISIONS.md`, `CURRENT.md`, `ops/focus.md` | decision health and relevance | Decision summary / system panel |
| today_actions | `ops/focus.md`, `CURRENT.md`, `career/pipeline.md`, `DECISIONS.md` | best current actions | Now / Actions tab |
| session_delta | `CURRENT.md`, `ops/focus.md`, `career/pipeline.md`, `DECISIONS.md` | what changed and where to resume | Session recap / resume banner |

## File Connection Notes
### Connection to `CURRENT.md`
- provides system phase, current step, top priorities, risks, open questions, and required next moves
- anchors `today_actions` and `session_delta`
- helps `decision_state` determine which decisions are actively shaping present execution

### Connection to `ops/focus.md`
- provides the active priority, next_action, blocker, and anti_focus records
- is the main source for `today_actions`
- informs `decision_state` about execution-relevant decisions
- contributes changed focus items to `session_delta`

### Connection to `career/pipeline.md`
- provides opportunity state, blockers, and missing live data
- helps `today_actions` determine whether the career engine is actually active
- contributes changed opportunity ids to `session_delta`
- can trigger missing-decision signals in `decision_state` when pipeline policy becomes necessary

### Connection to `DECISIONS.md`
- is the primary source for `decision_state`
- constrains action ordering and interpretation in `today_actions`
- contributes new or changed decision ids to `session_delta`
- helps future UI explain not just what is active, but why
