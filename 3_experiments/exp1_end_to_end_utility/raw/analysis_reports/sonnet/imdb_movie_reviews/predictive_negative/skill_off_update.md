---
dataset: imdb_movie_reviews
scenario: predictive_negative
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "label_pos"
query: "What review signals predict negative IMDb audience satisfaction?"
source_table: augment_table/imdb_movie_reviews/predictive_negative/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:24:37.783768+00:00
wall_seconds: 37.66
---

# Predictive Signals for Negative IMDb Audience Satisfaction

**Dataset:** 250 reviews (125 negative `label_pos=0`, 125 positive `label_pos=1`), perfectly balanced.

---

## Key Findings

### 1. Strongest Predictors of Negative Sentiment

| Feature | Neg mean | Pos mean | Correlation w/ negative |
|---|---|---|---|
| `neg_minus_pos_ratio` | 0.0102 | −0.0123 | **0.55** |
| `neg_word_ratio` | 0.0166 | 0.0033 | **0.45** |
| `pos_word_ratio` | 0.0064 | 0.0157 | −0.37 (inverse) |
| `intensified_neg_count` | 0.328 | 0.040 | **0.28** |
| `negation_count` | 1.92 | 1.30 | 0.22 |

**`neg_minus_pos_ratio`** (negative minus positive lexical ratio) is the single best predictor (r = 0.55). Reviews where negative words substantially outnumber positive words are overwhelmingly negative in sentiment.

**`neg_word_ratio`** independently carries strong signal (r = 0.45), indicating raw density of negative vocabulary is predictive on its own.

**`pos_word_ratio`** acts as a protective factor — high positive-word density strongly predicts *non-negative* outcomes (r = −0.37).

---

### 2. Threshold-Level Evidence

| Condition | N | Negative Rate |
|---|---|---|
| `neg_word_ratio ≥ 0.02` | 36 | **94%** |
| `intensified_neg_count ≥ 1` | 36 | **92%** |
| `neg_minus_pos_ratio ≥ 0.01` | 46 | **93%** |
| `pos_word_ratio ≥ 0.015` | 87 | 26% |

Reviews with even a single **intensified negative expression** (e.g., "absolutely terrible", "completely unwatchable") are negative 92% of the time. This makes `intensified_neg_count` a high-precision flag despite low base rate.

---

### 3. Weaker or Null Signals

- **`negation_before_pos_count`** (e.g., "not good"): Mean difference is small (0.08 vs. 0.06) and correlation is only 0.04 — barely predictive.
- **`exclamation_count`**: Nearly identical across groups (0.47 vs. 0.52); essentially no predictive value.
- **`caps_ratio`**: Negligible difference; not useful as a standalone signal.
- **`avg_sentence_length`**: Slightly shorter in negative reviews (17.4 vs. 19.1 words), r = −0.12 — a weak tendency, not reliable alone.
- **`review_length_log`**: Marginally longer negative reviews (r = 0.09), not practically meaningful.

---

## Summary

The clearest signals of negative IMDb audience satisfaction are:

1. **High `neg_minus_pos_ratio`** — the dominant predictor; reflects net negative vocabulary tone.
2. **High `neg_word_ratio`** — dense use of negative words is a reliable indicator.
3. **Presence of `intensified_neg_count > 0`** — intensified negativity is a near-certain flag (92% precision).
4. **Low `pos_word_ratio`** — absence of positive language reinforces negativity prediction.
5. **Higher `negation_count`** — moderate signal; many negations add context but are less decisive alone.

**Caveats:** The dataset is small (250 rows), and features are lexicon-based heuristics. Negation-before-positive patterns and surface features (caps, exclamations) show little discriminative power in this sample. Models relying solely on these weaker features would underperform.
