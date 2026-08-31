---
dataset: customer_support_tickets
scenario: focus_inference
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What are the main kinds of issues these support tickets are about?"
source_table: augment_table/customer_support_tickets/focus_inference/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:11:06.179625+00:00
wall_seconds: 59.26
---

# Customer Support Tickets: Main Kinds of Issues Analysis

## Executive Summary

This analysis examines 250 customer support tickets to identify the primary categories of issues. The dataset reveals a diverse portfolio of support requests, dominated by functional defects and feature requests, with a significant portion involving service availability and performance concerns.

## Primary Issue Classification

The support tickets are distributed across several main kinds of issues:

| Issue Category | Count | % of Total |
|---|---|---|
| **Functional Bugs** | 71 | 28.4% |
| **Feature Requests** | 57 | 22.8% |
| **Service Outages** | 28 | 11.2% |
| **Performance Issues** | 26 | 10.4% |
| **Policy/Billing Questions** | 22 | 8.8% |
| **UX/UI Issues** | 22 | 8.8% |
| **Data/Recovery Issues** | 8 | 3.2% |
| **Security Issues** | 7 | 2.8% |
| **Billing Disputes** | 6 | 2.4% |
| **Documentation Requests** | 2 | 0.8% |
| **Integration Issues** | 1 | 0.4% |

## Major Groupings

### Technical Problems (59.8% of tickets)

The largest category comprises technical defects and degradations:

- **Functional bugs** (28.4%): Service behavior deviations, incorrect outputs, missing functionality in existing features (e.g., session drops, CSV export issues, permission cascading problems)
- **Outages** (11.2%): Complete or near-complete service unavailability affecting single or multiple tenants (e.g., 502 errors, webhook failures, database connectivity issues)
- **Performance issues** (10.4%): Latency degradation, query timeouts, memory leaks (e.g., search taking 6-9 seconds instead of sub-second, app startup regression from 2 to 6 seconds)
- **UX/UI bugs** (8.8%): Minor usability defects, layout issues, navigation problems (e.g., truncated tooltips, misaligned elements)

### Customer Requests (31.6% of tickets)

- **Feature requests** (22.8%): Enhancement proposals, new capability requests, quality-of-life improvements (e.g., dark mode, bulk operations, better notification controls)
- **Information requests** (8.8%): Policy questions, clarifications on contract terms, billing mechanics, feature availability (e.g., pricing for add-ons, tier eligibility)

### High-Criticality Issues (8.4% of tickets)

- **Security incidents** (2.8%): Credential exposure, data access vulnerabilities, unauthorized token usage, suspected breaches
- **Data/recovery issues** (3.2%): Data loss, corrupted state, failed migrations, restoration requests
- **Billing disputes** (2.4%): Overcharges, phantom line items, failed refund processes

## Impact and Scope Patterns

### Severity Distribution
The issue_severity column shows substantial concentration in high-impact problems:
- **Medium severity**: 97 tickets (38.8%)
- **High impact**: 55 tickets (22.0%)
- **Blocking P1**: 53 tickets (21.2%)
- **Low impact**: 45 tickets (18.0%)

### Affected Scope
Scope distribution reveals system-wide and tenant-level prevalence:
- **Entire tenant**: 120 tickets (48.0%)—systemic impact across all users in an account
- **Not applicable/future impact**: 67 tickets (26.8%)—feature requests and policy questions with no current impact
- **Subset of users**: 48 tickets (19.2%)—regional, group-specific, or permission-scoped issues
- **Single user**: 13 tickets (5.2%)—isolated user experience problems
- **Multi-tenant/system-wide**: 2 tickets (0.8%)—platform-level incidents

## Resolution Pathways

The actionability field indicates what types of fixes are required:
- **Engineering fixes required**: 140 tickets (56.0%)—code or configuration changes by engineering
- **Product roadmap items**: 54 tickets (21.6%)—feature requests deferred to roadmap planning
- **Self-service guidance**: 23 tickets (9.2%)—policy questions and how-to clarifications
- **Data recovery**: 14 tickets (5.6%)—restore from backup or manual data remediation
- **Configuration changes**: 11 tickets (4.4%)—admin panel or tenant-level settings adjustments
- **Credential/access management**: 8 tickets (3.2%)—account recovery, MFA reset, access grants

## Key Observations

1. **Bug-driven workload**: Nearly half of all tickets (47.2%) are defect reports, indicating significant ongoing quality issues spanning functional correctness, service availability, and performance.

2. **Outage and performance concerns are material**: Service outages (11.2%) and performance degradation (10.4%) collectively represent 21.6% of the queue, signaling infrastructure or scalability challenges.

3. **Feature request volume is substantial**: 22.8% of tickets are enhancement requests, suggesting customers perceive feature gaps or quality-of-life shortcomings relative to competitor offerings.

4. **Tenant-level impact is the norm**: Nearly half of all issues (48.0%) affect entire tenants, not isolated users, indicating systemic or configuration-wide problems rather than isolated edge cases.

5. **Diverse resolution modalities**: While engineering fixes dominate (56.0%), over 40% of tickets require non-code resolutions (guidance, roadmap deferral, data recovery, configuration, access management), pointing to operational and product process bottlenecks.

6. **High-criticality incidents are present but minority**: Security and data loss issues (6.0% combined) represent meaningful risk but are lower volume than functional bugs or performance issues.

## Conclusion

The main kinds of issues in this support queue are: **(1) functional software defects**, **(2) feature enhancement requests**, and **(3) service availability/performance problems**. Approximately 60% are technical problems requiring engineering intervention, while 32% are customer feature and policy requests. The remaining 8% are high-stakes incidents (security, data loss, billing disputes) or administrative issues. Impact tends to be broad (tenant-wide rather than per-user), and resolution pathways are diverse, reflecting the complexity of a mature SaaS platform.
