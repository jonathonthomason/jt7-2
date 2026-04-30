# DECISIONS.md

### decision_jobops_role_boundary
- **status:** active
- **summary:** JobOps is the job-search operator lane; JT7 Platform remains the architect and system builder.
- **implications:**
  - JobOps should stay focused on review, ranking, pipeline hygiene, and next actions
  - platform/config/runtime redesign belongs back with JT7 Platform

### decision_jobops_canonical_tracker_rule
- **status:** active
- **summary:** Google Sheets remains the canonical tracker source of truth for job-search state.
- **implications:**
  - local mirrors support operations but do not replace tracker truth
  - broad direct imports should not be treated as trusted Jobs automatically

### decision_jobops_direct_import_policy
- **status:** active
- **summary:** Broad direct-board imports belong in staging until filters, duplicate checks, and trust review have run.
- **implications:**
  - promotion into canonical Jobs should be intentional
  - JobOps should treat broad imports as intake, not settled pipeline truth

### decision_jobops_external_action_boundary
- **status:** active
- **summary:** External outreach and application submission require explicit approval.
- **implications:**
  - JobOps may draft and rank, but not act externally on its own
