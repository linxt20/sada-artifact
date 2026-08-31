---
dataset: amazon_polarity_reviews
scenario: predictive_negative
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "label_pos"
query: "What review signals predict negative Amazon product satisfaction?"
source_table: augment_table/amazon_polarity_reviews/predictive_negative/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:08:54.093850+00:00
wall_seconds: 37.26
---

# Predicting Negative Amazon Product Satisfaction

**Dataset:** 250 reviews (125 negative `label_pos=0`, 125 positive `label_pos=1`), balanced split.

---

## Key Predictive Signals

### 1. Sentiment Intensity (Strongest Signal)

| Intensity | Positive Rate | N |
|-----------|--------------|---|
| 1 (lowest) | 0% | 61 |
| 2 | 0% | 51 |
| 3 | 55% | 22 |
| 4 | 95% | 37 |
| 5 (highest) | 99% | 79 |

**Sentiment intensity is the most discriminating single feature.** Scores of 1–2 perfectly predict negative satisfaction (n=112). Scores of 4–5 almost perfectly predict positive satisfaction. Score 3 is a transition zone. Practically, any review with intensity ≤ 2 can be flagged as negative with near-zero false positives.

---

### 2. Expectation Gap (Strong Signal)

| Expectation Gap | Positive Rate | N |
|----------------|--------------|---|
| `description_mismatch` | 0% | 5 |
| `Unknown` | 0% | 1 |
| `quality_below_expectations` | 4% | 114 |
| `not_present` | 33% | 3 |
| `met_expectations` | 93% | 106 |
| `better_than_expected` | 100% | 21 |

`quality_below_expectations` (n=114) is the single most common negative signal — 96% of such reviews are negative. `description_mismatch` is also a reliable negative predictor (0% positive, though small n=5). Conversely, `met_expectations` and `better_than_expected` almost exclusively map to positive reviews.

---

### 3. Defect Type (Moderate Signal — Many Reviews Lack This Label)

| Defect Type | Positive Rate | N |
|-------------|--------------|---|
| `accuracy_or_content_error` | 0% | 10 |
| `compatibility_issue` | 0% | 1 |
| `functional_failure` | 4% | 28 |
| `build_quality` | 10% | 10 |
| `design_flaw` | 22% | 9 |
| `missing_or_incomplete` | 17% | 6 |
| `not_present` | 65% | 186 |

When a defect type is explicitly tagged (i.e., not `not_present`), reviews are overwhelmingly negative. `accuracy_or_content_error` and `functional_failure` are the strongest defect-based negative signals. However, 186 of 250 reviews have `not_present` for this field, limiting its standalone utility.

---

### 4. Product Category (Weak–Moderate Signal)

| Category | Positive Rate | N |
|----------|--------------|---|
| `software_or_game` | 33% | 9 |
| `physical_product` | 36% | 80 |
| `media_film` | 44% | 9 |
| `media_book` | 52% | 83 |
| `consumable_or_food` | 67% | 9 |
| `media_music` | 73% | 40 |
| `apparel` | 100% | 3 |

Physical products and software tend toward negative reviews; music and apparel skew positive. These differences are partially confounded with category representation and small sample sizes for several categories (e.g., `apparel` n=3). This signal is weaker and less reliable standalone.

---

### 5. Reviewer Use Context (Weak Signal)

| Use Context | Positive Rate | N |
|-------------|--------------|---|
| `child_or_family` | 43% | 7 |
| `not_present` | 48% | 98 |
| `replacement_purchase` | 50% | 16 |
| `gift` | 57% | 7 |
| `personal_use` | 60% | 55 |
| `professional_or_work` | 83% | 6 |

Use context shows limited discriminative power and most categories have small or near-balanced counts. `professional_or_work` leans positive but n=6 is too small to rely on.

---

## Summary: Signal Priority

| Rank | Feature | Predictive Strength | Notes |
|------|---------|--------------------|----|
| 1 | `sentiment_intensity` | Very Strong | 1–2 → negative; 4–5 → positive |
| 2 | `expectation_gap` | Strong | `quality_below_expectations` drives most negatives |
| 3 | `defect_type` (when present) | Strong | But sparse (74% `not_present`) |
| 4 | `product_category_signal` | Weak–Moderate | Small n in some cells |
| 5 | `reviewer_use_context` | Weak | Near-chance in most categories |

---

## Exceptions & Caveats

- **Sentiment intensity 3** is a transition zone (55% positive) and not reliably predictive either way.
- **`defect_type = not_present`** still has 35% negative reviews — absence of a tagged defect does not mean satisfaction.
- **Several categories** (`apparel`, `consumable_or_food`, `software_or_game`) have very small samples (n < 10), making category-level conclusions tentative.
- The dataset is perfectly balanced (50/50), which may not reflect real-world Amazon review distributions.
