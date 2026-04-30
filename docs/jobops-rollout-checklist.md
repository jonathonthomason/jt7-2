# JobOps Rollout Checklist

## Phase A — State Integrity
- [x] confirm Sheets vs local Jobs mismatch source
- [x] define direct-board import policy
- [ ] create explicit staging layer for direct-board imports
- [ ] reconcile current local-only import rows against the staging policy

## Phase B — JobOps Wiring
- [x] create dedicated `jobops` agent workspace
- [x] separate JobOps agent instructions from Platform instructions
- [x] configure `jobops` agent to use its own workspace
- [x] keep existing account-based route binding to `agentId: jobops`
- [x] disable elevated mode for `jobops`
- [ ] add full Telegram bot token for the `jobops` account in OpenClaw config
- [ ] verify inbound DM routing through the Job Ops bot
- [ ] verify replies come from the Job Ops bot identity

## Session / Routing Rules
- [ ] confirm default account -> `platform`
- [ ] confirm `jobops` account -> `jobops`
- [ ] define stable session labels for Platform and JobOps surfaces
- [ ] validate cross-session handoff path using `sessions_send`

## Safety Boundaries
- [x] encode JobOps safety rules in its agent workspace
- [x] keep JobOps out of elevated mode
- [ ] decide whether additional hard tool restrictions are needed after first live tests

## Validation
- [ ] send a test DM to Platform bot
- [ ] send a test DM to Job Ops bot
- [ ] confirm role separation feels distinct in practice
- [ ] confirm JobOps does not answer platform architecture prompts as if they were in scope

## Blocker
The live Job Ops Telegram account cannot be activated until the full bot token is available for config entry.
