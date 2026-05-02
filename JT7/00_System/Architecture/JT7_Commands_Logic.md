# JT7 Commands Logic

## jt7execute

Autonomous execution mode.
Select highest-leverage next action.
Execute within safe boundaries.
Validate result.
Return proof + next action.
Always move toward end-to-end working system.

### Full command behavior

Continue from your last response.

Goal:
Move JT7 toward a reliable working product, with priority on a successful end-to-end chain run.

Operate autonomously within this boundary:
You may make small, safe code/config/doc updates without approval when they clearly move toward:
- end-to-end chain reliability
- phase completion
- operator product readiness
- roadmap-aligned runtime hardening

Do not ask for approval unless the action is:
- destructive
- credential/billing related
- externally sending messages
- changing canonical data in Google Sheets
- broad architecture rewrite
- outside the current JT7 roadmap

Before acting, choose the highest-leverage next move by asking:
“What action most directly reduces uncertainty or moves the system toward a working end-to-end product?”

Then execute it.

### Return

1) ACTION TAKEN
- what you chose
- why it was highest leverage

2) RESULT
- what changed
- pass/fail
- first failure point, if any

3) PROOF
- files changed
- commands run
- report/output path

4) GOAL PROGRESS
- how this reduced drift, risk, or uncertainty
- how it moves phase completion or product readiness forward

5) NEXT ACTION
- exactly one next autonomous step

### Rules
- no multiple options
- no vague planning
- no unrelated cleanup
- no scope expansion
- prefer fixing the first failing boundary
- prefer validation over polish
- prefer working product over perfect architecture

## JT7_EXECUTE_BLOCK

Goal:
Move JT7 meaningfully toward a working end-to-end system in a single execution block.

Mode:
Autonomous. Multi-step. Controlled.

---

STEP 1 — RAPID AUDIT (no more than 5 bullets)

- current working components
- first failing boundary
- biggest risk to end-to-end execution
- any drift from roadmap/phase goal
- what must NOT be touched

---

STEP 2 — TACTICAL PLAN (max 3–5 steps)

Create a short execution plan where:
- each step is small but meaningful
- all steps together move toward end-to-end success
- steps are logically connected (not random fixes)

Must prioritize:
- unblocking execution
- validating system behavior
- restoring reliability

---

STEP 3 — EXECUTE BLOCK

Execute the plan in sequence.

You may:
- modify code
- run commands
- fix adjacent issues IF directly blocking flow

You may NOT:
- refactor broadly
- change architecture direction
- touch unrelated areas

Stop execution early if:
- a new critical failure appears
- risk increases
- system behavior becomes unclear

---

STEP 4 — VALIDATION

- run the system (or closest possible end-to-end path)
- identify:
 - did we get further than before?
 - what is now the first failing boundary?

---

STEP 5 — REPORT

1) ACTIONS TAKEN
- list of steps executed

2) RESULT
- what now works
- what still fails

3) PROOF
- files changed
- commands run
- report/output path

4) PROGRESS
- how far closer to full end-to-end success (rough %)

---

STEP 6 — NEXT BLOCK

Provide the next execution block (NOT a single step):

NEXT BLOCK:
- 2–4 steps max
- tightly focused on the new first failing boundary

---

Rules:

- prioritize working system over clean system
- prioritize momentum over perfection
- no infinite loops of micro-fixes
- no unrelated improvements
- no waiting for user unless truly blocked
