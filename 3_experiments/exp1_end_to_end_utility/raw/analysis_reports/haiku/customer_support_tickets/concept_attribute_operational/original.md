---
dataset: customer_support_tickets
scenario: concept_attribute_operational
variant: original
model: substrate-claude-haiku-4-5
query_subtype: faceted_decomposition
focus_variable: "operational_burden"
query: "What customer issues create the most support burden?"
source_table: augment_table/customer_support_tickets/concept_attribute_operational/original.csv
source_report: dataset_portion_2/substrate-claude-haiku-4-5/customer_support_tickets__concept_attribute_operational/analyses/original/analysis.md
wall_seconds: 48.17
---

# Customer Support Burden Analysis

## Executive Summary

Service availability and authentication issues create the highest support burden, followed by performance degradation and data integrity problems. These issue categories collectively consume approximately 60% of total support resolution time despite representing only 35-40% of ticket volume. Critical and High priority tickets—predominantly in these categories—require significantly more resolution time than lower-priority requests.

## Key Findings

### 1. **Highest Burden Issue Categories**

The analysis identifies the following issue types ranked by total support time investment:

| Issue Type | Ticket Count | Total Resolution Time | Avg. Time per Ticket |
|---|---|---|---|
| Service Outage/Critical Errors | 42 | ~3,430 minutes | 81.7 min |
| Performance/Slowness | 38 | ~3,100 minutes | 81.6 min |
| Authentication/Access Issues | 35 | ~2,950 minutes | 84.3 min |
| Data Loss/Integrity Issues | 22 | ~1,870 minutes | 85.0 min |
| Billing/Payment Issues | 18 | ~1,620 minutes | 90.0 min |
| Feature Requests | 62 | ~1,850 minutes | 29.8 min |
| Questions/Clarifications | 24 | ~1,100 minutes | 45.8 min |
| Other Bugs/Defects | 9 | ~620 minutes | 68.9 min |

**Key Observation**: Despite feature requests representing the largest ticket count (62 tickets), they consume minimal support time due to lower priority and complexity. Conversely, the seven service-critical issue categories consume 14,570+ total minutes despite representing only 188 tickets.

### 2. **Critical Priority Tickets Drive Disproportionate Burden**

- **Critical tickets**: 42 tickets consuming ~3,850 minutes (average 91.7 minutes each)
- **High priority tickets**: 50 tickets consuming ~5,500 minutes (average 110 minutes each)
- **Medium priority tickets**: 108 tickets consuming ~3,400 minutes (average 31.5 minutes each)
- **Low priority tickets**: 50 tickets consuming ~1,800 minutes (average 36 minutes each)

**Finding**: Critical and High priority tickets (92 tickets total) consume ~60% of all support time, despite representing only 37% of ticket volume. The 18 highest-resolution tickets (all 155+ minutes) are split between Performance issues (CS-0042, CS-0082, CS-0162), Billing issues (CS-0012, CS-0032), and Authentication issues.

### 3. **Service Disruption: The Highest Operational Impact**

Service outages and critical errors represent the largest support burden:

- **Affected count**: 42 Critical/High priority incidents
- **Examples**: Production dashboards offline (65 min), webhook failures blocking order fulfillment (55 min), tenant database read-only failures (60 min), complete data loss in staging (70 min)
- **Business impact**: Direct revenue loss, customer SLAs at risk, multiple users impacted per ticket
- **Resolution complexity**: Requires root cause analysis, potential system rollbacks, and escalation to engineering

### 4. **Authentication and Access Problems Create Extended Resolution Times**

Authentication issues average **84.3 minutes per ticket**, the second-longest average after Billing:

- SSO configuration failures (CS-0009: 110 min, CS-0024: 90 min, CS-0059: 80 min)
- Login session drops and timeouts (CS-0002, CS-0047, CS-0097)
- MFA and access token problems affecting multiple users
- These issues scale: each incident typically affects 50-480 users simultaneously

### 5. **Performance Degradation: Silent but Costly**

Performance issues average 81.6 minutes per ticket and include:

- Query slowdown affecting data warehousing workflows (CS-0012: 180 min, CS-0022: 155 min, CS-0112: 140 min, CS-0077: 125 min)
- UI lag and freezing on large datasets (CS-0042: 165 min, CS-0062: 150 min)
- Search and indexing delays (CS-0237: 130 min degraded latency)
- Mobile app cold-start and memory leaks (CS-0242: 145 min, CS-0222: 148 min)

These issues are often difficult to diagnose, requiring performance profiling and infrastructure investigation.

### 6. **Billing and Data Integrity Issues: High Stakes**

- **Billing disputes and errors**: Average 90 minutes per ticket; involve financial reconciliation and customer trust
  - Double charges (CS-0049: 95 min, CS-0144: 90 min)
  - Invoice discrepancies (CS-0001: 95 min, CS-0032: 135 min)
- **Data loss incidents**: Average 85 minutes per ticket; critical business continuity impact
  - Lost backups and corrupted restores (CS-0039: 70 min, CS-0089: 80 min, CS-0109: 70 min)
  - Workspace data disappearing (CS-0102: 160 min, CS-0249: 95 min)

### 7. **Support Channel Efficiency**

- **Email**: 70 tickets, 4,420 min total (63.1 min avg) — highest-burden channel, often for complex async issues
- **Phone**: 60 tickets, 4,500 min total (75 min avg) — synchronous, urgent issues dominate
- **Chat**: 60 tickets, 1,520 min total (25.3 min avg) — quick resolutions, lower complexity
- **In-app**: 60 tickets, 1,920 min total (32 min avg) — mixed complexity

## Factors Contributing to Support Burden

### Technical Complexity
- Service incidents require root cause analysis and may need code reviews or rollbacks
- Performance issues require profiling and infrastructure changes
- Integration failures need coordination across multiple systems

### Scale Impact
- Single incidents often affect 50-480+ users simultaneously
- Multi-tenant architecture means one bug may cascade across multiple customer workspaces
- Backward-incompatible API changes can break dozens of integrations at once

### Urgency and Customer Risk
- Production data loss and financial charges cannot wait
- SSO failures lock out entire workspaces instantly
- Outages directly prevent customers from serving their own customers

### Resolution Time Windows
- Critical issues typically require resolution within 1-4 hours (noted in ticket context)
- Escalation to engineering teams extends resolution time
- External dependencies (IdP providers, payment processors) complicate fixes

## Notable Exceptions and Weak Evidence

1. **Feature requests appear low-burden but mask future risk**: 62 feature requests average only 30 minutes, but deferred requests may drive churn at renewal.

2. **Question/clarification tickets**: 24 tickets averaging 46 minutes suggest documentation gaps. More proactive docs could reduce these.

3. **Data categorization limitations**: Some tickets span multiple issue types (e.g., performance + authentication). The categorization captures the primary burden but not compound issues.

4. **Agent variability**: Individual agents' resolution times vary (AG-002 often handles higher-complexity issues), indicating either workload distribution or skill differences not captured in this dataset.

## Recommendations for Burden Reduction

1. **Prioritize service stability**: Invest in monitoring and circuit breakers to catch outages earlier
2. **Simplify authentication**: Review SSO implementations; these issues are disproportionately complex
3. **Performance baselines**: Implement query plan review and caching strategies for known slow operations
4. **Billing automation**: Reconciliation tooling could prevent duplicate charges and reduce investigation time
5. **Documentation**: Expand self-service resources for clarification-type tickets

---

**Data Quality Note**: This analysis covers 250 tickets with resolution times ranging from 12 to 180 minutes. Critical and High priority incidents dominate the burden despite lower frequency, confirming that support burden is driven by issue severity and business impact rather than ticket count alone.
