import os
import json
import requests
from textwrap import dedent

TOKEN = os.environ["NOTION_TOKEN"]
PARENT_PAGE_ID = os.environ["NOTION_PARENT_PAGE_ID"]

NOTION_VERSION = "2022-06-28"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
}

created = {
    "pages": {},
    "databases": {}
}

def notion_post(path, payload):
    r = requests.post(f"https://api.notion.com/v1/{path}", headers=headers, json=payload)
    if r.status_code >= 300:
        raise RuntimeError(f"POST {path} failed\\nStatus: {r.status_code}\\nResponse: {r.text}")
    return r.json()

def notion_patch(path, payload):
    r = requests.patch(f"https://api.notion.com/v1/{path}", headers=headers, json=payload)
    if r.status_code >= 300:
        raise RuntimeError(f"PATCH {path} failed\\nStatus: {r.status_code}\\nResponse: {r.text}")
    return r.json()

def rich_text(text):
    return [{"type": "text", "text": {"content": text}}]

def title(text):
    return [{"type": "text", "text": {"content": text}}]

def paragraph_block(text):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": rich_text(text)}
    }

def heading_block(text, level=2):
    key = f"heading_{level}"
    return {
        "object": "block",
        "type": key,
        key: {"rich_text": rich_text(text)}
    }

def bulleted(text):
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": rich_text(text)}
    }

def create_page(parent_id, title_text, children=None, icon=None):
    payload = {
        "parent": {"type": "page_id", "page_id": parent_id},
        "properties": {
            "title": {
                "title": title(title_text)
            }
        }
    }
    if icon:
        payload["icon"] = {"type": "emoji", "emoji": icon}

    if children:
        payload["children"] = children
    res = notion_post("pages", payload)
    created["pages"][title_text] = res["id"]
    return res

def create_database(parent_id, title_text, properties, description=None, icon="🗂️"):
    children = []
    if description:
        children.append(paragraph_block(description))
    payload = {
        "parent": {"type": "page_id", "page_id": parent_id},
        "icon": {"type": "emoji", "emoji": icon},
        "title": title(title_text),
        "properties": properties
    }
    if children:
        payload["children"] = children
    res = notion_post("databases", payload)
    created["databases"][title_text] = res["id"]
    return res

root = create_page(
    PARENT_PAGE_ID,
    "JT Command Center",
    icon="🧠",
    children=[
        heading_block("JT Command Center", 1),
        paragraph_block("Personal operating system for goals, job search, business incubation, execution, wellness, finance, and agent coordination."),
        heading_block("Primary Dashboards", 2),
        bulleted("Life OS"),
        bulleted("Daily Command"),
        bulleted("Goals & Roadmap"),
        bulleted("Job Search HQ"),
        bulleted("Business Lab"),
        bulleted("Community App Lab"),
        bulleted("Wellness / Faith / Sobriety"),
        bulleted("Finance / Investing"),
        bulleted("Agent Control Center"),
        bulleted("Inbox / Capture"),
        bulleted("Reviews & Planning"),
        bulleted("Reference / SOPs"),
    ]
)
root_id = root["id"]

top_pages = [
    ("Life OS", "🌿"),
    ("Daily Command", "⚙️"),
    ("Goals & Roadmap", "🎯"),
    ("Job Search HQ", "💼"),
    ("Business Lab", "🧪"),
    ("Community App Lab", "🤝"),
    ("Wellness / Faith / Sobriety", "🕊️"),
    ("Finance / Investing", "💸"),
    ("Agent Control Center", "🤖"),
    ("Inbox / Capture", "📥"),
    ("Reviews & Planning", "📝"),
    ("Reference / SOPs", "📚"),
]


for page_name, icon in top_pages:
    create_page(
        root_id,
        page_name,
        icon=icon,
        children=[
            paragraph_block(f"{page_name} dashboard / workspace. Build for clarity, momentum, and low cognitive load.")
        ]
    )

db_specs = {
    "Areas of Life": {
        "icon": "🧭",
        "description": "High-level life pillars that organize goals, projects, habits, and tasks.",
        "properties": {
            "Name": {"title": {}},
            "Domain Type": {"select": {"options": [
                {"name": "Life", "color": "default"},
                {"name": "Career", "color": "blue"},
                {"name": "Business", "color": "green"},
                {"name": "Health", "color": "yellow"},
                {"name": "Finance", "color": "purple"},
                {"name": "Spiritual", "color": "orange"},
                {"name": "Admin", "color": "gray"},
            ]}},
            "Priority": {"number": {"format": "number"}},
            "Active": {"checkbox": {}},
            "Description": {"rich_text": {}},
            "Owner Agent": {"rich_text": {}},
            "Notes": {"rich_text": {}}
        }
    },
    "Goals": {
        "icon": "🎯",
        "description": "Strategic goals across life, career, business, wellness, and finance.",
        "properties": {
            "Goal Name": {"title": {}},
            "Time Horizon": {"select": {"options": [
                {"name": "90 Days", "color": "blue"},
                {"name": "1 Year", "color": "green"},
                {"name": "3 Years", "color": "yellow"},
                {"name": "5 Years", "color": "purple"},
                {"name": "Lifetime", "color": "orange"},
            ]}},
            "Status": {"select": {"options": [
                {"name": "Active", "color": "green"},
                {"name": "Paused", "color": "yellow"},
                {"name": "Achieved", "color": "blue"},
                {"name": "Dropped", "color": "red"},
                {"name": "Someday", "color": "gray"},
            ]}},
            "Why it Matters": {"rich_text": {}},
            "Success Criteria": {"rich_text": {}},
            "Failure Criteria": {"rich_text": {}},
            "Milestone Date": {"date": {}},
            "Progress %": {"number": {"format": "percent"}},
            "Next Action": {"rich_text": {}},
            "Owner Agent": {"rich_text": {}},
            "Notes": {"rich_text": {}}
        }
    },
    "Milestones": {
        "icon": "🏁",
        "description": "Concrete checkpoints under major goals and projects.",
        "properties": {
            "Milestone": {"title": {}},
            "Due Date": {"date": {}},
            "Status": {"select": {"options": [
                {"name": "Planned", "color": "default"},
                {"name": "In Progress", "color": "blue"},
                {"name": "Blocked", "color": "red"},
                {"name": "Complete", "color": "green"},
            ]}},
            "Pass Criteria": {"rich_text": {}},
            "Failure Criteria": {"rich_text": {}},
            "Blocking Risks": {"rich_text": {}},
            "Next Step": {"rich_text": {}},
            "Notes": {"rich_text": {}}
        }
    },
    "Projects": {
        "icon": "🛠️",
        "description": "Execution layer for job search, product ideas, life systems, and operating initiatives.",
        "properties": {
            "Project Name": {"title": {}},
            "Project Type": {"select": {"options": [
                {"name": "Career", "color": "blue"},
                {"name": "Product", "color": "green"},
                {"name": "Business", "color": "purple"},
                {"name": "Life", "color": "yellow"},
                {"name": "System", "color": "gray"},
            ]}},
"Status": {"select": {"options": [
                {"name": "Active", "color": "green"},
                {"name": "Planned", "color": "default"},
                {"name": "Blocked", "color": "red"},
                {"name": "Paused", "color": "yellow"},
                {"name": "Done", "color": "blue"},
            ]}},
            "Priority": {"select": {"options": [
                {"name": "P1", "color": "red"},
                {"name": "P2", "color": "yellow"},
                {"name": "P3", "color": "blue"},
            ]}},
            "Start Date": {"date": {}},
            "Target Date": {"date": {}},
            "Outcome": {"rich_text": {}},
            "Agent Owner": {"rich_text": {}},
            "Human Review Needed": {"checkbox": {}},
            "Notes": {"rich_text": {}}
        }
    },
    "Tasks": {
        "icon": "✅",
        "description": "Daily executable work with lightweight planning and agent ownership.",
        "properties": {
            "Task": {"title": {}},
            "Status": {"select": {"options": [
                {"name": "Inbox", "color": "default"},
                {"name": "Today", "color": "blue"},
                {"name": "In Progress", "color": "yellow"},
                {"name": "Waiting", "color": "orange"},
                {"name": "Done", "color": "green"},
                {"name": "Dropped", "color": "red"},
            ]}},
            "Priority": {"select": {"options": [
                {"name": "P1", "color": "red"},
                {"name": "P2", "color": "yellow"},
                {"name": "P3", "color": "blue"},
            ]}},
            "Due": {"date": {}},
            "Agent Owner": {"rich_text": {}},
            "Effort": {"select": {"options": [
                {"name": "5m", "color": "gray"},
                {"name": "15m", "color": "blue"},
                {"name": "30m", "color": "green"},
                {"name": "60m+", "color": "orange"},
            ]}},
            "Recurring": {"checkbox": {}},
            "Daily Critical": {"checkbox": {}},
            "Waiting On": {"rich_text": {}},
            "Notes": {"rich_text": {}}
        }
    },
    "Habits / Routines": {
        "icon": "🔁",
        "description": "Repeatable actions that support stability, momentum, and long-term goals.",
        "properties": {
            "Habit": {"title": {}},
            "Frequency": {"select": {"options": [
                {"name": "Daily", "color": "green"},
                {"name": "Weekly", "color": "blue"},
                {"name": "Weekdays", "color": "yellow"},
                {"name": "Custom", "color": "gray"},
            ]}},
            "Time of Day": {"select": {"options": [
                {"name": "Morning", "color": "yellow"},
                {"name": "Midday", "color": "blue"},
                {"name": "Evening", "color": "purple"},
                {"name": "Anytime", "color": "gray"},
            ]}},
            "Minimum Viable Version": {"rich_text": {}},
            "Why": {"rich_text": {}},
            "Status": {"select": {"options": [
                {"name": "Active", "color": "green"},
                {"name": "Paused", "color": "yellow"},
                {"name": "Dropped", "color": "red"},
            ]}},
            "Current Streak": {"number": {"format": "number"}},
            "Notes": {"rich_text": {}}
        }
    },
    "Agent Registry": {
        "icon": "🤖",
        "description": "Registry of agents, roles, cadences, inputs, outputs, and approval rules.",
        "properties": {
            "Agent Name": {"title": {}},
            "Function": {"rich_text": {}},
            "Domain": {"select": {"options": [
                {"name": "Career", "color": "blue"},
                {"name": "Planning", "color": "green"},
                {"name": "Finance", "color": "yellow"},
                {"name": "Product", "color": "purple"},
                {"name": "Wellness", "color": "orange"},
                {"name": "System", "color": "gray"},
                ]}},
                "Inputs": {"rich_text": {}},
                "Outputs": {"rich_text": {}},
                "Systems Used": {"rich_text": {}},
                "Trigger Type": {"select": {"options": [
                    {"name": "Manual", "color": "default"},
                    {"name": "Scheduled", "color": "blue"},
                    {"name": "Event-Driven", "color": "green"},
                ]}},
                "Cadence": {"rich_text": {}},
                "Status": {"select": {"options": [
                    {"name": "Active", "color": "green"},
                    {"name": "Paused", "color": "yellow"},
                    {"name": "Draft", "color": "gray"},
                ]}},
                "Escalation Rule": {"rich_text": {}},
                "Human Approval Needed": {"checkbox": {}},
                "Prompt / SOP Link": {"url": {}}
            }
        },
        "Agent Runs / Logs": {
            "icon": "📜",
            "description": "Operational visibility into what agents did, changed, and whether review is needed.",
            "properties": {
                "Run Title": {"title": {}},
                "Timestamp": {"date": {}},
                "Status": {"select": {"options": [
                    {"name": "Success", "color": "green"},
                    {"name": "Needs Review", "color": "yellow"},
                    {"name": "Failed", "color": "red"},
                    {"name": "Skipped", "color": "gray"},
                ]}},
                "Trigger": {"rich_text": {}},
                "Input Summary": {"rich_text": {}},
                "Output Summary": {"rich_text": {}},
                "Records Created": {"number": {"format": "number"}},
                "Records Updated": {"number": {"format": "number"}},
                "Errors": {"rich_text": {}},
                "Needs Review": {"checkbox": {}},
                "Follow-up Task": {"rich_text": {}}
            }
        },
        "Opportunities / Job Pipeline": {
            "icon": "💼",
            "description": "Applications, recruiter activity, interviews, follow-ups, and status tracking.",
            "properties": {
                "Company": {"title": {}},
                "Role": {"rich_text": {}},
                "Source": {"select": {"options": [
                    {"name": "LinkedIn", "color": "blue"},
                    {"name": "Indeed", "color": "yellow"},
                    {"name": "Built In", "color": "green"},
                    {"name": "Otta", "color": "purple"},
                    {"name": "Referral", "color": "orange"},
                    {"name": "Direct", "color": "gray"},
                    {"name": "Recruiter", "color": "pink"},
                ]}},
                "Location": {"rich_text": {}},
                "Remote/Hybrid": {"select": {"options": [
                    {"name": "Remote", "color": "green"},
                    {"name": "Hybrid", "color": "yellow"},
                    {"name": "Onsite", "color": "red"},
                ]}},
                "Status": {"select": {"options": [
                    {"name": "Target", "color": "gray"},
                    {"name": "Applied", "color": "blue"},
                    {"name": "Recruiter Outreach", "color": "purple"},
                    {"name": "Recruiter Screen", "color": "pink"},
                    {"name": "Hiring Manager", "color": "orange"},
                    {"name": "Panel / Loop", "color": "yellow"},
                    {"name": "Take Home / Exercise", "color": "brown"},
                    {"name": "Final Round", "color": "red"},
                    {"name": "Offer", "color": "green"},
                    {"name": "Rejected", "color": "red"},
                    {"name": "Withdrawn", "color": "gray"},
                    {"name": "Ghosted / Stale", "color": "default"},
                    {"name": "On Hold", "color": "yellow"},
                ]}},
                "Applied Date": {"date": {}},
                "Last Touch": {"date": {}},
                "Next Follow-up": {"date": {}},
                "Compensation": {"rich_text": {}},
                "Notes": {"rich_text": {}},
                "Priority": {"select": {"options": [
                    {"name": "High", "color": "red"},
                    {"name": "Medium", "color": "yellow"},
                    {"name": "Low", "color": "blue"},
                ]}},
                "Fit Score": {"number": {"format": "number"}},
                "Link": {"url": {}}
            }
        },
        "Companies / Targets": {
            "icon": "🏢",
            "description": "Longer-term target companies and strategic employer tracking.",
            "properties": {
                "Company": {"title": {}},
                "Industry": {"rich_text": {}},
                "Region": {"rich_text": {}},
                "Priority": {"select": {"options": [
                    {"name": "High", "color": "red"},
                    {"name": "Medium", "color": "yellow"},
                    {"name": "Low", "color": "blue"},
                ]}},
                "Why Target": {"rich_text": {}},
                "Last Reviewed": {"date": {}},
                "Status": {"select": {"options": [
                    {"name": "Active Target", "color": "green"},
                    {"name": "Researching", "color": "blue"},
                    {"name": "Paused", "color": "yellow"},
                    {"name": "Closed", "color": "gray"},
                ]}},
                "Notes": {"rich_text": {}}
            }
        },
        "Contacts": {
            "icon": "👥",
            "description": "Recruiters, hiring managers, collaborators, advisors, and key relationships.",
            "properties": {
                "Name": {"title": {}},
                "Company": {"rich_text": {}},
                "Role": {"rich_text": {}},
                "Contact Type": {"select": {"options": [
                    {"name": "Recruiter", "color": "purple"},
                    {"name": "Hiring Manager", "color": "blue"},
                    {"name": "Advisor", "color": "green"},
                    {"name": "Collaborator", "color": "yellow"},
                    {"name": "Friend", "color": "gray"},
                ]}},
                "Email": {"email": {}},
                "LinkedIn": {"url": {}},
                "Relationship Status": {"select": {"options": [
                    {"name": "New", "color": "default"},
                    {"name": "Warm", "color": "yellow"},
                    {"name": "Active", "color": "green"},
                    {"name": "Dormant", "color": "gray"},
                ]}},
                "Last Contact": {"date": {}},
                "Next Action": {"rich_text": {}},
                "Notes": {"rich_text": {}}
            }
        },
        "Business Ideas / Ventures": {
            "icon": "💡",
            "description": "Business and product concepts, incubated with next steps and strategic framing.",
            "properties": {
                "Idea": {"title": {}},
                "Category": {"select": {"options": [
                    {"name": "SaaS", "color": "blue"},
                    {"name": "Services", "color": "green"},
                    {"name": "Marketplace", "color": "purple"},
                    {"name": "Community", "color": "yellow"},
                    {"name": "Systems", "color": "gray"},
                ]}},
                "Status": {"select": {"options": [
                    {"name": "Active", "color": "green"},
                    {"name": "Incubating", "color": "blue"},
                    {"name": "Backlog", "color": "gray"},
                    {"name": "Paused", "color": "yellow"},
                ]}},
                "Thesis": {"rich_text": {}},
                "Audience": {"rich_text": {}},
                "Problem": {"rich_text": {}},
                "Monetization": {"rich_text": {}},
                "Priority": {"select": {"options": [
                    {"name": "High", "color": "red"},
                    {"name": "Medium", "color": "yellow"},
                    {"name": "Low", "color": "blue"},
                ]}},
                "Productizable Modules": {"rich_text": {}},
                "Next Step": {"rich_text": {}}
            }
        },
        "Product Modules": {
            "icon": "🧩",
            "description": "Reusable system parts that can be lifted into future products or ventures.",
            "properties": {
                "Module Name": {"title": {}},
                "Function": {"rich_text": {}},
                "Reusability": {"select": {"options": [
                    {"name": "High", "color": "green"},
                    {"name": "Medium", "color": "yellow"},
                    {"name": "Low", "color": "gray"},
                ]}},
                "Dependencies": {"rich_text": {}},
                "Target User": {"rich_text": {}},
                "Status": {"select": {"options": [
                    {"name": "Defined", "color": "blue"},
                    {"name": "In Progress", "color": "yellow"},
                    {"name": "Validated", "color": "green"},
                    {"name": "Backlog", "color": "gray"},
                ]}},
                "Documentation": {"url": {}},
                "Notes": {"rich_text": {}}
            }
        },
        "Finance Items": {
            "icon": "💳",
            "description": "Recurring costs, savings targets, investing priorities, and financial awareness items.",
            "properties": {
                "Item": {"title": {}},
                "Type": {"select": {"options": [
                    {"name": "Expense", "color": "red"},
                    {"name": "Income", "color": "green"},
                    {"name": "Investment", "color": "blue"},
                    {"name": "Savings Goal", "color": "yellow"},
                ]}},
                "Category": {"rich_text": {}},
                "Amount": {"number": {"format": "dollar"}},
                "Frequency": {"select": {"options": [
                    {"name": "Monthly", "color": "blue"},
                    {"name": "Weekly", "color": "green"},
                    {"name": "Quarterly", "color": "yellow"},
                    {"name": "Annual", "color": "purple"},
                    {"name": "One-Time", "color": "gray"},
                ]}},
                "Fixed/Variable": {"select": {"options": [
                    {"name": "Fixed", "color": "green"},
                    {"name": "Variable", "color": "yellow"},
                ]}},
                "Notes": {"rich_text": {}}
            }
        },
        "Reflections / Journal": {
            "icon": "📝",
            "description": "Reflections, lessons, friction, wins, spiritual notes, and operating insight.",
            "properties": {
                "Entry Title": {"title": {}},
                "Date": {"date": {}},
                "Category": {"select": {"options": [
                    {"name": "Daily Reflection", "color": "blue"},
                    {"name": "Spiritual", "color": "yellow"},
                    {"name": "Career", "color": "green"},
                    {"name": "Systems", "color": "gray"},
                    {"name": "Lesson", "color": "purple"},
                ]}},
                "Energy": {"select": {"options": [
                    {"name": "High", "color": "green"},
                    {"name": "Medium", "color": "yellow"},
                    {"name": "Low", "color": "red"},
                ]}},
                "Wins": {"rich_text": {}},
                "Friction": {"rich_text": {}},
                "Lesson": {"rich_text": {}},
                "Prayer / Reflection": {"rich_text": {}},
                "Next Adjustment": {"rich_text": {}}
            }
        },
        "SOPs / Playbooks": {
            "icon": "📘",
            "description": "Repeatable operating procedures for JT and supporting agents.",
            "properties": {
                "SOP Name": {"title": {}},
                "Domain": {"select": {"options": [
                    {"name": "Career", "color": "blue"},
                    {"name": "System", "color": "gray"},
                    {"name": "Finance", "color": "yellow"},
                    {"name": "Wellness", "color": "green"},
                    {"name": "Product", "color": "purple"},
                ]}},
                "Trigger": {"rich_text": {}},
                "Steps": {"rich_text": {}},
                "Inputs": {"rich_text": {}},
                "Outputs": {"rich_text": {}},
                "Last Updated": {"date": {}},
                "Status": {"select": {"options": [
                    {"name": "Draft", "color": "gray"},
                    {"name": "Active", "color": "green"},
                    {"name": "Needs Update", "color": "yellow"},
                ]}}
            }
        }
    }
    
for db_name, spec in db_specs.items():
    create_database(
        root_id,
        db_name,
        properties=spec["properties"],
        description=spec["description"],
        icon=spec["icon"]
    )

report_path = "notion_pass1_build_report.json"
with open(report_path, "w") as f:
    json.dump(created, f, indent=2)

print(json.dumps(created, indent=2))
print(f"\nWrote build report to {report_path}")
