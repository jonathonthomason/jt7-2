def ensure_recruiter(parsed, recruiters_rows, recruiter_ids, new_recruiters, normalize_company, normalize_text, next_id):
    email = parsed['sender_email'].lower()
    domain = parsed['sender_domain']
    company = parsed['company']
    for row in recruiters_rows:
        values = row['values']
        if email and values.get('email', '').lower() == email:
            return values.get('recruiter_id', ''), False
        if company and normalize_company(values.get('company_name', '')) == normalize_company(company):
            return values.get('recruiter_id', ''), False
        if domain and domain and domain in normalize_text(values.get('profile_link', '') + ' ' + values.get('email', '')):
            return values.get('recruiter_id', ''), False

    if not (email or company):
        return '', False

    recruiter_id = next_id('recruiter_', recruiter_ids + [r[0] for r in new_recruiters])
    new_recruiters.append([
        recruiter_id,
        parsed['sender_name'],
        company,
        '',
        'Prospect',
        '',
        parsed['sender_email'],
        '',
    ])
    return recruiter_id, True
