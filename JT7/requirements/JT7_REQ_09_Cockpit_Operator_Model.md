# JT7 — Cockpit Operator Model

## Purpose
Define the JT7-2 cockpit as the operator workspace that separates untrusted intake from trusted operational state.

## Core Product Framing
JT7 is not merely a dashboard.

JT7-2 uses an operator cockpit model:
- signals are reviewed
- opportunities are operated
- intelligence learns from operator decisions and outcomes

## Architectural Boundary
### JT7 Scope
JT7 acts as the system architect and platform builder.

Primary responsibilities:
- implement the `job-search-ui` React/TypeScript platform
- refine business requirements into buildable behavior
- maintain the synchronization layer between Google Sheets, markdown mirrors, and the OpenClaw gateway

### JobOps Scope
Once the platform is solid, JobOps becomes the primary operational user of the cockpit for:
- Gmail signal triage
- recruiter follow-ups
- interview scheduling
- daily pipeline operations

### Handoff Model
- JT7 builds the cockpit
- JobOps pilots the cockpit
- JT7 is the engineer
- JobOps is the pilot

## Trust Boundary
The cockpit has two layers.

### Untrusted Intake Layer
Contains:
- raw signals
- inferred metadata
- duplicate candidates
- ambiguous recruiter/job signals

### Trusted Operational Layer
Contains:
- verified opportunities
- accepted contacts
- active next actions
- event history tied to real records

### Rule
A record must not enter the main dashboard/pipeline as a true opportunity until it passes verification or is explicitly created by the operator.

## First Surface
### Review Queue
The first cockpit surface to build is the Review Queue.

Reason:
- it is the trust gateway
- it reduces false-positive contamination
- it aligns with Execution Layer Hardening
- it creates cleaner downstream opportunity state

## Core Screens
1. Review Queue
2. Pipeline Overview
3. Opportunity Detail

## Core Object Model
### Trusted objects
- Opportunity
- Contact
- NextAction
- Event

### Untrusted/pre-trusted objects
- Signal
- inferred signal metadata pending review

## Source Link Requirement
All major cockpit records must preserve direct operational links.

### Opportunity links
- job posting URL
- application URL
- company careers URL
- canonical source URL
- tracker URL

### Signal links
- source message URL
- source thread URL
- posting URL
- sender profile URL
- evidence URL

### Contact links
- LinkedIn URL
- email thread URL
- company profile URL

## Event Logging Requirement
Every meaningful cockpit action must create:
- a current-state update when applicable
- an immutable event record

Event records should preserve:
- action type
- timestamp
- actor
- prior state
- new state
- reason/note when available

## Intelligence Implication
Cockpit event history is a required future input for:
- parser improvement
- source quality scoring
- recruiter quality analysis
- opportunity conversion analysis
- recommendation generation
- stall/risk detection

## Build Order
1. Review Queue
2. trusted-state model wiring
3. Pipeline Overview
4. Opportunity Detail
5. broader intelligence consumption

## Product Rule
Signals are reviewed.
Opportunities are operated.
Intelligence learns from the history.
