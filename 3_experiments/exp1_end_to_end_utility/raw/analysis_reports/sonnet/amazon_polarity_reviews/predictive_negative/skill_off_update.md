---
dataset: amazon_polarity_reviews
scenario: predictive_negative
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "label_pos"
query: "What review signals predict negative Amazon product satisfaction?"
source_table: augment_table/amazon_polarity_reviews/predictive_negative/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:02:38.865840+00:00
wall_seconds: 44.01
---

# Review Signals Predicting Negative Amazon Product Satisfaction

**Dataset:** 250 Amazon reviews, balanced 125 negative (`label_pos=0`) / 125 positive (`label_pos=1`)  
**Focus variable:** `label_pos` (0 = negative satisfaction, 1 = positive)

---

## Key Predictive Signals

### 1. Composite Negative Score (Strongest Single Predictor)
`composite_neg_score` aggregates lexical negativity signals into one score.

| Label | Mean | Median | Max |
|-------|------|--------|-----|
| Negative (0) | 3.66 | 3.0 | 22.2 |
| Positive (1) | –0.03 | 0.0 | 5.4 |

**Decision rule:** `composite_neg_score > 3` → **89.1% of such reviews are negative**.  
The near-zero median for positive reviews means this threshold carries minimal false-positive risk.

---

### 2. Negative Word Count
Mean negative word count in negative reviews (2.56) is **3.9× higher** than in positive reviews (0.66).

**Rule:** `neg_word_count ≥ 3` → **90.2% negative precision**.

---

### 3. Negative Phrases
Explicit multi-word negative phrases (`neg_phrase_count ≥ 1`) are present in 24% of negative but barely 1% of positive reviews.

**Rule:** `neg_phrase_count ≥ 1` → **96.2% negative precision** (highest precision among individual signals, but low recall due to rarity).

---

### 4. Intensified Negativity
`intensified_neg_count ≥ 1` (e.g., "absolutely terrible", "completely useless"):

- Negative reviews mean: 0.096 vs. positive: 0.008  
- **Rule:** `intensified_neg_count ≥ 1` → **90.9% negative precision**

---

### 5. Sentiment Ratio
Positive `sentiment_ratio` (proportion of negative-leaning tokens) strongly separates classes.

| Label | Mean Sentiment Ratio |
|-------|---------------------|
| Negative (0) | +0.027 |
| Positive (1) | –0.029 |

**Rule:** `sentiment_ratio > 0.02` → **95.8% negative precision**.

---

### 6. Question Count
Rhetorical or complaint-driven questions appear more in negative reviews (mean 0.16 vs. 0.04).  
**Rule:** `question_count ≥ 1` → 72.2% negative precision — **useful supporting signal, but weak alone**.

---

### 7. Caps Word Count
All-caps words (expressing frustration/emphasis) average **2× higher** in negative reviews (1.45 vs. 0.72). Useful as a tie-breaker but not reliable as a standalone predictor.

---

## Practical Decision Tree

```
composite_neg_score > 3  →  NEGATIVE (89% precision)
  ELSE IF neg_phrase_count ≥ 1  →  NEGATIVE (96% precision)
  ELSE IF sentiment_ratio > 0.02  →  NEGATIVE (96% precision)
  ELSE IF neg_word_count ≥ 3  →  NEGATIVE (90% precision)
  ELSE  →  LIKELY POSITIVE
```

---

## Exceptions and Weak Evidence

- **`exclamation_count`**: Nearly identical across negative (0.97) and positive (1.15) reviews — exclamation marks are not a negative signal; positive reviews use them slightly more.
- **`short_title_flag`**: Slightly more common in positive reviews (66%) than negative (56%) — short titles marginally favor positive labels but are unreliable.
- **`negated_pos_count`** (e.g., "not good"): Elevated in negatives (0.088 vs. 0.040) but low absolute counts limit utility.
- **Augmented categorical columns** (ProductCategory, ComplaintSeverity, etc.) were not present in the `skill_off` variant — no category-level breakdown is possible from this file.
- High-scoring outliers exist in positive reviews (`composite_neg_score` up to 5.4), indicating mixed-sentiment reviews can confound the score.

---

## Summary

The most decision-ready signals for predicting negative satisfaction are, in order:
1. **`composite_neg_score > 3`** — best combined predictor
2. **`sentiment_ratio > 0.02`** — near-identical precision, independent derivation
3. **`neg_phrase_count ≥ 1`** — highest precision but sparse
4. **`neg_word_count ≥ 3`** — robust fallback

Combining any two of these signals should yield >95% negative-label precision on this dataset.
