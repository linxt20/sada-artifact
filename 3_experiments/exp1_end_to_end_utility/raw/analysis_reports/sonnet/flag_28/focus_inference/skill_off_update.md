---
dataset: flag_28
scenario: focus_inference
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's worth attention in these goal records."
source_table: augment_table/flag_28/focus_inference/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:19:59.994058+00:00
wall_seconds: 74.4
---

# Goal Records: What's Worth Attention

## Overview

The dataset contains **550 goal records** across four departments (Marketing, HR, IT, Finance) with four tracking metrics (Employee Turnover Rate, Expense Ratio, Sales Increase, Survey Score). The `attention_flag` column is the primary triage signal: **260 goals (47%) are flagged "Needs Attention"**, 266 (48%) are "On Track", and 24 (4%) are Cancelled.

---

## 1. Scale of the Attention Problem

| Attention Flag | Count | Share |
|---|---|---|
| On Track | 266 | 48% |
| Needs Attention | 260 | 47% |
| Cancelled | 24 | 4% |

Nearly half of all active goals are underperforming. The `is_overdue` flag maps perfectly onto `Needs Attention` — every overdue goal carries a "Needs Attention" flag, and zero overdue goals show "On Track" — confirming that deadline overrun is the direct driver of the flag.

---

## 2. Completion Gap: How Far Behind Are Struggling Goals?

`completion_gap = percent_complete − target_percentage`

- **Overall mean gap:** −23.9 percentage points (the average goal is well below its target)
- **"Needs Attention" mean gap:** −35.3 pp, with `percent_complete` averaging only **42.7%**
- **"On Track" goals** all have non-negative gaps, meaning they have met or exceeded their targets at completion

The worst individual gaps reach −97 pp (goals barely started against high targets). Ten of the worst-performing goals have `percent_complete` ≤ 14, yet remain "In Progress" or "Planned".

---

## 3. Priority Paradox: Low- and Medium-Priority Goals Drive Most Failures

Counter-intuitively, **Critical- and High-priority goals perform best**:

| Priority | Avg Completion Gap |
|---|---|
| Critical | +2.6 pp |
| High | +0.1 pp |
| Medium | −36.2 pp |
| Low | −37.3 pp |

Among the 260 "Needs Attention" goals:
- Medium: 112 (43%)
- Low: 97 (37%)
- High: 26 (10%)
- Critical: 25 (10%)

**Critical goals flagged "Needs Attention": 25** — these are the highest-urgency intervention targets, as they combine organizational priority with underperformance.

---

## 4. Department Performance

IT stands out with the best average completion gap (−4.2 pp), while Marketing and HR lag furthest behind:

| Department | Avg Completion Gap |
|---|---|
| IT | −4.2 pp |
| Finance | −28.0 pp |
| HR | −29.9 pp |
| Marketing | −31.8 pp |

Marketing also holds the largest goal count (148), making its underperformance the single largest volume risk.

---

## 5. Category Distribution: No Clear Hotspot, But Revenue Growth Tops Failures

All five categories contribute roughly equally to "Needs Attention" flags (46–57 goals each). Revenue Growth leads slightly with 57 flagged goals, suggesting it may be systematically over-ambitious relative to execution capacity.

---

## 6. Data Quality: Negative Duration Days

**82 records (15%) have negative `duration_days`** (end_date before start_date). These include 26 that are still "In Progress" and 8 "Planned". This is a structural data-quality issue: goals with impossible date ranges cannot be reliably tracked for overdue status and should be audited before relying on `is_overdue` for those records. Forty-five completed goals also have negative durations, suggesting retroactive date entry or data entry errors.

---

## 7. Target Ambition vs. Execution

- Mean `target_percentage`: **74.8%** — goals are set to ambitious levels on average
- Most goals in descriptions reference a **20% improvement** target as a standard
- The broad gap between target ambition (high) and `percent_complete` (mean 50.8%) across the full portfolio points to systemic execution risk, not just isolated failures

---

## Key Takeaways for Decision-Makers

1. **47% of goals need attention** — this is not a tail problem; it is a portfolio-wide execution issue
2. **Prioritize the 25 Critical + "Needs Attention" goals** immediately — high urgency, confirmed underperformance
3. **Marketing and HR departments** have the worst completion gaps at scale; department-level interventions are warranted
4. **Low/Medium-priority goals are falling through the cracks** — oversight mechanisms appear to focus on Critical/High, leaving the majority underserved
5. **82 records with negative duration days** require date-field correction before automated overdue tracking can be trusted
