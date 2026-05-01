# CURRENT.md

## Current State Record
- **id:** current_state_2026_04_30
- **updated_at:** 2026-04-30T22:00:00-05:00
- **system_phase:** Cockpit + Runtime Hardening
- **current_step:** Top-3 execution stack has been worked through; staging intake now supports duplicate-safe merge vs promote decisions and auto-gates obvious off-target imports; one real JobOps loop was validated successfully from live output
- **confidence_level:** medium_high

## State Summary
- **state_summary:** JT7 now has a real Review Queue cockpit surface in `job-search-ui`, a live JobOps bot lane with dedicated routing and operating memory, and an explicit staging-intake UI that scores fit, auto-gates obvious off-target imports, and supports duplicate-safe local merge behavior for broad direct-board intake. A live JobOps output sample confirmed good lane discipline and useful ranked staging judgments. The main remaining gaps are Indeed access and true canonical promotion/writeback behavior beyond local UI state.

## Top Priorities
- **top_priorities:**
  - implement a real staging-to-canonical promotion and merge model so trusted tracker updates stop depending on ad hoc local behavior
  - tighten intake filtering and ranking against Jonathon’s search requirements so weak-fit backlog stops forming upstream
  - validate one real JobOps operating loop and tighten its instructions from actual use
  - keep cockpit/runtime persistence consistent across Sheets, local mirror, git, and Drive-accessible artifacts
  - keep cross-bot checkpoint rules clean so Platform remains the final commit/push authority

## Active Risks
- **active_risks:**
  - low-quality Gmail signals and broad direct-board imports can still create weak review items or cold jobs if filtering and promotion rules remain too loose
  - Indeed remains blocked by anti-bot flow, leaving one source partially inaccessible
  - some legacy docs and filenames still reflect older platform assumptions instead of the current cockpit/runtime reality
  - gateway is reachable but still not loaded as a clean LaunchAgent service, so lifecycle transitions remain fragile
  - Drive mirror behavior currently uploads fresh copies rather than updating a single canonical mirrored doc in place

## Open Questions
- **open_questions:**
  - what filters should gate direct-board imports so only Jonathon-fit roles land in the apply set by default?
  - what canonical Drive update mechanism should replace duplicate file uploads?
  - which remaining docs still materially misrepresent the live JT7 app/runtime state?
  - what standing cross-bot checkpoint rule should govern when JobOps hands off durable updates to Platform for final commit/push?

## Required Next Moves
- **required_next_moves:**
  - move the local promotion/merge model into real canonical tracker writeback behavior
  - convert the validated JobOps shortlist format into a standing durable JobOps instruction if it continues to prove useful
  - normalize Drive mirror behavior so updated docs refresh canonical mirrored copies rather than creating duplicates
  - continue keeping cockpit/runtime docs and storage rules aligned with the actual live JT7 execution path

## Related Files
- **related_files:**
  - ROADMAP.md
  - ops/focus.md
  - DECISIONS.md
  - docs/storage-rules.md
  - job-search-ui/docs/local-git-drive-rules.md
  - job-search-ui/docs/review-queue-build-brief.md
  - docs/jt7-job-ops-bot-agent-spec.md
  - docs/direct-board-import-policy.md
  - docs/jobops-rollout-checklist.md
  - docs/jobops-telegram-config-snippet.jsonc
  - agents/jobops/
  - job-search-ui/scripts/run_jt7_chain.py
  - job-search-ui/scripts/import_direct_board_jobs.py
  - job-search-ui/runtime/jt7_tasks.json
  - job-search-ui/runtime/jt7_scheduler.json
