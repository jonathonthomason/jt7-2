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
