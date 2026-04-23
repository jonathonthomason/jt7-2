# Project Recenter

## Project

- Name: job-search-ui
- Absolute path: /Users/jtemp/.openclaw/workspace/job-search-ui
- Purpose: Local runnable MVP job-search app for proving the front-end shell, mock data flow, and route structure.

## Current State

The app is a local React + TypeScript + Vite MVP with MSW-backed mock job data, React Router routes, and a demo-auth protected dashboard shell. The repo, persona system, storage rules, and GitHub/Google auth foundations are in place, but proof-of-life is still incomplete because Playwright smoke verification has not passed cleanly and runtime port contention has caused unstable local verification.

### What is working
- App code exists locally and in git
- React Query global provider is active
- MSW mock layer is wired into startup
- Jobs list route exists and fetches mock data
- Job detail route exists and fetches a single mock job
- Companies route exists
- Sign-in route exists
- Protected dashboard route logic exists
- Build succeeds

### What is partially working
- Local dev runtime works, but port contention has caused repeated start conflicts
- Preview runtime works, but exact preview verification has not been consistently clean
- Playwright config and smoke test exist, but end-to-end proof is incomplete

### What is broken or unverified
- Stable verification on exact locked ports is not confirmed
- Playwright smoke test is not passing cleanly
- Browser-verified click-through from jobs list to detail is not fully confirmed in automated proof

## Tech Stack

- Framework: React
- Language: TypeScript
- Build tool: Vite
- Router: React Router DOM
- Testing: Vitest, Playwright
- Mock/data layer: MSW + local JSON fixture
- Ports (dev + preview): 5173, 4173

## Features (Current Only)

- Jobs list
  - status: working
  - description: Fetches and renders job links from MSW mock API data.
- Job detail
  - status: working
  - description: Fetches and renders a single mock job by ID.
- Company route
  - status: working
  - description: Renders a simple company slug page.
- Demo auth
  - status: working
  - description: Uses `demo_auth` in localStorage to gate protected routes.
- Protected dashboard
  - status: working
  - description: Redirects signed-out users to sign-in and renders placeholder dashboard content when signed in.
- Mock API
  - status: working
  - description: Intercepts `/api/jobs` and `/api/jobs/:jobId` through MSW.
- Playwright smoke test
  - status: partial
  - description: Config and test file exist, but clean passing proof is not currently established.

## Routes

- `/jobs` — working
- `/jobs/:jobId` — working
- `/companies/:slug` — working
- `/auth/sign-in` — working
- `/app/dashboard` — working
- `* -> /jobs` — working

## Key Files

- `package.json` — defines scripts, dependencies, and testing commands
- `vite.config.ts` — defines Vite runtime config and target ports
- `.env` — enables MSW
- `src/main.tsx` — bootstraps MSW and the React Query provider
- `src/App.tsx` — contains the active route shell and page logic
- `src/mocks/browser.ts` — MSW browser worker setup
- `src/mocks/handlers.ts` — API handlers for mock job endpoints
- `src/mocks/fixtures/jobs.json` — current job fixture data
- `playwright.config.ts` — preview-backed browser test config
- `tests/smoke.spec.ts` — smoke test for the Jobs page
- `docs/mvp-build-brief.md` — current MVP brief
- `docs/local-git-drive-rules.md` — local/git/drive logic rule file

## Runtime

- dev command: `npm run dev`
- preview command: `npm run preview`
- test command: `npm run test:e2e`
- working URLs:
  - `http://127.0.0.1:5173/jobs` (target)
  - `http://127.0.0.1:4173/jobs` (target)
- latest verified results:
  - `npm run build` passed
  - preview server has started locally
  - smoke test file exists but full pass is not cleanly verified

## Blockers

- Port contention on 5173 and 4173 has caused unstable verification
- Playwright smoke proof is not yet cleanly passing
- End-to-end browser proof for the exact locked-port MVP sequence remains incomplete

## Next Steps (Top 5)

1. Stabilize dev startup on port 5173 with no conflicting process
2. Stabilize preview startup on port 4173 with no conflicting process
3. Re-run and fix Playwright smoke until it passes cleanly
4. Confirm browser click-through from jobs list to job detail
5. Expand mock fixture and UI from markdown-guided logic for jobs, recruiters, and related tracking entities

## Roadmap (High Level)

- Phase 1: stabilize MVP
- Phase 2: product features
- Phase 3: tracking system
- Phase 4: dashboard/operator layer
- Phase 5: integrations

## Resume Instructions

```bash
cd /Users/jtemp/.openclaw/workspace/job-search-ui
npm install
npm run build
npm run dev
npm run preview -- --host 127.0.0.1 --port 4173
npm run test:e2e
```
