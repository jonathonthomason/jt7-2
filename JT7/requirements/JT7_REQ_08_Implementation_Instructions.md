# JT7 — Implementation Instructions

## Do NOT touch
- auth
- API config
- gateway
- Telegram
- environment

## Workflow
1. Audit
2. Identify files
3. Explain mismatch
4. Propose minimal change
5. Wait for approval
6. Edit one surface
7. Run app
8. Report changes

## Build Order
Start with:
/execute/today

## Cheap Mode
- short responses
- no retries
- no multi-agent runs
- no large refactors

## Prompt Template

Use JT7 requirements.

Task:
Audit /execute/today

Return:
- files
- mismatch
- change set
- risk
- next step

Do not edit yet.