# external_action_request

## Purpose
Defines a request to perform a high-impact external action against an external system or account.

## Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| external_action_request_id | string | yes | Unique external action request identifier |
| tenant_id | string | yes | Tenant scope |
| run_id | string | no | Related workflow or orchestrator run |
| requester_actor_id | string | yes | User or agent requesting action |
| requester_actor_type | string | yes | human or agent |
| target_integration | string | yes | gmail, calendar, drive, linkedin, indeed, workday, builtin, otta, creative_circle, browser, etc |
| action_type | string | yes | send_email, submit_application, confirm_event, modify_account_state, move_asset, etc |
| target_resource_ref | string | no | Specific external resource reference |
| payload_summary | string | yes | Human-readable summary of the proposed action |
| payload_ref | string | no | Reference to structured payload |
| approval_required | boolean | yes | Whether explicit approval is required |
| approval_request_id | string | no | Linked approval request if created |
| risk_level | string | yes | low, medium, high |
| status | string | yes | pending, approved, denied, executed, failed, canceled |
| requested_at | datetime | yes | Request timestamp |
| resolved_at | datetime | no | Resolution timestamp |
| executed_at | datetime | no | Execution timestamp |
| result_summary | string | no | Execution result summary |
| notes | string | no | Notes or assumptions |

## Rules
- all external send or commit actions should create an external_action_request
- approval-gated actions must not execute before approval resolution
- executed actions must retain audit linkage to request and result
