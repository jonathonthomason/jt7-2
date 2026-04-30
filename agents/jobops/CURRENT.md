# CURRENT.md

## Current State Record
- **id:** jobops_current_state_2026_04_30
- **updated_at:** 2026-04-30T17:45:00-05:00
- **system_phase:** JobOps Activation
- **current_step:** Telegram JobOps bot is live and routed; next work is to make JobOps behavior durable and then implement a proper staging flow for direct-board imports.
- **confidence_level:** medium_high

## State Summary
- **state_summary:** JobOps is now connected as its own Telegram bot surface and has a dedicated workspace/auth path. The main operational gap is not connectivity but workflow maturity: staging policy must be enforced in practice and JobOps needs tighter review/ranking routines.

## Top Priorities
- **top_priorities:**
  - keep canonical tracker state clean by treating broad direct-board imports as staging, not trusted Jobs
  - triage and rank review intake into a smaller, high-signal morning action set
  - escalate parser, routing, or tracker-policy issues back to JT7 Platform instead of working around them silently

## Active Risks
- **active_risks:**
  - broad direct imports can still overwhelm review and imply false canonicality if staging is not implemented clearly
  - review workload can become noisy if ranking rules stay too loose
  - JobOps may still inherit too much platform context unless the lane stays disciplined

## Required Next Moves
- **required_next_moves:**
  - define the first operational review/ranking pass shape for JobOps
  - implement or enforce a visible staging layer for direct-board intake
  - validate that JobOps answers operational prompts as JobOps rather than drifting into platform architecture
  - maintain the new durable RACI/instruction docs as scope authority when explicitly instructed
