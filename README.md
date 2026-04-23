# JT7

JT7 is Jonathon Thomason’s AI-operated job search and execution system.

## Purpose
JT7 exists to:
- run a structured job-search operating system
- maintain pipeline truth across Gmail, Calendar, job boards, and tracker data
- reduce cognitive load through scheduled execution, persistent state, and clear operator surfaces

## Core System Model
JT7 is organized as three connected layers:

### 1. Logic layer
Markdown files define system rules, task logic, tracker behavior, storage rules, Gmail ingestion rules, and project recenter state.

Key areas:
- `job-search-ui/docs/`
- root control files such as `MISSION.md`, `CURRENT.md`, `MEMORY.md`, and related operating docs

### 2. Runtime layer
Executable scripts and persisted runtime state drive the scheduled task system.

Key areas:
- `job-search-ui/scripts/`
- `job-search-ui/runtime/`
- `job-search-ui/data_mirror/`

### 3. Application layer
The React/Vite app provides the local UI shell and operator-facing surface.

Key area:
- `job-search-ui/`

## Source of Truth Model
- **Google Sheets** = live operational tracker truth
- **local workspace** = runtime + local structured mirror
- **git/GitHub** = versioned history of local files and mirrors
- **Google Drive** = mirrored access layer for important docs

## Current Tracker
Live tracker sheet:
- `JT7_Job_Tracker_Source_of_Truth`

Current tabs:
- Jobs
- Recruiters
- Competition
- Signals
- Actions
- TaskRuns
- Lookup

## Scheduled Task System
JT7 currently runs on a scheduled chain model with these core tasks:
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

Scheduled local run times:
- 8:30 AM America/Chicago
- 12:30 PM America/Chicago
- 6:00 PM America/Chicago

## Important Paths
- Root project: `/Users/jtemp/.openclaw/workspace`
- App: `/Users/jtemp/.openclaw/workspace/job-search-ui`
- App recenter file: `/Users/jtemp/.openclaw/workspace/job-search-ui/PROJECT_RECENTER.md`
- Runtime task state: `/Users/jtemp/.openclaw/workspace/job-search-ui/runtime/jt7_tasks.json`
- Runtime schedule state: `/Users/jtemp/.openclaw/workspace/job-search-ui/runtime/jt7_scheduler.json`
- Runtime chain runner: `/Users/jtemp/.openclaw/workspace/job-search-ui/scripts/run_jt7_chain.py`

## Quick Start
### Run the app
```bash
cd /Users/jtemp/.openclaw/workspace/job-search-ui
npm install
npm run dev
```

### Run the JT7 task chain manually
```bash
cd /Users/jtemp/.openclaw/workspace/job-search-ui
/usr/bin/python3 /Users/jtemp/.openclaw/workspace/job-search-ui/scripts/run_jt7_chain.py
```

### Inspect scheduler state
```bash
cat /Users/jtemp/.openclaw/workspace/job-search-ui/runtime/jt7_scheduler.json
```

### Inspect task state
```bash
cat /Users/jtemp/.openclaw/workspace/job-search-ui/runtime/jt7_tasks.json
```

## Notes
This repo contains both product/app work and system logic/runtime work.
The job-search app is the primary active implementation surface right now.
