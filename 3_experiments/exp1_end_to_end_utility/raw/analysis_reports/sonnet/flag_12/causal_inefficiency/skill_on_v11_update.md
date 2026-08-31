---
dataset: flag_12
scenario: causal_inefficiency
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "resolution_efficiency"
query: "Why are some incidents resolved inefficiently, and which underlying issues drive it?"
source_table: augment_table/flag_12/causal_inefficiency/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:13:49.708708+00:00
wall_seconds: 72.03
---

# Incident Resolution Inefficiency Analysis
**Dataset:** `sonnet__skill_on_v11_update.csv` | **n = 500 incidents** | **Variant: skill_on**

---

## Executive Summary

Inefficient resolutions (defined as resolution time ≥ 252.7 hours, the 75th percentile) affect **~25% of incidents**. Mean resolution time is **178 hours (~7.4 days)**. Several structural and operational factors drive slower closures, with **maintenance action type**, **Inquiry/Help category**, **specific assignee workload/skill patterns**, and **reassignment** as the most actionable levers.

---

## Key Findings

### 1. Resolution Action Type — Strongest Single Driver
Incidents requiring `maintenance` resolve slowest and have the highest inefficiency rate:

| Resolution Action | Mean Hours | Inefficiency Rate | Count |
|---|---|---|---|
| maintenance | 196.5 | **40.0%** | 5 |
| repair | 181.8 | 25.7% | 233 |
| connectivity_fix | 173.7 | 23.4% | 94 |
| update_install | 156.4 | 23.3% | 43 |
| replacement | 176.2 | 21.4% | 56 |
| configuration_change | 185.8 | **0.0%** | 2 |

`maintenance` incidents are rare (n=5) so the 40% rate should be treated as directional. `repair` actions dominate volume (n=233) and carry a materially elevated inefficiency rate, making them the largest aggregate contributor.

---

### 2. Incident Category — Inquiry/Help Incidents Disproportionately Slow
Despite typically being lower-complexity requests, `Inquiry / Help` incidents have the highest inefficiency rate (35%) and mean resolution time (182 hours):

| Category | Mean Hours | Inefficiency Rate |
|---|---|---|
| Inquiry / Help | 182.1 | **35.0%** | 
| Hardware | 181.4 | 25.9% |
| Software | 153.6 | 21.2% |
| Network | 161.6 | 18.2% |
| Database | 172.4 | 10.5% |

This suggests a routing or prioritisation problem: informational/help requests are not being triaged to faster-resolution channels.

---

### 3. Assignee Skill Variation — Luke Wilson Stands Out
Resolution efficiency varies meaningfully across the five assignees:

| Assignee | Mean Hours | Inefficiency Rate | Incidents |
|---|---|---|---|
| Luke Wilson | **195.5** | **32.8%** | 116 |
| Howard Johnson | 175.5 | 27.4% | 106 |
| Charlie Whitherspoon | 178.8 | 24.3% | 103 |
| Fred Luddy | 165.0 | 18.9% | 90 |
| Beth Anglin | 172.4 | 18.8% | 85 |

Luke Wilson handles the largest volume (116 incidents, 23% of total) yet shows the slowest mean resolution and highest inefficiency rate — nearly 14 percentage points above Fred Luddy and Beth Anglin. His caseload is concentrated in Hardware (83%), and his reassignment rate (29.3%) is close to the dataset average (28.6%), so reassignment alone does not explain the gap. This pattern is consistent with a skill-fit or capacity constraint relative to the incident mix.

---

### 4. Reassignment — Moderate Contributor
Reassigned incidents take slightly longer and fail to resolve efficiently more often:

| Reassignment | Mean Hours | Inefficiency Rate |
|---|---|---|
| False | 176.1 | 23.8% |
| True | 184.2 | **27.9%** |

The gap (~8 hours mean, ~4 pp inefficiency) is real but modest, suggesting reassignment is a symptom rather than a primary cause. Interestingly, reassigned incidents have a *lower* recurrence signal rate (20.3% vs. 36.7% for non-reassigned), implying reassigned tickets tend to be novel or complex — contributing to delay for different reasons.

---

### 5. Physical Intervention Requirement
Incidents requiring on-site physical intervention average ~11.5 hours longer than remote-resolvable ones (180.4 vs. 168.9 hours) and have a modestly higher inefficiency rate (25.4% vs. 23.3%). This reflects logistical overhead rather than a process failure, though incidents combining **reassignment + physical intervention** average **194 hours** — the most delayed combination (n=115).

---

### 6. Recurrence Signal
Recurring incidents resolve marginally slower (182.3 vs. 176.6 hours, ~1.8 pp higher inefficiency rate). The weak signal suggests recurrence is not a dominant inefficiency driver in this dataset, though it may indicate unresolved root causes in printer and hardware-heavy incident clusters.

---

### 7. Priority Inversion (Notable Exception)
Critical (P1) incidents resolve **faster** on average (167 hours) than High (P2) incidents (180 hours). This suggests escalation procedures work correctly for top-priority items, but P2 incidents — which form the bulk of volume — may lack sufficient urgency handling.

---

## Root Cause Summary

| Driver | Strength | Evidence |
|---|---|---|
| Repair/maintenance action type | **Moderate–High** | +28–40% inefficiency vs. best-performing types |
| Inquiry/Help routing gap | **Moderate** | 35% inefficiency rate, highest of all categories |
| Assignee skill/capacity (Luke Wilson) | **Moderate** | 32.8% inefficiency, 195.5 hr mean on highest volume |
| Reassignment + physical intervention combination | **Moderate** | 194 hr mean for combined cases |
| Recurrence without root-cause resolution | **Weak** | Only ~6 hr mean difference |
| Priority inversion (P1 vs P2) | **Informational** | P1 handled faster; P2 backlog may be undertriaged |

---

## Recommendations

1. **Review Inquiry/Help routing**: Redirect simple information requests to self-service or fast-track queues to reduce the 35% inefficiency rate in that category.
2. **Address Luke Wilson's incident mix or provide targeted support**: Investigate whether workload redistribution or skill development can close the ~14 pp efficiency gap with peers.
3. **Pre-authorise physical dispatches**: For incidents flagged `requires_physical_intervention=True`, proactive scheduling can reduce the mean 194-hour tail for reassigned+physical cases.
4. **Root-cause recurring hardware incidents**: Printer and input device clusters show persistent recurrence; preventive maintenance or asset replacement cycles may reduce reopen rates.
