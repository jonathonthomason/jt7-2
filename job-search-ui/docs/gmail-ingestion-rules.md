# Gmail Ingestion Rules

## Purpose
Canonical Gmail-driven tracking logic for the JT7 scheduled task system.

This file defines how incoming mail should drive pipeline updates, signal creation, recruiter tracking, and action generation.

---

## Core Role of Gmail
Gmail is the primary inbound signal layer for job-search communications.

It should be used to detect and drive updates from:
- recruiters
- hiring managers
- hiring teams
- hiring companies
- job boards
- application systems
- scheduling tools
- candidate communications

Gmail should be treated as a first-class evidence source for status changes.

---

## What Gmail Should Detect
The email scan should look for:
- recruiter replies
- outreach from recruiters
- application confirmations
- interview scheduling
- interview updates or reschedules
- interview cancellations
- rejections
- follow-up requests
- availability requests
- reminders
- stale/no-response indicators when applicable

---

## Primary Task Ownership
Gmail logic feeds these task modules:
- EMAIL_SIGNAL_SCAN
- SIGNAL_CLASSIFICATION
- PIPELINE_STATE_SYNC
- PIPELINE_UPDATE
- ACTION_GENERATION
- PRIORITY_SURFACING
- PASS_LOGGER

It also enforces the Gmail thread state model and label system defined in:
- `docs/gmail-organization-rules.md`

---

## Inbound Signal Sources
### Direct human sources
- recruiter emails
- hiring manager emails
- coordinator / scheduler emails
- talent acquisition emails

### Platform and system sources
- LinkedIn
- Indeed
- Built In
- Greenhouse
- Workday
- Welcome to the Jungle
- scheduling systems such as Calendly or similar
- ATS / confirmation system mailboxes

---

## Output Targets
Gmail-derived signals may update:
- `Signals`
- `Jobs`
- `Recruiters`
- `Actions`
- `TaskRuns`

If an email clearly maps to an interview event, the scan should also create or update event-related state when that structure exists.

---

## Signal Classification Targets
Gmail-derived signals should classify into at least:
- `NEW_APPLICATION`
- `APPLICATION_CONFIRMATION`
- `RECRUITER_REPLY`
- `RECRUITER_OUTREACH`
- `INTERVIEW_SCHEDULED`
- `INTERVIEW_UPDATED`
- `INTERVIEW_CANCELLED`
- `REJECTION`
- `FOLLOW_UP_REQUIRED`
- `AVAILABILITY_REQUEST`
- `NETWORKING_SIGNAL`
- `STALE_NO_RESPONSE_PATTERN`

---

## Matching Rules
Email signals should attempt to match against existing tracker records using:
- company name
- recruiter name
- sender email domain
- known contact email
- role title keywords
- thread continuity
- existing job links or ATS references

### Match priority
1. exact known recruiter/contact email
2. exact company + role match
3. known thread continuity
4. sender domain + company inference
5. content-based role/company inference

If confidence is weak:
- create signal
- avoid destructive overwrite
- surface for review if needed

---

## Update Rules
### Safe auto-update cases
Auto-update is allowed when confidence is high for:
- application confirmation
- interview scheduled
- interview updated
- rejection
- recruiter reply tied to existing thread/company/role

### Cautious update cases
Use review-aware behavior when:
- company match is ambiguous
- role match is ambiguous
- multiple open applications could match
- sender identity is unclear
- the message implies a stage change but lacks explicit context

### Non-destructive rule
Do not overwrite stronger existing tracker data with weaker inferred email data.
Always preserve evidence.

---

## Evidence Rule
Every meaningful Gmail-derived update should attach evidence metadata when possible:
- source: gmail
- sender
- subject
- message date
- thread id if available
- short excerpt or summary

---

## Action Generation Rules
Gmail-derived signals should generate actions such as:
- reply to recruiter
- confirm interview
- provide availability
- prepare for interview
- follow up after stale silence
- review rejection outcome and close record

Each action should include:
- instruction
- reason
- urgency

---

## Priority Surfacing Rules
Surface automatically when Gmail indicates:
- interview scheduled
- interview changed or cancelled
- recruiter reply requiring action
- follow-up needed within 48 hours
- application moved to next stage
- rejection requiring closure/update

---

## Tracker Sync Rule
When Gmail creates meaningful tracker CRUD:
1. update Google Sheets first
2. sync local mirror second
3. commit local mirror changes to git third when data changed

Gmail should never update only a chat response without updating persistent system state.

---

## Success Rule
Gmail ingestion is working when:
- important recruiting and application emails create structured signals
- interviews are captured from mail reliably
- recruiter communication updates pipeline state
- actions are generated automatically
- dashboard/task views reflect the change without manual reconstruction
