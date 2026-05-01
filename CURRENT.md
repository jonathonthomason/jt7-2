# CURRENT.md

## Current State Record
- **id:** current_state_2026_04_30
- **updated_at:** 2026-05-01T15:07:00-05:00
- **system_phase:** Cockpit + Runtime Hardening
- **system_status:** IDLE
- **current_step:** System is paused cleanly after implementing resume-time catch-up semantics for the JT7 scheduler and persisting the new scheduler contract. Gateway is healthy on loopback, the active model is `openai-codex/gpt-5.4`, no active executions are running, and the workspace is safe to shut down
- **confidence_level:** high

## State Summary
- **state_summary:** JT7 has a real Review Queue cockpit surface in `job-search-ui`, a live JobOps bot lane with dedicated routing and operating memory, and an explicit staging-intake UI that scores fit, auto-gates obvious off-target imports, and supports duplicate-safe local merge behavior for broad direct-board intake. A runtime-side planner defines tracker-facing create/merge/hold/reject decisions while filtering duplicate checks against canonical jobs only. This session added resume-time catch-up semantics (`single-pass-on-resume`) to the scheduler and persisted scheduler metadata for `scheduledFor`, `triggerMode`, and missed slots. The JT7 chain’s `gog` binary resolution remains stabilized to an absolute path. Read-only Sheets/Gmail/Calendar access is verified, but the specific 2026-05-01 08:30 scheduler-only failure still lacks root-cause explanation. The system is intentionally paused in an IDLE shutdown-safe state.

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
  - scheduler now has resume-time catch-up semantics, but the specific 2026-05-01 morning failure still needs root-cause explanation because direct live `gog sheets get Jobs!A1:Z1000` succeeds now
  - Drive mirror behavior currently uploads fresh copies rather than updating a single canonical mirrored doc in place

## Open Questions
- **open_questions:**
  - what filters should gate direct-board imports so only Jonathon-fit roles land in the apply set by default?
  - what canonical Drive update mechanism should replace duplicate file uploads?
  - which remaining docs still materially misrepresent the live JT7 app/runtime state?
  - what standing cross-bot checkpoint rule should govern when JobOps hands off durable updates to Platform for final commit/push?

## Required Next Moves
- **required_next_moves:**
  - inspect the 2026-05-01 08:30 scheduler-only failure path now that resume-time catch-up semantics are in place
  - validate the new single-pass-on-resume scheduler behavior against the next real resume/use cycle
  - connect the new staging writeback planner to real Sheets-side create/update behavior with safe dry-run and apply modes
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
