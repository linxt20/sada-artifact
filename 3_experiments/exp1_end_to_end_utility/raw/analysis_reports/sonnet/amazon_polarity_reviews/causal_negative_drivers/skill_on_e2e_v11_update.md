---
dataset: amazon_polarity_reviews
scenario: causal_negative_drivers
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "label_pos"
query: "Why do some Amazon products receive predominantly negative reviews, and which factors contribute the most?"
source_table: augment_table/amazon_polarity_reviews/causal_negative_drivers/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:09:06.527760+00:00
wall_seconds: 63.58
---

# Causal Negative Drivers in Amazon Polarity Reviews

## Executive Summary

Across 250 balanced reviews (125 negative, 125 positive), two dominant causal mechanisms explain negative ratings: **product performance gaps** (product falls short of stated specifications or functional expectations) and **reviewer expectation mismatches** (the reviewer brought expectations the product was never designed to meet). These two mechanisms account for 84% of negative reviews that have a TAPP-identified driver. Product category is the strongest structural predictor: electronics and toys attract negative reviews at rates above 75%, while media and apparel skew positive.

---

## Method Note

TAPP-generated columns used in this analysis:
- `performance_gap_type` — classifies the type of functional shortfall (e.g., `below_spec`, `poor_ergonomics`, `insufficient_capacity`, `limited_compatibility`)
- `product_category` — assigns the review to a product domain
- `reviewer_expectation_mismatch` — identifies whether and how reviewer expectations diverged from product scope (e.g., `genre_expectation`, `price_value_mismatch`, `brand_reputation`, `sequel_or_series_comparison`)
- `complaint_specificity` — ordinal score (1–3) for how concrete/specific the complaint is (coverage: 135/250 rows; 115 missing)

These columns supplement the original structured fields: `review_id`, `label_pos` (0 = negative, 1 = positive), `title`, and `content`.

---

## 1. Outcome Variable: Negative Review Rate

The dataset is balanced: 125 negative (`label_pos=0`) and 125 positive (`label_pos=1`) reviews. The analysis below identifies which factors are disproportionately concentrated in the negative half.

---

## 2. Product Category: Strongest Structural Driver

| Product Category | Neg | Pos | Neg Rate |
|---|---|---|---|
| electronics_hardware | 22 | 6 | **78.6%** |
| toy_game | 9 | 2 | **81.8%** |
| household_appliance | 8 | 3 | **72.7%** |
| sporting_fitness | 3 | 1 | 75.0% |
| media_film | 19 | 15 | 55.9% |
| media_book | 40 | 43 | 48.2% |
| other | 11 | 18 | 37.9% |
| media_music | 11 | 29 | **27.5%** |
| apparel_accessories | 0 | 6 | **0%** |

**Key finding:** Tangible, functional products (electronics, toys, appliances) have negative rates of 73–82%. Media products split closer to 50/50, with music skewing positive. Apparel has zero negative reviews in this sample. This pattern suggests that products with measurable performance thresholds attract more negative reviews when they fail to meet expectations, while subjective/taste-based media is more evenly polarized.

---

## 3. Performance Gap (`performance_gap_type`): Strongest TAPP Predictor

| Gap Type | Total | Neg | Neg Rate |
|---|---|---|---|
| `below_spec` | 44 | 43 | **97.7%** |
| `insufficient_capacity` | 3 | 3 | 100% |
| `poor_ergonomics` | 4 | 3 | 75.0% |
| `limited_compatibility` | 3 | 2 | 66.7% |
| `not_present` | 196 | 74 | 37.8% |

`below_spec` is the single most discriminating TAPP signal: 43 of 44 reviews tagged with it are negative (97.7%). Among the 125 negative reviews, 51 (40.8%) carry at least one performance gap type. This signal is concentrated in electronics, appliances, and toys — consistent with the category analysis above.

---

## 4. Expectation Mismatch (`reviewer_expectation_mismatch`): Secondary Driver

| Mismatch Type | Neg | Pos | Neg Share among labeled |
|---|---|---|---|
| `genre_expectation` | 32 | 7 | 82.1% |
| `brand_reputation` | 13 | 0 | **100%** |
| `price_value_mismatch` | 15 | 4 | 78.9% |
| `sequel_or_series_comparison` | 19 | 17 | 52.9% |
| `not_present` | 46 | 97 | 32.2% |

`brand_reputation` mismatches are exclusively negative (13/13), suggesting that when reviewers cite brand expectations not met, they always leave negative reviews. `genre_expectation` (32 negative) is the highest-volume driver, particularly concentrated in `media_book` (where 40 of 83 book reviews are negative) — readers who expected a different style or topic. `price_value_mismatch` (15 negative) appears across categories.

Among the 125 negative reviews:
- 51 have a performance gap (not_present = 74; gap present = 51)
- 79 have an expectation mismatch (not_present = 46; mismatch present = 79)
- 24 have **both** — compounding effect
- Only 19 negative reviews (15%) have neither signal, meaning unexplained by these two facets

---

## 5. Complaint Specificity (`complaint_specificity`): Directional but Partial Coverage

This column covers only 135 of 250 rows (115 missing), limiting its reliability. Among the covered rows:

| Specificity | Neg | Pos |
|---|---|---|
| 1 (vague) | 11 | 1 |
| 2 (moderate) | 49 | 14 |
| 3 (specific) | 57 | 3 |

Higher specificity is associated with negative reviews — reviewers who are more specific tend to be dissatisfied and itemizing failures. However, given the 46% missing rate, this should be treated as directional rather than conclusive.

---

## 6. Synthesis: Causal Negative Review Framework

```
Negative Reviews (n=125)
├── Performance Gap Present (40.8%, n=51)
│   ├── below_spec (n=43): product fails stated capabilities → electronics/appliances
│   ├── poor_ergonomics (n=3): usability failures
│   └── capacity/compatibility (n=5): functional limitations
├── Expectation Mismatch Only, No Gap (44.0%, n=55)
│   ├── genre_expectation (n=32): wrong tone/style in media
│   ├── price_value_mismatch (n=15): cost not justified
│   └── brand_reputation (n=13): brand credibility breach
├── Both Gap + Mismatch (19.2%, n=24): compounding failures
└── Neither signal (15.2%, n=19): tone/style/personal taste
```

---

## 7. Key Conclusions

1. **Product category is the top structural driver.** Electronics, toys, and appliances receive negative reviews at 73–82% rates, vs. 28–55% for media.
2. **`below_spec` performance gaps are the most reliable causal signal** (97.7% negative rate). When a product demonstrably fails its specifications, a negative review is almost certain.
3. **Expectation mismatches explain the majority of media-product negatives.** `genre_expectation` (82% negative) and `brand_reputation` (100% negative) are high-precision drivers concentrated in books, music, and film.
4. **`price_value_mismatch`** surfaces across categories (15 negative reviews, 79% negative rate) and represents a cross-cutting driver not captured by category alone.
5. **Complaint specificity** directionally confirms dissatisfied reviewers are more detailed (score 3 dominates negatives), but the 46% missing rate limits quantitative weight.
