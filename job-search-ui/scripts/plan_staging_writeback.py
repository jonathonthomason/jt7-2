#!/usr/bin/env python3
import json
from pathlib import Path

import sys
sys.path.append('/Users/jtemp/.openclaw/workspace/job-search-ui')

from runtime.services.staging_writeback import JOB_COLUMNS, plan_staging_writeback

ROOT = Path('/Users/jtemp/.openclaw/workspace/job-search-ui')
PREVIEW_JSON = ROOT / 'runtime' / 'direct_board_import_preview.json'
JOBS_JSON = ROOT / 'data_mirror' / 'Jobs.json'


def load_jobs():
    rows = json.loads(JOBS_JSON.read_text())
    header = rows[0]
    return [dict(zip(header, row + [''] * (len(header) - len(row)))) for row in rows[1:]]


def load_staged():
    preview = json.loads(PREVIEW_JSON.read_text())
    rows = preview.get('proposed_rows', [])
    staged = []
    for row in rows:
        values = dict(zip(JOB_COLUMNS, row + [''] * (len(JOB_COLUMNS) - len(row))))
        values['provenance'] = values.get('notes', '')
        staged.append(values)
    return staged


def main():
    jobs = load_jobs()
    staged = load_staged()
    plans = []
    simulated_jobs = list(jobs)
    for item in staged[:25]:
        plan = plan_staging_writeback(item, simulated_jobs)
        plans.append({
            'company': item.get('company', ''),
            'role': item.get('role', ''),
            'location': item.get('location', ''),
            'action': plan.action,
            'reason': plan.reason,
            'matched_job_id': plan.matched_job_id,
            'create_job_id': plan.create_row[0] if plan.create_row else '',
        })
        if plan.create_row:
            simulated_jobs.append(dict(zip(JOB_COLUMNS, plan.create_row)))
        elif plan.update_values:
            simulated_jobs = [plan.update_values if row.get('job_id', '') == plan.matched_job_id else row for row in simulated_jobs]
    print(json.dumps({'sample_size': len(plans), 'plans': plans}, indent=2))


if __name__ == '__main__':
    main()
