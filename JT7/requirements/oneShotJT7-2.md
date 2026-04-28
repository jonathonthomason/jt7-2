
Operate in JT7 v1.5 MVP execution mode.

Goal:
Build a functioning JT7 MVP with parity to the original JT7 direction.

Underlying principle:
Do not separate UI from logic. Build functional UI components and interaction flows while wiring the existing documented logic already present in the repo.

Use existing repo Markdown docs as the source of truth for:
- signal logic
- Gmail ingestion logic
- job board logic
- recruiter tracking
- application tracking
- Today’s Plan logic
- scheduler / task run logic
- state persistence
- action generation

Do not rebuild from shallow assumptions.
First locate and use the existing docs.

BUILD THE FULL MVP FLOW:

1. Global Shell
- Persistent left nav
- EXECUTE / MANAGE / INTELLIGENCE / SYSTEM groupings
- Top header
- Context switcher: JT Personal / Job Search
- Command/search input
- Notifications/signal tray
- Right detail panel

Routes:
- /execute/today
- /manage/jobs
- /manage/recruiters
- /manage/outreach
- /manage/messages
- /intelligence/competition
- /intelligence/wiki
- /intelligence/reports
- /design-system/components
- /design-system/foundations
- /settings

2. State Store
Create or wire a local MVP state layer.

Use local JSON if needed:
- data/state.json

Track:
- signals
- jobs
- recruiters
- outreach
- messages
- actions
- taskRuns
- completed actions
- waiting/deferred actions

All UI actions must mutate this state.

3. Signal System
Implement functional Signal Cards for:
- Gmail/recruiter messages
- job board opportunities
- applied job confirmations
- application status updates
- follow-up reminders
- system/task alerts

Signal card fields:
- type
- source
- timestamp
- priority
- related company
- related role
- related recruiter/contact
- summary
- why it matters
- status
- primary action
- secondary actions

Sources must support:
- Gmail
- LinkedIn
- Indeed
- Otta / Welcome to the Jungle
- Workday
- Greenhouse
- company career pages
- manual entry

If real integration is not currently available, create structured MVP adapters/mocks that match the documented logic and can later be swapped for real ingestion.

4. Run Sweep
Make Run Sweep functional.

Behavior:
Run Sweep →
- read existing documented logic
- ingest/update signals from available local/mock/adapted sources
- classify signals
- create/update jobs
- create/update recruiters
- create/update actions
- recompute Today’s Plan
- persist task run result
- update UI timestamp/counts

No dead button.

5. Today’s Plan
Make /execute/today the main operator surface.

Sections:
- Hero
- Operator Band
- New Signals
- Execution Cards
- Why This Plan
- Waiting / Deferred
- Completed Today

Hero:
- Today’s Plan
- X of Y completed
- Next up

Operator Band:
- Last run status
- Run Sweep
- Refresh
- New signal count
- Last updated timestamp

6. Execution Cards
Execution Cards must be functional.

Each card includes:
- priority
- channel
- action title
- target
- related job/company/recruiter
- why now
- status
- primary CTA
- secondary CTAs
- expand/collapse
- inline composer
- complete/defer/waiting behavior

Actions:
- Reply
- Draft
- Apply
- Review Job
- Follow Up
- Mark Waiting
- Defer
- Complete
- Dismiss
- Log Note

Each CTA must update local state and refresh visible UI.

7. Job Management
Build /manage/jobs as a working table.

Columns:
- role
- company
- status
- source
- priority
- date found
- date applied
- last signal
- next action
- recruiter/contact
- link

Statuses:
- Found
- Saved
- Reviewing
- Applied
- Interviewing
- Offer
- Rejected
- Archived

Actions:
- Review
- Apply
- Update Status
- Open Detail
- Create Follow-up
- Archive

8. Recruiter Management
Build /manage/recruiters.

Fields:
- name
- company/agency
- status
- last contact
- next action
- related jobs
- notes

Statuses:
- New
- Active
- Warm
- Waiting
- Follow-up Due
- Inactive
- Do Not Contact

Actions:
- Draft Reply
- Follow Up
- Log Note
- Open Detail

9. Outreach + Messages
Build basic functional:
- /manage/outreach
- /manage/messages

Outreach tracks:
- contact
- company
- channel
- message type
- status
- sent date
- follow-up date
- related job

Messages tracks:
- inbound
- outbound
- drafts
- related job/recruiter
- recommended action

10. Right Detail Panel
Functional right panel for:
- signal
- job
- recruiter
- action
- message

Panel shows:
- title
- type
- status
- source
- summary
- related objects
- action history
- editable note/status
- primary action
- close button

Do not use modal stacks.

11. Intelligence Layer
Build MVP surfaces:
- Competition
- Wiki
- Reports

These can use existing documented logic and local data.

Competition:
- role patterns
- market signals
- positioning notes

Wiki:
- reusable answers
- narratives
- frameworks
- company research

Reports:
- pipeline health
- applications by status
- recruiter response trend
- completed actions
- weekly summary

12. Design System
Build:
- /design-system/components
- /design-system/foundations

Use IBM Carbon-inspired system:
- dark low-glare UI
- dense but readable
- semantic colors
- Tile-based cards
- DataTable-style tables
- Tag-style statuses
- Button hierarchy
- SideNav/Header shell

Component docs must include:
- Execution Card
- Signal Card
- Operator Band
- Right Detail Panel
- Status Tags
- Data Tables
- Inline Composer

13. Functional Rules
No dead CTAs.
No fake buttons unless clearly marked as mock integration.
Every click should do at least one of:
- mutate state
- open panel
- update status
- create action
- mark complete
- refresh plan
- log event

14. Constraints
Do NOT touch:
- OpenClaw auth
- API provider settings
- gateway config
- Telegram config
- environment variables

Do NOT:
- add unnecessary dependencies
- rewrite the app from scratch
- delete existing logic docs
- replace existing architecture without need

15. Required Output
After implementation, return:

1. Docs discovered and used
2. Files modified
3. Features implemented
4. Functional flows now working
5. Mocked adapters remaining
6. How to run locally
7. Exact routes to test
8. Known gaps
9. Build result

This should be an executive, functioning MVP pass.
Build the system, not another static prototype.
```

This is the right tone now:
