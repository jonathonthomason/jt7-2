# JT7 Auth Architecture and Onboarding Spec

## Document Metadata
- **System:** JT7 Job Intelligence System
- **Document type:** authentication architecture and onboarding specification
- **Status:** draft-initial
- **Primary path:** `JT7/00_System/Architecture/JT7_Auth_Architecture_and_Onboarding_Spec.md`

## 1. Problem Statement
Authentication complexity exists because external systems do not expose a single universal access model.

For Google specifically, authentication differs materially between:
- personal Google accounts
- standard Google Workspace user accounts
- advanced Workspace admin-managed service-account setups

These are not interchangeable.

Why Google auth differs between personal vs Workspace:
- personal Google accounts are user-owned and typically authorize apps through direct OAuth consent
- Google Workspace environments may support the same OAuth user flow, but may also support organization-managed service-account delegation when explicitly configured by an administrator
- service-account impersonation depends on Workspace admin controls that do not exist for personal Gmail accounts

What breaks when the wrong auth mode is used:
- personal users cannot complete Workspace-only impersonation flows
- service-account auth may appear technically configured but still fail against personal Drive or Sheets resources
- missing or incorrect scopes can allow partial access but block required operations
- onboarding becomes confusing because users are asked to perform steps irrelevant to their account type

Why JT7 must explicitly handle this distinction:
- the system needs a reliable way to choose the correct auth flow before setup starts
- false assumptions create avoidable failures
- both product UX and agent behavior depend on knowing what auth model applies
- JT7 must scale across personal, single-user, and multi-user environments without mixing incompatible auth strategies

## 2. Auth Modes Overview

> Runtime note: for JT7's current MVP and runtime readiness standard, `gog` should be treated as the canonical Google capability layer. Personal Google OAuth user auth is the correct model for this environment. Gmail read/search, Sheets read/write, and Drive read/write are only considered accessible when auth, tool availability, runtime execution, and command-path verification all pass. Telegram should not be assumed to be a valid execution surface unless explicitly verified.

## 2.1 Mode 1 — OAuth User Auth (Default)
### Description
Interactive OAuth login where the user signs in directly and grants JT7 access.

### Use for
- personal Gmail and personal Google Drive users
- most normal single-user JT7 setups
- most standard Workspace users unless a dedicated enterprise delegation pattern is intentionally required

### Characteristics
- interactive login
- user grants access directly
- simplest and safest default
- appropriate for Drive and Sheets access tied to a real user account

### Do not use when
- the environment explicitly requires non-interactive enterprise delegation
- an administrator has mandated service-account-based access architecture instead

## 2.2 Mode 2 — Workspace Service Account (Advanced)
### Description
Service-account-based access pattern for Google Workspace environments using domain-wide delegation and impersonation.

### Use for
- enterprise or admin-managed Google Workspace environments
- cases where an admin has explicitly configured domain-wide delegation
- multi-user or organizational deployments that require managed non-user auth patterns

### Characteristics
- requires admin setup
- requires Workspace domain-wide delegation
- supports impersonation of Workspace users
- intended for advanced managed environments

### Do not use when
- the connected account is a personal Gmail / personal Google Drive account
- the Workspace admin has not configured delegation
- the JT7 instance is a normal single-user setup that can use OAuth directly

## 3. Account Type Decision Layer
A required onboarding decision step must exist before Google auth begins.

### Required onboarding question
**What type of Google account are you connecting?**

### Option 1 — Personal Google account (Gmail)
- **Auth mode:** `oauth_user`
- **Setup path:** interactive OAuth user login
- **Guidance:** use personal sign-in and grant Drive/Sheets access directly
- **Warning:** do not use Workspace service-account impersonation

### Option 2 — Google Workspace account (company-managed)
- **Auth mode:** default to `oauth_user`; allow `service_account` only if explicitly configured
- **Setup path:** start with OAuth user auth unless enterprise delegation is intentionally required
- **Guidance:** standard users should not be pushed into service-account setup by default
- **Warning:** service-account flow requires admin support and domain-wide delegation

### Option 3 — Not sure
- **Auth mode:** default to `oauth_user`
- **Setup path:** route to simplest working interactive login path first
- **Guidance:** if OAuth user auth succeeds, remain there; only escalate to Workspace service-account flow if enterprise requirements demand it
- **Warning:** do not assume Workspace-managed service-account setup just because the email uses a custom domain

## 4. Default System Behavior
JT7 default behavior should be:
- use OAuth user auth by default
- treat service-account flow as advanced and opt-in
- never assume a Google account is Workspace-based without explicit user confirmation
- never attempt impersonation unless explicitly configured for a Workspace deployment
- verify read and write access after auth before marking the integration ready

## 5. Onboarding Flow

## 5.1 Step 1 — User selects account type
The user must choose:
- personal Google account
- Google Workspace account
- not sure

## 5.2 Step 2 — System explains recommended auth method
JT7 should clearly explain:
- why the selected mode is recommended
- what access will be requested
- what the user should expect next

## 5.3 Step 3 — User completes auth
- OAuth user auth: user signs in and grants scopes
- Workspace service account: admin/operator completes advanced configuration and delegation setup

## 5.4 Step 4 — System verifies access
Verification must include:
- authentication success check
- Drive read test
- Sheets write-capability test or safe create test

## 5.5 Step 5 — System stores auth metadata
JT7 should store:
- provider
- account type
- auth mode
- granted scopes
- connection state
- verification timestamp

## 5.6 Step 6 — System confirms readiness
JT7 should only confirm readiness when:
- auth succeeded
- required scopes are available
- read/write verification passed

## 6. Auth State Model
JT7 should track auth state per integration using a structured record.

Recommended fields:
- `provider` — e.g. `google`
- `account_type` — `personal` | `workspace`
- `auth_mode` — `oauth_user` | `service_account`
- `account_identifier` — email or principal identifier where applicable
- `scopes_granted` — normalized list of granted scopes
- `connection_state` — `connected` | `expired` | `failed`
- `last_verified_at` — last successful verification timestamp
- `notes` — optional operational context

Why this matters:
- agents need to know which auth path applies
- onboarding and troubleshooting depend on durable auth metadata
- future integrations should share the same state model

## 7. Google-Specific Implementation Guidance

## 7.1 Personal Accounts
Personal Google accounts must use OAuth user auth.

JT7 should not route personal Gmail users into service-account impersonation.

## 7.2 Workspace Accounts
Workspace accounts may use:
- OAuth user auth in normal cases
- service-account delegation only when enterprise setup explicitly requires it and admin support exists

## 7.3 Drive Folder Access Model
Drive access may rely on:
- files owned by the connected user
- folders shared with the connected user
- in advanced Workspace cases, folders accessible through the impersonated identity

JT7 should verify actual folder access, not just token validity.

## 7.4 Required Scopes
For Google Drive and Sheets integration, JT7 should verify access sufficient for:
- reading Drive contents
- locating target folders
- creating Sheets files
- reading and updating sheet content

At minimum, Drive and Sheets access must be granted.

## 7.5 Verification Steps
Google integration verification should include:
1. auth success check
2. Drive read test
3. target folder visibility test
4. Drive or Sheets write test
5. returned object ID/link capture

A connection is not considered complete until both read and write capabilities are verified.

## 8. Failure Scenarios

## 8.1 Wrong Auth Mode Selected
### Detection
- service-account flow attempted for personal Gmail account
- auth setup path requires Workspace-only features that do not exist

### Recovery
- stop advanced flow
- route user back to account-type selection
- switch to OAuth user auth

## 8.2 Missing Scopes
### Detection
- auth succeeds but Drive or Sheets actions fail with permissions errors

### Recovery
- re-run OAuth flow with required scopes
- verify scopes before marking integration ready

## 8.3 Expired Tokens
### Detection
- previously working auth begins failing on access attempts
- token refresh or API access errors occur

### Recovery
- refresh token if supported
- otherwise re-authenticate user
- update `connection_state`

## 8.4 Drive Access But No Folder Permissions
### Detection
- authentication succeeds but JT7 folder is not visible or writable

### Recovery
- confirm correct account is connected
- share target folder with that account if necessary
- re-run verification test

## 8.5 Service Account Without Delegation
### Detection
- service-account auth path is configured but impersonation or access fails

### Recovery
- confirm Workspace admin configuration
- if not configured, fall back to OAuth user auth where appropriate

## 8.6 Revoked Access
### Detection
- token exists but API requests fail due to revoked permissions

### Recovery
- mark connection as failed or expired
- require re-authentication
- re-run verification after reconnect

## 9. Product Design Implications
Authentication must be explicit in onboarding UI because:
- users often do not know which Google auth model applies
- the wrong flow creates confusing failure states
- implicit assumptions lead to wasted time and broken setup paths

Why silent assumptions cause failure:
- a personal Gmail user may be incorrectly routed into enterprise-only setup
- a Workspace user may be given advanced configuration they do not need
- agents cannot troubleshoot correctly if account type and auth mode are hidden

How this affects multi-user JT7 instances:
- each user or tenant may have a different provider/account type combination
- auth state must be tracked per user/integration, not globally assumed
- onboarding must separate individual-user auth from enterprise-admin auth

How to design for clarity and low friction:
- ask account type early
- default to simplest valid flow
- explain why the recommended method is selected
- verify access before claiming success
- surface remediation steps clearly on failure

## 10. Future Extensibility
This model extends cleanly to other providers because the same structure applies:
- provider type
- account type or tenant context
- auth mode
- scopes/permissions
- connection state
- verification status

This supports:
- Slack OAuth installs
- Notion token-based or OAuth connections
- multiple integrations per user
- multi-tenant JT7 systems
- enterprise deployments with admin-managed auth paths

The main architectural rule should remain stable:
- choose auth mode based on provider + account context
- do not collapse all auth into one assumed setup path

## 11. Next Steps
Recommended next steps:
- return to Google OAuth user auth setup for the personal account
- verify Drive and Sheets access using the correct user-auth flow
- then proceed to workbook creation and system execution
