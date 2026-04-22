# JT7 Jobs Data Spec

## Document Metadata
- **System:** JT7 Job Intelligence System
- **Document type:** detailed entity data specification
- **Entity:** Jobs
- **Status:** draft-initial
- **Primary path:** `JT7/00_System/Data-Specs/JT7_Jobs_Data_Spec.md`

## 1. Purpose and Role
> Consolidation note: this document describes a richer legacy Jobs entity model. JT7's current consolidated MVP operating model now uses Google Sheets as the single operational source of truth and a shared cross-layer schema (`company`, `role`, `status`, `last_activity`, `next_step`, `contact`, `source`, `thread_id`, `notes`) with the final status model (`Applied`, `Recruiter Contacted`, `Screening`, `Interviewing`, `Offer`, `Rejected`, `Cold`). Until rewritten, treat this document as partially legacy and subordinate to the newer consolidated model.

The Jobs tracker is the canonical structured record of job opportunities in JT7.

It is used to:
- track opportunities from lead through archive
- support prioritization and follow-up decisions
- connect jobs to recruiters and communications
- preserve a stable opportunity record across multiple sources
- support agent writes, Telegram-triggered updates, and future ingestion workflows

The Jobs tracker supports decisions such as:
- which roles should be prioritized
- which opportunities need follow-up
- which applications are active, stalled, rejected, or closed
- which jobs are duplicates or variants of the same opportunity

Relationship to other entities:
- **Recruiters:** one or more recruiters may be linked to a job
- **Communications:** communications may reference a job directly
- **External sources:** job boards, company sites, emails, referrals, and manual inputs may all create or update job records

## 2. Canonical Schema

| Field Name | Type | Required | Description | Example | Notes |
|---|---|---:|---|---|---|
| job_id | id | yes | canonical unique job record id | `job_figma_principal_product_designer_20260402` | generated; should not be casually edited |
| title | string | yes | role title | `Principal Product Designer` | normalized human-readable title |
| company | string | yes | company name | `Figma` | normalized display name |
| location | string | no | raw or human-readable location | `Remote (US)` | may come from job post or recruiter note |
| location_type | enum | no | normalized location type | `remote` | controlled value |
| source_type | enum | yes | source category | `job_board` | controlled value |
| source_platform | enum | no | platform name | `linkedin` | controlled value |
| posting_url | string | no | canonical posting URL | `https://...` | strongest external identity field when stable |
| direct_apply_url | string | no | URL used to apply directly | `https://company.com/careers/...` | may differ from posting URL |
| company_careers_url | string | no | company careers root URL | `https://company.com/careers` | optional convenience field |
| recruiter_id | id | no | primary recruiter/contact id | `rec_jane_doe_linkedin` | for V1, single primary recruiter; many-to-many can be added later |
| status | enum | yes | current job lifecycle state | `saved` | controlled value |
| fit_score | number | no | normalized fit score | `8` | recommended range 1–10 |
| salary_min | number | no | minimum numeric salary if parseable | `220000` | currency assumed by system policy if not expanded later |
| salary_max | number | no | maximum numeric salary if parseable | `260000` | optional |
| salary_raw | string | no | raw compensation text | `$220k-$260k + equity` | preserve source wording |
| posted_date | date | no | date job was posted if known | `2026-03-29` | can be null |
| date_found | date | yes | date job entered JT7 awareness | `2026-04-02` | required for operational tracking |
| date_applied | date | no | date application submitted | `2026-04-03` | required if status is applied or beyond |
| last_status_change | datetime | yes | timestamp of most recent status change | `2026-04-03T10:15:00Z` | must update on status change |
| followup_date | date | no | date next follow-up is due | `2026-04-10` | used for follow-up tracking |
| source_ref | string | no | external source reference id | `linkedin_job_12345` | helpful for dedupe |
| fit_notes | string | no | concise rationale for fit score | `Strong systems leadership fit` | short, operational |
| notes | string | no | operational notes | `Need tailored resume before applying` | append-preserve behavior |
| sync_status | enum | yes | sync state of the record | `clean` | controlled value |
| created_at | datetime | yes | creation timestamp | `2026-04-02T09:15:00Z` | immutable after creation |
| updated_at | datetime | yes | most recent update timestamp | `2026-04-03T10:15:00Z` | update on every successful write |

## 3. Identity Rules

## 3.1 Canonical Uniqueness Logic
A Job should be uniquely identified using the strongest available identity in this order:
1. `posting_url`
2. `source_ref`
3. normalized `company + title + location`
4. normalized `company + title` with manual review if ambiguity exists

## 3.2 Fallback Matching Logic When URL Is Missing
If `posting_url` is missing, attempt to match using:
- same company
- same normalized title
- same location or location_type if available
- similar source timing and notes context

If confidence is high, update existing record.
If confidence is medium, flag for review.
If confidence is low, create new record.

## 3.3 job_id Generation Rules
Recommended pattern:
- `job_<normalized_company>_<normalized_title>_<yyyymmdd>`

Where:
- company and title are normalized to lowercase underscore-separated tokens
- date component should reflect `date_found` for initial creation

If collision occurs:
- add short disambiguator such as location token or sequence suffix

## 3.4 Create vs Update Rules
### Create new job when
- no high-confidence match exists
- source clearly represents a distinct role
- same company/title but different location materially changes the opportunity
- same role is clearly a new later posting and should be tracked distinctly

### Update existing job when
- posting URL or source_ref matches existing record
- recruiter email clearly refers to an already tracked job
- same company/title/location and no evidence it is a distinct opening

## 3.5 Tricky Identity Cases

### Reposted jobs
- if same role is clearly reposted and materially the same opportunity, update existing record and note reposting
- if role was closed and later reopened as a materially new listing, create new record and link via notes or future related_job field

### Same role on multiple sites
- use one canonical job record
- preserve strongest posting URL in `posting_url`
- store alternate references in notes or future supplemental fields

### Updated posting URLs
- update `posting_url` if new URL is clearly the same job and more canonical
- preserve old URL in notes if operationally useful

### Referral-only leads with no URL yet
- partial job record is acceptable if company and title are known enough to be actionable
- set `source_type = referral`
- keep `posting_url = null`

## 4. Status Model

## 4.1 Status Values
- `lead`
- `saved`
- `applied`
- `interviewing`
- `offer`
- `rejected`
- `archived`

## 4.2 Status Definitions

### lead
- **Meaning:** role exists as a potential opportunity but is not yet reviewed enough for active pipeline inclusion
- **Use when:** recruiter mentions a role vaguely, referral lead exists, or imported role is not yet reviewed
- **Set manually/automatically:** both

### saved
- **Meaning:** role is intentionally tracked and worth further action, but no application submitted yet
- **Use when:** role has been reviewed and retained
- **Set manually/automatically:** both

### applied
- **Meaning:** application submitted
- **Use when:** direct apply, referral submission, or company application is completed
- **Set manually/automatically:** both

### interviewing
- **Meaning:** any active interview process exists
- **Use when:** recruiter screen, hiring manager screen, panel, or assessment is active
- **Set manually/automatically:** both

### offer
- **Meaning:** offer extended or clearly imminent enough to treat as offer stage
- **Use when:** formal offer exists
- **Set manually/automatically:** generally manual or confirmed signal

### rejected
- **Meaning:** opportunity is closed unsuccessfully
- **Use when:** explicit rejection or confirmed closure occurs
- **Set manually/automatically:** both if evidence is strong

### archived
- **Meaning:** record retained for history but not active
- **Use when:** stale role, obsolete lead, old offer, or long-closed role should remain out of active views
- **Set manually/automatically:** generally manual, sometimes rule-driven later

## 4.3 Allowed Transitions
- lead → saved
- lead → archived
- saved → applied
- saved → archived
- applied → interviewing
- applied → rejected
- interviewing → offer
- interviewing → rejected
- offer → archived
- rejected → archived

## 4.4 Invalid Transitions
- archived → interviewing without explicit reopen rule
- rejected → interviewing without evidence of reactivation
- offer → applied
- lead → offer

## 4.5 Auto-Update Guidance
- recruiter/interview scheduling email may set `interviewing`
- application confirmation may set `applied`
- explicit rejection email may set `rejected`
- no auto-update should occur when ambiguity is high

## 5. Required Fields for Record Creation

## 5.1 Minimum Required Fields
A new job record must have:
- `job_id`
- `title`
- `company`
- `source_type`
- `status`
- `date_found`
- `last_status_change`
- `sync_status`
- `created_at`
- `updated_at`

## 5.2 Recommended Fields for High-Quality Record
- `posting_url`
- `source_platform`
- `location`
- `location_type`
- `fit_score`
- `fit_notes`
- `followup_date`
- `recruiter_id`
- `salary_raw`

## 5.3 Fields That Can Be Backfilled Later
- `posting_url`
- `direct_apply_url`
- `company_careers_url`
- `recruiter_id`
- `salary_min`
- `salary_max`
- `salary_raw`
- `posted_date`
- `date_applied`
- `fit_score`
- `fit_notes`
- `followup_date`

## 5.4 Block Write When
- `title` missing
- `company` missing
- `source_type` missing
- duplicate certainty is high and create-new is attempted without override reason
- status is invalid

## 5.5 Partial Record Acceptance
Partial job creation is acceptable when:
- title and company are known
- job is operationally actionable
- missing fields can reasonably be backfilled later

Typical acceptable partial cases:
- recruiter mention with no URL yet
- manual lead from a referral
- imported job list row with sparse metadata but clear job identity

## 6. Update Rules

## 6.1 Safe-to-Overwrite Fields
Safe to overwrite when newer verified data arrives:
- `location`
- `location_type`
- `direct_apply_url`
- `company_careers_url`
- `fit_score`
- `salary_min`
- `salary_max`
- `salary_raw`
- `followup_date`
- `fit_notes`

## 6.2 Preserve / Append Fields
These should preserve history or append rather than blindly replace:
- `notes`
- URL changes if old URL may still matter
- status history context

## 6.3 Notes Handling
- append short new notes rather than replacing useful existing notes
- avoid long diary-style notes in the tracker cell if possible
- prefer concise operational notes

## 6.4 Timestamp Updates
- `created_at` never changes
- `updated_at` updates on every write
- `last_status_change` updates only when `status` changes
- `date_applied` should be set when status first becomes `applied`

## 6.5 Status Change Logging
At minimum for V1:
- update `last_status_change`
- append reason/context to `notes` if needed

Later enhancements may add explicit status history tables, but not required for V1.

## 6.6 Agent vs Manual Edits
- same data rules should apply to both
- agent writes should be stricter about controlled values and timestamps
- manual edits may be tolerated with warnings if normalization is still possible

## 7. Deduplication Rules

## 7.1 Primary Duplicate Detection
Check in this order:
1. exact `posting_url`
2. exact `source_ref`
3. normalized `company + title + location`

## 7.2 Secondary Duplicate Detection
Use when primary keys are missing:
- normalized `company + title`
- similar `date_found`
- same recruiter and same role mention
- same source platform + very similar URL path

## 7.3 Duplicate Handling
### High confidence duplicate
- update existing record
- do not create new one

### Medium confidence duplicate
- flag for manual review
- allow temporary staging if needed, but do not silently merge

### Low confidence duplicate
- create new record

## 7.4 Merge Rules
When merge is appropriate:
- preserve existing `job_id`
- keep earliest `created_at`
- keep latest `updated_at`
- preserve richer structured values
- append notes rather than losing context

## 7.5 Conflicting Value Handling
If conflicting values arrive across sources:
- prefer newer verified value
- preserve raw conflicting evidence in notes if important
- do not overwrite strong identity fields casually

## 8. Validation Rules

## 8.1 Hard Validation Failures
Reject record when:
- `title` missing
- `company` missing
- `status` invalid
- `source_type` invalid
- `date_found` missing
- `created_at` or `updated_at` missing

## 8.2 Soft Warnings
Warn when:
- URL missing
- recruiter unknown
- salary unknown
- fit score absent
- source platform absent though source_type is job_board
- likely duplicate but not certain

## 8.3 Incomplete-but-Allowed Records
Allowed when:
- recruiter lead has no URL yet
- salary/location missing
- fit evaluation not done yet
- source reference missing but role identity is still strong enough

## 8.4 Invalid Date / State Combinations
Examples of invalid or warning-worthy combinations:
- `date_applied` present while status is `lead` or `saved`
- `followup_date` earlier than `date_found` without explicit note
- `posted_date` after `date_found` may warn if inconsistent
- `offer` with no prior applied/interviewing state should warn

## 8.5 Invalid URL / Source Combinations
Warn or reject when:
- `posting_url` exists but `source_type` is clearly inconsistent
- `source_platform = linkedin` but URL is non-LinkedIn and not a copied redirect note
- `source_type = referral` with fabricated job board source platform

## 9. Spreadsheet Implementation Guidance

## 9.1 Recommended Column Order
1. job_id
2. status
3. company
4. title
5. recruiter_id
6. source_type
7. source_platform
8. posting_url
9. direct_apply_url
10. company_careers_url
11. location
12. location_type
13. fit_score
14. fit_notes
15. salary_min
16. salary_max
17. salary_raw
18. posted_date
19. date_found
20. date_applied
21. last_status_change
22. followup_date
23. notes
24. sync_status
25. created_at
26. updated_at
27. source_ref

## 9.2 Frozen Columns
Recommended freeze:
- `job_id`
- `status`
- `company`
- `title`

These are the highest-value orientation columns.

## 9.3 Controlled Value Columns
Use controlled values for:
- `status`
- `source_type`
- `source_platform`
- `location_type`
- `sync_status`

## 9.4 Columns That Should Not Be Casually Edited
- `job_id`
- `created_at`
- `last_status_change` (except through controlled update)
- `sync_status` unless operating mode requires it

## 9.5 Formulas / Derived Columns
For V1:
- avoid heavy formula dependence in canonical columns
- lightweight helper columns are acceptable later, but core data should remain explicit
- canonical fields should be directly readable by agents without relying on spreadsheet-only logic

## 9.6 Human Readability Rules
- keep key orientation fields early in the sheet
- keep raw URLs and source references grouped
- keep notes concise
- do not overload notes with structured data that should have its own field

## 10. Integration Guidance

## 10.1 Telegram Commands
Telegram should be able to:
- create a job lead
- update job status
- add notes
- set next follow-up
- link recruiter if known

Telegram-triggered updates should respect the same validation and dedupe rules.

## 10.2 Recruiter Linking
- `recruiter_id` should point to the Recruiters tracker
- if recruiter is unknown, job can be created unlinked
- later linking should update the record rather than recreate it

## 10.3 Communications Linking
- communications should reference `job_id`
- the job may store the most recent communication indirectly or later through a derived view
- do not store redundant communication summaries if the Communication entity exists

## 10.4 Email-Derived Updates
Email may:
- create a lead
- update status to applied/interviewing/rejected
- add or update recruiter linkage
- set follow-up date

## 10.5 Job Board Ingestion
Job board ingestion should:
- normalize platform/source fields
- use URL/source reference for dedupe
- prefer update over create when duplicate confidence is high

## 10.6 Drive / Local Sync Behavior
- Drive holds canonical spreadsheet state when online
- local mirror is fallback and local working copy
- sync status should indicate whether record is clean or pending
- no local/runtime-only edits should remain unpromoted indefinitely

## 11. Edge Cases

## 11.1 No URL Job Lead
### Handling rule
- allow creation if title and company are known
- set `source_type = referral` or other appropriate value
- keep `posting_url = null`

## 11.2 Recruiter Mentions Role Vaguely
### Handling rule
- create `lead` only if role/company are specific enough to be useful
- otherwise store in recruiter/communication layer first and wait for stronger identity

## 11.3 Multiple Recruiters Tied to Same Role
### Handling rule
- V1: keep one primary `recruiter_id` in Jobs
- preserve additional recruiter linkage through Recruiters/Communications until many-to-many support is expanded

## 11.4 Role Closed and Reposted
### Handling rule
- if clearly a new posting cycle, create new job record
- note linkage to prior role in notes or future related-job mechanism

## 11.5 Salary Unknown
### Handling rule
- allow null salary fields
- do not block record creation

## 11.6 Company Confidential
### Handling rule
- if company genuinely unknown, block full Job creation unless placeholder policy exists
- if known privately but hidden in source, use the best stable permitted identifier available

## 11.7 Duplicate Role from LinkedIn and Company Site
### Handling rule
- one canonical job record
- prefer company site or strongest canonical source URL
- preserve alternate source in notes or source_ref-related handling

## 11.8 Same Company, Same Title, Different Location
### Handling rule
- treat as distinct jobs if location materially changes the opportunity
- include location/location_type in duplicate logic

## 12. Recommended V1 Jobs Schema

## 12.1 Must-Have Columns for V1
- job_id
- title
- company
- source_type
- source_platform
- posting_url
- recruiter_id
- status
- date_found
- last_status_change
- notes
- sync_status
- created_at
- updated_at

## 12.2 Nice-to-Have Columns for Later
- direct_apply_url
- company_careers_url
- location
- location_type
- fit_score
- fit_notes
- salary_min
- salary_max
- salary_raw
- posted_date
- date_applied
- followup_date
- source_ref

## 13. Dependencies and Next Document
This spec depends on:
- `JT7_System_Architecture.md`
- `JT7_Artifact_Inventory_and_Folder_Map.md`
- `JT7_Structured_Data_Master_Plan.md`

Recommended next document:
- `JT7_Recruiters_Data_Spec.md`
