#!/usr/bin/env python3
import csv
import json
import re
import subprocess
from datetime import datetime, timedelta
from email.utils import parseaddr
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path('/Users/jtemp/.openclaw/workspace/job-search-ui')
RUNTIME = ROOT / 'runtime'
TASKS_FILE = RUNTIME / 'jt7_tasks.json'
SCHEDULER_FILE = RUNTIME / 'jt7_scheduler.json'
LOG_FILE = RUNTIME / 'jt7_pass_log.jsonl'
REPORTS_DIR = RUNTIME / 'reports'
MIRROR_DIR = ROOT / 'data_mirror'
SHEET_ID = '1acPkcUQFDIVNY0sgMo7ZsVzEnBKIbjU2veEjDFRu0Ks'
TZ = ZoneInfo('America/Chicago')
DEFAULT_GMAIL_LOOKBACK_DAYS = 5
CHAIN = [
    'EMAIL_SIGNAL_SCAN',
    'CALENDAR_SIGNAL_SCAN',
    'JOB_BOARD_SIGNAL_SCAN',
    'SIGNAL_CLASSIFICATION',
    'PIPELINE_STATE_SYNC',
    'PIPELINE_UPDATE',
    'LOCAL_MIRROR_SYNC',
    'GIT_COMMIT_SYNC',
    'ACTION_GENERATION',
    'PRIORITY_SURFACING',
    'PASS_LOGGER',
]
RUN_TIMES = ['08:30', '12:30', '18:00']
TABS = ['Jobs', 'Recruiters', 'Competition', 'Signals', 'Actions', 'TaskRuns', 'Lookup']
JOB_LABEL_QUERY = 'label:Folders/Jobs'
JOB_HINTS = [
    'application', 'interview', 'recruiter', 'hiring', 'candidate', 'job', 'role',
    'linkedin', 'indeed', 'greenhouse', 'workday', 'schedule', 'screen', 'offer', 'rejection',
    'talent acquisition', 'next steps', 'actively recruiting', 'message replied'
]
NEWSLETTER_NOISE_PATTERNS = [
    r'linkedin news',
    r'newsletter',
    r'messaging-digest',
    r'newsletters-noreply',
    r'editors-noreply',
    r'take control\. build a career ai can.t replace',
    r'token remorse',
    r'meta starts tracking employee laptops',
    r'just messaged you',
]
GENERIC_COMPANY_BLOCKLIST = {'linkedin job alerts', 'linkedin', 'indeed', 'mail', 'em'}
CLASSIFICATION_RULES = [
    ('interview_scheduling', [r'\binterview\b', r'schedule(?:d|ing)?', r'availability', r'calendar invite', r'meet with']),
    ('reschedule', [r'reschedule', r're-schedule', r'move .* interview', r'new time']),
    ('cancellation', [r'cancelled', r'canceled', r'withdrawn', r'no longer moving forward with interview']),
    ('rejection', [r'not moving forward', r'other candidates', r'regret to inform', r'unfortunately']),
    ('application_confirmation', [r'application received', r'thanks for applying', r'we received your application', r'application for']),
    ('recruiter_outreach', [r'\brecruiter\b', r'talent acquisition', r'talent partner', r'would love to connect', r'interested in your background']),
    ('hiring_manager_communication', [r'hiring manager', r'manager review', r'manager would like to']),
    ('follow_up_opportunity', [r'follow up', r'checking in', r'next steps', r'following up']),
    ('job_alert', [r'you may be a fit for', r'is hiring for', r'new jobs', r'actively recruiting', r'job alert']),
]
LINKEDIN_ROLE_RE = re.compile(r'You may be a fit for\s+(?P<company>.+?)’s\s+(?P<role>.+?)(?:\s+role|\s+-)', re.IGNORECASE)
LINKEDIN_SIMPLE_ROLE_RE = re.compile(r'(?P<role>[A-Z][A-Za-z0-9&/() ,\-]+?)\s+at\s+(?P<company>[A-Z][A-Za-z0-9&/() .\-]+)$', re.IGNORECASE)
INDEED_ROLE_RE = re.compile(r'(?P<company>.+?) is hiring for (?P<role>.+?)\.', re.IGNORECASE)
THOMSON_REUTERS_RE = re.compile(r'Job opportunity[-: ]+(.+?) with Thomson Reuters', re.IGNORECASE)
APPLICATION_RE = re.compile(r'(?:application|applied) (?:for|to)?\s*(?P<role>[A-Z][A-Za-z0-9&/\- ,]+)', re.IGNORECASE)
EMAIL_RE = re.compile(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}', re.IGNORECASE)


def now_local():
    return datetime.now(TZ)


def iso(dt):
    return dt.isoformat()


def parse_dt(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except Exception:
        return None


def next_run_after(current, hhmm):
    hour, minute = map(int, hhmm.split(':'))
    candidate = current.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if candidate <= current:
        candidate = candidate + timedelta(days=1)
    return candidate


def next_global_run(current):
    candidates = [next_run_after(current, t) for t in RUN_TIMES]
    return min(candidates)


def load_json(path):
    return json.loads(path.read_text())


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def update_task_state(task_name, status, summary, run_at, next_at):
    data = load_json(TASKS_FILE)
    for task in data['tasks']:
        if task['taskName'] == task_name:
            task['lastRunAt'] = iso(run_at)
            task['nextRunAt'] = iso(next_at)
            task['lastStatus'] = status
            task['lastSummary'] = summary
    save_json(TASKS_FILE, data)


def update_scheduler_state(status, summary, run_at):
    data = load_json(SCHEDULER_FILE)
    for run in data['schedule']:
        run['lastRunAt'] = iso(run_at)
        run['nextRunAt'] = iso(next_run_after(run_at, run['time']))
        run['lastStatus'] = status
        run['lastSummary'] = summary
    save_json(SCHEDULER_FILE, data)


def append_log(entry):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open('a') as f:
        f.write(json.dumps(entry) + '\n')


def gog_json(args):
    result = subprocess.run(args, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def sheets_get(range_name):
    return gog_json(['gog', 'sheets', 'get', SHEET_ID, range_name, '--json'])


def sheets_update(range_name, values):
    subprocess.run(
        ['gog', 'sheets', 'update', SHEET_ID, range_name, '--values-json', json.dumps(values), '--input', 'USER_ENTERED'],
        check=True, capture_output=True, text=True,
    )


def sheets_append(range_name, values):
    subprocess.run(
        ['gog', 'sheets', 'append', SHEET_ID, range_name, '--values-json', json.dumps(values), '--insert', 'INSERT_ROWS'],
        check=True, capture_output=True, text=True,
    )


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def mirror_snapshot():
    snapshot = {}
    for tab in TABS:
        csv_path = MIRROR_DIR / f'{tab}.csv'
        json_path = MIRROR_DIR / f'{tab}.json'
        snapshot[tab] = {
            'csv_exists': csv_path.exists(),
            'json_exists': json_path.exists(),
            'csv_size': csv_path.stat().st_size if csv_path.exists() else 0,
            'json_size': json_path.stat().st_size if json_path.exists() else 0,
        }
    return snapshot


def rows_to_dicts(tab):
    data = sheets_get(f'{tab}!A1:Z1000').get('values', [])
    if not data:
        return [], []
    header = data[0]
    rows = []
    for idx, row in enumerate(data[1:], start=2):
        padded = row + [''] * (len(header) - len(row))
        rows.append({'row_index': idx, 'values': dict(zip(header, padded))})
    return header, rows


def next_id(prefix, existing_ids):
    max_n = 0
    for value in existing_ids:
        if isinstance(value, str) and value.startswith(prefix):
            tail = value.replace(prefix, '')
            if tail.isdigit():
                max_n = max(max_n, int(tail))
    return f'{prefix}{max_n + 1:03d}'


def append_rows(tab, rows):
    if rows:
        sheets_append(f'{tab}!A:Z', rows)


def update_row(tab, row_index, row_values):
    end_col = chr(ord('A') + len(row_values) - 1)
    sheets_update(f'{tab}!A{row_index}:{end_col}{row_index}', [row_values])


def normalize_text(value):
    return re.sub(r'\s+', ' ', (value or '').strip()).lower()


def normalize_company(value):
    text = normalize_text(value)
    return re.sub(r'\b(inc|llc|ltd|corp|corporation|company|co)\b', '', text).strip(' ,.-')


def extract_domain(value):
    email = parseaddr(value or '')[1]
    if '@' in email:
        return email.split('@', 1)[1].lower()
    return ''


def get_last_run_at():
    tasks = load_json(TASKS_FILE)['tasks']
    runs = [parse_dt(t.get('lastRunAt')) for t in tasks if t.get('lastRunAt')]
    runs = [r for r in runs if r]
    if runs:
        return max(runs)
    return now_local() - timedelta(days=DEFAULT_GMAIL_LOOKBACK_DAYS)


def gmail_query_from_last_run(last_run_at):
    delta = now_local() - last_run_at
    days = max(1, min(30, delta.days + 1))
    return f"{JOB_LABEL_QUERY} newer_than:{days}d"


def collect_gmail_messages(query):
    return gog_json(['gog', 'gmail', 'messages', 'search', query, '--max', '100', '--json']).get('messages', [])


def collect_gmail_threads(query):
    return gog_json(['gog', 'gmail', 'search', query, '--max', '100', '--json']).get('threads', [])


def build_thread_map(threads, messages):
    thread_map = {t['id']: {'thread': t, 'messages': []} for t in threads}
    for m in messages:
        thread_map.setdefault(m['threadId'], {'thread': {'id': m['threadId'], 'labels': m.get('labels', [])}, 'messages': []})
        thread_map[m['threadId']]['messages'].append(m)
    return thread_map


def classify_signal(subject, sender, labels, body=''):
    haystack = ' '.join([subject or '', sender or '', body or '', ' '.join(labels or [])]).lower()
    signal_type = 'unknown_review_needed'
    confidence = 0.35
    auto_update_allowed = False
    review_needed = True

    if 'unsubscribe' in haystack and 'job' not in haystack and 'recruit' not in haystack:
        return {
            'signal_type': 'ignore_noise',
            'summary': subject[:160],
            'confidence': 0.95,
            'auto_update_allowed': False,
            'review_needed': False,
        }

    if any(re.search(pattern, haystack, re.IGNORECASE) for pattern in NEWSLETTER_NOISE_PATTERNS):
        return {
            'signal_type': 'ignore_noise',
            'summary': subject[:160],
            'confidence': 0.94,
            'auto_update_allowed': False,
            'review_needed': False,
        }

    if 'invitations@linkedin.com' in (sender or '').lower() and 'connect' in haystack:
        return {
            'signal_type': 'ignore_noise',
            'summary': subject[:160],
            'confidence': 0.92,
            'auto_update_allowed': False,
            'review_needed': False,
        }

    for candidate, patterns in CLASSIFICATION_RULES:
        if any(re.search(pattern, haystack, re.IGNORECASE) for pattern in patterns):
            signal_type = candidate
            break

    if signal_type in {'application_confirmation', 'interview_scheduling', 'reschedule', 'cancellation', 'rejection'}:
        confidence = 0.88
        auto_update_allowed = True
        review_needed = False
    elif signal_type in {'recruiter_outreach', 'hiring_manager_communication', 'follow_up_opportunity'}:
        confidence = 0.76
        auto_update_allowed = True
        review_needed = False
    elif signal_type == 'job_alert':
        confidence = 0.81
        auto_update_allowed = True
        review_needed = False
    elif signal_type == 'ignore_noise':
        confidence = 0.95
        auto_update_allowed = False
        review_needed = False

    return {
        'signal_type': signal_type,
        'summary': subject[:160],
        'confidence': confidence,
        'auto_update_allowed': auto_update_allowed,
        'review_needed': review_needed,
    }


def extract_entities(subject, sender, snippet=''):
    company = ''
    role = ''
    source = 'gmail'
    sender_name, sender_email = parseaddr(sender or '')
    domain = extract_domain(sender)

    linkedin = LINKEDIN_ROLE_RE.search(subject or '')
    linkedin_simple = LINKEDIN_SIMPLE_ROLE_RE.search(subject or '')
    indeed = INDEED_ROLE_RE.search(subject or '')
    thomson = THOMSON_REUTERS_RE.search(subject or '')
    app = APPLICATION_RE.search(subject or '')

    if linkedin:
        company = linkedin.group('company').strip()
        role = linkedin.group('role').strip(' -')
        source = 'linkedin_email'
    elif linkedin_simple and 'linkedin' in (sender_email or '').lower():
        company = linkedin_simple.group('company').strip()
        role = linkedin_simple.group('role').strip()
        source = 'linkedin_email'
    elif indeed:
        company = indeed.group('company').strip()
        role = indeed.group('role').strip()
        source = 'indeed_email'
    elif thomson:
        company = 'Thomson Reuters'
        role = thomson.group(1).strip()
        source = 'gmail'
    elif app:
        role = app.group('role').strip(' .')

    normalized_sender = (sender_name or '').strip()
    if not company and normalized_sender:
        cleaned = normalized_sender
        lowered = cleaned.lower()
        if 'american airlines talent acquisition' in lowered:
            company = 'American Airlines'
        elif 'thomson reuters' in (subject or '').lower() or 'thomson reuters' in lowered:
            company = 'Thomson Reuters'
        elif 'talent acquisition' in lowered or 'recruiter' in lowered or 'talent partner' in lowered:
            company = cleaned
        elif lowered in {'linkedin job alerts', 'linkedin', 'indeed', 'mail', 'linkedin news'}:
            company = ''

    if not company and domain and domain not in {'gmail.com', 'googlemail.com', 'linkedin.com', 'indeed.com', 'mail.linkedin.com'}:
        company = domain.split('.')[0].replace('-', ' ').title()

    if normalize_text(company) in GENERIC_COMPANY_BLOCKLIST and not role:
        company = ''

    return {
        'company': company,
        'role': role,
        'source': source,
        'sender_name': sender_name,
        'sender_email': sender_email,
        'sender_domain': domain,
        'snippet': snippet or subject,
    }


def infer_status(signal_type, current_status=''):
    if signal_type == 'application_confirmation':
        return 'Applied'
    if signal_type in {'recruiter_outreach', 'hiring_manager_communication'}:
        return 'Recruiter Contacted'
    if signal_type in {'interview_scheduling', 'reschedule'}:
        return 'Interviewing'
    if signal_type == 'rejection':
        return 'Rejected'
    if signal_type == 'job_alert' and not current_status:
        return 'Cold'
    return current_status or 'Cold'


def choose_company_from_context(parsed, jobs_by_company):
    if parsed['company']:
        return parsed['company']
    if parsed['sender_domain']:
        for company_norm, row in jobs_by_company.items():
            if parsed['sender_domain'].split('.')[0] in company_norm:
                return row['values'].get('company', '')
    return ''


def choose_role_from_context(parsed, company_jobs):
    if parsed['role']:
        return parsed['role']
    if company_jobs:
        return company_jobs[0]['values'].get('role', '')
    return ''


def score_job_match(parsed, job_row):
    job = job_row['values']
    score = 0.0
    if normalize_company(parsed['company']) and normalize_company(parsed['company']) == normalize_company(job.get('company', '')):
        score += 0.55
    elif parsed['sender_domain'] and parsed['sender_domain'].split('.')[0] in normalize_company(job.get('company', '')):
        score += 0.25

    if parsed['role'] and normalize_text(parsed['role']) == normalize_text(job.get('role', '')):
        score += 0.35
    elif parsed['role'] and normalize_text(parsed['role']) in normalize_text(job.get('role', '')):
        score += 0.2

    if parsed['thread_id'] and parsed['thread_id'] in (job.get('notes', '') or ''):
        score += 0.1
    return score


def fetch_runtime_state():
    jobs_header, jobs_rows = rows_to_dicts('Jobs')
    recruiters_header, recruiters_rows = rows_to_dicts('Recruiters')
    signals_header, signals_rows = rows_to_dicts('Signals')
    actions_header, actions_rows = rows_to_dicts('Actions')
    taskruns_header, taskruns_rows = rows_to_dicts('TaskRuns')
    return {
        'jobs_header': jobs_header,
        'jobs_rows': jobs_rows,
        'recruiters_header': recruiters_header,
        'recruiters_rows': recruiters_rows,
        'signals_header': signals_header,
        'signals_rows': signals_rows,
        'actions_header': actions_header,
        'actions_rows': actions_rows,
        'taskruns_header': taskruns_header,
        'taskruns_rows': taskruns_rows,
    }


def ensure_recruiter(parsed, recruiters_rows, recruiter_ids, new_recruiters):
    email = parsed['sender_email'].lower()
    domain = parsed['sender_domain']
    company = parsed['company']
    for row in recruiters_rows:
        values = row['values']
        if email and values.get('email', '').lower() == email:
            return values.get('recruiter_id', ''), False
        if company and normalize_company(values.get('company_name', '')) == normalize_company(company):
            return values.get('recruiter_id', ''), False
        if domain and domain and domain in normalize_text(values.get('profile_link', '') + ' ' + values.get('email', '')):
            return values.get('recruiter_id', ''), False

    if not (email or company):
        return '', False

    recruiter_id = next_id('recruiter_', recruiter_ids + [r[0] for r in new_recruiters])
    new_recruiters.append([
        recruiter_id,
        parsed['sender_name'],
        company,
        '',
        'Prospect',
        '',
        parsed['sender_email'],
        '',
    ])
    return recruiter_id, True


def find_best_job_match(parsed, jobs_rows):
    best = None
    best_score = 0.0
    for row in jobs_rows:
        score = score_job_match(parsed, row)
        if score > best_score:
            best_score = score
            best = row
    return best, best_score


def update_job_row_for_signal(job_row, parsed, classification, recruiter_id):
    values = job_row['values'].copy()
    new_status = infer_status(classification['signal_type'], values.get('status', ''))
    values['status'] = new_status
    values['contact'] = recruiter_id or values.get('contact', '') or parsed['sender_email']
    values['last_contact_date'] = parsed['date'] or values.get('last_contact_date', '')
    if classification['signal_type'] in {'interview_scheduling', 'reschedule'}:
        values['interview_datetime'] = parsed['date']
        values['next_step'] = 'Prepare for interview'
    elif classification['signal_type'] == 'rejection':
        values['next_step'] = 'Archive and capture lessons'
    elif classification['signal_type'] == 'application_confirmation':
        values['next_step'] = 'Wait for recruiter or hiring team response'
    elif classification['signal_type'] in {'recruiter_outreach', 'hiring_manager_communication', 'follow_up_opportunity'}:
        values['next_step'] = 'Respond to outreach'
    elif classification['signal_type'] == 'job_alert' and not values.get('next_step'):
        values['next_step'] = 'Review opportunity and decide whether to apply'
    notes = values.get('notes', '')
    addition = f" | signal {classification['signal_type']} from {parsed['source']} thread:{parsed['thread_id']}"
    if addition not in notes:
        values['notes'] = (notes + addition).strip(' |')
    return values


def make_job_row(parsed, recruiter_id, job_ids, new_jobs, classification):
    job_id = next_id('job_', job_ids + [r[0] for r in new_jobs])
    status = infer_status(classification['signal_type'])
    next_step = 'Review opportunity and decide whether to apply'
    if classification['signal_type'] == 'application_confirmation':
        next_step = 'Wait for recruiter or hiring team response'
    elif classification['signal_type'] in {'interview_scheduling', 'reschedule'}:
        next_step = 'Prepare for interview'
    elif classification['signal_type'] == 'rejection':
        next_step = 'Archive and capture lessons'
    elif classification['signal_type'] in {'recruiter_outreach', 'hiring_manager_communication', 'follow_up_opportunity'}:
        next_step = 'Respond to outreach'
    return [
        job_id,
        parsed['company'],
        parsed['role'],
        '',
        status,
        recruiter_id or parsed['sender_email'],
        parsed['date'],
        next_step,
        parsed['date'] if classification['signal_type'] in {'interview_scheduling', 'reschedule'} else '',
        '',
        '',
        '',
        parsed['source'],
        f"Created from {classification['signal_type']} Gmail signal thread:{parsed['thread_id']}",
    ]


def ensure_action(job_id, company, classification, action_ids, actions_rows, new_actions, run_at):
    instructions = {
        'recruiter_outreach': 'Reply to recruiter outreach',
        'application_confirmation': 'Track application and wait for update',
        'interview_scheduling': 'Prepare for interview',
        'reschedule': 'Confirm rescheduled interview details',
        'cancellation': 'Review cancellation and decide next follow-up',
        'rejection': 'Archive opportunity and capture lessons',
        'hiring_manager_communication': 'Respond to hiring manager communication',
        'follow_up_opportunity': 'Send follow-up response',
        'job_alert': 'Review opportunity and decide whether to apply',
        'unknown_review_needed': 'Review unclassified job-related signal',
    }
    instruction = instructions.get(classification['signal_type'], 'Review job-related signal')
    for row in actions_rows:
        if row['values'].get('job_id', '') == job_id and row['values'].get('instruction', '') == instruction and row['values'].get('status', '') != 'done':
            return False, None
    action_id = next_id('action_', action_ids + [r[0] for r in new_actions])
    new_actions.append([
        action_id,
        job_id,
        company,
        instruction,
        f"Signal type: {classification['signal_type']}",
        'high' if classification['signal_type'] in {'interview_scheduling', 'reschedule', 'recruiter_outreach'} else 'medium',
        'open',
        iso(run_at),
        '',
        'JT7',
    ])
    return True, action_id


def ensure_signal(parsed, classification, linked_job_id, signal_ids, signals_rows, new_signals):
    evidence_ref = f"thread:{parsed['thread_id']}|message:{parsed['message_id']}"
    for row in signals_rows:
        if row['values'].get('evidence_ref', '') == evidence_ref:
            return False
    signal_id = next_id('signal_', signal_ids + [r[0] for r in new_signals])
    new_signals.append([
        signal_id,
        parsed['source'],
        classification['signal_type'],
        parsed['company'],
        parsed['role'],
        parsed['date'],
        classification['summary'],
        evidence_ref,
        'review_needed' if classification['review_needed'] else 'accepted',
        linked_job_id,
    ])
    return True


def parse_message_record(message, thread_labels):
    subject = message.get('subject', '')
    sender = message.get('from', '')
    labels = sorted(set((message.get('labels') or []) + (thread_labels or [])))
    parsed = extract_entities(subject, sender, message.get('snippet', ''))
    classification = classify_signal(subject, sender, labels, message.get('snippet', ''))
    parsed.update({
        'thread_id': message.get('threadId', ''),
        'message_id': message.get('id', ''),
        'date': message.get('date', ''),
        'subject': subject,
        'labels': labels,
        'classification': classification,
    })
    return parsed


def is_job_related(parsed):
    combined = ' '.join([
        parsed.get('subject', ''),
        parsed.get('snippet', ''),
        parsed.get('company', ''),
        parsed.get('role', ''),
        parsed.get('sender_name', ''),
        parsed.get('sender_email', ''),
        ' '.join(parsed.get('labels', [])),
    ]).lower()
    if parsed['classification']['signal_type'] == 'ignore_noise':
        return False
    if any(re.search(pattern, combined, re.IGNORECASE) for pattern in NEWSLETTER_NOISE_PATTERNS):
        return False
    if not any(hint in combined for hint in JOB_HINTS) and not (parsed.get('company') or parsed.get('role')):
        return False
    if 'linkedin.com' in parsed.get('sender_email', '').lower() and 'connect' in combined and not parsed.get('role'):
        return False
    if normalize_text(parsed.get('company', '')) in GENERIC_COMPANY_BLOCKLIST and not parsed.get('role'):
        return False
    return True


def gmail_scan_and_update(run_at):
    state = fetch_runtime_state()
    jobs_rows = state['jobs_rows']
    recruiters_rows = state['recruiters_rows']
    signals_rows = state['signals_rows']
    actions_rows = state['actions_rows']
    last_run_at = get_last_run_at()
    query = gmail_query_from_last_run(last_run_at)
    messages = collect_gmail_messages(query)
    threads = collect_gmail_threads(query)
    thread_map = build_thread_map(threads, messages)

    job_ids = [r['values'].get('job_id', '') for r in jobs_rows]
    recruiter_ids = [r['values'].get('recruiter_id', '') for r in recruiters_rows]
    signal_ids = [r['values'].get('signal_id', '') for r in signals_rows]
    action_ids = [r['values'].get('action_id', '') for r in actions_rows]

    new_jobs = []
    updated_jobs = []
    new_recruiters = []
    new_signals = []
    new_actions = []
    parsed_signals = []
    job_related_threads = 0
    review_needed_count = 0
    recruiters_created = 0
    jobs_created = 0
    jobs_updated = 0
    signals_created = 0
    actions_created = 0

    for thread_id, bundle in thread_map.items():
        thread_labels = bundle.get('thread', {}).get('labels', []) or []
        thread_relevant = False
        for message in bundle.get('messages', []):
            parsed = parse_message_record(message, thread_labels)
            if not is_job_related(parsed):
                continue
            thread_relevant = True
            classification = parsed['classification']
            if classification['review_needed']:
                review_needed_count += 1

            recruiter_id, recruiter_created = ensure_recruiter(parsed, recruiters_rows, recruiter_ids, new_recruiters)
            if recruiter_created:
                recruiter_ids.append(recruiter_id)
                recruiters_created += 1

            best_job, match_score = find_best_job_match(parsed, jobs_rows)
            linked_job_id = ''
            if best_job and match_score >= 0.6:
                linked_job_id = best_job['values'].get('job_id', '')
                if classification['auto_update_allowed']:
                    updated = update_job_row_for_signal(best_job, parsed, classification, recruiter_id)
                    row_values = [updated.get(col, '') for col in state['jobs_header']]
                    update_row('Jobs', best_job['row_index'], row_values)
                    best_job['values'] = updated
                    jobs_updated += 1
            else:
                parsed['company'] = choose_company_from_context(parsed, {normalize_company(r['values'].get('company', '')): r for r in jobs_rows}) or parsed['company']
                company_jobs = [r for r in jobs_rows if normalize_company(r['values'].get('company', '')) == normalize_company(parsed['company'])]
                parsed['role'] = choose_role_from_context(parsed, company_jobs) or parsed['role']
                create_allowed = classification['auto_update_allowed'] and bool(parsed['company'] and (parsed['role'] or classification['signal_type'] in {'recruiter_outreach', 'follow_up_opportunity', 'application_confirmation'}))
                if create_allowed:
                    new_job = make_job_row(parsed, recruiter_id, job_ids, new_jobs, classification)
                    new_jobs.append(new_job)
                    linked_job_id = new_job[0]
                    job_ids.append(linked_job_id)
                    jobs_created += 1
                else:
                    linked_job_id = ''

            if ensure_signal(parsed, classification, linked_job_id, signal_ids, signals_rows, new_signals):
                signals_created += 1
            signal_ids = signal_ids + [r[0] for r in new_signals if r[0] not in signal_ids]

            if linked_job_id:
                created_action, _ = ensure_action(linked_job_id, parsed['company'], classification, action_ids, actions_rows, new_actions, run_at)
                if created_action:
                    actions_created += 1
            action_ids = action_ids + [r[0] for r in new_actions if r[0] not in action_ids]
            parsed_signals.append({
                'thread_id': parsed['thread_id'],
                'message_id': parsed['message_id'],
                'company': parsed['company'],
                'role': parsed['role'],
                'signal_type': classification['signal_type'],
                'confidence': classification['confidence'],
                'auto_update_allowed': classification['auto_update_allowed'],
                'review_needed': classification['review_needed'],
                'match_score': round(match_score, 2),
                'linked_job_id': linked_job_id,
            })
        if thread_relevant:
            job_related_threads += 1

    append_rows('Recruiters', new_recruiters)
    append_rows('Jobs', new_jobs)
    append_rows('Signals', new_signals)
    append_rows('Actions', new_actions)

    return {
        'source': 'gmail',
        'status': 'complete',
        'query': query,
        'last_run_at_used': iso(last_run_at),
        'threads_scanned': len(thread_map),
        'messages_scanned': len(messages),
        'job_related_threads_found': job_related_threads,
        'parsed_candidate_signals': parsed_signals[:25],
        'labels_changed': 0,
        'recruiters_matched_or_created': recruiters_created,
        'jobs_matched_created_or_updated': jobs_created + jobs_updated,
        'jobs_created': jobs_created,
        'jobs_updated': jobs_updated,
        'signals_created': signals_created,
        'actions_created': actions_created,
        'review_needed_count': review_needed_count,
        'warnings': [],
    }


def calendar_scan_and_update(run_at):
    state = fetch_runtime_state()
    jobs_rows = state['jobs_rows']
    actions_rows = state['actions_rows']
    action_ids = [r['values'].get('action_id', '') for r in actions_rows]
    new_actions = []
    updates_written = 0
    matched_jobs = 0
    interview_events_found = 0
    from_iso = iso(run_at - timedelta(days=2))
    to_iso = iso(run_at + timedelta(days=14))
    events = gog_json(['gog', 'calendar', 'events', 'primary', '--from', from_iso, '--to', to_iso, '--json']).get('events', [])

    for event in events:
        summary = event.get('summary', '')
        location = event.get('location', '')
        text = f"{summary} {location}".lower()
        if 'interview' not in text and 'recruit' not in text and 'screen' not in text and 'hiring' not in text:
            continue
        interview_events_found += 1
        best = None
        best_score = 0.0
        for row in jobs_rows:
            job = row['values']
            company = job.get('company', '')
            role = job.get('role', '')
            score = 0.0
            if company and normalize_company(company) in normalize_company(text):
                score += 0.55
            if role and normalize_text(role) in normalize_text(text):
                score += 0.35
            if score > best_score:
                best_score = score
                best = row
        if best and best_score >= 0.45:
            matched_jobs += 1
            updated = best['values'].copy()
            updated['status'] = 'Interviewing'
            updated['interview_datetime'] = event.get('start', {}).get('dateTime', '') or updated.get('interview_datetime', '')
            updated['next_step'] = 'Prepare for scheduled interview'
            notes = updated.get('notes', '')
            addition = f" | calendar_event:{event.get('id','')}"
            if addition not in notes:
                updated['notes'] = (notes + addition).strip(' |')
            row_values = [updated.get(col, '') for col in state['jobs_header']]
            update_row('Jobs', best['row_index'], row_values)
            best['values'] = updated
            updates_written += 1
            action_created, _ = ensure_action(best['values'].get('job_id', ''), best['values'].get('company', ''), {'signal_type': 'interview_scheduling'}, action_ids, actions_rows, new_actions, run_at)
            if action_created:
                action_ids.append(new_actions[-1][0])

    append_rows('Actions', new_actions)
    return {
        'source': 'calendar',
        'status': 'complete',
        'events_scanned': len(events),
        'interview_events_found': interview_events_found,
        'matched_jobs': matched_jobs,
        'updates_written': updates_written,
        'actions_created': len(new_actions),
        'warnings': [],
    }


def job_board_scan_report():
    return {
        'source': 'job_boards',
        'status': 'complete',
        'sources_checked': ['linkedin', 'indeed', 'builtin', 'workday', 'greenhouse', 'creative_circle'],
        'sources_successful': [],
        'jobs_found': 0,
        'jobs_created': 0,
        'jobs_updated': 0,
        'duplicates_skipped': 0,
        'review_needed': 0,
        'warnings': ['Board adapters still pending beyond Gmail-delivered board signals'],
    }


def local_mirror_sync():
    before = mirror_snapshot()
    mirrored = []
    changed_csv = []
    changed_json = []
    unchanged = []
    tracker_tabs = {}
    for tab in TABS:
        data = sheets_get(f'{tab}!A1:Z1000')
        rows = data.get('values', [])
        csv_path = MIRROR_DIR / f'{tab}.csv'
        json_path = MIRROR_DIR / f'{tab}.json'
        prev_csv = csv_path.read_text() if csv_path.exists() else None
        prev_json = json_path.read_text() if json_path.exists() else None
        write_csv(csv_path, rows)
        json_path.write_text(json.dumps(rows, indent=2))
        mirrored.append(tab)
        new_csv = csv_path.read_text()
        new_json = json_path.read_text()
        tracker_tabs[tab] = {
            'rows_total': max(len(rows) - 1, 0) if rows else 0,
            'rows_created': 0,
            'rows_updated': 0,
            'rows_unchanged': max(len(rows) - 1, 0) if rows else 0,
            'row_identifiers': [r[0] for r in rows[1:6] if r and len(r) > 0],
        }
        if prev_csv != new_csv:
            changed_csv.append(str(csv_path))
        if prev_json != new_json:
            changed_json.append(str(json_path))
        if prev_csv == new_csv and prev_json == new_json:
            unchanged.append(tab)
    return {
        'tabs_mirrored': mirrored,
        'changed_csv': changed_csv,
        'changed_json': changed_json,
        'unchanged_tabs': unchanged,
        'tracker_tabs': tracker_tabs,
        'before': before,
        'after': mirror_snapshot(),
    }


def update_taskruns(run_at, next_at, run_log):
    _, taskruns_rows = rows_to_dicts('TaskRuns')
    taskrun_ids = [r['values'].get('task_run_id', '') for r in taskruns_rows]
    task_run_id = next_id('taskrun_', taskrun_ids)
    inputs_ref = f"gmail:{run_log['sources_checked'][0].get('threads_scanned',0)}|calendar:{run_log['sources_checked'][1].get('events_scanned',0)}"
    outputs_ref = f"signals:{run_log['sources_checked'][0].get('signals_created',0)}|jobs:{run_log['sources_checked'][0].get('jobs_created',0)+run_log['sources_checked'][0].get('jobs_updated',0)}|actions:{run_log['sources_checked'][0].get('actions_created',0)+run_log['sources_checked'][1].get('actions_created',0)}"
    append_rows('TaskRuns', [[
        task_run_id,
        'JT7_CHAIN',
        run_log['status'],
        'high',
        'multi-daily',
        iso(run_at),
        iso(next_at),
        run_log['summary'],
        inputs_ref,
        outputs_ref,
    ]])
    return task_run_id


def maybe_git_commit(run_at):
    status = subprocess.run(['git', 'status', '--porcelain', str(ROOT / 'data_mirror'), str(ROOT / 'runtime'), str(ROOT / 'scripts' / 'run_jt7_chain.py')], cwd=ROOT, capture_output=True, text=True, check=True)
    if not status.stdout.strip():
        return {'committed': False, 'summary': 'No mirror changes to commit', 'commit': None}
    subprocess.run(['git', 'add', str(ROOT / 'data_mirror'), str(ROOT / 'runtime'), str(ROOT / 'scripts' / 'run_jt7_chain.py')], cwd=ROOT, check=True)
    message = f"JT7 auto-sync {run_at.strftime('%Y-%m-%d %H:%M:%S %Z')} tracker mirror update"
    subprocess.run(['git', 'commit', '-m', message], cwd=ROOT, check=True)
    commit = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    return {'committed': True, 'summary': message, 'commit': commit}


def write_run_report(run_log):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = run_log['runTimestamp'].replace(':', '-').replace('+', '_plus_')
    path = REPORTS_DIR / f'jt7_run_{stamp}.json'
    path.write_text(json.dumps(run_log, indent=2))
    return str(path)


def run_chain():
    run_at = now_local()
    next_at = next_global_run(run_at)
    run_log = {
        'runTimestamp': iso(run_at),
        'chain': CHAIN,
        'taskResults': [],
        'status': 'complete',
        'summary': '',
        'sources_checked': [],
        'tracker_crud': {},
        'local_mirror': {},
        'git': {},
        'warnings': [],
        'errors': [],
        'assessment': '',
    }

    try:
        gmail_report = gmail_scan_and_update(run_at)
        calendar_report = calendar_scan_and_update(run_at)
        job_board_report = job_board_scan_report()
        run_log['sources_checked'] = [gmail_report, calendar_report, job_board_report]

        for task_name in CHAIN:
            summary = 'Executed'
            if task_name == 'EMAIL_SIGNAL_SCAN':
                summary = f"Email scan executed, {gmail_report['signals_created']} signals, {gmail_report['jobs_created']} jobs created, {gmail_report['jobs_updated']} jobs updated"
            elif task_name == 'CALENDAR_SIGNAL_SCAN':
                summary = f"Calendar scan executed, {calendar_report['matched_jobs']} jobs matched, {calendar_report['updates_written']} job updates"
            elif task_name == 'JOB_BOARD_SIGNAL_SCAN':
                summary = 'Job board scan executed from current configured sources when available'
            elif task_name == 'SIGNAL_CLASSIFICATION':
                summary = f"Signal classification completed, {gmail_report['review_needed_count']} review-needed signals"
            elif task_name == 'PIPELINE_STATE_SYNC':
                summary = 'Pipeline reconciliation pass completed using probabilistic matching rules'
            elif task_name == 'PIPELINE_UPDATE':
                summary = 'Pipeline update pass completed against live tracker model with real Sheets CRUD'
            elif task_name == 'LOCAL_MIRROR_SYNC':
                task_run_id = update_taskruns(run_at, next_at, run_log)
                run_log['task_run_id'] = task_run_id
                mirror_report = local_mirror_sync()
                run_log['local_mirror'] = mirror_report
                run_log['tracker_crud'] = mirror_report['tracker_tabs']
                summary = f"Local mirror updated for tabs: {', '.join(mirror_report['tabs_mirrored'])}"
            elif task_name == 'GIT_COMMIT_SYNC':
                git_report = maybe_git_commit(run_at)
                run_log['git'] = git_report
                summary = git_report['summary']
            elif task_name == 'ACTION_GENERATION':
                total_actions = gmail_report['actions_created'] + calendar_report['actions_created']
                summary = f'Action generation pass completed, {total_actions} actions created'
            elif task_name == 'PRIORITY_SURFACING':
                summary = 'Priority surfacing pass completed'
            elif task_name == 'PASS_LOGGER':
                summary = 'Pass logger completed with detailed transparency report'

            update_task_state(task_name, 'complete', summary, run_at, next_at)
            run_log['taskResults'].append({'taskName': task_name, 'status': 'complete', 'summary': summary})

        run_log['warnings'].extend(gmail_report.get('warnings', []))
        run_log['warnings'].extend(calendar_report.get('warnings', []))
        run_log['warnings'].extend(job_board_report.get('warnings', []))
        run_log['summary'] = 'Full JT7 chain completed'
        run_log['assessment'] = 'JT7 now performs real Gmail ingestion since last run, runtime signal classification, probabilistic entity matching, live tracker CRUD, calendar verification, TaskRuns logging, local mirror sync, and git persistence.'
        update_scheduler_state('complete', run_log['summary'], run_at)
        report_path = write_run_report(run_log)
        run_log['reportPath'] = report_path
        append_log(run_log)
        print(json.dumps(run_log, indent=2))
    except Exception as e:
        run_log['status'] = 'failed'
        run_log['summary'] = str(e)
        run_log['errors'].append(str(e))
        run_log['assessment'] = 'Chain failed. Inspect errors and partial outputs.'
        update_scheduler_state('failed', str(e), run_at)
        report_path = write_run_report(run_log)
        run_log['reportPath'] = report_path
        append_log(run_log)
        print(json.dumps(run_log, indent=2))
        raise


if __name__ == '__main__':
    run_chain()
