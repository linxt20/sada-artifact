---
dataset: customer_support_tickets
scenario: focus_inference
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What are the main kinds of issues these support tickets are about?"
source_table: augment_table/customer_support_tickets/focus_inference/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:06:12.369411+00:00
wall_seconds: 45.77
---

# Customer Support Tickets: Main Issue Categories Analysis

## Overview

This analysis examines 250 customer support tickets to identify the main kinds of issues these tickets address. The dataset reveals a diverse range of problems spanning system functionality, feature requests, infrastructure disruptions, and operational challenges.

## Primary Issue Categories

### 1. **Bugs** (34.0%, 85 tickets) - Most Prevalent
Bugs represent the largest category of support issues, accounting for one-third of all tickets. These span multiple domains:
- **Authentication bugs** (7 tickets): Session management failures, SSO issues, password resets
- **UX/Usability bugs** (4 tickets): UI interaction problems, responsiveness issues
- **Permission/Access bugs** (4 tickets): Role-based access failures, permission caching issues
- **Data handling bugs**: CSV export issues, file uploads, data import/export failures
- **API consistency bugs**: Schema mismatches, backwards-incompatible changes
- **Browser/platform compatibility**: Cross-browser and OS-specific rendering failures

Examples: Mobile app crashes on Android 14, session drops in Chrome, CSV export with stray BOM characters, webhook signature verification failures.

### 2. **Feature Requests** (26.8%, 67 tickets) - Second Largest
A significant portion of tickets represent enhancement requests and new capabilities:
- **UX enhancements** (10 tickets): Dark mode, keyboard shortcuts, navigation improvements
- **Compliance features** (6 tickets): GDPR data export formats, audit trail requirements
- **Security features** (6 tickets): Field-level encryption, role-based access controls
- **Workflow enhancements** (4 tickets): Project duplication, automated templates
- **Integration expansions** (4 tickets): Slack delivery, Google Sheets piping, Ariba punch-out

Examples: Favorite report pinning, color-coded tags, scheduled report Slack delivery, custom emoji reactions on comments.

### 3. **Infrastructure Issues** (15.6%, 39 tickets)
Critical operational disruptions affecting multiple users:
- **Service outages** (3 tickets): 502 errors, dashboard unavailability, blank canvas rendering
- **Data recovery** (2 tickets): Workspace restoration failures, data loss scenarios
- **Authentication infrastructure** (3 tickets): SSO configuration, OAuth failures, API authentication
- **Network/connectivity** (3 tickets): CORS errors, VPC peering issues, DNS problems
- **Database/storage** (3 tickets): Connection pool exhaustion, read-only modes, CDN failures

Examples: Production dashboard 502 errors, webhook delivery failures, CORS errors on chat widget, read-only database states.

### 4. **Performance Issues** (8.4%, 21 tickets)
Degradation in system responsiveness and efficiency:
- **Memory leaks** (3 tickets): Electron app memory creep, browser tab memory consumption
- **Query performance** (2 tickets): Report generation slowdowns, search latency
- **Indexing performance** (2 tickets): Background job delays after scaling
- **API latency** (1 ticket): GraphQL endpoint degradation from 180ms to 720ms p95

Examples: 30% slowdown on large dataset queries, knowledge base search taking 6-9 seconds, memory consumption reaching 3GB in desktop client.

### 5. **Billing Issues** (8.0%, 20 tickets)
Financial accuracy and payment processing problems:
- **Pricing clarification** (4 tickets): Tiered pricing questions, volume discount scope
- **Billing accuracy** (2 tickets): Invoice discrepancies, phantom line items
- **Payment processing** (2 tickets): Failed payments, declined card handling, dunning email issues
- **Billing errors** (2 tickets): Double-charging, duplicate line items

Examples: Invoice showing duplicate seat charges, customer double-charged via Stripe, monthly usage report discrepancies.

### 6. **Authentication Issues** (2.8%, 7 tickets)
Identity and access control problems:
- SSO failures and configuration issues
- Session management problems
- API key/token authentication failures
- MFA/2FA delays and delivery issues

### 7. **Security Issues** (2.8%, 7 tickets)
Data protection and security vulnerabilities:
- **Security incidents** (2 tickets): Misconfigured share links, phishing campaigns, account compromise
- **Privacy concerns** (1 ticket): Sensitive data in push notifications
- **Vulnerability reports** (1 ticket): Session fixation issues

### 8. **Integration Issues** (1.6%, 4 tickets)
Third-party connection and sync problems:
- OAuth token issues
- Salesforce sync failures
- Order management system integration outages

## Distribution by Severity

The dataset shows a balanced severity distribution:
- **Critical** (20.0%, 50 tickets): Service outages, data loss, security incidents, complete access loss
- **High** (20.0%, 50 tickets): Significant degradation, widespread functionality impact
- **Medium** (30.4%, 76 tickets): Affects specific users or features, workarounds available
- **Low** (29.6%, 74 tickets): Feature requests, minor UI issues, clarifications

## Key Patterns

1. **Functional Issues Dominate**: Bugs and infrastructure problems (49.6% combined) represent actual system failures requiring engineering intervention.

2. **Enhancement-Driven Growth**: Feature requests (26.8%) indicate ongoing product expansion needs, particularly around UX, compliance, and workflow automation.

3. **Operational Reliability**: Performance and infrastructure issues (24.0% combined) highlight scalability and reliability concerns as the customer base grows.

4. **Billing Accuracy**: Even at 8.0%, billing issues carry high resolution urgency due to financial impact and customer trust implications.

5. **Cross-functional Scope**: Issues span authentication, data handling, third-party integrations, and compliance—indicating a complex platform with many integration points.

## Conclusion

Support tickets primarily address three core problem areas: **product bugs requiring fixes** (34%), **feature enhancements for competitive positioning** (27%), and **infrastructure/operational stability** (16%). The remaining 23% covers performance optimization, billing accuracy, and security/compliance enhancements. This distribution suggests a maturing platform balancing stability improvements with feature velocity and expansion into enterprise compliance requirements.
