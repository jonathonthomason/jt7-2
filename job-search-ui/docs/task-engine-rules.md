# Task Engine Rules

## Purpose
Canonical runtime task-engine rules for the JT7 job-search system.

This file defines the live scheduled task system, full-chain execution model, and tracker sync behavior.

---

## Core Rule
All behavior must run as persistent tasks over structured task objects.

The system must not rely on logic files alone.
It must maintain:
- live scheduled runtime jobs
- persisted task instances
- lastRunAt / nextRunAt state
- full task chaining
- tracker sync enforcement

---

## Scheduled Runtime
Timezone:
- America/Chicago

Daily runs:
- Morning: 8:30 AM
- Midday: 12:30 PM
- Evening: 6:00 PM

Each scheduled run must execute the full chain.

---

## Full Chain
- EMAIL_SIGNAL_SCAN
- CALENDAR_SIGNAL_SCAN
- JOB_BOARD_SIGNAL_SCAN
- SIGNAL_CLASSIFICATION
- PIPELINE_STATE_SYNC
- PIPELINE_UPDATE
- LOCAL_MIRROR_SYNC
- GIT_COMMIT_SYNC
- ACTION_GENERATION
- PRIORITY_SURFACING
- PASS_LOGGER

If a task fails:
- log the failure
- preserve chain state
- do not silently skip
- do not falsely claim success

---

## Required Task State
Each task instance must maintain:
- taskId
- taskName
- isEnabled
- cadence
- lastRunAt
- nextRunAt
- lastStatus
- lastSummary

---

## Tracker Persistence Rule
Tracker is a 3-layer synchronized system:

1. Google Sheets
   - live operational source of truth
2. local workspace mirror
   - structured mirror/export for backup, runtime inspection, and recovery
3. git/GitHub
   - versioned history of local mirror changes

### CRUD enforcement
Every meaningful tracker CRUD operation must:
- update Google Sheets first
- update local mirror second
- commit mirror changes to git third when data changed

Sheets remains authoritative live operational truth.

---

## Task Modules
### EMAIL_SIGNAL_SCAN
- reads Gmail for job-related signals
- captures recruiter replies, confirmations, rejections, interview scheduling, reschedules, cancellations, follow-ups, hiring-manager communication, and application receipts
- applies Gmail-driven tracking rules from `docs/gmail-driven-tracking-rules.md`
- outputs to Signals and downstream tracker writes when allowed

### CALENDAR_SIGNAL_SCAN
- reads calendar for interviews, recruiter calls, and follow-ups
- outputs events/signals

### JOB_BOARD_SIGNAL_SCAN
- ingests job-board-originated signals and application data from currently available sources
- outputs to Jobs and Signals

### SIGNAL_CLASSIFICATION
- classifies raw signals into structured meaning
- outputs classification, inferred stage, confidence, and summary

### PIPELINE_STATE_SYNC
- reconciles signals, events, and jobs
- outputs proposed updates, status changes, and action candidates

### PIPELINE_UPDATE
- applies allowed updates to Jobs, Recruiters, Competition, Signals, Actions, TaskRuns, and Lookup when required

### LOCAL_MIRROR_SYNC
- exports tracker state locally as CSV/JSON mirror

### GIT_COMMIT_SYNC
- commits local mirror changes when meaningful updates occurred

### ACTION_GENERATION
- generates next-best actions for operator

### PRIORITY_SURFACING
- ranks urgent and important items for operator-facing views

### PASS_LOGGER
- logs each chain run, summary, timestamps, records touched, errors, and next run state

---

## Success Rule
System is healthy when:
- new signals create or update tracker records automatically
- interviews are captured reliably
- local mirror updates after meaningful CRUD
- git commits occur after meaningful mirror changes
- every pass is logged with persisted task state
