# ops/focus.md

## Focus Items

### focus_01
- **id:** focus_activate_career_engine
- **title:** Activate the career engine
- **type:** priority
- **domain:** career
- **status:** active
- **priority_rank:** 1
- **summary:** Make the search visible, structured, and moving through real pipeline entries, clearer positioning, and asset visibility.
- **related_files:**
  - CURRENT.md
  - career/pipeline.md
  - career/strategy.md
- **related_entity_ids:** []
- **owner:** shared
- **due_at:** null
- **notes:**
  - Highest-value system priority
  - Career-first alignment must remain visible in active work

### focus_02
- **id:** focus_stabilize_jt7_operating_system
- **title:** Stabilize the JT7 operating system
- **type:** priority
- **domain:** product
- **status:** active
- **priority_rank:** 2
- **summary:** Complete the core system layer so JT7 can support real use, roadmap execution, and future UI rendering.
- **related_files:**
  - CURRENT.md
  - ROADMAP.md
  - product/thesis.md
  - product/schemas.md
- **related_entity_ids:** []
- **owner:** shared
- **due_at:** null
- **notes:**
  - Product work should support the career engine, not outrun it

### focus_03
- **id:** focus_reduce_execution_drag
- **title:** Reduce execution drag
- **type:** priority
- **domain:** execution
- **status:** active
- **priority_rank:** 3
- **summary:** Keep current state, blockers, and next moves visible so progress does not depend on context reconstruction.
- **related_files:**
  - CURRENT.md
  - MEMORY.md
  - DECISIONS.md
- **related_entity_ids:** []
- **owner:** shared
- **due_at:** null
- **notes:**
  - Execution support exists to reduce friction across career and product work

### focus_04
- **id:** focus_enter_first_pipeline_roles
- **title:** Enter first real pipeline roles
- **type:** next_action
- **domain:** career
- **status:** done
- **priority_rank:** 1
- **summary:** Populate `career/pipeline.md` with the first real companies and roles so career work becomes visible and actionable.
- **related_files:**
  - career/pipeline.md
  - CURRENT.md
- **related_entity_ids:**
  - opp_autodesk_ux_product_designer
  - opp_crossover_ux_product_designer
  - opp_level_ux_product_designer
  - opp_better_ux_product_designer
  - opp_achieve_debt_relief_ux_product_designer
  - opp_pattison_id_ux_product_designer
  - opp_deloitte_ux_product_designer
- **owner:** shared
- **due_at:** null
- **notes:**
  - Initial live opportunity import completed from prior spreadsheet summary

### focus_05
- **id:** focus_capture_job_search_assets
- **title:** Capture job-search assets and gaps
- **type:** next_action
- **domain:** career
- **status:** active
- **priority_rank:** 2
- **summary:** Identify what resume, portfolio, and case-study materials already exist and what is missing.
- **related_files:**
  - CURRENT.md
  - career/strategy.md
- **related_entity_ids:** []
- **owner:** shared
- **due_at:** null
- **notes:**
  - Asset visibility is required for stronger pipeline execution

### focus_06
- **id:** focus_refine_positioning_statement
- **title:** Refine positioning statement
- **type:** next_action
- **domain:** career
- **status:** active
- **priority_rank:** 3
- **summary:** Convert strategy language into a concise outreach-ready positioning statement.
- **related_files:**
  - career/strategy.md
- **related_entity_ids:** []
- **owner:** shared
- **due_at:** null
- **notes:**
  - Needed for outreach, applications, and role-fit clarity

### focus_07
- **id:** focus_no_live_pipeline_data
- **title:** No live pipeline data
- **type:** blocker
- **domain:** career
- **status:** resolved
- **priority_rank:** 1
- **summary:** No live companies or roles have been entered into the pipeline yet.
- **related_files:**
  - career/pipeline.md
  - CURRENT.md
- **related_entity_ids:**
  - opp_autodesk_ux_product_designer
  - opp_crossover_ux_product_designer
  - opp_level_ux_product_designer
  - opp_better_ux_product_designer
  - opp_achieve_debt_relief_ux_product_designer
  - opp_pattison_id_ux_product_designer
  - opp_deloitte_ux_product_designer
- **owner:** shared
- **due_at:** null
- **notes:**
  - Initial live pipeline import resolved the zero-data blocker

### focus_08
- **id:** focus_missing_asset_inventory
- **title:** Missing asset inventory
- **type:** blocker
- **domain:** career
- **status:** blocked
- **priority_rank:** 2
- **summary:** Resume, portfolio, and case-study assets are not yet inventoried in the system.
- **related_files:**
  - CURRENT.md
  - career/strategy.md
- **related_entity_ids:** []
- **owner:** shared
- **due_at:** null
- **notes:**
  - Prevents clear assessment of readiness and gaps

### focus_10
- **id:** focus_validate_live_pipeline_entries
- **title:** Validate imported pipeline entries
- **type:** next_action
- **domain:** career
- **status:** active
- **priority_rank:** 2
- **summary:** Review imported roles and recruiter firms, add missing links/details, and clarify ambiguous statuses like Pattison ID confirmed.
- **related_files:**
  - career/pipeline.md
  - CURRENT.md
- **related_entity_ids:**
  - opp_pattison_id_ux_product_designer
- **owner:** shared
- **due_at:** null
- **notes:**
  - Important after runtime proof-of-life is stabilized
  - Focus on links, exact titles, and follow-up readiness

### focus_11
- **id:** focus_prove_one_live_loop
- **title:** Prove one live Gmail-to-Sheets loop
- **type:** next_action
- **domain:** product
- **status:** active
- **priority_rank:** 1
- **summary:** Verify one real signal can be read from Gmail, processed, matched to tracker truth, written to Google Sheets, and confirmed after write.
- **related_files:**
  - CURRENT.md
  - JT7/00_System/Architecture/JT7_Workbook_Implementation_Plan.md
  - JT7/00_System/Architecture/JT7_Auth_Architecture_and_Onboarding_Spec.md
- **related_entity_ids:** []
- **owner:** shared
- **due_at:** null
- **notes:**
  - This is the core MVP proof-of-life milestone
  - Requires stable runtime execution surface, not just architecture

### focus_12
- **id:** focus_stabilize_runtime_surface
- **title:** Stabilize runtime execution surface
- **type:** blocker
- **domain:** product
- **status:** blocked
- **priority_rank:** 1
- **summary:** Telegram/OpenClaw execution has not been reliable enough to verify a live Gmail-to-Sheets loop end to end.
- **related_files:**
  - CURRENT.md
- **related_entity_ids:** []
- **owner:** shared
- **due_at:** null
- **notes:**
  - Use gog as canonical Google capability layer
  - Gmail read/search, Sheets read/write, and Drive read/write are only considered accessible when auth, tool availability, runtime execution, and command-path verification all pass
  - Do not assume Telegram is a valid execution surface unless verified

### focus_09
- **id:** focus_avoid_overbuilding_before_use
- **title:** Avoid overbuilding before career workflow is active
- **type:** anti_focus
- **domain:** system
- **status:** active
- **priority_rank:** null
- **summary:** Do not expand tooling, backlog, or UI abstraction faster than real career execution needs.
- **related_files:**
  - ROADMAP.md
  - CURRENT.md
  - product/thesis.md
- **related_entity_ids:** []
- **owner:** shared
- **due_at:** null
- **notes:**
  - Protects the system from product-first drift
