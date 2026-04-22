# MVP Build Brief

## Purpose
Current source of truth for the running MVP.

This brief is archival and expected to become obsolete quickly.

---

## Goal
Build a local runnable job-search MVP that proves the front-end shell works.

---

## MVP Stack
Use:
- React
- TypeScript
- Vite
- React Router
- TanStack Query
- Tailwind
- MSW
- Vitest
- Playwright

This stack is already established in the files and is good enough for MVP.

---

## MVP Routes
Build only these routes now:
- `/jobs`
- `/jobs/:jobId`
- `/companies/:slug`
- `/auth/sign-in`
- `/app/dashboard`

That is the correct minimum app shell.

---

## MVP Behavior
Implement only this behavior:
- jobs list fetched from MSW
- job detail fetched from MSW
- sign-in page with demo auth
- protected dashboard route
- local dev run on localhost
- production preview run
- one working smoke test

---

## Exact Files to Create Now
Use the starter file set already defined in the uploaded report:
- `package.json`
- `vite.config.ts`
- `tsconfig.json`
- `src/main.tsx`
- `src/App.tsx`
- `src/mocks/browser.ts`
- `src/mocks/handlers.ts`
- `src/mocks/fixtures/jobs.json`
- `.env.example`
- `playwright.config.ts`
- `tests/smoke.spec.ts`
- `Dockerfile`
- `.github/workflows/ci.yml`

These are the files that convert the brief into something actually runnable.

---

## Proof-of-Life Requirements
The MVP is considered live only when all of these pass:
- `npm run dev`
- `http://localhost:5173/jobs` loads
- `http://localhost:5173/jobs/job_001` loads
- `http://localhost:5173/auth/sign-in` loads
- `/app/dashboard` redirects when signed out
- `npm run build`
- `npm run preview`
- `http://localhost:4173/jobs` loads
- Playwright smoke test passes

That exact sequencing is already laid out in the report.

---

## Not in MVP Yet
Do not let the agent drift into these yet:
- full OpenAPI coverage
- richer fixtures
- Storybook
- full i18n
- accessibility hardening pass
- advanced dashboard modules
- notifications/messages/schedule
- real Gmail/Sheets/JT7 ingestion
- host-specific deployment polish beyond basic preview/build

These are roadmap items after MVP works.

---

## Git Rule
After each successful stage:
```bash
git add .
git commit -m "step: <what was completed>"
```

Examples:
```bash
git add .
git commit -m "step: scaffold complete"
git add .
git commit -m "step: routes and mocks working"
```
