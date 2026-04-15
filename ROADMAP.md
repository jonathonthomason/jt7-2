# ROADMAP.md

## Roadmap Metadata
- **System:** JT7
- **Roadmap version:** 2.0
- **Purpose:** define the active multi-phase build plan for JT7 as an operating system and future product
- **Current phase:** Phase 6 — Productization / Unified Platform Refactor
- **Current step:** JT7-R2.6.2

# JT7 ROADMAP 2.0

## Phase 1 — Core Activation
- **Status:** complete
- **Objective:** establish the operating core

### Steps
- [x] **JT7-R2.1.1** — IDENTITY.md, USER.md
- [x] **JT7-R2.1.2** — AGENTS.md
- [x] **JT7-R2.1.3** — HEARTBEAT.md

---

## Phase 2 — Workstreams
- **Status:** complete
- **Objective:** establish the first active workstream layer

### Steps
- [x] **JT7-R2.2.1** — career, product, ops files

---

## Phase 3 — Canonical Data Layer
- **Status:** complete
- **Objective:** define structured schemas, align files to canonical models, and introduce derived state

### Steps
- [x] **JT7-R2.3.1** — schema definitions
- [x] **JT7-R2.3.2** — schema → file alignment
- [x] **JT7-R2.3.3** — derived state layer

---

## Phase 4 — Integrations
- **Status:** complete
- **Objective:** define the minimum useful external integration and ingestion layer

### Steps
- [x] **JT7-R2.4.1** — Google (gog)
- [x] **JT7-R2.4.2** — Gmail ingestion
- [x] **JT7-R2.4.3** — minimal ingestion layer
- [ ] **JT7-R2.4.4** — Browser layer (LinkedIn, Indeed, BuiltIn)

---

## Phase 5 — UI Layer
- **Status:** complete
- **Objective:** create a minimal UI that renders the operating system cleanly

### Steps
- [x] **JT7-R2.5.1** — UI IA definition
- [x] **JT7-R2.5.2** — minimal shell
- [x] **JT7-R2.5.3** — Now tab
- [x] **JT7-R2.5.4** — Pipeline tab
- [x] **JT7-R2.5.5** — Actions tab

---

## Phase 6 — Productization
- **Status:** in_progress
- **Objective:** turn JT7 from an internal system into a product-ready artifact set

### Steps
- [x] **JT7-R2.6.1** — first live import / MVP proof foundation
- [x] **JT7-R2.6.2** — unified multi-surface platform model
- [ ] **JT7-R2.6.3** — runtime proof-of-life loop
- [ ] **JT7-R2.6.4** — deployment stabilization
- [ ] **JT7-R2.6.5** — product-facing artifact consolidation

## Operating Rules
- every task should map to a roadmap label
- completed work should update this file
- current step should be visible at the top of the roadmap
- downstream work should not start before prerequisite structure exists unless explicitly justified

## Immediate Focus
- **Current execution target:** JT7-R2.6.3
- **Phase goal:** activate the unified five-surface platform model in runtime-safe form while continuing toward a trustworthy Gmail → Processing → Sheets end-to-end loop
- **Why now:** the platform structure has been refactored around one shared core and five surfaces; the next gap is runtime activation and verification, not more surface ambiguity
