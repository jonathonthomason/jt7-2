# Direct Board Import Policy

## Decision
Use a **separate staging layer** for direct-board imports.
Do **not** write broad direct-board imports directly into canonical `Jobs` tracker state.

## Why
The 2026-04-30 pass showed that broad direct imports can produce a large local-only delta (`184` appended rows) that is too noisy to be treated as trusted tracker truth.

## Policy
### Canonical truth
- Google Sheets `Jobs` remains the canonical system of record.
- Canonical `Jobs` should contain only trusted opportunities.

### Direct-board staging
- direct-board imports should land in a staging layer, not canonical `Jobs`
- staging may be represented locally first, but the target model should be a dedicated staging surface/tab
- staging rows must preserve source, evidence link, and import provenance

### Promotion rule
Promote from staging into canonical `Jobs` only after:
1. fit/ranking filters run
2. duplicate checks pass
3. confidence is high enough or a human confirms

## Rejected alternatives
### Local staging only
Rejected as the long-term default because it creates silent divergence between local operational state and the Sheets system of record.

### Direct filtered promotion into Jobs
Rejected for now because filters are not mature enough and risk polluting canonical tracker state.

## Current recommendation
- near term: keep broad import rows out of canonical `Jobs`
- staging promotion should happen one item at a time through the explicit runtime writeback path, not bulk import
- next implementation target: create an explicit staging layer for direct-board imports
- JobOps should operate on staged import data as intake, not as trusted state by default
