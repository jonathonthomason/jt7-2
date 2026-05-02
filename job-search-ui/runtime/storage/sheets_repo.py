import json
import subprocess


REVIEW_QUEUE_HEADER = [[
    'review_id',
    'signal_id',
    'timestamp',
    'source',
    'signal_type',
    'extracted_company',
    'extracted_role',
    'extracted_recruiter',
    'proposed_action',
    'proposed_job_update',
    'confidence',
    'reason_for_review',
    'status',
    'resolution_notes',
]]


def local_reviewqueue_rows(mirror_dir):
    json_path = mirror_dir / 'ReviewQueue.json'
    if not json_path.exists():
        return [], []
    data = json.loads(json_path.read_text())
    if not data:
        return [], []
    header = data[0]
    rows = []
    for idx, row in enumerate(data[1:], start=2):
        padded = row + [''] * (len(header) - len(row))
        rows.append({'row_index': idx, 'values': dict(zip(header, padded))})
    return header, rows


def _is_missing_reviewqueue_range_error(error):
    detail = str(error)
    return 'Unable to parse range: ReviewQueue!' in detail or 'Unable to parse range: \'ReviewQueue\'!' in detail


def rows_to_dicts(tab, sheets_get, mirror_dir):
    try:
        data = sheets_get(f'{tab}!A1:Z1000').get('values', [])
    except (RuntimeError, subprocess.CalledProcessError) as error:
        if tab == 'ReviewQueue' and _is_missing_reviewqueue_range_error(error):
            return local_reviewqueue_rows(mirror_dir)
        raise
    if not data:
        if tab == 'ReviewQueue':
            return local_reviewqueue_rows(mirror_dir)
        return [], []
    header = data[0]
    rows = []
    for idx, row in enumerate(data[1:], start=2):
        padded = row + [''] * (len(header) - len(row))
        rows.append({'row_index': idx, 'values': dict(zip(header, padded))})
    return header, rows


def append_rows(tab, rows, mirror_dir, write_csv, sheets_append):
    if not rows:
        return
    if tab == 'ReviewQueue':
        csv_path = mirror_dir / 'ReviewQueue.csv'
        json_path = mirror_dir / 'ReviewQueue.json'
        existing = []
        if json_path.exists():
            existing = json.loads(json_path.read_text())
        if not existing:
            existing = REVIEW_QUEUE_HEADER.copy()
        existing.extend(rows)
        write_csv(csv_path, existing)
        json_path.write_text(json.dumps(existing, indent=2))
        return
    sheets_append(f'{tab}!A:Z', rows)


def update_row(tab, row_index, row_values, sheets_update):
    end_col = chr(ord('A') + len(row_values) - 1)
    sheets_update(f'{tab}!A{row_index}:{end_col}{row_index}', [row_values])
