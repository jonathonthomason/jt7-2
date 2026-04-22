# JT7 Recruiters Data Spec

## Document Metadata
- **System:** JT7 Job Intelligence System
- **Document type:** detailed entity data specification
- **Entity:** Recruiters / Contacts
- **Status:** draft-initial
- **Primary path:** `JT7/00_System/Data-Specs/JT7_Recruiters_Data_Spec.md`

## 1. Purpose and Role
> Consolidation note: this document describes a richer legacy Recruiters entity model. JT7's current consolidated MVP operating model now uses Google Sheets as the single operational source of truth and a shared cross-layer schema (`company`, `role`, `status`, `last_activity`, `next_step`, `contact`, `source`, `thread_id`, `notes`) with a stricter single status model. Until rewritten, treat this document as partially legacy and subordinate to the newer consolidated model.

The Recruiters tracker is the canonical structured record of recruiter and recruiter-adjacent contacts in JT7.

It is used to:
- track who has contacted Jonathon or been contacted
- maintain a stable contact identity separate from individual messages
- support follow-up and outreach decisions
- connect people to jobs and communications
- preserve relationship state over time across multiple channels and events

The Recruiters tracker supports decisions such as:
- who should be followed up with next
- which relationships are active, warm, cold, or dormant
- which recruiter is tied to which role or company
- whether a new communication updates an existing contact or creates a new one

Relationship to other entities:
- **Jobs:** recruiters may be linked to one or more jobs
- **Communications:** communications are events; recruiters are persistent contacts
- **Outreach workflows:** recruiter records are the durable surface used for follow-up, relationship tracking, and contact state

Why recruiter tracking must be distinct from communications logs:
- a recruiter is a person/entity relationship record
- a communication is a time-bound event
- one recruiter can have many communications
- outreach state should persist even if communications are noisy, incomplete, or distributed across channels

## 2. Canonical Schema

| Field Name | Type | Required | Description | Example | Notes |
|---|---|---:|---|---|---|
| recruiter_id | id | yes | canonical recruiter/contact id | `rec_jane_doe_figma` | generated; should not be casually edited |
| full_name | string | yes* | full contact name | `Jane Doe` | required unless strong alternate identity exists |
| first_name | string | no | first name | `Jane` | derived or manually entered |
| last_name | string | no | last name | `Doe` | derived or manually entered |
| company | string | no | current associated company | `Figma` | may be null for early partial record |
| role_title | string | no | recruiter/contact role title | `Senior Recruiter` | may later reflect hiring manager or referrer |
| contact_type | enum | yes | recruiter / hiring_manager / referrer / agency_recruiter / other | `recruiter` | controlled value |
| email | string | no | primary email | `jane@figma.com` | strongest identity if available |
| email_aliases | list[string] | no | additional known emails | `jane.doe@gmail.com` | useful for alias resolution |
| linkedin_url | string | no | LinkedIn profile URL | `https://linkedin.com/in/...` | strong fallback identity |
| phone | string | no | phone number | `+1-555-...` | optional |
| location | string | no | contact location if relevant | `San Francisco, CA` | optional |
| source_type | enum | yes | original source category | `email` | controlled value |
| source_detail | string | no | more specific origin detail | `gmail inbound recruiter outreach` | human-readable provenance |
| relationship_status | enum | yes | long-lived relationship state | `warm` | controlled value |
| outreach_status | enum | yes | current outreach/communication state | `contacted` | controlled value |
| linked_job_ids | list[id] | no | jobs associated with this contact | `job_figma_principal_product_designer_20260402|job_acme_staff_product_designer_20260410` | store IDs only |
| last_contacted_at | datetime | no | most recent outbound contact timestamp | `2026-04-02T16:30:00Z` | updates on outbound communication |
| last_response_at | datetime | no | most recent inbound response timestamp | `2026-04-02T17:10:00Z` | updates on inbound communication |
| next_followup_date | date | no | next follow-up target date | `2026-04-07` | operational field |
| notes | string | no | concise operational notes | `Reached out after portfolio review` | append-preserve behavior |
| sync_status | enum | yes | sync state of the record | `clean` | controlled value |
| created_at | datetime | yes | record creation timestamp | `2026-04-02T16:20:00Z` | immutable after creation |
| updated_at | datetime | yes | last record update timestamp | `2026-04-02T17:10:00Z` | updates on every successful write |

## 3. Identity Rules

## 3.1 Primary Uniqueness Logic
A recruiter/contact should be uniquely identified using the strongest available identity in this order:
1. `email`
2. `linkedin_url`
3. normalized `full_name + company`
4. normalized `full_name + role_title + source context` with manual review if weak

## 3.2 Fallback Matching Logic If Email Is Missing
If email is missing, attempt to match using:
- exact LinkedIn URL
- same normalized full name + same company
- same normalized full name + same role title + same source context

If confidence is high, update existing record.
If confidence is medium, flag for manual review.
If confidence is low, create new record.

## 3.3 recruiter_id Generation Rules
Recommended pattern:
- `rec_<normalized_name>_<normalized_company_or_identity_token>`

Preferred suffix priority:
1. company token if stable
2. email local-part token if company absent
3. linkedin token if email absent
4. fallback sequence only if needed

## 3.4 Create vs Update Rules
### Create new recruiter when
- no high-confidence identity match exists
- same name appears at clearly different companies and is likely a different contact context
- same person is operating in a materially separate role context requiring separate tracking only if system policy later supports it

### Update existing recruiter when
- email matches
- LinkedIn URL matches
- name + company strongly match
- communication clearly belongs to an existing recruiter record

## 3.5 Recruiter Changes Companies
Preferred rule:
- if identity is clearly the same person and core identifier (email personal / LinkedIn) remains stable, update the same recruiter record and update `company`
- append prior company context in notes if relevant
- if company-specific history becomes operationally important later, add historical fields or related records rather than creating silent duplicates

## 3.6 Multiple Roles / Contexts for Same Contact
- keep one canonical recruiter/contact record by default
- update `role_title` to the most relevant current role
- preserve prior context in notes if operationally important
- do not split into multiple contacts unless identity/context truly diverges

## 3.7 Tricky Identity Cases

### LinkedIn-only contact with no email
- allowed
- LinkedIn URL becomes strongest identity

### Same recruiter contacts from different email aliases
- treat as same recruiter if name/company and context match strongly
- preserve aliases in `email_aliases`

### Recruiter later revealed to be hiring manager
- update `contact_type`
- do not create new contact unless identity was previously wrong

### Agency recruiter vs internal recruiter
- distinguish via `contact_type`
- keep as separate records unless identity is clearly the same person

### Personal email instead of corporate email
- allow as primary email if that is the only strong identifier
- preserve company separately if known

## 4. Relationship and Outreach Status Models

## 4.1 Relationship Status Values
- `cold`
- `warm`
- `active`
- `dormant`
- `archived`

### Meaning
#### cold
- known contact, no meaningful engagement yet

#### warm
- some interaction or clear relevance exists, but not yet active ongoing engagement

#### active
- live conversation, active opportunity, or current meaningful recruiter relationship

#### dormant
- previously active/warm but currently inactive

#### archived
- no longer relevant as an active relationship, retained for history

### Allowed transitions
- cold → warm
- warm → active
- active → dormant
- dormant → warm
- any active state → archived when intentionally retired

### Invalid transitions
- cold → archived without reason if record is too new to judge
- archived → active without explicit reactivation update

### Auto-update guidance
- inbound recruiter contact may move cold → warm
- ongoing multi-message exchange or linked active job may move warm → active
- inactivity over chosen threshold may later move active → dormant

### Manual override
- always allowed when human context is stronger than automation

## 4.2 Outreach Status Values
- `not_contacted`
- `contacted`
- `replied`
- `scheduled`
- `closed_loop`
- `no_response`

### Meaning
#### not_contacted
- no outbound or meaningful tracked contact yet

#### contacted
- outbound message sent or first active contact made

#### replied
- contact responded

#### scheduled
- call, meeting, or next-step event is scheduled

#### closed_loop
- interaction cycle resolved or closed cleanly

#### no_response
- outreach sent, no response after reasonable interval

### Allowed transitions
- not_contacted → contacted
- contacted → replied
- contacted → no_response
- replied → scheduled
- replied → closed_loop
- scheduled → closed_loop
- no_response → replied if contact later responds

### Invalid transitions
- closed_loop → contacted without new outreach event
- not_contacted → scheduled without tracked contact path

### Auto-update guidance
- outbound communication can set `contacted`
- inbound reply can set `replied`
- calendar/interview coordination can set `scheduled`
- stale unanswered outreach can set `no_response`

### Manual override
- allowed when communications were off-system or when event interpretation needs correction

## 5. Required Fields for Record Creation

## 5.1 Minimum Required Fields
A recruiter/contact record must have:
- `recruiter_id`
- `contact_type`
- `source_type`
- `relationship_status`
- `outreach_status`
- `sync_status`
- `created_at`
- `updated_at`
- plus at least one usable identity field:
  - `full_name`
  - or `email`
  - or `linkedin_url`

## 5.2 Preferred Fields for High-Quality Record
- `full_name`
- `company`
- `role_title`
- `email`
- `linkedin_url`
- `linked_job_ids`
- `last_contacted_at`
- `last_response_at`
- `next_followup_date`

## 5.3 Partial Record Acceptance
Partial records are acceptable when:
- LinkedIn-only contact exists with no email
- recruiter is mentioned by name and company but no other identity exists yet
- inbound communication has enough identity value to preserve

## 5.4 Block Write When
- no usable identity exists
- `contact_type` missing
- `relationship_status` invalid
- `outreach_status` invalid
- duplicate certainty is high and create-new is attempted without override reason

## 5.5 Unknown Value Representation
Use null for unknown optional fields.
Do not invent placeholder emails, URLs, or phone numbers.

## 6. Update Rules

## 6.1 Safe-to-Overwrite Fields
Safe to overwrite with newer verified data:
- `company`
- `role_title`
- `location`
- `phone`
- `next_followup_date`
- `source_detail`

## 6.2 Preserve / History-Sensitive Fields
Preserve and append rather than casually overwrite:
- `notes`
- `email_aliases`
- prior company/context when relevant
- relationship context that explains status changes

## 6.3 linked_job_ids Handling
- store as IDs only
- append new job IDs if not already present
- do not duplicate IDs
- remove only if link was clearly erroneous

## 6.4 Notes Handling
- append concise operational notes
- do not replace useful historical context without reason
- avoid storing full communication transcripts here

## 6.5 last_contacted_at and last_response_at Behavior
- `last_contacted_at` updates on outbound contact
- `last_response_at` updates on inbound response
- do not clear older values unless correcting bad data

## 6.6 Status Change Handling
- update `relationship_status` only when relationship meaning changes
- update `outreach_status` when the communication cycle changes
- `updated_at` changes on any successful write

## 6.7 Agent Writes vs Manual Edits
- same validation rules for both
- agent writes should prefer normalized values and append-safe behavior
- manual edits may be tolerated with warnings if normalizable

## 7. Deduplication Rules

## 7.1 Primary Duplicate Detection
Check in this order:
1. exact `email`
2. exact `linkedin_url`
3. exact `email_aliases` match

## 7.2 Fallback Duplicate Detection
Use when primary identity is missing:
- normalized `full_name + company`
- normalized `full_name + role_title + source_detail`
- same person inferred across LinkedIn and email with matching name/company signals

## 7.3 Merge vs Manual Review
### Merge automatically when
- email matches exactly
- LinkedIn URL matches exactly
- email alias confidently resolves to same person

### Flag for manual review when
- same name but different company with weak context
- LinkedIn and email sources appear similar but not certain
- conflicting company associations exist without strong identity proof

## 7.4 Conflicting Emails / Names / Company Associations
- preserve strongest known identity field
- merge aliases when confidence is high
- do not overwrite `email` with weaker unverified email
- if company changes, update current `company` and preserve older context in notes if useful

## 7.5 LinkedIn vs Email Source Conflict
- if LinkedIn URL and email clearly refer to same person, merge into one canonical record
- if confidence is moderate only, hold for manual review before merge

## 8. Validation Rules

## 8.1 Hard Validation Failures
Reject write when:
- no usable identity field exists
- `contact_type` is missing or not in the controlled value set
- `relationship_status` is missing or not in the controlled value set
- `outreach_status` is missing or not in the controlled value set
- `sync_status` is missing or not in the controlled value set
- `created_at` is missing or invalid
- `updated_at` is missing or invalid
- `email` is present but not in valid email format
- `linkedin_url` is present but not in valid LinkedIn URL format

## 8.2 Soft Warnings
Warn when:
- company missing
- role_title missing
- both email and LinkedIn absent but only name present
- probable duplicate but not certain
- linked jobs absent for an active recruiter
- next follow-up date exists but no recent contact context exists
- `full_name` is present but cannot be cleanly split into first/last name if split fields are expected later
- personal email is used for a recruiter record without company confirmation

## 8.3 Incomplete-but-Allowed Records
Allowed when:
- name-only recruiter/contact from a warm lead
- LinkedIn-only contact
- company-known contact with no role title yet
- email-only contact with uncertain company but clear outreach relevance

## 8.4 Invalid Date / State Combinations
Warn or reject when:
- `last_response_at` is earlier than a more recent known inbound event being written
- `scheduled` outreach status exists with no prior contacted/replied path and no manual override note
- `no_response` is set while `last_response_at` is recent and no explanation exists
- `archived` relationship status exists with a future `next_followup_date` and no explicit preservation note
- `last_contacted_at` is later than `updated_at`
- `created_at` is later than `updated_at`

## 8.5 Format Constraints
### Email
- must be syntactically valid email format
- lowercase preferred for normalization
- no placeholder strings such as `unknown@unknown.com`

### LinkedIn URL
- should be a valid LinkedIn profile/company/contact URL when used for identity
- normalize tracking/query fragments away where practical
- non-LinkedIn URLs should not be written to `linkedin_url`

### Status values
- `contact_type`, `relationship_status`, `outreach_status`, `source_type`, and `sync_status` must resolve to controlled values only
- no freeform variants such as `Replied`, `reply`, `warm-ish`, or `emailed once`

### Dates and datetimes
- `next_followup_date` should be date-only
- `last_contacted_at`, `last_response_at`, `created_at`, and `updated_at` should be datetime fields
- all date values must be parseable and internally consistent

## 9. Spreadsheet Implementation Guidance

## 9.1 Recommended Column Order
1. recruiter_id
2. full_name
3. company
4. contact_type
5. relationship_status
6. outreach_status
7. email
8. email_aliases
9. linkedin_url
10. role_title
11. linked_job_ids
12. next_followup_date
13. last_contacted_at
14. last_response_at
15. source_type
16. source_detail
17. phone
18. location
19. notes
20. sync_status
21. created_at
22. updated_at
23. first_name
24. last_name

## 9.2 Controlled Value Columns
Use controlled values for:
- `contact_type`
- `source_type`
- `relationship_status`
- `outreach_status`
- `sync_status`

## 9.3 Columns That Should Not Be Casually Edited
- `recruiter_id`
- `created_at`
- `updated_at` except through controlled system update
- `email_aliases` without dedupe awareness
- `linked_job_ids` without understanding ID-based linking
- relationship/outreach statuses without understanding transition logic

## 9.4 linked_job_ids Representation
For V1 spreadsheet implementation:
- store `linked_job_ids` as multi-value text using a stable delimiter such as `|`
- values must be canonical job IDs only
- no job titles or company names in this field
- agents should parse and write this field deterministically

## 9.5 Human Readability Rules
- keep identity and status columns early in the sheet
- keep source and follow-up fields near status fields
- keep notes concise and operational
- avoid burying key decision fields behind rarely used metadata
- do not use notes as a substitute for fields that already exist

## 9.6 Agent Safety Rules
- canonical columns should be explicit, not formula-dependent
- helper views or reporting tabs can exist later, but not as source-of-truth columns
- agent writes should target canonical columns only

## 10. Integration Guidance

## 10.1 Telegram Commands
Telegram should be able to:
- create recruiter/contact record
- update relationship status
- update outreach status
- add notes
- set next follow-up date
- link recruiter to job ID

## 10.2 Email-Derived Contact Creation
Email-derived ingestion should:
- resolve recruiter by email first
- fall back to name + company if needed
- create partial recruiter record only when identity is strong enough to be operationally useful
- update `last_response_at` or `last_contacted_at` based on communication direction

## 10.3 Outreach Tracking
Recruiter records should support:
- who has been contacted
- who replied
- who needs follow-up
- who is dormant or closed

Outreach state should not require reading the full communication log every time.

## 10.4 Jobs Tracker Linking
- `linked_job_ids` should reference canonical job IDs from the Jobs tracker
- recruiter record may exist without linked jobs initially
- when a job becomes known later, update recruiter record rather than recreate it

## 10.5 Communications Tracker Linking
- communications should reference `recruiter_id`
- recruiter record should not duplicate communication-event detail
- recruiter state should summarize the relationship, not replicate the log

## 10.6 Drive / Local Sync Behavior
- canonical recruiter data lives in the Drive spreadsheet layer
- local mirror supports degraded mode and local access
- sync behavior must preserve canonical IDs, timestamps, and `sync_status`
- partial local writes should be reconcilable without losing recruiter identity continuity

## 11. Edge Cases

## 11.1 Recruiter with No Email
### Preferred handling
- allow creation if LinkedIn URL or strong name/company identity exists
- do not invent email

## 11.2 Vague Inbound Recruiter Message
### Preferred handling
- create recruiter record only if the sender identity is stable enough
- do not create job linkage unless role context is sufficiently clear
- if message is too vague, preserve in communications/manual review first

## 11.3 Same Person Changes Company
### Preferred handling
- keep same recruiter record if identity is clearly the same person
- update `company`
- preserve prior company context in notes if operationally relevant

## 11.4 Multiple Recruiters at Same Company
### Preferred handling
- separate recruiter records
- company alone is never sufficient to merge people

## 11.5 Same Recruiter Tied to Multiple Jobs
### Preferred handling
- one recruiter record
- append multiple canonical job IDs in `linked_job_ids`

## 11.6 Recruiter vs Hiring Manager Ambiguity
### Preferred handling
- use best current `contact_type`
- if ambiguous, start with `other` or recruiter-adjacent safe value per lookup policy
- update later when identity context becomes clear

## 11.7 Duplicate Name Across Companies
### Preferred handling
- assume separate records unless strong identity proves same person

## 11.8 Internal Referral Contact Who Is Not a Recruiter
### Preferred handling
- create record with `contact_type = referrer`
- keep in same tracker because relationship/outreach handling still applies
- do not force recruiter classification

## 12. Recommended V1 Recruiters Schema

## 12.1 Must-Have Columns for V1
- recruiter_id
- full_name
- company
- contact_type
- email
- linkedin_url
- source_type
- relationship_status
- outreach_status
- linked_job_ids
- last_contacted_at
- last_response_at
- next_followup_date
- notes
- sync_status
- created_at
- updated_at

## 12.2 Nice-to-Have Columns for Later
- first_name
- last_name
- email_aliases
- phone
- location
- source_detail
- role_title

## 13. Dependencies and Next Document
This spec depends on:
- `JT7_System_Architecture.md`
- `JT7_Artifact_Inventory_and_Folder_Map.md`
- `JT7_Structured_Data_Master_Plan.md`
- `JT7_Jobs_Data_Spec.md`

Recommended next document:
- `JT7_Communications_Data_Spec.md`
