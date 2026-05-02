# JT7 IA and Interaction Flows

## Purpose
Document the current information architecture and interaction flows for the JT7 system across three levels:
1. system platform
2. JobOps agent
3. primary human user

This is a current-state product architecture outline, not a final UX spec.
It is meant to support roadmap refinement, screen planning, workflow hardening, and future schema design.

---

## 1. Product Model

JT7 currently operates as a multi-layer cockpit system.

### Core framing
- **JT7 Platform** builds and maintains the system
- **JobOps** operates the cockpit
- **Primary human user** makes consequential judgment calls and uses trusted state to run the search

### Core product rule
- signals are reviewed
- opportunities are operated
- trust must be earned before canonical mutation

### Core trust boundary
- **Untrusted layer:** intake, raw signals, inferred metadata, staged imports
- **Trusted layer:** canonical jobs, accepted contacts, next actions, event history, operational tasks

---

# 2. System Platform Level

## 2.1 Platform IA

### A. Intake Systems
Purpose: receive and normalize inbound opportunity signals.

**Primary objects:**
- email-derived signals
- job-board import rows
- calendar-derived signals
- recruiter messages
- parsed metadata
- duplicate candidates

**Responsibilities:**
- ingestion
- parsing
- normalization
- confidence assignment
- provenance preservation

---

### B. Review and Staging Systems
Purpose: hold pre-trusted information until it is reviewed or promoted.

**Primary objects:**
- Review Queue items
- staged opportunities
- duplicate / collision candidates
- hold reasons
- mismatch-hold state
- source-link evidence
- promotion recommendations

**Responsibilities:**
- isolate noisy intake from canonical state
- prepare operator-safe review surfaces
- preserve evidence and rationale
- enforce one-item promotion discipline
- block promotion when application-readiness gates fail

---

### C. Trusted Operational Systems
Purpose: store and expose clean job-search operating state.

**Primary objects:**
- Jobs
- Recruiters / Contacts
- Actions / Next Actions
- Signals after accepted linkage
- TaskRuns / audit-adjacent state
- event history
- application-readiness fields

**Responsibilities:**
- canonical workflow state
- pipeline operation
- action tracking
- recruiter follow-through
- dashboard-ready records
- aligned application-point context for location, ATS, and differentiation

---

### D. Persistence and Sync Systems
Purpose: coordinate truth, mirrors, and operational evidence.

**Primary stores:**
- Google Sheets as canonical tracker truth
- local JSON/CSV mirrors as operational recovery/audit layer
- markdown docs as system-logic source of truth in workspace/git
- Google Drive as mirrored reference/access layer
- git history as versioned product/runtime evidence

**Responsibilities:**
- trusted writeback
- local mirror sync
- reporting
- controlled persistence
- runtime hygiene

---

### E. Orchestration and Runtime Systems
Purpose: execute scheduled or triggered work reliably.

**Primary objects:**
- scheduler state
- pass logs
- task registry
- runtime reports
- execution status

**Responsibilities:**
- scheduled runs
- catch-up behavior
- task sequencing
- fault isolation
- proof of execution

---

## 2.2 Platform-Level Primary Use Cases

### Core Validation Rule — Application Readiness
No opportunity should move from staging into the trusted pipeline without a verified match across three canonical dimensions:
1. location requirements
2. ATS optimization basis
3. differentiation highlights

If any dimension fails or remains ambiguous, the item should move to `Mismatch Hold` instead of being labeled cleanly apply-ready.


### Use Case 1 — Ingest new signals
**Goal:** convert external inputs into structured intake objects.

**Flow:**
1. receive inbound signal
2. parse metadata
3. attach provenance and source links
4. evaluate confidence / duplication risk
5. route to review, staging, or trusted update candidate

**Output:**
- structured intake object with evidence and routing state

---

### Use Case 2 — Protect canonical truth
**Goal:** prevent noisy intake from contaminating `Jobs`.

**Flow:**
1. receive staged or reviewed candidate
2. apply trust checks
3. evaluate duplicate and same-company collision rules
4. require evidence link presence
5. validate location fit, ATS basis, and differentiation readiness
6. allow promote / merge / hold / reject path
7. send failed validation cases to `Mismatch Hold`

**Output:**
- only trusted opportunities mutate canonical state

---

### Use Case 3 — Persist meaningful runtime state
**Goal:** ensure operational changes survive cleanly.

**Flow:**
1. successful task or writeback occurs
2. canonical tracker updates first when relevant
3. local mirrors refresh
4. runtime evidence files update
5. git persistence captures intentional artifacts only
6. Drive mirror refreshes important docs/artifacts when relevant

**Output:**
- auditable, durable operational state without runtime junk pollution

---

### Use Case 4 — Recover from degraded dependencies
**Goal:** keep the cockpit usable when an external contract is imperfect.

**Flow:**
1. detect missing tab, failed call, or malformed dependency behavior
2. classify whether failure is platform-critical or fail-soft eligible
3. use approved fallback when safe
4. preserve alert / evidence for repair
5. prevent local fallback from becoming silent canonical truth

**Output:**
- continued operation with explicit degradation boundaries

---

## 2.3 Platform Interaction Model

### Core platform interactions
- ingest
- parse
- stage
- sync
- persist
- recover
- report
- escalate

### Platform user of record
The platform is not the daily end-user surface.
It is the underlying service architecture that enables JobOps and the human dashboard.

---

# 3. JobOps Agent Level

## 3.1 JobOps IA

### A. Onboarding / Grounding
Purpose: gather enough evidence to build persona-aware search criteria.

**Primary objects:**
- resume
- portfolio
- dossier
- target criteria
- exclusion criteria
- operating preferences

---

### B. Review Queue
Purpose: resolve ambiguous intake before trusted mutation.

**Primary objects:**
- Signal
- extracted company / role / recruiter fields
- confidence score or review reason
- evidence links
- proposed disposition

**Available actions:**
- Confirm
- Link
- Dismiss
- Defer
- Mark duplicate
- Escalate

---

### C. Staging Queue
Purpose: evaluate broad-board or staged opportunities before promotion.

**Primary objects:**
- staged role
- source link
- fit assessment
- duplicate candidate
- same-company collision candidate
- hold or reject reason

**Available actions:**
- Promote
- Merge
- Hold
- Reject

---

### D. Trusted Pipeline Operations
Purpose: operate confirmed opportunities.

**Primary objects:**
- canonical job row
- recruiter/contact
- next action
- follow-up state
- notes
- event trail
- location fit state
- ATS optimization notes
- differentiation highlights

---

### E. Human Handoff Layer
Purpose: prepare a decision-ready set for the primary human.

**Primary objects:**
- shortlisted opportunities
- recommended actions
- risk / ambiguity notes
- hold reasons
- mismatch-hold items
- unresolved edge cases
- optimization brief

---

## 3.2 JobOps Primary Use Cases

### Use Case 1 — Ground a new user
**Goal:** move from generic search to evidence-based targeting.

**Flow:**
1. request grounding artifacts
2. ingest resume / portfolio / dossier
3. extract strengths, targets, and constraints
4. define fit and exclusion rules
5. produce first search profile

**Output:**
- usable search/ranking profile

---

### Use Case 2 — Triage raw signals
**Goal:** convert noisy inbound items into reviewable or dismissible units.

**Flow:**
1. inspect signal and metadata
2. confirm relevance and confidence
3. identify duplicates or ambiguity
4. choose confirm / link / dismiss / defer / escalate
5. preserve rationale and evidence

**Output:**
- clean review disposition without contaminating trusted state

---

### Use Case 3 — Promote staged opportunities
**Goal:** convert good staged items into canonical opportunities safely.

**Flow:**
1. inspect staged item
2. validate source link and provenance
3. compare against canonical jobs
4. detect duplicate or same-company collision
5. validate location fit, ATS basis, and differentiation readiness
6. choose promote / merge / hold / reject
7. route strategy-gap cases into `Mismatch Hold`

**Output:**
- trusted opportunity mutation or safe non-promotion decision

---

### Use Case 4 — Prepare human decisions
**Goal:** reduce user effort by packaging decision-ready work.

**Flow:**
1. rank reviewed opportunities
2. add concise rationale
3. check location fit explicitly
4. prepare ATS optimization basis
5. prepare differentiation highlights
6. flag risks or unknowns
7. identify recommended next action
8. surface only the items needing judgment

**Output:**
- human decision set with low noise and clear tradeoffs

---

### Use Case 5 — Operate daily pipeline
**Goal:** maintain momentum from trusted state.

**Flow:**
1. review current canonical jobs
2. identify most urgent next actions
3. update follow-up readiness
4. monitor recruiter/interview status
5. maintain apply-ready vs submit-ready distinction
6. hand off action prompts or approvals to the human when needed

**Output:**
- current, actionable pipeline state

---

## 3.3 JobOps Interaction Model

### Core JobOps interactions
- ask
- intake
- review
- rank
- hold
- promote
- merge
- escalate
- hand off

### JobOps product stance
JobOps is the **cockpit operator**, not the platform architect.
It should optimize clarity, trust, and readiness, not runtime mechanics.

---

# 4. Primary Human User Level

## 4.1 Human-Level IA

### A. Identity and Search Profile
Purpose: define the candidate and target market.

**Primary objects:**
- target seniority
- role family
- strengths
- constraints
- exclusions
- work preferences

---

### B. Decision Dashboard
Purpose: present the highest-value reviewed items and pending decisions.

**Primary objects:**
- recommended opportunities
- staged promotion candidates
- ambiguous edge cases
- follow-up prompts
- suggested next moves

---

### C. Canonical Pipeline View
Purpose: operate the active job search from trusted state.

**Primary objects:**
- active jobs
- status
- next action
- recruiter touchpoints
- interview steps
- supporting links

---

### D. Exception and Approval Surface
Purpose: handle consequential or ambiguous cases.

**Primary objects:**
- unusual role fits
- duplicate uncertainty
- missing evidence edge cases
- mismatch-hold items
- application/outreach decisions
- escalation items from JobOps

---

### E. Progress / Momentum Surface
Purpose: help the user see whether the search is moving.

**Primary objects:**
- today’s next actions
- overdue follow-ups
- new reviewed items
- interview / recruiter movement
- blockers and stalls

---

## 4.2 Human Primary Use Cases

### Use Case 1 — Complete onboarding
**Goal:** give the system enough evidence to search intelligently.

**Flow:**
1. provide resume / portfolio / dossier
2. clarify target roles and constraints
3. review generated profile
4. correct assumptions
5. confirm search framing

**Output:**
- accurate profile and targeting model

---

### Use Case 2 — Review prepared opportunities
**Goal:** spend time on judgment rather than cleanup.

**Flow:**
1. open prepared shortlist or decision dashboard
2. inspect top opportunities and rationale
3. approve / reject / hold edge cases
4. confirm promotions or actions that require judgment
5. move accepted items into active operating flow

**Output:**
- high-confidence decision set

---

### Use Case 3 — Operate the active search
**Goal:** manage the pipeline from trusted state.

**Flow:**
1. review current jobs and next steps
2. choose highest-priority actions
3. update statuses and notes
4. decide whether to apply, follow up, or prepare
5. continue momentum with minimal context reconstruction

**Output:**
- active, current job-search pipeline

---

### Use Case 4 — Resolve exceptions
**Goal:** handle the cases automation should not decide alone.

**Flow:**
1. inspect escalated case
2. review evidence and risk notes
3. decide approve / reject / hold
4. confirm consequential mutation or defer decision
5. return case to trusted flow

**Output:**
- human-owned exception resolution

---

### Use Case 5 — Monitor progress
**Goal:** know whether the search is healthy and moving.

**Flow:**
1. inspect momentum indicators
2. review due follow-ups and stale items
3. notice gaps in pipeline movement
4. select the next meaningful action
5. re-enter operating flow

**Output:**
- reduced drift and clearer execution cadence

---

## 4.3 Human Interaction Model

### Core human interactions
- provide
- confirm
- review
- approve
- reject
- hold
- act
- monitor

### Human product stance
The human should not have to manage platform internals.
The system should reduce noise, compress context, and surface only the decisions that benefit from human judgment.

---

# 5. Cross-Level Interaction Flows

## Flow A — New user grounding
**System platform:** supports evidence storage and schema persistence
**JobOps:** requests and interprets grounding artifacts
**Human:** provides documents and confirms positioning

**Sequence:**
1. human shares resume / portfolio / dossier
2. JobOps extracts targets, strengths, constraints
3. platform stores resulting profile artifacts
4. JobOps returns first search profile
5. human confirms or corrects

---

## Flow B — Signal to review queue
**System platform:** ingests and normalizes signal
**JobOps:** evaluates signal disposition
**Human:** only intervenes if ambiguity is high

**Sequence:**
1. signal arrives
2. platform parses and preserves evidence
3. JobOps reviews confidence / duplication
4. JobOps confirms, links, dismisses, defers, or escalates
5. event history records outcome

---

## Flow C — Staging to canonical promotion
**System platform:** enforces writeback path and trust rules
**JobOps:** decides promote / merge / hold / reject
**Human:** intervenes on ambiguous or consequential cases

**Sequence:**
1. staged opportunity is surfaced
2. JobOps checks fit, evidence, duplicates, collision risk
3. if clean, JobOps promotes or merges
4. platform writes canonical update and syncs mirrors
5. if risky, JobOps holds or escalates to human

---

## Flow D — Decision dashboard handoff
**System platform:** renders trusted and prepared state
**JobOps:** packages recommendation + rationale
**Human:** makes final decision

**Sequence:**
1. JobOps ranks and annotates opportunities
2. JobOps prepares location fit, ATS basis, differentiation highlights, and an optimization brief
3. platform presents decision-ready set with matching structured fields
4. human reviews rationale, evidence, and application-readiness context
5. human approves / rejects / holds
6. approved items become `Apply-Ready`
7. platform records decision and updates trusted state

---

## Flow E — Daily pipeline operation
**System platform:** maintains current canonical state and action visibility
**JobOps:** keeps queue and next actions ready
**Human:** performs the high-value search actions

**Sequence:**
1. platform surfaces current pipeline and due actions
2. JobOps prepares the top next moves
3. human chooses and executes priority actions
4. status and next actions update
5. momentum remains visible

---

## Flow F — Resume optimization / transformation layer
**System platform:** validates structured readiness and records artifact state
**JobOps:** drafts tailored submission artifacts
**Human:** approves final submission-ready materials

**Sequence:**
1. human approves an `Apply-Ready` opportunity from the decision dashboard
2. JobOps compares the base resume against the job description
3. JobOps generates a tailored artifact by aligning title/summary, ATS keywords, and role-specific differentiation highlights
4. platform verifies that the tailored artifact still satisfies location, ATS, and differentiation requirements
5. the role moves to `Submit-Ready` when the transformation completes cleanly

---

## 5.1 Structured State Model
| State | Definition | Transition Trigger |
| :--- | :--- | :--- |
| **Review** | Raw signal, unverified. | Intake system. |
| **Staging** | Processed, high-confidence opportunity candidate. | JobOps triage. |
| **Mismatch Hold** | Valid opportunity, but one or more application-readiness dimensions do not match strategy or are incomplete. | Validation gate failure. |
| **Apply-Ready** | Verified opportunity with matched location, ATS basis, differentiation highlights, and optimization brief. | Validation gate success + human decision readiness. |
| **Submit-Ready** | Tailored submission artifact completed and re-verified. | Transformation completion. |

# 6. Primary Screens / Surfaces Implied by the Current Model

## Platform-facing / internal
- runtime status / reports
- scheduler status
- sync / persistence artifacts
- audit / event evidence

## JobOps-facing
- onboarding workspace
- Review Queue
- staging queue
- shortlist / recommendation prep view
- canonical jobs operating view

## Human-facing
- decision dashboard
- canonical pipeline view
- today / next action view
- exception review view
- progress / momentum view

---

# 7. Current Gaps

## Platform gaps
- persistence behavior is cleaner but still not fully canonicalized for Drive refresh behavior
- some fallback behavior is still compensating for imperfect live contracts
- runtime evidence retention rules need continued tightening

## JobOps gaps
- no single structured onboarding object yet
- fit/ranking rules are defined conceptually more than structurally
- staging and review heuristics need a cleaner UI-ready model

## Human UX gaps
- the decision dashboard pattern is defined but not yet unified into one polished operator flow
- canonical pipeline, review decisions, and momentum views are still conceptually stronger than they are as one integrated experience
- exception handling still needs a more explicit product pattern

---

# 8. Product Direction
This architecture should evolve toward:
1. one canonical onboarding schema
2. one unified decision dashboard
3. cleaner staging / promotion / merge interaction patterns
4. stronger human-visible progress and momentum surfaces
5. explicit event-driven learning loops from operator and human decisions

## Related Files
- `docs/jobops-onboarding-ia-outline.md`
- `docs/jobops-platform-operating-spec.md`
- `docs/jt7-job-ops-bot-agent-spec.md`
- `JT7/requirements/JT7_REQ_09_Cockpit_Operator_Model.md`
- `agents/jobops/AGENTS.md`
- `agents/jobops/MEMORY.md`
