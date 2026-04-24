from dataclasses import dataclass


@dataclass(frozen=True)
class RecruiterRecord:
    recruiter_id: str
    contact_name: str
    company_name: str
    email: str
    tracking_status: str
