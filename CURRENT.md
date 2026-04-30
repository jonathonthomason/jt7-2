# CURRENT.md

## Current State Record
- **id:** current_state_2026_04_30
- **updated_at:** 2026-04-30T06:45:00-05:00
- **system_phase:** Cockpit + Runtime Hardening
- **current_step:** Review Queue v1 is implemented and verified; JobOps bot/agent operating model is now specified; next work should wire the JobOps surface and narrow signal quality / board-import precision
- **confidence_level:** medium_high

## State Summary
- **state_summary:** JT7 now has a real Review Queue cockpit surface in `job-search-ui`, plus a fresh 2026-04-30 runtime scrub and direct board refresh. The main remaining gaps are Indeed access, direct-import precision, and tighter prioritization of imported opportunities.

## Top Priorities
- **top_priorities:**
  - improve parsing and import precision so review noise and off-target board results stop polluting the tracker
  - keep cockpit/runtime persistence consistent across Sheets, local mirror, git, and Drive-accessible artifacts
  - turn the new Review Queue surface into the foundation for the rest of the JT7-2 cockpit
  - define and route the separate JobOps bot surface cleanly inside the same OpenClaw core

## Active Risks
- **active_risks:**
  - low-quality Gmail signals and broad direct-board imports can still create weak review items or cold jobs if filtering remains too loose
  - Indeed remains blocked by anti-bot flow, leaving one source partially inaccessible
  - some legacy docs and filenames still reflect older platform assumptions instead of the current cockpit/runtime reality
  - JobOps routing/config is specified but not yet wired into live channel/account configuration
  - Drive mirror behavior currently uploads fresh copies rather than updating a single canonical mirrored doc in place

## Open Questions
- **open_questions:**
  - what filters should gate direct-board imports so only Jonathon-fit roles land in the apply set by default?
  - what canonical Drive update mechanism should replace duplicate file uploads?
  - which remaining docs still materially misrepresent the live JT7 app/runtime state?
  - what exact OpenClaw config/binding shape should be used to route the Job Ops bot to its dedicated agent behavior?

## Required Next Moves
- **required_next_moves:**
  - tighten source-specific Gmail filtering for newsletters, digests, and reply notifications unless they contain a valid role/company pattern
  - add stronger direct-board filtering and ranking so imported jobs favor senior/principal product design fit, remote, and DFW relevance
  - normalize Drive mirror behavior so updated docs refresh canonical mirrored copies rather than creating duplicates
  - continue keeping cockpit/runtime docs and storage rules aligned with the actual live JT7 execution path
  - translate the JobOps bot/agent spec into concrete OpenClaw channel account + binding config

## Related Files
- **related_files:**
  - ROADMAP.md
  - ops/focus.md
  - DECISIONS.md
  - docs/storage-rules.md
  - job-search-ui/docs/local-git-drive-rules.md
  - job-search-ui/docs/review-queue-build-brief.md
  - docs/jt7-job-ops-bot-agent-spec.md
  - job-search-ui/scripts/run_jt7_chain.py
  - job-search-ui/scripts/import_direct_board_jobs.py
  - job-search-ui/runtime/jt7_tasks.json
  - job-search-ui/runtime/jt7_scheduler.json
