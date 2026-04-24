import re
from email.utils import parseaddr


def classify_signal(subject, sender, labels, body, classification_rules, newsletter_noise_patterns):
    haystack = ' '.join([subject or '', sender or '', body or '', ' '.join(labels or [])]).lower()
    signal_type = 'unknown_review_needed'
    confidence = 0.35
    auto_update_allowed = False
    review_needed = True

    if 'unsubscribe' in haystack and 'job' not in haystack and 'recruit' not in haystack:
        return {
            'signal_type': 'ignore_noise',
            'summary': subject[:160],
            'confidence': 0.95,
            'auto_update_allowed': False,
            'review_needed': False,
        }

    if any(re.search(pattern, haystack, re.IGNORECASE) for pattern in newsletter_noise_patterns):
        return {
            'signal_type': 'ignore_noise',
            'summary': subject[:160],
            'confidence': 0.94,
            'auto_update_allowed': False,
            'review_needed': False,
        }

    if 'invitations@linkedin.com' in (sender or '').lower() and 'connect' in haystack:
        return {
            'signal_type': 'ignore_noise',
            'summary': subject[:160],
            'confidence': 0.92,
            'auto_update_allowed': False,
            'review_needed': False,
        }

    for candidate, patterns in classification_rules:
        if any(re.search(pattern, haystack, re.IGNORECASE) for pattern in patterns):
            signal_type = candidate
            break

    if signal_type in {'application_confirmation', 'interview_scheduling', 'reschedule', 'cancellation', 'rejection'}:
        confidence = 0.88
        auto_update_allowed = True
        review_needed = False
    elif signal_type in {'recruiter_outreach', 'hiring_manager_communication', 'follow_up_opportunity'}:
        confidence = 0.76
        auto_update_allowed = True
        review_needed = False
    elif signal_type == 'job_alert':
        confidence = 0.81
        auto_update_allowed = True
        review_needed = False
    elif signal_type == 'ignore_noise':
        confidence = 0.95
        auto_update_allowed = False
        review_needed = False

    return {
        'signal_type': signal_type,
        'summary': subject[:160],
        'confidence': confidence,
        'auto_update_allowed': auto_update_allowed,
        'review_needed': review_needed,
    }


def extract_entities(subject, sender, snippet, extract_domain, linkedin_role_re, linkedin_simple_role_re, indeed_role_re, thomson_reuters_re, application_re, normalize_text, generic_company_blocklist):
    company = ''
    role = ''
    source = 'gmail'
    sender_name, sender_email = parseaddr(sender or '')
    domain = extract_domain(sender)

    linkedin = linkedin_role_re.search(subject or '')
    linkedin_simple = linkedin_simple_role_re.search(subject or '')
    indeed = indeed_role_re.search(subject or '')
    thomson = thomson_reuters_re.search(subject or '')
    app = application_re.search(subject or '')

    if linkedin:
        company = linkedin.group('company').strip()
        role = linkedin.group('role').strip(' -')
        source = 'linkedin_email'
    elif linkedin_simple and 'linkedin' in (sender_email or '').lower():
        company = linkedin_simple.group('company').strip()
        role = linkedin_simple.group('role').strip()
        source = 'linkedin_email'
    elif indeed:
        company = indeed.group('company').strip()
        role = indeed.group('role').strip()
        source = 'indeed_email'
    elif thomson:
        company = 'Thomson Reuters'
        role = thomson.group(1).strip()
        source = 'gmail'
    elif app:
        role = app.group('role').strip(' .')

    normalized_sender = (sender_name or '').strip()
    if not company and normalized_sender:
        cleaned = normalized_sender
        lowered = cleaned.lower()
        if 'american airlines talent acquisition' in lowered:
            company = 'American Airlines'
        elif 'thomson reuters' in (subject or '').lower() or 'thomson reuters' in lowered:
            company = 'Thomson Reuters'
        elif 'talent acquisition' in lowered or 'recruiter' in lowered or 'talent partner' in lowered:
            company = cleaned
        elif lowered in {'linkedin job alerts', 'linkedin', 'indeed', 'mail', 'linkedin news'}:
            company = ''

    if not company and domain and domain not in {'gmail.com', 'googlemail.com', 'linkedin.com', 'indeed.com', 'mail.linkedin.com'}:
        company = domain.split('.')[0].replace('-', ' ').title()

    if normalize_text(company) in generic_company_blocklist and not role:
        company = ''

    return {
        'company': company,
        'role': role,
        'source': source,
        'sender_name': sender_name,
        'sender_email': sender_email,
        'sender_domain': domain,
        'snippet': snippet or subject,
    }


def parse_message_record(message, thread_labels, extract_entities_fn, classify_signal_fn):
    subject = message.get('subject', '')
    sender = message.get('from', '')
    labels = sorted(set((message.get('labels') or []) + (thread_labels or [])))
    parsed = extract_entities_fn(subject, sender, message.get('snippet', ''))
    classification = classify_signal_fn(subject, sender, labels, message.get('snippet', ''))
    parsed.update({
        'thread_id': message.get('threadId', ''),
        'message_id': message.get('id', ''),
        'date': message.get('date', ''),
        'subject': subject,
        'labels': labels,
        'classification': classification,
    })
    return parsed


def is_job_related(parsed, newsletter_noise_patterns, job_hints, normalize_text, generic_company_blocklist):
    combined = ' '.join([
        parsed.get('subject', ''),
        parsed.get('snippet', ''),
        parsed.get('company', ''),
        parsed.get('role', ''),
        parsed.get('sender_name', ''),
        parsed.get('sender_email', ''),
        ' '.join(parsed.get('labels', [])),
    ]).lower()
    if parsed['classification']['signal_type'] == 'ignore_noise':
        return False
    if any(re.search(pattern, combined, re.IGNORECASE) for pattern in newsletter_noise_patterns):
        return False
    if not any(hint in combined for hint in job_hints) and not (parsed.get('company') or parsed.get('role')):
        return False
    if 'linkedin.com' in parsed.get('sender_email', '').lower() and 'connect' in combined and not parsed.get('role'):
        return False
    if normalize_text(parsed.get('company', '')) in generic_company_blocklist and not parsed.get('role'):
        return False
    return True
