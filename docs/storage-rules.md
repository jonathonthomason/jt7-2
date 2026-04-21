# Storage Rules

## Purpose
Canonical storage rules for JT7 system logic.

This file defines where different classes of information should live and which store is the source of truth.

---

## Core Rule
Use the right system for the right job.
Do not collapse operational tracking, editable documents, and versioned system logic into one storage layer.

---

## Source of Truth Rules

### Markdown docs
- canonical location: local workspace + GitHub
- use for:
  - architecture docs
  - workflows
  - schemas
  - persona references
  - system rules
  - operating notes that benefit from version control
- why:
  - reliable version history
  - clean diffs
  - safer maintenance
  - easier structured updates

### Google Drive
- role: convenience mirror and access layer
- use for:
  - mirrored copies of important markdown docs
  - human-accessible exports
  - lightweight reference access
- not canonical for markdown system logic
- why:
  - easier manual access
  - easier sharing
  - useful as a convenience layer, not a governance layer

### Google Sheets
- canonical location for live tracker data
- use for:
  - job tracking boards
  - operational lists
  - status tracking
  - row-based workflow state
- why:
  - better for live structured tracking
  - easier operational mutation
  - better fit for job-search workflow execution

---

## Practical Rules
- keep markdown canonical in workspace/GitHub
- mirror selected markdown docs to Google Drive when convenient or useful
- keep live operational tracker state in Google Sheets
- do not treat Drive copies as canonical when a workspace/GitHub markdown file exists
- do not treat markdown docs as the live operational source of truth when the state belongs in Sheets

---

## Current System Decision
- markdown source of truth: workspace/GitHub
- markdown mirror layer: Google Drive
- live tracker source of truth: Google Sheets

---

## Maintenance Rule
If storage behavior changes, update this file before changing operating behavior so the system logic stays explicit.
