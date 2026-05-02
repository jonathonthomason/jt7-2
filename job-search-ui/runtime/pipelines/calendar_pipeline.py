def calendar_scan_and_update(run_at, gog_json, rows_to_dicts, ensure_action, action_ids, actions_rows, new_actions, append_rows, mirror_dir, write_csv, sheets_append, iso, timedelta, normalize_company, normalize_text, update_row):
    from_iso = iso(run_at - timedelta(days=2))
    to_iso = iso(run_at + timedelta(days=14))
    events = gog_json(['calendar', 'events', 'primary', '--from', from_iso, '--to', to_iso, '--json']).get('events', [])
    state_jobs_header, jobs_rows = rows_to_dicts('Jobs')
    matched_jobs = 0
    updates_written = 0
    interview_events_found = 0
    for event in events:
        summary = event.get('summary', '')
        location = event.get('location', '')
        text = f"{summary} {location}".lower()
        if 'interview' not in text and 'recruit' not in text and 'screen' not in text and 'hiring' not in text:
            continue
        interview_events_found += 1
        best = None
        best_score = 0.0
        for row in jobs_rows:
            job = row['values']
            company = job.get('company', '')
            role = job.get('role', '')
            score = 0.0
            if company and normalize_company(company) in normalize_company(text):
                score += 0.55
            if role and normalize_text(role) in normalize_text(text):
                score += 0.35
            if score > best_score:
                best_score = score
                best = row
        if best and best_score >= 0.45:
            matched_jobs += 1
            updated = best['values'].copy()
            updated['status'] = 'Interviewing'
            updated['interview_datetime'] = event.get('start', {}).get('dateTime', '') or updated.get('interview_datetime', '')
            updated['next_step'] = 'Prepare for scheduled interview'
            notes = updated.get('notes', '')
            addition = f" | calendar_event:{event.get('id','')}"
            if addition not in notes:
                updated['notes'] = (notes + addition).strip(' |')
            row_values = [updated.get(col, '') for col in state_jobs_header]
            update_row('Jobs', best['row_index'], row_values)
            best['values'] = updated
            updates_written += 1
            created_action, _ = ensure_action(best['values'].get('job_id', ''), best['values'].get('company', ''), {'signal_type': 'interview_scheduling'}, action_ids, actions_rows, new_actions, run_at)
            if created_action:
                action_ids.append(new_actions[-1][0])
    append_rows('Actions', new_actions, mirror_dir, write_csv, sheets_append)
    return {
        'source': 'calendar',
        'status': 'complete',
        'events_scanned': len(events),
        'interview_events_found': interview_events_found,
        'matched_jobs': matched_jobs,
        'updates_written': updates_written,
        'actions_created': len(new_actions),
        'warnings': [],
    }
