from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from runtime.utils.id_utils import next_id

WritebackAction = Literal['create', 'merge', 'hold', 'reject']


@dataclass(frozen=True)
class StagingWritebackPlan:
    action: WritebackAction
    reason: str
    staged_company: str
    staged_role: str
    matched_job_id: str = ''
    create_row: list[str] | None = None
    update_values: dict[str, str] | None = None


JOB_COLUMNS = [
    'job_id',
    'company',
    'role',
    'location',
    'status',
    'contact',
    'last_contact_date',
    'next_step',
    'interview_datetime',
    'direct_application_link',
    'job_posting_link',
    'fit_score',
    'source',
    'notes',
]


TARGET_ROLE_TOKENS = [
    'senior product designer',
    'principal product designer',
    'lead product designer',
    'staff product designer',
    'design lead',
    'founding product designer',
    'product design manager',
]

ALLOWED_LOCATION_TOKENS = [
    'remote',
    'dallas',
    'fort worth',
    'dfw',
    'irving',
    'plano',
    'frisco',
    'addison',
    'grapevine',
    'arlington',
    'richardson',
]

WEAK_ROLE_TOKENS = [
    'design system',
    'mobile',
    'visual',
    'brand',
    'ui designer',
    'marketing designer',
]


def norm(value: str) -> str:
    return ' '.join((value or '').strip().lower().split())


def location_allowed(location: str) -> bool:
    text = norm(location)
    return any(token in text for token in ALLOWED_LOCATION_TOKENS)


def target_role_match(role: str) -> bool:
    text = norm(role)
    return any(token in text for token in TARGET_ROLE_TOKENS)


def weak_role_match(role: str) -> bool:
    text = norm(role)
    return any(token in text for token in WEAK_ROLE_TOKENS)


def is_canonical_job(job: dict[str, str]) -> bool:
    return bool(norm(job.get('job_id', '')) and norm(job.get('company', '')) and norm(job.get('role', '')))


def canonical_jobs(jobs: list[dict[str, str]]) -> list[dict[str, str]]:
    return [job for job in jobs if is_canonical_job(job)]


def find_duplicate_job(staged: dict[str, str], jobs: list[dict[str, str]]) -> dict[str, str] | None:
    staged_company = norm(staged.get('company', ''))
    staged_role = norm(staged.get('role', ''))
    staged_link = norm(staged.get('job_posting_link', '') or staged.get('direct_application_link', ''))
    staged_location = norm(staged.get('location', ''))

    for job in jobs:
        job_company = norm(job.get('company', ''))
        job_role = norm(job.get('role', ''))
        job_link = norm(job.get('job_posting_link', '') or job.get('direct_application_link', ''))
        job_location = norm(job.get('location', ''))
        if staged_link and job_link and staged_link == job_link:
            return job
        if staged_company and staged_company == job_company and staged_role and staged_role == job_role:
            if not staged_location or not job_location or staged_location == job_location:
                return job
    return None


def build_create_row(staged: dict[str, str], existing_ids: list[str], now_iso: str) -> list[str]:
    job_id = next_id('job_', existing_ids)
    notes = staged.get('notes', '') or ''
    provenance = staged.get('provenance', '') or 'Promoted from staging intake'
    combined_notes = ' | '.join(part for part in [notes, provenance] if part)
    return [
        job_id,
        staged.get('company', ''),
        staged.get('role', ''),
        staged.get('location', ''),
        'Reviewing',
        '',
        now_iso,
        'Review promoted staging opportunity and decide whether to apply',
        '',
        staged.get('direct_application_link', ''),
        staged.get('job_posting_link', ''),
        staged.get('fit_score', ''),
        staged.get('source', 'staging'),
        combined_notes,
    ]


def build_merge_values(existing_job: dict[str, str], staged: dict[str, str], now_iso: str) -> dict[str, str]:
    merged = existing_job.copy()
    merged['status'] = 'Reviewing' if merged.get('status', '') in {'Cold', 'Found', 'Not Applied'} else merged.get('status', '')
    merged['last_contact_date'] = now_iso
    merged['next_step'] = 'Review refreshed staging evidence and decide whether to apply'
    if not merged.get('job_posting_link'):
        merged['job_posting_link'] = staged.get('job_posting_link', '')
    if not merged.get('direct_application_link'):
        merged['direct_application_link'] = staged.get('direct_application_link', '')
    notes = merged.get('notes', '')
    addition = staged.get('provenance', '') or 'Merged staged evidence'
    if addition and addition not in notes:
        merged['notes'] = ' | '.join(part for part in [notes, addition] if part)
    return merged


def plan_staging_writeback(staged: dict[str, str], jobs: list[dict[str, str]], now_iso: str | None = None) -> StagingWritebackPlan:
    now_iso = now_iso or datetime.utcnow().isoformat()
    all_jobs = list(jobs)
    jobs = canonical_jobs(jobs)
    company = staged.get('company', '')
    role = staged.get('role', '')

    if not target_role_match(role):
        return StagingWritebackPlan('reject', 'outside_target_role_set', company, role)

    if weak_role_match(role):
        return StagingWritebackPlan('hold', 'weak_role_pattern_requires_manual_review', company, role)

    if not location_allowed(staged.get('location', '')):
        return StagingWritebackPlan('hold', 'outside_allowed_location_rule', company, role)

    duplicate = find_duplicate_job(staged, jobs)
    if duplicate:
        return StagingWritebackPlan(
            'merge',
            'duplicate_match_found',
            company,
            role,
            matched_job_id=duplicate.get('job_id', ''),
            update_values=build_merge_values(duplicate, staged, now_iso),
        )

    existing_ids = [job.get('job_id', '') for job in all_jobs]
    return StagingWritebackPlan(
        'create',
        'no_duplicate_and_fit_passed',
        company,
        role,
        create_row=build_create_row(staged, existing_ids, now_iso),
    )
