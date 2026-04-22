# JT_PERSONAL integration_permissions

## Purpose
Defines tenant-level permissions for integrations and action classes across bots and agents.

---

## Gmail

### gmail.read
- integration_domain: gmail
- action_class: read
- allowed_subject_ids:
  - jt7_job_ops_bot
  - jt7_planning_bot
- approval_level: none
- audit_required: true
- execution_mode: direct

### gmail.organize
- integration_domain: gmail
- action_class: organize
- allowed_subject_ids:
  - jt7_job_ops_bot
- approval_level: recommended
- audit_required: true
- execution_mode: approval_gated

### gmail.draft
- integration_domain: gmail
- action_class: draft
- allowed_subject_ids:
  - jt7_job_ops_bot
- approval_level: none
- audit_required: true
- execution_mode: direct

### gmail.send
- integration_domain: gmail
- action_class: send
- allowed_subject_ids:
  - jt7_job_ops_bot
- approval_level: required
- audit_required: true
- execution_mode: approval_gated

---

## Calendar

### calendar.read
- integration_domain: calendar
- action_class: read
- allowed_subject_ids:
  - jt7_job_ops_bot
  - jt7_planning_bot
- approval_level: none
- audit_required: true
- execution_mode: direct

### calendar.write
- integration_domain: calendar
- action_class: write
- allowed_subject_ids:
  - jt7_job_ops_bot
  - jt7_planning_bot
- approval_level: recommended
- audit_required: true
- execution_mode: approval_gated

### calendar.send
- integration_domain: calendar
- action_class: send
- allowed_subject_ids:
  - jt7_job_ops_bot
- approval_level: required
- audit_required: true
- execution_mode: approval_gated

---

## Drive / Docs / Sheets

### drive.read
- integration_domain: drive
- action_class: read
- allowed_subject_ids:
  - jt7_platform_bot
  - jt7_job_ops_bot
  - jt7_planning_bot
- approval_level: none
- audit_required: true
- execution_mode: direct

### drive.organize
- integration_domain: drive
- action_class: organize
- allowed_subject_ids:
  - jt7_job_ops_bot
  - jt7_planning_bot
- approval_level: recommended
- audit_required: true
- execution_mode: approval_gated

### docs.write
- integration_domain: docs
- action_class: write
- allowed_subject_ids:
  - jt7_platform_bot
  - jt7_job_ops_bot
  - jt7_planning_bot
- approval_level: recommended
- audit_required: true
- execution_mode: approval_gated

### sheets.read
- integration_domain: sheets
- action_class: read
- allowed_subject_ids:
  - jt7_job_ops_bot
  - jt7_platform_bot
- approval_level: none
- audit_required: true
- execution_mode: direct

### sheets.write
- integration_domain: sheets
- action_class: write
- allowed_subject_ids:
  - jt7_job_ops_bot
- approval_level: recommended
- audit_required: true
- execution_mode: approval_gated

---

## Browser / External account actions

### browser.authenticated
- integration_domain: browser
- action_class: read
- allowed_subject_ids:
  - jt7_job_ops_bot
- approval_level: recommended
- audit_required: true
- execution_mode: approval_gated

### external.account.write
- integration_domain: external_account
- action_class: mutate
- allowed_subject_ids:
  - jt7_job_ops_bot
- approval_level: required
- audit_required: true
- execution_mode: approval_gated

---

## Shared Rules

### Rule 1
Read actions are lowest risk and default to allow when in-domain.

### Rule 2
Organize and write actions should begin as approval-aware.

### Rule 3
Send and mutate actions are always high-sensitivity by default.

### Rule 4
Platform bot defines policy but should not own routine operational external writes.

---

## Status
- state: defined
- implementation_phase: permission architecture ready
