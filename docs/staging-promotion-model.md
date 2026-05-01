# Staging Promotion Model

## Purpose
Define how staged direct-board opportunities move into canonical `Jobs` tracker state.

## Core Rule
Staging is intake. Canonical `Jobs` is trusted tracker state.
A staged row should never create silent duplicate tracker truth.

## Decision Paths

### 1. Promote new canonical job
Use when:
- duplicate check finds no canonical match
- fit/ranking clears threshold
- a human or trusted rule accepts the opportunity

Result:
- create a new canonical job row/state record
- preserve provenance from staging
- mark staging item as reviewed/promoted

### 2. Merge into existing canonical job
Use when:
- duplicate check finds a likely canonical match
- the staged row adds useful provenance, link, or freshness
- the staged item does not justify a separate job row

Result:
- update the existing canonical job with staged provenance/evidence
- do not create a new canonical job row
- mark staging item as merged/reviewed

### 3. Hold for manual review
Use when:
- duplicate risk exists but confidence is not high enough to merge automatically
- fit is unclear
- role/location signals are mixed

Result:
- keep staged item out of canonical `Jobs`
- preserve notes about why it is blocked

### 4. Reject
Use when:
- role is weak-fit or outside search constraints
- staging row is noisy, redundant, or irrelevant

Result:
- do not create or update canonical `Jobs`
- keep rejection traceability in staging history

## Current Local MVP Behavior
- no duplicate -> local promote creates a review-state job
- likely duplicate -> local merge updates the existing local job instead of creating a new one
- ambiguous -> hold
- weak fit -> reject or hold based on operator judgment

## Next Runtime Step
Move this model from local cockpit state into real tracker writeback with explicit Sheets-side staging/canonical handling.
