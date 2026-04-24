# JT7 (for hiring teams)

JT7 is a personal AI-operated job search platform that I designed and built as both:
- a working operating system for my own search
- a product-thinking artifact that shows how I use AI, OpenClaw, and structured prompting to move from concept to real implementation

This file is meant to explain not just what JT7 does, but how I used AI in a disciplined product and engineering workflow to produce architecture, logic, UI structure, and live code.

## Why I built it this way

A job search is operationally messy.
Signals arrive through email, calendar, job boards, recruiter replies, spreadsheets, and ad hoc notes. Most people handle that through fragmented tools and manual memory.

I approached the problem as a product systems problem:
- separate evidence from truth
- make logic explicit
- keep state durable
- build calm execution surfaces
- reduce cognitive overhead
- preserve traceability from input to decision to action

The result is JT7: a system where AI is not just generating text, but helping define contracts, structure workflows, scaffold implementation, and maintain continuity across the product.

## How I used AI in this repo

I used AI as a structured design-and-build collaborator, not as a black-box code generator.

My approach was:
1. define the operating model in Markdown first
2. use prompting to turn vague ideas into explicit contracts, rules, and schemas
3. scaffold implementation around those contracts
4. iterate from planning artifacts into real runtime behavior
5. refactor working vertical slices into modular architecture once the end-to-end loop was proven

In other words, AI was used to accelerate:
- systems framing
- artifact creation
- architecture definition
- code scaffolding
- runtime refactoring
- documentation alignment

But the important part is that the system was directed through product decisions, not left to uncontrolled generation.

## Core build philosophy

The repo reflects a few deliberate principles.

### 1. Markdown defines the product contract
I used Markdown files to define:
- rules
- schemas
- operating assumptions
- workflow logic
- runtime boundaries
- product/system decisions

That let me use AI to reason against explicit artifacts rather than constantly re-describing intent in chat.

### 2. Build the smallest real loop first
Instead of overdesigning the whole platform, I pushed toward a real proof loop:
- read Gmail
- classify signals
- reconcile against tracker truth
- write to Google Sheets
- sync local mirrors
- log the run
- render an operator-facing UI

Once that loop was real, I started modularizing it.

### 3. Separate logic, runtime, storage, and UI
A major architectural direction in this repo was to avoid collapsing everything into one app layer.

The system is intentionally split into:
- Markdown logic/contracts
- Python runtime modules
- storage/mirror layers
- React UI surfaces

### 4. Keep product intent visible during implementation
I did not want the project to become “just a script” or “just a dashboard.”
The product goal stayed consistent: an operator system that turns fragmented search activity into actionable, verified state.

## Key architectural decisions

## 1. Source-of-truth split
One of the most important design choices was establishing a clean truth model:
- **Google Sheets** = live operational truth
- **Gmail / Calendar / job boards** = evidence sources
- **local artifacts** = structured mirrors and runtime state
- **git/GitHub** = version history and persistence
- **Google Drive** = mirrored access layer for important docs

This matters because AI-generated systems get messy quickly if truth boundaries are fuzzy.

## 2. Markdown-first system design
A large amount of the platform logic was first expressed in Markdown.

Examples include:
- root operating files like `MISSION.md`, `CURRENT.md`, `DECISIONS.md`, `MEMORY.md`
- runtime rules in `job-search-ui/docs/`
- architecture and data-spec docs under `JT7/`
- contract files like `ACTIONS.md`, `TODAYS_PLAN.md`, and `RUNTIME_BOUNDARIES.md`

That gave me durable, reviewable logic surfaces that AI could use as working context.

## 3. Vertical slice before modular extraction
I first built JT7 as a working vertical slice.
That included a large orchestration script, live tracker writes, runtime reports, mirrors, and UI wiring.

Once the loop was real, I started extracting modules.
That was intentional.
I wanted to avoid abstract architecture that had never touched real data.

## 4. Phase-based modularization
After the working loop existed, I started refactoring toward a more composable runtime.

Examples of extracted modules now include:
- `runtime/domain/actions.py`
- `runtime/domain/jobs.py`
- `runtime/domain/signals.py`
- `runtime/services/action_generation.py`
- `runtime/services/action_lifecycle.py`
- `runtime/services/signal_lifecycle.py`
- `runtime/services/reconciliation.py`
- `runtime/storage/local_mirror.py`
- `runtime/adapters/homepage_state.py`
- `runtime/pipelines/todays_plan.py`

This reflects how I use AI in practice:
- get a real loop working
- inspect the monolith honestly
- extract the safest boundaries first
- verify behavior after each refactor

## Key UX and product design decisions

## 1. Treat the interface as an operator surface, not a dashboard
A major UX choice was to avoid generic analytics-heavy dashboard behavior.

Instead, the Today surface was designed to answer:
- what matters now
- what should happen next
- what is blocked
- what is waiting
- what evidence supports that recommendation

That is why the interaction model emphasizes:
- one dominant next best action
- a small supporting action set
- calm spacing
- plain language
- minimal jargon
- fast scanability

## 2. Calm, enterprise-like visual direction
The visual/product direction was intentionally:
- dark-mode-first
- quiet
- structured
- information-forward
- low-noise
- similar in spirit to enterprise control surfaces rather than consumer dashboards

## 3. Verified-state rendering
Another key UX decision was that the UI should render verified system state, not raw ingestion noise.

That means the UI is downstream of:
- classified signals
- tracker state
- action rules
- runtime artifacts

not just “whatever was found in an email.”

## 4. Persona and workflow awareness
This repo also includes persona and workflow thinking, not just raw code.

Examples:
- user/persona files under `career/personas/`
- system/operator behavior files at the root
- structured workflow docs for ingestion, pass logging, storage, and task execution

This reflects my design bias that a product system is not complete unless user framing, system behavior, and execution logic are coherent together.

## Scaffolding and component decisions

## Logic scaffolding
I used AI to create and refine the document/control structure first:
- mission/state/memory/decision files
- roadmap and schema files
- docs that defined execution rules and storage rules
- contract artifacts for runtime modules

## Runtime scaffolding
The Python runtime started as a working orchestrator and then evolved into extracted modules.
That allowed fast proof-of-life first, followed by cleaner architecture.

## App scaffolding
The UI was built as a React + TypeScript + Vite app with a thin operator surface.
I intentionally preserved route structure and existing auth boundaries during later UI work instead of rewriting the app shell.

## Component approach
The Today surface was broken into focused components such as:
- `TodayPlanPage`
- `NextBestAction`
- `ExecutionCard`
- `CompletedToday`
- `SignalNotes`
- `ProgressStrip`

That reflects a common pattern in my work:
- define a clear content contract
- compress the UX to the essential decisions
- keep components small and composable

## Workflow design approach

JT7 was designed around workflows rather than around isolated screens.

Examples of workflow thinking in this repo:
- Gmail ingestion and classification rules
- signal-to-job linking
- action generation
- review-needed handling
- scheduled refresh runs
- local mirror and git persistence
- Today’s Plan derivation from canonical runtime state

This matters because the system is fundamentally about turning asynchronous evidence into reliable next actions.

## Data, git, and persistence approach

I wanted the system to leave behind a durable trail of what happened.

That meant treating persistence as part of the product, not an implementation detail.

The repo reflects that through:
- structured tracker rows in Google Sheets
- mirrored CSV/JSON artifacts locally
- runtime reports in `job-search-ui/runtime/reports/`
- task state in runtime JSON files
- git commits capturing meaningful execution changes and checkpoints

This is one of the clearest ways AI was used pragmatically: not just generating files, but helping maintain a system where state, outputs, and rules stay inspectable.

## What to look at in the repo

If you want to understand how I used AI to build this, the best areas are:

### Root control files
- `README.md`
- `MISSION.md`
- `CURRENT.md`
- `DECISIONS.md`
- `MEMORY.md`

### Product and system specs
- `JT7/`
- `product/`
- `docs/`

### Runtime logic
- `job-search-ui/scripts/run_jt7_chain.py`
- `job-search-ui/runtime/`
- `job-search-ui/docs/`

### UI surface
- `job-search-ui/src/`
- especially the Today feature and selector layer

### Personas and user framing
- `career/personas/`

## What this project demonstrates about my approach

I use AI best when the work requires:
- structuring ambiguity
- making logic explicit
- preserving continuity
- rapidly scaffolding and testing ideas
- moving between product design and implementation detail
- iterating from working loops to cleaner architecture

This repo is a good example of that.
It is not “AI wrote some code for me.”
It is a system where I used AI as part of a disciplined product design and build process.

## Summary

JT7 shows how I approach AI-assisted product building:
- define the system clearly
- externalize logic in durable artifacts
- use AI to accelerate structure and implementation
- prove the workflow with real data
- refactor toward better architecture once reality is known
- keep UX grounded in verified state and operator needs

For a more operator-facing technical overview of the live runtime, see:
- `README.md`
