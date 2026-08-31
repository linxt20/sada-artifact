---
dataset: amazon_fine_food_review
scenario: causal_low_score_attribution
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "low_review_score"
query: "What factors explain low review scores?"
source_table: augment_table/amazon_fine_food_review/causal_low_score_attribution/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:08:06.996129+00:00
wall_seconds: 46.26
---

# Low Review Score Attribution — Amazon Fine Food Reviews

## Dataset Overview

- **Total reviews:** 10,000
- **Low scores (1–2):** 1,522 (15.2%)
- **High scores (4–5):** 7,616 (76.2%)
- **Engineered columns:** `product_consistency_change` (bool), `product_category`

---

## Key Factors Explaining Low Scores

### 1. Product Consistency Change (Strongest Signal)

`product_consistency_change` is the single most discriminating variable.

| Group | Low-Score Rate (1–2) | High-Score Rate (4–5) |
|---|---|---|
| `product_consistency_change = True` | **52.6%** | 31.1% |
| `product_consistency_change = False` | 14.5% | 77.1% |

When a product undergoes a consistency change (e.g., reformulation, labeling discrepancy), the probability of a low score increases by **~3.6×**. This is the clearest causal lever in the data. Only 196 of 10,000 reviews (2%) involve this flag, but its effect is large.

---

### 2. Product Category

Low-score rates vary substantially across categories:

| Product Category | Total Reviews | Low-Score Rate |
|---|---|---|
| `canned_soup_seafood` | 242 | **22.7%** |
| `other` | 1,132 | 18.8% |
| `baby_food_formula` | 401 | 17.7% |
| `beverage_other` | 794 | 16.6% |
| `pet_food_treat` | 812 | 15.8% |
| `coffee_kcup_tea` | 2,732 | 15.6% |
| `snack_chip_baked` | 2,734 | 13.8% |
| `health_supplement` | 452 | 13.1% |
| `condiment_sauce` | 701 | **8.6%** |

`canned_soup_seafood` and `baby_food_formula` show the highest dissatisfaction rates. `condiment_sauce` reviews are notably more positive (mean score 4.51 vs. dataset mean ~4.1). Category reflects different quality expectations and product reliability.

---

### 3. Review Engagement (Helpfulness Votes)

Low-score reviews attract more votes from other customers:

- **Mean helpfulness denominator — Low scores:** 3.4 votes
- **Mean helpfulness denominator — High scores:** 1.7 votes

Negative reviews tend to be more extensively validated by other buyers, suggesting they describe widely shared experiences rather than outlier complaints.

---

### 4. Review Text Length

Low-score reviews are longer on average:

- **Mean text length — Low scores:** ~475 characters
- **Mean text length — High scores:** ~394 characters

Dissatisfied reviewers write more, consistent with the motivation to detail problems (e.g., mislabeling, taste degradation, packaging failures).

---

### 5. Qualitative Themes in Low-Score Summaries

The most frequent low-score summary terms include: *Disappointed, Awful, Horrible, Waste of money, Disgusting, Yuck, Not as Advertised*. The "Not as Advertised" theme directly mirrors the `product_consistency_change` signal — product descriptions not matching received items is a recurring complaint driver.

---

## Exceptions and Weak Evidence

- `product_consistency_change = True` still has **21% five-star reviews**, so consistency changes do not uniformly cause dissatisfaction (e.g., some changes may be improvements).
- Category effects may partly reflect sample size differences or platform listing quality rather than intrinsic product issues.
- No direct rating-over-time trend was analyzed; temporal drift could be a confound.

---

## Summary

| Factor | Strength | Direction |
|---|---|---|
| `product_consistency_change = True` | Strong | ↑ Low scores |
| Category: `canned_soup_seafood`, `baby_food_formula` | Moderate | ↑ Low scores |
| Category: `condiment_sauce` | Moderate | ↓ Low scores |
| Higher helpfulness votes | Moderate | Associated with low scores |
| Longer review text | Weak–Moderate | Associated with low scores |

**Product consistency change is the primary explainable causal factor for low scores.** Category is a secondary structural predictor. Review engagement and length are correlates rather than causes.
