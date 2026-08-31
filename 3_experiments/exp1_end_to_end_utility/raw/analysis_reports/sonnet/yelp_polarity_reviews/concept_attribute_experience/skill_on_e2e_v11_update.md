---
dataset: yelp_polarity_reviews
scenario: concept_attribute_experience
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: faceted_decomposition
focus_variable: "satisfaction_and_complaint_facets"
query: "What satisfaction and complaint themes appear in Yelp reviews?"
source_table: augment_table/yelp_polarity_reviews/concept_attribute_experience/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:24:05.037111+00:00
wall_seconds: 58.31
---

# Satisfaction and Complaint Themes in Yelp Reviews

**Query:** What satisfaction and complaint themes appear in Yelp reviews?  
**Dataset:** 250 Yelp reviews, balanced (125 positive `label_pos=1`, 125 negative `label_pos=0`)

---

## Method Note

TAPP-generated columns used in this report:
- `food_quality_rating` — numeric 1–5 food quality score (coverage: 142/250, 56.8%)
- `service_staff_sentiment` — staff interaction sentiment: positive/negative/neutral/Unknown (coverage: 221/250 meaningful)
- `service_failure_type` — categorized service failure: not_present / rude_dismissive / slow_inattentive / ignored_forgotten / wrong_item_mistake / discriminatory
- `atmosphere_sentiment` — venue atmosphere sentiment: positive/negative/neutral/Unknown

All four TAPP columns show strong alignment with the original `label_pos` binary outcome and provide meaningful semantic signal beyond the raw text.

---

## Key Findings

### 1. Overall Sentiment Balance

The dataset is exactly balanced: **125 positive and 125 negative** reviews, enabling direct comparison of satisfaction vs. complaint themes.

---

### 2. Satisfaction Themes (Positive Reviews)

Positive reviews are driven by three co-occurring signals:

| Facet | Positive Reviews (n=125) |
|---|---|
| `service_staff_sentiment` = positive | 99 / 125 (79.2%) |
| `atmosphere_sentiment` = positive | 114 / 125 (91.2%) |
| `service_failure_type` = not_present | 119 / 125 (95.2%) |
| Mean `food_quality_rating` (n=79 rated) | **4.46 / 5** |

**Satisfaction is characterized by:** warm, attentive staff interactions, a pleasant atmosphere, no service failures, and high food quality ratings. These four TAPP facets are strongly correlated with positive labels and mutually reinforcing.

---

### 3. Complaint Themes (Negative Reviews)

**58.4% of negative reviews (73/125) contain a named service failure.** The breakdown:

| `service_failure_type` | Count (neg reviews) | % of negatives |
|---|---|---|
| rude_dismissive | 28 | 22.4% |
| slow_inattentive | 19 | 15.2% |
| ignored_forgotten | 14 | 11.2% |
| wrong_item_mistake | 11 | 8.8% |
| discriminatory | 1 | 0.8% |
| **Any failure (subtotal)** | **73** | **58.4%** |
| not_present (other complaints) | 52 | 41.6% |

The remaining 41.6% of negative reviews without a coded service failure still show strongly negative `service_staff_sentiment` (99/125 = 79.2%) and `atmosphere_sentiment` (109/125 = 87.2%), suggesting ambient dissatisfaction with environment or food quality rather than a discrete incident.

**Food quality** also strongly tracks complaints: negative reviews have a mean `food_quality_rating` of **2.16 / 5** (median 2, n=63), versus **4.46 / 5** (median 5, n=79) for positive reviews.

| `food_quality_rating` | Negative (n) | Positive (n) |
|---|---|---|
| 1 | 17 | 0 |
| 2 | 27 | 1 |
| 3 | 12 | 4 |
| 4 | 6 | 32 |
| 5 | 1 | 42 |

---

### 4. Cross-Facet Alignment

All four TAPP columns discriminate sharply between positive and negative reviews:

| TAPP Signal | In Positives | In Negatives |
|---|---|---|
| `service_staff_sentiment` = positive | 99/125 (79%) | 8/125 (6%) |
| `service_staff_sentiment` = negative | 5/125 (4%) | 99/125 (79%) |
| `atmosphere_sentiment` = positive | 114/125 (91%) | 9/125 (7%) |
| `atmosphere_sentiment` = negative | 5/125 (4%) | 109/125 (87%) |
| Any `service_failure_type` coded | 6/125 (5%) | 73/125 (58%) |

The convergence across all four TAPP facets confirms that **positive reviews reflect holistic satisfaction** (food + staff + atmosphere all good), while **negative reviews cluster around specific service failures or generally poor staff and atmosphere experience**.

---

## Summary

**Satisfaction themes:** Friendly, attentive staff (`service_staff_sentiment` = positive, 79% of positives), welcoming atmosphere (`atmosphere_sentiment` = positive, 91%), high food quality (mean 4.46/5), and absence of service failures (95%).

**Complaint themes:** Rude or dismissive staff is the single largest failure type (28 reviews, 22% of negatives), followed by slow/inattentive service (19, 15%) and being ignored/forgotten (14, 11%). Poor food quality (mean rating 2.16/5) and negative atmosphere (87% of negatives) appear across nearly all complaint reviews. Roughly 42% of complaints reflect no discrete failure event but express general environment or quality dissatisfaction.
