# JT7 (for hiring teams)

JT7 is Jonathon Thomason’s self-directed AI-operated job search system.

It is both:
- a working personal operating system for managing a modern job search
- a product and systems-thinking artifact that shows how Jonathon approaches workflow design, operational clarity, and real-world execution

## What this demonstrates

JT7 is not just a concept deck or design exercise.
It is a live system built to:
- ingest job-search signals from Gmail and Calendar
- classify and reconcile those signals against a structured tracker
- persist operational state across Google Sheets, local artifacts, and git history
- surface the highest-priority next actions in a calm operator UI
- reduce cognitive overhead in a fragmented, multi-source workflow

In practical terms, it demonstrates Jonathon’s ability to:
- frame messy workflows as systems
- define clean operating models
- design around traceability and decision quality
- move from architecture to working implementation
- balance product thinking with execution discipline

## Why it matters

Most job-search tooling is fragmented.
Signals live in email, scheduling lives in calendar, trackers drift, and next steps become unclear.

JT7 treats the problem like an operating system problem:
- separate evidence from truth
- preserve state cleanly
- make action visible
- prevent context loss
- design the interface around decision-making, not noise

That framing reflects how Jonathon thinks about product design more broadly:
- systems over isolated screens
- clarity over feature sprawl
- workflow integrity over superficial polish
- practical execution over abstract strategy alone

## Current system shape

JT7 currently operates across three connected layers.

### 1. Logic layer
Markdown defines the rules, contracts, and operating model.

### 2. Runtime layer
Python executes ingestion, reconciliation, persistence, and reporting.

### 3. Application layer
A React/Vite interface renders the operator surface for execution.

## Live operating model

Current source-of-truth model:
- **Google Sheets** for live tracker truth
- **local structured artifacts** for mirrors and runtime state
- **git/GitHub** for versioned history
- **Google Drive** as a mirrored access layer for important documents

Current execution chain includes:
- email signal scan
- calendar signal scan
- job-board signal scan
- signal classification
- pipeline reconciliation
- pipeline update
- local mirror sync
- git commit sync
- action generation
- priority surfacing
- pass logging

## What this says about Jonathon

This project reflects a product designer who is comfortable working across:
- product strategy
- systems architecture
- information design
- workflow modeling
- implementation-adjacent execution
- operational rigor

It also reflects a bias toward building real things, not just describing them.

## How to read this project

If you are reviewing JT7 as part of Jonathon’s candidacy, the useful lens is:
- how the system is framed
- how ambiguity is turned into structure
- how data/state boundaries are defined
- how the workflow was made operational
- how the implementation preserves product intent

This is best understood as a working product-thinking artifact, not just a code sample and not just a design artifact.

## Primary repo README

For the operator-facing technical overview, see:
- `README.md`

That file is the better reference for:
- runtime details
- local paths
- task-chain execution
- tracker/storage mechanics

## Summary

JT7 is a concrete example of Jonathon Thomason designing and building a system that:
- structures a complex workflow
- preserves truth across tools
- surfaces action clearly
- reduces user cognitive load
- bridges product thinking and actual execution
