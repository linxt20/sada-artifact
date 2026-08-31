---
dataset: flag_12
scenario: concept_attribute_inefficiency
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "incident_inefficiency_reasons"
query: "What recurring issues drive resolution inefficiency?"
source_table: augment_table/flag_12/concept_attribute_inefficiency/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:09:56.405305+00:00
wall_seconds: 47.53
---

# Resolution Inefficiency Analysis — Skill-Off Variant

## Dataset Overview

- **500 incidents** spanning Jan–Mar 2023  
- Overall average resolution time: **178.40 hours (~7.4 days)**  
- **48.8%** of tickets exceed average resolution time (`above_avg_resolution = 1`)  
- **70.2%** of tickets are repeat issues (`is_repeat_issue = 1`)

---

## Key Drivers of Resolution Inefficiency

### 1. Dominant Issue Type: Printers (Hardware)

Printer incidents account for **203 of 500 tickets (40.6%)** — by far the largest single issue type. Of those, **96% are repeat issues**, meaning the same printer problems recur without durable fixes. Despite this high repeat rate, **50.2%** still exceed average resolution time, indicating that repeat exposure is not translating into faster resolution. This suggests a skill or process gap specific to printer support under the skill-off condition.

### 2. High Repeat Rate Across the Board

The overall repeat issue rate of **70.2%** is the single most striking structural driver of inefficiency. Recurrence means the same problems consume agent time repeatedly without root-cause closure. Issue types with the highest combination of repeat rate **and** above-average resolution burden:

| Issue Type        | Tickets | Repeat Rate | Above-Avg Resolution |
|-------------------|---------|-------------|----------------------|
| Printer           | 203     | 96.1%       | 50.2%                |
| Monitor/Display   | 71      | 67.6%       | 46.5%                |
| Keyboard          | 56      | 60.7%       | 50.0%                |
| Hardware Failure  | 30      | 46.7%       | 56.7%                |
| Database          | 19      | 26.3%       | 57.9%                |

### 3. Hardware Failures and Database Issues: Low Volume, High Inefficiency

Despite relatively low ticket counts, **hardware failure (56.7% above-avg)** and **database (57.9% above-avg)** issues have the highest rates of above-average resolution time. These likely require specialized skills that are absent or constrained under the skill-off setting, causing disproportionate delays.

### 4. Agent-Level Skill Gaps (Luke Wilson)

Among assigned agents, **Luke Wilson** stands out with the highest average resolution time (**195.5 hours**) and the highest above-average rate (**54.3%**), handling 116 tickets. This is notably worse than Beth Anglin (avg 172.4 hrs, 44.7% above-avg). Under a skill-off scenario, agent capability variance likely amplifies resolution delays.

### 5. Priority Does Not Effectively Triage Resolution

Counter-intuitively, **1-Critical tickets resolve faster** (avg 167 hrs, 40.7% above-avg) than **2-High tickets** (avg 180 hrs, 50.5% above-avg), which dominate volume (394 tickets). This suggests priority labeling is not driving appropriate escalation or resource allocation for the bulk of incidents.

---

## Exceptions and Weak Evidence

- **Software category** shows the lowest above-avg resolution rate (45.5%) and fastest average resolution (153.6 hrs), suggesting it is handled more effectively even under skill-off conditions.
- Repeat issues do **not** meaningfully correlate with longer resolution times in this dataset (repeat avg: 176.6 hrs vs. non-repeat: 182.6 hrs), implying that recurrence per se does not slow individual ticket resolution — the inefficiency lies in the *volume* of repeated work, not per-incident slowdown.
- Evidence for skill-off impact is structural (agent variance, issue-type concentration) rather than directly observable from a single column.

---

## Summary

Resolution inefficiency is primarily driven by: **(1)** chronic recurrence of printer and hardware issues without root-cause resolution, **(2)** high above-average resolution rates for complex issue types (hardware failure, database) that demand specialized skills absent under skill-off conditions, and **(3)** agent-level performance gaps, particularly Luke Wilson's caseload. Addressing durable fixes for printer/hardware issues and improving skill coverage for database and hardware failure tickets would most directly reduce resolution inefficiency.
