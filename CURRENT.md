# CURRENT.md

## Current State Record
- **id:** current_state_2026_04_15
- **updated_at:** 2026-04-15T09:15:00-05:00
- **system_phase:** Unified Multi-Surface Platform Refactor
- **current_step:** replace legacy planning-surface model with platform + job ops + life + TA knowledge
- **confidence_level:** medium

## State Summary
- **state_summary:** JT7 is being refactored into one unified platform with five disciplined conversation surfaces, one control plane, and explicit shared-context and handoff behavior. The active structure is now platform, job ops, life, TA knowledge, and tasks.

## Top Priorities
- **top_priorities:**
  - lock the unified 5-surface platform model into tenant config and docs
  - preserve one shared core while enforcing domain boundaries
  - keep career-critical runtime proof work unblocked by architecture drift

## Active Risks
- **active_risks:**
  - some legacy docs and filenames still reflect older three-bot, four-surface, or planning-based assumptions
  - runtime surface behavior is defined in docs but not yet fully activated in OpenClaw/Telegram
  - current-state and roadmap artifacts can drift if the new surface model is not propagated consistently
  - career execution can be delayed if platform work keeps expanding without runtime activation

## Open Questions
- **open_questions:**
  - what is the exact live session and bot mapping to use now that Telegram bot tokens are available?
  - should TA knowledge be strictly transcript intelligence first or a broader knowledge surface from day one?
  - which artifacts still need renaming so filenames match the new 4-surface reality?

## Required Next Moves
- **required_next_moves:**
  - finish propagating the 5-surface model into current-state, decision, and roadmap artifacts
  - define the remaining routing, handoff, and shared-context schemas/modules required for runtime implementation
  - map live Telegram/OpenClaw surfaces to `jt7_platform_bot`, `jt7_job_ops_bot`, `jrt7_life_bot`, `jt7_ta_knowledge_bot`, and `jt7_tasks_bot`
  - continue separate runtime proof-of-life work for Gmail → Sheets without letting platform docs fork from execution truth

## Related Files
- **related_files:**
  - ROADMAP.md
  - ops/focus.md
  - DECISIONS.md
  - tenants/JT_PERSONAL/bot_surfaces.md
  - tenants/JT_PERSONAL/surface_policies.md
  - docs/three-bot-surface-model.md
  - docs/openclaw-thread-routing-config-spec.md
