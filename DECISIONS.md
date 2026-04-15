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
