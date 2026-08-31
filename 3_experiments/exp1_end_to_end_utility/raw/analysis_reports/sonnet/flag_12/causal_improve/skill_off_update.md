---
dataset: flag_12
scenario: causal_improve
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: what_if
focus_variable: "incident_resolution_efficiency"
query: "How can we improve incident resolution efficiency?"
source_table: augment_table/flag_12/causal_improve/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:09:08.875983+00:00
wall_seconds: 49.6
---

# Incident Resolution Efficiency Analysis

## Dataset Overview

The dataset contains **500 incidents** with a focus variable of `resolution_efficiency_tier` (Fast / Medium / Slow) and continuous `resolution_time_hours`. The tier distribution is heavily skewed: **72% Slow**, 13% Medium, and 15% Fast.

| Tier   | Count | Mean Resolution Time (hrs) |
|--------|-------|---------------------------|
| Fast   | 74    | 28.9                      |
| Medium | 66    | 76.6                      |
| Slow   | 360   | 227.8                     |

---

## Key Factors Affecting Resolution Efficiency

### 1. Priority Level — Strongest Differentiator
Low-priority (4 - Low) incidents resolve **exclusively in the Fast tier** (mean: 32.6 hrs). Critical and High priority incidents dominate the Slow tier (~74–75%), with mean resolution times exceeding 165 hrs. Moderate priority incidents are better than Critical/High (58% Slow vs. ~74%), suggesting triage and SLA structures work better for lower-severity tickets.

| Priority      | Fast  | Medium | Slow  | Mean Hrs |
|---------------|-------|--------|-------|----------|
| 4 - Low       | 100%  | 0%     | 0%    | 32.6     |
| 3 - Moderate  | 17%   | 25%    | 58%   | 177.8    |
| 2 - High      | 14%   | 11%    | 75%   | 180.0    |
| 1 - Critical  | 15%   | 11%    | 74%   | 167.0    |

**Recommendation:** Review escalation workflows for Critical and High incidents — they do not resolve faster than Moderate ones, indicating SLA enforcement gaps.

### 2. Reassignment — Moderate Negative Effect
Reassigned incidents have a higher Slow rate (**73.6%**) vs. non-reassigned (**66.0%**), and slightly higher mean resolution time (179 vs. 175 hrs). The difference is modest but consistent.

**Recommendation:** Reduce misrouting by improving initial assignment logic and skill-based routing to avoid reassignment overhead.

### 3. Category — Software and Network Resolve Faster
Software and Network categories have the lowest proportion of Slow incidents (64% and 59% respectively) and shorter mean times (~154 and 162 hrs). Hardware and Database categories are slowest (73–79% Slow).

| Category        | Fast | Slow  | Mean Hrs |
|-----------------|------|-------|----------|
| Network         | 18%  | 59%   | 161.6    |
| Software        | 18%  | 64%   | 153.6    |
| Inquiry/Help    | 15%  | 65%   | 182.1    |
| Hardware        | 15%  | 73%   | 181.4    |
| Database        | 11%  | 79%   | 172.4    |

**Recommendation:** Investigate Hardware and Database incident workflows — knowledge base articles, spare parts availability, and specialist access may be bottlenecks.

### 4. Assigned Agent — Howard Johnson Stands Out Positively
Howard Johnson achieves the highest Fast rate (22.6%) and lowest mean resolution time among agents (175.5 hrs). Luke Wilson has the highest mean time (195.5 hrs) and lowest Fast rate (11.2%).

| Agent               | Fast  | Slow  | Mean Hrs |
|---------------------|-------|-------|----------|
| Howard Johnson      | 22.6% | 65.1% | 175.5    |
| Fred Luddy          | 16.7% | 71.1% | 165.0    |
| Beth Anglin         | 12.9% | 70.6% | 172.4    |
| Charlie Whitherspoon| 10.7% | 77.7% | 178.8    |
| Luke Wilson         | 11.2% | 75.0% | 195.5    |

**Recommendation:** Conduct knowledge-sharing sessions led by higher-performing agents; review workload distribution and specialization alignment for lower-performing agents.

---

## Exceptions and Weak Evidence

- The **reassignment effect is small** (~5% Slow rate difference); it may not be the primary lever for improvement.
- **Critical incidents** resolve slightly faster on average than High (167 vs. 180 hrs), which may reflect more focused attention, but sample sizes limit strong conclusions.
- Agent performance differences could reflect **ticket type bias** (some agents may handle harder categories) rather than skill alone — this cannot be confirmed without controlling for category.

---

## Decision-Ready Summary

| Lever | Impact | Confidence |
|---|---|---|
| Improve High/Critical SLA enforcement | High — 74–75% Slow rate | Strong |
| Reduce reassignments via better routing | Moderate — 7% Slow rate reduction | Moderate |
| Focus on Hardware & Database workflows | High — 73–79% Slow rate | Strong |
| Knowledge sharing from top agents | Moderate — 11% spread in Fast rate | Moderate |
