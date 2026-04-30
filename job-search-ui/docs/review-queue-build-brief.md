# Review Queue Build Brief

## Audience
Engineering

## Objective
Build Review Queue v1 as the first JT7-2 cockpit surface inside `job-search-ui`.

## Why This First
Review Queue is the trust gateway between raw signals and trusted opportunities.

If it is not established first:
- false positives continue to contaminate downstream state
- dashboard behavior stays fuzzy
- signal vs opportunity boundaries blur

## Phase 1 Scope
### In scope
- implementation-layer types for `Signal`, `Opportunity`, `Contact`, `NextAction`, and `Event`
- canonical enums and review states
- mock fixtures
- pure review action helpers
- Review Queue list view
- signal detail/review panel
- source/evidence link display
- event creation scaffolding

### Out of scope
- full pipeline dashboard
- full opportunity detail experience
- final sync orchestration
- production backend integration beyond agreed mock/state boundaries

## Confirmed Build Decisions
1. First surface: Review Queue
2. Canonical schema lives in `job-search-ui`
3. Start with data model scaffolding, then UI scaffolding
4. Adapt existing app shell/components by default; replace only where architecture conflict is real

## Implementation Sequence
1. define domain types
2. define enums and event types
3. create representative fixtures
4. build pure review action helpers
5. create Review Queue route/screen
6. render queue list and signal detail panel
7. wire review actions to in-memory/mock state
8. emit immutable event records for each meaningful action
9. validate future integration touchpoints with pipeline/opportunity surfaces

## Required Review Outcomes
- confirm as new opportunity
- link to existing opportunity
- dismiss as noise
- mark duplicate
- defer for later review
- escalate as parser/system issue

## Required Event Payload Shape
Each meaningful review action should capture:
- event type
- actor
- timestamp
- prior state
- new state
- linked entity IDs when applicable
- reason/note when available

## Acceptance Criteria
### Data model
- all five core object types exist
- canonical enums are defined
- source/evidence links are first-class fields

### Review logic
- all six review outcomes work against mock state
- confirm/link flows create or update trusted records correctly
- each meaningful action emits an event object

### UI
- queue renders mock signals
- operator can inspect a signal in detail
- operator can perform every review action
- evidence links are visible and usable
- trusted/untrusted boundary is visually clear

## Guardrails
### Must preserve
- trust boundary
- source and evidence links
- immutable event history
- separation of signal review from opportunity operations

### Must avoid
- mixing raw signals directly into dashboard state
- burying URLs inside notes only
- state mutation without event creation
- broad refactors that do not directly support the cockpit model

## Adapt vs Replace Rule
### Adapt first
- app shell
- routing
- shared UI primitives
- existing panels/tables/drawers where structurally compatible

### Replace or isolate when necessary
- feature structures that collapse signal and opportunity into one object
- state flows that assume dashboard-first trust
- patterns that make event history or source links hard to support

## Phase 1 Success
Review Queue v1 succeeds when an operator can:
1. inspect a raw signal
2. choose a disposition
3. create/update trusted state only when appropriate
4. preserve the decision in event history
5. keep unresolved intake out of the trusted dashboard flow
