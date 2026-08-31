---
dataset: airlines_review
scenario: causal_qatar_business
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "non_recommendation_outcome"
query: "Explain why some Qatar Airways Business-Class flights receive a non-recommended (Recommended = no) result."
source_table: augment_table/airlines_review/causal_qatar_business/sonnet__skill_off_update.csv
generated_at: 2026-07-28T12:56:44.859329+00:00
wall_seconds: 44.47
---

# Why Some Qatar Airways Business-Class Flights Receive a Non-Recommended Result

## Dataset Overview

The dataset contains **592 Business-Class reviews** of Qatar Airways. Of these, **127 (21.5%) are marked "Recommended = no"** and 465 (78.5%) are "yes."

---

## Primary Driver: Value For Money

The single strongest differentiator between recommended and non-recommended reviews is **Value For Money** (VFM):

| Group | Mean VFM | Low_Value_For_Money flag rate |
|---|---|---|
| Recommended = no | **2.22 / 5** | **54%** |
| Recommended = yes | **4.29 / 5** | 5% |

More than half of all non-recommended reviews explicitly carry the `Low_Value_For_Money = yes` flag, and the mean VFM score (2.22) is less than half that of recommended reviews. In many cases passengers paid significant premiums (e.g., $2,300 upgrade fees mentioned in reviews) and felt the experience did not justify the cost.

---

## Secondary Driver: Overall Rating

Non-recommended reviews have a dramatically lower **Overall Rating** (mean **3.82**) versus recommended reviews (mean **8.43**). The distribution of non-recommended Overall Ratings is heavily skewed low: **68 of 127 (54%)** are rated ≤ 4 out of 10.

The `Overall_Vs_Service_Gap` column (Overall Rating minus Avg Service Rating) averages only **0.20** for non-recommended reviews, compared to **4.28** for recommended ones, meaning passengers gave holistic scores barely above their service sub-scores — the satisfaction gap that normally boosts the overall rating is absent.

---

## Contributing Factor: Operational Issues (Delays & Disruptions)

The `Mentions_Delay_Or_Disruption` flag is raised in **47%** of non-recommended reviews vs. **33%** in recommended ones. Operational failures (missed connections, long waits for aircraft steps, long bus transfers) appear to undermine the overall experience even when in-cabin service sub-ratings are adequate.

---

## Service Sub-Ratings: Less Differentiated

Interestingly, **service sub-ratings show smaller gaps** between recommended and non-recommended groups:

| Sub-rating | no (mean) | yes (mean) |
|---|---|---|
| Seat Comfort | 3.87 | 4.01 |
| Staff Service | 4.01 | 4.39 |
| Food & Beverages | 3.85 | 3.94 |
| Inflight Entertainment | 4.16 | 4.12 |

These differences are modest, suggesting that passengers who do not recommend Qatar Airways Business Class are **not primarily dissatisfied with in-cabin product quality** but rather with the overall value proposition and operational reliability.

---

## Edge Cases / Weak Evidence

- **43 non-recommended reviews** have an `Avg_Service_Rating ≥ 4.0`, yet still give a "no." Their mean VFM is 2.86 and mean Overall Rating is 4.65, reinforcing that value perception and operational problems — not just service quality — drive the negative recommendation.
- `Mentions_Price_Complaint` is moderately elevated (39% vs. 31%), providing additional weak corroborating evidence for cost-related dissatisfaction.
- `Mentions_Seat_Issue` and `Mentions_Service_Complaint` are **higher in the recommended group** than the non-recommended group, suggesting these flags are noisy and not reliable predictors of recommendation.

---

## Summary

Qatar Airways Business-Class flights receive a **non-recommended** verdict primarily because:

1. **Low perceived Value For Money** — the most discriminating factor (VFM mean 2.22 vs. 4.29; 54% Low_Value_For_Money flag rate).
2. **Low Overall Rating** — holistic dissatisfaction not fully explained by sub-ratings alone.
3. **Operational disruptions** — delays, long ground transfers, and logistical failures that erode the premium experience.

In-cabin product metrics (seat, food, entertainment, staff) play a secondary role and are insufficient on their own to explain non-recommendation.
