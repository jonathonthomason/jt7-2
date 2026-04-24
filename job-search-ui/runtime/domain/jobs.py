from dataclasses import dataclass


@dataclass(frozen=True)
class JobRecord:
    job_id: str
    company: str
    role: str
    status: str
    contact: str
    last_contact_date: str
    next_step: str
    interview_datetime: str
    source: str
    notes: str


def update_job_row_for_signal(job_row: dict, parsed: dict, classification: dict, recruiter_id: str, infer_status):
    values = job_row['values'].copy()
    new_status = infer_status(classification['signal_type'], values.get('status', ''))
    values['status'] = new_status
    values['contact'] = recruiter_id or values.get('contact', '') or parsed['sender_email']
    values['last_contact_date'] = parsed['date'] or values.get('last_contact_date', '')
    if classification['signal_type'] in {'interview_scheduling', 'reschedule'}:
        values['interview_datetime'] = parsed['date']
        values['next_step'] = 'Prepare for interview'
    elif classification['signal_type'] == 'rejection':
        values['next_step'] = 'Archive and capture lessons'
    elif classification['signal_type'] == 'application_confirmation':
        values['next_step'] = 'Wait for recruiter or hiring team response'
    elif classification['signal_type'] in {'recruiter_outreach', 'hiring_manager_communication', 'follow_up_opportunity'}:
        values['next_step'] = 'Respond to outreach'
    elif classification['signal_type'] == 'job_alert' and not values.get('next_step'):
        values['next_step'] = 'Review opportunity and decide whether to apply'
    notes = values.get('notes', '')
    addition = f" | signal {classification['signal_type']} from {parsed['source']} thread:{parsed['thread_id']}"
    if addition not in notes:
        values['notes'] = (notes + addition).strip(' |')
    return values


def make_job_row(parsed: dict, recruiter_id: str, job_id: str, classification: dict, infer_status):
    status = infer_status(classification['signal_type'])
    next_step = 'Review opportunity and decide whether to apply'
    if classification['signal_type'] == 'application_confirmation':
        next_step = 'Wait for recruiter or hiring team response'
    elif classification['signal_type'] in {'interview_scheduling', 'reschedule'}:
        next_step = 'Prepare for interview'
    elif classification['signal_type'] == 'rejection':
        next_step = 'Archive and capture lessons'
    elif classification['signal_type'] in {'recruiter_outreach', 'hiring_manager_communication', 'follow_up_opportunity'}:
        next_step = 'Respond to outreach'
    return [
        job_id,
        parsed['company'],
        parsed['role'],
        '',
        status,
        recruiter_id or parsed['sender_email'],
        parsed['date'],
        next_step,
        parsed['date'] if classification['signal_type'] in {'interview_scheduling', 'reschedule'} else '',
        '',
        '',
        '',
        parsed['source'],
        f"Created from {classification['signal_type']} Gmail signal thread:{parsed['thread_id']}",
    ]
