# CURRENT.md

## Current State Record
- **id:** current_state_2026_04_30
- **updated_at:** 2026-05-02T07:13:00-05:00
- **system_phase:** Cockpit + Runtime Hardening
- **system_status:** IDLE
- **current_step:** System is paused cleanly. Gateway health is confirmed on loopback, the active model is `openai-codex/gpt-5.4`, there are no active execution processes, and the workspace is safe to shut down.
- **confidence_level:** high

## State Summary
- **state_summary:** JT7 is still in `Cockpit + Runtime Hardening`, but the runtime loop is now materially stronger: the live JT7 chain completes end-to-end again, Gmail and Calendar ingestion no longer die on malformed `gog` invocation paths, the `ReviewQueue` read path now falls back cleanly to the local mirror when the live sheet tab contract is missing, staging-to-canonical writeback rules are stricter around off-target roles, missing source links, and same-company collisions, and auto-sync commit scope is narrowed to operational artifacts instead of sweeping browser-profile noise. The remaining weakness is post-run persistence hygiene, not core chain execution.

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
  - post-run persistence still leaves dirty runtime/browser files in the worktree even when auto-sync commits the right subset
  - Indeed remains partially blocked by anti-bot flow, so one board source is still degraded
  - Drive mirror behavior currently creates snapshot copies rather than refreshing a single canonical mirrored file, so mirror sprawl is growing

## Open Questions
- **open_questions:**
  - what filters should gate direct-board imports so only Jonathon-fit roles land in the apply set by default?
  - what canonical Drive update mechanism should replace duplicate file uploads?
  - which remaining docs still materially misrepresent the live JT7 app/runtime state?
  - what standing cross-bot checkpoint rule should govern when JobOps hands off durable updates to Platform for final commit/push?

## Required Next Moves
- **required_next_moves:**
  - trace why `jt7_pass_log.jsonl`, `jt7_scheduler.json`, new reports, and browser-side artifacts still leave the worktree dirty after a successful run
  - validate the hardened scheduler/catch-up path on the next real resume cycle now that the chain succeeds again
  - validate the new UI→runtime promotion bridge during normal operator use now that both browser promote and merge proofs pass cleanly
  - connect the new staging writeback planner to real Sheets-side create/update behavior with safe dry-run and apply modes
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
