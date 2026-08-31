---
dataset: yelp_polarity_reviews
scenario: causal_negative
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "label_pos"
query: "Which factors best explain negative Yelp experiences?"
source_table: augment_table/yelp_polarity_reviews/causal_negative/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:25:41.520325+00:00
wall_seconds: 45.14
---

# Factors Explaining Negative Yelp Experiences

## Dataset Overview
- **250 reviews**, balanced: 125 negative (`label_pos = 0`) and 125 positive (`label_pos = 1`).
- Key augmented columns: `complaint_category`, `negative_signal_count`, and per-aspect mention counts (`service`, `food`, `price`, `wait`, `cleanliness`, `atmosphere`).

---

## 1. Primary Complaint Categories (Negative Reviews)

| Complaint Category | Count | % of Negatives | Avg Negative Signals |
|---|---|---|---|
| food_quality | 43 | 34.4% | 2.21 |
| service | 41 | 32.8% | 1.98 |
| other | 17 | 13.6% | 1.59 |
| wait_time | 10 | 8.0% | 2.40 |
| price | 10 | 8.0% | 2.00 |
| atmosphere | 2 | 1.6% | 2.50 |
| cleanliness | 2 | 1.6% | 1.00 |

**Food quality** and **service** are the two dominant drivers, together accounting for ~67% of all negative reviews. They are nearly equal in prevalence.

---

## 2. Negative Signal Intensity

- Negative reviews carry a mean `negative_signal_count` of **2.03** vs. **0.92** for positive reviews — roughly 2× higher.
- `wait_time` and `atmosphere` complaints generate the highest average signal counts (2.40 and 2.50), suggesting these issues, when present, provoke stronger dissatisfaction. However, they are rare (10 and 2 cases respectively), making this evidence weak.

---

## 3. Mention-Count Patterns

| Aspect | Negative Mean | Positive Mean | Δ |
|---|---|---|---|
| service_mention_count | 1.07 | 0.70 | +0.37 |
| wait_mention_count | 0.63 | 0.27 | +0.36 |
| food_mention_count | 1.22 | 1.54 | −0.32 |
| price_mention_count | 0.26 | 0.28 | ≈0 |
| cleanliness_mention_count | 0.11 | 0.07 | +0.04 |
| atmosphere_mention_count | 0.14 | 0.26 | −0.12 |

- **Service and wait** mentions are meaningfully elevated in negative reviews.
- **Food** mentions are actually *higher* in positive reviews, suggesting food discussion alone is not a reliable negative predictor — valence matters.
- **Price and cleanliness** show negligible differences between groups.

---

## 4. Causal Summary

```
Negative Yelp Experience
├── Food Quality Issues (34%)  — primary driver; high signal intensity
├── Service Failures (33%)     — near-equal driver; staff conduct/inattentiveness
├── Wait / Delay Problems (8%) — low frequency but high signal intensity when present
├── Price-Value Mismatch (8%)  — moderate signal; independent of mention-count difference
└── Other / Uncategorized (14%) — heterogeneous; lower average signal intensity
```

---

## 5. Exceptions & Caveats

- **Atmosphere and cleanliness** are rarely the primary complaint (2 cases each); conclusions about them are unreliable.
- The `other` category (17 cases) likely masks additional causal factors not captured by the current schema.
- Food mentions are *more* frequent in positive reviews; this column reflects topic salience, not sentiment — using it alone would be misleading.
- The dataset is perfectly balanced (125/125) by construction, which may not reflect real-world Yelp distributions.

---

## Decision-Ready Takeaways

1. **Food quality and service are the two factors that best explain negative Yelp experiences**, each accounting for roughly one-third of negatives.
2. **Wait/delay problems**, though infrequent, generate disproportionately intense dissatisfaction when they occur.
3. Negative reviews carry ~2× the negative-signal density of positive ones — severity, not just topic, differentiates them.
4. **Price, cleanliness, and atmosphere** are weak explanatory factors in this dataset.
