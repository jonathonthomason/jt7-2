# JobOps Onboarding IA Outline

## Purpose
Document the current onboarding information architecture for JT7 JobOps so it can be refined against roadmap goals without losing the present operating model.

## Product Intent
JobOps onboarding exists to gather enough evidence to build a high-quality, persona-aware search profile quickly.

The onboarding experience should:
- feel conversational rather than form-like
- gather evidence before assumptions
- translate user context into operational filtering and ranking behavior
- prepare the system to protect the trust boundary between intake and canonical tracker state

---

## 1. Top-Level Onboarding Information Architecture

### A. Welcome / Framing
**Goal:** establish why onboarding exists and why evidence matters.

**Content:**
- what JobOps does
- why grounding is needed before filtering jobs
- what the user gets out of onboarding
- what happens after enough context is gathered

**Outcome:**
- user understands onboarding as search grounding, not admin overhead

### B. Evidence Intake
**Goal:** collect the minimum viable grounding inputs.

**Content groups:**
1. resume or work-history document
2. portfolio, case studies, or work samples
3. dossier or persona brief
4. LinkedIn or equivalent profile context
5. optional supporting notes / constraints

**Outcome:**
- enough raw evidence exists to derive search criteria from real proof rather than preference guessing

### C. Search Target Definition
**Goal:** turn evidence into explicit targeting criteria.

**Content groups:**
1. target seniority
2. target role family
3. preferred industries / company types
4. work setup / geography
5. explicit eligible geos and hybrid tolerance
6. strengths to optimize for
7. roles to avoid
8. constraints / non-negotiables
9. exclusion patterns that should trigger application-readiness hold behavior

**Outcome:**
- search filters become evidence-based and operationally usable
- location-match logic can be enforced explicitly at application point

### D. Fit Model Calibration
**Goal:** define how the system should evaluate opportunities.

**Content groups:**
1. positive fit signals
2. negative fit signals
3. stretch-role rules
4. same-company / duplicate rules
5. confidence thresholds
6. human-review triggers
7. primary ATS keyword themes
8. strategic signals that later become differentiation highlights
9. measurable impact themes that can become resume bullet stubs

**Outcome:**
- JobOps can distinguish auto-rank, hold, reject, and escalate behavior
- onboarding can seed the later ATS optimization and differentiation process with real evidence

### E. Operational Preferences
**Goal:** define how work should be surfaced to the human operator.

**Content groups:**
1. shortlist style
2. decision cadence
3. noise tolerance
4. follow-up preferences
5. approval boundaries
6. communication style

**Outcome:**
- JobOps output behavior matches the operator’s preferred workflow

### F. Onboarding Output
**Goal:** convert onboarding into working system behavior.

**Outputs:**
1. persona-grounded search profile
2. ranking and filtering rules
3. role include / exclude logic
4. review-queue heuristics
5. shortlist criteria
6. dashboard defaults / human-review rules
7. keyword bank for ATS optimization
8. differentiation library for role-specific positioning
9. screening guardrails for common knockout questions and risks

**Outcome:**
- onboarding becomes reusable system logic rather than a one-time conversation
- the application-readiness gate has structured inputs instead of ad hoc interpretation

---

## 2. Current Conversational Workflow

### Step 1 — Orient
**System action:** explain the goal and ask for grounding artifacts.

**Primary asks:**
- resume
- portfolio / case studies
- dossier if available

### Step 2 — Gather Core Evidence
**System action:** ingest whatever exists and identify what is still missing.

**If docs exist:**
- extract strengths, role targets, and constraints

**If docs do not exist:**
- ask for the minimum viable starting artifact
- optionally provide a dossier-generation prompt

### Step 3 — Define Target
**System action:** clarify:
- role level
- role family
- geography / remote preference
- company type
- avoid list

### Step 4 — Calibrate Filters
**System action:** define:
- what should rank high
- what should be downgraded
- what should never move trusted state automatically

### Step 5 — Confirm Profile
**System action:** return a concise profile summary covering:
- strongest positioning
- role targets
- filter logic
- exclusion logic
- how JobOps will prioritize opportunities
- the initial keyword bank, differentiation library, and location-match assumptions

---

## 3. Current Data Model Outline

### Section 1 — Identity
- name
- discipline
- target seniority
- current market goal

### Section 2 — Evidence Sources
- resume
- portfolio
- case studies
- LinkedIn
- dossier
- evidence gaps

### Section 3 — Target Criteria
- preferred titles
- preferred domains
- preferred company types
- preferred geography
- eligible geos
- preferred work mode
- hybrid tolerance

### Section 4 — Strengths Profile
- domain strengths
- workflow strengths
- leadership / collaboration signals
- measurable impact themes
- strategic differentiation
- ATS keyword themes
- differentiation hooks
- reusable impact bullet stubs

### Section 5 — Exclusion Criteria
- off-target disciplines
- low-seniority roles
- bad-fit environments
- location exclusions
- role-pattern exclusions
- mismatch-hold triggers

### Section 6 — Operating Preferences
- shortlist format
- ranking strictness
- review depth
- approval boundaries
- output tone

---

## 4. Current Human + Agent Role Split During Onboarding

### JobOps owns
- collecting grounding evidence
- deriving search criteria
- defining fit rules
- identifying confidence thresholds
- preparing the first operational profile

### Human owns
- providing evidence
- correcting assumptions
- confirming constraints and preferences
- approving high-impact interpretation when needed

### JT7 Platform owns
- architecture for onboarding persistence
- system rules for trust boundaries
- canonical documentation and workflow design

---

## 5. Current UX Principle
The current onboarding architecture follows this order:
1. understand the person
2. define the search
3. calibrate the filter
4. operationalize the output

In plain language:
- evidence first
- targeting second
- calibration third
- operation fourth

---

## 6. Current Weak Spots
1. there is no single canonical structured onboarding object yet
2. dossier / resume / portfolio inputs are conceptually clear but not fully normalized into one schema
3. onboarding outputs are spread across docs and agent instructions rather than one explicit UI-ready model
4. fit calibration and review-threshold logic still need a cleaner structured artifact
5. the handoff from onboarding profile to live cockpit behavior is defined conceptually but not yet fully rendered as one operator-facing product flow

---

## 7. Roadmap Direction
This outline should be refined toward:
- a UI-ready onboarding schema
- clearer dashboard handoff behavior
- stronger mapping from onboarding evidence to intake filters and ranking logic
- tighter alignment between onboarding outputs and staging / review / shortlist behavior
- a canonical search profile that feeds location matching, ATS optimization, and differentiation at application point

## Related Files
- `docs/jobops-new-user-onboarding.md`
- `docs/jt7-job-ops-bot-agent-spec.md`
- `docs/jobops-platform-operating-spec.md`
- `agents/jobops/AGENTS.md`
- `agents/jobops/USER.md`
- `agents/jobops/MEMORY.md`
- `JT7/requirements/JT7_REQ_09_Cockpit_Operator_Model.md`
