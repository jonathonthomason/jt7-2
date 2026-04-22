# HEARTBEAT.md

## System Role
Heartbeat is JT7’s proactive monitoring loop.
Its purpose is to preserve momentum, surface real issues early, and prevent drift without creating noise.

## Core Rule
If nothing needs attention, reply exactly:
`HEARTBEAT_OK`

If something does need attention:
- do not include `HEARTBEAT_OK`
- send only the useful alert
- keep it short, specific, and actionable

## Operating Goals
- protect momentum
- maintain visibility into current priorities
- surface blockers before they become stalls
- detect drift from the three priority lanes
- catch stale decisions and missing updates
- reduce context reconstruction overhead

## Check Order
Heartbeat should check in this order:
1. active focus
2. blockers
3. career pipeline movement
4. stale decisions
5. drift from goals
6. memory hygiene

Stop at the first high-value issue worth surfacing.
Do not stack multiple weak alerts into one heartbeat.

## What To Check
### 1. Active focus
Primary files:
- `CURRENT.md`
- `ops/focus.md`

Check for:
- missing or stale top priorities
- active tasks with no next actions
- focus that no longer matches real work
- unresolved open questions that are blocking movement

Needs attention if:
- top priorities are unclear
- current state is stale
- active tasks are vague
- next actions are missing

### 2. Blockers
Primary files:
- `ops/focus.md`
- `CURRENT.md`
- relevant workstream files

Check for:
- named blockers with no response plan
- recurring blockers across sessions
- stalled work without a declared reason
- missing decisions preventing movement

Needs attention if:
- a blocker is real and unresolved
- the same blocker keeps reappearing
- work has stopped without a clear cause
- a missing decision is preventing action

### 3. Career pipeline movement
Primary files:
- `career/pipeline.md`
- `career/strategy.md`

Check for:
- active opportunities
- visible role-search movement
- clear next actions per opportunity
- overdue follow-ups
- mismatch between career priority and actual activity

Needs attention if:
- no active opportunities are tracked
- the pipeline is stale
- follow-ups are due but not planned
- interview-stage work has no preparation tasks
- career remains the top priority in theory but not in action

### 4. Stale decisions
Primary files:
- `DECISIONS.md`
- `CURRENT.md`
- active workstream files

Check for:
- unresolved decisions blocking progress
- implied decisions not yet written down
- multiple files signaling ambiguity about direction

Needs attention if:
- a stale decision is slowing execution
- direction is unclear across files
- conversation changed strategy but files did not

### 5. Drift from goals
Primary files:
- `MISSION.md`
- `CURRENT.md`
- `ops/focus.md`
- active workstream files

Check for:
- product work growing faster than career outcomes
- execution tooling expanding without real leverage
- tasks accumulating outside the three priority lanes
- maintenance work crowding out meaningful progress

Needs attention if:
- career is no longer clearly first in practice
- system-building is displacing active job search work
- current effort does not map cleanly to career, product, or execution

### 6. Memory hygiene
Primary files:
- `MEMORY.md`
- `DECISIONS.md`
- `CURRENT.md`
- latest daily memory file

Check for:
- missing durable context
- decisions that were made but not recorded
- stale current-state summaries
- important information still trapped in conversation

Needs attention if:
- future-critical context is not stored
- a meaningful decision is not in `DECISIONS.md`
- `CURRENT.md` no longer reflects the real situation
- a useful insight will likely be lost if not captured

## When To Check
### Frequent heartbeat pass
Use normal heartbeat polls for lightweight checks:
- active focus
- blockers
- drift from goals

### Periodic deeper pass
At lower frequency, also inspect:
- career pipeline health
- stale decisions
- memory hygiene

### Trigger-based checks
Escalate sooner when:
- a new priority is introduced
- a blocker appears repeatedly
- a deadline or follow-up becomes time-sensitive
- major structure changes occur
- career activity appears to be stalling

## Quietness Rules
Heartbeat should be quiet by default.

### Stay quiet when
- no meaningful state changed
- priorities remain clear
- no blocker needs intervention
- a recent heartbeat already surfaced the same issue
- the signal is weak, speculative, or low leverage

### Speak when
- there is a real risk to momentum
- a blocker needs explicit naming
- a missing decision is holding up action
- current state is materially stale
- career movement is missing or at risk

## Escalation Rules
### Escalate immediately when
- career work is stale despite being top priority
- a blocker is recurring and unresolved
- a follow-up or interview action is at risk of being missed
- current-state files no longer reflect reality
- product/system work is clearly displacing career-critical work

### Escalate cautiously when
- the signal is real but not urgent
- a pattern is emerging but not yet persistent
- a decision is starting to age without immediate consequences

### Do not escalate when
- the issue is already known and recently surfaced
- there is no concrete next move
- the issue is mostly cosmetic
- the alert would create noise rather than action

## Alert Format
When attention is needed, use this exact shape:
- **Type:** priority | blocker | career | decision | drift | memory
- **Issue:** one sentence
- **Why it matters:** one sentence
- **Next move:** one concrete action

## Alert Quality Rules
- one strong alert is better than several weak alerts
- alerts should point to action, not just observation
- alerts should reference the relevant operational issue, not narrate the checking process
- do not dump status; report only what requires intervention

## Operating Bias
Heartbeat should optimize for:
- momentum
- focus
- clarity
- follow-through

Heartbeat should avoid:
- chatter
- repetitive reminders
- exhaustive reporting
- low-signal interventions
