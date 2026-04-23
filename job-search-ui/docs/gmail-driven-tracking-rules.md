# Gmail-Driven Tracking Rules

## Purpose
Canonical Gmail-driven tracking logic for JT7.

This file defines how Gmail acts as the primary inbound signal layer for job-search state changes, how Calendar is used as verification for interview/event signals, how job boards act as discovery and supplemental evidence, and how accepted updates flow into the live tracker and synchronized mirror system.

---

## Operating Model
- Gmail = primary inbound signal layer
- Calendar = interview and event verification layer
- Job boards = discovery and supplemental evidence
- Google Sheets = live tracker truth
- local mirror = synchronized structured persistence layer
- git = versioned history of local mirror changes

---

## Gmail Detection Scope
Gmail must detect and interpret signals for:
- recruiter replies
- interview scheduling
- reschedules
- cancellations
- confirmations
- rejections
- follow-ups
- hiring manager communication
- job board confirmations
- application receipts

These Gmail signals may update:
- `Signals`
- `Jobs`
- `Recruiters`
- `Actions`
- `TaskRuns`

---

## Thread Scanning Rules
### Scan targets
- inbox
- relevant JT7 labels
- thread history for existing job-related conversations

### Scan scope
- process only new or changed messages since last run when possible
- operate at thread level, not just single-message level
- maintain thread state awareness across runs

### Thread state awareness
Thread logic must recognize:
- waiting -> action-needed transitions
- action-needed -> waiting transitions after user response
- interview-active state
- closed / archived / completed state

---

## Signal Extraction Rules
For each relevant Gmail signal, extract when possible:
- sender
- sender domain
- subject
- timestamp
- thread id
- message id
- body summary
- detected company
- detected recruiter or person
- detected role
- signal type
- confidence

---

## Deduplication Rules
Do not create duplicate `Signals` or `Jobs` records for the same event.

Use these identifiers in descending priority:
1. Gmail thread id
2. Gmail message id
3. existing linked job/application record
4. company + recruiter/person + timestamp proximity
5. company + role + thread continuity

If deduplication confidence is weak:
- preserve the signal
- mark for review
- avoid destructive merges

---

## Sender and Domain Classification Model
### Source classes
- recruiter
- hiring_manager
- employer_hr
- job_board
- scheduler
- automated_system
- irrelevant_noise
- unknown_review_needed

### Domain/source heuristics
#### recruiter agency domains
Classify as `recruiter` when domain or sender strongly suggests agency recruiting.
Examples include staffing/recruiting firms and recruiter-specific sender patterns.

#### employer/company domains
Classify as `hiring_manager` or `employer_hr` when domain matches known employer/company context or clearly indicates internal company hiring communication.

#### job boards
Classify as `job_board` when sender/domain matches platforms such as:
- linkedin
- indeed
- builtin
- greenhouse-hosted candidate mail if platform-identified
- workday-originated recruiting mail when platform-identifiable
- Welcome to the Jungle

#### scheduling systems
Classify as `scheduler` when sender/domain or content indicates scheduling infrastructure such as Calendly or similar tools.

#### generic HR/ATS systems
Classify as `automated_system` when sender/domain indicates system-generated notifications, confirmations, or ATS workflow mail.

#### unknown senders
Classify as `unknown_review_needed` unless content and thread evidence justify stronger classification.

### Confidence guidance
- domain + sender + thread continuity aligned -> high confidence
- domain aligned but role/entity mapping uncertain -> medium confidence
- weak or ambiguous evidence -> low confidence

---

## Signal Classification Targets
Classify Gmail-derived signals into at least:
- `APPLICATION_CONFIRMATION`
- `RECRUITER_OUTREACH`
- `RECRUITER_REPLY`
- `INTERVIEW_SCHEDULED`
- `INTERVIEW_UPDATED`
- `INTERVIEW_CANCELLED`
- `REJECTION`
- `FOLLOW_UP_REQUIRED`
- `HIRING_MANAGER_COMMUNICATION`
- `JOB_BOARD_CONFIRMATION`
- `AVAILABILITY_REQUEST`
- `FINAL_ROUND_SIGNAL`
- `OFFER_SIGNAL`
- `STALE_NO_RESPONSE_PATTERN`
- `IRRELEVANT_NOISE`

---

## Status Mapping Model
### Pipeline status mapping
- application receipt / confirmation -> `Applied`
- recruiter outreach asking to connect -> `Recruiter Contacted`
- phone screen scheduling -> `Screening`
- hiring manager interview scheduling -> `Interviewing`
- panel / onsite / loop request -> `Interviewing`
- take-home / exercise -> `Interviewing`
- final interview language -> `Interviewing`
- rejection language -> `Rejected`
- offer language -> `Offer`
- cancellation / pause language -> review-needed or `Cold` / hold logic depending on context
- no response after defined window -> follow-up candidate / stale candidate logic, not immediate destructive status overwrite

### Action behavior mapping
Each signal must map to one of:
- auto-update allowed
- action required
- human review required
- no-op / log only

---

## Matching Model
### 1. Recruiter matching
Priority:
1. exact email match
2. normalized sender name + domain match
3. recruiter agency + known company context
4. create recruiter record if confidence is high enough

### 2. Company matching
Priority:
1. exact company name already in tracker
2. domain-based inference
3. thread history context
4. job board metadata if present

### 3. Job matching
Priority:
1. exact role title match
2. explicit thread linked to existing application
3. company + title + recent timeline match
4. otherwise create review-needed signal instead of forcing bad linkage

### 4. Unknown handling
- do not silently invent wrong matches
- create review-needed records when below threshold
- preserve evidence for later resolution

---

## Confidence Threshold Model
### High confidence
- safe to auto-update tracker
- criteria: strong thread identity, clear sender/domain classification, explicit message meaning, high-confidence company/job match

### Medium confidence
- create signal + proposed update + review-needed
- criteria: relevant signal is likely real, but company/job/person matching is not strong enough for safe automatic mutation

### Low confidence
- log only or ignore unless clearly relevant
- criteria: weak relevance, ambiguous sender, ambiguous company/role, or likely noise

---

## Auto-Update vs Review-Needed Rules
### Auto-update examples
- explicit rejection email from known thread -> auto-update `Rejected`
- interview confirmation tied to known recruiter/thread -> auto-update + create action
- application confirmation from known system -> auto-update `Applied`

### Review-needed examples
- ambiguous mail from unknown sender with unclear role/company
- unclear status progression without strong thread linkage
- multiple open applications could match the same thread

### Action-only examples
- recruiter reply that clearly needs response but does not yet justify a stage change
- follow-up reminder without a new explicit pipeline stage

### Log-only examples
- newsletters
- marketing mail
- weakly related or irrelevant notifications

---

## Tracker Write Rules
When Gmail signals are accepted:
- `Signals` receives raw + classified signal record
- `Jobs` receives status update or new record when justified
- `Recruiters` receives recruiter/person linkage when justified
- `Actions` receives follow-up / prep / reply tasks when needed
- `TaskRuns` receives execution logging

Writes must preserve evidence and avoid destructive overwrite of stronger existing data.

---

## Calendar Verification Layer
Use Calendar as a verification layer for interview/event signals.

Rules:
- if Gmail suggests interview scheduling, check Calendar for matching event when available
- if Calendar confirms, raise confidence
- if Gmail indicates reschedule/cancel, reconcile against Calendar and update downstream state
- calendar evidence may strengthen but should not erase stronger direct communication context without reconciliation

---

## Job Board Role
Job boards are used as:
- discovery source
- supplemental evidence
- fallback context

Job boards should not override clearer Gmail evidence unless explicit logic supports it.

---

## Scheduler and Runtime Alignment
This Gmail-driven tracking logic runs inside the live JT7 chain:
- EMAIL_SIGNAL_SCAN
- SIGNAL_CLASSIFICATION
- PIPELINE_STATE_SYNC
- PIPELINE_UPDATE
- LOCAL_MIRROR_SYNC
- GIT_COMMIT_SYNC
- ACTION_GENERATION
- PRIORITY_SURFACING
- PASS_LOGGER

Minimum runtime schedule:
- 8:30 AM America/Chicago
- 12:30 PM America/Chicago
- 6:00 PM America/Chicago

This is persisted through the runtime scheduler/task state files and the executable chain runner.

---

## Persistence Rule
For meaningful CRUD:
1. update Google Sheets first
2. update local mirror second
3. commit local mirror changes to git third

Do not create competing primaries.
Sheets remains the authoritative live truth.

---

## Success Rule
System is healthy when Gmail acts as a real primary signal layer for:
- signal creation
- classification
- matching
- confidence-based update decisions
- tracker writes
- action generation
- scheduled execution with persisted runtime state
