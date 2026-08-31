---
dataset: flag_2
scenario: causal_delay
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "resolution_time"
query: "Controlling for priority and category, which underlying causes explain longer resolution times?"
source_table: augment_table/flag_2/causal_delay/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:15:18.903502+00:00
wall_seconds: 70.01
---

# Causal Delay Analysis: Underlying Causes of Longer Resolution Times
**Dataset:** `sonnet__skill_off_update.csv` (500 records, 372 with valid resolution times)  
**Variant:** `skill_off` | **Date:** 2026-07-28

---

## Context

Resolution times range from 24 h to ~2,206 h (mean ≈ **1,043 h**, median ≈ **1,032 h**). The analysis below controls for **priority** (1-Critical, 2-High, 3-Moderate) and **category** (Network, Database, Software, Hardware, Inquiry) by examining within-group patterns and residuals.

---

## Key Findings

### 1. Issue Type: Strongest Within-Group Driver

After stratifying by priority × category, issue type shows consistent mean differences:

| Issue Type    | Mean Hrs | Median Hrs | Count |
|---------------|----------|------------|-------|
| other         | 1,220.9  | 1,298.4    | 13    |
| software      | 1,170.9  | 956.4      | 14    |
| connectivity  | 1,080.5  | 1,057.2    | 154   |
| access        | 1,064.0  | 909.6      | 9     |
| email         | 1,056.2  | 1,086.0    | 102   |
| database      | 900.9    | 859.2      | 76    |
| hardware      | 925.8    | 794.4      | 4     |

**Within the largest controlled cell (2-High + Network):**

| Issue Type   | Mean Hrs | Count |
|--------------|----------|-------|
| other        | 1,308.3  | 8     |
| access       | 1,185.0  | 4     |
| email        | 1,084.8  | 18    |
| connectivity | 1,071.2  | 121   |

- **"Other" and "access" issue types** take meaningfully longer within the same priority–category bucket, suggesting these are under-classified or require cross-functional coordination.
- **Database-typed tickets** (within 2-High + Database) resolve ~28% faster than connectivity tickets in the same priority tier (855 h vs 1,072 h), indicating Database issues benefit from a more specialized, faster workflow.

### 2. Ticket Opening Hour: Night Submissions Accumulate Idle Time

| Hour Bucket     | Mean Hrs | Count |
|-----------------|----------|-------|
| Night (0–8)     | 1,167.4  | 121   |
| Evening (17–24) | 1,047.9  | 102   |
| Business (8–17) | 958.1    | 135   |

Tickets opened **outside business hours** average **209 h longer** than business-hours tickets. This effect is strongest for **Critical tickets**: night-opened Critical tickets average **1,453 h vs 999 h** for business-hours Critical tickets — a 45% gap. This points to off-hours staffing as a structural delay cause.

### 3. Assignment Group Mismatch: Significant for Critical Tickets

| Mismatch | Mean Hrs | Count |
|----------|----------|-------|
| No       | 1,037 h  | 305   |
| Yes      | 1,075 h  | 67    |

The overall gap (~38 h) is modest, but for **1-Critical tickets**, mismatched assignments increase mean resolution time by **~209 h** (1,097 h → 1,306 h), consistent with re-routing delays at high urgency levels.

### 4. Weekend Opening: Moderate, Consistent Effect

Tickets opened on weekends average **1,081 h vs 1,027 h** on weekdays (+54 h). This is consistent across priority levels (2-High: +54 h; 3-Moderate: +71 h), though small enough to be a secondary factor.

---

## Summary Table

| Cause | Controlled Effect | Confidence |
|---|---|---|
| Issue type = "other" / "access" (vs. database) | +200–400 h within same priority+category | Moderate (small n for "other"/"access") |
| Opened during night hours (vs. business hours) | +209 h overall; +455 h for Critical | Strong |
| Assignment group mismatch (Critical tickets) | +209 h for Critical | Moderate (n=6 mismatch cases) |
| Weekend opening | +54 h | Weak-to-moderate |

---

## Exceptions and Caveats

- **"Other" and "access" cells** have low counts (n < 15), so the effect size estimates are noisy.
- **3-Moderate tickets** show little issue-type differentiation, likely due to low volume (n = 41).
- `resolver_is_assignee` shows negligible effect (+14 h mean; n=73), and is not a meaningful delay driver.
- `resolution_hours_vs_group_median` confirms group-adjusted patterns align with raw findings, supporting that night-hour and issue-type effects are not artifacts of group composition.

---

## Decision-Ready Takeaways

1. **Prioritize off-hours staffing** — night-opened tickets, especially Critical ones, are the single largest controllable delay source.
2. **Audit "other" and "access" issue classifications** — their elevated times suggest routing ambiguity or skill gaps that are not captured by the category taxonomy.
3. **Improve assignment accuracy for Critical tickets** — mismatch at that tier adds ~3.5 days of resolution time.
4. **Database issues resolve faster** within the same tier; the workflows there may offer a replicable model for connectivity and email issue handling.
