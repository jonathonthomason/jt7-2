# staging-queue-requirements.md

## Purpose
Define the next business and technical requirements for JobOps intake handling, shortlist generation, and queue readiness.

This document is an operator-side requirements reference.
It clarifies what must be true before staged leads are treated as active queue candidates.

## Scope
In scope:
- staged lead intake
- ranking and shortlist behavior
- duplicate handling
- link completeness expectations
- source/provenance expectations
- queue readiness rules

Out of scope:
- gateway/runtime changes
- architecture redesign
- infra execution
- config mutation

## Business Requirements

### BR-01 — Staging must remain distinct from canonical jobs
Broad imports and weak-confidence leads must stay in staging until intentionally promoted.

### BR-02 — Persona/profile must drive criteria
Operational search requirements should be derived from the active persona/profile source, then used to evaluate fit.

### BR-03 — Active queue must stay small and high-signal
Only the strongest currently actionable items should enter the active queue.
The queue should favor quality over volume.

### BR-04 — Same-company role collisions need explicit handling
When multiple staged roles exist for the same company, JobOps should:
- select a primary candidate when one is clearly stronger
- mark alternates as secondary or hold
- avoid flooding the active queue with same-company variants

### BR-05 — Level stretch must be explicit
If a role is above the primary target level, JobOps should mark it as stretch and not silently mix it with standard pursue items.

### BR-06 — Source quality should affect confidence
Direct-board imports, email alerts, recruiter outreach, and human-confirmed opportunities should not be treated as equally trustworthy by default.

### BR-07 — Reasons for inclusion and exclusion must be traceable
Every surfaced lead should carry a short inclusion reason, exclusion risk, and next operator action.

### BR-08 — Weak or ambiguous items should be held, not forced forward
If fit, distinctness, or actionability is weak, JobOps should keep the item out of the active queue.

## Technical Requirements

### TR-01 — Preserve normalized provenance
Each staged lead should preserve:
- source
- source subtype when available
- posting URL
- import or signal notes
- board/company identifiers when available

### TR-02 — Capture direct apply link separately
If available, `direct_application_link` should be captured distinctly from `job_posting_link`.
If unavailable, the item should remain explicitly incomplete rather than implying the posting URL is the apply URL.

### TR-03 — Duplicate clustering must work across sources
The same role should be recognized across:
- direct board imports
- LinkedIn alerts
- recruiter emails
- company-hosted job pages

Minimum duplicate keys should include some combination of:
- normalized company
- normalized title
- location mode
- source URL or board job id

### TR-04 — Staging rows need explicit lifecycle state
Each staged lead should support a visible lifecycle such as:
- new
- reviewed
- shortlisted
- queued
- held
- rejected
- promoted

### TR-05 — Queue readiness needs explicit fields
A queue-ready lead should have, at minimum:
- fit tier
- duplicate risk
- source
- posting link
- next operator action
- shortlist reason
- hold/exclude reason when not queued

### TR-06 — Multi-role company grouping should be visible
The system should make it easy to see that two or more staged leads belong to the same company cluster so JobOps can suppress redundant queue entries.

### TR-07 — Search criteria lineage should be visible
Search decisions should be traceable back to:
- active persona/profile source
- active search requirements file
- any current manual overrides

### TR-08 — Source diversity should be measurable
The system should support simple reporting on lead mix by source so JobOps can detect overreliance on any one intake channel.

## Operator Rules
- Do not treat completion of these requirements as permission to promote staged rows automatically.
- Keep Google Sheets as canonical tracker truth.
- Use local mirrors and staging artifacts operationally, not as independent truth.
- Escalate implementation design to Platform when fulfillment requires system changes.

## Implementation Layer Mapping

### Data model
Own here when the requirement needs persistent fields, normalized state, or cross-surface semantics.

- **BR-01** — requires explicit staging vs canonical identity and trust-boundary fields.
- **BR-04** — requires company-cluster / primary-vs-secondary relationship support.
- **BR-05** — requires a distinct fit tier or stretch flag, not just display copy.
- **BR-06** — requires normalized source-trust metadata.
- **BR-07** — requires persistent inclusion reason, exclusion risk, and next action fields.
- **BR-08** — requires hold-worthy ambiguity/distinctness state, not just UI labels.
- **TR-01** — source, subtype, posting URL, notes, and board/company identifiers belong in the staged record.
- **TR-02** — `direct_application_link` must be stored distinctly from `job_posting_link`.
- **TR-03** — duplicate keys and cluster metadata belong in the model.
- **TR-04** — lifecycle state is a core staged-record field.
- **TR-05** — queue-readiness fields belong in the model so staging and queue surfaces read the same truth.
- **TR-06** — company grouping/cluster identifiers belong in the model.
- **TR-07** — criteria lineage fields belong in the model if the system must show provenance later.
- **TR-08** — source rollup can be computed, but normalized source categories must exist in the model first.

### Staging UI
Own here when the requirement changes operator review behavior before queue entry.

- **BR-01** — visible trust boundary and explicit non-canonical status.
- **BR-04** — show same-company collisions and identify the strongest candidate vs alternates.
- **BR-05** — visibly mark stretch roles instead of blending them into standard pursue items.
- **BR-06** — display source quality/trust cues during staging review.
- **BR-07** — show reason to include, reason not to include, and next operator action.
- **BR-08** — make hold the default for ambiguous rows rather than forcing binary promote/reject behavior.
- **TR-02** — show posting-link vs direct-apply completeness distinctly.
- **TR-04** — surface lifecycle state transitions clearly.
- **TR-06** — show company grouping/collision context inline.
- **TR-07** — display the active requirements/persona source used for evaluation.

### Queue UI
Own here when the requirement affects the shape of the active shortlist / operator queue after staging.

- **BR-03** — queue needs small, high-signal ranking and suppression of weak items.
- **BR-04** — queue should suppress same-company alternates unless explicitly kept.
- **BR-05** — queue should distinguish `pursue` vs `stretch`.
- **BR-07** — every queued item should show shortlist reason, risk, and next action.
- **BR-08** — held/ambiguous items should stay out of the active queue.
- **TR-05** — queue-ready fields must render directly in queue cards/lists.
- **TR-06** — queue should expose company grouping where relevant.
- **TR-08** — source-mix reporting likely belongs first in queue/ops views, backed by normalized data.

### Ingestion logic
Own here when the requirement affects what is captured, normalized, deduplicated, or pre-scored before UI review.

- **BR-02** — persona/profile criteria should influence fit scoring and rule evaluation as early as practical.
- **BR-04** — same-company collision candidates should be pre-clustered at ingest time.
- **BR-06** — source quality should influence default confidence and ranking.
- **BR-08** — weak/ambiguous items should be pre-held or down-ranked before surfacing.
- **TR-01** — ingestion must capture and normalize provenance at import time.
- **TR-02** — ingestion must preserve direct-apply link separately when available.
- **TR-03** — ingestion must compute duplicate keys/clusters across source types.
- **TR-06** — ingestion should emit company cluster hints to reduce UI-only inference.
- **TR-07** — ingestion/runtime should stamp which active requirements source was used.

## Current placement assessment

### Mostly already started
- **Data model:** staging already has `source`, `sourceBoard`, `boardJobId`, `provenance`, `status`, `fitBand`, `fitScore`, `duplicateRisk`, `duplicateMatches`, `recommendedAction`, `reasons`, and `link`.
- **Staging UI:** trust boundary, duplicate risk, merge/promote split, and fit-based review are already visible.
- **Ingestion/runtime:** initial fit and duplicate heuristics already exist.

### Clear gaps
- **Data model gaps:** no explicit lifecycle beyond `pending/promote/hold/reject`; no stretch tier; no company-cluster id/primary-vs-secondary fields; no separate shortlist reason vs exclusion risk vs next action fields; no criteria-lineage fields.
- **Staging UI gaps:** no explicit same-company collision presentation, no direct-apply completeness display, no stretch badge, no criteria-lineage visibility.
- **Queue UI gaps:** no dedicated shortlist/active queue surface yet for staged-to-queue candidates; no source-mix or suppression view.
- **Ingestion gaps:** no normalized direct-apply link contract, no cross-source duplicate clustering beyond current local heuristics, no stamped persona/search-requirements lineage.

## Recommended implementation order
1. **Data model first** — add lifecycle, stretch/fit tier, direct-apply link, shortlist/exclusion/next-action fields, company-cluster metadata, and criteria lineage.
2. **Ingestion second** — populate those fields during import/planning so UI is reading structured truth instead of inventing it.
3. **Staging UI third** — expose collision groups, completeness, stretch, and criteria lineage for operator decisions.
4. **Queue UI fourth** — build the active shortlist surface on top of the normalized staged model.

## Immediate Next Requirement Priorities
1. explicit same-company collision policy
2. normalized direct-apply link capture
3. duplicate clustering across source types
4. visible staging lifecycle states
5. queue-readiness fields for shortlist output
