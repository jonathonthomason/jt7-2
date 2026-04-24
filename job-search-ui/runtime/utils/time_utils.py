from datetime import datetime, timedelta


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


def next_global_run(current, run_times):
    candidates = [next_run_after(current, t) for t in run_times]
    return min(candidates)
