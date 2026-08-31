---
dataset: customer_support_tickets
scenario: focus_inference
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What are the main kinds of issues these support tickets are about?"
source_table: augment_table/customer_support_tickets/focus_inference/original.csv
generated_at: 2026-07-26T13:05:53.007257+00:00
wall_seconds: 54.02
---

# Customer Support Ticket Analysis: Main Issue Categories

## Dataset Overview
- **Total tickets:** 250 (CS-0001 to CS-0250)
- **Priority levels:** Critical, High, Medium, Low
- **Channels:** Email, Chat, Phone, In-App

---

## Main Issue Categories

### 1. 🔴 Outages & Critical Service Disruptions
The single largest category by business impact. These are tickets where core platform functionality is completely unavailable for one or more tenants.

**Examples:**
- Production 502 gateway errors (CS-0003), tenant fully unresponsive / NXDOMAIN (CS-0129)
- Webhook delivery failures blocking order fulfilment (CS-0014, CS-0169)
- Scheduled job / cron automation failures (CS-0069, CS-0154)
- Database put into read-only mode (CS-0029); admin console stuck loading (CS-0149)
- All cron-triggered automations stopped (CS-0154); entire platform unresponsive (CS-0074, CS-0174)

**Pattern:** Almost exclusively **Critical** priority, submitted via **phone** or **in-app**. Resolution times typically 55–110 minutes.

---

### 2. 🔐 Authentication & Identity Issues
A prominent cluster spanning SSO, MFA, session management, and OAuth.

**Examples:**
- Okta/SAML login rejecting all users for a tenant (CS-0009)
- SSO toggle broken with dead help link (CS-0033)
- SMS-based 2FA codes delayed up to 7 minutes in EU (CS-0006)
- MFA recovery account pending 11 days (CS-0164)
- Primary admin deleted by SCIM deprovisioning (CS-0059)
- Session drops every 12–15 minutes (CS-0002)
- OAuth app revocation not taking effect (CS-0159); Twilio auth token failures (CS-0124)

**Pattern:** Mixed Critical/High/Medium. Frequently escalated when an entire tenant is locked out (hundreds to thousands of users affected).

---

### 3. 💳 Billing, Invoicing & Account Management
A consistent thread of billing errors, payment failures, and pricing questions.

**Examples:**
- Duplicate invoice line items (CS-0001, CS-0144)
- Double-charged end-users via Stripe (CS-0049)
- Failed payment going to a deactivated card/former employee (CS-0017)
- Phantom seats appearing on invoice (CS-0184)
- Usage discrepancy: 2.3M API calls billed vs. 1.8M logged (CS-0032)
- Billing portal showing zero seats before renewal (CS-0204)
- Pricing questions on tiers, overages, proration, and discounts (CS-0007, CS-0065, CS-0215)

**Pattern:** Mix of High/Critical for active billing errors, Low/Medium for pricing inquiries. High urgency when finance teams have deadlines.

---

### 4. ⚡ Performance Degradation & Slow Queries
A large and recurring category, often triggered by platform updates, schema migrations, or index rebuilds.

**Examples:**
- Report generation 3× slower after migration (CS-0012, CS-0112)
- GraphQL p95 latency: 180 ms → 720 ms (CS-0077)
- Search-as-you-type: 80 ms → 600 ms in APAC (CS-0237)
- Knowledge base search: near-instant → 6–9 seconds (CS-0022)
- Bulk update of 5k records: 2 min → 12 min (CS-0217)
- Memory leaks in browser tab, Electron client, back-end worker (CS-0062, CS-0142, CS-0247)
- App start-up regression on Android: 2 s → 6 s (CS-0242)

**Pattern:** Predominantly **High** priority. Often linked to specific version bumps or migrations mentioned in the description. Long resolution times (100–165 minutes).

---

### 5. 🐛 Bugs in Core Features (UI, Data, Integrations)
A broad set of functional defects spanning many product areas.

**Sub-themes:**
- **Data integrity bugs:** CSV BOM character in exports (CS-0005), webhook signing secret not invalidated (CS-0043), sort order mismatch after index rebuild (CS-0157), currency rounding loss (CS-0090)
- **UI/UX defects:** Drag-and-drop dropping cards to wrong column (CS-0023), bulk-edit modal closing unexpectedly (CS-0063), toolbar missing strikethrough on mobile (CS-0103), file picker z-index error (CS-0183)
- **Integration bugs:** Jira export ignoring priority field (CS-0203), vCard export with stray semicolon (CS-0073), magic link opening browser instead of app on iOS (CS-0110), calendar timezone off in .ics (CS-0026)
- **Workflow builder / automation bugs:** Lost unsaved changes (CS-0010), conditional branches evaluating incorrectly (CS-0134), automations stuck after OAuth rotation (CS-0224)

**Pattern:** Mostly **Medium** priority. Wide spread across channels.

---

### 6. 🔒 Security Incidents & Concerns
A smaller but high-severity cluster demanding immediate attention.

**Examples:**
- Confirmed data exposure via non-expiring share link (CS-0189)
- API signing keys leaked in plaintext in a support response (CS-0244)
- Session fixation vulnerability flagged by pen test (CS-0139)
- Credential stuffing attack locking out primary admin (CS-0199)
- Active phishing campaign on shared CDN (CS-0219)
- SCIM-deleted admin losing billing/SSO access (CS-0059)

**Pattern:** All **Critical**; phone channel dominant. Smallest count but highest escalation risk.

---

### 7. 📦 Feature Requests & UX Enhancements
The second-largest volume category—entirely **Low** priority with short resolution times (12–30 minutes).

**Examples:**
- Pin favourite reports to navigation (CS-0004)
- Dark mode for invoice preview (CS-0011)
- Slack delivery for scheduled reports (CS-0018)
- Custom emoji reactions on task comments (CS-0038)
- Bulk archive of old projects (CS-0231)
- Offline read access for knowledge base on mobile (CS-0091)
- Per-project read-only role for auditors (CS-0058)

**Pattern:** All Low priority, exclusively submitted via email or in-app. No direct service impact.

---

### 8. ❓ Account, Compliance & Pricing Questions
Informational queries from finance, legal, security, and compliance teams.

**Examples:**
- GDPR data export format (CS-0045)
- SOC 2 Type II scope for AI features (CS-0115)
- FIPS 140-2 validation for field-level encryption (CS-0085)
- Audit log storage quota on Team plan (CS-0025)
- Contract auto-renewal clause clarification (CS-0135)
- Whether AI features respect customer-managed encryption keys (CS-0145)

**Pattern:** All **Low**, submitted via email. Often driven by procurement, legal, or security review deadlines.

---

## Summary Table

| Category | Approx. Ticket Count | Dominant Priority | Notes |
|---|---|---|---|
| Outages & service disruptions | ~25 | Critical | Highest business impact |
| Auth & identity issues | ~25 | Critical / High | Whole-tenant lockouts common |
| Performance degradation | ~20 | High | Often release-triggered |
| Core feature bugs | ~50 | Medium | Broadest category |
| Billing & account management | ~20 | High / Medium | Mix of errors and questions |
| Security incidents | ~8 | Critical | Low count, extreme urgency |
| Feature requests | ~55 | Low | High volume, no service impact |
| Compliance & pricing questions | ~45 | Low | Informational only |

---

## Notable Patterns & Exceptions

- **Release correlation:** Many High and Critical tickets explicitly cite a recent version bump, schema migration, or configuration change (e.g., CS-0005 after 4.7 release, CS-0052 after schema migration). This suggests insufficient regression testing on deployments.
- **Tenant-wide blast radius:** Critical tickets frequently involve 100s–1000s of affected users per event, making per-ticket counts understate actual impact.
- **Low vs. impactful feature requests:** Some "Low" feature requests (e.g., per-project read-only for auditors, data export controls) have implicit compliance implications that may warrant reprioritisation.
- **Weak evidence:** True root causes are not always confirmed in ticket descriptions; several Medium tickets suggest "suspected" causes (e.g., race conditions, caching bugs) without confirmed diagnosis.
