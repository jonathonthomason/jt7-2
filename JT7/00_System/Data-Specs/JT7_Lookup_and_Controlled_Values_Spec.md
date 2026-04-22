# JT7 Lookup and Controlled Values Spec

## Document Metadata
- **System:** JT7 Job Intelligence System
- **Document type:** controlled values and lookup specification
- **Status:** draft-initial
- **Primary path:** `JT7/00_System/Data-Specs/JT7_Lookup_and_Controlled_Values_Spec.md`
- **Role:** single source of truth for shared enums, lookup tables, and controlled values across structured data entities

## 1. Purpose and Role
> Consolidation note: this document reflects an earlier broader controlled-values model. JT7's current consolidated MVP operating model now enforces a smaller final status set for live opportunity tracking (`Applied`, `Recruiter Contacted`, `Screening`, `Interviewing`, `Offer`, `Rejected`, `Cold`) and a shared cross-layer schema. Until rewritten, treat this document as partially legacy and subordinate to the newer consolidated model.

Controlled values are required to make JT7 data:
- consistent across spreadsheets
- safe for agent writes
- reliable for filtering and reporting
- predictable for automation and validation
- resistant to spelling drift and ad hoc status invention

Without enforced controlled values, the system breaks in predictable ways:
- reporting fragments because similar meanings use different labels
- filters and dashboards become unreliable
- agents produce inconsistent values
- state transitions lose meaning
- dedupe and validation logic weaken

Controlled values are used by:
- **spreadsheets:** dropdowns, validation, filtering, summaries
- **agents:** safe writes and update logic
- **Telegram commands:** normalization of fuzzy user inputs into canonical values
- **validation logic:** accept/reject/warn decisions for structured records

## 2. Lookup Categories

## 2.1 Job Status Values

### `lead`
- **Description:** role exists as a possible opportunity but is not yet fully reviewed or promoted into active pipeline handling
- **Use when:** role is newly discovered, vague, or not yet curated
- **Do not use when:** application has already been submitted or the role is clearly active in pipeline work

### `saved`
- **Description:** role is intentionally tracked and worth further action
- **Use when:** role has been reviewed and retained for possible action
- **Do not use when:** application has been submitted or the role is only a weak lead

### `applied`
- **Description:** application has been submitted
- **Use when:** direct apply, referral apply, or equivalent submission is complete
- **Do not use when:** no actual submission has occurred

### `interviewing`
- **Description:** active interview process is underway
- **Use when:** recruiter screen, hiring manager screen, panel, or assessment is active
- **Do not use when:** only application has been submitted with no interview progress

### `offer`
- **Description:** offer has been extended or clearly entered final offer state
- **Use when:** formal or confirmed offer exists
- **Do not use when:** final rounds are active but no offer yet

### `rejected`
- **Description:** opportunity has been closed unsuccessfully
- **Use when:** explicit rejection or confirmed process closure exists
- **Do not use when:** silence or uncertainty exists without clear closure

### `archived`
- **Description:** record retained for history but not active
- **Use when:** stale, irrelevant, superseded, or historically retained role should leave active views
- **Do not use when:** role is still operationally relevant

## 2.2 Recruiter Relationship Status

### `cold`
- **Description:** known contact with no meaningful active relationship yet
- **Use when:** contact exists but no real engagement has happened
- **Do not use when:** there has already been substantive interaction

### `warm`
- **Description:** some useful interaction or relationship context exists
- **Use when:** contact is more than merely known, but not strongly active
- **Do not use when:** an ongoing live conversation is happening

### `active`
- **Description:** meaningful current recruiter/contact relationship exists
- **Use when:** live back-and-forth, active opportunity involvement, or ongoing engagement exists
- **Do not use when:** relationship is stale or only lightly established

### `dormant`
- **Description:** previously warm or active relationship is currently inactive
- **Use when:** history exists but current momentum does not
- **Do not use when:** no prior meaningful relationship existed

### `archived`
- **Description:** contact retained for history but removed from active relationship handling
- **Use when:** no longer relevant operationally
- **Do not use when:** relationship may still require follow-up

## 2.3 Recruiter Outreach Status

### `not_contacted`
- **Description:** no outbound contact or meaningful outreach state yet
- **Use when:** recruiter exists but outreach has not started
- **Do not use when:** a message has already been sent

### `contacted`
- **Description:** outbound contact has been made
- **Use when:** email, LinkedIn message, or equivalent outreach has been sent
- **Do not use when:** contact only exists as inbound with no outbound action

### `replied`
- **Description:** contact responded
- **Use when:** recruiter/contact replied to outreach or initiated active conversation back
- **Do not use when:** no actual reply occurred

### `scheduled`
- **Description:** a meeting, call, or next-step interaction is scheduled
- **Use when:** concrete scheduled event exists
- **Do not use when:** only interest exists without a scheduled step

### `closed_loop`
- **Description:** outreach cycle is resolved or closed
- **Use when:** no further immediate outreach action is pending
- **Do not use when:** contact is still waiting on reply or follow-up

### `no_response`
- **Description:** outreach was made and no response arrived in a reasonable window
- **Use when:** silence is operationally meaningful
- **Do not use when:** follow-up window has not elapsed yet

## 2.4 Communication Status

### `logged`
- **Description:** event recorded but not yet classified as awaiting response or closed
- **Use when:** a communication exists but workflow state is not yet resolved
- **Do not use when:** response expectation is already clear

### `pending_response`
- **Description:** a reply is expected or awaited
- **Use when:** communication requires or expects response
- **Do not use when:** event is informational only

### `responded`
- **Description:** response to relevant communication occurred
- **Use when:** reply or return response has been received/sent as appropriate
- **Do not use when:** communication is still awaiting reply

### `closed`
- **Description:** communication loop is resolved
- **Use when:** no immediate additional communication action remains
- **Do not use when:** follow-up is still needed

### `no_response`
- **Description:** communication has gone unanswered past expected response window
- **Use when:** silence is now meaningful
- **Do not use when:** too early to classify as no response

## 2.5 Communication Outcome

### `positive`
- **Description:** interaction advanced relationship or opportunity positively
- **Use when:** message is encouraging, advances process, or signals positive momentum
- **Do not use when:** signal is uncertain

### `neutral`
- **Description:** informational or non-directional interaction
- **Use when:** message carries limited directional meaning
- **Do not use when:** clear positive or negative signal exists

### `negative`
- **Description:** interaction harms or closes opportunity or relationship direction
- **Use when:** rejection, disinterest, or explicitly negative signal exists
- **Do not use when:** ambiguity remains

### `unknown`
- **Description:** outcome cannot yet be confidently interpreted
- **Use when:** available evidence is insufficient
- **Do not use when:** clear tone/result is visible

## 2.6 Communication Action Required

### `none`
- **Description:** no action required from this event
- **Use when:** event is complete or informational only
- **Do not use when:** follow-up or response is required

### `follow_up`
- **Description:** a follow-up is needed
- **Use when:** next step is another message or contact attempt
- **Do not use when:** more specific action is known and available

### `schedule_call`
- **Description:** scheduling action required
- **Use when:** need is to arrange a meeting or conversation
- **Do not use when:** no scheduling action exists

### `send_material`
- **Description:** send resume, portfolio, availability, or related materials
- **Use when:** requested or clearly needed
- **Do not use when:** material transfer is not part of next step

### `apply`
- **Description:** formal application should be submitted
- **Use when:** communication indicates an application step is needed
- **Do not use when:** application is already complete

### `other`
- **Description:** action exists but does not fit current categories
- **Use when:** no existing controlled action fits
- **Do not use when:** an existing specific action fits adequately

## 2.7 Channels

### `email`
- use for email communication
- do not use for LinkedIn messages or calls

### `linkedin`
- use for LinkedIn direct messages or platform outreach
- do not use for profile URLs alone without communication

### `call`
- use for phone or voice call events
- do not use for scheduled meetings that did not occur yet unless modeled as communication event

### `in_person`
- use for real in-person interaction
- do not use for virtual meetings

### `referral`
- use for referral-origin interactions when channel itself is best represented as referral pathway
- do not use when actual interaction channel is better represented as email/linkedin/etc.

### `other`
- use when channel is real but outside known set
- do not use as lazy fallback when exact channel is known

## 2.8 Source Types

### `linkedin`
- use when source originates from LinkedIn listing, profile, or outreach surface

### `indeed`
- use when source originates from Indeed

### `built_in`
- use when source originates from Built In

### `company_site`
- use when source originates from company careers or direct company source

### `referral`
- use when source originated through a human referral path

### `email`
- use when source originated from email discovery or parsing

### `manual`
- use when a human manually created the record without a structured external source

### `import`
- use when source entered through file/list import

### `other`
- use when real source exists but does not fit known categories

## 2.9 Competition Benchmark Types

### `peer_candidate`
- direct comparable candidate benchmark

### `aspirational_profile`
- benchmark profile representing desired future positioning

### `local_market_signal`
- market-specific benchmark signal

### `company_signal`
- signal about a company’s apparent preference pattern

### `portfolio_reference`
- benchmark mainly useful for portfolio comparison

### `other`
- meaningful benchmark not captured above

## 2.10 Signal Strength

### `low`
- weak or incomplete signal
- use when benchmark value is limited or uncertain

### `medium`
- useful but not definitive signal
- use when evidence is meaningful but not strong enough for high confidence

### `high`
- strong and relevant signal
- use when evidence is both clear and strategically useful

## 2.11 Role Level Signal

### `senior`
- use when signal maps best to senior-level benchmark

### `staff`
- use when signal maps best to staff-level benchmark

### `principal`
- use when signal maps best to principal-level benchmark

### `director`
- use when signal maps best to director-level benchmark

### `unknown`
- use when level cannot be inferred reliably

## 2.12 Sync Status

### `clean`
- record is aligned with canonical state
- use when no sync issue exists

### `pending_sync`
- record changed locally and has not yet reconciled
- use in degraded mode or staged sync scenarios

### `error`
- sync or record state error exists
- use when reconciliation or correction is needed

## 3. Transition Rules

## 3.1 Job Status Transitions
### Allowed transitions
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

### Disallowed transitions
- archived → interviewing without explicit reactivation rule
- rejected → offer without intermediate explicit correction
- lead → offer

### Auto-transition triggers
- application confirmation may set `applied`
- interview scheduling may set `interviewing`
- explicit rejection may set `rejected`

### Manual override
- allowed when stronger human context exists

## 3.2 Recruiter Relationship Status Transitions
### Allowed transitions
- cold → warm
- warm → active
- active → dormant
- dormant → warm
- warm/active/dormant → archived

### Disallowed transitions
- archived → active without explicit reactivation
- cold → dormant without meaningful prior interaction

### Auto-transition triggers
- inbound recruiter contact may move cold → warm
- active exchange may move warm → active
- inactivity may later move active → dormant

### Manual override
- allowed

## 3.3 Recruiter Outreach Status Transitions
### Allowed transitions
- not_contacted → contacted
- contacted → replied
- contacted → no_response
- replied → scheduled
- replied → closed_loop
- scheduled → closed_loop
- no_response → replied

### Disallowed transitions
- closed_loop → contacted without new outreach event
- not_contacted → scheduled without tracked contact path

### Auto-transition triggers
- outbound outreach → contacted
- inbound reply → replied
- confirmed meeting/call → scheduled
- overdue silence → no_response

### Manual override
- allowed

## 3.4 Communication Status Transitions
### Allowed transitions
- logged → pending_response
- logged → closed
- pending_response → responded
- pending_response → no_response
- responded → closed
- no_response → responded

### Disallowed transitions
- closed → pending_response without new communication context
- logged → responded without actual response event

### Auto-transition triggers
- outbound message expecting reply → pending_response
- reply event → responded
- unanswered delay → no_response
- resolved thread → closed

### Manual override
- allowed where communication interpretation requires human judgment

## 4. Spreadsheet Implementation

## 4.1 Lookup Tab Recommendation
Use a dedicated **Lookup** tab in the workbook.

Recommended columns:
- `lookup_group`
- `value_key`
- `value_label`
- `description`
- `active`
- `sort_order`
- `notes`

## 4.2 Dropdown Validation
- controlled fields in entity tabs should use dropdown validation from the Lookup tab where practical
- dropdowns should write canonical `value_key`, not freeform display text

## 4.3 Hardcoded vs Referenced Values
- do not hardcode controlled values independently across multiple tabs
- use one referenceable lookup source
- if a platform limitation forces temporary hardcoding, it must still match this spec exactly

## 4.4 Drift Prevention
- no freeform variants in canonical fields
- no undocumented new values
- inactive/deprecated values should remain in lookup history but not appear in active dropdowns

## 4.5 Agent Validation Before Write
Agents must:
- validate all controlled fields against this spec or lookup table
- normalize fuzzy input before write
- reject or warn on unknown values depending on severity
- never invent a new controlled value ad hoc

## 5. Agent Usage Rules
- agents must only write values from this spec
- agents must reject unknown values for required controlled fields unless explicit staging/review mode exists
- agents may map fuzzy human input to the nearest valid controlled value when mapping is unambiguous
- agents must not invent new values without explicit update to this spec
- if multiple controlled values are plausible, agents should warn or request confirmation rather than guess silently

## 6. Extension Rules

## 6.1 Adding New Values
New values may be added only when:
- existing values are insufficient
- the addition is documented in this spec
- affected entity specs remain aligned
- transition/validation implications are reviewed

## 6.2 Deprecating Values
When deprecating a value:
- do not silently delete it from historical meaning
- mark it inactive in lookup tables
- define replacement mapping if applicable
- preserve legacy record interpretability

## 6.3 Handling Legacy Values
If old data contains legacy or invalid values:
- map to canonical replacement where safe
- otherwise flag for review
- do not silently discard ambiguous states

## 6.4 Versioning the Lookup System
- maintain a stable canonical file for current values
- note meaningful changes in document metadata or change history later if needed
- treat lookup changes as system-level changes, not local ad hoc edits

## 7. Validation Rules

## 7.1 Invalid Value Encountered
If an invalid controlled value is encountered:
- reject write for required controlled fields in canonical records
- warn for optional controlled fields where a safe fallback exists
- flag inconsistent records for review

## 7.2 Fallback Behavior
Safe fallback rules:
- use `unknown` only where the category explicitly supports it
- use `other` only where the category explicitly supports it
- do not substitute `other` for convenience when a precise known value exists

## 7.3 Warning vs Rejection
### Reject when
- required status/state field is invalid
- required source/sync/contact type field is invalid
- transition violates explicit disallowed transition logic

### Warn when
- fuzzy input had to be normalized
- value is technically valid but context is weak
- a legacy value was mapped to a canonical value

## 7.4 Inconsistent Records
Records should be flagged when:
- controlled values conflict with timestamps or linked state
- a value is valid in isolation but invalid in transition context
- old deprecated values still appear in active datasets

## 8. Recommended V1 Controlled Values
Use the full minimal set below for V1 implementation:

### Job status
- lead
- saved
- applied
- interviewing
- offer
- rejected
- archived

### Recruiter relationship status
- cold
- warm
- active
- dormant
- archived

### Recruiter outreach status
- not_contacted
- contacted
- replied
- scheduled
- closed_loop
- no_response

### Communication status
- logged
- pending_response
- responded
- closed
- no_response

### Communication outcome
- positive
- neutral
- negative
- unknown

### Communication action required
- none
- follow_up
- schedule_call
- send_material
- apply
- other

### Channels
- email
- linkedin
- call
- in_person
- referral
- other

### Source types
- linkedin
- indeed
- built_in
- company_site
- referral
- email
- manual
- import
- other

### Competition benchmark types
- peer_candidate
- aspirational_profile
- local_market_signal
- company_signal
- portfolio_reference
- other

### Signal strength
- low
- medium
- high

### Role level signal
- senior
- staff
- principal
- director
- unknown

### Sync status
- clean
- pending_sync
- error

## 9. Dependencies and Next Document
This spec depends on:
- `JT7_System_Architecture.md`
- `JT7_Artifact_Inventory_and_Folder_Map.md`
- `JT7_Structured_Data_Master_Plan.md`
- `JT7_Jobs_Data_Spec.md`
- `JT7_Recruiters_Data_Spec.md`
- `JT7_Communications_Data_Spec.md`
- `JT7_Competition_Data_Spec.md`

Recommended next document:
- `JT7_Workbook_Implementation_Plan.md`
