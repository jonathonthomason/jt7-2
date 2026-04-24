#!/usr/bin/env python3
import csv
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta
from email.utils import parseaddr
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.append('/Users/jtemp/.openclaw/workspace/job-search-ui')

from runtime.domain.actions import ACTION_REQUIRED_SIGNAL_TYPES
from runtime.domain.jobs import make_job_row, update_job_row_for_signal
from runtime.ingestion.gmail import build_thread_map, collect_gmail_messages, collect_gmail_threads
from runtime.pipelines.calendar_pipeline import calendar_scan_and_update
from runtime.pipelines.chain_runner import build_task_summary
from runtime.pipelines.job_board_pipeline import job_board_scan_report
from runtime.services.action_generation import ACTION_ROW_COLUMNS, build_action_row
from runtime.services.action_lifecycle import apply_action_update
from runtime.services.classification import classify_signal, extract_entities, is_job_related, parse_message_record
from runtime.services.reconciliation import find_best_job_match
from runtime.services.recruiter_matching import ensure_recruiter
from runtime.services.review_queue import confidence_bucket, ensure_review_queue_entry, should_block_job_creation
from runtime.services.signal_lifecycle import ensure_signal
from runtime.storage.local_mirror import local_mirror_sync
from runtime.storage.reporting import write_run_report
from runtime.storage.runtime_state import fetch_runtime_state
from runtime.storage.sheets_repo import append_rows, rows_to_dicts, update_row
from runtime.storage.taskruns_repo import update_taskruns

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
TABS = ['Jobs', 'Recruiters', 'Competition', 'Signals', 'Actions', 'ReviewQueue', 'TaskRuns', 'Lookup']
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
GENERIC_COMPANY_BLOCKLIST = {'linkedin job alerts', 'linkedin', 'indeed', 'mail', 'em', 'builtin', 'built in'}
NO_JOB_CREATE_SOURCES = {'linkedin job alerts', 'builtin', 'built in', 'indeed job alerts', 'job alerts'}
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


def next_id(prefix, existing_ids):
    max_n = 0
    for value in existing_ids:
        if isinstance(value, str) and value.startswith(prefix):
            tail = value.replace(prefix, '')
            if tail.isdigit():
                max_n = max(max_n, int(tail))
    return f'{prefix}{max_n + 1:03d}'


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


def ensure_action(job_id, company, classification, action_ids, actions_rows, new_actions, run_at, signal_id=''):
    action_row = build_action_row(
        next_id('action_', action_ids + [r[0] for r in new_actions]),
        job_id,
        company,
        classification,
        run_at,
        signal_id=signal_id,
    )
    instruction = action_row[3]
    for row in actions_rows:
        if row['values'].get('job_id', '') == job_id and row['values'].get('instruction', '') == instruction and row['values'].get('status', '') != 'done':
            updated = apply_action_update(row['values'], classification, run_at, signal_id=signal_id)
            row_values = [updated.get(col, '') for col in ACTION_ROW_COLUMNS]
            update_row('Actions', row['row_index'], row_values, sheets_update)
            row['values'] = updated
            return False, row['values'].get('action_id', '')
    new_actions.append(action_row)
    return True, action_row[0]


def gmail_scan_and_update(run_at):
    state = fetch_runtime_state(lambda tab: rows_to_dicts(tab, sheets_get, MIRROR_DIR))
    jobs_rows = state['jobs_rows']
    recruiters_rows = state['recruiters_rows']
    signals_rows = state['signals_rows']
    actions_rows = state['actions_rows']
    review_rows = state['review_rows']
    last_run_at = get_last_run_at()
    query = gmail_query_from_last_run(last_run_at)
    messages = collect_gmail_messages(query, gog_json)
    threads = collect_gmail_threads(query, gog_json)
    thread_map = build_thread_map(threads, messages)

    job_ids = [r['values'].get('job_id', '') for r in jobs_rows]
    recruiter_ids = [r['values'].get('recruiter_id', '') for r in recruiters_rows]
    signal_ids = [r['values'].get('signal_id', '') for r in signals_rows]
    action_ids = [r['values'].get('action_id', '') for r in actions_rows]
    review_ids = [r['values'].get('review_id', '') for r in review_rows]

    new_jobs = []
    updated_jobs = []
    new_recruiters = []
    new_signals = []
    new_actions = []
    new_reviews = []
    parsed_signals = []
    job_related_threads = 0
    review_needed_count = 0
    recruiters_created = 0
    jobs_created = 0
    jobs_updated = 0
    signals_created = 0
    signals_updated = 0
    actions_created = 0
    review_needed_created = 0
    signals_marked_review_required = 0
    blocked_job_creations = 0
    orphan_actions = 0
    signal_to_job_update = []
    signal_to_action = []
    signals_by_confidence = {'high': 0, 'medium': 0, 'low': 0}

    for thread_id, bundle in thread_map.items():
        thread_labels = bundle.get('thread', {}).get('labels', []) or []
        thread_relevant = False
        for message in bundle.get('messages', []):
            parsed = parse_message_record(message, thread_labels, lambda subject, sender, snippet: extract_entities(subject, sender, snippet, extract_domain, LINKEDIN_ROLE_RE, LINKEDIN_SIMPLE_ROLE_RE, INDEED_ROLE_RE, THOMSON_REUTERS_RE, APPLICATION_RE, normalize_text, GENERIC_COMPANY_BLOCKLIST), lambda subject, sender, labels, body: classify_signal(subject, sender, labels, body, CLASSIFICATION_RULES, NEWSLETTER_NOISE_PATTERNS))
            if not is_job_related(parsed, NEWSLETTER_NOISE_PATTERNS, JOB_HINTS, normalize_text, GENERIC_COMPANY_BLOCKLIST):
                continue
            thread_relevant = True
            classification = parsed['classification']
            bucket = confidence_bucket(classification['confidence'])
            signals_by_confidence[bucket] += 1
            if classification['review_needed'] or bucket == 'medium':
                review_needed_count += 1

            recruiter_id, recruiter_created = ensure_recruiter(parsed, recruiters_rows, recruiter_ids, new_recruiters, normalize_company, normalize_text, next_id)
            if recruiter_created:
                recruiter_ids.append(recruiter_id)
                recruiters_created += 1

            best_job, match_score = find_best_job_match(parsed, jobs_rows, score_job_match)
            linked_job_id = ''

            if best_job and match_score >= 0.6:
                linked_job_id = best_job['values'].get('job_id', '')
            else:
                parsed['company'] = choose_company_from_context(parsed, {normalize_company(r['values'].get('company', '')): r for r in jobs_rows}) or parsed['company']
                company_jobs = [r for r in jobs_rows if normalize_company(r['values'].get('company', '')) == normalize_company(parsed['company'])]
                parsed['role'] = choose_role_from_context(parsed, company_jobs) or parsed['role']

            blocked_job_create, block_reason = should_block_job_creation(parsed, classification, normalize_text, NO_JOB_CREATE_SOURCES, GENERIC_COMPANY_BLOCKLIST)
            if blocked_job_create:
                classification['no_job_create'] = True
                classification['review_needed'] = True
                if classification['confidence'] > 0.5:
                    classification['confidence'] = 0.5
                signals_marked_review_required += 1

            signal_created, signal_id, signal_persisted = ensure_signal(parsed, classification, linked_job_id, signal_ids, signals_rows, new_signals, state['signals_header'], lambda tab, row_index, row_values: update_row(tab, row_index, row_values, sheets_update), next_id)
            if signal_created:
                signals_created += 1
            else:
                signals_updated += 1
            if signal_id and signal_id not in signal_ids:
                signal_ids.append(signal_id)

            create_allowed = bucket == 'high' and not blocked_job_create and bool(parsed['company'] and parsed['role'] and signal_id)
            if signal_id and not linked_job_id and create_allowed:
                new_job = make_job_row(parsed, recruiter_id, next_id('job_', job_ids + [r[0] for r in new_jobs]), classification, infer_status)
                new_job[-1] = f"{new_job[-1]} | signal_id:{signal_id}"
                new_jobs.append(new_job)
                linked_job_id = new_job[0]
                job_ids.append(linked_job_id)
                jobs_created += 1
                new_signals[-1][-1] = linked_job_id
                signal_to_job_update.append({'signal_id': signal_id, 'job_id': linked_job_id, 'mode': 'create'})
            elif signal_id and linked_job_id and bucket == 'high' and classification['auto_update_allowed']:
                updated = update_job_row_for_signal(best_job, parsed, classification, recruiter_id, infer_status)
                notes = updated.get('notes', '')
                addition = f" | signal_id:{signal_id}"
                if addition not in notes:
                    updated['notes'] = (notes + addition).strip(' |')
                row_values = [updated.get(col, '') for col in state['jobs_header']]
                update_row('Jobs', best_job['row_index'], row_values, sheets_update)
                best_job['values'] = updated
                jobs_updated += 1
                if signal_created:
                    new_signals[-1][-1] = linked_job_id
                signal_to_job_update.append({'signal_id': signal_id, 'job_id': linked_job_id, 'mode': 'update'})
            else:
                if blocked_job_create and not linked_job_id:
                    blocked_job_creations += 1
                if bucket == 'medium' or blocked_job_create:
                    created_review, _ = ensure_review_queue_entry(parsed, classification, signal_id, linked_job_id, review_rows, review_ids, new_reviews, recruiter_id, match_score, next_id, ACTION_REQUIRED_SIGNAL_TYPES, infer_status, lambda: iso(now_local()))
                    if created_review:
                        review_needed_created += 1

            requires_action = classification['signal_type'] in ACTION_REQUIRED_SIGNAL_TYPES and classification['signal_type'] != 'ignore_noise'
            if linked_job_id and signal_id and bucket == 'high' and requires_action:
                created_action, action_id = ensure_action(linked_job_id, parsed['company'], classification, action_ids, actions_rows, new_actions, run_at, signal_id=signal_id)
                if created_action:
                    actions_created += 1
                    signal_to_action.append({'signal_id': signal_id, 'action_id': action_id, 'job_id': linked_job_id})
            elif requires_action and not signal_id:
                orphan_actions += 1
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

    append_rows('Recruiters', new_recruiters, MIRROR_DIR, write_csv, sheets_append)
    append_rows('Jobs', new_jobs, MIRROR_DIR, write_csv, sheets_append)
    append_rows('Signals', new_signals, MIRROR_DIR, write_csv, sheets_append)
    append_rows('Actions', new_actions, MIRROR_DIR, write_csv, sheets_append)
    append_rows('ReviewQueue', new_reviews, MIRROR_DIR, write_csv, sheets_append)

    warnings = []
    signals_persisted = signals_created + signals_updated
    if job_related_threads > 0 and signals_persisted == 0:
        warnings.append('Run incomplete: job-related threads found but zero persisted signals')

    return {
        'source': 'gmail',
        'status': 'failed' if job_related_threads > 0 and signals_persisted == 0 else 'complete',
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
        'signals_updated': signals_updated,
        'signals_persisted': signals_persisted,
        'signals_marked_review_required': signals_marked_review_required,
        'actions_created': actions_created,
        'review_needed_count': review_needed_count,
        'review_needed_created': review_needed_created,
        'blocked_job_creations': blocked_job_creations,
        'orphan_actions': orphan_actions,
        'review_queue_pending_count': len([r for r in review_rows if r['values'].get('status', '') == 'pending']) + review_needed_created,
        'signals_by_confidence': signals_by_confidence,
        'signal_to_job_update': signal_to_job_update,
        'signal_to_action': signal_to_action,
        'warnings': warnings,
    }


def maybe_git_commit(run_at):
    status = subprocess.run(['git', 'status', '--porcelain', str(ROOT / 'data_mirror'), str(ROOT / 'runtime'), str(ROOT / 'scripts' / 'run_jt7_chain.py')], cwd=ROOT, capture_output=True, text=True, check=True)
    if not status.stdout.strip():
        return {'committed': False, 'summary': 'No mirror changes to commit', 'commit': None}
    subprocess.run(['git', 'add', str(ROOT / 'data_mirror'), str(ROOT / 'runtime'), str(ROOT / 'scripts' / 'run_jt7_chain.py')], cwd=ROOT, check=True)
    message = f"JT7 auto-sync {run_at.strftime('%Y-%m-%d %H:%M:%S %Z')} tracker mirror update"
    subprocess.run(['git', 'commit', '-m', message], cwd=ROOT, check=True)
    commit = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    return {'committed': True, 'summary': message, 'commit': commit}


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
        state_for_calendar = fetch_runtime_state(lambda tab: rows_to_dicts(tab, sheets_get, MIRROR_DIR))
        action_ids = [r['values'].get('action_id', '') for r in state_for_calendar['actions_rows']]
        calendar_report = calendar_scan_and_update(run_at, gog_json, lambda tab: rows_to_dicts(tab, sheets_get, MIRROR_DIR), ensure_action, action_ids, state_for_calendar['actions_rows'], [], append_rows, MIRROR_DIR, write_csv, sheets_append, iso, timedelta, normalize_company, normalize_text, lambda tab, row_index, row_values: update_row(tab, row_index, row_values, sheets_update))
        job_board_report = job_board_scan_report()
        run_log['sources_checked'] = [gmail_report, calendar_report, job_board_report]

        for task_name in CHAIN:
            if task_name == 'LOCAL_MIRROR_SYNC':
                task_run_id = update_taskruns(run_at, next_at, run_log, lambda tab: rows_to_dicts(tab, sheets_get, MIRROR_DIR), next_id, lambda tab, rows: append_rows(tab, rows, MIRROR_DIR, write_csv, sheets_append), iso)
                run_log['task_run_id'] = task_run_id
                mirror_report = local_mirror_sync(TABS, MIRROR_DIR, mirror_snapshot, sheets_get, write_csv)
                run_log['local_mirror'] = mirror_report
                run_log['tracker_crud'] = mirror_report['tracker_tabs']
                summary = build_task_summary(task_name, gmail_report, calendar_report, run_log.get('git'), mirror_report)
            elif task_name == 'GIT_COMMIT_SYNC':
                git_report = maybe_git_commit(run_at)
                run_log['git'] = git_report
                summary = build_task_summary(task_name, gmail_report, calendar_report, git_report, run_log.get('local_mirror'))
            else:
                summary = build_task_summary(task_name, gmail_report, calendar_report, run_log.get('git'), run_log.get('local_mirror'))

            update_task_state(task_name, 'complete', summary, run_at, next_at)
            run_log['taskResults'].append({'taskName': task_name, 'status': 'complete', 'summary': summary})

        run_log['warnings'].extend(gmail_report.get('warnings', []))
        run_log['warnings'].extend(calendar_report.get('warnings', []))
        run_log['warnings'].extend(job_board_report.get('warnings', []))
        run_log['summary'] = 'Full JT7 chain completed'
        run_log['assessment'] = 'JT7 now performs real Gmail ingestion since last run, runtime signal classification, probabilistic entity matching, live tracker CRUD, calendar verification, TaskRuns logging, local mirror sync, and git persistence.'
        update_scheduler_state('complete', run_log['summary'], run_at)
        report_path = write_run_report(run_log, REPORTS_DIR)
        run_log['reportPath'] = report_path
        append_log(run_log)
        print(json.dumps(run_log, indent=2))
    except Exception as e:
        run_log['status'] = 'failed'
        run_log['summary'] = str(e)
        run_log['errors'].append(str(e))
        run_log['assessment'] = 'Chain failed. Inspect errors and partial outputs.'
        update_scheduler_state('failed', str(e), run_at)
        report_path = write_run_report(run_log, REPORTS_DIR)
        run_log['reportPath'] = report_path
        append_log(run_log)
        print(json.dumps(run_log, indent=2))
        raise


if __name__ == '__main__':
    run_chain()
