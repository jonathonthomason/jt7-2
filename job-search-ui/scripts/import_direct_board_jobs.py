#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

sys.path.append('/Users/jtemp/.openclaw/workspace/job-search-ui')

from runtime.adapters.job_boards import load_job_board_targets, scan_builtin_targets, scan_greenhouse_targets, scan_indeed_targets, scan_linkedin_targets
from runtime.utils.id_utils import next_id
from runtime.utils.file_utils import write_csv

ROOT = Path('/Users/jtemp/.openclaw/workspace/job-search-ui')
MIRROR_DIR = ROOT / 'data_mirror'
JOBS_JSON = MIRROR_DIR / 'Jobs.json'
JOBS_CSV = MIRROR_DIR / 'Jobs.csv'
OUTPUT_JSON = ROOT / 'runtime' / 'direct_board_import_preview.json'
TARGETS = ROOT / 'runtime' / 'job_board_targets.json'


def load_rows(path: Path):
    return json.loads(path.read_text()) if path.exists() else []


def row_dicts(rows):
    header = rows[0]
    return header, [dict(zip(header, row + [''] * (len(header) - len(row)))) for row in rows[1:]]


def norm(value: str):
    return ' '.join((value or '').strip().lower().split())


def is_duplicate(match: dict, jobs: list[dict]):
    posting = norm(match.get('job_posting_link', ''))
    company = norm(match.get('company', ''))
    role = norm(match.get('role', ''))
    location = norm(match.get('location', ''))
    for job in jobs:
        job_posting = norm(job.get('job_posting_link', ''))
        if posting and job_posting and posting == job_posting:
            return True, 'job_posting_link'
        if company and role and company == norm(job.get('company', '')) and role == norm(job.get('role', '')):
            existing_loc = norm(job.get('location', ''))
            if not location or not existing_loc or location == existing_loc:
                return True, 'company_role_location'
    return False, ''


def make_job_row(job_id: str, match: dict):
    source = f"{match.get('source', 'board')}_direct"
    return [
        job_id,
        match.get('company', ''),
        match.get('role', ''),
        match.get('location', ''),
        'Cold',
        '',
        '',
        'Review opportunity and decide whether to apply',
        '',
        '',
        match.get('job_posting_link', ''),
        '',
        source,
        f"Imported from direct board scan ({match.get('source','board')}) | board_token:{match.get('board_token','')} | job_board_id:{match.get('job_board_id','')}",
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply-local', action='store_true', help='append proposed rows into local Jobs mirror')
    parser.add_argument('--source', choices=['all', 'linkedin', 'greenhouse', 'builtin'], default='linkedin')
    args = parser.parse_args()

    config = load_job_board_targets(TARGETS)
    builtin_matches, _, builtin_warnings = scan_builtin_targets(config)
    linkedin_matches, _, linkedin_warnings = scan_linkedin_targets(config)
    indeed_matches, _, indeed_warnings = scan_indeed_targets(config)
    greenhouse_matches, _, greenhouse_warnings = scan_greenhouse_targets(config)
    all_matches = builtin_matches + linkedin_matches + indeed_matches + greenhouse_matches
    warnings = builtin_warnings + linkedin_warnings + indeed_warnings + greenhouse_warnings

    matches = all_matches if args.source == 'all' else [row for row in all_matches if row.get('source') == args.source]

    rows = load_rows(JOBS_JSON)
    header, existing_jobs = row_dicts(rows)
    existing_ids = [job.get('job_id', '') for job in existing_jobs]

    proposed = []
    skipped = []
    for match in matches:
        duplicate, reason = is_duplicate(match, existing_jobs + [dict(zip(header, row)) for row in proposed])
        if duplicate:
            skipped.append({'company': match.get('company', ''), 'role': match.get('role', ''), 'reason': reason})
            continue
        job_id = next_id('job_', existing_ids + [row[0] for row in proposed])
        proposed.append(make_job_row(job_id, match))

    preview = {
        'source_filter': args.source,
        'matches_considered': len(matches),
        'jobs_proposed': len(proposed),
        'jobs_skipped_as_duplicates': len(skipped),
        'proposed_rows': proposed,
        'skipped_examples': skipped[:25],
        'warnings': warnings,
    }
    OUTPUT_JSON.write_text(json.dumps(preview, indent=2))

    if args.apply_local and proposed:
        updated = rows + proposed
        write_csv(JOBS_CSV, updated)
        JOBS_JSON.write_text(json.dumps(updated, indent=2))

    print(json.dumps(preview, indent=2))


if __name__ == '__main__':
    main()
