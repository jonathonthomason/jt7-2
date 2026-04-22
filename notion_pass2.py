import os
import json
import requests
from datetime import datetime

TOKEN = os.environ["NOTION_TOKEN"]
NOTION_VERSION = "2022-06-28"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
}

IDS = {
    "root_page": "33e2ef93-c492-818d-8852-d0117ed61a15",
    "areas": "33e2ef93-c492-8172-bb05-ee35c15e57a3",
    "goals": "33e2ef93-c492-8116-a8b9-f8e5517c6baa",
    "projects": "33e2ef93-c492-8186-97e8-db1093224d40",
    "tasks": "33e2ef93-c492-81fe-9535-c89db3ba32d6",
    "habits": "33e2ef93-c492-813a-8ff0-df480934120b",
    "agents": "33e2ef93-c492-8197-b61d-c062460a4d9b",
    "opportunities": "33e2ef93-c492-8197-b978-c89a58b8ba3f",
    "companies": "33e2ef93-c492-81e4-8bc2-d8e13a3e3bf5",
    "contacts": "33e2ef93-c492-8116-bafc-d418fb948f5b",
    "business_ideas": "33e2ef93-c492-812a-bf77-e56b8901e44b",
    "product_modules": "33e2ef93-c492-8113-a6e6-d89c790ee9c5",
    "finance": "33e2ef93-c492-81f9-8bdc-f07d89413fd8",
    "journal": "33e2ef93-c492-8187-804a-d3f862bb4d92",
    "sops": "33e2ef93-c492-817e-93f8-ef57f5764dd9",
}

created = {
    "pages": [],
    "records": {}
}

def notion_post(path, payload):
    r = requests.post(f"https://api.notion.com/v1/{path}", headers=headers, json=payload)
    if r.status_code >= 300:
        raise RuntimeError(f"POST {path} failed\nStatus: {r.status_code}\nResponse: {r.text}")
    return r.json()

def rt(text):
    return [{"type": "text", "text": {"content": text}}]

def title_prop(name, value):
    return {name: {"title": rt(value)}}

def rich_text_prop(name, value):
    return {name: {"rich_text": rt(value)}}

def select_prop(name, value):
    return {name: {"select": {"name": value}}}

def checkbox_prop(name, value):
    return {name: {"checkbox": value}}

def number_prop(name, value):
    return {name: {"number": value}}

def date_prop(name, value):
    return {name: {"date": {"start": value}}}

def url_prop(name, value):
    return {name: {"url": value}}

def email_prop(name, value):
    return {name: {"email": value}}

def create_db_row(database_id, properties):
    payload = {
        "parent": {"database_id": database_id},
        "properties": properties
    }
    return notion_post("pages", payload)

def create_page(parent_page_id, title, blocks):
    payload = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "properties": {
            "title": {
                "title": rt(title)
            }
        },
        "children": blocks
    }
    return notion_post("pages", payload)

def paragraph(text):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": rt(text)}
    }

def heading(text, level=2):
    key = f"heading_{level}"
    return {
        "object": "block",
        "type": key,
        key: {"rich_text": rt(text)}
    }

def bullet(text):
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": rt(text)}
    }

areas = [
("God / Faith", "Spiritual", 1, True, "Foundational spiritual grounding, prayer, reflection, and alignment.", "Wellness / Faith Agent"),
("Family / Relationships", "Life", 2, True, "Protect and strengthen close relationships and future family direction.", "Daily Planning Agent"),
("Job Search", "Career", 1, True, "Primary near-term career engine and pipeline operations.", "Job Search Agent"),
("Career / Craft", "Career", 2, True, "Longer-term product design mastery, positioning, and craft growth.", "Job Search Agent"),
("Business Building", "Business", 3, True, "Portable systems, consulting, reusable modules, and ventures.", "Business Lab Agent"),
("Community Product", "Business", 2, True, "Community volunteering app and related trust/safety product exploration.", "Community Product Agent"),
("Health / Fitness", "Health", 2, True, "Training, steps, movement, recovery, sleep support.", "Wellness / Faith Agent"),
("Sobriety / Recovery", "Health", 1, True, "Recovery continuity, sobriety support, and check-ins.", "Wellness / Faith Agent"),
("Finances / Investing", "Finance", 2, True, "Cash discipline, savings, investing, passive income direction.", "Finance Tracking Agent"),
("Learning / Wisdom", "Life", 3, True, "Lessons, reflection, study, and durable learning.", "Review / Reflection Agent"),
("Life Admin", "Admin", 3, True, "Logistics, paperwork, recurring obligations, cleanup.", "Inbox / Capture Agent"),
]

created["records"]["Areas of Life"] = []
for name, domain, priority, active, desc, agent in areas:
    res = create_db_row(
        IDS["areas"],
        {
            **title_prop("Name", name),
            **select_prop("Domain Type", domain),
            **number_prop("Priority", priority),
            **checkbox_prop("Active", active),
            **rich_text_prop("Description", desc),
            **rich_text_prop("Owner Agent", agent),
            **rich_text_prop("Notes", "")
        }
    )
    created["records"]["Areas of Life"].append({"name": name, "id": res["id"]})

goals = [
    ("Find strong FTE role", "1 Year", "Active", "Land a strong senior/principal product design role.", "Secure interviews and convert into offer.", "Too much drift without real pipeline movement.", 0.25, "Review active pipeline and improve response speed.", "Job Search Agent"),
    ("Build modular portable business systems", "3 Years", "Active", "Create reusable systems that can become products or services.", "Repeatable modules with clear use cases and value.", "Ideas stay conceptual and unshipped.", 0.10, "Define highest-value reusable system modules.", "Business Lab Agent"),
    ("Build job search product/system", "1 Year", "Active", "Turn JT7 into a real job command center and product primitive.", "Stable operator workflow, modular logic, real proof loops.", "Overdesign without daily usefulness.", 0.30, "Tighten command-center usability.", "Business Lab Agent"),
    ("Build community volunteering app", "3 Years", "Active", "Develop a serious community product with trust, matching, ratings, and accessibility built in.", "Clear thesis, research track, module map, and concept maturity.", "It gets buried behind lower-leverage work.", 0.12, "Capture product foundation and core unknowns.", "Community Product Agent"),
    ("Improve wellness / spirituality / sobriety", "1 Year", "Active", "Strengthen spiritual grounding, recovery structure, and body support.", "Consistent routines and better internal stability.", "Inconsistent habits and poor recovery support.", 0.20, "Track minimum viable routines.", "Wellness / Faith Agent"),
    ("Build life roadmap / legacy", "5 Years", "Active", "Move from reactive planning to intentional life architecture.", "Clear long-horizon direction across work, faith, family, and finances.", "Stay fragmented and short-term reactive.", 0.08, "Keep goals and areas aligned.", "Review / Reflection Agent"),
    ("Grow investing / passive income", "3 Years", "Active", "Improve financial resilience and long-term compounding.", "Visible savings/investing discipline and passive income exploration.", "No system for tracking or prioritizing capital moves.", 0.10, "Capture finance structure and recurring items.", "Finance Tracking Agent"),
]

created["records"]["Areas of Life"] = []
for name, domain, priority, active, desc, agent in areas:
    res = create_db_row(
        IDS["areas"],
        {
            **title_prop("Name", name),
            **select_prop("Domain Type", domain),
            **number_prop("Priority", priority),
            **checkbox_prop("Active", active),
            **rich_text_prop("Description", desc),
            **rich_text_prop("Owner Agent", agent),
            **rich_text_prop("Notes", "")
        }
    )
    created["records"]["Areas of Life"].append({"name": name, "id": res["id"]})


projects = [
    ("JT7 / OpenClaw rebuild", "System", "Active", "P1", "Rebuild JT7 into a stable, recoverable command center.", "JT7 Operator", True),
    ("Notion command center buildout", "System", "Active", "P1", "Create a usable personal OS in Notion.", "Notion Maintenance Agent", True),
    ("Job search operating system", "Career", "Active", "P1", "Maintain visible pipeline state, follow-ups, and momentum.", "Job Search Agent", True),
    ("Community volunteering platform concept", "Product", "Active", "P2", "Develop concept, research, trust/safety and matching model.", "Community Product Agent", True),
    ("Portable business systems framework", "Business", "Active", "P2", "Identify reusable modules and operating patterns.", "Business Lab Agent", False),
    ("Personal finance tightening", "Life", "Active", "P2", "Improve money awareness, recurring costs, and savings direction.", "Finance Tracking Agent", False),
    ("Portfolio / positioning updates", "Career", "Planned", "P1", "Strengthen narrative and hiring readiness.", "Job Search Agent", True),
]

created["records"]["Projects"] = []
for name, ptype, status, priority, outcome, owner, review in projects:
    res = create_db_row(
        IDS["projects"],
        {
            **title_prop("Project Name", name),
            **select_prop("Project Type", ptype),
            **select_prop("Status", status),
            **select_prop("Priority", priority),
            **rich_text_prop("Outcome", outcome),
            **rich_text_prop("Agent Owner", owner),
            **checkbox_prop("Human Review Needed", review),
            **rich_text_prop("Notes", "")
        }
    )
    created["records"]["Projects"].append({"name": name, "id": res["id"]})

habits = [
    ("Morning prayer / stillness", "Daily", "Morning", "5 minutes of stillness and prayer.", "Spiritual grounding before reacting.", "Active"),
    ("Daily planning", "Daily", "Morning", "Review today and choose top 3.", "Reduces drift and decision fatigue.", "Active"),
    ("Job pipeline review", "Weekdays", "Morning", "Review active roles and next follow-ups.", "Keeps the career engine moving.", "Active"),
    ("Workout / walk / steps", "Daily", "Anytime", "Walk or meaningful movement.", "Supports mood, energy, and resilience.", "Active"),
    ("Expense review", "Weekly", "Evening", "Check transactions and awareness.", "Keeps finances visible.", "Active"),
    ("AA / sobriety support actions", "Daily", "Anytime", "One support/recovery action.", "Protect sobriety continuity.", "Active"),
    ("Evening reset", "Daily", "Evening", "Reset space and close loops.", "End cleaner than the day started.", "Active"),
]

created["records"]["Habits / Routines"] = []
for habit, freq, tod, mvv, why, status in habits:
    res = create_db_row(
        IDS["habits"],
        {
            **title_prop("Habit", habit),
            **select_prop("Frequency", freq),
            **select_prop("Time of Day", tod),
            **rich_text_prop("Minimum Viable Version", mvv),
            **rich_text_prop("Why", why),
            **select_prop("Status", status),
            **number_prop("Current Streak", 0),
            **rich_text_prop("Notes", "")
        }
    )
    created["records"]["Habits / Routines"].append({"name": habit, "id": res["id"]})

agents = [
("Job Search Agent", "Pipeline management, application tracking, follow-ups, recruiter handling.", "Career", "Gmail, Sheets, manual updates", "Updated pipeline state, follow-up tasks, summaries", "Gmail, Google Sheets, Notion", "Manual", "Daily", "Active", "Escalate when status confidence is low or a recruiter reply needs judgment.", True),
    ("Inbox / Capture Agent", "Capture loose inputs and route them to the right system.", "Planning", "Ad hoc notes, ideas, tasks", "Routed records and inbox cleanup", "Notion", "Manual", "As needed", "Active", "Escalate ambiguous captures.", False),
    ("Daily Planning Agent", "Translate current state into executable daily priorities.", "Planning", "Tasks, goals, calendar context", "Daily priority stack", "Notion", "Scheduled", "Daily", "Active", "Escalate if too many competing P1 items exist.", False),
    ("Finance Tracking Agent", "Track costs, savings focus, and investing structure.", "Finance", "Finance items, recurring expenses", "Finance summaries and tasks", "Notion", "Weekly", "Weekly", "Active", "Escalate larger decisions or unclear categorization.", False),
    ("Business Lab Agent", "Incubate ventures and reusable modules.", "Product", "Ideas, modules, projects", "Prioritized venture direction", "Notion", "Manual", "Weekly", "Active", "Escalate if ventures outrun career priority.", False),
    ("Community Product Agent", "Advance the community app concept and research.", "Product", "Research, ideas, constraints", "Concept structure and next moves", "Notion", "Manual", "Weekly", "Active", "Escalate trust/safety/product decisions.", False),
    ("Wellness / Faith Agent", "Support routines, reflection, and sobriety continuity.", "Wellness", "Habits, reflections, check-ins", "Routine prompts and notes", "Notion", "Scheduled", "Daily", "Active", "Escalate when routines collapse or support is needed.", False),
    ("Review / Reflection Agent", "Weekly and periodic reflection, lessons, and planning alignment.", "Planning", "Journal, goals, tasks", "Reflection entries and adjustments", "Notion", "Scheduled", "Weekly", "Active", "Escalate when repeated friction patterns appear.", False),
    ("Notion Maintenance Agent", "Keep the Notion workspace consistent and usable.", "System", "Schema, pages, templates", "Workspace maintenance and updates", "Notion", "Manual", "As needed", "Active", "Escalate schema changes that affect multiple workflows.", True),
]

created["records"]["Agent Registry"] = []
for name, function, domain, inputs, outputs, systems, trigger, cadence, status, escalation, approval in agents:
    res = create_db_row(
        IDS["agents"],
        {
            **title_prop("Agent Name", name),
            **rich_text_prop("Function", function),
            **select_prop("Domain", domain),
            **rich_text_prop("Inputs", inputs),
            **rich_text_prop("Outputs", outputs),
            **rich_text_prop("Systems Used", systems),
            **select_prop("Trigger Type", trigger),
            **rich_text_prop("Cadence", cadence),
            **select_prop("Status", status),
            **rich_text_prop("Escalation Rule", escalation),
            **checkbox_prop("Human Approval Needed", approval)
        }
    )
    created["records"]["Agent Registry"].append({"name": name, "id": res["id"]})

opportunities = [
    ("Autodesk", "UX / Product Designer", "Direct", "Remote", "Remote", "Target", "High", 8, "https://www.autodesk.com/"),
    ("Deloitte", "Lead UX Designer, Agentic AI Platform", "Indeed", "Remote", "Remote", "Applied", "High", 8, ""),
    ("Better", "UX / Product Designer", "LinkedIn", "Remote", "Remote", "Target", "Medium", 7, ""),
    ("Match Group", "Lead Product Designer", "LinkedIn", "Remote", "Remote", "Applied", "High", 9, ""),
    ("RealPage", "Product Designer I - UX", "Recruiter", "Remote", "Remote", "Recruiter Outreach", "Medium", 6, ""),
]

created["records"]["Opportunities / Job Pipeline"] = []
today = datetime.utcnow().date().isoformat()
for company, role, source, location, remotehybrid, status, priority, fit, link in opportunities:
    props = {
        **title_prop("Company", company),
        **rich_text_prop("Role", role),
        **select_prop("Source", source),
        **rich_text_prop("Location", location),
        **select_prop("Remote/Hybrid", remotehybrid),
        **select_prop("Status", status),
        **select_prop("Priority", priority),
        **number_prop("Fit Score", fit),
        **rich_text_prop("Notes", ""),
        **url_prop("Link", link),
    }
    if status in ("Applied", "Recruiter Outreach"):
        props.update(date_prop("Last Touch", today))
    if status == "Applied":
        props.update(date_prop("Applied Date", today))
    res = create_db_row(IDS["opportunities"], props)
    created["records"]["Opportunities / Job Pipeline"].append({"name": f"{company} — {role}", "id": res["id"]})

business_ideas = [
    ("Job search platform / command center", "Systems", "Active", "Create a serious operator-first command system for job search.", "Experienced professionals managing fragmented search operations.", "Job search state is fragmented across inboxes, notes, trackers, and memory.", "SaaS or tooling + services hybrid.", "High", "Tracker, intake, drafts, follow-up logic.", "Keep making JT7 usable daily."),
    ("Portable business agent systems framework", "Systems", "Incubating", "Modular agent-supported systems can be repurposed across domains.", "Operators, founders, solo professionals.", "Most people lack a usable operating system for recurring work.", "Consulting, templates, productized systems.", "High", "Agent control, SOPs, workflow tracking.", "Define module library."),
    ("Community volunteering app", "Community", "Active", "Use matching, trust, accessibility, and local relevance to improve volunteering participation.", "Communities, volunteers, organizers.", "Volunteering discovery and trust are too fragmented.", "Marketplace / platform / partnerships.", "High", "Matching, trust/safety, ratings, accessibility.", "Capture product foundation in Notion."),
    ("Reusable onboarding/auth modules", "SaaS", "Backlog", "Portable auth and onboarding systems are broadly reusable.", "Product teams and builders.", "Auth/onboarding is repetitive and often weakly implemented.", "Licensing / product modules.", "Medium", "Auth, onboarding, approvals.", "Keep as reusable module candidate."),
    ("Agentic workflow consulting layer", "Services", "Incubating", "There is service demand around agent-assisted workflow design.", "Small teams, operators, founders.", "Teams struggle to operationalize AI in real workflows.", "Consulting and implementation.", "Medium", "Playbooks, workflow models, monitoring.", "Clarify ideal buyer.")
]

created["records"]["Business Ideas / Ventures"] = []
for idea, category, status, thesis, audience, problem, monetization, priority, modules, next_step in business_ideas:
    res = create_db_row(
        IDS["business_ideas"],
        {
            **title_prop("Idea", idea),
            **select_prop("Category", category),
            **select_prop("Status", status),
            **rich_text_prop("Thesis", thesis),
            **rich_text_prop("Audience", audience),
            **rich_text_prop("Problem", problem),
            **rich_text_prop("Monetization", monetization),
            **select_prop("Priority", priority),
            **rich_text_prop("Productizable Modules", modules),
            **rich_text_prop("Next Step", next_step)
        }
    )
    created["records"]["Business Ideas / Ventures"].append({"name": idea, "id": res["id"]})
assumptions_page = create_page(
    IDS["root_page"],
    "JT Command Center - Assumptions / Next Refinements",
    [
        heading("Assumptions", 1),
        bullet("Relations and rollups are not fully wired yet in this pass; structure is seeded first so the workspace becomes immediately usable."),
        bullet("Dashboard views and templates will need a dedicated pass because Notion API support for view creation is limited compared with manual UI setup."),
        bullet("Seed data is intentionally practical and incomplete; JT can refine names, priorities, and notes later."),
        bullet("Job Search remains the highest-leverage operational domain in the current system."),
        bullet("Community App Lab is treated as a first-class venture, not a buried backlog item."),
        heading("Next Refinements", 2),
        bullet("Wire core relations across Areas, Goals, Projects, Tasks, Habits, and Agents."),
        bullet("Create manual dashboard linked views inside each top-level page."),
        bullet("Add Daily Reset, Weekly Review, Job Follow-up, New Venture, New Goal, and Agent SOP templates."),
        bullet("Add finance seed records, company targets, contacts, and SOP records."),
        bullet("Add daily/weekly review workflow pages and first reflection entries."),
    ]
)
created["pages"].append({
    "title": "JT Command Center - Assumptions / Next Refinements",
    "id": assumptions_page["id"]
})

report_path = "notion_pass2_build_report.json"
with open(report_path, "w") as f:
    json.dump(created, f, indent=2)

print(json.dumps(created, indent=2))
print(f"\nWrote build report to {report_path}")
