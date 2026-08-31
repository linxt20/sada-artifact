---
dataset: customer_support_tickets
scenario: concept_attribute_operational
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "operational_burden"
query: "What customer issues create the most support burden?"
source_table: augment_table/customer_support_tickets/concept_attribute_operational/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:11:33.033194+00:00
wall_seconds: 106.42
---

# Customer Support Burden Analysis Report

## Executive Summary

This analysis examines 250 customer support tickets to identify which issues create the most operational burden for support and engineering teams. **The highest support burden is driven by three converging factors: (1) production outages and critical defects affecting entire tenants, (2) performance degradation issues requiring deep engineering investigation, and (3) authentication/security failures that block customer operations.**

---

## Burden Composition & Severity

### Priority and Impact Volume
- **Critical tickets** (50 tickets, 20%): Average resolution **74.4 minutes**, consuming **3,720 total minutes** of support capacity
  - **42 of 50 (84%)** affect entire customer tenants, creating exponential support multiplier
  - Represent the highest priority workload but are being resolved faster than High-priority tickets

- **High-priority tickets** (50 tickets, 20%): Average resolution **131.1 minutes**, consuming **6,555 total minutes**
  - Exceed Critical tickets in total burden despite lower priority classification
  - Indicate potential misclassification or complex root causes requiring extended investigation

### Production Outages & Incidents
- **62 tickets (24.8%)** marked as production outages/incidents
  - Average resolution time: **84.7 minutes**
  - Total burden: **5,249 minutes**
  - **47 of 62 (75.8%)** are Critical priority
  - These represent the most time-sensitive workload triggering immediate escalation

### Tenant-Wide Impact (Highest Leverage Concern)
- **84 tickets (33.6%)** affect `all_users_tenant` scope
  - Average resolution time: **83.3 minutes**
  - Total burden: **6,999 minutes** (highest single category)
  - Top categories: bug_platform_defect (37), performance_degradation (16), data_integrity_loss (8)

---

## Issue Categories Creating Most Support Burden

### 1. **Platform Bugs (Bug_Platform_Defect)** — Largest Burden Driver
- **105 tickets (42%)** of all tickets
- **Total burden score: 6,456.1** (highest composite score)
- **6,361 total resolution minutes**
- Average resolution: 60.6 minutes
- **37 tickets affect all_users_tenant** (35% of this category)
- **26 are Critical priority** 

**Key Patterns:**
- Configuration_or_state_inconsistency (most common root cause)
- Infrastructure resource exhaustion (common secondary cause)
- Affects UI/UX client, authentication, and database components
- Many involve state synchronization or cache invalidation failures

---

### 2. **Performance Degradation** — Highest Per-Ticket Burden
- **25 tickets (10%)** despite low volume
- **Total burden score: 1,894.2**
- **3,542 total resolution minutes**
- **Average resolution: 141.7 minutes** (5.8x higher than feature requests; 2.3x higher than bugs)
- **All 25 tickets are High or Critical priority**
- **16 affect entire tenants**

**Key Patterns:**
- Requires deep investigation into query plans, resource utilization, infrastructure capacity
- Common root causes: index/query performance degradation, infrastructure resource exhaustion
- Affects reporting_analytics, database_connection_pool, api_endpoint components
- Examples: search degradation (6-9s vs sub-second), report generation delays, sync latency, memory creep

---

### 3. **Authentication Access Issues** — High-Impact Security/Blocking
- **14 tickets classified as authentication_access** (plus 26 involving authentication_sso_mfa system component)
- **1,226.2 burden score** (third-highest category)
- **1,062 total resolution minutes**
- Average resolution: 75.9 minutes
- **8 are Critical priority** (57%)
- **7 affect entire tenants**

**Key Patterns:**
- Session/token validation failures
- SSO/SAML misconfigurations or provider integration issues
- Account lockouts and recovery procedures
- Direct blocker of customer operations (business-blocking impact)

---

### 4. **Data Integrity/Loss Issues** — Finance & Compliance Risk
- **9 tickets (3.6%)**
- **1,122.5 burden score**
- **825 total resolution minutes**
- Average resolution: 91.7 minutes (highest excluding performance degradation)
- **7 are Critical priority** (78%)
- **8 affect entire tenants** (89%)

**Key Patterns:**
- Complete data loss scenarios (backups, restore failures)
- Partial data corruption from migrations or bulk operations
- Audit trail gaps during compliance reviews
- Examples: workspace data loss after restore, duplicate charges during billing, lost historical analytics data

---

### 5. **Integration Connectivity Issues** — Downstream Cascading Risk
- **9 tickets (3.6%)**
- **906.8 burden score**
- **668 total resolution minutes**
- Average resolution: 74.2 minutes
- **5 are Critical priority** (56%)
- **7 affect entire tenants** (78%)

**Key Patterns:**
- Third-party dependency failures (webhooks, API integrations, OAuth)
- Sync failures affecting downstream systems (Salesforce, NetSuite, BigQuery)
- Certificate/credential rotation issues
- Business process breakdown (order sync failures block fulfillment)

---

### 6. **Account/Billing Issues** — Finance Close Risk
- **7 tickets (2.8%)**
- **671.0 burden score**
- **710 total resolution minutes**
- Average resolution: 101.4 minutes
- **4 are Critical priority** (57%)
- Common impacts: finance_close_or_compliance_at_risk, downstream systems disrupted
- Examples: duplicate billing entries, incorrect seat counts on renewal, invoice discrepancies

---

## System Components Creating Most Burden

### Critical Component Breakdown (components affecting >5 tickets):

| Component | Tickets | Avg Resolution | Burden Score | Critical Count |
|-----------|---------|-----------------|--------------|-----------------|
| **authentication_sso_mfa** | 26 | 74.3 min | 1,743.3 | 8 |
| **ui_ux_client** | 54 | 39.1 min | 1,680.9 | 1 |
| **database_connection_pool** | 14 | 94.8 min | 1,412.7 | 7 |
| **api_endpoint** | 17 | 90.7 min | 1,384.2 | 7 |
| **reporting_analytics** | 11 | 103.7 min | ~1,100 | 2 |
| **payment_billing** | 11 | 88.4 min | 897.2 | 6 |

**Authentication/SSO** and **database components** create disproportionate burden due to:
- High resolution times (74-95 minutes)
- Critical priority prevalence (8 and 7 critical respectively)
- Tenant-wide blast radius when they fail

---

## Root Cause Patterns (Technical Burden Drivers)

### By Frequency and Burden:

1. **Configuration/State Inconsistency** (42 tickets, 3,256.6 burden)
   - Stale caches, state synchronization failures, partial rollbacks
   - Requires configuration review and system state verification

2. **Infrastructure Resource Exhaustion** (26 tickets, 2,762.0 burden)
   - Connection pool exhaustion, memory creep, query timeout limits
   - Requires infrastructure scaling or optimization investigation

3. **Schema Mismatch/Migration Issues** (19 tickets, 1,167.7 burden)
   - Backward compatibility breaks, data format inconsistencies
   - Requires engineering investigation of data transformation pipelines

4. **Caching/Invalidation Stale Data** (21 tickets, 1,132.7 burden)
   - Cached values not refreshing, permission caches, search index staleness
   - Requires distributed system cache coherence debugging

5. **Index/Query Performance** (14 tickets, 995.2 burden + 2,052 total minutes)
   - Highest average resolution time (146.6 min) in this group
   - Requires query optimization and database tuning expertise

---

## Blocking Impact Analysis

### Customer Business Impact Classification:

- **Customer Business Blocked** (134 tickets, 10,048.9 burden score)
  - The dominant blocker type across all severity levels
  - Includes production outages, authentication failures, sync disruptions
  - Average resolution: 80.1 minutes (suggests complexity)

- **Finance/Compliance at Risk** (12 tickets, 1,093.5 burden score)
  - Billing discrepancies, audit gaps, compliance requirement misses
  - Average resolution: 94.5 minutes (requires careful handling)
  - Examples: year-end audits, SOX reviews, regulatory deadlines

- **Downstream System Impacted** (8 tickets, 591.3 burden score)
  - Cascade failures affecting customer's business processes
  - Examples: order sync failures, warehouse fulfillment blocks, BI report staleness

---

## Data Risk Exposure

### Issues Involving Data Risk (74 tickets, 29.6% of workload):

| Risk Type | Count | Avg Resolution | Burden |
|-----------|-------|-----------------|--------|
| Data Inconsistency/Corruption | 38 | 56.3 min | 2,053.9 |
| Quota/Limit Exceeded | 13 | 118.5 min | 834.0 |
| Data Loss Confirmed | 6 | 98.3 min | 799.0 |
| Data Exposure/Security Breach | 7 | 79.3 min | 705.5 |
| Billing Discrepancy | 7 | 100.7 min | 670.5 |
| Config Rollback Loss | 3 | 58.3 min | 337.5 |

- **29.6% of all support tickets involve data risk**
- Average resolution for data-at-risk cases: **77.1 minutes** (vs. 62.2 overall)
- These require higher scrutiny and often involve root cause analysis, forensics, or financial adjustment

---

## Key Exceptions & Weak Evidence

### Important Caveats:

1. **Feature Request Underrepresentation**: 55 low-priority feature requests consume only 1,243 total minutes (22.6 avg), suggesting good triage efficiency, but one large feature request could shift burden if complex scoping is needed.

2. **Medium Priority Complexity**: While 76 Medium-priority tickets average only 41.6 min each, some exceed 150 minutes, indicating outliers with hidden complexity.

3. **Configuration Documentation Underestimated?**: 26 "configuration_documentation" tickets average 69.3 min, higher than bugs (60.6 min), suggesting some are misclassified troubleshooting rather than pure documentation queries.

4. **Per-Ticket Variability**: Performance degradation shows 141.7 min average but ranges from 50 to 160+ minutes—some may be premature closure (simple config fix) vs. true engineering deep-dives.

5. **Data Risk Classification Gaps**: "not_present" value appears 72 times in system_component field, indicating missing categorization for some tickets—true component distribution may differ from observed.

---

## Recommendations for Burden Reduction

Based on support burden patterns, high-impact interventions would target:

1. **Infrastructure Scalability** (26 resource exhaustion incidents)
   - Connection pool tuning, capacity planning, auto-scaling policies
   - ROI: 26 tickets × 95 min avg = ~2,470 min/year saved

2. **Cache Coherence Hardening** (21 stale data incidents)
   - Improve invalidation triggering, reduce TTLs for critical caches
   - ROI: 21 tickets × 108 min avg = ~2,268 min/year saved

3. **Authentication/SSO Resilience** (26 auth tickets, 8 Critical)
   - Implement retry logic, improve token management, provider fallback
   - ROI: 26 tickets × 74 min avg = ~1,924 min/year saved

4. **Performance Query Optimization** (25 performance issues, 141.7 min avg)
   - Index tuning, query plan reviews, resource allocation
   - ROI: 25 tickets × 141.7 min avg = ~3,542 min/year saved

5. **Configuration Validation** (42 config/state inconsistency tickets)
   - Self-service runbooks, automated state checks, config drift detection
   - ROI: 42 tickets × 68 min avg (subset applicable to automation) = potential 2,856 min/year saved

---

## Conclusion

**Customer issues creating the most support burden are:**

1. **Production defects affecting entire tenants** (42 Critical tickets causing 3,720 min; 37 bugs affecting all_users_tenant causing 6,361 min total)
2. **Performance degradation requiring engineering investigation** (25 tickets, longest resolution time at 141.7 min average)
3. **Authentication/SSO failures** (26 tickets, 74.3 min avg, 8 Critical, blocking customer operations)
4. **Infrastructure resource exhaustion** (26 incidents, average 95 min requiring scale/optimization work)
5. **Configuration state inconsistency** (42 incidents, largest root cause category, requires targeted runbooks)

**Total support burden across 250 tickets: 12,214 minutes (~203 hours).** High-priority issues (Critical + High + Production Outages) consume **68% of total support time** despite representing only **44% of ticket volume**, indicating effective triage but also that complexity is concentrated in highest-impact scenarios.
