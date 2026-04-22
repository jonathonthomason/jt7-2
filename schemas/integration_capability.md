# integration_capability

## Purpose
Defines a capability that allows a bot, agent, or role to interact with an external system or internal service boundary.

## Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| capability_id | string | yes | Unique capability identifier |
| tenant_id | string | yes | Tenant scope |
| integration_domain | string | yes | gmail, calendar, drive, docs, sheets, jobboard, browser, external_account |
| action_class | string | yes | read, organize, draft, write, send, mutate |
| resource_scope | string | yes | What resource set is affected |
| allowed_subject_ids | array<string> | yes | Roles, bots, or agents allowed to use the capability |
| approval_level | string | yes | none, recommended, required |
| audit_required | boolean | yes | Whether every action must be logged |
| execution_mode | string | yes | direct, approval_gated, orchestrated_only |
| status | string | yes | active, paused, deprecated |
| created_at | datetime | yes | Creation timestamp |
| updated_at | datetime | yes | Last update timestamp |
| notes | string | no | Notes or assumptions |

## Rules
- capabilities are tenant-scoped
- send and mutate actions should default to stronger approval levels than read and organize
- execution_mode should align with risk and ownership boundaries
- capability grants do not override surface policy or tenant policy
