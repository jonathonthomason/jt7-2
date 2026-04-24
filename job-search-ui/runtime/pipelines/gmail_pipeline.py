from runtime.domain.actions import ACTION_REQUIRED_SIGNAL_TYPES
from runtime.services.review_queue import confidence_bucket, ensure_review_queue_entry, should_block_job_creation


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


def gmail_scan_and_update(
    run_at,
    fetch_runtime_state,
    rows_to_dicts,
    sheets_get,
    mirror_dir,
    get_last_run_at,
    now_local,
    default_gmail_lookback_days,
    job_label_query,
    collect_gmail_messages,
    collect_gmail_threads,
    build_thread_map,
    gog_json,
    parse_message_record,
    extract_entities,
    extract_domain,
    linkedin_role_re,
    linkedin_simple_role_re,
    indeed_role_re,
    thomson_reuters_re,
    application_re,
    normalize_text,
    generic_company_blocklist,
    classify_signal,
    classification_rules,
    newsletter_noise_patterns,
    is_job_related,
    job_hints,
    ensure_recruiter,
    normalize_company,
    next_id,
    find_best_job_match,
    ensure_signal,
    update_row,
    sheets_update,
    make_job_row,
    infer_status,
    update_job_row_for_signal,
    ensure_action,
    append_rows,
    write_csv,
    sheets_append,
    iso,
):
    state = fetch_runtime_state(lambda tab: rows_to_dicts(tab, sheets_get, mirror_dir))
    jobs_rows = state['jobs_rows']
    recruiters_rows = state['recruiters_rows']
    signals_rows = state['signals_rows']
    actions_rows = state['actions_rows']
    review_rows = state['review_rows']
    last_run_at = get_last_run_at()
    query = gmail_query_from_last_run(last_run_at, now_local, default_gmail_lookback_days, job_label_query)
    messages = collect_gmail_messages(query, gog_json)
    threads = collect_gmail_threads(query, gog_json)
    thread_map = build_thread_map(threads, messages)

    job_ids = [r['values'].get('job_id', '') for r in jobs_rows]
    recruiter_ids = [r['values'].get('recruiter_id', '') for r in recruiters_rows]
    signal_ids = [r['values'].get('signal_id', '') for r in signals_rows]
    action_ids = [r['values'].get('action_id', '') for r in actions_rows]
    review_ids = [r['values'].get('review_id', '') for r in review_rows]

    new_jobs = []
    new_recruiters = []
    new_signals = []
    new_actions = []
    new_reviews = []
    parsed_signals = []
    job_related_threads = 0
    review_needed_count = 0
    recruiters_created = 0
    jobs_created = 0
    jobs_updated = 0
    signals_created = 0
    signals_updated = 0
    actions_created = 0
    review_needed_created = 0
    signals_marked_review_required = 0
    blocked_job_creations = 0
    orphan_actions = 0
    signal_to_job_update = []
    signal_to_action = []
    signals_by_confidence = {'high': 0, 'medium': 0, 'low': 0}

    for thread_id, bundle in thread_map.items():
        thread_labels = bundle.get('thread', {}).get('labels', []) or []
        thread_relevant = False
        for message in bundle.get('messages', []):
            parsed = parse_message_record(
                message,
                thread_labels,
                lambda subject, sender, snippet: extract_entities(
                    subject,
                    sender,
                    snippet,
                    extract_domain,
                    linkedin_role_re,
                    linkedin_simple_role_re,
                    indeed_role_re,
                    thomson_reuters_re,
                    application_re,
                    normalize_text,
                    generic_company_blocklist,
                ),
                lambda subject, sender, labels, body: classify_signal(
                    subject,
                    sender,
                    labels,
                    body,
                    classification_rules,
                    newsletter_noise_patterns,
                ),
            )
            if not is_job_related(parsed, newsletter_noise_patterns, job_hints, normalize_text, generic_company_blocklist):
                continue
            thread_relevant = True
            classification = parsed['classification']
            bucket = confidence_bucket(classification['confidence'])
            signals_by_confidence[bucket] += 1
            if classification['review_needed'] or bucket == 'medium':
                review_needed_count += 1

            recruiter_id, recruiter_created = ensure_recruiter(
                parsed,
                recruiters_rows,
                recruiter_ids,
                new_recruiters,
                normalize_company,
                normalize_text,
                next_id,
            )
            if recruiter_created:
                recruiter_ids.append(recruiter_id)
                recruiters_created += 1

            best_job, match_score = find_best_job_match(
                parsed,
                jobs_rows,
                lambda p, row: score_job_match(p, row, normalize_company, normalize_text),
            )
            linked_job_id = ''

            if best_job and match_score >= 0.6:
                linked_job_id = best_job['values'].get('job_id', '')
            else:
                parsed['company'] = choose_company_from_context(
                    parsed,
                    {normalize_company(r['values'].get('company', '')): r for r in jobs_rows},
                ) or parsed['company']
                company_jobs = [
                    r for r in jobs_rows
                    if normalize_company(r['values'].get('company', '')) == normalize_company(parsed['company'])
                ]
                parsed['role'] = choose_role_from_context(parsed, company_jobs) or parsed['role']

            blocked_job_create, block_reason = should_block_job_creation(
                parsed,
                classification,
                normalize_text,
                no_job_create_sources=[],
                generic_company_blocklist=generic_company_blocklist,
            )
            if blocked_job_create:
                classification['no_job_create'] = True
                classification['review_needed'] = True
                if classification['confidence'] > 0.5:
                    classification['confidence'] = 0.5
                signals_marked_review_required += 1

            signal_created, signal_id, signal_persisted = ensure_signal(
                parsed,
                classification,
                linked_job_id,
                signal_ids,
                signals_rows,
                new_signals,
                state['signals_header'],
                lambda tab, row_index, row_values: update_row(tab, row_index, row_values, sheets_update),
                next_id,
            )
            if signal_created:
                signals_created += 1
            else:
                signals_updated += 1
            if signal_id and signal_id not in signal_ids:
                signal_ids.append(signal_id)

            create_allowed = bucket == 'high' and not blocked_job_create and bool(parsed['company'] and parsed['role'] and signal_id)
            if signal_id and not linked_job_id and create_allowed:
                new_job = make_job_row(
                    parsed,
                    recruiter_id,
                    next_id('job_', job_ids + [r[0] for r in new_jobs]),
                    classification,
                    infer_status,
                )
                new_job[-1] = f"{new_job[-1]} | signal_id:{signal_id}"
                new_jobs.append(new_job)
                linked_job_id = new_job[0]
                job_ids.append(linked_job_id)
                jobs_created += 1
                new_signals[-1][-1] = linked_job_id
                signal_to_job_update.append({'signal_id': signal_id, 'job_id': linked_job_id, 'mode': 'create'})
            elif signal_id and linked_job_id and bucket == 'high' and classification['auto_update_allowed']:
                updated = update_job_row_for_signal(best_job, parsed, classification, recruiter_id, infer_status)
                notes = updated.get('notes', '')
                addition = f" | signal_id:{signal_id}"
                if addition not in notes:
                    updated['notes'] = (notes + addition).strip(' |')
                row_values = [updated.get(col, '') for col in state['jobs_header']]
                update_row('Jobs', best_job['row_index'], row_values, sheets_update)
                best_job['values'] = updated
                jobs_updated += 1
                if signal_created:
                    new_signals[-1][-1] = linked_job_id
                signal_to_job_update.append({'signal_id': signal_id, 'job_id': linked_job_id, 'mode': 'update'})
            else:
                if blocked_job_create and not linked_job_id:
                    blocked_job_creations += 1
                if bucket == 'medium' or blocked_job_create:
                    created_review, _ = ensure_review_queue_entry(
                        parsed,
                        classification,
                        signal_id,
                        linked_job_id,
                        review_rows,
                        review_ids,
                        new_reviews,
                        recruiter_id,
                        match_score,
                        next_id,
                        ACTION_REQUIRED_SIGNAL_TYPES,
                        infer_status,
                        lambda: iso(now_local()),
                    )
                    if created_review:
                        review_needed_created += 1

            requires_action = classification['signal_type'] in ACTION_REQUIRED_SIGNAL_TYPES and classification['signal_type'] != 'ignore_noise'
            if linked_job_id and signal_id and bucket == 'high' and requires_action:
                created_action, action_id = ensure_action(
                    linked_job_id,
                    parsed['company'],
                    classification,
                    action_ids,
                    actions_rows,
                    new_actions,
                    run_at,
                    signal_id=signal_id,
                )
                if created_action:
                    actions_created += 1
                    signal_to_action.append({'signal_id': signal_id, 'action_id': action_id, 'job_id': linked_job_id})
            elif requires_action and not signal_id:
                orphan_actions += 1
            action_ids = action_ids + [r[0] for r in new_actions if r[0] not in action_ids]
            parsed_signals.append({
                'thread_id': parsed['thread_id'],
                'message_id': parsed['message_id'],
                'company': parsed['company'],
                'role': parsed['role'],
                'signal_type': classification['signal_type'],
                'confidence': classification['confidence'],
                'auto_update_allowed': classification['auto_update_allowed'],
                'review_needed': classification['review_needed'],
                'match_score': round(match_score, 2),
                'linked_job_id': linked_job_id,
            })
        if thread_relevant:
            job_related_threads += 1

    append_rows('Recruiters', new_recruiters, mirror_dir, write_csv, sheets_append)
    append_rows('Jobs', new_jobs, mirror_dir, write_csv, sheets_append)
    append_rows('Signals', new_signals, mirror_dir, write_csv, sheets_append)
    append_rows('Actions', new_actions, mirror_dir, write_csv, sheets_append)
    append_rows('ReviewQueue', new_reviews, mirror_dir, write_csv, sheets_append)

    warnings = []
    signals_persisted = signals_created + signals_updated
    if job_related_threads > 0 and signals_persisted == 0:
        warnings.append('Run incomplete: job-related threads found but zero persisted signals')

    return {
        'source': 'gmail',
        'status': 'failed' if job_related_threads > 0 and signals_persisted == 0 else 'complete',
        'query': query,
        'last_run_at_used': iso(last_run_at),
        'threads_scanned': len(thread_map),
        'messages_scanned': len(messages),
        'job_related_threads_found': job_related_threads,
        'parsed_candidate_signals': parsed_signals[:25],
        'labels_changed': 0,
        'recruiters_matched_or_created': recruiters_created,
        'jobs_matched_created_or_updated': jobs_created + jobs_updated,
        'jobs_created': jobs_created,
        'jobs_updated': jobs_updated,
        'signals_created': signals_created,
        'signals_updated': signals_updated,
        'signals_persisted': signals_persisted,
        'signals_marked_review_required': signals_marked_review_required,
        'actions_created': actions_created,
        'review_needed_count': review_needed_count,
        'review_needed_created': review_needed_created,
        'blocked_job_creations': blocked_job_creations,
        'orphan_actions': orphan_actions,
        'review_queue_pending_count': len([r for r in review_rows if r['values'].get('status', '') == 'pending']) + review_needed_created,
        'signals_by_confidence': signals_by_confidence,
        'signal_to_job_update': signal_to_job_update,
        'signal_to_action': signal_to_action,
        'warnings': warnings,
    }
