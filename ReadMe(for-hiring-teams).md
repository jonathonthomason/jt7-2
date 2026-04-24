# JT7 (for hiring teams)

A job search is operationally messy. Signals arrive through email, calendar, job boards, recruiter replies, and spreadsheets. Most people handle that with fragmented tools and manual memory.

I treated it as a product problem — and built the system I wished existed.

---

## What it is

JT7 is a personal AI-operated job search platform I designed and built from scratch. It runs on a scheduled pipeline that ingests signals from Gmail, Google Calendar, and job boards, reconciles them against a live tracker, generates prioritized actions, and surfaces them through a React operator UI.

It is a working system. It runs three times a day. I use it daily.

---

## Why it exists

I approached the job search the same way I approach enterprise workflow problems:

- separate evidence from truth
- make logic explicit and durable
- keep state inspectable
- build calm execution surfaces
- reduce cognitive load through structure, not willpower

The result is a system where AI is not just generating text — it is helping maintain contracts, enforce boundaries, and preserve continuity across a live product.

---

## How I used AI to build it

JT7 was built using a multi-model agentic workflow.

### Phase 1 — Build with OpenClaw + GPT (Codex)
The core system was built using OpenClaw, an agentic CLI framework running GPT/Codex as the execution engine.

My process:

1. Define the operating model in Markdown first
2. Use structured prompting to turn vague ideas into explicit contracts, schemas, and rules
3. Scaffold implementation around those contracts
4. Build the smallest real working loop first — then modularize
5. Refactor toward cleaner architecture once real data proved the model

### Phase 2 — Architecture review with Claude Code
Once the system was running, I brought Claude Code in as a second pass — pointed directly at the live repo.

I used it to:
- audit the runtime architecture against the original contracts
- pressure-test the task chain logic
- surface refactor opportunities in the module boundaries
- validate that the system behaved as designed, not just as coded

This reflects how I think about AI tooling in practice: different models have different strengths. OpenClaw + Codex is fast and execution-oriented. Claude Code is strong at reasoning about existing systems and surfacing structural issues.

Using both — in sequence, with clear intent — produced a more reliable system than either would have alone.

---

## Architecture

### Source of truth model
- **Google Sheets** — live operational tracker truth
- **Gmail / Calendar / job boards** — evidence sources
- **Local artifacts** — structured mirrors and runtime state
- **Git / GitHub** — version history and persistence

### System layers
- **Logic layer** — Markdown files defining rules, schemas, workflow contracts, and operating assumptions
- **Runtime layer** — Python modules handling ingestion, classification, reconciliation, action generation, and scheduled execution
- **Application layer** — React + TypeScript + Vite operator UI

### Scheduled task chain
Runs at 8:30 AM, 12:30 PM, and 6:00 PM CT:

`EMAIL_SIGNAL_SCAN → CALENDAR_SIGNAL_SCAN → JOB_BOARD_SIGNAL_SCAN → SIGNAL_CLASSIFICATION → PIPELINE_STATE_SYNC → PIPELINE_UPDATE → ACTION_GENERATION → PRIORITY_SURFACING → PASS_LOGGER`

---

## Core build philosophy

### Markdown defines the product contract
I used Markdown files to define rules, schemas, operating assumptions, workflow logic, and runtime boundaries. That let me use AI to reason against explicit artifacts rather than constantly re-describing intent in chat.

### Build the smallest real loop first
Instead of overdesigning, I pushed toward a real proof loop: read Gmail → classify signals → reconcile against tracker → write to Sheets → sync mirrors → log the run → render UI. Once that loop was real, I modularized it.

### Separate logic, runtime, storage, and UI
The system is intentionally split into Markdown logic/contracts, Python runtime modules, storage/mirror layers, and React UI surfaces. Collapsing these into one layer is where AI-assisted systems get messy fast.

---

## UX decisions

The operator UI was designed around one question: *what should happen next, and why?*

- One dominant next best action
- A small supporting action set
- Verified system state — not raw ingestion noise
- Calm, information-forward visual direction
- Fast scanability over analytical depth

The UI is downstream of classified signals, tracker state, and action rules. It renders what the system knows — not what it guesses.

---

## Key files

| Area | Path |
|---|---|
| Operating model | `MISSION.md`, `CURRENT.md`, `DECISIONS.md`, `MEMORY.md` |
| Runtime chain | `job-search-ui/scripts/run_jt7_chain.py` |
| Runtime modules | `job-search-ui/runtime/` |
| UI surface | `job-search-ui/src/` |
| System specs | `JT7/`, `product/`, `docs/` |

---

## What this demonstrates

- Product systems thinking applied outside a client context
- Multi-model agentic workflow — OpenClaw + GPT for build, Claude Code for architecture review
- Full-stack execution: Markdown contracts → Python runtime → React UI
- Source-of-truth architecture for async, multi-source data
- UX grounded in operator needs, not dashboard aesthetics

---

## Quick start

```bash
# Run the app
cd job-search-ui
npm install && npm run dev

# Run the task chain manually
python3 job-search-ui/scripts/run_jt7_chain.py
```

---

Built by [Jonathon Thomason](https://jonathonthomason.com)
