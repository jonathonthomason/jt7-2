# JT7 Workbook Implementation Plan

## Document Metadata
- **System:** JT7 Job Intelligence System
- **Document type:** workbook implementation contract
- **Status:** draft-initial
- **Primary path:** `JT7/00_System/Architecture/JT7_Workbook_Implementation_Plan.md`

## 1. Workbook Strategy

> Consolidation note: this document reflects an earlier, richer multi-entity workbook model. JT7's current consolidated MVP operating model uses Google Sheets as the single operational source of truth, but runtime/business logic now centers on a shared schema (`company`, `role`, `status`, `last_activity`, `next_step`, `contact`, `source`, `thread_id`, `notes`) and a single final status model (`Applied`, `Recruiter Contacted`, `Screening`, `Interviewing`, `Offer`, `Rejected`, `Cold`). Until this file is fully rewritten, treat it as partially legacy and subordinate to the newer consolidated runtime/governance rules.

### Decision
Use **one workbook with multiple tabs** as the V1 implementation.

### Recommendation
**Chosen approach:** single workbook with multiple tabs.

### Why
- easiest for humans to review in one place
- easiest for agents to read/write with a single canonical structured data surface
- lookup values can be centralized cleanly
- cross-entity navigation is simpler
- lower operational overhead than coordinating multiple files
- best fit for early implementation and controlled migration from an existing spreadsheet

### Not chosen
Separate files per entity are not recommended for V1 because they increase coordination cost, linking complexity, and migration friction.

## 2. Workbook Structure

## 2.1 Required Tabs
1. `Jobs`
2. `Recruiters`
3. `Communications`
4. `Competition`
5. `Lookup`

## 2.2 Optional Future Tabs
- `Dashboard`
- `Review_Queue`

## 3. Tab Definitions

## 3.1 Jobs
- **Purpose:** canonical opportunity tracker
- **Source entity:** `JT7_Jobs_Data_Spec.md`
- **Who writes:** human + agent
- **Sensitivity level:** mixed; some columns safe to edit, some controlled

## 3.2 Recruiters
- **Purpose:** canonical recruiter/contact tracker
- **Source entity:** `JT7_Recruiters_Data_Spec.md`
- **Who writes:** human + agent
- **Sensitivity level:** mixed; identity and status columns require care

## 3.3 Communications
- **Purpose:** canonical communication event log
- **Source entity:** `JT7_Communications_Data_Spec.md`
- **Who writes:** human + agent
- **Sensitivity level:** mixed; event identity and status columns require care

## 3.4 Competition
- **Purpose:** canonical market-intelligence benchmark tracker
- **Source entity:** `JT7_Competition_Data_Spec.md`
- **Who writes:** human + agent
- **Sensitivity level:** mixed; identity and signal fields require care

## 3.5 Lookup
- **Purpose:** single source of truth for controlled values
- **Source entity:** `JT7_Lookup_and_Controlled_Values_Spec.md`
- **Who writes:** human + agent only through explicit controlled update process
- **Sensitivity level:** controlled; should not be casually edited

## 4. Column Mapping

## 4.1 Jobs Tab

| Order | Column | Spec Field | Required | Controlled | Derived | Agent Write | Human Edit |
|---|---|---|---:|---:|---:|---:|---:|
| 1 | job_id | job_id | yes | no | generated | yes | careful |
| 2 | status | status | yes | yes | no | yes | careful |
| 3 | company | company | yes | no | no | yes | yes |
| 4 | title | title | yes | no | no | yes | yes |
| 5 | recruiter_id | recruiter_id | no | no | no | yes | yes |
| 6 | source_type | source_type | yes | yes | no | yes | careful |
| 7 | source_platform | source_platform | no | yes | no | yes | careful |
| 8 | posting_url | posting_url | no | no | no | yes | yes |
| 9 | direct_apply_url | direct_apply_url | no | no | no | yes | yes |
| 10 | company_careers_url | company_careers_url | no | no | no | yes | yes |
| 11 | location | location | no | no | no | yes | yes |
| 12 | location_type | location_type | no | yes | no | yes | careful |
| 13 | fit_score | fit_score | no | no | no | yes | yes |
| 14 | fit_notes | fit_notes | no | no | no | yes | yes |
| 15 | salary_min | salary_min | no | no | no | yes | yes |
| 16 | salary_max | salary_max | no | no | no | yes | yes |
| 17 | salary_raw | salary_raw | no | no | no | yes | yes |
| 18 | posted_date | posted_date | no | no | no | yes | yes |
| 19 | date_found | date_found | yes | no | no | yes | careful |
| 20 | date_applied | date_applied | no | no | no | yes | yes |
| 21 | last_status_change | last_status_change | yes | no | derived on status update | yes | careful |
| 22 | followup_date | followup_date | no | no | no | yes | yes |
| 23 | notes | notes | no | no | no | yes | yes |
| 24 | sync_status | sync_status | yes | yes | no | yes | careful |
| 25 | created_at | created_at | yes | no | generated | yes | no |
| 26 | updated_at | updated_at | yes | no | generated | yes | no |
| 27 | source_ref | source_ref | no | no | no | yes | careful |

## 4.2 Recruiters Tab

| Order | Column | Spec Field | Required | Controlled | Derived | Agent Write | Human Edit |
|---|---|---|---:|---:|---:|---:|---:|
| 1 | recruiter_id | recruiter_id | yes | no | generated | yes | careful |
| 2 | full_name | full_name | yes* | no | no | yes | yes |
| 3 | company | company | no | no | no | yes | yes |
| 4 | contact_type | contact_type | yes | yes | no | yes | careful |
| 5 | relationship_status | relationship_status | yes | yes | no | yes | careful |
| 6 | outreach_status | outreach_status | yes | yes | no | yes | careful |
| 7 | email | email | no | no | no | yes | yes |
| 8 | email_aliases | email_aliases | no | no | no | yes | careful |
| 9 | linkedin_url | linkedin_url | no | no | no | yes | yes |
| 10 | role_title | role_title | no | no | no | yes | yes |
| 11 | linked_job_ids | linked_job_ids | no | no | no | yes | careful |
| 12 | next_followup_date | next_followup_date | no | no | no | yes | yes |
| 13 | last_contacted_at | last_contacted_at | no | no | derived from comms/input | yes | careful |
| 14 | last_response_at | last_response_at | no | no | derived from comms/input | yes | careful |
| 15 | source_type | source_type | yes | yes | no | yes | careful |
| 16 | source_detail | source_detail | no | no | no | yes | yes |
| 17 | phone | phone | no | no | no | yes | yes |
| 18 | location | location | no | no | no | yes | yes |
| 19 | notes | notes | no | no | no | yes | yes |
| 20 | sync_status | sync_status | yes | yes | no | yes | careful |
| 21 | created_at | created_at | yes | no | generated | yes | no |
| 22 | updated_at | updated_at | yes | no | generated | yes | no |
| 23 | first_name | first_name | no | no | derived/manual | yes | yes |
| 24 | last_name | last_name | no | no | derived/manual | yes | yes |

## 4.3 Communications Tab

| Order | Column | Spec Field | Required | Controlled | Derived | Agent Write | Human Edit |
|---|---|---|---:|---:|---:|---:|---:|
| 1 | comm_id | comm_id | yes | no | generated | yes | careful |
| 2 | recruiter_id | recruiter_id | yes* | no | no | yes | careful |
| 3 | job_id | job_id | no | no | no | yes | careful |
| 4 | channel | channel | yes | yes | no | yes | careful |
| 5 | direction | direction | yes | yes | no | yes | careful |
| 6 | status | status | yes | yes | no | yes | careful |
| 7 | outcome | outcome | yes | yes | no | yes | careful |
| 8 | action_required | action_required | yes | yes | no | yes | careful |
| 9 | response_expected | response_expected | yes | no | no | yes | yes |
| 10 | next_followup_date | next_followup_date | no | no | no | yes | yes |
| 11 | subject_or_topic | subject_or_topic | no | no | no | yes | yes |
| 12 | summary | summary | yes | no | no | yes | yes |
| 13 | raw_excerpt | raw_excerpt | no | no | no | yes | yes |
| 14 | full_text_reference | full_text_reference | no | no | no | yes | careful |
| 15 | source_type | source_type | yes | yes | no | yes | careful |
| 16 | source_ref | source_ref | no | no | no | yes | careful |
| 17 | thread_ref | thread_ref | no | no | no | yes | careful |
| 18 | date_sent | date_sent | no | no | no | yes | careful |
| 19 | date_received | date_received | no | no | no | yes | careful |
| 20 | notes | notes | no | no | no | yes | yes |
| 21 | sync_status | sync_status | yes | yes | no | yes | careful |
| 22 | created_at | created_at | yes | no | generated | yes | no |
| 23 | updated_at | updated_at | yes | no | generated | yes | no |

## 4.4 Competition Tab

| Order | Column | Spec Field | Required | Controlled | Derived | Agent Write | Human Edit |
|---|---|---|---:|---:|---:|---:|---:|
| 1 | competition_id | competition_id | yes | no | generated | yes | careful |
| 2 | person_name | person_name | yes* | no | no | yes | yes |
| 3 | company | company | no | no | no | yes | yes |
| 4 | role_title | role_title | no | no | no | yes | yes |
| 5 | benchmark_type | benchmark_type | yes | yes | no | yes | careful |
| 6 | signal_strength | signal_strength | yes | yes | no | yes | careful |
| 7 | role_level_signal | role_level_signal | yes | yes | no | yes | careful |
| 8 | status | status | yes | yes | no | yes | careful |
| 9 | current_location | current_location | no | no | no | yes | yes |
| 10 | target_location | target_location | no | no | no | yes | yes |
| 11 | linkedin_url | linkedin_url | no | no | no | yes | yes |
| 12 | portfolio_url | portfolio_url | no | no | no | yes | yes |
| 13 | source_type | source_type | yes | yes | no | yes | careful |
| 14 | source_detail | source_detail | no | no | no | yes | yes |
| 15 | skills_signals | skills_signals | no | no | no | yes | yes |
| 16 | industry_signals | industry_signals | no | no | no | yes | yes |
| 17 | compensation_signal | compensation_signal | no | no | no | yes | yes |
| 18 | date_logged | date_logged | yes | no | no | yes | careful |
| 19 | last_reviewed_at | last_reviewed_at | no | no | derived/manual | yes | careful |
| 20 | notes | notes | no | no | no | yes | yes |
| 21 | sync_status | sync_status | yes | yes | no | yes | careful |
| 22 | created_at | created_at | yes | no | generated | yes | no |
| 23 | updated_at | updated_at | yes | no | generated | yes | no |

## 4.5 Lookup Tab

| Order | Column | Purpose |
|---|---|---|
| 1 | lookup_group | category name |
| 2 | value_key | canonical machine value |
| 3 | value_label | human-readable label |
| 4 | description | meaning/usage summary |
| 5 | active | true/false availability |
| 6 | sort_order | display order |
| 7 | notes | optional operational notes |

## 5. ID and Linking Strategy

## 5.1 ID Storage
- each entity uses a canonical string ID in its first column
- IDs are stored as plain text
- IDs must remain stable after creation

## 5.2 Cross-Entity References
- `Jobs.recruiter_id` links to `Recruiters.recruiter_id`
- `Recruiters.linked_job_ids` stores one or more `job_id` values
- `Communications.recruiter_id` links to `Recruiters.recruiter_id`
- `Communications.job_id` links to `Jobs.job_id`

## 5.3 linked_job_ids Representation
- use multi-value text in V1
- delimiter: `|`
- values must be canonical job IDs only
- no names or titles in reference columns

## 5.4 Relationship Resolution Rules
Agents should:
- resolve by ID first
- resolve by identity logic second
- write null for optional unresolved links only where allowed by the entity spec
- block canonical write where required link is missing and no staging path exists

## 5.5 Missing Link Handling
- missing optional link: allow null
- missing required link: block or stage outside canonical sheet
- never invent IDs

## 6. Lookup Integration

## 6.1 Lookup Tab Structure
Use one dedicated `Lookup` tab with grouped value rows.

Each entity tab should reference `value_key` values from the relevant `lookup_group`.

## 6.2 Dropdown Validation
Dropdown validation should be used for all controlled-value columns.
Validation should reference the Lookup tab, not independent hardcoded lists where possible.

## 6.3 Columns That Must Use Controlled Values
### Jobs
- status
- source_type
- source_platform
- location_type
- sync_status

### Recruiters
- contact_type
- relationship_status
- outreach_status
- source_type
- sync_status

### Communications
- channel
- direction
- status
- outcome
- action_required
- source_type
- sync_status

### Competition
- benchmark_type
- signal_strength
- role_level_signal
- status
- source_type
- sync_status

## 6.4 Drift Prevention
- no freeform status/category values in entity tabs
- inactive values remain in Lookup history but are excluded from active use
- agents must validate against Lookup before write

## 6.5 Agent Validation Rule
Before writing, agents must:
- validate all controlled-value fields
- normalize fuzzy input to canonical value when unambiguous
- reject unknown controlled values
- avoid writing deprecated values unless explicitly handling legacy records

## 7. Write Behavior Rules

## 7.1 Required Fields Before Write
Agents and Telegram-triggered writes must satisfy each entity’s minimum create requirements before writing canonical rows.

## 7.2 Default Values
Default only where explicitly supported by the entity spec.
Examples:
- sync_status may default to `clean` in normal online canonical writes
- jobs status may default to `saved` only if workflow policy allows it
- competition `role_level_signal` may default to `unknown` where allowed

## 7.3 Block Writes When
- required fields are missing
- required controlled values are invalid
- duplicate certainty is high and update/merge path is ignored
- required relationship field is missing with no permitted partial/staging path

## 7.4 Partial Writes
Allowed only where the entity spec permits them.
Examples:
- job without posting URL
- recruiter without email
- communication without job_id
- competition record without LinkedIn URL

## 7.5 Missing Relationships
- write null only for relationships explicitly allowed to be null
- do not fabricate cross-entity links
- preserve unresolved relationship as null or external review item

## 7.6 Append vs Overwrite Rules
- notes should generally append, not replace useful prior context
- timestamps should overwrite with latest valid event data where appropriate
- IDs should never be overwritten casually

## 8. Update Behavior Rules

## 8.1 Record Update Logic
- update existing row when identity match confidence is high
- create new row when identity is clearly new
- flag for manual review when confidence is medium and merge risk exists

## 8.2 Timestamp Behavior
- `created_at` immutable after creation
- `updated_at` updates on every successful write
- status-specific timestamps update only when relevant state changes

## 8.3 Status Change Tracking
For V1:
- update current status column
- update relevant status timestamp column if one exists
- append minimal note if needed to preserve context

## 8.4 Notes Behavior
- append concise operational context
- avoid long freeform logs inside notes cells
- if detail becomes too large, move it into reference docs and link back

## 8.5 Conflicting Updates
If conflicting update arrives:
- prefer stronger verified source
- preserve old context in notes when useful
- flag for review if conflict affects identity or high-risk state

## 9. Deduplication in Spreadsheet Context

## 9.1 How Duplicates Are Detected In-Sheet
Agents should check existing rows using each entity’s identity rules before write.

## 9.2 Agent Pre-Write Check
Before create, agent should:
1. validate required fields
2. normalize controlled values
3. search for duplicate by primary keys
4. search by fallback matching logic if primary identity missing
5. choose update / create / manual review

## 9.3 Flagging Duplicates
When probable duplicate is uncertain:
- do not auto-merge silently
- add to manual review process or operational note
- preserve candidate conflict details externally if needed

## 9.4 Merge vs Manual Review
- merge when high-confidence identity match exists
- manual review when only fuzzy identity overlap exists

## 10. Human vs Agent Editing Boundaries

## 10.1 Human-Editable Freely
Generally safe human-edit columns:
- company/title/location text
- notes
- fit notes / signal notes
- source_detail
- next_followup_date
- summary fields

## 10.2 Human-Editable Carefully
Columns humans should treat carefully:
- IDs
- controlled-value status fields
- relationship reference IDs
- timestamps
- URLs used for identity

## 10.3 Agent-Controlled Columns
Prefer agent/system control for:
- generated IDs
- created_at
- updated_at
- sync_status
- duplicate-sensitive linkage fields during automated ingestion

## 10.4 Validation Warning Triggers
Warnings should occur when humans edit:
- controlled value fields with invalid value
- identity fields in a way that may create duplicates
- linked ID columns with non-canonical values
- timestamps in invalid formats

## 11. Versioning and Backup Behavior

## 11.1 Workbook Versioning
- maintain one canonical workbook file name for active use
- create dated snapshots when major schema or content changes occur
- archive superseded workbook versions rather than overwriting without recoverability

## 11.2 Snapshot Timing
Create snapshots when:
- schema changes materially
- migration completes
- large imports complete
- reconciliation after degraded mode resolves

## 11.3 Backup Naming Convention
Recommended backup naming pattern:
- `<workbook_name>_YYYY-MM-DD_HHMM`

## 11.4 Mirror and Backup Interaction
- Drive workbook is canonical in online mode
- local mirror holds the current working copy/fallback
- backup layer stores dated recovery snapshots
- backup failure must not block canonical write success

## 12. Migration Plan from Existing Spreadsheet

## 12.1 Evaluation Process
The current spreadsheet should be evaluated for:
- sheet/tab count
- existing column names
- mixed-purpose tabs
- duplicated fields
- freeform status values
- identity/linking gaps
- notes that should become structured fields

## 12.2 What Maps Directly
Likely direct mappings:
- existing job rows → Jobs
- recruiter lists → Recruiters
- communication logs → Communications
- market/competition sheets → Competition
- status/value lists → Lookup

## 12.3 What Needs Renaming
Rename columns when:
- names are inconsistent with canonical spec
- multiple similar columns represent same field
- field names are ambiguous or UI-only

## 12.4 What Needs Splitting
Split when:
- one sheet mixes recruiters and communications
- one column mixes multiple values that deserve structure
- notes fields contain repeatable structured data

## 12.5 What Should Be Deprecated
Deprecate:
- duplicate status columns
- freeform uncontrolled categories
- mixed entity tabs without stable identity
- legacy columns that cannot be interpreted safely

## 12.6 How to Avoid Data Loss
- do not overwrite the current spreadsheet in place without snapshot
- inventory columns before remapping
- keep original raw export/reference during migration
- migrate into explicit canonical fields and preserve ambiguous source context in notes or archive

## 12.7 Recommendation
**Recommended approach: create a clean V1 workbook, then migrate data into it.**

### Why
- cleaner than forcing existing mixed structure into canonical rules
- reduces drift and legacy ambiguity
- makes controlled values enforceable from day one
- safer for agents and future automation

## 13. Recommended V1 Workbook Setup

## 13.1 Exact Tabs
- Jobs
- Recruiters
- Communications
- Competition
- Lookup

## 13.2 Minimal Columns Per Tab
### Jobs
- job_id
- status
- company
- title
- recruiter_id
- source_type
- source_platform
- posting_url
- date_found
- last_status_change
- notes
- sync_status
- created_at
- updated_at

### Recruiters
- recruiter_id
- full_name
- company
- contact_type
- relationship_status
- outreach_status
- email
- linkedin_url
- linked_job_ids
- next_followup_date
- last_contacted_at
- last_response_at
- notes
- sync_status
- created_at
- updated_at

### Communications
- comm_id
- recruiter_id
- job_id
- channel
- direction
- status
- outcome
- action_required
- response_expected
- summary
- source_type
- next_followup_date
- sync_status
- created_at
- updated_at

### Competition
- competition_id
- person_name
- benchmark_type
- signal_strength
- role_level_signal
- status
- source_type
- date_logged
- notes
- sync_status
- created_at
- updated_at

### Lookup
- lookup_group
- value_key
- value_label
- description
- active
- sort_order
- notes

## 13.3 What Is Required to Start Execution Immediately
- workbook created with required tabs
- canonical columns created in exact order
- Lookup tab populated with V1 controlled values
- dropdown validation configured for controlled fields
- IDs and timestamps handled consistently

## 13.4 What Can Wait
- Dashboard tab
- Review Queue tab
- extended helper formulas
- richer derived/reporting views
- nonessential optional columns

## 14. Ready for Execution
Once this document is complete, the system is ready to move to:
- spreadsheet creation
- Telegram command implementation
- ingestion workflows
