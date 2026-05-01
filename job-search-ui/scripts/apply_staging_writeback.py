#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import subprocess
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import sys
sys.path.append('/Users/jtemp/.openclaw/workspace/job-search-ui')

from runtime.services.staging_writeback import JOB_COLUMNS, plan_staging_writeback
from runtime.storage.local_mirror import local_mirror_sync
from runtime.storage.sheets_repo import update_row
from runtime.utils.file_utils import write_csv

ROOT = Path('/Users/jtemp/.openclaw/workspace/job-search-ui')
RUNTIME = ROOT / 'runtime'
PREVIEW_JSON = RUNTIME / 'direct_board_import_preview.json'
MIRROR_DIR = ROOT / 'data_mirror'
REPORTS_DIR = RUNTIME / 'reports'
SHEET_ID = '1acPkcUQFDIVNY0sgMo7ZsVzEnBKIbjU2veEjDFRu0Ks'
TZ = ZoneInfo('America/Chicago')
GOG_BIN = '/opt/homebrew/bin/gog'
GOG_ACCOUNT = 'jonathon.thomason@gmail.com'
GOG_BASE_ARGS = ['--json', '--no-input', '--account', GOG_ACCOUNT]


def now_local() -> datetime:
    return datetime.now(TZ)


def iso(dt: datetime) -> str:
    return dt.isoformat()


def gog_json(args: list[str]) -> dict:
    cmd = [GOG_BIN, *args]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        stderr = (e.stderr or '').strip()
        stdout = (e.stdout or '').strip()
        detail = stderr or stdout or str(e)
        raise RuntimeError(f'gog command failed: {cmd} :: {detail}') from e
    return json.loads(result.stdout)


def sheets_get(range_name: str) -> dict:
    return gog_json(['sheets', 'get', SHEET_ID, range_name, *GOG_BASE_ARGS])


def sheets_append(range_name: str, values: list[list[str]]) -> None:
    cmd = [
        GOG_BIN,
        'sheets', 'append', SHEET_ID, range_name,
        '--values-json', json.dumps(values),
        '--insert', 'INSERT_ROWS',
        '--no-input', '--account', GOG_ACCOUNT,
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        stderr = (e.stderr or '').strip()
        stdout = (e.stdout or '').strip()
        detail = stderr or stdout or str(e)
        raise RuntimeError(f'gog append failed: {cmd} :: {detail}') from e


def sheets_update(range_name: str, values: list[list[str]]) -> None:
    cmd = [
        GOG_BIN,
        'sheets', 'update', SHEET_ID, range_name,
        '--values-json', json.dumps(values),
        '--input', 'USER_ENTERED',
        '--no-input', '--account', GOG_ACCOUNT,
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        stderr = (e.stderr or '').strip()
        stdout = (e.stdout or '').strip()
        detail = stderr or stdout or str(e)
        raise RuntimeError(f'gog update failed: {cmd} :: {detail}') from e


def load_jobs_live() -> tuple[list[str], list[dict[str, str]]]:
    rows = sheets_get('Jobs!A1:Z1000').get('values', [])
    if not rows:
        return [], []
    header = rows[0]
    out = []
    for idx, row in enumerate(rows[1:], start=2):
        padded = row + [''] * (len(header) - len(row))
        values = dict(zip(header, padded))
        values['row_index'] = str(idx)
        out.append(values)
    return header, out


def load_staged_rows() -> list[dict[str, str]]:
    preview = json.loads(PREVIEW_JSON.read_text())
    staged = []
    for idx, row in enumerate(preview.get('proposed_rows', []), start=1):
        values = dict(zip(JOB_COLUMNS, row + [''] * (len(JOB_COLUMNS) - len(row))))
        values['provenance'] = values.get('notes', '')
        values['notes'] = ''
        values['staged_id'] = f'staged_{values.get("job_id", idx)}'
        values['preview_index'] = str(idx)
        staged.append(values)
    return staged


def select_staged(staged_rows: list[dict[str, str]], index: int | None, staged_id: str | None) -> dict[str, str]:
    if staged_id:
        for row in staged_rows:
            if row.get('staged_id') == staged_id:
                return row
        raise SystemExit(f'No staged item found for id: {staged_id}')
    if index is None:
        raise SystemExit('Provide --index or --staged-id')
    if index < 1 or index > len(staged_rows):
        raise SystemExit(f'Index out of range: {index} (1-{len(staged_rows)})')
    return staged_rows[index - 1]


def row_values_from_dict(header: list[str], values: dict[str, str]) -> list[str]:
    return [values.get(column, '') for column in header]


def write_report(payload: dict) -> str:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = payload['executedAt'].replace(':', '-').replace('/', '-')
    path = REPORTS_DIR / f'staging_writeback_{stamp}.json'
    path.write_text(json.dumps(payload, indent=2))
    return str(path)


def refresh_jobs_mirror() -> dict:
    return local_mirror_sync(['Jobs'], MIRROR_DIR, lambda: {
        'Jobs': {
            'csv_exists': (MIRROR_DIR / 'Jobs.csv').exists(),
            'json_exists': (MIRROR_DIR / 'Jobs.json').exists(),
            'csv_size': (MIRROR_DIR / 'Jobs.csv').stat().st_size if (MIRROR_DIR / 'Jobs.csv').exists() else 0,
            'json_size': (MIRROR_DIR / 'Jobs.json').stat().st_size if (MIRROR_DIR / 'Jobs.json').exists() else 0,
        }
    }, sheets_get, write_csv)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Plan or apply a narrow staging→canonical Jobs writeback.')
    parser.add_argument('--index', type=int, help='1-based index into runtime/direct_board_import_preview.json proposed_rows')
    parser.add_argument('--staged-id', help='Explicit staged id (e.g. staged_job_057)')
    parser.add_argument('--apply', action='store_true', help='Apply the planned create/merge to live Google Sheets Jobs')
    parser.add_argument('--json', action='store_true', help='Emit JSON only')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    executed_at = now_local()
    jobs_header, jobs = load_jobs_live()
    staged_rows = load_staged_rows()
    staged = select_staged(staged_rows, args.index, args.staged_id)
    plan = plan_staging_writeback(staged, jobs, now_iso=iso(executed_at))

    payload = {
        'executedAt': iso(executed_at),
        'sheetId': SHEET_ID,
        'staged': {
            'staged_id': staged.get('staged_id', ''),
            'preview_index': staged.get('preview_index', ''),
            'company': staged.get('company', ''),
            'role': staged.get('role', ''),
            'location': staged.get('location', ''),
            'job_posting_link': staged.get('job_posting_link', ''),
            'source': staged.get('source', ''),
        },
        'plan': asdict(plan),
        'mode': 'apply' if args.apply else 'plan',
        'result': 'planned',
        'mirror': None,
    }

    if args.apply:
        if plan.action == 'create' and plan.create_row:
            sheets_append('Jobs!A:Z', [plan.create_row])
            payload['result'] = 'created'
            payload['created_job_id'] = plan.create_row[0]
        elif plan.action == 'merge' and plan.update_values and plan.matched_job_id:
            match = next((job for job in jobs if job.get('job_id') == plan.matched_job_id), None)
            if not match:
                raise SystemExit(f'Matched job not found in live Jobs: {plan.matched_job_id}')
            row_index = int(match['row_index'])
            row_values = row_values_from_dict(jobs_header, plan.update_values)
            update_row('Jobs', row_index, row_values, sheets_update)
            payload['result'] = 'merged'
            payload['merged_job_id'] = plan.matched_job_id
        elif plan.action in {'hold', 'reject'}:
            payload['result'] = plan.action
        else:
            raise SystemExit(f'Unsupported apply plan: {plan.action}')

        payload['mirror'] = refresh_jobs_mirror()

    payload['reportPath'] = write_report(payload)

    if args.json:
        print(json.dumps(payload, indent=2))
        return

    summary = {
        'staged_id': payload['staged']['staged_id'],
        'company': payload['staged']['company'],
        'role': payload['staged']['role'],
        'action': plan.action,
        'reason': plan.reason,
        'result': payload['result'],
        'reportPath': payload['reportPath'],
    }
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
