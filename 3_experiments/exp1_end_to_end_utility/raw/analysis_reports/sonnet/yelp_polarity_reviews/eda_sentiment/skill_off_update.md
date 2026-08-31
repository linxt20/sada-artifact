---
dataset: yelp_polarity_reviews
scenario: eda_sentiment
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "label_pos"
query: "How do review themes differ between positive and negative Yelp sentiment?"
source_table: augment_table/yelp_polarity_reviews/eda_sentiment/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:25:55.299590+00:00
wall_seconds: 35.78
---

# Review Theme Analysis: Positive vs. Negative Yelp Sentiment

## Dataset Overview

- **Total reviews:** 250 (125 positive, 125 negative), perfectly balanced.
- **Augmented columns:** Six binary theme flags (`theme_food_quality`, `theme_service`, `theme_ambiance`, `theme_price_value`, `theme_wait_time`, `theme_repeat_visit`), a `themes_present` string, and a `theme_count`.

---

## Theme Prevalence by Sentiment

| Theme | Positive | Negative | Δ (Pos − Neg) |
|---|---|---|---|
| **food_quality** | 57.6% | 46.4% | **+11.2 pp** |
| **service** | 44.8% | 56.8% | **−12.0 pp** |
| **ambiance** | 17.6% | 18.4% | −0.8 pp |
| **price_value** | 29.6% | 20.0% | **+9.6 pp** |
| **wait_time** | 33.6% | 35.2% | −1.6 pp |
| **repeat_visit** | 26.4% | 31.2% | −4.8 pp |

---

## Key Findings

### 1. Service is the dominant negative theme
Service is the most frequently flagged theme in negative reviews (56.8%) — 12 percentage points higher than in positive reviews (44.8%). The most common negative theme combination is `service|wait_time` (12 occurrences), reflecting complaints about staff neglect or slow, inattentive experiences. This aligns with review language such as *"they forgot we were there — twice."*

### 2. Food quality anchors positive reviews
Food quality appears in 57.6% of positive reviews vs. 46.4% of negative ones (+11.2 pp). In positive reviews, `food_quality` alone is the single most common combination (14 reviews), meaning food praise is often the sole point of a glowing review.

### 3. Price/value is a positive differentiator
Price-value framing appears in 29.6% of positive reviews but only 20.0% of negative ones (+9.6 pp). Positive reviewers use price favorably (deals, good value for money), while negative reviewers mention it less — suggesting dissatisfied customers focus more on service failures than cost.

### 4. Repeat-visit intent skews slightly negative
`repeat_visit` is mentioned more in negative reviews (31.2% vs. 26.4%). This is counterintuitive but may reflect explicit statements of *not* returning ("I will never come back"), which the theme classifier may be capturing neutrally based on keyword presence rather than valence.

### 5. Ambiance and wait time are roughly neutral
Both themes appear at nearly identical rates across sentiments (ambiance: ~18%; wait time: ~34%), making them weak discriminators of overall polarity.

### 6. Thematic complexity is equal
Average `theme_count` is nearly identical: **2.10 (positive)** vs. **2.08 (negative)**. Negative reviews are not inherently more multi-thematic than positive ones.

---

## Notable Exceptions and Caveats

- **13 positive and 12 negative reviews have `themes_present = "none"`**, representing a non-trivial share (~10%) with no detected theme — likely very short or atypical reviews, which limits coverage.
- The `repeat_visit` finding (more common in negatives) is a weak-evidence exception that warrants caution; it could be a labeling artifact.
- Differences in ambiance and wait time are negligible and should not be used to characterize sentiment polarity.

---

## Summary

> **Positive reviews** center on **food quality and perceived value**; satisfaction is expressed through the product itself.  
> **Negative reviews** center on **service failures**, often combined with wait-time complaints — the interaction experience, not the food, drives dissatisfaction.
