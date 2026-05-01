# CURRENT.md

## Current State Record
- **id:** current_state_2026_04_30
- **updated_at:** 2026-05-01T16:34:48-05:00
- **system_phase:** Cockpit + Runtime Hardening
- **system_status:** IDLE
- **current_step:** System is paused cleanly. Gateway health is confirmed on loopback, the active model is `openai-codex/gpt-5.4`, local UI/API execution processes have been stopped, no active subagents are running, and the workspace is safe to shut down.
- **confidence_level:** high

## State Summary
- **state_summary:** JT7 still sits in `Cockpit + Runtime Hardening`, but it is materially further along inside that phase. This session added resume-time catch-up semantics (`single-pass-on-resume`) to the scheduler, hardened the JT7 chain’s Sheets path with explicit `gog` account + `--no-input` usage and better stderr capture, proved two live staging→canonical create writebacks into Google Sheets `Jobs`, added a thin local API bridge so UI promotion/merge actions can hit the real runtime apply path, surfaced writeback success/failure more clearly in the staging UI, refreshed local mirrors, pushed the intentional code/evidence set to git, and uploaded a Drive snapshot of those artifacts. What did not happen: no real click-path operator audit yet, no real merge writeback proven in normal use, no true root cause found for the 2026-05-01 08:30 scheduler failure, and Drive mirroring still creates snapshot copies instead of updating a single canonical mirrored file in place.

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
  - gateway is healthy but still not loaded as a clean LaunchAgent service, so lifecycle transitions remain fragile
  - scheduler now has resume-time catch-up semantics, but the specific 2026-05-01 morning failure is still not root-caused; it is only narrowed to a transient or opaque `gog` exit-2 condition
  - Drive mirror behavior currently creates snapshot copies rather than refreshing a single canonical mirrored file, so mirror sprawl is growing
  - the UI→runtime bridge is proven technically, but not yet proven through a normal operator click audit

## Open Questions
- **open_questions:**
  - what filters should gate direct-board imports so only Jonathon-fit roles land in the apply set by default?
  - what canonical Drive update mechanism should replace duplicate file uploads?
  - which remaining docs still materially misrepresent the live JT7 app/runtime state?
  - what standing cross-bot checkpoint rule should govern when JobOps hands off durable updates to Platform for final commit/push?

## Required Next Moves
- **required_next_moves:**
  - validate the hardened `gog` invocation and new single-pass-on-resume scheduler behavior against the next real resume/use cycle
  - validate the new UI→runtime promotion bridge during normal operator use and prove at least one normal click-driven promotion path end-to-end
  - prove the staging writeback merge path against a real duplicate when one naturally appears or through a controlled UI-safe harness
  - if another scheduler failure occurs, use the improved stderr capture to isolate exact `gog` failure cause immediately
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
