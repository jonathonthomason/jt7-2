from dataclasses import dataclass


@dataclass(frozen=True)
class SignalRecord:
    signal_id: str
    source: str
    signal_type: str
    company: str
    role: str
    detected_at: str
    summary: str
    evidence_ref: str
    status: str
    linked_job_id: str = ''
