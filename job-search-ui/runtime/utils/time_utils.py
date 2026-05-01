from datetime import datetime, timedelta


def parse_dt(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except Exception:
        return None


def scheduled_time_on(day_like, hhmm):
    hour, minute = map(int, hhmm.split(':'))
    return day_like.replace(hour=hour, minute=minute, second=0, microsecond=0)


def next_run_after(current, hhmm):
    candidate = scheduled_time_on(current, hhmm)
    if candidate <= current:
        candidate = candidate + timedelta(days=1)
    return candidate


def next_global_run(current, run_times):
    candidates = [next_run_after(current, t) for t in run_times]
    return min(candidates)


def missed_run_slots(last_run_at, current, run_times):
    if not last_run_at or not run_times:
        return []

    slots = []
    day_cursor = last_run_at.replace(hour=0, minute=0, second=0, microsecond=0)
    end_day = current.replace(hour=0, minute=0, second=0, microsecond=0)

    while day_cursor <= end_day:
        for hhmm in sorted(run_times):
            candidate = scheduled_time_on(day_cursor, hhmm)
            if last_run_at < candidate <= current:
                slots.append(candidate)
        day_cursor = day_cursor + timedelta(days=1)

    return slots
