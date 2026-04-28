NOISE_COMPANIES = {
    'linkedin',
    'linkedin news',
    'linkedin sales navigator',
    'brian de haaff via linkedin',
    'eric zwierzynski via linkedin',
    'thoughtworks via linkedin',
    'tasnim dhani, aphr via linkedin',
    'makenzie larose via linkedin',
    'josh baron via linkedin',
    'sarahdoody',
    'lensa',
    'postjobfree',
    'ashbyhq',
    'mail',
    'talent',
    'indeed',
    'linkedin job alerts',
    'efinancialcareers',
}

NOISE_SUBJECT_TOKENS = {
    'i want to connect',
    'take control. build a career ai can’t replace.',
    'meta starts tracking employee laptops',
    'message replied:',
    'the psychology of token remorse',
    'just messaged you',
    'claim your exclusive offer',
    'why 5 people joined my ux job search program',
    'read our design faq',
    'accepted your invitation',
    'explore their network',
    'free interview cheat sheet',
    'was sent to ',
    'jobs similar to ',
}


def should_ignore_existing_signal(signal, normalize_text):
    signal_type = normalize_text(signal.get('signal_type', ''))
    company = normalize_text(signal.get('company', ''))
    excerpt = normalize_text(signal.get('raw_excerpt', ''))

    if signal_type == 'unknown_review_needed' and company in NOISE_COMPANIES:
        return True
    if signal_type == 'unknown_review_needed' and any(token in excerpt for token in NOISE_SUBJECT_TOKENS):
        return True
    if signal_type == 'interview_scheduling' and 'free interview cheat sheet' in excerpt:
        return True
    if signal_type == 'job_alert' and company in {'linkedin', 'linkedin job alerts', 'indeed'} and not normalize_text(signal.get('role', '')):
        return True
    return False
