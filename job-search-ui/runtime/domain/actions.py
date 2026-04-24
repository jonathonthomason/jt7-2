from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


@dataclass(frozen=True)
class ActionRecord:
    action_id: str
    job_id: str
    company: str
    instruction: str
    reason: str
    urgency: str
    status: str
    created_at: str
    due_at: str
    owner: str


ACTION_REQUIRED_SIGNAL_TYPES = {
    'recruiter_outreach',
    'interview_scheduling',
    'reply_received',
    'follow_up_opportunity',
    'reschedule',
    'hiring_manager_communication',
}


def proposed_action_instruction(signal_type: str) -> str:
    instructions = {
        'recruiter_outreach': 'Reply to recruiter outreach',
        'application_confirmation': 'Track application and wait for update',
        'interview_scheduling': 'Prepare for interview',
        'reschedule': 'Confirm rescheduled interview details',
        'cancellation': 'Review cancellation and decide next follow-up',
        'rejection': 'Archive opportunity and capture lessons',
        'hiring_manager_communication': 'Respond to hiring manager communication',
        'follow_up_opportunity': 'Send follow-up response',
        'reply_received': 'Review reply and respond',
        'job_alert': 'Review opportunity and decide whether to apply',
        'unknown_review_needed': 'Review unclassified job-related signal',
    }
    return instructions.get(signal_type, 'Review job-related signal')


def canonical_action_status(classification: dict, linked_job_id: str = '') -> str:
    signal_type = classification.get('signal_type', '')
    if classification.get('resolved') or classification.get('completed'):
        return 'done'
    if classification.get('waiting'):
        return 'waiting'
    if classification.get('no_job_create'):
        return 'blocked'
    if signal_type == 'application_confirmation':
        return 'waiting'
    if signal_type in {'rejection', 'cancellation'}:
        return 'done'
    if signal_type in {'recruiter_outreach', 'reply_received', 'follow_up_opportunity', 'interview_scheduling', 'reschedule', 'hiring_manager_communication'}:
        return 'open'
    if linked_job_id:
        return 'open'
    return 'blocked'


def canonical_action_due_at(classification: dict, run_at: datetime) -> str:
    signal_type = classification.get('signal_type', '')
    if signal_type in {'interview_scheduling', 'reschedule'}:
        return (run_at + timedelta(hours=24)).isoformat()
    if signal_type in {'recruiter_outreach', 'reply_received', 'follow_up_opportunity', 'hiring_manager_communication'}:
        return (run_at + timedelta(hours=48)).isoformat()
    return ''


def action_urgency(signal_type: str) -> str:
    return 'high' if signal_type in {'interview_scheduling', 'reschedule', 'recruiter_outreach'} else 'medium'
