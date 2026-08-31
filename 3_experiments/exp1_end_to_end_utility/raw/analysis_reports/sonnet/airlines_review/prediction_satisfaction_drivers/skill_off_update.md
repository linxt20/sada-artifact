---
dataset: airlines_review
scenario: prediction_satisfaction_drivers
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating"
query: "What drives customer satisfaction (Overall Rating) across the different airlines?"
source_table: augment_table/airlines_review/prediction_satisfaction_drivers/sonnet__skill_off_update.csv
generated_at: 2026-07-28T12:58:58.014045+00:00
wall_seconds: 57.27
---

# Customer Satisfaction Drivers — Airlines Review Analysis

**Dataset:** 900 reviews · 5 sub-rating dimensions · augmented features  
**Focus variable:** Overall Rating (1–10, mean = 5.66, median = 6)

---

## 1. Dominant Driver: Value For Money

**Value For Money is by far the strongest predictor of Overall Rating** (correlation = **0.88** across the full dataset). This holds across every cabin class:

| Class | VFM ↔ Overall Rating | 2nd-ranked driver |
|---|---|---|
| Economy | 0.89 | Staff Service (0.24) |
| Premium Economy | 0.93 | Food & Beverages (0.42) |
| Business | 0.81 | Seat Comfort (0.18) |
| First | 0.71 | Food & Beverages (0.25) |

The class-adjusted VFM metric (`Value_For_Money_Class_Adjusted`) also correlates at **0.83**, confirming the pattern persists even after accounting for cabin-level expectations.

Sub-rating comparison reinforces this: highly satisfied passengers (Overall ≥ 7) rate VFM at **4.41/5**, while dissatisfied passengers (Overall ≤ 3) rate it at only **1.50/5** — the widest absolute gap of any dimension.

---

## 2. Secondary Drivers: Staff Service & Seat Comfort

After Value For Money, **Staff Service** (r = 0.21) and **Seat Comfort** (r = 0.20) are the next most correlated dimensions — essentially tied. Food & Beverages (0.13) and Inflight Entertainment (0.09) contribute less to overall scores.

This ranking is echoed in the **Pain Point** and **Delight Driver** frequencies:

| Dimension | Pain Point count | Delight Driver count |
|---|---|---|
| Seat Comfort | 275 | 339 |
| Staff Service | 184 | 268 |
| Food & Beverages | 164 | 130 |
| Value For Money | 170 | 50 |
| Inflight Entertainment | 107 | 113 |

Seat Comfort and Staff Service are both the **most praised and most complained-about** dimensions, indicating high variance in delivery — and thus high leverage for satisfaction improvement.

---

## 3. Satisfaction Gap as a Summary Signal

The engineered `Satisfaction_Gap` (Overall Rating minus Avg Sub-Rating) correlates at **0.89** with Overall Rating. Passengers in the top quartile of Satisfaction Gap average **9.3/10** overall; those in the bottom quartile average **1.7/10**. This confirms that when overall perception exceeds the average of individual sub-ratings, it signals a holistic positive experience beyond measurable attributes.

Higher `Sub_Rating_Variance` (r = −0.29 with Overall Rating) also suggests that **inconsistency across dimensions hurts satisfaction** — a weak link in one area drags the overall score down.

---

## 4. Cabin Class & Traveller Type Effects

- **Business Class** passengers rate highest on average (6.78 vs 5.24 for Economy), but the VFM correlation is still the dominant driver even at this tier.
- **Solo Leisure** travellers report the highest average satisfaction (6.03); **Family Leisure** the lowest (5.17).
- **Service Tier** (High/Medium/Low) tracks strongly with ratings: High → 6.49, Low → 3.98.

---

## 5. Recommendation Threshold

The "Recommended: yes" rate jumps from **1.5%** (Overall 1–3) to **97.5%** (Overall 7–10), confirming that the rating scale above 7 constitutes a genuine advocacy threshold, not just a neutral response.

---

## Key Takeaways

1. **Value For Money is the single greatest driver of satisfaction** across all cabin classes — perceived price-to-quality ratio should be the primary improvement lever.
2. **Seat Comfort and Staff Service** are high-variance dimensions that swing passengers between pain and delight; their wide spread makes them critical operational targets.
3. **Inflight Entertainment** has the weakest correlation with Overall Rating and ranks lowest as a delight driver — investment here has diminishing satisfaction returns.
4. **Consistency matters**: high sub-rating variance is associated with lower overall scores, even when some individual dimensions score well.
5. **Caution:** there is no explicit airline identifier in the dataset, so airline-level comparisons rely on inferred groupings (Class, Route origin, Service Tier) rather than direct airline labels.
