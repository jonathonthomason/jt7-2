# JT7 Competition Data Spec

## Document Metadata
- **System:** JT7 Job Intelligence System
- **Document type:** detailed entity data specification
- **Entity:** Competition
- **Status:** draft-initial
- **Primary path:** `JT7/00_System/Data-Specs/JT7_Competition_Data_Spec.md`

## 1. Purpose and Role
> Consolidation note: this document remains useful for future market-intelligence support, but JT7's current consolidated MVP effort is centered on the Gmail/Calendar/manual → Processing → Google Sheets loop for live job-search status tracking. Until competition tracking becomes part of the active MVP loop again, treat this document as secondary to the core consolidated runtime model.

The Competition tracker is the canonical structured record of market-intelligence signals related to peer candidates, comparable profiles, portfolio benchmarks, role-level market signals, and other external talent indicators.

It is used to:
- capture useful competitive and market positioning signals
- identify recurring profile patterns in target roles and companies
- support portfolio and positioning decisions
- help distinguish noise from meaningful market evidence
- preserve benchmark signals outside Jobs, Recruiters, or Communications

The Competition tracker supports decisions such as:
- what skills or experience signals appear repeatedly in target markets
- how Jonathon’s current positioning compares to visible peer patterns
- which profile signals matter for senior/staff/principal opportunities
- whether certain companies or markets appear to favor specific portfolio or background traits

Why it should remain separate from Jobs and Recruiters:
- jobs are opportunity records
- recruiters are relationship records
- communications are event records
- competition is market intelligence, not operational pipeline state
- mixing competition data into jobs or recruiter notes creates noise and reduces auditability

How it helps with market positioning, portfolio strategy, and job-search prioritization:
- surfaces benchmark profiles worth studying
- shows market-level expectations or recurring signals
- helps identify gaps in positioning narrative or portfolio evidence
- supports selective prioritization of roles where fit signals align strongly

## 2. Canonical Schema

| Field Name | Type | Required | Description | Example |
|---|---|---:|---|---|
| competition_id | id | yes | canonical competition record id | `comp_john_smith_figma_principal_pd` |
| person_name | string | yes* | name of benchmark person or candidate | `John Smith` |
| company | string | no | current or associated company | `Figma` |
| role_title | string | no | associated role title | `Principal Product Designer` |
| current_location | string | no | current known location | `New York, NY` |
| target_location | string | no | target or relevant market location | `Remote (US)` |
| linkedin_url | string | no | LinkedIn profile URL | `https://linkedin.com/in/...` |
| portfolio_url | string | no | portfolio or website URL | `https://johnsmith.design` |
| source_type | enum | yes | where the signal came from | `linkedin` |
| source_detail | string | no | specific provenance note | `LinkedIn search result for principal product designer` |
| benchmark_type | enum | yes | benchmark class | `peer_candidate` |
| signal_strength | enum | yes | confidence/value strength of the signal | `medium` |
| skills_signals | string | no | concise list of skill/profile signals | `systems thinking; fintech; growth design` |
| industry_signals | string | no | industry/domain indicators | `design systems; SaaS; collaboration tools` |
| compensation_signal | string | no | compensation clue if visible | `$240k listed role benchmark` |
| role_level_signal | enum | yes | inferred role level benchmark | `principal` |
| notes | string | no | concise analytical notes | `Strong benchmark for systems-led principal portfolio framing` |
| date_logged | date | yes | date entered into JT7 | `2026-04-02` |
| last_reviewed_at | datetime | no | last review/update time | `2026-04-10T14:00:00Z` |
| status | enum | yes | competition record lifecycle state | `active` |
| sync_status | enum | yes | sync state of the record | `clean` |
| created_at | datetime | yes | creation timestamp | `2026-04-02T13:00:00Z` |
| updated_at | datetime | yes | last update timestamp | `2026-04-10T14:00:00Z` |

## 3. Identity Rules

## 3.1 Primary Uniqueness Logic
A competition record should be uniquely identified using the strongest available identity in this order:
1. `linkedin_url`
2. `portfolio_url`
3. normalized `person_name + company + role_title`
4. normalized `person_name + benchmark_type + source context` with manual review if weak

## 3.2 Fallback Matching Logic When URLs Are Missing
If no URLs are available, attempt to match using:
- same normalized person name
- same company
- same role title
- similar benchmark context and source detail

If confidence is high, update existing record.
If confidence is medium, flag for manual review.
If confidence is low, create new record.

## 3.3 competition_id Generation Rules
Recommended pattern:
- `comp_<normalized_name>_<normalized_company_or_context>_<normalized_role_or_type>`

If person identity is weak or not appropriate, use a benchmark-style id:
- `comp_<benchmark_type>_<company_or_market>_<yyyymmdd>_<sequence>`

## 3.4 Create vs Update Rules
### Create new record when
- no strong identity match exists
- the signal represents a distinct person or benchmark artifact
- the same person appears in materially different benchmark contexts that should remain distinguishable only if future modeling requires it

### Update existing record when
- LinkedIn URL matches
- portfolio URL matches
- person name + company + role strongly match
- new source adds better evidence to the same benchmark person/profile

## 3.5 Same Person Across Multiple Sources
- keep one canonical competition record when identity match confidence is high
- merge new evidence into source detail, notes, or signal fields
- do not create redundant records for the same person just because multiple public sources exist

## 3.6 Tricky Identity Cases

### Same person with LinkedIn and portfolio only
- merge into one canonical record when names/context align
- prefer LinkedIn URL first for identity, preserve portfolio URL alongside it

### No clear current company
- allow partial record if benchmark is still operationally useful
- company may remain null

### Duplicate names in same market
- require stronger identity such as URL, portfolio, company, or context before merging
- otherwise flag for manual review

### Public profile changed over time
- update existing record
- preserve prior context in notes when materially important

## 4. Status Model

## 4.1 Status Values
- `active`
- `watch`
- `archived`
- `low_relevance`

### active
- benchmark is currently relevant to market or positioning decisions
- use for strong, current signals worth reviewing

### watch
- signal is potentially useful but not yet high-value enough for active use
- use for weaker or incomplete but plausible benchmarks

### archived
- record retained for historical reference but not part of active benchmark review

### low_relevance
- known signal exists but currently low value for JT7 decision-making

## 4.2 Allowed Transitions
- watch → active
- active → low_relevance
- active → archived
- low_relevance → watch
- archived → watch if reactivated intentionally

## 4.3 Manual vs Automatic Setting
- initial status may be agent-inferred based on signal strength and relevance
- manual override is always allowed
- archival should generally be deliberate, not silent

## 5. Benchmark and Signal Model

## 5.1 benchmark_type Values
- `peer_candidate`
- `aspirational_profile`
- `local_market_signal`
- `company_signal`
- `portfolio_reference`
- `other`

### Meaning
#### peer_candidate
- person appears to be directly comparable to a likely competing candidate

#### aspirational_profile
- profile represents a benchmark for desired future positioning, even if not a direct competitor

#### local_market_signal
- market-level benchmark tied to local or target hiring environment

#### company_signal
- signal is more about company preference patterns than a single person

#### portfolio_reference
- benchmark exists primarily for portfolio comparison or inspiration

#### other
- useful benchmark that does not fit the above categories cleanly

## 5.2 signal_strength Values
- `low`
- `medium`
- `high`

### Meaning
- **low:** weak or partial signal; keep if still worth monitoring
- **medium:** useful evidence with moderate confidence or relevance
- **high:** strong, repeated, or highly relevant benchmark signal

## 5.3 role_level_signal Values
- `senior`
- `staff`
- `principal`
- `director`
- `unknown`

### Meaning
- inferred level represented by the benchmark profile or signal
- should reflect the role-level implication, not merely title text if title is noisy

## 5.4 Usage Rules
- agents should infer benchmark_type and role_level_signal only when evidence is reasonably clear
- if unclear, use `other` or `unknown` rather than invent precision
- signal_strength should reflect both confidence and relevance, not confidence alone

## 6. Required Fields for Record Creation

## 6.1 Minimum Required Fields
A competition record must have:
- `competition_id`
- `benchmark_type`
- `signal_strength`
- `role_level_signal`
- `status`
- `source_type`
- `date_logged`
- `sync_status`
- `created_at`
- `updated_at`
- plus at least one benchmark identity anchor:
  - `person_name`
  - or `linkedin_url`
  - or `portfolio_url`
  - or sufficient structured company/market benchmark context

## 6.2 Preferred Fields for Useful Record
- `person_name`
- `company`
- `role_title`
- `linkedin_url`
- `portfolio_url`
- `skills_signals`
- `industry_signals`
- `notes`

## 6.3 Partial Records
Partial records are acceptable when:
- a benchmark signal is useful but full identity is unavailable
- company or role is missing but the signal still helps positioning work
- a company-level or market-level benchmark exists without a single person anchor

## 6.4 Block Write When
- no meaningful benchmark identity or context exists
- benchmark_type missing
- signal_strength missing
- role_level_signal missing
- status invalid
- source_type invalid

## 6.5 Unknown Value Handling
- use null for unknown optional fields
- use `unknown` only for controlled fields that support it, such as `role_level_signal`
- do not invent company, role, or profile URLs

## 7. Update Rules

## 7.1 Safe-to-Overwrite Fields
Safe to overwrite with newer verified data:
- `company`
- `role_title`
- `current_location`
- `target_location`
- `skills_signals`
- `industry_signals`
- `compensation_signal`
- `role_level_signal`
- `signal_strength`
- `status`

## 7.2 Preserve Prior Context
Preserve or append rather than overwrite without trace:
- `notes`
- source provenance details
- materially relevant older company or role context

## 7.3 notes Handling
- append concise analytical notes
- avoid turning the sheet into long-form narrative storage
- preserve only context that helps positioning or market intelligence decisions

## 7.4 last_reviewed_at Behavior
- update when a human or agent meaningfully reviews or refines the record
- do not update it for trivial non-semantic sync-only writes

## 7.5 Signal Refinement Over Time
- signals may become more precise as better evidence appears
- `signal_strength` and `role_level_signal` may be refined
- agents should prefer updating existing record when identity confidence is high

## 7.6 Agent vs Manual Edits
- same validation rules should apply to both
- agent writes should prefer normalization and explicit uncertainty handling
- manual edits may override interpretation when human context is stronger

## 8. Deduplication Rules

## 8.1 Primary Duplicate Detection
Check in this order:
1. exact `linkedin_url`
2. exact `portfolio_url`
3. normalized `person_name + company + role_title`

## 8.2 Fallback Duplicate Detection
Use when URLs are missing:
- normalized `person_name + company`
- normalized `person_name + role_title + target_location`
- same benchmark note/source context with strong overlap

## 8.3 Same Person From Multiple Sources
- merge into one canonical record when identity confidence is high
- preserve multiple source references in notes or source detail
- do not create separate records for the same person unless identity is genuinely ambiguous

## 8.4 Merge vs Manual Review
### Merge automatically when
- LinkedIn URL matches exactly
- portfolio URL matches exactly
- person/company/role match strongly and no conflict exists

### Flag for manual review when
- duplicate name with weak company/role context
- same person may have changed companies but identity is uncertain
- source conflicts materially on company or role title without strong URL identity

## 8.5 Conflict Handling
If company, location, or role-title values conflict:
- prefer newer verified public data when identity is strong
- preserve prior context in notes if strategically relevant
- do not silently overwrite if identity confidence is weak

## 9. Validation Rules

## 9.1 Hard Validation Failures
Reject write when:
- no benchmark identity/context exists
- `benchmark_type` invalid
- `signal_strength` invalid
- `role_level_signal` invalid
- `status` invalid
- `source_type` invalid
- `date_logged` missing or invalid
- `created_at` or `updated_at` missing or invalid

## 9.2 Soft Warnings
Warn when:
- no company present
- no role_title present
- no LinkedIn or portfolio URL present
- duplicate confidence is medium but not high
- benchmark is active with very weak notes or signals
- last_reviewed_at is very old while status remains active

## 9.3 Acceptable Incomplete Records
Allowed when:
- no portfolio exists
- no LinkedIn exists
- company unknown but benchmark remains useful
- person identity weak but company-level or market-level signal is still actionable

## 9.4 Valid URL / Source Combinations
- LinkedIn URL should be used only for LinkedIn-like identity URLs
- portfolio URL should be used only for portfolio/website references
- source_type should reflect actual source class, not interpretation
- if source is manual benchmark note with no URL, that is acceptable if clearly documented

## 9.5 Invalid Status or Signal Values
- no freeform alternatives to controlled values
- values like `high-ish`, `principal?`, or `sort of relevant` are invalid in canonical fields
- uncertainty should live in notes, while controlled fields use normalized values or `unknown`

## 10. Spreadsheet Implementation Guidance

## 10.1 Recommended Column Order
1. competition_id
2. person_name
3. company
4. role_title
5. benchmark_type
6. signal_strength
7. role_level_signal
8. status
9. current_location
10. target_location
11. linkedin_url
12. portfolio_url
13. source_type
14. source_detail
15. skills_signals
16. industry_signals
17. compensation_signal
18. date_logged
19. last_reviewed_at
20. notes
21. sync_status
22. created_at
23. updated_at

## 10.2 Controlled-Value Columns
Use controlled values for:
- `benchmark_type`
- `signal_strength`
- `role_level_signal`
- `status`
- `source_type`
- `sync_status`

## 10.3 Columns Safe for Manual Editing
- `notes`
- `skills_signals`
- `industry_signals`
- `current_location`
- `target_location`
- `status`
- `signal_strength` with care

## 10.4 Columns to Treat Carefully
- `competition_id`
- `created_at`
- `updated_at`
- `linkedin_url`
- `portfolio_url`
- `role_level_signal` when inferred weakly

## 10.5 Readability Rules
- keep identity, benchmark type, and relevance fields early in the sheet
- keep long notes later in the row
- use concise signal text rather than long commentary in cells
- avoid turning notes into mini-profiles

## 11. Integration Guidance

## 11.1 Telegram Commands
Telegram should be able to:
- add benchmark record
- update relevance/status
- add notes
- set signal strength
- mark benchmark as watch/active/archived

## 11.2 External Public-Source Research
Competition records may be created from:
- LinkedIn research
- public portfolios
- company team pages
- public market observations
- community-sourced intelligence

## 11.3 Portfolio and Positioning Analysis
Competition should support:
- identifying benchmark profiles
- extracting repeated skills/industry signals
- informing positioning and portfolio refinement

## 11.4 Market Signal Review
Competition should remain informational:
- it informs positioning and prioritization
- it does not directly mutate Jobs or Recruiters without explicit logic elsewhere

## 11.5 Drive / Local Sync Behavior
- canonical competition data lives in Drive spreadsheet layer
- local mirror supports degraded mode and local analysis
- sync should preserve canonical IDs, timestamps, and controlled values consistently

## 12. Edge Cases

## 12.1 Profile With No Portfolio
### Preferred handling
- allow record if LinkedIn or other benchmark evidence exists
- keep `portfolio_url = null`

## 12.2 Profile With No LinkedIn
### Preferred handling
- allow record if portfolio or strong source context exists
- keep `linkedin_url = null`

## 12.3 Duplicate Names
### Preferred handling
- do not merge on name alone
- require stronger company/role/URL evidence

## 12.4 Vague Benchmark Note With No Profile URL
### Preferred handling
- allow only if benchmark context is still operationally useful
- prefer watch or low-signal state rather than high-confidence active state

## 12.5 Same Person Changes Company
### Preferred handling
- update existing record if identity is clearly the same person
- preserve prior company context in notes if useful

## 12.6 Aspirational Profile Not in Same Market
### Preferred handling
- allowed
- use `benchmark_type = aspirational_profile`
- do not confuse with direct competitive candidate signal

## 12.7 Incomplete Role-Level Signal
### Preferred handling
- set `role_level_signal = unknown`
- do not over-infer level from vague profile evidence

## 12.8 Outdated Profile Data
### Preferred handling
- preserve record if still useful historically
- downgrade status or signal strength if clearly stale
- update `last_reviewed_at`

## 13. Recommended V1 Competition Schema

## 13.1 Must-Have Fields
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

## 13.2 Optional Fields for Later
- company
- role_title
- current_location
- target_location
- linkedin_url
- portfolio_url
- source_detail
- skills_signals
- industry_signals
- compensation_signal
- last_reviewed_at

## 14. Dependencies and Next Document
This spec depends on:
- `JT7_System_Architecture.md`
- `JT7_Artifact_Inventory_and_Folder_Map.md`
- `JT7_Structured_Data_Master_Plan.md`
- `JT7_Jobs_Data_Spec.md`
- `JT7_Recruiters_Data_Spec.md`
- `JT7_Communications_Data_Spec.md`

Recommended next document:
- `JT7_Lookup_and_Controlled_Values_Spec.md`
