---
dataset: education_survey_responses
scenario: causal_low_satisfaction
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "satisfaction_1to5"
query: "Why is learning satisfaction low for certain groups, and which factors drive it?"
source_table: augment_table/education_survey_responses/causal_low_satisfaction/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:07:15.364990+00:00
wall_seconds: 62.22
---

# Learning Satisfaction Analysis: Drivers of Low Satisfaction

## Overview

The dataset contains 250 survey responses from Students, Teachers, and Parents across grade levels (K–5, 6–8, 9–12) and five subjects. Overall mean satisfaction is **3.14 / 5**, with **74 respondents (30%)** flagged as low satisfaction (scores 1–2).

---

## Key Finding: Clarity Is the Strongest Driver of Low Satisfaction

When `primary_driver` is **clarity**, average satisfaction drops to **2.43** — the lowest of any driver category. Among the 74 low-satisfaction respondents, clarity is the most frequently cited driver (17 cases, ~23%), closely followed by technology (16) and engagement (14).

| Primary Driver | Avg. Satisfaction | Low-Sat Flag Rate |
|----------------|:-----------------:|:-----------------:|
| clarity        | 2.43              | highest impact    |
| engagement     | 3.11              | moderate          |
| none           | 3.23              | baseline          |
| technology     | 3.32              | moderate          |
| workload       | 3.43              | lower impact      |

Compared to the high/medium-satisfaction group, low-satisfaction respondents show **elevated clarity mentions (0.35 vs. 0.21)** — the largest divergence of any factor — confirming clarity as the primary differentiator.

---

## Factor Mention Comparison: Low vs. High Satisfaction Groups

| Factor | Low-Sat Mean | High/Med Mean | Δ |
|--------|:------------:|:-------------:|:---:|
| clarity_mentions | **0.351** | 0.205 | +0.146 |
| engagement_mentions | 0.311 | 0.364 | −0.053 |
| tech_issue_mentions | 0.338 | 0.364 | −0.026 |
| workload_mentions | 0.162 | 0.119 | +0.043 |

> **Notable exception:** Technology issues are actually mentioned *slightly more* in the high/medium-satisfaction group than in the low-satisfaction group. This suggests that technology problems alone do not reliably drive low satisfaction — context (e.g., whether the lesson recovers) may matter more.

---

## Groups Most Affected

### By Subject
Math (34%) and Arts (33%) have the highest low-satisfaction flag rates, while Science (25%) has the lowest.

| Subject | Low-Sat Flag Rate |
|---------|:-----------------:|
| Math    | 34%               |
| Arts    | 33%               |
| English | 28%               |
| History | 28%               |
| Science | 25%               |

### By Grade Level
K–5 Parents (36%) and 9–12 Teachers (32%) and Students (32%) show elevated low-satisfaction rates. K–5 parents likely reflect difficulties young children face with online clarity and platform usability.

### By Role
Low-satisfaction rates are nearly uniform across Students (30%), Teachers (30%), and Parents (29%), indicating this is a systemic issue rather than role-specific.

---

## Summary of Causal Factors

1. **Clarity** — The single strongest driver of low satisfaction. When learners or observers report that instruction is hard to follow (confusing explanations, poor lesson structure), satisfaction scores fall sharply to ~2.4.
2. **Engagement** — A secondary driver; disengaged students correlate with lower satisfaction, though the mention gap is smaller than clarity.
3. **Technology** — Widely mentioned overall but not a reliable predictor of *low* satisfaction on its own; it likely amplifies other problems (e.g., a clarity issue worsened by camera freeze, as in ED-0001).
4. **Workload** — Weakest driver; elevated slightly in low-satisfaction group but accounts for only 3 of 74 low-satisfaction primary drivers.

---

## Caveats

- 24 of 74 low-satisfaction respondents have `primary_driver = none`, meaning the open-text responses did not surface a clear single cause — these may reflect compound or unmeasured factors.
- The dataset is observational; causal direction (e.g., whether poor clarity causes disengagement or vice versa) cannot be definitively established.
- Subject-level and grade-level differences are modest and should be interpreted with caution given cell sizes (~50 responses per subject).
