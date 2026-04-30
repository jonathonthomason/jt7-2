# DECISIONS.md

## Decision Records

### decision_01
- **id:** decision_adopt_jt7_identity
- **title:** Adopt JT7 as the operating identity
- **domain:** system
- **status:** active
- **decision_date:** 2026-04-02
- **owner:** shared
- **summary:** JT7 is the active identity for the assistant and operating system
- **why:** Jonathon explicitly defined the assistant as a personal AI operations system rather than a generic assistant
- **implications:**
  - JT7 should operate as job search agent, product strategist, system architect, and execution copilot
  - future files should reinforce operator behavior over assistant persona behavior
- **related_files:**
  - IDENTITY.md
  - AGENTS.md
  - USER.md
- **related_entity_ids:** []
- **next_review_at:** null

### decision_02
- **id:** decision_priority_order_career_product_execution
- **title:** Prioritize career, then product, then execution
- **domain:** system
- **status:** active
- **decision_date:** 2026-04-02
- **owner:** shared
- **summary:** JT7 should optimize in the order of career, product, and execution
- **why:** Jonathon explicitly ranked the priorities and career has the highest immediate leverage
- **implications:**
  - career outcomes should take precedence over product refinement
  - execution systems should support career movement and product leverage
- **related_files:**
  - MISSION.md
  - AGENTS.md
  - CURRENT.md
  - ops/focus.md
- **related_entity_ids:** []
- **next_review_at:** null

### decision_03
- **id:** decision_rebuild_scaffold_into_operating_system
- **title:** Rebuild the scaffold into a functioning operating system
- **domain:** system
- **status:** active
- **decision_date:** 2026-04-02
- **owner:** shared
- **summary:** Treat the existing workspace as a scaffold that must be upgraded into a real operating system
- **why:** The original workspace had useful philosophy and structure but lacked a complete operational layer
- **implications:**
  - preserve useful foundations
  - introduce stronger mission, state, memory, decision, and workstream layers
- **related_files:**
  - AGENTS.md
  - MISSION.md
  - CURRENT.md
  - SYSTEM_MAP.md
- **related_entity_ids:** []
- **next_review_at:** null

### decision_04
- **id:** decision_introduce_foundation_files
- **title:** Introduce root foundation files
- **domain:** system
- **status:** active
- **decision_date:** 2026-04-02
- **owner:** shared
- **summary:** Introduce mission, current-state, memory, system-map, decisions, and roadmap files at the root
- **why:** The scaffold lacked explicit strategic direction, durable memory, system mapping, and tracked decision continuity
- **implications:**
  - the root becomes the system control surface
  - workstreams can remain focused on active execution
- **related_files:**
  - MISSION.md
  - CURRENT.md
  - MEMORY.md
  - SYSTEM_MAP.md
  - DECISIONS.md
  - ROADMAP.md
- **related_entity_ids:** []
- **next_review_at:** null

### decision_05
- **id:** decision_do_not_pretend_unverified_workspace_state
- **title:** Do not claim full workspace knowledge when state is unverified
- **domain:** execution
- **status:** active
- **decision_date:** 2026-04-02
- **owner:** JT7
- **summary:** JT7 should distinguish verified state from inference whenever inspection is limited
- **why:** Operational trust depends on accuracy and false certainty creates hidden fragility
- **implications:**
  - verified and inferred state must remain clearly separated
  - files should be updated with known facts, not imagined state
- **related_files:**
  - AGENTS.md
  - CURRENT.md
  - MEMORY.md
- **related_entity_ids:** []
- **next_review_at:** null

### decision_06
- **id:** decision_google_sheets_operational_truth
- **title:** Use Google Sheets as the live operational source of truth
- **domain:** system
- **status:** active
- **decision_date:** 2026-04-05
- **owner:** shared
- **summary:** JT7 should treat Google Sheets as the single operational source of truth for live tracker state, while markdown remains architecture, governance, memory, and audit documentation.
- **why:** Competing tracker truths across markdown and Sheets create drift, duplicated logic, and unreliable UI/runtime behavior.
- **implications:**
  - Gmail, Calendar, and manual input are evidence sources rather than truth stores
  - markdown docs must not silently compete with Sheets for live tracker authority
  - runtime proof-of-life depends on verified Gmail/Sheets execution rather than local file state alone
- **related_files:**
  - CURRENT.md
  - SYSTEM_MAP.md
  - MISSION.md
  - ROADMAP.md
- **related_entity_ids:** []
- **next_review_at:** null

### decision_07
- **id:** decision_consolidated_mvp_schema_and_status_model
- **title:** Consolidate JT7 MVP around one shared schema and one status model
- **domain:** system
- **status:** active
- **decision_date:** 2026-04-05
- **owner:** shared
- **summary:** JT7 MVP should use one shared schema (`company`, `role`, `status`, `last_activity`, `next_step`, `contact`, `source`, `thread_id`, `notes`) and one final opportunity status model (`Applied`, `Recruiter Contacted`, `Screening`, `Interviewing`, `Offer`, `Rejected`, `Cold`).
- **why:** Multiple schema versions and status vocabularies were creating architecture drift and making end-to-end runtime behavior harder to stabilize.
- **implications:**
  - older richer specs should be treated as partially legacy until rewritten
  - layer responsibilities should align to the consolidated flow: Intake -> Processing -> Sheets -> Interaction
  - legacy opportunity states like lead, saved, researching, and archived must be normalized away in live operational use
- **related_files:**
  - CURRENT.md
  - ROADMAP.md
  - JT7/00_System/Architecture/JT7_Workbook_Implementation_Plan.md
  - JT7/00_System/Data-Specs/JT7_Jobs_Data_Spec.md
- **related_entity_ids:** []
- **next_review_at:** null

### decision_08
- **id:** decision_gog_canonical_google_capability_layer
- **title:** Treat gog as the canonical Google capability layer
- **domain:** execution
- **status:** active
- **decision_date:** 2026-04-05
- **owner:** shared
- **summary:** JT7 should use gog as the canonical Google capability layer and treat Gmail read/search, Sheets read/write, and Drive read/write as accessible only when auth, tool availability, runtime execution, and command-path verification all pass.
- **why:** Runtime truth was being confused with intended architecture; the system needs a strict capability test before claiming operational readiness.
- **implications:**
  - personal Google OAuth user auth is the correct default model for this JT7 instance
  - Telegram should not be assumed to be a valid execution surface unless explicitly verified
  - MVP proof-of-life is blocked until one stable runtime surface can complete the Gmail -> Sheets loop end to end
- **related_files:**
  - CURRENT.md
  - MISSION.md
  - SYSTEM_MAP.md
  - JT7/00_System/Architecture/JT7_Auth_Architecture_and_Onboarding_Spec.md
- **related_entity_ids:** []
- **next_review_at:** null

### decision_09
- **id:** decision_unified_multi_surface_platform_model
- **title:** Use one unified platform core across multiple conversation surfaces
- **domain:** system
- **status:** active
- **decision_date:** 2026-04-15
- **owner:** Jonathon
- **summary:** JT7 must operate as one engine, one gateway, and one shared brain, with multiple conversation surfaces acting as domain-specific entry points rather than separate systems.
- **why:** Jonathon explicitly directed JT7 to behave like a real product platform with focused surfaces, reusable logic, and no forked systems.
- **implications:**
  - all bot/thread surfaces must share one underlying platform core
  - routing, handoff, and shared-memory behavior must be centralized
  - surfaces must not act like general assistants
- **related_files:**
  - CURRENT.md
  - docs/three-bot-surface-model.md
  - docs/openclaw-thread-routing-config-spec.md
  - tenants/JT_PERSONAL/bot_surfaces.md
- **related_entity_ids:** []
- **next_review_at:** null

### decision_10
- **id:** decision_five_surface_target_model_platform_job_ops_life_knowledge_tasks
- **title:** Adopt platform, job ops, life, TA knowledge, and tasks as the active surface set
- **domain:** system
- **status:** active
- **decision_date:** 2026-04-15
- **owner:** Jonathon
- **summary:** The active JT7 target model uses five conversation surfaces: platform, job ops, life, TA knowledge, and tasks. The previously assumed planning bot is not part of the current live target model.
- **why:** Jonathon explicitly added `JT7 Tasks` after defining the earlier active set and now has tokens for all active bot surfaces.
- **implications:**
  - planning-centric artifacts must be updated or deprecated
  - tenant config and docs must align to the five-surface set
  - platform remains the control plane while the other four surfaces operate as workers
  - tasks becomes the dedicated execution-queue and follow-through surface
- **related_files:**
  - CURRENT.md
  - tenants/JT_PERSONAL/bot_surfaces.md
  - tenants/JT_PERSONAL/surface_policies.md
  - tenants/JT_PERSONAL/bot_runtime_profile.md
- **related_entity_ids:** []
- **next_review_at:** null

### decision_11
- **id:** decision_explicit_handoff_and_context_split
- **title:** Require explicit handoff and explicit shared-context packaging across surfaces
- **domain:** system
- **status:** active
- **decision_date:** 2026-04-15
- **owner:** Jonathon
- **summary:** JT7 must separate shared global context from thread-local context and move cross-surface work only through explicit handoff or shared-context packaging.
- **why:** Silent domain switching and uncontrolled context mixing break platform integrity and traceability.
- **implications:**
  - shared context includes goals, rules, decisions, identity, and priorities
  - thread-local context includes active tasks, recent actions, and domain-specific state
  - cross-surface movement must preserve traceability and avoid duplicate ownership
- **related_files:**
  - docs/multi-agent-thread-implementation-spec.md
  - docs/openclaw-thread-routing-config-spec.md
  - tenants/JT_PERSONAL/surface_policies.md
  - tenants/JT_PERSONAL/bot_runtime_profile.md
- **related_entity_ids:** []
- **next_review_at:** null

### decision_12
- **id:** decision_channel_surfaces_canonical_live_mapping
- **title:** Use `tenants/JT_PERSONAL/channel_surfaces.md` as the canonical live bot-to-surface mapping
- **domain:** system
- **status:** active
- **decision_date:** 2026-04-15
- **owner:** Jonathon
- **summary:** `tenants/JT_PERSONAL/channel_surfaces.md` is the canonical live mapping artifact for JT7 bot identities to tenant-scoped conversation surfaces under one shared platform.
- **why:** The system needed one explicit artifact that defines the live mapping layer between bot identities, surface roles, default agents, handoff targets, and primary platform entry.
- **implications:**
  - `jt7_platform_bot` is the primary inbound platform entry and control plane in the canonical mapping
  - all other bots are defined as domain worker surfaces under one shared engine
  - runtime wiring should bind to this artifact rather than inferring mapping from broader architecture docs
- **related_files:**
  - tenants/JT_PERSONAL/channel_surfaces.md
  - CURRENT.md
  - docs/openclaw-thread-routing-config-spec.md
- **related_entity_ids:** []
- **next_review_at:** null

### decision_13
- **id:** decision_task_pass_persistence_local_git_drive
- **title:** Persist each meaningful JT7 task pass across local, git, and Drive
- **domain:** execution
- **status:** active
- **decision_date:** 2026-04-22
- **owner:** Jonathon
- **summary:** Each meaningful JT7 task pass event should leave behind synchronized local artifacts, git history, and Drive-accessible mirrors, while Google Sheets remains the live tracker truth for tracker state.
- **why:** Jonathon explicitly directed JT7 to maintain local + git + Drive persistence for each task pass event rather than leaving Drive as an optional afterthought.
- **implications:**
  - task pass evidence should persist locally first
  - changed runtime artifacts and mirrors should be committed to git when meaningful changes occurred
  - relevant docs and mirrored artifacts should be refreshed to Drive when they changed
  - system requirements and docs must be updated to match the live JT7 app state instead of drifting behind implementation
- **related_files:**
  - USER.md
  - MISSION.md
  - CURRENT.md
  - docs/storage-rules.md
  - job-search-ui/docs/local-git-drive-rules.md
- **related_entity_ids:** []
- **next_review_at:** null

### decision_14
- **id:** decision_architectural_boundary_platform_builder_vs_jobops
- **title:** Separate JT7 platform-building responsibilities from JobOps operational responsibilities
- **domain:** system
- **status:** active
- **decision_date:** 2026-04-29
- **owner:** Jonathon
- **summary:** JT7 should operate as the system architect and platform builder for JT7-2, focusing on the job-search-ui, React/TypeScript implementation, business requirements, and the synchronization layer between Google Sheets, markdown mirrors, and the OpenClaw gateway, while daily operational job-search work will transition to JobOps once the platform is solid.
- **why:** Jonathon explicitly established a strict separation of concerns so platform building and operational job-search execution do not blur together.
- **implications:**
  - JT7 should prioritize building the cockpit rather than acting as the long-term daily JobOps operator
  - business requirements refinement and platform implementation are core JT7 responsibilities
  - infrastructure logic across Sheets, markdown mirrors, and gateway remains inside JT7 scope
  - Gmail signal triage, recruiter follow-ups, and interview scheduling belong to JobOps after handoff
  - JT7 should prepare for a clear engineer-to-pilot transition model
- **related_files:**
  - MEMORY.md
  - CURRENT.md
  - job-search-ui/
- **related_entity_ids:** []
- **next_review_at:** null

### decision_15
- **id:** decision_review_queue_first_cockpit_surface
- **title:** Make Review Queue the first JT7-2 cockpit surface and default landing route
- **domain:** product
- **status:** active
- **decision_date:** 2026-04-30
- **owner:** Jonathon
- **summary:** JT7-2 should establish trust before dashboarding by shipping Review Queue v1 first, routing `/` to `/review-queue`, and using review-state/action/event primitives as the foundation for later cockpit surfaces.
- **why:** Raw signals were still too noisy to safely treat as trusted pipeline state, so the cockpit needed an explicit trust gateway before broader execution and reporting surfaces.
- **implications:**
  - Review Queue is now the primary entry point for the cockpit MVP
  - review decisions should emit explicit events and preserve source/evidence boundaries
  - downstream views should treat trusted state as the output of review rather than raw intake
  - future cockpit surfaces should adapt to the review-first model instead of bypassing it
- **related_files:**
  - job-search-ui/src/App.tsx
  - job-search-ui/src/state/mvpState.tsx
  - job-search-ui/src/features/mvp/MvpPages.tsx
  - job-search-ui/src/domain/cockpit/
  - job-search-ui/docs/review-queue-build-brief.md
- **related_entity_ids:** []
- **next_review_at:** null

### decision_16
- **id:** decision_jobops_separate_bot_same_openclaw_core
- **title:** Run JobOps as a separate bot surface on the same OpenClaw core
- **domain:** system
- **status:** active
- **decision_date:** 2026-04-30
- **owner:** Jonathon
- **summary:** JT7 Job Ops should launch as a separate Telegram bot surface with its own dedicated JobOps agent behavior, while remaining on the same OpenClaw Gateway/core as JT7 Platform unless hard isolation later becomes necessary.
- **why:** Jonathon wants a clean direct channel for job-search operations without fragmenting the platform into multiple independent systems too early.
- **implications:**
  - separate bot identity should provide a separate user-facing operational lane
  - JobOps should have one primary domain role even if internal subagents are used behind the scenes
  - platform-building work stays with JT7 Platform, while review/triage/pipeline operations move to JobOps
  - multi-account Telegram on one Gateway is the preferred starting architecture
  - separate Gateway/profile remains a later option for harder isolation if needed
- **related_files:**
  - docs/jt7-job-ops-bot-agent-spec.md
  - docs/three-bot-surface-model.md
  - docs/openclaw-thread-routing-config-spec.md
- **related_entity_ids:** []
- **next_review_at:** null
