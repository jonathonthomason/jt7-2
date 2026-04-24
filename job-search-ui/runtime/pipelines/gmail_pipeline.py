def gmail_query_from_last_run(last_run_at, now_local, default_gmail_lookback_days, job_label_query):
    delta = now_local() - last_run_at
    days = max(1, min(30, delta.days + 1))
    return f"{job_label_query} newer_than:{days}d"


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


def score_job_match(parsed, job_row, normalize_company, normalize_text):
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
