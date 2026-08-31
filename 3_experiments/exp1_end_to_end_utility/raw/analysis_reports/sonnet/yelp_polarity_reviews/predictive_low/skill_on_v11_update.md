---
dataset: yelp_polarity_reviews
scenario: predictive_low
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "label_pos"
query: "What review signals predict low Yelp user satisfaction?"
source_table: augment_table/yelp_polarity_reviews/predictive_low/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:24:06.970913+00:00
wall_seconds: 37.89
---

# Review Signals Predicting Low Yelp User Satisfaction

**Dataset:** `yelp_polarity_reviews / predictive_low` — 250 reviews, balanced (125 negative `label_pos=0`, 125 positive `label_pos=1`)

---

## Key Predictive Signals

### 1. Service Failure Type

| Failure Type | % Negative Reviews |
|---|---|
| `ignored_forgotten` | **100%** |
| `rude_dismissal` | **100%** |
| `wrong_order_handling` | 80% |
| `slow_inattentive` | 84% |
| `not_present` | 37% |

Any coded service failure is a near-certain predictor of low satisfaction. Reviews with no failure coded (`not_present`) are still majority-positive (63%), but 37% of them are still negative — suggesting other signals matter when explicit failures are absent.

---

### 2. Staff Conduct

| Staff Conduct | % Negative Reviews |
|---|---|
| `hostile_abusive` | **100%** |
| `rude_condescending` | **96%** |
| `neutral` | 53% |
| `not_present` | 36% |
| `professional_friendly` | **12%** |

Staff conduct is the strongest single predictor. `rude_condescending` or `hostile_abusive` conduct almost perfectly classifies a review as negative. `professional_friendly` is a strong positive signal (88% positive reviews).

---

### 3. Complaint Intensity

Among the subset of reviews with a coded `complaint_intensity` score (n=147):

- **Negative reviews** mean intensity: **3.4** (median 3.0)
- **Positive reviews** mean intensity: **1.9** (median 2.0)

High intensity scores (4–5) cluster overwhelmingly in negative reviews (43 of 59 intensity-4 reviews are negative; 16 of 17 intensity-5 are negative). Scores of 1–2 appear mainly in positive reviews.

> **Note:** 103 of 250 reviews have no `complaint_intensity` value (mostly positive reviews), which limits this signal's standalone coverage but strengthens it as a conditional predictor.

---

### 4. Return Intent

| Return Intent | % Negative Reviews |
|---|---|
| `will_not_return` | **100%** |
| `not_stated` | 49% |
| `neutral_or_conditional` | 33% |
| `will_return_positive` | **6%** |

`will_not_return` is a perfect retroactive marker of dissatisfaction. However, 175 of 250 reviews (70%) are coded `not_stated`, limiting this signal's practical predictive reach — it's highly specific but not sensitive.

---

## Summary of Decision Rules

| Signal | Strength | Direction |
|---|---|---|
| Staff conduct = `rude_condescending` / `hostile_abusive` | Very Strong | → Low satisfaction |
| Any service failure type present | Very Strong | → Low satisfaction |
| Return intent = `will_not_return` | Very Strong (low coverage) | → Low satisfaction |
| Complaint intensity ≥ 4 | Strong (conditional) | → Low satisfaction |
| Staff conduct = `professional_friendly` | Strong | → High satisfaction |
| Return intent = `will_return_positive` | Strong (low coverage) | → High satisfaction |

---

## Caveats & Weak Evidence

- **`neutral` staff conduct** is ambiguous: 53% negative, nearly a coin flip — it adds little predictive value on its own.
- **`not_stated` return intent** (the majority class) is nearly uninformative (49% negative).
- Complaint intensity is **missing for ~41% of rows**, and when present it skews toward negative reviews, suggesting it's an annotator-coded signal rather than a natural review feature — use with caution in generalization.
- A minority of reviews with `not_present` failure type are still negative (37%), suggesting latent dissatisfaction drivers (e.g., food quality, price) not fully captured by the current columns.
