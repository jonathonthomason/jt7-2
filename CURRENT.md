# CURRENT.md

## Current State Record
- **id:** current_state_2026_04_22
- **updated_at:** 2026-04-22T21:04:00-05:00
- **system_phase:** Execution Layer Hardening
- **current_step:** improve parsing accuracy, reduce false positives, and keep runtime/docs aligned to live JT7 behavior
- **confidence_level:** medium_high

## State Summary
- **state_summary:** JT7 now performs real Gmail ingestion, runtime classification, probabilistic matching, Sheets CRUD, TaskRuns logging, local mirror sync, git sync, and Drive-aware documentation maintenance. The main remaining gap is parsing precision, not missing execution.

## Top Priorities
- **top_priorities:**
  - improve parsing accuracy so newsletter and digest noise stop polluting the tracker
  - keep runtime persistence consistent across Sheets, local mirror, git, and Drive-accessible artifacts
  - keep system requirements and docs current with actual JT7 runtime behavior

## Active Risks
- **active_risks:**
  - low-quality Gmail signals can still create or reinforce weak tracker rows if source filtering remains too loose
  - some legacy docs and filenames still reflect older platform assumptions instead of the current execution-layer reality
  - Drive mirror behavior currently uploads fresh copies rather than updating a single canonical mirrored doc in place
  - job-board adapters beyond Gmail-delivered board emails remain only partially implemented

## Open Questions
- **open_questions:**
  - which existing low-quality jobs/signals/actions should be cleaned from the tracker after the looser earlier parsing passes?
  - what canonical Drive update mechanism should replace duplicate file uploads?
  - which remaining docs still materially misrepresent the live JT7 app/runtime state?

## Required Next Moves
- **required_next_moves:**
  - tighten source-specific Gmail filtering for newsletters, digests, and reply notifications unless they contain a valid role/company pattern
  - improve recruiter/company/job extraction so generic sender artifacts stop becoming review noise or weak entities
  - normalize Drive mirror behavior so updated docs refresh canonical mirrored copies rather than creating duplicates
  - continue keeping runtime docs and storage rules aligned with the actual live JT7 execution path

## Related Files
- **related_files:**
  - ROADMAP.md
  - ops/focus.md
  - DECISIONS.md
  - docs/storage-rules.md
  - job-search-ui/docs/local-git-drive-rules.md
  - job-search-ui/scripts/run_jt7_chain.py
  - job-search-ui/runtime/jt7_tasks.json
  - job-search-ui/runtime/jt7_scheduler.json
