---
dataset: amazon_fine_food_review
scenario: predictive_score_features
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "review_score"
query: "What features can be extracted to train a model to predict a review's score?"
source_table: augment_table/amazon_fine_food_review/predictive_score_features/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:01:02.872624+00:00
wall_seconds: 30.86
---

# Feature Analysis: Predicting Amazon Food Review Score

## Dataset Overview

- **Rows:** 10,000 reviews; **Target:** `Score` (1–5 integer rating)
- **Class distribution:** Heavily skewed toward 5-star (61.8%), with 1-star (9.3%), 4-star (14.3%), 3-star (8.6%), and 2-star (5.9%).

---

## Engineered Features Available

The dataset augments the raw text with 10 numeric features. Their Pearson correlations with `Score` are:

| Feature | Correlation with Score | Notes |
|---|---|---|
| `negative_keyword_count` | **−0.335** | Strongest single predictor |
| `positive_keyword_count` | **+0.281** | Strong positive signal |
| `question_count` | −0.121 | More questions → lower score |
| `text_length` / `word_count` | −0.100 | Longer reviews slightly lower-rated |
| `exclamation_count` | +0.082 | Enthusiasm correlates with higher scores |
| `summary_length` | −0.067 | Weak negative signal |
| `review_year` | −0.037 | Negligible |
| `helpfulness_ratio` | +0.034 | Negligible linear correlation |
| `uppercase_ratio` | −0.019 | Negligible |

---

## Key Feature Findings

### 1. Sentiment Keywords (Strongest Signal)
`positive_keyword_count` (+0.281) and `negative_keyword_count` (−0.335) are the most predictive features by a wide margin. Together they form a basic sentiment proxy that directly maps to the score scale.

### 2. Review Length & Word Count
`text_length` and `word_count` (correlated ~1.0 with each other, both −0.10) suggest dissatisfied reviewers write slightly longer reviews to explain their complaints. Useful as a feature but weak alone.

### 3. Question Count (−0.121)
Reviews with more questions tend to be lower-rated—plausibly because confused or disappointed buyers raise concerns in their text.

### 4. Exclamation Count (+0.082)
Mild positive signal; enthusiastic language is associated with higher scores.

### 5. Raw Text & Summary (NLP Features)
`Text` and `Summary` columns are available for TF-IDF, embeddings, or fine-tuned language model features—likely far more predictive than the hand-crafted counts above.

### 6. Helpfulness Ratio & Temporal Features
`helpfulness_ratio` and `review_year` show near-zero correlation with Score and are unlikely to add meaningful predictive value for score estimation specifically.

---

## Recommended Feature Set for Modeling

1. **Text embeddings** from `Text` and `Summary` (e.g., sentence-transformers or TF-IDF + SVD)
2. **`positive_keyword_count`** and **`negative_keyword_count`** — highest signal among numeric features
3. **`question_count`** and **`exclamation_count`** — punctuation-based sentiment proxies
4. **`word_count`** / `text_length` — minor length signal
5. **`helpfulness_ratio`** — weak but free signal; include with caution

---

## Caveats

- All numeric correlations are **linear**; non-linear models (e.g., gradient boosting) may extract more value from weaker features.
- The 5-star class dominates (61.8%), so accuracy-based evaluation will be misleading; macro-F1 or weighted-F1 is preferable.
- Keyword counts are simple heuristics—their quality depends entirely on the keyword list used, which is not documented in the data.
