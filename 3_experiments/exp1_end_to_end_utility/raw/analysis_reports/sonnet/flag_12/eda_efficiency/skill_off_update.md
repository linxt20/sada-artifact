---
dataset: flag_12
scenario: eda_efficiency
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "resolution_efficiency"
query: "How does incident resolution efficiency vary across category, priority, and assignment group?"
source_table: augment_table/flag_12/eda_efficiency/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:09:52.415378+00:00
wall_seconds: 31.42
---

# Incident Resolution Efficiency Analysis

**Dataset:** 500 closed/resolved incidents | **Focus variable:** `resolution_time_hours`, `sla_met`, `resolution_speed_category`

---

## 1. By Category

| Category | Mean Hrs | Median Hrs | N | SLA Met % |
|---|---|---|---|---|
| Software | 153.6 | 148.0 | 33 | 12.1% |
| Network | 161.6 | 186.4 | 22 | 9.1% |
| Database | 172.4 | 177.6 | 19 | 10.5% |
| Hardware | 181.4 | 175.4 | 406 | 12.3% |
| Inquiry / Help | 182.1 | 182.7 | 20 | 15.0% |

**Software** resolves fastest on average (~154 hrs), while **Hardware** and **Inquiry/Help** are slowest (~181–182 hrs). However, Hardware dominates the dataset (81% of tickets), so overall metrics are heavily Hardware-driven. SLA compliance is uniformly poor across all categories (9–15%), with **Network** the worst and **Inquiry/Help** marginally the best — though sample sizes for non-Hardware categories are small (19–33 tickets), limiting confidence.

---

## 2. By Priority

| Priority | Mean Hrs | Median Hrs | N | SLA Met % | Very Slow % |
|---|---|---|---|---|---|
| 1 - Critical | 167.0 | 164.7 | 27 | **0.0%** | 100% |
| 2 - High | 180.0 | 176.6 | 394 | 11.7% | 86% |
| 3 - Moderate | 177.8 | 164.2 | 77 | 16.9% | 58% |
| 4 - Low | 32.6 | 32.6 | 2 | 100% | 0% |

**Critical incidents fail SLA 100% of the time** — a significant finding. Despite being highest priority, they do not resolve faster than High-priority tickets (167 hrs vs. 180 hrs mean), suggesting escalation does not translate to faster resolution. Moderate tickets have the best SLA compliance (16.9%) among meaningful-volume groups and a higher share of Fast/On-time resolutions. The 4 - Low data point (n=2, 100% SLA) is too sparse to generalize.

---

## 3. By Assignment Group

| Assignment Group | Mean Hrs | Median Hrs | N | SLA Met % |
|---|---|---|---|---|
| Software | 153.6 | 148.0 | 33 | 12.1% |
| Network | 161.6 | 161.1 | 23 | 8.7% |
| Service Desk | 176.4 | 179.5 | 19 | 15.8% |
| Database | 178.3 | 178.9 | 20 | 10.0% |
| Hardware | 181.5 | 175.6 | 405 | 12.3% |

Assignment groups closely mirror category groupings (tickets are largely routed by category). **Software** group leads in efficiency; **Hardware** group is the slowest and handles the vast majority of tickets. **Service Desk** achieves the highest SLA rate (15.8%) despite a slower mean resolution time, possibly indicating better SLA target calibration. **Network** has the lowest SLA compliance (8.7%) relative to its resolution speed.

---

## 4. Key Takeaways

- **Overall SLA compliance is critically low** (~12% system-wide), indicating systemic under-performance regardless of category, priority, or group.
- **Software/Network categories resolve faster** than Hardware/Inquiry, but the dataset is dominated by Hardware tickets.
- **Critical priority does not yield faster resolution** — a counterintuitive and operationally significant pattern worth investigating (possible triage or resource bottleneck).
- **Moderate priority incidents outperform Critical on both SLA and speed distribution**, suggesting prioritization workflows may need review.
- Non-Hardware categories have small sample sizes (≤33), so their averages carry **high uncertainty**.
