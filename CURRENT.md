# CURRENT.md

## Current State Record
- **id:** current_state_2026_04_30
- **updated_at:** 2026-05-02T15:04:00-05:00
- **system_phase:** Cockpit + Runtime Hardening
- **system_status:** IDLE
- **current_step:** System is paused and safe to shut down. Gateway health is confirmed on loopback, the active model is `openai-codex/gpt-5.4`, no active executions are running, and the newest blocker is a failed 12:30 catch-up run caused by missing `gog` Sheets auth for `jonathon.thomason@gmail.com`.
- **confidence_level:** high

## State Summary
- **state_summary:** JT7 remains in `Cockpit + Runtime Hardening`. This session materially sharpened the product contract: application-readiness is now explicit across location fit, ATS optimization basis, and differentiation highlights; onboarding now seeds those downstream requirements; and the state model now distinguishes `Review`, `Staging`, `Mismatch Hold`, `Apply-Ready`, and `Submit-Ready` plus a resume-transformation layer. No meaningful UI/product demo was built. The most important runtime regression discovered at shutdown is a real 12:30 catch-up failure: the scheduler resumed, attempted a live Sheets read, and failed because `gog` no longer had Sheets auth for `jonathon.thomason@gmail.com`. The system is stable enough to pause, but not healthy enough to trust unattended runs until auth is restored and application-readiness is enforced structurally rather than only in docs.

## Top Priorities
- **top_priorities:**
  - restore `gog` Sheets auth so scheduled JT7 runs can be trusted again
  - turn the new application-readiness contract into a canonical schema and state model the UI/runtime can enforce
  - implement a real staging-to-canonical promotion and merge model so trusted tracker updates stop depending on ad hoc local behavior
  - tighten intake filtering and ranking against Jonathon’s search requirements so weak-fit backlog stops forming upstream
  - keep cockpit/runtime persistence consistent across Sheets, local mirror, git, and Drive-accessible artifacts

## Active Risks
- **active_risks:**
  - low-quality Gmail signals and broad direct-board imports can still create weak review items or cold jobs if filtering and promotion rules remain too loose
  - application-readiness logic now exists in docs, but mismatch between prose, future schema fields, and runtime behavior could create false `apply-ready` confidence if not enforced structurally
  - scheduled runtime trust is degraded because the latest catch-up run failed on missing `gog` Sheets auth
  - Indeed remains blocked by anti-bot flow, leaving one source partially inaccessible
  - some legacy docs and filenames still reflect older platform assumptions instead of the current cockpit/runtime reality
  - gateway is healthy but still not loaded as a clean LaunchAgent service, so lifecycle transitions remain fragile
  - post-run persistence still leaves dirty runtime/browser files in the worktree even when auto-sync commits the right subset
  - Indeed remains partially blocked by anti-bot flow, so one board source is still degraded
  - Drive mirror behavior currently creates snapshot copies rather than refreshing a single canonical mirrored file, so mirror sprawl is growing

## Open Questions
- **open_questions:**
  - why did `gog` Sheets auth disappear for `jonathon.thomason@gmail.com` between the last successful run and the 12:30 catch-up run?
  - what exact canonical schema fields should represent location fit, ATS basis, differentiation highlights, optimization brief, and tailored artifact state?
  - what filters should gate direct-board imports so only Jonathon-fit roles land in the apply set by default?
  - what canonical Drive update mechanism should replace duplicate file uploads?

## Required Next Moves
- **required_next_moves:**
  - restore and verify `gog` Sheets auth for `jonathon.thomason@gmail.com`, then rerun the smallest possible live read before trusting the scheduler again
  - define the canonical schema fields and state transitions for `Mismatch Hold`, `Apply-Ready`, `Submit-Ready`, optimization brief, and tailored artifact state
  - trace why `jt7_pass_log.jsonl`, `jt7_scheduler.json`, new reports, and browser-side artifacts still leave the worktree dirty after a successful run
  - validate the new UI→runtime promotion bridge during normal operator use now that both browser promote and merge proofs pass cleanly
  - connect the new staging writeback planner to real Sheets-side create/update behavior with safe dry-run and apply modes
  - normalize Drive mirror behavior so updated docs refresh canonical mirrored copies rather than creating duplicates

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
