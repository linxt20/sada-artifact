---
dataset: customer_support_tickets
scenario: predictive_long
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "resolution_minutes"
query: "What signals suggest a support ticket will take longer to resolve?"
source_table: augment_table/customer_support_tickets/predictive_long/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:06:30.460692+00:00
wall_seconds: 58.2
---

# Analysis Report: Signals of Long-Resolution Support Tickets
**Dataset:** customer_support_tickets (haiku__skill_off variant)  
**Focus Variable:** resolution_minutes  
**Query:** What signals suggest a support ticket will take longer to resolve?

## Executive Summary

Analysis of 250 support tickets reveals that **ticket priority, communication channel, and investigation requirements** are the strongest signals for extended resolution time. High-priority tickets via email consistently take 2.5–3.5× longer to resolve than low-priority tickets, while tickets requiring investigation are 51% likely to exceed the 75th percentile (89 minutes).

---

## Key Findings

### 1. **Priority is the Dominant Signal**
Priority level shows the strongest correlation (r = 0.559) with resolution time:

| Priority | Count | Avg Time | % Long |
|----------|-------|----------|--------|
| **High** | 50 | **131.1 min** | **98.0%** |
| Critical | 50 | 74.4 min | 22.0% |
| Medium | 76 | 41.6 min | 1.3% |
| Low | 74 | 37.5 min | 2.7% |

**Insight:** High-priority tickets take nearly twice as long as Critical (counterintuitively), suggesting "High" may capture non-emergency escalations requiring deeper investigation or coordination, while "Critical" often triggers rapid incident response paths.

### 2. **Email Channel Strongly Predicts Long Resolution**
Communication channel significantly impacts resolution time:

| Channel | Count | Avg Time | % Long |
|---------|-------|----------|--------|
| **Email** | 100 | **98.3 min** | **52.0%** |
| Phone | 50 | 70.2 min | 22.0% |
| Chat | 50 | 22.5 min | 0.0% |
| In-App | 50 | 35.0 min | 0.0% |

**Insight:** Email is asynchronous and often involves billing, performance, or investigation issues that require extended back-and-forth. Chat and in-app channels show instant resolution characteristics (<35 min average), likely for simple clarifications or UX issues.

### 3. **High Priority + Email: Near-Universal Long Resolution**
The combination of High priority and email channel is a near-perfect long-resolution signal:
- **n=49 tickets; 100% exceed 75th percentile (89 min)**
- **Average: 132.8 minutes**

Example patterns in this segment:
- Billing disputes with invoice corrections
- Performance degradation requiring investigation
- Schema or integration failures needing root cause analysis

### 4. **"Needs Investigation" Flag: 51% Long Resolution Rate**
Tickets flagged as requiring investigation are 2.5× more likely to extend beyond 89 minutes:
- **Needs investigation=Yes:** 51.3% long, avg 90.1 min
- **Needs investigation=No:** 20.4% long, avg 60.2 min
- **Correlation with resolution time: r = 0.264**

Combinations amplify this:
- Investigation + blocked customer: **70% long (101 min avg)**
- Investigation + High priority: **135.3 min avg**

### 5. **Customer Blocked Status: Moderate Predictor (31% Long)**
When customers report being blocked:
- **31.0% exceed 89-min threshold**
- **Average: 74.1 min** (vs. 62.1 for unblocked)
- **Correlation: r = 0.124**

This suggests blocked customers *do* correlate with longer resolution but is not deterministic—some blocked issues (technical bugs on chat) resolve quickly via workarounds.

### 6. **Technical Issue Complexity is a Weak Signal**
Presence of technical issues shows minimal correlation (r = 0.018) with resolution time:
- **Technical issue=Yes:** avg 66.4 min, 19.1% long
- **Technical issue=No:** avg 64.5 min, 26.6% long

This counterintuitive pattern suggests purely technical bugs often have clear reproduction steps and known runbooks, whereas non-technical issues (billing, policy, cross-team coordination) involve more manual judgment.

### 7. **Negative Signal: Multiple Users Does Not Predict Longer Resolution**
Surprisingly, tickets affecting multiple users show *lower* long-resolution rates (20.9% vs. 28.9%), suggesting incidents with broad impact may have pre-built escalation and incident response playbooks that accelerate resolution.

---

## Weak Evidence & Exceptions

1. **Critical Priority Paradox:** 22% of Critical tickets exceed 89 min, suggesting rapid response classification may differ from resolution complexity. Many Critical tickets likely reach resolution by declaring the incident or providing a workaround, while High-priority work (e.g., deep performance investigations) takes longer.

2. **External Integration Flag Weak:** Correlation is only r = 0.087, suggesting third-party dependencies don't strongly predict duration in this dataset.

3. **Single High-Priority Email Exception:** One Medium-priority email ticket (CS-0005) reached 140 min, confirming that channel + priority are the primary factors, not priority alone.

---

## Recommendations for Identifying Long-Resolution Tickets

### Red Flags (High → Long Resolution):
1. **High priority + email channel** → expect 130+ min average
2. **Requires investigation flag** → 51% risk of exceeding 89 min
3. **Customer blocked + investigation** → particularly high-friction (101 min avg, 70% long)
4. **Performance, billing, or integration issues** in email channel

### Green Flags (Likely Fast Resolution):
1. **Chat or in-app channel** → 22–35 min average, 0% long
2. **Low or Medium priority** → 37–41 min average
3. **No investigation flag** → 60 min average

### Decision-Ready Threshold:
For triage or SLA planning, tickets matching **High priority + email** should be treated as intrinsically long-duration work and routed to senior agents or engineering early.

---

## Data Quality Notes

- **Sample size:** 250 tickets across 20 agents and 4 channels
- **Long-resolution threshold (75th percentile):** 89 minutes
- **No missing values in binary flags**
- **Variant:** skill_off (no agent-skill augmentation applied)
