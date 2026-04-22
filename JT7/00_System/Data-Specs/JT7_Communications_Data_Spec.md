# JT7 Communications Data Spec

## Document Metadata
- **System:** JT7 Job Intelligence System
- **Document type:** detailed entity data specification
- **Entity:** Communications
- **Status:** draft-initial
- **Primary path:** `JT7/00_System/Data-Specs/JT7_Communications_Data_Spec.md`

## 1. Purpose and Role
> Consolidation note: this document describes a richer legacy Communications entity model. JT7's current consolidated MVP operating model still treats communications as append-first evidence, but the governing shared schema and final job-status model now live above this richer spec. Until rewritten, treat this document as partially legacy and subordinate to the newer consolidated model.

The Communications tracker is the canonical record of meaningful interaction events in JT7.

It exists to:
- log every meaningful recruiter, hiring, referral, or outreach interaction
- preserve a clear interaction timeline
- link interaction events to recruiter records and jobs
- support follow-up logic and response tracking
- provide an auditable history of what happened, when, and through which channel

Why Communications must be a separate entity:
- recruiter records are durable relationship records
- job records are durable opportunity records
- communications are time-bound events
- one recruiter may have many communications
- one job may be affected by many communications
- timeline truth should not be buried in notes fields on Jobs or Recruiters

How it differs from recruiter notes:
- notes summarize durable contact state or context
- communications log specific events
- notes are relationship-level
- communications are event-level

How it supports decision-making and follow-ups:
- identifies who is awaiting response
- shows what follow-up is due
- captures whether interaction tone/outcome is positive or negative
- supports recruiter and job state updates from concrete evidence

How it acts as the timeline of truth:
- each event is its own record
- records are timestamped
- events can be linked to recruiter and job entities
- duplicate or ambiguous ingestion can be resolved against this event log

## 2. Canonical Schema

| Field Name | Type | Required | Description | Example |
|---|---|---:|---|---|
| comm_id | id | yes | canonical communication record id | `com_20260402_jane_email_01` |
| recruiter_id | id | yes* | linked recruiter/contact id | `rec_jane_doe_figma` |
| job_id | id | no | linked job id | `job_figma_principal_product_designer_20260402` |
| channel | enum | yes | communication channel | `email` |
| direction | enum | yes | inbound or outbound | `inbound` |
| subject_or_topic | string | no | short subject or topic | `Principal design role intro` |
| summary | string | yes | concise event summary | `Recruiter reached out about principal product designer role` |
| raw_excerpt | string | no | short raw excerpt or snippet | `Hi Jonathon, I came across your profile...` |
| full_text_reference | string | no | pointer to stored full-text source | `drive://03_Research/External_Snapshots/msg_abc123.md` |
| status | enum | yes | communication lifecycle state | `pending_response` |
| outcome | enum | yes | event tone/result | `positive` |
| action_required | enum | yes | next action category | `follow_up` |
| next_followup_date | date | no | next follow-up target date | `2026-04-05` |
| response_expected | boolean | yes | whether a reply is expected | `true` |
| source_type | enum | yes | creation/source mode | `email_parse` |
| source_ref | string | no | external reference id | `gmail_msg_abc123` |
| thread_ref | string | no | external thread/conversation reference | `gmail_thread_xyz789` |
| date_sent | datetime | no | outbound send time | `2026-04-02T15:05:00Z` |
| date_received | datetime | no | inbound received time | `2026-04-02T15:06:00Z` |
| notes | string | no | operational notes | `Needs reply with portfolio link` |
| sync_status | enum | yes | sync state of the record | `clean` |
| created_at | datetime | yes | creation timestamp | `2026-04-02T15:06:30Z` |
| updated_at | datetime | yes | last update timestamp | `2026-04-02T15:10:00Z` |

## 3. Identity Rules

## 3.1 ID Generation Rules
Recommended pattern:
- `com_<yyyymmdd>_<normalized_contact_or_unknown>_<channel>_<sequence>`

Examples:
- `com_20260402_jane_email_01`
- `com_20260402_unknown_linkedin_01`

## 3.2 Canonical Uniqueness Logic
Strongest uniqueness signals in order:
1. `source_ref`
2. `channel + thread_ref + source_ref`
3. `recruiter_id + direction + channel + date_sent/date_received`
4. `summary + recruiter_id + near-identical timestamp` with manual review if weak

## 3.3 Duplicate Avoidance for Email Parsing
Email parsing should:
- prefer `source_ref` as primary message identity
- preserve `thread_ref` as a grouping field
- treat the same message parsed twice as update/ignore, not create-new

## 3.4 Threads vs Messages
- canonical communication record should represent a meaningful message/event, not a whole thread summary by default
- thread linkage belongs in `thread_ref`
- future derived views may summarize threads, but canonical log should preserve event granularity

## 3.5 Repeated Messages
- multiple messages in one day are separate records if they are distinct events
- do not collapse them just because they share recruiter, channel, or date

## 4. Relationship Rules

## 4.1 recruiter_id Requirement
- `recruiter_id` is required whenever identity can be resolved
- for true unknown-contact cases, temporary unresolved communication staging may be allowed before final canonical creation
- canonical Communications records should prefer resolved recruiter linkage

## 4.2 job_id Rule
- `job_id` is optional but preferred
- use when the communication clearly relates to a known job
- leave null if job relationship is unknown or ambiguous

## 4.3 Missing Links at Creation Time
### Missing recruiter_id
- if contact identity is too weak, hold in review/staging rather than writing incomplete canonical record
- if a meaningful event exists and contact can be resolved shortly, temporary null may be tolerated only if system policy explicitly allows staged rows

### Missing job_id
- allowed
- backfill later when role context becomes clear

## 4.4 Resolving Links Later
- if recruiter becomes known later, update `recruiter_id`
- if job becomes known later, update `job_id`
- preserve timestamps and original event identity during link updates

## 4.5 Influence on Recruiter and Job States
Communications may update:
- Recruiter `last_contacted_at`
- Recruiter `last_response_at`
- Recruiter `outreach_status`
- Recruiter `relationship_status` in some cases
- Job `status` when communication clearly indicates apply/interview/reject/offer state
- Job `followup_date` or operational note when relevant

## 5. Status and Outcome Model

## 5.1 Communication Status Values
- `logged`
- `pending_response`
- `responded`
- `closed`
- `no_response`

### Meaning
#### logged
- event recorded, no further communication state interpretation applied yet

#### pending_response
- the event requires or expects a reply

#### responded
- a response to the relevant outreach/event has occurred

#### closed
- the communication loop is complete

#### no_response
- reasonable follow-up window passed without reply

### Allowed Transitions
- logged → pending_response
- logged → closed
- pending_response → responded
- pending_response → no_response
- responded → closed
- no_response → responded if reply later arrives

### Auto-update vs Manual
- agent/email parsing may set `logged`, `pending_response`, or `responded` when evidence is strong
- `closed` and `no_response` may be rule-assisted but should allow manual override

## 5.2 Outcome Values
- `positive`
- `neutral`
- `negative`
- `unknown`

### Meaning
#### positive
- message advances opportunity or relationship positively

#### neutral
- message is informational or non-directional

#### negative
- message closes or damages the opportunity path

#### unknown
- tone/result not yet clear

### Auto-update vs Manual
- default to `unknown` or `neutral` if interpretation is uncertain
- only set `negative` automatically when evidence is explicit, such as rejection

## 5.3 Action Required Values
- `none`
- `follow_up`
- `schedule_call`
- `send_material`
- `apply`
- `other`

### Meaning
#### none
- no action required from this event

#### follow_up
- reply or follow-up should occur

#### schedule_call
- scheduling action required

#### send_material
- send resume, portfolio, availability, or similar

#### apply
- communication indicates application should be submitted

#### other
- required action does not fit existing categories

### Auto-update vs Manual
- may be inferred from explicit request language in email parsing
- should remain manually adjustable

## 6. Required Fields for Record Creation

## 6.1 Minimum Required Fields
A communication record must have:
- `comm_id`
- `channel`
- `direction`
- `summary`
- `status`
- `outcome`
- `action_required`
- `response_expected`
- `source_type`
- `sync_status`
- `created_at`
- `updated_at`
- plus either:
  - `recruiter_id`
  - or an approved temporary staging process outside canonical sheet

## 6.2 Recommended Fields
- `recruiter_id`
- `job_id`
- `subject_or_topic`
- `raw_excerpt`
- `source_ref`
- `thread_ref`
- `date_sent` or `date_received`
- `next_followup_date`

## 6.3 Partial Entries
Partial canonical entries are acceptable when:
- recruiter is known
- job is unknown
- message summary is still useful
- a real interaction occurred and must be logged

## 6.4 Block Logging When
- no meaningful event exists
- summary is empty
- direction is unknown
- channel is unknown
- recruiter identity cannot be resolved and no staging layer is being used

## 6.5 Unknown Value Handling
- use null for unknown optional fields
- do not invent timestamps, thread ids, or message refs
- use `unknown` only for controlled outcome/state categories where appropriate, not for identifiers

## 7. Update Rules

## 7.1 Safe Update Behavior
Safe to overwrite with newer verified data:
- `job_id`
- `subject_or_topic`
- `raw_excerpt`
- `full_text_reference`
- `status`
- `outcome`
- `action_required`
- `next_followup_date`
- `thread_ref`

## 7.2 Summary vs Raw Excerpt
- `summary` should remain a concise normalized explanation of the event
- `raw_excerpt` should preserve source-like wording when useful
- do not replace good summary with noisy raw text

## 7.3 Notes Handling
- append concise operational notes
- avoid duplicating summary or raw excerpt unnecessarily

## 7.4 Timestamp Behavior
- `created_at` never changes
- `updated_at` changes on any successful write
- `date_sent` should be used for outbound messages
- `date_received` should be used for inbound messages
- if both are relevant for a transformed/imported event, preserve only the source-valid one unless protocol expands later

## 7.5 Follow-Up Date Updates
- update `next_followup_date` whenever follow-up logic changes
- clear it when communication loop is clearly closed and no follow-up is required

## 7.6 Status Changes Over Time
- `logged` may become `pending_response`
- `pending_response` may become `responded` or `no_response`
- `responded` may become `closed`
- later inbound reply may move `no_response` → `responded`

## 8. Deduplication Rules

## 8.1 Duplicate Detection Logic
Check in this order:
1. exact `source_ref`
2. exact `channel + source_ref`
3. exact `thread_ref + near-identical timestamp + same recruiter_id`
4. same recruiter + same channel + same direction + same timestamp window + same summary

## 8.2 Email Parsing Duplication
- the same parsed email should never create multiple communication records if `source_ref` matches
- repeated ingestion should update or skip, not duplicate

## 8.3 Thread vs Individual Message Handling
- each meaningful message = one communication record
- thread summary should not replace per-message event logging
- if a thread summary artifact exists later, it belongs in derived/reporting logic, not canonical event rows

## 8.4 Merge vs Flag Rules
### Merge / skip duplicate when
- source_ref is identical
- timestamp/channel/recruiter match with near-certain equivalence

### Flag for review when
- same-day messages are very similar but not clearly the same
- one source provides only thread-level reference and another provides message-level reference

## 9. Validation Rules

## 9.1 Required Relationships
- `recruiter_id` should exist for canonical record creation unless staged externally first
- `job_id` is optional but preferred when clear

## 9.2 Valid Direction + Timestamp Logic
- inbound communications should normally have `date_received`
- outbound communications should normally have `date_sent`
- missing both should warn or reject depending on source quality
- inbound record with only `date_sent` should warn unless justified by source transformation
- outbound record with only `date_received` should warn unless justified by source transformation

## 9.3 Valid Channel Values
Allowed channels should come from controlled values such as:
- `email`
- `linkedin`
- `call`
- `in_person`
- `text`
- `other`

No freeform channel values should be written into canonical records.

## 9.4 Date Logic
- `next_followup_date` should not precede the communication event date without explicit reason
- `created_at` should not be later than `updated_at`
- event timestamps should be parseable datetimes

## 9.5 Acceptable Incomplete Records
Allowed when:
- job_id unknown
- raw excerpt absent
- full text reference absent
- subject/topic absent but summary is strong

Not acceptable when:
- no recruiter link and no staging policy
- no summary
- no direction
- no channel

## 10. Spreadsheet Implementation Guidance

## 10.1 Recommended Column Order
1. comm_id
2. recruiter_id
3. job_id
4. channel
5. direction
6. status
7. outcome
8. action_required
9. response_expected
10. next_followup_date
11. subject_or_topic
12. summary
13. raw_excerpt
14. full_text_reference
15. source_type
16. source_ref
17. thread_ref
18. date_sent
19. date_received
20. notes
21. sync_status
22. created_at
23. updated_at

## 10.2 Controlled Value Columns
Use controlled values for:
- `channel`
- `direction`
- `status`
- `outcome`
- `action_required`
- `source_type`
- `sync_status`

## 10.3 Readability Rules
- keep routing and state fields early in the sheet
- keep summary visible before raw excerpt
- keep long text fields late in the sheet
- preserve one-row-per-event readability

## 10.4 Long Text Handling
- `summary` should stay short enough for normal spreadsheet reading
- `raw_excerpt` should be short and optional
- long-form content should move to `full_text_reference`, not live in the main row
- multi-line summaries should be avoided where possible; use concise normalized text instead

## 11. Integration Guidance

## 11.1 Telegram
Telegram should support:
- log manual communication
- log call
- log follow-up
- update communication status
- set follow-up date

## 11.2 Email Parsing
Email parsing should:
- create communication entries from meaningful messages
- set recruiter link where possible
- set job link when role context is clear
- use `source_ref` and `thread_ref` to reduce duplicates

## 11.3 Recruiter Status Updates
Communications may update recruiter records:
- inbound response → `last_response_at`
- outbound contact → `last_contacted_at`
- communication state may influence recruiter `outreach_status`
- relationship state may change when active conversation emerges

## 11.4 Job Status Updates
Communications may update jobs when message evidence is clear:
- interview scheduling → `interviewing`
- rejection → `rejected`
- apply prompt or confirmation → `applied`

## 11.5 Follow-Up Systems
- `action_required` and `next_followup_date` should feed follow-up views or task generation later
- communications are the event truth behind follow-up logic

## 11.6 Drive / Local Sync
- canonical communications data lives in Drive spreadsheet layer
- local mirror supports degraded mode and local access
- sync should preserve IDs, timestamps, refs, and statuses consistently

## 12. Edge Cases

## 12.1 Email Thread vs Individual Messages
### Handling rule
- log individual meaningful messages as separate communication records
- preserve `thread_ref` for grouping

## 12.2 Recruiter Sends Multiple Messages in a Day
### Handling rule
- each meaningful message is its own record
- do not collapse by date alone

## 12.3 Vague Outreach Messages
### Handling rule
- if recruiter identity is known, log event with summary and unknown job link
- if recruiter identity is not strong enough, hold for review/staging

## 12.4 Call With No Written Record
### Handling rule
- allow manual communication record
- channel = call
- summary required
- source_type = manual

## 12.5 Missed Calls
### Handling rule
- log as communication if operationally relevant
- set action_required if callback/follow-up is needed

## 12.6 Follow-Up Without Response
### Handling rule
- status may move to `no_response`
- preserve next follow-up if another attempt is planned

## 12.7 Recruiter Ghosting
### Handling rule
- do not create new communication unless a new attempt occurs
- existing pending communication may move to `no_response`

## 12.8 Multi-Recipient Emails
### Handling rule
- if one primary recruiter/contact is operationally central, use that recruiter_id
- if multiple distinct contacts matter, log separate communication rows only when needed for contact-specific tracking

## 12.9 Same Message Parsed Twice
### Handling rule
- resolve by `source_ref`
- update/skip, never duplicate

## 13. Recommended V1 Communications Schema

## 13.1 Must-Have Fields
- comm_id
- recruiter_id
- channel
- direction
- summary
- status
- outcome
- action_required
- response_expected
- source_type
- sync_status
- created_at
- updated_at

## 13.2 Optional Fields for Later
- job_id
- subject_or_topic
- raw_excerpt
- full_text_reference
- next_followup_date
- source_ref
- thread_ref
- date_sent
- date_received
- notes

## 14. Dependencies and Next Document
This spec depends on:
- `JT7_System_Architecture.md`
- `JT7_Artifact_Inventory_and_Folder_Map.md`
- `JT7_Structured_Data_Master_Plan.md`
- `JT7_Jobs_Data_Spec.md`
- `JT7_Recruiters_Data_Spec.md`

Recommended next document:
- `JT7_Competition_Data_Spec.md`
