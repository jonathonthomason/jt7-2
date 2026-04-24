import json
from pathlib import Path


def load_json_rows(path: str):
    p = Path(path)
    if not p.exists():
        return []
    return json.loads(p.read_text())


def local_mirror_sync(tabs, mirror_dir, mirror_snapshot, sheets_get, write_csv):
    before = mirror_snapshot()
    mirrored = []
    changed_csv = []
    changed_json = []
    unchanged = []
    tracker_tabs = {}
    for tab in tabs:
        if tab == 'ReviewQueue':
            rows = json.loads((mirror_dir / 'ReviewQueue.json').read_text()) if (mirror_dir / 'ReviewQueue.json').exists() else []
        else:
            data = sheets_get(f'{tab}!A1:Z1000')
            rows = data.get('values', [])
        csv_path = mirror_dir / f'{tab}.csv'
        json_path = mirror_dir / f'{tab}.json'
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
