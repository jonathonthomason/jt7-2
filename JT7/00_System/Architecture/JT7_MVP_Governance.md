# JT7 MVP Governance

## Document Metadata
- **System:** JT7 Job Intelligence System
- **Document type:** MVP governance reference
- **Status:** active
- **Primary path:** `JT7/00_System/Architecture/JT7_MVP_Governance.md`

## Purpose
This document is the governing reference for JT7's current MVP operating model.

Its job is to reduce future conflict by defining the winning interpretation when older docs, richer schemas, or legacy workflow assumptions disagree with current MVP reality.

## Governing Rules

### 1. Operational Source of Truth
- Google Sheets is the single operational source of truth for live JT7 tracker state.
- Markdown files are architecture, governance, memory, roadmap, and audit artifacts.
- Gmail, Calendar, and manual input are evidence sources, not truth stores.

### 2. Canonical Google Capability Layer
- `gog` is the canonical Google capability layer for JT7.
- Personal Google OAuth user auth is the correct auth model for this JT7 instance.
- Gmail read/search, Sheets read/write, and Drive read/write are only considered accessible when all four pass:
  1. auth
  2. tool availability
  3. runtime execution
  4. command-path verification

### 3. Execution Surface Rule
- Telegram must not be assumed to be a valid execution surface unless explicitly verified.
- Runtime proof is determined by actual executable capability, not architecture intent.

### 4. Layer Ownership
#### Intake Layer
- collects and structures raw signals only
- does not assign status
- does not write tracker truth

#### Processing Layer
- owns classification
- owns matching
- owns deduplication
- owns confidence
- owns status interpretation
- owns next-step generation

#### System of Record
- stores and updates tracker state only
- does not interpret evidence

#### Interaction Layer
- surfaces state, suggestions, edits, and drafts
- does not own processing logic

### 5. Shared MVP Schema
The governing shared schema is:
- `company`
- `role`
- `status`
- `last_activity`
- `next_step`
- `contact`
- `source`
- `thread_id`
- `notes`

Richer internal or legacy structures are allowed only as implementation/reference layers and must not override this MVP model.

### 6. Final Opportunity Status Model
Only these statuses should be treated as the final live JT7 opportunity status model:
- Applied
- Recruiter Contacted
- Screening
- Interviewing
- Offer
- Rejected
- Cold

Legacy states such as `lead`, `saved`, `researching`, and `archived` must be normalized away in live operational use.

### 7. Evidence-to-Status Mapping
- application confirmation -> Applied
- recruiter outreach -> Recruiter Contacted
- interview scheduling -> Interviewing
- rejection -> Rejected
- offer -> Offer
- weak job alert / recommendation -> Cold unless stronger evidence appears

### 8. Write Safety Rule
A live JT7 loop is only considered valid when it can:
1. read source evidence
2. classify it
3. read tracker state
4. match the correct record
5. write the necessary change
6. verify the resulting state after write

If post-write verification is missing, proof-of-life is not complete.

### 9. Conflict Resolution Rule
If an older file conflicts with this MVP governance doc:
- this file wins
- older file should be marked as partially legacy until rewritten

### 10. Drift Prevention Rule
Future JT7 changes must not introduce:
- alternate live tracker truth stores
- alternate status vocabularies for the same opportunity state
- layer ownership overlap
- runtime claims without verified capability

## Current MVP Objective
Prove one trustworthy end-to-end loop:
- Gmail / Calendar / manual input
- Intake
- Processing
- Google Sheets writeback
- Interaction-layer reporting

This proof-of-life loop remains explicitly in scope during cleanup and governance work. Cleanup is only considered complete enough when runtime proof becomes the primary remaining blocker rather than documentation conflict.

## Current Blocker
The main blocker is runtime execution reliability, especially from Telegram/OpenClaw, not conceptual architecture.

## Usage
Use this file as the governing reference whenever:
- docs disagree
- status terms drift
- source-of-truth assumptions conflict
- runtime readiness is being assessed
- new JT7 module logic is being added or reviewed
