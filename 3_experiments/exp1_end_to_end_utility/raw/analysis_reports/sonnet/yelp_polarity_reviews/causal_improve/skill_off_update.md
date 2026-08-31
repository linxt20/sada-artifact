---
dataset: yelp_polarity_reviews
scenario: causal_improve
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: what_if
focus_variable: "user_satisfaction"
query: "How can businesses improve Yelp user satisfaction?"
source_table: augment_table/yelp_polarity_reviews/causal_improve/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:25:19.518276+00:00
wall_seconds: 42.11
---

# How Can Businesses Improve Yelp User Satisfaction?

**Dataset:** `sonnet__skill_off_update.csv` | 250 reviews (125 positive / 125 negative, perfectly balanced) | Focus variable: `label_pos` (1 = positive, 0 = negative)

---

## 1. Key Finding: Satisfaction Drivers Are Perfectly Separating

The `satisfaction_driver` column perfectly partitions polarity — every `strength:*` label maps exclusively to positive reviews and every `weakness:*` label maps exclusively to negative reviews. This confirms the column is a reliable signal of what makes or breaks satisfaction.

| Satisfaction Driver | Negative Reviews | Positive Reviews |
|---|---|---|
| `strength:service` | 0 | 31 |
| `strength:food_quality` | 0 | 27 |
| `strength:general` | 0 | 52 |
| `strength:value` | 0 | 8 |
| `strength:ambiance` | 0 | 7 |
| `weakness:unspecified` | 83 | 0 |
| `weakness:service` | 15 | 0 |
| `weakness:food_quality` | 10 | 0 |
| `weakness:value` | 10 | 0 |
| `weakness:ambiance` | 7 | 0 |

---

## 2. What Drives Positive Reviews

Among the 125 positive reviews, positive drivers rank as follows:

| Top Positive Driver | Count | Share of Positives |
|---|---|---|
| `general_positive` (no specific dimension) | 52 | 41.6% |
| `service` | 31 | 24.8% |
| `food_quality` | 27 | 21.6% |
| `value` | 8 | 6.4% |
| `ambiance` | 7 | 5.6% |

**Service and food quality together account for nearly half of all positive reviews**, making them the two highest-leverage dimensions for improvement.

---

## 3. What Drives Negative Reviews

Among the 125 negative reviews:

| Primary Complaint | Count | Share of Negatives |
|---|---|---|
| `unspecified` | 83 | 66.4% |
| `service` | 15 | 12.0% |
| `food_quality` | 10 | 8.0% |
| `value` | 10 | 8.0% |
| `ambiance` | 7 | 5.6% |

The dominant negative category is **unspecified dissatisfaction** (66%), suggesting reviewers often express general displeasure without pinpointing one root cause — possibly reflecting a cumulative poor experience rather than a single failure.

---

## 4. Sentiment Field Analysis

Dimensional sentiment scores corroborate the driver analysis:

| Dimension | Positive → label=1 rate | Negative → label=1 rate |
|---|---|---|
| Service | 34/41 = **83%** | 1/16 = 6% |
| Food | 34/42 = **81%** | 2/12 = 17% |
| Value | 15/18 = **83%** | 4/14 = 29% |
| Ambiance | 11/16 = **69%** | 6/17 = 35% |

- **Service and food quality** show the sharpest contrast between positive and negative sentiment on overall review polarity — fixing these has the highest expected return.
- **Ambiance** has the weakest discrimination: even negative ambiance sentiment correlates with a positive review 35% of the time, indicating customers tolerate poor ambiance when other dimensions deliver.

---

## 5. Actionable Recommendations

| Priority | Action | Evidence |
|---|---|---|
| 🔴 High | **Improve service consistency** | Service is the #1 named positive driver (31 reviews) and #1 named negative complaint (15 reviews); service sentiment has an 83% → positive conversion rate |
| 🔴 High | **Elevate food quality** | Food is the #2 positive driver (27 reviews); positive food sentiment yields 81% positive reviews |
| 🟡 Medium | **Address value perception** | 10 negative reviews cite value directly; positive value sentiment converts at 83% — competitive pricing or portion signaling could shift neutral customers |
| 🟡 Medium | **Investigate unspecified dissatisfaction** | 83 negative reviews carry no specific complaint, suggesting systemic experience issues (wait times, cleanliness, overall vibe) that no single dimension captures |
| 🟢 Lower | **Improve ambiance** | Smallest differentiator; customers appear willing to overlook weak ambiance if food/service excel |

---

## 6. Caveats

- The **`weakness:unspecified`** category (83 reviews, 66% of negatives) limits diagnostic precision — root causes here are unknown from structured columns alone.
- The `satisfaction_driver` column appears model-assigned (not human-labeled), which could introduce classification noise.
- The sample is balanced (50/50 by design), so base rates do not reflect real-world Yelp polarity distributions.
