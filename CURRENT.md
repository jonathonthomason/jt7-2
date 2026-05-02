# CURRENT.md

## Current State Record
- **id:** current_state_2026_04_30
- **updated_at:** 2026-05-02T12:40:00-05:00
- **system_phase:** Cockpit + Runtime Hardening
- **system_status:** IDLE
- **current_step:** Core runtime hardening remains in place, and the product spec layer now includes an explicit application-readiness gate with `Mismatch Hold`, `Apply-Ready`, and `Submit-Ready` states. The next design/build step is to turn those prose rules into a canonical schema and UI/runtime enforcement model.
- **confidence_level:** high

## State Summary
- **state_summary:** JT7 is still in `Cockpit + Runtime Hardening`, but the runtime loop is now materially stronger and the product model is sharper: the live JT7 chain completes end-to-end again, Gmail and Calendar ingestion no longer die on malformed `gog` invocation paths, the `ReviewQueue` read path now falls back cleanly to the local mirror when the live sheet tab contract is missing, staging-to-canonical writeback rules are stricter around off-target roles, missing source links, and same-company collisions, and the architecture/docs now define an explicit application-readiness gate across location fit, ATS optimization basis, and differentiation highlights. The system now distinguishes `Review`, `Staging`, `Mismatch Hold`, `Apply-Ready`, and `Submit-Ready`, plus a resume-transformation layer driven by an optimization brief. The remaining weakness is that these rules are still mostly doc-level rather than enforced by a canonical schema and runtime/UI state model.

## Top Priorities
- **top_priorities:**
  - turn the new application-readiness contract into a canonical schema and state model the UI/runtime can enforce
  - implement a real staging-to-canonical promotion and merge model so trusted tracker updates stop depending on ad hoc local behavior
  - tighten intake filtering and ranking against Jonathon’s search requirements so weak-fit backlog stops forming upstream
  - validate one real JobOps operating loop and tighten its instructions from actual use
  - keep cockpit/runtime persistence consistent across Sheets, local mirror, git, and Drive-accessible artifacts

## Active Risks
- **active_risks:**
  - low-quality Gmail signals and broad direct-board imports can still create weak review items or cold jobs if filtering and promotion rules remain too loose
  - application-readiness logic now exists in docs, but mismatch between prose, future schema fields, and runtime behavior could create false `apply-ready` confidence if not enforced structurally
  - Indeed remains blocked by anti-bot flow, leaving one source partially inaccessible
  - some legacy docs and filenames still reflect older platform assumptions instead of the current cockpit/runtime reality
  - gateway is healthy but still not loaded as a clean LaunchAgent service, so lifecycle transitions remain fragile
  - post-run persistence still leaves dirty runtime/browser files in the worktree even when auto-sync commits the right subset
  - Indeed remains partially blocked by anti-bot flow, so one board source is still degraded
  - Drive mirror behavior currently creates snapshot copies rather than refreshing a single canonical mirrored file, so mirror sprawl is growing

## Open Questions
- **open_questions:**
  - what exact canonical schema fields should represent location fit, ATS basis, differentiation highlights, optimization brief, and tailored artifact state?
  - what filters should gate direct-board imports so only Jonathon-fit roles land in the apply set by default?
  - what canonical Drive update mechanism should replace duplicate file uploads?
  - which remaining docs still materially misrepresent the live JT7 app/runtime state?

## Required Next Moves
- **required_next_moves:**
  - define the canonical schema fields and state transitions for `Mismatch Hold`, `Apply-Ready`, `Submit-Ready`, optimization brief, and tailored artifact state
  - trace why `jt7_pass_log.jsonl`, `jt7_scheduler.json`, new reports, and browser-side artifacts still leave the worktree dirty after a successful run
  - validate the hardened scheduler/catch-up path on the next real resume cycle now that the chain succeeds again
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
