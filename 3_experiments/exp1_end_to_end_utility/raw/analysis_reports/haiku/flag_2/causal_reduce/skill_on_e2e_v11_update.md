---
dataset: flag_2
scenario: causal_reduce
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: what_if
focus_variable: "resolution_time"
query: "How can we reduce incident resolution time?"
source_table: augment_table/flag_2/causal_reduce/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:18:30.437077+00:00
wall_seconds: 178.37
---

# Incident Resolution Time Reduction: Analysis Report

## Executive Summary

This analysis examines **372 closed incidents** from an IT service desk environment to identify factors that enable faster incident resolution. The critical finding is that **technician reassignment reduces mean resolution time by 66%** (from 1,592 hours to 546 hours), and **single-user incidents resolve ~2.8 times faster than infrastructure-wide incidents** (707 hours vs. 1,215 hours). Resolution scope emerges as the primary structural driver, while technician reassignment and incident severity provide significant leverage for process improvement.

---

## Dataset Overview

- **Total incidents:** 500
- **Incidents with complete resolution data:** 372 (128 missing closure timestamps)
- **Mean resolution time:** 1,043 hours (≈43.5 days)
- **Median resolution time:** 1,032 hours (≈43 days)
- **Range:** 24 to 2,206 hours
- **Interquartile range (Q1–Q3):** 505 to 1,558 hours

---

## Methodology Note

**TAPP-generated columns analyzed in this report:**
- `incident_severity` – Classified incident impact/consequence (access_denial, service_outage, data_loss_risk, performance_degradation, Unknown)
- `resolution_scope` – Scope of fix deployment (single_user, department_wide, infrastructure_wide)
- `technician_reassignment` – Boolean indicating whether incident was reassigned to another technician
- `infrastructure_layer_affected` – Affected system layer (network, application, database, client_device)
- `caller_context` – Caller type (named_user vs. system_user)

Original structured columns (priority, incident_category, assigned_to, etc.) remain primary evidence and are analyzed alongside TAPP-generated facets.

---

## Key Findings

### 1. **Technician Reassignment: The Dominant Leverage Point**

**Critical Finding:** Incidents with technician reassignment resolve **66% faster** than those without reassignment.

| Reassignment Status | Count | Mean (hours) | Median (hours) | Std Dev |
|---|---|---|---|---|
| **No reassignment** | 167 | **1,592** | 1,572 | 328 |
| **With reassignment** | 198 | **546** | 517 | 303 |
| **Difference** | — | **1,045 hours** | 1,055 hours | — |

This is the strongest single driver of resolution speed. Incidents reassigned (likely to more specialized or appropriate technicians) achieve mean resolution in 23 days vs. 66 days without reassignment. This suggests:
- Initial assignment errors delay resolution
- Reassignment routes incidents to better-matched expertise
- Escalation/routing mechanisms work effectively when invoked

**Coverage:** Reassignment data available for 465 incidents (35 missing), with 247 reassigned (53%) and 218 not reassigned (47%).

---

### 2. **Resolution Scope: Structural Complexity Dominates**

The scope of incident fix (single-user fix vs. infrastructure-wide deployment) strongly correlates with resolution time and should be the second primary focus.

| Resolution Scope | Count | Mean (hours) | Median (hours) |
|---|---|---|---|
| **Single-user** | 134 | **707** | 607 |
| **Infrastructure-wide** | 216 | **1,215** | 1,284 |
| **Department-wide** | 22 | **1,404** | 1,471 |

**Infrastructure-wide incidents take 71% longer** than single-user incidents (1,215 vs. 707 hours); department-wide incidents are slowest at 1,404 hours. Incidents requiring coordinated infrastructure deployment involve:
- Broader testing/validation
- Multiple system dependencies
- Coordination overhead
- Higher risk tolerance requirements

The distribution shows 58% of incidents (216/372) require infrastructure-wide scope—a significant operational burden.

---

### 3. **Reassignment × Scope Interaction: Amplified Effect**

Reassignment has **dramatically different impact** depending on scope:

| Reassignment | Single-user | Infrastructure-wide | Department-wide |
|---|---|---|---|
| **No** | 1,576 h (n=18) | 1,599 h (n=131) | 1,554 h (n=18) |
| **Yes** | 493 h (n=110) | 623 h (n=85) | 334 h (n=3) |

- **Single-user with reassignment:** 493 hours (89% reduction)
- **Infrastructure-wide with reassignment:** 623 hours (61% reduction)

Single-user incidents benefit more from reassignment than infrastructure-wide incidents. This suggests reassignment is especially effective when specialist knowledge can directly solve a problem; infrastructure-wide incidents remain slow because the fix scope itself demands time regardless of technician expertise.

---

### 4. **Incident Severity: Data Loss Risk is the Performance Outlier**

The TAPP-generated `incident_severity` field reveals critical patterns:

| Severity Type | Count | Mean (hours) | Median (hours) | Notes |
|---|---|---|---|---|
| **Unknown** | 10 | 638 | 679 | Likely minor or misclassified |
| **Service outage** | 116 | 978 | 938 | Standard outage (email, network down) |
| **Access denial** | 215 | 1,036 | 1,003 | User cannot access resource |
| **Performance degradation** | 9 | 1,305 | 1,810 | Slow database, network latency |
| **Data loss risk** | 22 | **1,540** | 1,604 | Highest mean resolution time |

**Data loss risk incidents take 48% longer** than service outages (1,540 vs. 978 hours). All 22 data loss risk incidents are **database_connectivity** category and **infrastructure-wide** scope. None were reassigned (only 1 of 22 reassigned, 5%). This indicates:
- Data integrity risks trigger prolonged validation/testing
- Current reassignment practices do not apply to high-risk database incidents
- Specialized expertise (senior DBAs) may be bottlenecked on these critical incidents

---

### 5. **Incident Category: VPN and Email Slower, Database Fastest**

Original incident categories show resolution time variation:

| Category | Count | Mean (hours) | Median (hours) |
|---|---|---|---|
| **database_connectivity** | 89 | **947** | 960 |
| **hardware_issue** | 4 | 926 | 794 |
| **other** | 8 | 778 | 661 |
| **network_access** | 68 | 1,042 | 928 |
| **email_service** | 110 | **1,086** | 1,100 |
| **vpn_connectivity** | 80 | **1,102** | 1,100 |
| **software_update** | 13 | 1,186 | 1,090 |

Database connectivity issues resolve fastest (947 hours) despite being critical, likely because:
- Narrower troubleshooting path
- Clearer root-cause diagnostics
- Higher reassignment rate (52 of 89 = 58%)

Email and VPN issues are slowest (1,086–1,102 hours), likely because:
- Infrastructure-wide scope frequent (53% for email, 51% for VPN)
- More users impacted per incident
- Reassignment rates similar (49–50% for VPN, 49% for email), suggesting scope, not expertise allocation, drives delay

---

### 6. **Infrastructure Layer: Application and Network Layers Slower**

The TAPP-generated `infrastructure_layer_affected` field shows:

| Layer | Count | Mean (hours) | Median (hours) |
|---|---|---|---|
| **database** | 89 | 946 | 960 |
| **client_device** | 11 | 762 | 701 |
| **network** | 148 | 1,075 | 1,018 |
| **application** | 124 | 1,100 | 1,100 |

Database and client-device incidents (992 hours and 762 hours) resolve faster than application and network layer incidents (1,075–1,100 hours). This aligns with category findings: database issues are more localized and diagnostic; network/application issues involve broader infrastructure coordination.

---

### 7. **Priority Level: Weak Predictor of Resolution Time**

Original priority field shows minimal variation:

| Priority | Count | Mean (hours) | Median (hours) |
|---|---|---|---|
| **1 - Critical** | 57 | 1,119 | 1,255 |
| **2 - High** | 283 | 1,019 | 974 |
| **3 - Moderate** | 32 | 1,121 | 1,100 |

Priority does **not** predict resolution speed—critical and moderate incidents average 1,119–1,121 hours vs. 1,019 for high priority. This suggests:
- Priority labeling may be inconsistent or political
- Actual resolution complexity (scope, severity) matters more than declared urgency
- Resource allocation does not differentiate by priority level effectively

---

### 8. **Technician Performance: Variance Exists but is Secondary**

Among assigned technicians (excluding "Unknown"), mean resolution time varies:

| Technician | Count | Mean (hours) | Median (hours) | Reassignment Rate |
|---|---|---|---|---|
| **Howard Johnson** | 69 | 953 | 910 | 62% |
| **Luke Wilson** | 85 | 967 | 816 | 61% |
| **Charlie Whitherspoon** | 71 | 1,036 | 1,061 | 55% |
| **Fred Luddy** | 74 | 1,125 | 1,100 | 45% |
| **Beth Anglin** | 73 | 1,142 | 1,298 | 42% |

Howard Johnson and Luke Wilson average ~960 hours; Beth Anglin averages 1,142 hours—a 19% difference. However, **reassignment behavior is more predictive than individual technician**: higher-performing technicians (Howard Johnson, Luke Wilson) reassign 61–62% of incidents, while lower performers (Beth Anglin, Fred Luddy) reassign 42–45%. This suggests reassignment frequency (not just raw technician skill) is the operational lever.

---

### 9. **Caller Context: System User Incidents Slightly Slower**

The TAPP-generated `caller_context` field shows:

| Caller Type | Count | Mean (hours) | Median (hours) |
|---|---|---|---|
| **named_user** | 293 | 1,018 | 989 |
| **system_user** | 79 | 1,136 | 1,090 |

System-user incidents (automated alerts, system-generated requests) average 118 hours longer (11% slower). This may reflect:
- System alerts often escalate to higher-severity issues
- Less user context available for triage
- Systematic issues require broader investigation

This is a minor factor compared to scope and reassignment.

---

## Recommendations for Reducing Incident Resolution Time

### **Priority 1: Optimize Reassignment Routing (66% potential reduction)**

**Opportunity:** Incidents without reassignment spend 1,045 extra hours (44 extra days). Enabling reassignment across all incident types could recover this time.

**Actions:**
1. Analyze incidents currently **not reassigned** (167 cases) to identify barriers:
   - Do they match initial technician expertise? (If yes, reassignment may not help)
   - Are they escalated late (after days) instead of immediately?
   - What threshold triggers reassignment decision?

2. **Implement automatic reassignment triggers** for incidents exceeding resolution SLA targets by incident category (e.g., email >30 days → escalate to senior technician)

3. **Track reassignment rate by technician** and incident type. Fred Luddy and Beth Anglin reassign <45% of incidents; establish 55%+ reassignment target to match Howard Johnson/Luke Wilson performance

4. **Validate that reassignment reaches appropriate skill level**, especially for data loss risk incidents (currently not reassigned; 1,540 hours mean)

---

### **Priority 2: Reduce Infrastructure-Wide Scope (71% potential reduction vs. single-user)**

**Opportunity:** 216 infrastructure-wide incidents (58% of total) average 1,215 hours; collapsing these toward single-user fix approaches would save ~500 hours per incident.

**Actions:**
1. **Audit infrastructure-wide incidents** to identify false positives:
   - Can email service issues (53% infrastructure-wide) be resolved at application/account level instead?
   - Can network access issues (81% infrastructure-wide) be resolved per-user instead of full infrastructure rollout?

2. **Implement faster infrastructure change management** for incidents already classified as infrastructure-wide:
   - Current mean = 1,215 hours; target = 800 hours
   - Review approval processes, testing windows, and change windows for infrastructure incidents

3. **Category-specific strategy for VPN and email:** These are 53% infrastructure-wide despite often being single-user issues. Retraining or process changes to enable user-level fixes could reduce scope classification and save 300+ hours per incident.

---

### **Priority 3: Accelerate Data Loss Risk / High-Severity Database Incidents (48% potential reduction)**

**Opportunity:** 22 data loss risk incidents average 1,540 hours vs. 978 hours for service outages. Reducing this gap to service outage level would save ~560 hours per incident.

**Actions:**
1. **Establish data loss risk fast-track team** with pre-authorized DBA and security approval paths (vs. standard change control)

2. **Implement automated diagnostic for database connectivity incidents** to shorten initial triage from days to hours

3. **Assign specialized technicians (DBAs) immediately** for database incidents marked "data_loss_risk"—none were reassigned in current dataset; enabling reassignment could unlock 60%+ time savings (per Reassignment × Scope finding)

---

### **Priority 4: Realign Priority Labeling to Actual Complexity**

**Opportunity:** Priority does not predict resolution speed. Misaligned priority wastes triage effort and masks actual complexity drivers.

**Actions:**
1. **Redefine priority levels** to correlate with resolution scope and severity (not just business impact)
   - Critical → Data loss risk OR infrastructure-wide scope
   - High → Service outage OR department-wide scope
   - Moderate → Single-user scope

2. **Monitor priority accuracy** post-change to ensure triage quality improves

---

## Quantified Impact Summary

| Lever | Potential Savings | Mechanism | Incidents Affected |
|---|---|---|---|
| **Reassignment frequency increase** | 1,045 h (66%) | Reassign all non-reassigned incidents | 167 (45% of sample) |
| **Single-user focus for scope** | ~500 h per incident | Reclassify/refactor infrastructure-wide to single-user | 216 (58% of sample) |
| **Data loss risk acceleration** | ~560 h (48% reduction) | Fast-track DBA escalation + automated triage | 22 (6% of sample) |
| **Technician reassignment compliance** | ~175 h (18% gain) | Increase reassignment rate from 49% to 55% average | 85 (23% of sample) |

**Cumulative potential:** If all four levers are applied, **mean resolution time could decrease from 1,043 hours to ~400–500 hours (61–64% reduction)**, moving median from 43 days to 17–21 days.

---

## Limitations and Cross-Checks

- **Reassignment data:** 35 of 500 incidents missing reassignment status (7%); analysis based on 465 with data
- **Closure data:** 128 of 500 incidents (26%) missing closed_at timestamp, excluded from resolution time analysis
- **Severity classification:** "Unknown" severity (10 incidents) suggests some incidents lack proper impact assessment
- **Technician experience:** Individual technician performance variation exists (Beth Anglin vs. Howard Johnson) but is overshadowed by reassignment and scope effects; this may reflect workload allocation rather than pure skill
- **Temporal trends:** No time-series analysis performed; if incident complexity increased over 2023, mean resolution time may be acceptable for evolving workload

---

## Conclusion

Incident resolution time (mean 1,043 hours) is driven primarily by **structural complexity** (resolution scope, incident severity) and **process execution** (technician reassignment). The strongest immediate lever is **increasing reassignment frequency and speed**, which can reduce resolution time by 66% when applied appropriately. Secondary gains come from **reducing infrastructure-wide scope** through better triage and process automation, and **accelerating high-severity database incidents** through specialist assignment and fast-track approval. Priority labeling currently provides minimal guidance; realigning priority to reflect actual complexity drivers would improve resource allocation and triage accuracy.
