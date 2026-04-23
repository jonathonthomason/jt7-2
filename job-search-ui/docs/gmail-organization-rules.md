# Gmail Organization Rules

## Purpose
Canonical Gmail organization and cleanup logic for JT7 daily execution.

This file defines the label system, thread state model, daily cleanup behavior, follow-up rules, interview handling, and tracker-sync behavior.

---

## Gmail Label System
Required labels:
- JT7/Action
- JT7/Waiting
- JT7/Interview
- JT7/Applied
- JT7/Archive
- JT7/Ignore

Optional labels enabled:
- JT7/High Priority
- JT7/Follow-Up

---

## State Model
Every job-related email thread must exist in exactly one state:
- Action
- Waiting
- Interview
- Applied
- Archive
- Ignore

No job-related thread should remain unlabeled or in conflicting states.

---

## Daily Gmail Task Behavior
For each scheduled run:
1. scan Gmail inbox for new emails since last run
2. identify job-related emails
3. classify each email
4. apply or update thread-level labels
5. enforce state transitions
6. update JT7 tracker
7. generate actions
8. archive processed threads so inbox remains low-noise

---

## Classification Rules
- recruiter outreach -> JT7/Action
- interview scheduled -> JT7/Interview
- rejection -> JT7/Archive
- application confirmation -> JT7/Applied
- reply received -> JT7/Action
- no action required -> JT7/Waiting or JT7/Archive

---

## State Transition Rules
- if user has replied -> move to JT7/Waiting
- if new reply received -> move to JT7/Action
- if process ends -> move to JT7/Archive
- remove outdated labels when state changes

---

## Follow-Up Rules
For threads in JT7/Waiting:
- detect no response after 3 to 5 days
- move thread back to JT7/Action
- apply JT7/Follow-Up when relevant
- generate follow-up action in tracker

---

## Interview Rules
For threads in JT7/Interview:
- detect upcoming interview events
- create prep actions
- ensure tracker is updated with event details
- elevate high-priority interview items when timing is near

---

## Tracker Sync Rule
When Gmail processing creates meaningful tracker CRUD:
1. update Google Sheets first
2. sync local mirror second
3. commit local mirror changes to git third when data changed

Gmail organization must feed persistent system state, not just labels.

---

## Logging Rule
Each Gmail run must log:
- emails processed
- labels applied or changed
- tracker updates
- actions created
- follow-ups triggered
- errors

Logs should be written into TaskRuns or the scheduler logging structure.

---

## Scheduled Execution Rule
This Gmail organization task runs as part of the JT7 scheduled daily chain:
- Morning
- Midday
- Evening

It belongs inside:
- EMAIL_SIGNAL_SCAN
- SIGNAL_CLASSIFICATION
- PIPELINE_UPDATE
- ACTION_GENERATION
- PASS_LOGGER

---

## Success Rule
System is healthy when:
- inbox remains clean and low-noise
- job-related emails are labeled and stateful
- important threads are not lost or untracked
- tracker stays in sync with Gmail activity
- follow-ups are automatically surfaced
- operator can immediately see what needs action, what is pending, and what is complete
