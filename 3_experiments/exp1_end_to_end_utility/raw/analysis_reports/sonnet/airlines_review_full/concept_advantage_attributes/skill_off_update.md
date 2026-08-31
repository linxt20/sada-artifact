---
dataset: airlines_review_full
scenario: concept_advantage_attributes
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "airline_competitive_advantage"
query: "What are the common advantage attributes of airlines whose overall rating is high?"
source_table: augment_table/airlines_review_full/concept_advantage_attributes/sonnet__skill_off_update.csv
generated_at: 2026-08-03T05:40:04.657671+00:00
wall_seconds: 39.99
---

# Common Advantage Attributes of High-Rating Airlines

## Dataset Overview

- **Total reviews:** 8,100  
- **High-rating group** (`is_high_rating = 1`, Overall Rating 8–10): **3,406 reviews**  
- **Low-rating group** (`is_high_rating = 0`, Overall Rating 1–7): **4,694 reviews**  
- **Advantage attributes tracked:** `adv_staff`, `adv_food`, `adv_seat_comfort`, `adv_entertainment`, `adv_value`, `adv_punctuality`, `adv_cleanliness`

---

## Attribute Prevalence by Rating Group

| Attribute | High-Rating Rate | Low-Rating Rate | Lift (High / Low) |
|---|---|---|---|
| `adv_staff` | **59.8%** | 18.1% | 3.31× |
| `adv_food` | **44.7%** | 13.9% | 3.21× |
| `adv_seat_comfort` | **35.4%** | 12.1% | 2.94× |
| `adv_entertainment` | **26.2%** | 8.4% | 3.12× |
| `adv_punctuality` | **13.4%** | 4.3% | 3.12× |
| `adv_cleanliness` | **10.5%** | 2.6% | 4.10× |
| `adv_value` | 5.1% | 2.8% | 1.82× |

---

## Key Findings

### 1. Staff Service is the Dominant Advantage
`adv_staff` is mentioned in **~60% of high-rating reviews**, far exceeding any other attribute. This is the single strongest differentiator between high- and low-rated airlines (3.31× lift).

### 2. Food & Beverages is the Second-Most Common Attribute
`adv_food` appears in **~45% of high-rating reviews** (3.21× lift). Among high-rating reviews that mention staff as an advantage, **1,047 also mention food** as an advantage — the most common two-attribute co-occurrence.

### 3. Seat Comfort Rounds Out the Top Three
`adv_seat_comfort` is cited in **35.4%** of high-rating reviews (2.94× lift). It frequently co-occurs with staff (811 reviews), indicating a strong multi-attribute profile for highly rated flights.

### 4. Entertainment and Punctuality are Meaningful but Secondary
Both `adv_entertainment` (26.2%) and `adv_punctuality` (13.4%) have lift values above 3×, indicating they are meaningfully associated with high ratings, but are mentioned far less often than the top three.

### 5. Cleanliness Has the Highest Lift but Low Base Rate
`adv_cleanliness` shows the highest lift (4.10×) but is mentioned in only ~10.5% of high-rating reviews. When reviewers notice cleanliness positively, it strongly correlates with high ratings — but it is rarely mentioned explicitly.

### 6. Value for Money is a Weak Differentiator
`adv_value` has the lowest lift (1.82×) and lowest mention rate in the high group (5.1%). This may reflect that high-rated airlines are often premium carriers where value is not the primary driver of satisfaction.

### 7. Multi-Attribute Reviews are Concentrated in High-Rating Group
High-rating reviews average **1.95 advantage attributes** per review vs. **0.62** for low-rating reviews. **59.3%** of high-rating reviews mention 2 or more advantages, vs. only 16.9% of low-rating reviews.

---

## Summary

The profile of a highly-rated airline review is strongly characterized by **staff service, food quality, and seat comfort** — in that order. Cleanliness has an outsized signal-to-noise ratio (highest lift), while value for money is the weakest differentiator. High-rating reviews consistently bundle multiple positives, suggesting that holistic experience quality — not a single factor — drives top scores.

> **Caveat:** The `adv_*` columns appear to be LLM-extracted attributes from review text, so their presence depends on what reviewers explicitly mention, not objective measurement. Attributes like punctuality and cleanliness may be underrepresented because passengers only mention them when they are notably good or bad.
