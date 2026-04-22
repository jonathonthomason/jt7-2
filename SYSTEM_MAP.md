# SYSTEM_MAP.md

## Purpose
This file explains how the workspace should function as JT7’s operating system.

The workspace should support three priorities:
1. career
2. product
3. execution

Each file should either:
- define the system
- hold durable context
- track current state
- support active work
- capture decisions

If a file does none of those things, it is probably noise.

## Core Root Files
### `AGENTS.md`
System operating rules.
Defines how JT7 should behave inside this workspace.
Should become the main operating manual for mission, priorities, memory behavior, boundaries, and file usage.

### `SOUL.md`
Behavioral philosophy.
Defines tone, temperament, and baseline operating posture.
Should remain the personality and principles layer.

### `IDENTITY.md`
JT7 identity and operator profile.
Should define who JT7 is, what role JT7 plays, and how JT7 should show up.

### `USER.md`
Jonathon operating profile.
Should define who Jonathon is, what he is optimizing for, how he works best, and how JT7 should adapt.

### `MISSION.md`
Strategic north star.
Defines the system purpose, priorities, success criteria, and anti-goals.

### `CURRENT.md`
Present-tense control center.
Defines what is true now, what matters now, and what should happen next.

### `MEMORY.md`
Long-term curated memory.
Stores durable context JT7 should not have to rediscover.

### `DECISIONS.md`
Decision ledger.
Captures key choices, rationale, and implications so the system stays coherent over time.

### `TOOLS.md`
Local operations reference.
Stores environment-specific notes, commands, constraints, and setup details.

### `HEARTBEAT.md`
Proactive support prompt.
Defines what JT7 should check periodically and when JT7 should proactively surface something.

## Transitional Files
### `BOOTSTRAP.md`
First-run scaffold.
This should be removed once identity and operating context are fully established.

## Future Directories
### `memory/`
Daily logs and session continuity.
Use for dated notes, working memory, and periodic state capture.

Suggested structure:
- `memory/YYYY-MM-DD.md`

### `career/`
Career search operating system.
Should contain:
- strategy
- target companies
- application/interview pipeline
- portfolio positioning
- interview preparation

### `product/`
JT7 product operating system.
Should contain:
- product thesis
- roadmap
- architecture
- experiments
- notes on differentiation and workflow design

### `ops/`
Execution layer.
Should contain:
- focus/current sprint
- inbox/capture
- review notes
- blockers

## How the System Should Work
### Strategic layer
`MISSION.md`
Defines what the system is trying to do.

### Operational layer
`CURRENT.md`, `HEARTBEAT.md`, `DECISIONS.md`
Defines what matters now, what is changing, and why.

### Memory layer
`MEMORY.md`, `memory/`
Prevents repeated rethinking and context loss.

### Workstream layer
`career/`, `product/`, `ops/`
Organizes active work by outcome, not by random note accumulation.

### Runtime truth layer
Google Sheets should be treated as the live operational source of truth for JT7 tracker state.
Gmail, Calendar, and manual input should be treated as evidence sources.
Markdown files should govern architecture, contracts, memory, roadmap, and audits rather than acting as competing live tracker stores.

### Runtime access rule
`gog` should be treated as the canonical Google capability layer.
A Google capability should only be considered accessible when auth, tool availability, runtime execution, and command-path verification all pass.
Telegram should not be assumed to be a valid execution surface unless verified.

## Design Rule
Keep the root small and legible.
Only foundational files should live there.
Everything else should move into clear workstream directories.
