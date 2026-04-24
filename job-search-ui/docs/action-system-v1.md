# Action System V1

## Purpose
Turn JT7 Actions from generated reminders into a truthful operational layer for Today's Plan.

## V1 Truth Model
JT7 Action System V1 is built on the existing runtime spine:
- Signals
- Jobs
- Recruiters
- Actions
- TaskRuns

No new backend architecture is introduced in V1.
The goal is to normalize behavior around the data that already exists.

## Canonical Action States
V1 uses four states:
- `open`
- `waiting`
- `done`
- `blocked`

## State Meanings
### open
The operator should act now or soon.
Examples:
- recruiter reply needs response
- follow-up should be sent
- job should be reviewed or applied to
- interview prep is needed

### waiting
The system is waiting on an external response or time-based checkpoint.
Examples:
- application submitted, waiting for response
- recruiter was answered, waiting on next reply
- interview is scheduled and no immediate prep remains

### done
The action has been completed and should move to historical/completed views.

### blocked
The action cannot safely proceed without review or missing information.
Examples:
- review-required signal blocking job creation
- ambiguous signal-to-job mapping
- incomplete company/role extraction

## V1 Mapping Rules
### Signal-driven blocked actions
If a signal is preserved but cannot safely create or update a Job, it should surface as a blocked review action.

### Signal-linked job actions
If a signal links cleanly to a Job and a next step exists, it should surface as an open action.

### Existing Actions rows
Existing `Actions` rows remain valid V1 inputs.
Their `status` values map into the canonical action state model when possible.

## Today's Plan Contract
Today's Plan should read from the action-state-aware selector layer and surface:
- Next Best Action
- supporting open/blocked actions
- completed today
- waiting (next pass)
- recent signals
- latest task run

## V1 Constraints
- do not imply bidirectional action editing from the UI yet
- do not imply completed/waiting persistence flows that do not exist yet
- do not create new domains before the current action truth is stable

## Next Steps After V1
1. persist action state transitions from the UI/runtime
2. surface waiting explicitly in the homepage
3. add completed-today persistence
4. align runtime action generation and action resolution rules
