---
dataset: yelp_polarity_reviews
scenario: predictive_low
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "label_pos"
query: "What review signals predict low Yelp user satisfaction?"
source_table: augment_table/yelp_polarity_reviews/predictive_low/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:26:35.832592+00:00
wall_seconds: 44.91
---

# Predicting Low Yelp User Satisfaction — Analysis Report

**Dataset:** `sonnet__skill_off_update.csv` (250 reviews)  
**Focus variable:** `predicted_low_satisfaction` (1 = low, 0 = not low)  
**Class distribution:** 88 low-satisfaction (35%), 162 not low-satisfaction (65%)

---

## 1. Ground-Truth Label Alignment

The engineered label (`predicted_low_satisfaction`) closely tracks the human annotation (`label_pos`):

| label_pos (human) | predicted_low = 0 | predicted_low = 1 |
|---|---|---|
| 0 (negative review) | 48 | **77** |
| 1 (positive review) | **114** | 11 |

~74% of human-negative reviews are flagged as low-satisfaction, and ~91% of human-positive reviews are not. The model is directionally accurate but somewhat conservative (48 negatives are not flagged).

---

## 2. Key Signals Ranked by Correlation

| Feature | Correlation with low satisfaction | Direction |
|---|---|---|
| `neg_word_count` | **+0.63** | Strongest positive predictor |
| `negation_adjusted_sentiment` | **−0.57** | Lower adjusted sentiment → low sat. |
| `sentiment_score` | **−0.52** | Raw sentiment also strong |
| `pos_word_count` | **−0.46** | Fewer positive words → low sat. |
| `complaint_phrase_count` | **+0.42** | Explicit complaints reinforce signal |
| `caps_ratio` | **+0.16** | Weak but present |
| `review_length_tokens` | **+0.08** | Very weak |
| `exclamation_ratio` | **−0.01** | Negligible |

---

## 3. Mean Feature Values by Outcome

| Feature | Not Low (0) | Low (1) |
|---|---|---|
| `neg_word_count` | 0.31 | **2.05** |
| `pos_word_count` | **2.60** | 0.80 |
| `sentiment_score` | **0.040** | −0.020 |
| `negation_adjusted_sentiment` | **0.031** | −0.036 |
| `complaint_phrase_count` | 0.00 | **0.25** |
| `caps_ratio` | 0.005 | 0.009 |
| `review_length_tokens` | 87 | 93 |

Low-satisfaction reviews average **6.6× more negative words** and **3.3× fewer positive words** than satisfied reviews.

---

## 4. Signal Interpretation

### Strongest signals
- **High `neg_word_count` (≥2):** The single clearest predictor. Low-satisfaction reviews accumulate explicit negative terms (e.g., "horrible," "worst," "rude," "disappointing").
- **Negative `negation_adjusted_sentiment`:** When the sentiment score drops below ~0, especially after negation adjustment, dissatisfaction is reliably indicated. Reviews with phrases like "not great," "never coming back," or "I wouldn't recommend" consistently score below zero on this metric.
- **Low `pos_word_count` (≤1):** Absence of positive language is nearly as diagnostic as presence of negative language.

### Moderate signals
- **`complaint_phrase_count` > 0:** 25% of low-satisfaction reviews contain explicit complaint phrases vs. 0% of satisfied ones—but many low-satisfaction reviews (75%) still score 0, making this a useful confirmatory rather than primary signal.
- **`caps_ratio` slightly elevated:** All-caps usage (shouting) is weakly associated with frustration (mean 0.009 vs. 0.005), visible in reviews like YLP-0012 and YLP-0021.

### Weak / Unreliable signals
- **`exclamation_ratio`:** Essentially no predictive value (r = −0.01). Exclamations appear in both enthusiastic positive reviews ("Loved it!!!") and angry negative ones, canceling out.
- **`review_length_tokens`:** Marginally longer in low-satisfaction reviews (93 vs. 87 tokens), but the difference is not meaningful.

---

## 5. Notable Exceptions

- **YLP-0013, YLP-0036, YLP-0010 (label_pos=0, predicted=0):** Negative reviews that were *not* flagged. These tend to use measured, descriptive language with few explicit negative words and neutral sentiment scores—showing that analytical/understated complaints can evade lexical detection.
- **YLP-0046 (label_pos=0, predicted=1):** A mixed review with 2 negative words that tips into predicted low satisfaction despite an overall balanced tone.
- **Positive reviews with any negation** (e.g., "not bad," "I don't mind"): Negation adjustment captures these but can occasionally suppress legitimate positivity in the sentiment score.

---

## 6. Decision-Ready Summary

> **To predict low Yelp satisfaction, prioritize:** (1) `neg_word_count ≥ 2`, (2) `negation_adjusted_sentiment < 0`, and (3) `pos_word_count ≤ 1`. These three features together account for the dominant signal. Add `complaint_phrase_count > 0` as a tie-breaker. Exclamation marks and review length are not reliable discriminators and should be deprioritized.
