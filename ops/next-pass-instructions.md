# Next Pass Instructions

## Intent
Pick up from a clean checkpoint after Review Queue v1 and the 2026-04-30 scrub/import pass.
Do not start with another broad rerun unless code changes require it.

## Current State Snapshot
- Latest runtime scrub completed successfully on `2026-04-30 06:25 CDT`.
- Review Queue v1 is implemented in `job-search-ui` and verified.
- Direct board import tooling is now live locally.
- A follow-up git commit is expected to capture Review Queue code, docs, and direct-board mirror changes.
- Latest successful runtime report:
  - `job-search-ui/runtime/reports/jt7_run_2026-04-30T06-25-52.962534-05-00.json`
- Latest direct board import preview:
  - `job-search-ui/runtime/direct_board_import_preview.json`

## What Changed Most Recently
- Added Review Queue domain/state/action/event scaffolding under `job-search-ui/src/domain/cockpit/`.
- Added `/review-queue` as the default landing route.
- Wired Review Queue list/detail/actions into the MVP shell.
- Ran the JT7 chain manually and refreshed runtime mirrors.
- Ran direct board import across accessible sources and appended proposed jobs into local `Jobs.csv` / `Jobs.json`.

## Latest Known Outcomes
### Review Queue build
- `npm run build` ✅
- `npm run test:e2e -- tests/smoke.spec.ts` ✅

### Runtime scrub
- Gmail scan created `10` jobs and updated `4`
- `34` signals persisted
- `20` review-needed rows created
- `5` existing noisy signals cleaned
- Review Queue pending count reached `76`

### Direct board import
- matches considered: `253`
- jobs proposed/appended locally: `184`
- duplicate skips: `69`
- accessible sources: Built In, LinkedIn, Greenhouse
- blocked source: Indeed (`Just a moment...` anti-bot wall)

## Highest-Leverage Next Work
1. Tighten direct-board filtering before another import pass.
   - Prefer senior/principal/staff/lead product design roles.
   - Prefer remote + DFW relevance.
   - Exclude clearly off-track roles and non-target geographies when query intent is remote.
2. Improve Review Queue prioritization so imported opportunities do not overwhelm operator attention.
3. Decide whether direct imports should write into Sheets automatically or stay local-first until filters improve.
4. Normalize Drive mirror updates so canonical docs refresh in place.

## Guardrails For The Next Pass
- Avoid another full chain rerun unless code changed.
- Avoid committing browser profile churn.
- Keep staging selective; there are unrelated workspace changes outside this pass.
- Treat Indeed as blocked until the anti-bot path is intentionally addressed.
- Prefer ranking/filtering work over adding more raw sources.

## Recommended First Move Next Time
Open `job-search-ui/runtime/direct_board_import_preview.json` and define the filter/ranking rules that would cut today’s 184 appended rows down to a high-signal apply set.
