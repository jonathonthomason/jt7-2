# JT7 Auth Onboarding Friction and Product Requirements

## Document Metadata
- **System:** JT7 Job Intelligence System
- **Document type:** product requirements and onboarding friction analysis
- **Status:** draft-initial
- **Primary path:** `JT7/00_System/Architecture/JT7_Auth_Onboarding_Friction_and_Product_Requirements.md`

## 1. What Happened
The JT7 Google integration setup surfaced several layers of authentication and provider-setup friction that exposed a gap between a developer-capable system and a usable product onboarding flow.

### 1.1 Personal Gmail vs Workspace Confusion
The setup path initially drifted toward Google Workspace-oriented assumptions before the actual account model was clarified.

Observed issue:
- the connected account was ultimately a personal Google account
- some setup exploration moved through Workspace-oriented service-account and impersonation concepts
- this created unnecessary complexity and confusion before the correct auth model was made explicit

Why it happened:
- Google supports multiple auth patterns
- those patterns are not interchangeable
- account type was not established early enough in the setup flow

### 1.2 Service Account vs OAuth Confusion
The setup process surfaced ambiguity between:
- OAuth user authentication for a personal Google account
- advanced service-account-based flows intended for Workspace environments

Observed issue:
- service-account setup was explored before the system definitively routed the user to the correct personal-account OAuth path
- this introduced false paths and debugging noise

Why it matters:
- personal Gmail users should not be pushed toward enterprise delegation concepts
- product flow must not expose advanced auth paths unless they are actually relevant

### 1.3 Google Cloud Console Setup Burden
Even the correct OAuth flow depends on external Google Cloud configuration.

Observed issue:
- the setup depends on credentials creation outside JT7
- Google Cloud project, OAuth client setup, and credentials handling introduce nontrivial friction

Why it matters:
- users are forced into a separate administrative interface
- JT7 currently relies on a setup burden that is easy to misconfigure

### 1.4 Consent Screen Friction
OAuth onboarding depends on Google consent-screen configuration.

Observed issue:
- access setup is not only about login; it also requires app-level consent setup
- this adds another hidden prerequisite before user auth can succeed cleanly

Why it matters:
- the user may think they are ready to connect a provider when the provider app itself is not actually configured
- setup failures can appear later than the root cause

### 1.5 Test-User Friction
During development-mode Google app setup, test-user restrictions can become another hidden blocker.

Observed issue:
- authentication may fail or behave unexpectedly if the intended user is not properly configured as an allowed test user
- this is a provider-specific constraint the product must account for

Why it matters:
- this is not intuitive for standard users
- it creates silent permission ambiguity that feels like random failure

### 1.6 Approval-Routing Friction in OpenClaw
The OpenClaw runtime also introduced execution friction while attempting to inspect and verify auth flows.

Observed issue:
- shell execution and approvals did not behave consistently from the Telegram surface
- some tasks required alternate approval routing or asynchronous completion behavior
- this slowed verification and made the setup process harder to reason about

Why it matters:
- even when JT7 logic is correct, tooling or approval-path friction can break the perceived onboarding experience
- setup systems must account for execution-environment constraints, not just provider auth rules

## 2. Why This Is Not Acceptable as a Product Onboarding Flow

> MVP/runtime note: this document remains valid as a product-learning artifact, but JT7's current operational focus is narrower: use `gog` as the canonical Google capability layer, treat personal Google OAuth as the correct auth model for this instance, and verify Gmail/Sheets/Drive capability through runtime truth rather than onboarding assumptions alone.

This setup path is not acceptable as a real product onboarding experience.

### 2.1 Too Manual
The process currently requires too many explicit technical steps:
- choosing the right auth model
- configuring provider credentials manually
- understanding external Google console setup
- verifying access with low-level commands

### 2.2 Too Many Hidden Dependencies
Critical prerequisites are not obvious at the moment the user begins setup:
- Google Cloud project configuration
- OAuth client creation
- consent screen configuration
- test-user setup in some modes
- Drive folder permissions
- execution/approval path availability in the host environment

### 2.3 Too Much Technical Knowledge Required
A normal user should not need to understand:
- OAuth client credentials
- service-account delegation
- Workspace impersonation
- Google app publishing or test-user states
- terminal-based token inspection

### 2.4 Too Much Failure Ambiguity
When setup fails, the cause is often unclear:
- wrong auth mode
- missing scopes
- missing credentials
- missing folder permissions
- provider app misconfiguration
- environment execution limitations

This produces failure without clear diagnosis, which is unacceptable for product onboarding.

## 3. Product Requirements That Emerge From This
The friction above translates directly into product requirements.

### 3.1 Provider-Aware Onboarding
JT7 must know which provider is being connected and route the user into a provider-specific flow.

Requirement:
- onboarding must not treat all integrations as generic credentials problems

### 3.2 Account-Type Branching
JT7 must explicitly ask what kind of account is being connected.

Requirement:
- Google setup must branch between personal Google account and Workspace environment
- this branch must occur before advanced configuration steps are shown

### 3.3 Default OAuth for Standard Users
OAuth user auth must be the default for most users.

Requirement:
- standard single-user setups should start with direct OAuth user auth
- advanced enterprise auth should not be the default path

### 3.4 Advanced Enterprise Mode for Workspace
Workspace service-account flows must be isolated as advanced/admin setup.

Requirement:
- only show service-account/delegation setup when the user explicitly indicates an enterprise Workspace context
- clearly warn that this path does not apply to personal Gmail users

### 3.5 Connection Verification
JT7 must verify integrations before claiming success.

Requirement:
- every provider setup must include real verification of required capabilities
- for Google, this means both read and write checks for Drive/Sheets use cases

### 3.6 Reconnect and Recovery UX
Failures and expired auth states must be recoverable without developer intervention.

Requirement:
- the product must surface reconnect actions
- the system must clearly explain what failed and what the user should do next

### 3.7 Setup Wizard Requirements
JT7 needs a real setup wizard, not a sequence of low-level commands.

Requirement:
- onboarding should be stepwise, stateful, and explicit
- users should always know what step they are in and what remains

### 3.8 Minimal Exposed Technical Concepts
The product should hide technical details unless the user is in an advanced admin flow.

Requirement:
- standard onboarding should avoid exposing raw auth architecture unless necessary
- terms like domain-wide delegation, service-account impersonation, or test-user configuration should only appear when relevant

## 4. Suggested Onboarding Architecture
A reusable onboarding architecture should follow a consistent flow.

### 4.1 Connect Provider
The user chooses the provider they want JT7 to connect.

Example:
- Google
- Slack
- Notion
- other future integrations

### 4.2 Detect or Confirm Account Type
The system asks the user what type of account is being connected.

For Google:
- personal Google account
- Google Workspace account
- not sure

### 4.3 Route Auth Path
The system selects the appropriate auth path based on provider and account type.

Examples:
- personal Google → OAuth user auth
- standard Workspace user → usually OAuth user auth
- enterprise Workspace admin setup → advanced service-account flow

### 4.4 Verify Scopes
After auth completes, JT7 must confirm that required permissions were granted.

For Google:
- Drive access
- Sheets access
- any future Gmail/calendar scopes only if actually needed

### 4.5 Confirm Readiness
The system should only mark the integration ready after verification succeeds.

Examples:
- Drive folder can be listed
- test file can be created if write access is required

### 4.6 Show Clear Errors and Recovery
If anything fails, JT7 must show:
- what failed
- likely reason
- next recovery action

The user should not need to infer the cause from low-level tool output.

## 5. Implications for JT7 as a Reusable Product
The current setup experience has direct implications for JT7 as a product.

### 5.1 Setup Must Be Simplified Before Broader Adoption
A system that requires developer-grade setup reasoning will not scale to broader use.

### 5.2 Auth Cannot Remain a Developer-Only Flow
Authentication and provider setup must become first-class product experiences.

### 5.3 Onboarding Is Part of the Product, Not a Side Concern
Onboarding determines whether the product can actually be used.

If onboarding is confusing:
- setup stalls
- trust drops
- integration value is delayed or lost

For JT7, onboarding quality is not secondary to the product. It is part of the product.

## 6. Recommended Next Steps
### 6.1 Unblock Current User Setup Manually if Needed
For the current JT7 instance, it is acceptable to finish setup through guided manual steps if that is the fastest route to working access.

### 6.2 Design a Real Auth Onboarding System Next
After the immediate user is unblocked, JT7 should define and design:
- provider-aware connection setup
- account-type routing
- auth verification steps
- reconnect and failure recovery UX
- reusable auth-state storage model

### 6.3 Treat This as Product Learning
The friction discovered here should be treated as valuable product input, not just setup inconvenience.

It reveals where JT7 must evolve from a capable internal system into a reusable product with clear and resilient onboarding.
