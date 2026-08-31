---
dataset: yelp_polarity_reviews
scenario: focus_inference
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What aspects of their experience are Yelp reviewers talking about?"
source_table: augment_table/yelp_polarity_reviews/focus_inference/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:26:32.558600+00:00
wall_seconds: 51.04
---

# Yelp Reviewer Experience Aspects — Focus Inference Report

**Dataset:** `yelp_polarity_reviews` · 250 reviews · Variant: `skill_off`  
**Query:** *What aspects of their experience are Yelp reviewers talking about?*

---

## 1. Concept Tree: Customer Experience Facets

The augmented table decomposes each review across eight binary aspect columns plus a free-text `primary_aspect` label. Together they map the following concept tree:

```
customer_experience
├── food_quality
├── service
├── ambiance
├── value
├── wait_time
├── menu_variety
├── location
└── cleanliness
```

---

## 2. Overall Aspect Prevalence

| Aspect | Mentioned (of 250) | % of reviews |
|---|---|---|
| **service** | 156 | **62%** |
| **food_quality** | 152 | **61%** |
| value | 91 | 36% |
| ambiance | 76 | 30% |
| menu_variety | 53 | 21% |
| wait_time | 52 | 21% |
| location | 33 | 13% |
| cleanliness | 25 | 10% |

**Service** and **food quality** are the two dominant aspects, each mentioned in roughly 6 out of 10 reviews and appearing together in the majority of multi-aspect reviews. **Value, ambiance, menu variety,** and **wait time** form a secondary tier (21–36%). **Location** and **cleanliness** are peripheral, surfacing in fewer than 15% of reviews.

---

## 3. Sentiment Breakdown by Aspect

| Aspect | Positive reviews (n=125) | Negative reviews (n=125) | Δ (pos − neg) |
|---|---|---|---|
| food_quality | 66% | 55% | **+11 pp** |
| service | 51% | 74% | **−23 pp** |
| ambiance | 32% | 29% | +3 pp |
| value | 40% | 33% | +7 pp |
| menu_variety | 28% | 14% | +14 pp |
| location | 18% | 8% | +10 pp |
| wait_time | 17% | 25% | −8 pp |
| cleanliness | 6% | 14% | −8 pp |

Key findings:
- **Service is the strongest differentiator for negative sentiment**: negative reviews mention it 74% of the time vs. 51% in positive reviews (−23 pp gap). The `primary_aspect` free-text confirms this — "poor service," "slow service," and "rude service" collectively account for ~37 of the top 20 keyword tokens.
- **Food quality** and **menu variety** skew positive: reviewers who praise a business are more likely to foreground food taste and selection.
- **Wait time** and **cleanliness** are disproportionately negative concerns, though at lower base rates.
- **Ambiance** and **value** show near-neutral sentiment splits, suggesting they are mentioned in both praise and criticism with roughly equal frequency.

---

## 4. Primary Aspect Distribution (free-text labels)

The top keywords extracted from `primary_aspect`:

| Keyword phrase | Count |
|---|---|
| food quality | 52 |
| poor service | 24 |
| value | 21 |
| service | 18 |
| poor food quality | 17 |
| menu variety | 11 |
| cleanliness | 10 |
| ambiance / atmosphere | ~18 |
| slow / long wait times | ~13 |

*"Food quality"* (positive and negative combined) is the single most-cited primary topic (~28% of reviews). *"Service"* in its various forms (poor, slow, rude, friendly) is the second-most-cited (~25%).

---

## 5. Multi-Aspect Coverage

Most reviews are multi-dimensional:

| # aspects mentioned | Reviews |
|---|---|
| 0 | 2 |
| 1 | 49 (20%) |
| 2 | 77 (31%) |
| 3 | 73 (29%) |
| 4+ | 49 (20%) |

Only 20% of reviews focus on a single aspect; 80% co-mention two or more. The median review covers ~2–3 facets simultaneously, meaning aspect analysis should account for co-occurrence rather than treating aspects as mutually exclusive.

---

## 6. Caveats and Weak Evidence

- **`primary_aspect` is highly fragmented** (221 unique string values for 250 rows), indicating the column was not normalized to a controlled vocabulary. Keyword extraction provides approximate counts only.
- **Location and cleanliness** have low base rates (10–13%), so comparisons across sentiment groups should be interpreted cautiously.
- The dataset spans multiple **business segments** (restaurants, retail, professional services, healthcare, etc.), which may inflate or dilute aspect frequencies. Service-heavy reviews likely dominate because restaurants are the plurality business type.
- **Ambiance** shows almost no sentiment difference (32% vs. 29%), suggesting it is mentioned incidentally rather than as a primary driver of satisfaction or dissatisfaction.

---

## 7. Summary

Yelp reviewers in this corpus focus overwhelmingly on two aspects: **service quality** (the #1 driver of negative reviews) and **food/product quality** (the #1 driver of positive reviews). A secondary cluster — **value, ambiance, menu variety, and wait time** — appears in 20–36% of reviews and provides supplementary context. **Cleanliness** and **location** are niche but high-signal when they do appear (cleanliness is twice as prevalent in negative reviews). For any downstream task, the `service` and `food_quality` binary columns, cross-referenced with `primary_aspect` keywords, offer the most reliable signal for understanding what reviewers are talking about.
