# Signal Verification SOP

## Audience
Operations, future JobOps behavior, engineering reference

## Purpose
Define the standard operating procedure for moving a signal from intake into trusted opportunity state or safely resolving it without contamination.

## Core Rule
Signals are untrusted on arrival.
They must be reviewed before entering the trusted dashboard/pipeline.

## Inputs
Signals may originate from:
- recruiter email
- job-board listing
- application confirmation
- application update
- interview signal
- manual operator entry
- other supported ingestion sources

## Verification Outcomes
A signal review must end in one of these dispositions:
- Confirm as new opportunity
- Link to existing opportunity
- Dismiss as noise
- Mark duplicate
- Defer for later review
- Escalate as parser/system issue

## Procedure
### 1. Inspect the signal
Review:
- source/channel
- summary and raw excerpt
- inferred company
- inferred role
- inferred contact
- inferred event type
- evidence/source links
- duplicate candidate if present

### 2. Determine whether the signal is operationally real
Ask:
- Is this a valid job-search opportunity or update?
- Is it new or already represented by an existing opportunity?
- Is the source reliable enough to promote?
- Is the information too ambiguous to trust yet?

### 3. Choose a disposition
#### Confirm as new opportunity
Use when the signal clearly represents a real new opportunity.

Required effects:
- create trusted opportunity state
- carry over verified fields and source links
- optionally create contact and next action
- create event record(s)

#### Link to existing opportunity
Use when the signal updates an already tracked opportunity.

Required effects:
- link signal to the existing opportunity
- update trusted state where appropriate
- refresh activity history
- create event record(s)

#### Dismiss as noise
Use when the signal is irrelevant, low-value, or not part of the intended operating model.

Required effects:
- mark signal dismissed
- keep audit trail
- do not create trusted opportunity state

#### Mark duplicate
Use when the signal appears to represent an already tracked item without adding distinct value.

Required effects:
- mark duplicate state
- link duplicate target if known
- keep event history
- do not create new opportunity state

#### Defer
Use when the signal may matter but should not yet be trusted or resolved.

Required effects:
- keep in a deferred review state
- preserve event history
- avoid promotion into trusted dashboard state

#### Escalate
Use when the signal reveals a parsing/system problem or ambiguity that should be corrected upstream.

Required effects:
- mark escalated state
- preserve source evidence
- record reason for escalation
- avoid promotion until resolved

## Event Logging Requirement
Every meaningful review action must create an event record containing:
- action type
- actor
- timestamp
- prior state
- new state
- linked IDs where applicable
- reason/note when available

## Source Link Requirement
Verification should preserve direct access to:
- original job posting
- application URL when present
- email/thread evidence
- recruiter profile/context when present
- internal opportunity detail/tracker location when created

## Quality Rules
- do not promote ambiguous items into trusted dashboard state just to keep flow moving
- do not bury source links in notes when structured fields exist
- do not mutate trusted state without corresponding event history
- prefer defer/escalate over false confidence

## Output Rule
The dashboard/pipeline should contain trusted opportunities only.
Raw or unresolved signals belong in the Review Queue, not the main operational surface.
