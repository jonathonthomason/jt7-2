# JT7 — Signal System

## Definition
Signal = any new or updated info requiring awareness or action

## Categories
COMMUNICATION
OPPORTUNITY
APPLICATION
SYSTEM

## Sources
- LinkedIn
- Indeed
- Wellfound
- Built In
- YC Jobs
- Company sites
- Recruiter email
- Manual

## Signal Fields
- Type
- Source
- Timestamp
- Priority
- Company
- Role
- Contact
- Summary
- Why it matters
- Actions

## Job Signals
Actions:
- Review
- Save
- Apply
- Dismiss

## Application Signals
Actions:
- View
- Update status
- Follow up
- Log note

## Priority
High:
- recruiter reply
- interview
- status change

Medium:
- good job match
- follow-up

Low:
- passive signal

## Cockpit Verification & Action Logging
### Verification Flow
Signals are untrusted on arrival.
They must be reviewed in the operator cockpit before entering trusted opportunity state.

Verification outcomes:
- Confirm as new opportunity
- Link to existing opportunity
- Dismiss as noise
- Mark duplicate
- Defer for later review
- Escalate as parser issue

### Action Logging Requirement
Every meaningful cockpit action must create:
- a current-state update when applicable
- an event record capturing the action

Event records should preserve:
- action type
- timestamp
- actor
- prior state
- new state
- reason / note when available

### Purpose
This action history is required so JT7 can later support intelligence use cases including:
- parser improvement
- source quality scoring
- recruiter quality patterns
- opportunity conversion analysis
- recommendation generation
- stall / risk detection

## Rule
Every signal must answer:
- What happened?
- Why it matters?
- What to do next?