---
dataset: yelp_polarity_reviews
scenario: eda_sentiment
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: exploratory_data_analysis
focus_variable: "label_pos"
query: "How do review themes differ between positive and negative Yelp sentiment?"
source_table: augment_table/yelp_polarity_reviews/eda_sentiment/original.csv
generated_at: 2026-07-26T13:59:41.587025+00:00
wall_seconds: 85.34
---

# Review Theme Analysis: Positive vs. Negative Yelp Sentiment

**Dataset:** `yelp_polarity_reviews / eda_sentiment / original`  
**Records:** 250 (125 positive `label_pos=1`, 125 negative `label_pos=0`)  
**Focus variable:** `label_pos` (binary sentiment label)

---

## 1. Dataset Overview

| Metric | Positive | Negative |
|---|---|---|
| Count | 125 | 125 |
| Avg. review length (chars) | 464 | 492 |
| Balance | 50% | 50% |

The corpus is perfectly balanced. Negative reviews are marginally longer (+6%), suggesting dissatisfied customers elaborate more in their complaints.

---

## 2. Theme Prevalence by Sentiment

The table below shows the percentage of reviews in each class that mention each theme (based on keyword matching):

| Theme | Positive (%) | Negative (%) | ∆ (Neg − Pos) |
|---|---|---|---|
| Food quality | 85.6 | 76.8 | −8.8 |
| Experience / loyalty | 48.8 | 44.0 | −4.8 |
| Service / staff | 38.4 | 52.8 | **+14.4** |
| Wait time | 36.8 | 40.8 | +4.0 |
| Price / value | 29.6 | 24.0 | −5.6 |
| Ambiance | 16.0 | 13.6 | −2.4 |

**Key findings:**
- **Food quality** is the dominant theme in both classes, but it is more prominent in positive reviews — satisfied customers lead with food praise.
- **Service/staff** is the starkest differentiator: negative reviews mention service ~37% more often than positive ones, marking poor staff interaction as the primary complaint driver.
- **Wait time** appears slightly more in negative reviews, consistent with frustration over slow service.
- **Price/value** and **ambiance** show only weak differences.

---

## 3. Sentiment-Specific Language

### Positive-class signals (exclamatory praise)

| Word | Positive | Negative |
|---|---|---|
| amazing | 13 | 1 |
| delicious | 17 | 2 |
| love | 25 | 8 |
| great | 44 | 19 |
| fantastic | 5 | 1 |
| recommend | 13 | 7 |

Positive reviews are saturated with superlative endorsements ("amazing," "delicious," "fantastic"), reflecting enthusiastic food and overall experience praise.

### Negative-class signals (failure & condemnation)

| Word | Positive | Negative |
|---|---|---|
| horrible | 1 | 13 |
| rude | 0 | 8 |
| never | 8 | 17 |
| worst | 1 | 6 |
| terrible | 0 | 4 |
| didn't | — | 22 (top-word) |

Negative reviews lean on condemnation words ("horrible," "rude," "worst") and negation ("didn't," "don't"), consistent with complaints about broken expectations.

### Return intent ("back")

- "back" appears in 39 negative vs. 25 positive reviews — negative reviews use it predominantly in "never coming back" / "won't be back" constructions (never+back: 8 neg vs. 3 pos).

---

## 4. Theme Narrative Summary

| Sentiment | Primary Narrative |
|---|---|
| **Positive** | Food-first praise → staff is warm and friendly → likely to return / recommend |
| **Negative** | Service failures dominate → staff described as rude or neglectful → food disappointments secondary → explicit vow not to return |

---

## 5. Caveats & Weak Evidence

- **Keyword matching is approximate.** Context is ignored (e.g., "great service — NOT!" would be counted as positive).
- **Ambiance and price** show no meaningful separation, making them poor differentiators in this dataset.
- **"recommend"** appears in 7 negative reviews, likely in the form "I would not recommend," illustrating polarity ambiguity in raw keyword counts.
- Sample size (n=250) is modest; patterns are suggestive but may not generalize to the full Yelp corpus.

---

## 6. Decision-Ready Takeaways

1. **Service quality is the strongest discriminating theme** between positive and negative reviews — far more so than food quality alone.
2. Positive reviews concentrate on **food praise + staff warmth**, while negative reviews concentrate on **staff failures + unmet expectations**.
3. **"Never back"** patterns and high-intensity condemnation words ("horrible," "rude") are reliable markers of the negative class.
4. Any model or annotation strategy for this dataset should weight service-related language heavily as a sentiment signal.
