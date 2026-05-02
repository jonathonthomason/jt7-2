#!/usr/bin/env python3
import csv
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.append('/Users/jtemp/.openclaw/workspace/job-search-ui')

from runtime.domain.actions import ACTION_REQUIRED_SIGNAL_TYPES
from runtime.pipelines.gmail_pipeline import gmail_scan_and_update
from runtime.domain.jobs import make_job_row, update_job_row_for_signal
from runtime.ingestion.gmail import build_thread_map, collect_gmail_messages, collect_gmail_threads
from runtime.pipelines.calendar_pipeline import calendar_scan_and_update
from runtime.pipelines.chain_runner import build_task_summary
from runtime.pipelines.job_board_pipeline import job_board_scan_report
from runtime.services.action_generation import ACTION_ROW_COLUMNS, build_action_row
from runtime.services.action_lifecycle import apply_action_update
from runtime.services.action_normalization import normalized_action_due_at, normalized_action_reason, normalized_action_status
from runtime.services.signal_cleanup import should_ignore_existing_signal
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
from runtime.utils.file_utils import load_json, save_json, write_csv
from runtime.utils.id_utils import next_id
from runtime.utils.text_utils import extract_domain, normalize_company, normalize_text
from runtime.utils.time_utils import missed_run_slots, next_global_run, next_run_after, parse_dt

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

GOG_BIN = shutil.which('gog') or '/opt/homebrew/bin/gog'
GOG_ACCOUNT = 'jonathon.thomason@gmail.com'
GOG_BASE_ARGS = ['--json', '--no-input', '--account', GOG_ACCOUNT]
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


def update_task_state(task_name, status, summary, run_at, next_at):
    data = load_json(TASKS_FILE)
    for task in data['tasks']:
        if task['taskName'] == task_name:
            task['lastRunAt'] = iso(run_at)
            task['nextRunAt'] = iso(next_at)
            task['lastStatus'] = status
            task['lastSummary'] = summary
    save_json(TASKS_FILE, data)


def enabled_run_times():
    data = load_json(SCHEDULER_FILE)
    return [run['time'] for run in data['schedule'] if run.get('isEnabled', True)]


# Resume-time policy: if one or more schedule windows were missed since the last
# recorded scheduler execution, the next invocation becomes a single consolidated
# catch-up pass rather than silently skipping those windows.
def scheduler_context(current):
    data = load_json(SCHEDULER_FILE)
    runs = data.get('schedule', [])
    enabled_times = [run['time'] for run in runs if run.get('isEnabled', True)]
    last_run_values = [parse_dt(run.get('lastRunAt')) for run in runs if run.get('lastRunAt')]
    last_run_values = [dt for dt in last_run_values if dt]
    last_run_at = max(last_run_values) if last_run_values else None
    missed_slots = missed_run_slots(last_run_at, current, enabled_times)
    scheduled_for = missed_slots[0] if missed_slots else current
    trigger_mode = 'catch-up' if missed_slots else 'scheduled'
    return {
        'enabled_times': enabled_times,
        'lastRunAt': last_run_at,
        'missedSlots': missed_slots,
        'scheduledFor': scheduled_for,
        'triggerMode': trigger_mode,
    }


def update_scheduler_state(status, summary, executed_at, scheduled_for=None, trigger_mode='scheduled', missed_slots=None):
    data = load_json(SCHEDULER_FILE)
    for run in data['schedule']:
        run['lastRunAt'] = iso(executed_at)
        run['nextRunAt'] = iso(next_run_after(executed_at, run['time']))
        run['lastStatus'] = status
        run['lastSummary'] = summary

    data['lastTriggerMode'] = trigger_mode
    data['lastExecutedAt'] = iso(executed_at)
    data['lastScheduledFor'] = iso(scheduled_for or executed_at)
    data['lastMissedSlots'] = [iso(slot) for slot in (missed_slots or [])]
    data['catchUpPolicy'] = 'single-pass-on-resume'
    save_json(SCHEDULER_FILE, data)


def append_log(entry):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open('a') as f:
        f.write(json.dumps(entry) + '\n')


def gog_json(args):
    cmd = [GOG_BIN, *args]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        stderr = (e.stderr or '').strip()
        stdout = (e.stdout or '').strip()
        detail = stderr or stdout or str(e)
        raise RuntimeError(f'gog command failed: {cmd} :: {detail}') from e
    return json.loads(result.stdout)


def sheets_get(range_name):
    return gog_json(['sheets', 'get', SHEET_ID, range_name, *GOG_BASE_ARGS])


def sheets_update(range_name, values):
    subprocess.run(
        [GOG_BIN, 'sheets', 'update', SHEET_ID, range_name, '--values-json', json.dumps(values), '--input', 'USER_ENTERED', '--no-input', '--account', GOG_ACCOUNT],
        check=True, capture_output=True, text=True,
    )


def sheets_append(range_name, values):
    subprocess.run(
        [GOG_BIN, 'sheets', 'append', SHEET_ID, range_name, '--values-json', json.dumps(values), '--insert', 'INSERT_ROWS', '--no-input', '--account', GOG_ACCOUNT],
        check=True, capture_output=True, text=True,
    )


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


def get_last_run_at():
    tasks = load_json(TASKS_FILE)['tasks']
    runs = [parse_dt(t.get('lastRunAt')) for t in tasks if t.get('lastRunAt')]
    runs = [r for r in runs if r]
    if runs:
        return max(runs)
    return now_local() - timedelta(days=DEFAULT_GMAIL_LOOKBACK_DAYS)


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


def action_classification_for_signal(signal_type, job_status=''):
    normalized_status = (job_status or '').strip().lower()
    return {
        'signal_type': signal_type,
        'no_job_create': False,
        'resolved': signal_type in {'rejection', 'cancellation'} or normalized_status in {'rejected'},
        'completed': normalized_status in {'rejected'},
        'waiting': signal_type == 'application_confirmation' or normalized_status in {'applied', 'offer'},
    }


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



def normalize_existing_actions(run_at):
    state = fetch_runtime_state(lambda tab: rows_to_dicts(tab, sheets_get, MIRROR_DIR))
    jobs_by_id = {row['values'].get('job_id', ''): row['values'] for row in state['jobs_rows']}
    signals_by_job = {}
    for row in state['signals_rows']:
        linked_job_id = row['values'].get('linked_job_id', '')
        if linked_job_id:
            signals_by_job.setdefault(linked_job_id, []).append(row['values'])

    actions_updated = 0
    for row in state['actions_rows']:
        action = row['values']
        job = jobs_by_id.get(action.get('job_id', ''), {})
        linked_signals = signals_by_job.get(action.get('job_id', ''), [])
        updated = action.copy()
        updated['status'] = normalized_action_status(action, job, linked_signals)
        updated['reason'] = normalized_action_reason(action, linked_signals)
        updated['due_at'] = normalized_action_due_at(action, linked_signals, run_at)
        row_values = [updated.get(col, '') for col in ACTION_ROW_COLUMNS]
        current_values = [action.get(col, '') for col in ACTION_ROW_COLUMNS]
        if row_values != current_values:
            update_row('Actions', row['row_index'], row_values, sheets_update)
            row['values'] = updated
            actions_updated += 1
    return actions_updated


def cleanup_existing_signals():
    state = fetch_runtime_state(lambda tab: rows_to_dicts(tab, sheets_get, MIRROR_DIR))
    signals_updated = 0
    for row in state['signals_rows']:
        signal = row['values']
        if should_ignore_existing_signal(signal, normalize_text) and signal.get('status', '') != 'ignored':
            updated = signal.copy()
            updated['status'] = 'ignored'
            row_values = [updated.get(col, '') for col in state['signals_header']]
            current_values = [signal.get(col, '') for col in state['signals_header']]
            if row_values != current_values:
                update_row('Signals', row['row_index'], row_values, sheets_update)
                signals_updated += 1
    return signals_updated

GIT_SYNC_INCLUDE_PREFIXES = [
    'data_mirror/',
    'runtime/reports/',
]

GIT_SYNC_INCLUDE_FILES = {
    'runtime/jt7_pass_log.jsonl',
    'runtime/jt7_scheduler.json',
    'runtime/jt7_tasks.json',
}

GIT_SYNC_EXCLUDE_PREFIXES = [
    'runtime/browser_profiles/',
]


def _git_status_paths():
    status = subprocess.run(
        ['git', 'status', '--porcelain'],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    paths = []
    for line in status.stdout.splitlines():
        if not line:
            continue
        path_part = line[3:]
        if ' -> ' in path_part:
            path_part = path_part.split(' -> ', 1)[1]
        paths.append(path_part.strip())
    return paths


def _git_sync_candidates():
    candidates = []
    repo_prefix = f'{ROOT.name}/'
    for path in _git_status_paths():
        rel = Path(path).as_posix()
        if rel.startswith(repo_prefix):
            rel = rel[len(repo_prefix):]
        if any(rel.startswith(prefix) for prefix in GIT_SYNC_EXCLUDE_PREFIXES):
            continue
        if rel in GIT_SYNC_INCLUDE_FILES or any(rel.startswith(prefix) for prefix in GIT_SYNC_INCLUDE_PREFIXES):
            candidates.append(rel)
    return sorted(dict.fromkeys(candidates))


def maybe_git_commit(run_at):
    candidates = _git_sync_candidates()
    if not candidates:
        return {'committed': False, 'summary': 'No mirror changes to commit', 'commit': None}
    subprocess.run(['git', 'add', '--', *candidates], cwd=ROOT, check=True)
    message = f"JT7 auto-sync {run_at.strftime('%Y-%m-%d %H:%M:%S %Z')} tracker mirror update"
    subprocess.run(['git', 'commit', '-m', message], cwd=ROOT, check=True)
    commit = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    return {'committed': True, 'summary': message, 'commit': commit}


def run_chain():
    wall_clock_at = now_local()
    sched = scheduler_context(wall_clock_at)
    run_at = wall_clock_at
    scheduled_for = sched['scheduledFor']
    next_at = next_global_run(wall_clock_at, sched['enabled_times'] or RUN_TIMES)
    run_log = {
        'runTimestamp': iso(run_at),
        'scheduledFor': iso(scheduled_for),
        'triggerMode': sched['triggerMode'],
        'missedSlotsCount': len(sched['missedSlots']),
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
        cleaned_signals = cleanup_existing_signals()
        gmail_report = gmail_scan_and_update(
            run_at,
            fetch_runtime_state,
            rows_to_dicts,
            sheets_get,
            MIRROR_DIR,
            get_last_run_at,
            now_local,
            DEFAULT_GMAIL_LOOKBACK_DAYS,
            JOB_LABEL_QUERY,
            collect_gmail_messages,
            collect_gmail_threads,
            build_thread_map,
            gog_json,
            parse_message_record,
            extract_entities,
            extract_domain,
            LINKEDIN_ROLE_RE,
            LINKEDIN_SIMPLE_ROLE_RE,
            INDEED_ROLE_RE,
            THOMSON_REUTERS_RE,
            APPLICATION_RE,
            normalize_text,
            GENERIC_COMPANY_BLOCKLIST,
            classify_signal,
            CLASSIFICATION_RULES,
            NEWSLETTER_NOISE_PATTERNS,
            is_job_related,
            JOB_HINTS,
            ensure_recruiter,
            normalize_company,
            next_id,
            find_best_job_match,
            ensure_signal,
            update_row,
            sheets_update,
            make_job_row,
            infer_status,
            action_classification_for_signal,
            update_job_row_for_signal,
            ensure_action,
            append_rows,
            write_csv,
            sheets_append,
            iso,
            NO_JOB_CREATE_SOURCES,
        )
        actions_normalized = normalize_existing_actions(run_at)
        gmail_report['actions_updated'] = gmail_report.get('actions_updated', 0) + actions_normalized
        gmail_report['signals_cleaned'] = cleaned_signals
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
        update_scheduler_state('complete', run_log['summary'], run_at, scheduled_for=scheduled_for, trigger_mode=sched['triggerMode'], missed_slots=sched['missedSlots'])
        report_path = write_run_report(run_log, REPORTS_DIR)
        run_log['reportPath'] = report_path
        append_log(run_log)
        print(json.dumps(run_log, indent=2))
    except Exception as e:
        run_log['status'] = 'failed'
        run_log['summary'] = str(e)
        run_log['errors'].append(str(e))
        run_log['assessment'] = 'Chain failed. Inspect errors and partial outputs.'
        update_scheduler_state('failed', str(e), run_at, scheduled_for=scheduled_for, trigger_mode=sched['triggerMode'], missed_slots=sched['missedSlots'])
        report_path = write_run_report(run_log, REPORTS_DIR)
        run_log['reportPath'] = report_path
        append_log(run_log)
        print(json.dumps(run_log, indent=2))
        raise


if __name__ == '__main__':
    run_chain()
