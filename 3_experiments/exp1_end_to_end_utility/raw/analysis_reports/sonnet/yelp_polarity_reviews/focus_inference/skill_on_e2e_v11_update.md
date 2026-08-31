---
dataset: yelp_polarity_reviews
scenario: focus_inference
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What aspects of their experience are Yelp reviewers talking about?"
source_table: augment_table/yelp_polarity_reviews/focus_inference/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:24:03.737684+00:00
wall_seconds: 43.61
---

# Yelp Review Aspects Analysis
**Query:** What aspects of their experience are Yelp reviewers talking about?  
**Dataset:** 250 Yelp reviews (125 positive, 125 negative); balanced binary label (`label_pos`)

---

## Method Note
TAPP-generated columns used: `food_quality_rating`, `food_item_highlight`, `service_quality_rating`, `service_issue_type`, `staff_behavior_tone`. These columns provide structured semantic signal about review content beyond the raw `label_pos` and `review_text` fields.

---

## Key Finding: Two Dominant Aspects — Service and Food

Yelp reviewers overwhelmingly discuss **service** and **food**, with service appearing in more reviews than food.

| Aspect | Reviews Mentioning (N=250) | Coverage |
|---|---|---|
| Service quality | 193 | 77.2% |
| Food quality | 148 | 59.2% |
| Both service + food | 106 | 42.4% |
| Service only | 87 | 34.8% |
| Food only | 42 | 16.8% |
| Neither | 15 | 6.0% |

---

## 1. Food Aspect (`food_quality_rating`, `food_item_highlight`)

Food is discussed in 59.2% of reviews. Positive mentions (76/148) slightly outnumber negative (28/148), with 44 mixed.

**`food_quality_rating` strongly predicts overall sentiment:**

| food_quality_rating | N | % Negative Review | % Positive Review |
|---|---|---|---|
| positive | 76 | 3.9% | 96.1% |
| mixed | 44 | 81.8% | 18.2% |
| negative | 28 | 96.4% | 3.6% |
| not_present | 102 | 57.8% | 42.2% |

`food_item_highlight` shows that 25 reviews praise a specific dish and 14 criticize one; 53 reviews discuss multiple items with mixed results — consistent with the mixed-rating group above.

---

## 2. Service Aspect (`service_quality_rating`, `service_issue_type`, `staff_behavior_tone`)

Service is the most-covered aspect (77.2%). It is an even stronger differentiator of overall sentiment than food.

**`service_quality_rating` vs. label:**

| service_quality_rating | N | % Negative Review | % Positive Review |
|---|---|---|---|
| positive | 78 | 5.1% | 94.9% |
| mixed | 44 | 68.2% | 31.8% |
| negative | 71 | 98.6% | 1.4% |
| not_present | 57 | 36.8% | 63.2% |

**`staff_behavior_tone` reinforces this pattern:**

| staff_behavior_tone | N | % Negative | % Positive |
|---|---|---|---|
| friendly_warm | 65 | 15.4% | 84.6% |
| rude_hostile | 70 | 97.1% | 2.9% |
| professional_neutral | 1 | 0% | 100% |
| Unknown | 114 | 41.2% | 58.8% |

**`service_issue_type` identifies specific failure modes in negative reviews:**

| service_issue_type | N | % Negative Reviews |
|---|---|---|
| rude_dismissive | 35 | 100% |
| slow_inattentive | 24 | 87.5% |
| ignored_forgotten | 7 | 85.7% |
| order_error | 7 | 85.7% |
| policy_inflexibility | 3 | 100% |
| not_present | 174 | 31.0% |

The most common service complaint is **rude/dismissive behavior** (35 reviews), followed by **slow or inattentive service** (24 reviews).

---

## Summary

Yelp reviewers primarily discuss two aspects of their experience:

1. **Service** (77% of reviews) — the dominant topic, covering staff behavior, attentiveness, and specific failure modes. Rude/hostile staff and service neglect are the strongest drivers of negative reviews.
2. **Food** (59% of reviews) — dish quality, specific items praised or criticized, with positive food ratings strongly associated with positive overall reviews.

Together these two aspects are present in 42% of reviews simultaneously, and at least one is present in 94% of all reviews. When neither is flagged (6% of reviews), reviews tend to discuss non-restaurant contexts (e.g., real estate, salons), explaining the lower predictive signal in that stratum.
