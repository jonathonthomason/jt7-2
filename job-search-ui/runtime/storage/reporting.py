import json


def write_run_report(run_log, reports_dir):
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = run_log['runTimestamp'].replace(':', '-').replace('+', '_plus_')
    path = reports_dir / f'jt7_run_{stamp}.json'
    path.write_text(json.dumps(run_log, indent=2))
    return str(path)
