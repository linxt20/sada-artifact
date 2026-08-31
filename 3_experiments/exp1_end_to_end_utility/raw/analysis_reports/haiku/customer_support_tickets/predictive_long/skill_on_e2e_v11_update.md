---
dataset: customer_support_tickets
scenario: predictive_long
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "resolution_minutes"
query: "What signals suggest a support ticket will take longer to resolve?"
source_table: augment_table/customer_support_tickets/predictive_long/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:13:13.085980+00:00
wall_seconds: 171.49
---

# Support Ticket Resolution Duration Analysis

## Executive Summary

Analysis of 250 customer support tickets identifies consistent signals predicting longer resolution times. Tickets taking above the median resolution time of 58 minutes (n=123, 49.2%) cluster around specific combinations of ticket properties. The strongest predictors combine **ticket channel, priority level, and semantic business impact**—with technical issue complexity (captured in TAPP-generated `issue_type`) and root cause clarity playing reinforcing roles.

---

## Methodology Note

This analysis uses the complete augmented table combining original structured columns (`ticket_id`, `priority`, `channel`, `agent_id`, `resolution_minutes`) with TAPP-generated semantic columns: **`issue_type`, `blocker_scope`, `business_impact`, and `root_cause_clarity`**. TAPP-generated columns are used to add semantic specificity and cross-check relationships with structured fields; they are not treated as replacements for raw evidence. All quantified claims include counts, means, medians, and percentages.

---

## Key Signals for Longer Resolution Times

### 1. **Email Channel is the Strongest Single Predictor** (Original Structured Column)

Email tickets take dramatically longer than other channels:

| Channel   | Count | Mean (min) | Median (min) | % Above Median |
|-----------|-------|-----------|-----------|---|
| **Email** | 100   | **98.3**  | **92.5**  | **80.0%** |
| Phone     | 50    | 70.2      | 72.5      | 76.0% |
| In-app    | 50    | 35.0      | 31.0      | 10.0% |
| Chat      | 50    | 22.5      | 23.0      | 0.0% |

**Finding**: Email channel tickets average 98.3 minutes vs. 22.5 minutes for chat—a **4.4× difference**. 80% of email tickets exceed the median resolution time. This suggests email communication patterns (asynchronous, longer thread context, potentially multiple stakeholders) correlate with investigation depth or complexity.

---

### 2. **High Priority Compounds Resolution Duration** (Original Structured Column)

Priority level strongly correlates with resolution time:

| Priority  | Count | Mean (min) | Median (min) | % Above Median |
|-----------|-------|-----------|-----------|---|
| **High**  | 50    | **131.1** | **131.0** | **98.0%** |
| Critical  | 50    | 74.4      | 72.5      | 86.0% |
| Medium    | 76    | 41.6      | 37.0      | 10.5% |
| Low       | 74    | 37.5      | 24.0      | 31.1% |

**Finding**: High-priority tickets take 3.5× longer than Medium (131.1 vs. 41.6 min) and 2× longer than Low. Notably, Critical-priority tickets (74.4 min mean) resolve *faster* than High-priority tickets (131.1 min)—likely because Critical issues trigger immediate escalation and dedicated resources.

**Combined Effect**: High-priority tickets routed through email average **132.8 minutes** (n=49), with 100% exceeding the median. This represents the strongest single combination observed.

---

### 3. **Performance Degradation Issues Take Longest** (TAPP-Generated: `issue_type`)

Among issue types, performance and infrastructure issues consistently require extended resolution:

| Issue Type                    | Count | Mean (min) | % Above Median |
|-------------------------------|-------|-----------|---|
| **Performance Degradation**   | 23    | **138.0** | **95.7%** |
| Billing/Invoice               | 7     | 101.4     | 100.0% |
| Data Loss/Corruption          | 7     | 95.7      | 100.0% |
| Configuration/Setup           | 9     | 104.3     | 77.8% |
| Authentication/Access         | 10    | 73.1      | 60.0% |
| Bug/Error (general)           | 92    | 59.4      | 35.9% |
| Feature Request               | 56    | 23.1      | 3.6% |

**Finding**: Performance degradation tickets average 138.0 minutes—**6× longer** than feature requests (23.1 min). Billing and data-loss issues (100% above median) suggest financial/compliance and data-integrity concerns trigger thorough investigation.

---

### 4. **Business Impact Severity Drives Duration** (TAPP-Generated: `business_impact`)

The semantic classification of business impact strongly predicts resolution time:

| Business Impact                           | Count | Mean (min) | % Above Median |
|-------------------------------------------|-------|-----------|---|
| **Performance/Quality Degradation**       | 30    | **128.3** | **90.0%** |
| **Financial/Compliance Risk**             | 18    | **89.4**  | **100.0%** |
| **Operational Blockers (Critical Workflows)** | 69    | **80.3**  | **73.9%** |
| User Experience Friction                  | 73    | 40.4      | 12.3% |
| Not Present (low urgency)                 | 60    | 37.8      | 30.0% |

**Finding**: Tickets affecting performance take 3.2× longer (128.3 min) than those causing mere user friction (40.4 min). Financial/compliance issues take 89.4 minutes on average and *all* (100%) exceed the median, suggesting compliance and billing matters receive comprehensive audit/investigation.

---

### 5. **Root Cause Clarity Significantly Extends Duration** (TAPP-Generated: `root_cause_clarity`)

The degree to which root cause is evident or documented correlates with resolution time:

| Root Cause Clarity                      | Count | Mean (min) | Median (min) | % Above Median |
|------------------------------------------|-------|-----------|-----------|---|
| **Customer-Provided Evidence**          | 131   | **80.9**  | **70.0**  | **60.3%** |
| **Requires Investigation**              | 9     | 59.4      | 60.0      | 66.7% |
| Suspected by Customer (no proof)        | 35    | 68.9      | 60.0      | 54.3% |
| Not Present (no root cause info)        | 75    | **35.7**  | **25.0**  | **25.3%** |

**Finding**: Tickets where customers provide evidence average **80.9 minutes**—**2.3× longer** than those with no root cause information (35.7 min). This suggests that **complete problem statements and evidence enable deeper investigation** rather than quick dismissal. Paradoxically, more thorough tickets take longer because they trigger comprehensive diagnosis.

---

### 6. **Scope of Impact Affects Triage and Resolution** (TAPP-Generated: `blocker_scope`)

The scope of who/what is affected correlates with resolution effort:

| Blocker Scope                  | Count | Mean (min) | Median (min) | % Above Median |
|--------------------------------|-------|-----------|-----------|---|
| **All Tenants/Enterprise**     | 32    | **81.2**  | **70.0**  | **71.9%** |
| Team or Account (scoped)       | 169   | 68.6      | 60.0      | 55.0% |
| Single User                    | 38    | 41.1      | 36.0      | 7.9% |
| Not Present                    | 11    | 41.2      | 27.0      | 36.4% |

**Finding**: Enterprise-wide outages (81.2 min mean) take 2× longer than single-user issues (41.1 min). However, team/account scope issues are most numerous (169/250) and represent a large share of above-median resolutions (93/169 = 55%).

---

## Composite Risk Patterns

The strongest resolution-time indicators emerge from combinations:

### Pattern 1: Email + High Priority (Slowest)
- **Count**: 49 tickets  
- **Mean**: 132.8 minutes  
- **100% exceed median**  
- **Typical issues**: Performance degradation, billing problems, infrastructure incidents routed through async email channels

### Pattern 2: Performance Degradation + Customer Evidence
- **Count**: 19 tickets  
- **Mean**: 142.5 minutes  
- Common characteristics: enterprise-level performance issues with telemetry, logs, or query data provided by customer

### Pattern 3: Operational Blockers with Team Scope
- **Count**: 47 tickets  
- **Mean**: 83.5 minutes  
- **78.7% exceed median**  
- Represents critical workflow interruptions requiring investigation and possible deployment/config changes

### Pattern 4: Contrast—Feature Requests (Fastest)
- **Count**: 56 tickets  
- **Mean**: 23.1 minutes  
- **Only 3.6% exceed median**  
- Simple triage and response; no investigation required

---

## Cross-Validation: TAPP Columns vs. Original Structured Data

The TAPP-generated semantic columns reinforce relationships already visible in priority and channel:

- **`issue_type`** adds specificity: email + High priority tickets concentrate in performance_degradation (26/49 High+Email tickets), confirmation that performance issues inherently require extended diagnosis.
- **`business_impact`** validates severity: High-priority tickets are predominantly marked operational_blockers or performance_degradation, confirming that priority labels correlate with task complexity.
- **`root_cause_clarity`** explains investigation burden: 79 of 131 (60.3%) tickets with customer-provided evidence exceed median time, vs. only 19 of 75 (25.3%) with no clarity. More information triggers deeper review.
- **`blocker_scope`** shows scale effect: enterprise-scope issues (all_tenants_or_enterprise) are 71.9% above median, supporting the pattern that wider impact = longer resolution.

No TAPP-generated column contradicts or substantially overlaps with structured fields; each adds orthogonal semantic signal.

---

## Actionable Signals Summary

Tickets are likely to exceed median (58 min) resolution time when:

1. **Routed via email** (80% above median) — especially with High priority
2. **Marked High priority** (98% above median, avg 131 min)
3. **Performance degradation or data-loss issue type** (96–100% above median)
4. **Business impact is performance/quality or financial/compliance** (90–100% above median)
5. **Customer provides detailed evidence or root cause hypothesis** (60% above median vs. 25% with no clarity)
6. **Scope is all-tenants/enterprise** (72% above median vs. 8% for single-user)

Conversely, tickets **likely to resolve quickly** (below median):
- Feature requests (3.6% above median)
- Chat channel (0% above median)
- Low/Medium priority (10–31% above median)
- Single-user scope (7.9% above median)
- No root cause information provided (25% above median)

---

## Data Coverage

Analysis covers 250 tickets with complete data across all 10 columns (0 missing values). Median resolution time: **58 minutes** (mean: 64.9, SD: 41.1). Resolution times ranged from 12 to 180 minutes.
