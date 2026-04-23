# Pass Logger Rules

## Purpose
Define the required transparency and troubleshooting output for every JT7 scheduled run.

## Required Run Report Sections
Every run must report:
- sources checked
- source-level success/failure
- records found
- records created
- records updated
- records skipped
- records needing review
- exact tracker tabs affected
- exact local mirror files changed
- git outcome
- warnings and errors
- overall batch assessment

---

## Gmail Report Requirements
Must include:
- threads scanned
- messages scanned
- job-related threads found
- labels changed
- signals created
- recruiters matched/created
- jobs matched/created/updated
- actions created

---

## Calendar Report Requirements
Must include:
- events scanned
- interview events found
- matched jobs
- updates written

---

## Job Board Report Requirements
Must include:
- sources checked
- sources successful
- jobs found
- jobs created
- jobs updated
- duplicates skipped
- review-needed results

---

## Tracker CRUD Report Requirements
Must report per tab:
- Jobs
- Recruiters
- Competition
- Signals
- Actions
- TaskRuns
- Lookup

For each:
- rows created
- rows updated
- rows unchanged
- row identifiers when possible

---

## Local Mirror Report Requirements
Must include:
- CSV files changed
- JSON files changed
- unchanged mirror files

---

## Git Report Requirements
Must include:
- whether a commit happened
- commit hash if commit occurred
- no-change reason if skipped

---

## Troubleshooting Requirements
Must include:
- source failures
- auth failures
- zero-result anomalies
- partial-chain failures
- downstream tasks skipped due to dependency failures

---

## Assessment Rule
Each run must end with:
- overall status
- summary of meaningful changes
- summary of missing/blocked execution
- operator-facing troubleshooting readiness
