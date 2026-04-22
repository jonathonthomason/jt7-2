# JT7 Structured Data Master Plan

## Document Metadata
- **System:** JT7 Job Intelligence System
- **Document type:** structured data master plan
- **Status:** draft-initial
- **Primary path:** `JT7/00_System/Architecture/JT7_Structured_Data_Master_Plan.md`
- **Purpose:** define the normalized spreadsheet-based data model for core JT7 entities and their operational rules

## 1. Document Role
> Consolidation note: this document reflects a broader earlier structured-data vision with multiple rich entities. JT7's current consolidated MVP operating model is narrower: Google Sheets remains the single operational source of truth, and the active runtime loop is centered on Gmail/Calendar/manual evidence flowing into a simpler shared schema and status model. Until rewritten, treat this document as partially legacy and subordinate to `JT7_MVP_Governance.md`.

This document defines the structured data layer for JT7.
It covers:
- entities
- schemas
- identity rules
- relationships
- status systems
- deduplication
- write/update behavior
- lookup tables
- spreadsheet structure
- validation rules
- extensibility rules

It is intended for both human operators and agents.

## 2. Design Goals
- easy for humans to review in spreadsheets
- safe for agents to read and write
- normalized enough to reduce duplication and drift
- extensible without breaking existing records
- explicit about identity, status, and linking rules
- practical for incremental implementation

## 3. Core Entities

## 3.1 Jobs
- **Purpose:** track jobs/opportunities through the search lifecycle
- **Role in system:** canonical opportunity layer
- **Relationships:**
  - may link to zero or more recruiters
  - may link to zero or more communications
  - may reference competition records indirectly

## 3.2 Recruiters
- **Purpose:** track recruiters, hiring managers, referrers, and similar contacts
- **Role in system:** canonical contact layer for opportunity-related relationships
- **Relationships:**
  - may link to zero or more jobs
  - may link to zero or more communications

## 3.3 Communications
- **Purpose:** track communication events across email, LinkedIn, calls, and related channels
- **Role in system:** canonical communication/event layer
- **Relationships:**
  - may link to one recruiter
  - may link to one job
  - may exist with one link missing temporarily if data is incomplete

## 3.4 Competition
- **Purpose:** track competition signals, peer candidates, or role competition context
- **Role in system:** contextual intelligence layer
- **Relationships:**
  - standalone by default
  - may optionally reference jobs or companies later

## 3.5 Lookup Tables
- **Purpose:** centralize controlled values used by all other entities
- **Role in system:** normalization and validation support
- **Relationships:**
  - all status, channel, source, and sync fields should resolve against lookups

## 4. Entity Schemas

## 4.1 Jobs Schema

| Field Name | Type | Required | Description | Example |
|---|---|---:|---|---|
| job_id | id | yes | canonical unique job record id | `job_figma_principal_product_designer_20260402` |
| company_name | string | yes | company tied to the job | `Figma` |
| job_title | string | yes | role title | `Principal Product Designer` |
| source_type | enum | yes | acquisition source | `linkedin` |
| source_url | string | no | canonical listing URL if available | `https://...` |
| source_ref | string | no | external reference id or import reference | `linkedin_job_12345` |
| location | string | no | human-readable location | `Remote (US)` |
| location_type | enum | no | normalized location mode | `remote` |
| compensation_text | string | no | raw comp text | `$220k-$260k + equity` |
| status | enum | yes | current pipeline state | `saved` |
| status_updated_at | datetime | yes | last status change time | `2026-04-02T20:00:00Z` |
| priority | enum | no | priority band | `high` |
| fit_score | number | no | normalized fit estimate | `8` |
| fit_notes | string | no | short fit rationale | `Strong systems/design leadership fit` |
| recruiter_ids | list[id] | no | linked recruiters | `rec_jane_doe_linkedin` |
| last_communication_id | id | no | most recent linked communication | `com_20260402_jane_email_01` |
| next_action | string | no | explicit next move | `Tailor resume and apply` |
| next_action_due | date | no | due date for next action | `2026-04-04` |
| notes | string | no | short operational notes | `Role aligns with principal-level systems work` |
| sync_status | enum | yes | record sync state | `clean` |
| created_at | datetime | yes | first record creation time | `2026-04-02T19:55:00Z` |
| updated_at | datetime | yes | last record update time | `2026-04-02T20:00:00Z` |

## 4.2 Recruiters Schema

| Field Name | Type | Required | Description | Example |
|---|---|---:|---|---|
| recruiter_id | id | yes | canonical recruiter/contact id | `rec_jane_doe_linkedin` |
| full_name | string | yes | recruiter/contact name | `Jane Doe` |
| company_name | string | no | associated company | `Figma` |
| role_type | enum | yes | recruiter / hiring_manager / referrer / other | `recruiter` |
| email | string | no | contact email | `jane@figma.com` |
| linkedin_url | string | no | LinkedIn profile URL | `https://linkedin.com/in/...` |
| phone | string | no | phone if available | `+1-555-...` |
| status | enum | yes | current recruiter relationship state | `warm` |
| last_contact_at | datetime | no | most recent known contact time | `2026-04-02T16:20:00Z` |
| last_contact_channel | enum | no | latest communication channel | `email` |
| linked_job_ids | list[id] | no | related jobs | `job_figma_principal_product_designer_20260402` |
| notes | string | no | operational notes | `Reached out after portfolio review` |
| sync_status | enum | yes | record sync state | `clean` |
| created_at | datetime | yes | first record creation time | `2026-04-02T16:20:00Z` |
| updated_at | datetime | yes | last update time | `2026-04-02T16:20:00Z` |

## 4.3 Communications Schema

| Field Name | Type | Required | Description | Example |
|---|---|---:|---|---|
| communication_id | id | yes | canonical communication id | `com_20260402_jane_email_01` |
| occurred_at | datetime | yes | communication timestamp | `2026-04-02T16:20:00Z` |
| channel | enum | yes | email / linkedin / call / text / other | `email` |
| direction | enum | yes | inbound / outbound | `inbound` |
| recruiter_id | id | no | linked recruiter/contact | `rec_jane_doe_linkedin` |
| job_id | id | no | linked job | `job_figma_principal_product_designer_20260402` |
| subject_or_topic | string | no | short title or topic | `Intro re: principal design role` |
| summary | string | yes | concise communication summary | `Recruiter reached out about principal role` |
| raw_source_ref | string | no | external message/thread reference | `gmail_thread_abc123` |
| status | enum | yes | communication state | `pending` |
| next_action | string | no | required follow-up | `Reply with availability` |
| next_action_due | date | no | due date for follow-up | `2026-04-03` |
| notes | string | no | additional communication notes | `Portfolio likely reviewed` |
| sync_status | enum | yes | record sync state | `clean` |
| created_at | datetime | yes | first record creation time | `2026-04-02T16:25:00Z` |
| updated_at | datetime | yes | last update time | `2026-04-02T16:25:00Z` |

## 4.4 Competition Schema

| Field Name | Type | Required | Description | Example |
|---|---|---:|---|---|
| competition_id | id | yes | canonical competition record id | `comp_john_smith_figma_principal_pd` |
| person_name | string | yes | candidate or competitive signal identity | `John Smith` |
| company_name | string | no | associated company if known | `Figma` |
| role_title | string | no | role they are tied to if known | `Principal Product Designer` |
| signal_type | enum | yes | candidate / market_signal / internal_competition / other | `candidate` |
| source_type | enum | no | where the signal came from | `community` |
| signal_date | date | no | when the signal was observed | `2026-04-01` |
| summary | string | yes | concise description of the competition signal | `Mentioned as another candidate already in process` |
| confidence | enum | no | low / medium / high | `medium` |
| notes | string | no | supporting context | `Mention came through private Slack group` |
| sync_status | enum | yes | record sync state | `clean` |
| created_at | datetime | yes | first creation time | `2026-04-02T18:00:00Z` |
| updated_at | datetime | yes | last update time | `2026-04-02T18:00:00Z` |

## 4.5 Lookup Tables Schema

Lookup tables should minimally include:
- job_statuses
- recruiter_statuses
- communication_statuses
- communication_channels
- source_types
- sync_status_values
- location_types
- role_types
- signal_types

Suggested fields for lookup records:

| Field Name | Type | Required | Description | Example |
|---|---|---:|---|---|
| lookup_group | string | yes | lookup table name | `job_statuses` |
| value_key | string | yes | machine-readable value | `applied` |
| value_label | string | yes | human-readable label | `Applied` |
| sort_order | number | no | ordering control | `2` |
| active | boolean | yes | whether value is usable | `true` |
| notes | string | no | explanatory notes | `Used after application submission` |

## 5. Identity Rules

## 5.1 Job Identity
### Preferred uniqueness inputs
- `source_url` if stable and available
- otherwise: normalized `company_name` + normalized `job_title` + source context

### Recommended ID generation
- `job_<normalized_company>_<normalized_title>_<yyyymmdd>`

### Create vs Update Rule
- create when no existing record matches canonical identity
- update when same role/company/source already exists

### Duplicate detection keys
1. exact `source_url`
2. exact `source_ref`
3. normalized `company_name + job_title`

## 5.2 Recruiter Identity
### Preferred uniqueness inputs
- email if available
- otherwise LinkedIn URL
- otherwise normalized `full_name + company_name`

### Recommended ID generation
- `rec_<normalized_name>_<primary_identity_token>`

### Create vs Update Rule
- create when no existing recruiter identity matches
- update when email or LinkedIn URL already matches

### Duplicate detection keys
1. exact email
2. exact LinkedIn URL
3. normalized full name + company

## 5.3 Communication Identity
### Preferred uniqueness inputs
- external message/thread reference if available
- otherwise `occurred_at + recruiter_id + channel + direction`

### Recommended ID generation
- `com_<yyyymmdd>_<normalized_contact_or_unknown>_<channel>_<sequence>`

### Create vs Update Rule
- create for new event
- update when same source reference or same event tuple is detected

### Duplicate detection keys
1. exact `raw_source_ref`
2. exact timestamp + recruiter + channel + direction

## 5.4 Competition Identity
### Preferred uniqueness inputs
- normalized `person_name + company_name + role_title`

### Recommended ID generation
- `comp_<normalized_name>_<normalized_company>_<normalized_role>`

### Create vs Update Rule
- create when identity tuple is new
- update when same person/company/role signal reappears with more detail

### Duplicate detection keys
1. normalized name + company + role
2. if no role, normalized name + company + signal type

## 6. Relationships

## 6.1 Jobs ↔ Recruiters
- stored using IDs, not names
- Jobs store `recruiter_ids`
- Recruiters store `linked_job_ids`

### Missing link rule
- if relationship is likely but not confirmed, do not fabricate link
- keep record unlinked until enough evidence exists

## 6.2 Communications ↔ Recruiters
- Communications store `recruiter_id`
- Recruiter records may infer `last_contact_at` and `last_contact_channel` from communications

### Missing link rule
- allow communication record with null `recruiter_id` temporarily
- require later reconciliation if enough contact info becomes available

## 6.3 Communications ↔ Jobs
- Communications store `job_id`
- Jobs may store `last_communication_id`

### Missing link rule
- if communication references a role but exact job mapping is uncertain, keep `job_id` null and flag for review

## 6.4 Competition
- standalone by default
- may later reference company or job IDs if modeled explicitly
- should not block operation if relationship is unknown

## 7. Status Systems

## 7.1 Jobs Status Values
- `saved`
- `applied`
- `interviewing`
- `offer`
- `rejected`
- `archived`

### Allowed transitions
- saved → applied
- saved → archived
- applied → interviewing
- applied → rejected
- interviewing → offer
- interviewing → rejected
- offer → archived
- rejected → archived

### Invalid transitions
- archived → interviewing without explicit reopen logic
- rejected → offer without intermediate review/update

### Auto-update triggers
- application confirmation can move saved → applied
- interview scheduling can move applied → interviewing
- explicit rejection can move applied/interviewing → rejected

## 7.2 Recruiters Status Values
- `cold`
- `warm`
- `active`
- `dormant`

### Allowed transitions
- cold → warm
- warm → active
- active → dormant
- dormant → warm

### Invalid transitions
- cold → dormant without any prior interaction context

### Auto-update triggers
- inbound recruiter contact can move cold → warm
- active communication thread can move warm → active
- long inactivity can move active → dormant

## 7.3 Communications Status Values
- `pending`
- `responded`
- `no_response`
- `scheduled`
- `closed`

### Allowed transitions
- pending → responded
- pending → no_response
- responded → scheduled
- responded → closed
- scheduled → closed

### Invalid transitions
- closed → pending without a new communication record

### Auto-update triggers
- reply sent/received can move pending → responded
- scheduled meeting/interview can move responded → scheduled
- completed or dead conversation can move to closed

## 8. Deduplication Logic

## 8.1 Jobs
### Duplicate fields
- source_url
- source_ref
- normalized company + title

### If duplicate found
- prefer update over create
- append operational notes rather than overwrite blindly
- preserve earliest `created_at`
- update `updated_at`

### Merge rule
- merge structured fields from the strongest/newest record
- preserve existing notes by append-with-separator or normalized note history later

## 8.2 Recruiters
### Duplicate fields
- email
- LinkedIn URL
- full name + company

### If duplicate found
- update existing record
- merge missing fields into richer profile
- preserve stable recruiter_id

## 8.3 Communications
### Duplicate fields
- raw_source_ref
- occurred_at + recruiter_id + channel + direction

### If duplicate found
- update summary/notes only if new information is materially better
- do not create duplicate communication event rows

## 8.4 Competition
### Duplicate fields
- person name + company + role
- person name + company + signal_type if role missing

### If duplicate found
- update notes/confidence/source detail
- do not create duplicate competitive records for same signal identity

## 9. Write Rules

## 9.1 General Write Rule
Agents and Telegram-triggered workflows should create records only when minimum required identity and schema conditions are met.

## 9.2 Jobs Write Rule
### Required before create
- company_name
- job_title
- status
- status_updated_at
- created_at
- updated_at
- sync_status

### Defaults if missing
- `status = saved`
- `sync_status = clean` if canonical direct write, otherwise pending state if degraded-mode logic exists later
- `priority = null`

### Block write when
- company and title are both missing
- duplicate certainty is high and merge target exists but create is attempted without reason

### Allow partial creation when
- company and title exist but source_url or compensation are missing

## 9.3 Recruiters Write Rule
### Required before create
- full_name or strong identity field
- role_type
- status
- created_at
- updated_at
- sync_status

### Block write when
- no usable identity exists

### Allow partial creation when
- recruiter has name but not email or LinkedIn

## 9.4 Communications Write Rule
### Required before create
- occurred_at
- channel
- direction
- summary
- status
- created_at
- updated_at
- sync_status

### Block write when
- no timestamp and no reliable source ref exist

### Allow partial creation when
- recruiter_id and job_id are unknown but event itself is real and summary is usable

## 9.5 Competition Write Rule
### Required before create
- person_name
- signal_type
- summary
- created_at
- updated_at
- sync_status

### Allow partial creation when
- company or role is unknown but signal is still operationally useful

## 10. Update Rules

## 10.1 General Update Rule
Update an existing record when identity match confidence is high.
Create new record when identity match is weak or record clearly represents a new event/entity.

## 10.2 Missing or Conflicting Data
- preserve non-conflicting existing values
- fill null fields with new known values
- if values conflict materially, prefer newer verified data and log note if needed
- do not silently replace strong identifiers without reason

## 10.3 Notes Behavior
- append operational notes rather than overwrite unless note is explicitly a replacement field
- avoid unbounded note sprawl; later normalization can split notes/history if needed

## 10.4 Timestamp Behavior
- `created_at` never changes after record creation
- `updated_at` changes on every successful write
- status-specific timestamps should update when status changes

## 11. Lookup Tables

## 11.1 Required Controlled Values
- job status values
- recruiter status values
- communication status values
- channels
- source types
- sync status values
- location types
- role types
- signal types

## 11.2 Why These Must Be Controlled
- prevent spelling drift
- simplify validation
- simplify filtering/reporting
- reduce agent write ambiguity
- preserve stable downstream logic

## 11.3 Agent Reference Rule
- agents should write lookup keys, not ad hoc human variants
- if raw input is messy, normalize before write
- if no valid lookup value exists, route to manual review or use a safe fallback value from lookup policy

## 12. Spreadsheet Structure Recommendation

## 12.1 Option A — One workbook, multiple tabs
### Tabs
- Jobs
- Recruiters
- Communications
- Competition
- Lookups
- optional dashboards

## 12.2 Option B — Separate files per entity
### Files
- jobs workbook
- recruiters workbook
- communications workbook
- competition workbook
- lookup workbook

## 12.3 Recommendation
**Recommend Option A: one workbook with multiple tabs** for the first implementation.

### Why
- easier for humans to navigate
- easier to keep controlled values centralized
- simpler for early agents and import flows
- lower coordination overhead
- better for cross-entity review in one place

### Later split rule
If volume, permissions, or performance complexity grows, entity-specific workbooks can be introduced later without changing the entity model.

## 13. Validation Rules

## 13.1 Valid Record
A record is valid when:
- required fields are present
- identity rule is satisfied
- controlled values resolve correctly
- timestamps are syntactically valid

## 13.2 Warning Conditions
Trigger warning when:
- partial record created
- link fields are unresolved
- duplicate confidence is medium but not high
- controlled value had to be normalized from messy input
- notes contain likely structured data that should later be split

## 13.3 Rejection Conditions
Reject write when:
- minimum identity cannot be established
- required fields are missing
- controlled values are invalid and cannot be normalized safely
- duplicate certainty is high but create-new is attempted without override rule

## 13.4 Incomplete Record Flagging
Incomplete records should be marked via:
- missing critical optional link fields
- null identity-adjacent fields
- warning state in import/review workflow
- later explicit `needs_review` support if required

## 14. Future Extensibility

## 14.1 Safe Field Addition
To add new fields safely:
- append new columns rather than repurpose old ones
- keep old column names stable
- define new field in entity spec before use
- provide default null-compatible behavior

## 14.2 Avoiding Breaking Changes
- do not rename columns casually
- do not overload a field with a new meaning
- do not mix raw and normalized values in the same field
- prefer new columns or new lookup groups over semantic mutation

## 14.3 Adding New Entities Later
Future entities can be added when:
- they have clear identity rules
- they are not merely notes disguised as data
- they improve operational clarity

Candidate future entities:
- companies as first-class structured records
- assets
- interviews
- referrals
- tasks/actions if spreadsheets later need operational support

## 15. Next Steps
1. `JT7_Jobs_Data_Spec.md` — detailed jobs spec and row-level write rules
2. `JT7_Recruiters_Data_Spec.md` — detailed recruiters spec and relationship rules
3. `JT7_Communications_Data_Spec.md` — detailed communications spec and event logic
4. `JT7_Telegram_Command_Model.md` — command grammar and write behavior for Telegram-triggered updates
5. `JT7_Competition_Data_Spec.md` — competition-specific interpretation and write rules
