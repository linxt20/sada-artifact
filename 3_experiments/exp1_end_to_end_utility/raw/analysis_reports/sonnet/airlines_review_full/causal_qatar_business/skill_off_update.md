---
dataset: airlines_review_full
scenario: causal_qatar_business
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "non_recommendation_outcome"
query: "Explain why some Qatar Airways Business-Class flights receive a non-recommended (Recommended = no) result."
source_table: augment_table/airlines_review_full/causal_qatar_business/sonnet__skill_off_update.csv
generated_at: 2026-08-03T05:39:29.734401+00:00
wall_seconds: 41.82
---

# Why Some Qatar Airways Business-Class Flights Receive a Non-Recommended Result

## Overview

Of 592 Qatar Airways Business-Class reviews in this dataset, **127 (21.5%)** carry a `Recommended = no` result. The analysis below identifies the dominant drivers using the scored sub-categories, the `Non-Rec Risk Factors`, `Weakest Category`, and `Overall Rating Band` columns.

---

## 1. Primary Driver: Poor Value For Money

The single strongest separating factor between recommended and non-recommended reviews is the **Value For Money** score.

| Metric | Recommended = no | Recommended = yes |
|---|---|---|
| Mean Value For Money | **2.22** | 4.29 |
| `Value For Money Poor = yes` | **54% (69/127)** | 5% (25/465) |
| Weakest Category = Value For Money | **53% (67/127)** | — |

In the `Non-Rec Risk Factors` column, `poor_value_for_money` appears in **82 of 127** non-recommended reviews (65%), most often paired with `very_low_overall_rating`. Passengers paying premium Business-Class prices (sometimes referencing $1,500–$2,300 upgrades) felt they did not receive commensurate quality, particularly when hard-product issues arose mid-flight.

---

## 2. Secondary Driver: Low Overall Rating

Overall Rating collapses nearly all sub-category dissatisfaction into one signal:

| Overall Rating Band | Count (no rec) | % of non-rec |
|---|---|---|
| Low (1–4) | 68 | 54% |
| Medium (5–7) | 37 | 29% |
| High (8–10) | 22 | 17% |

Mean Overall Rating for non-recommended reviews is **3.8 vs. 8.4** for recommended. The `very_low_overall_rating` risk factor appears in **66 of 127** non-recommended cases (52%), making it the most frequently flagged individual factor.

---

## 3. Contributing Sub-Category Weaknesses

While Value For Money and Overall Rating dominate, service and product failures compound the outcome:

| Sub-category | Mean (no rec) | Mean (yes rec) | Gap |
|---|---|---|---|
| Staff Service | 4.01 | 4.39 | −0.38 |
| Seat Comfort | 3.87 | 4.01 | −0.14 |
| Food & Beverages | 3.85 | 3.94 | −0.09 |
| Inflight Entertainment | 4.16 | 4.12 | +0.04 |

**Seat Comfort** is the weakest category in 19 non-recommended reviews (15%) and **Food & Beverages** in 18 (14%), often appearing alongside Value For Money complaints in multi-factor risk combinations (e.g., `very_low_overall_rating;poor_value_for_money;poor_seat_comfort`). Hard-product failures (broken/reclining seats, poor seat comfort on long-haul flights) are specifically called out in review text.

---

## 4. Traveller Type Patterns

| Type of Traveller | Count (no rec) |
|---|---|
| Business | 46 (36%) |
| Solo Leisure | 41 (32%) |
| Couple Leisure | 30 (24%) |
| Family Leisure | 10 (8%) |

Business travellers are the largest non-recommending group, consistent with high expectations for reliability and value on premium fares.

---

## 5. Exceptions and Weak Evidence

- **22 non-recommended reviews (17%)** carry `Non-Rec Risk Factors = none`, yet still result in `Recommended = no`. These cases have mean Overall Rating of 6.5 and Value For Money of 3.4 — moderate scores suggesting a subjective threshold effect where passengers felt just dissatisfied enough to withhold recommendation despite no extreme failures.
- **Inflight Entertainment** shows virtually no gap between recommended and non-recommended groups and is rarely the weakest category, indicating it is not a causal factor.
- The high-rating-band non-recommended cases (22 reviews) suggest recommendation can sometimes be withheld even with good scores, likely driven by isolated incidents (e.g., billing disputes, ground experience issues) not fully captured in the numeric columns.

---

## Summary

Non-recommended outcomes in Qatar Airways Business Class are **primarily caused by poor perceived Value For Money** (mean score 2.2, flagged in 65% of cases), strongly amplified by **low Overall Ratings** (mean 3.8). Secondary contributors include staff service lapses and hard-product failures (seat comfort, food quality) on long-haul routes. These factors often co-occur, forming compound risk profiles that tip passengers from neutral to non-recommending despite Qatar Airways' generally high sub-category scores among satisfied customers.
