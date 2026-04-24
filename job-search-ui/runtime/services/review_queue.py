import json

from runtime.domain.actions import proposed_action_instruction


def confidence_bucket(confidence):
    if confidence >= 0.8:
        return 'high'
    if confidence >= 0.5:
        return 'medium'
    return 'low'


def should_block_job_creation(parsed, classification, normalize_text, no_job_create_sources, generic_company_blocklist):
    source_norm = normalize_text(parsed.get('company', '') or parsed.get('sender_name', '') or parsed.get('source', ''))
    role_norm = normalize_text(parsed.get('role', ''))
    company_norm = normalize_text(parsed.get('company', ''))
    signal_type = classification.get('signal_type', '')

    if signal_type == 'ignore_noise':
        return True, 'ignore_noise'
    if source_norm in no_job_create_sources:
        return True, f'blocked_source:{source_norm}'
    if not role_norm:
        return True, 'missing_role'
    if not company_norm:
        return True, 'missing_company'
    if company_norm in generic_company_blocklist:
        return True, f'generic_company:{company_norm}'
    if signal_type in {'unknown_review_needed'}:
        return True, f'weak_signal_type:{signal_type}'
    return False, ''


def reason_for_review(parsed, classification, match_score):
    reasons = []
    if not parsed.get('company'):
        reasons.append('missing_company')
    if not parsed.get('role'):
        reasons.append('missing_role')
    if match_score < 0.6:
        reasons.append('weak_job_match')
    reasons.append(f"signal_type:{classification['signal_type']}")
    return ', '.join(reasons)


def ensure_review_queue_entry(parsed, classification, signal_id, linked_job_id, review_rows, review_ids, new_reviews, recruiter_id, match_score, next_id, action_required_signal_types, infer_status, iso_now):
    for row in review_rows:
        if row['values'].get('signal_id', '') == signal_id:
            return False, row['values'].get('review_id', '')
    review_id = next_id('review_', review_ids + [r[0] for r in new_reviews])
    proposed_action = proposed_action_instruction(classification['signal_type']) if classification['signal_type'] in action_required_signal_types else ''
    proposed_job_update = json.dumps({
        'linked_job_id': linked_job_id,
        'proposed_status': infer_status(classification['signal_type']),
        'company': parsed.get('company', ''),
        'role': parsed.get('role', ''),
    })
    new_reviews.append([
        review_id,
        signal_id,
        iso_now(),
        parsed.get('source', 'gmail'),
        classification['signal_type'],
        parsed.get('company', ''),
        parsed.get('role', ''),
        recruiter_id or parsed.get('sender_email', ''),
        proposed_action,
        proposed_job_update,
        str(classification['confidence']),
        reason_for_review(parsed, classification, match_score),
        'pending',
        '',
    ])
    return True, review_id
