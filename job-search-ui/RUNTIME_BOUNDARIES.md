# RUNTIME_BOUNDARIES.md

## Principle
Markdown defines the contract.
Python modules enforce the contract.
Data stores reflect current state.
UI renders only verified state.

## Orchestration boundary
`run_jt7_chain.py` should orchestrate modules.
It should not permanently own business rules that belong in domain/services/adapters.

## Phase 3A extracted modules
- runtime/domain/actions.py
- runtime/services/action_generation.py
- runtime/services/action_lifecycle.py
- runtime/adapters/homepage_state.py
- runtime/pipelines/todays_plan.py
- runtime/storage/local_mirror.py
