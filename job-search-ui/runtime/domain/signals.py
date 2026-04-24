from dataclasses import dataclass


@dataclass(frozen=True)
class SignalRecord:
    signal_id: str
    source: str
    signal_type: str
    company: str
    role: str
    date: str
    summary: str
    evidence_ref: str
    status: str
    linked_job_id: str = ''


def signal_status_from_confidence(classification: dict) -> str:
    if classification['signal_type'] == 'ignore_noise':
        return 'ignored'
    if classification.get('no_job_create'):
        return 'review_required_no_job_create'
    if classification['confidence'] >= 0.8:
        return 'accepted'
    if classification['confidence'] >= 0.5:
        return 'review_needed'
    return 'logged_low_confidence'
