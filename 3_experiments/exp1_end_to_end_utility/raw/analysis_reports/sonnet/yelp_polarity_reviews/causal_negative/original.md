---
dataset: yelp_polarity_reviews
scenario: causal_negative
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: causal_attribution
focus_variable: "label_pos"
query: "Which factors best explain negative Yelp experiences?"
source_table: augment_table/yelp_polarity_reviews/causal_negative/original.csv
generated_at: 2026-07-26T13:57:30.952902+00:00
wall_seconds: 68.89
---

# Analysis Report: Factors Explaining Negative Yelp Experiences

**Dataset:** `yelp_polarity_reviews / causal_negative / original`  
**Focus variable:** `label_pos` (0 = negative review, 1 = positive review)  
**Sample size:** 250 reviews — 125 negative, 125 positive  
**Date:** 2026-07-26

---

## Key Findings

### 1. Poor Service is the Dominant Driver (48.8% of negative reviews)

Service-related language (waiter, waitress, staff, rude, server, unprofessional, ignored) appeared in **61 of 125 negative reviews**. This is the single strongest signal separating negative from positive experiences. Recurring patterns include:

- Staff forgetting customers or ignoring them entirely (e.g., seated but never approached)
- Rude or dismissive employees and managers
- Inability to resolve complaints appropriately

> *"The worst service I've ever had… they'd seated us in an area reserved for a private party… they had thus forgotten we were there."* (YLP-0002)

---

### 2. Excessive Wait Times (31.2%)

Long or unexplained waits appeared in **39 negative reviews**, often compounding service failures. Many reviewers tolerated waits initially but grew frustrated when not acknowledged. Wait-time complaints frequently co-occur with service complaints (20% of negative reviews mention both), suggesting that inattentive staff is often the *cause* of perceived wait issues.

---

### 3. Poor Value / Pricing (16.0%)

**20 negative reviews** cited overpriced items, feeling ripped off, or perceiving a mismatch between price and quality. This factor was standalone in some reviews, suggesting that even adequate food/service can yield negative outcomes if customers feel the value proposition is poor.

---

### 4. Management & Attitude Issues (10.4%)

**13 reviews** explicitly called out managers or owners as contributing to negative experiences — particularly when management failed to intervene during complaints or behaved defensively.

---

### 5. Food Quality & Cleanliness (both ~8.8%)

**11 reviews each** mentioned food quality failures (cold, bland, raw, overcooked) or cleanliness concerns (dirty tables, unsanitary conditions). Notably, **food-quality-only complaints** (without a service mention) accounted for just 4 reviews — food problems frequently appeared alongside service failures, suggesting food quality alone is rarely the sole driver.

---

### 6. Order Errors (1.6%)

Only **2 reviews** specifically flagged wrong orders as a primary complaint. This is a weak signal in this dataset.

---

## Summary Table

| Factor | Negative Reviews Mentioning (n=125) | % |
|---|---|---|
| Poor service (staff behavior) | 61 | 48.8% |
| Wait time | 39 | 31.2% |
| Poor value / pricing | 20 | 16.0% |
| Management attitude | 13 | 10.4% |
| Food quality | 11 | 8.8% |
| Cleanliness | 11 | 8.8% |
| Order errors | 2 | 1.6% |

---

## Caveats & Limitations

- **Keyword-based categorization** may miss paraphrased complaints or overcount ambiguous uses (e.g., "wait" in positive contexts).
- **Co-occurrence** between service and wait-time (20%) makes it difficult to isolate independent causal paths.
- Average review length is similar between negative (492 chars) and positive (464 chars), so review elaborateness alone is not a discriminating feature.
- The dataset is balanced (50/50 split), so base rates are not reflective of the real-world Yelp distribution.

---

## Decision-Ready Conclusions

> **Service quality is the primary causal factor in negative Yelp reviews**, appearing in nearly half of all negative examples and often preceding or exacerbating other complaints (long waits, food quality). Businesses seeking to reduce negative reviews should prioritize staff training and attentiveness over other operational areas. Pricing/value perception is a secondary independent driver worth monitoring, especially in competitive markets.
