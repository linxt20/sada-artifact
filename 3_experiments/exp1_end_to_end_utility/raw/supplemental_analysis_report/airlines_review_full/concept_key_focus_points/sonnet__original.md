---
dataset: airlines_review_full
scenario: concept_key_focus_points
variant: original
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "airline_service_quality"
query: "Help me understand the key points in this table — what should I concentrate on?"
source_table: augment_table/airlines_review_full/concept_key_focus_points/original.csv
generated_at: 2026-08-03T05:40:35.271692+00:00
wall_seconds: 45.85
---

# Airlines Review Dataset — Key Focus Points

## Dataset at a Glance
- **8,100 verified passenger reviews** across 10+ airlines, covering Economy, Business, Premium Economy, and First Class.
- **Focus variable:** `Overall Rating` (1–10 scale) and binary `Recommended` (yes/no).
- Five sub-scores: Seat Comfort, Staff Service, Food & Beverages, Inflight Entertainment, Value For Money (each 1–5).

---

## 1. Value For Money Dominates Overall Rating
The single strongest driver of `Overall Rating` is **Value For Money** (correlation ≈ **0.88**), far ahead of all other sub-scores:

| Sub-score | Correlation with Overall Rating |
|---|---|
| Value For Money | **0.88** |
| Staff Service | 0.23 |
| Seat Comfort | 0.21 |
| Food & Beverages | 0.16 |
| Inflight Entertainment | 0.14 |

> **Key takeaway:** Passengers primarily judge their experience through a value lens. Improvements in any other area matter far less unless perceived value is also high.

---

## 2. Bimodal Rating Distribution — Little Middle Ground
Ratings cluster at the extremes rather than the middle:

| Bucket | Share of Reviews |
|---|---|
| Low (1–3) | 37% |
| Mid (4–6) | 14% |
| High (7–10) | 48% |

Passengers are either satisfied or strongly dissatisfied. The `Recommended` split reflects this: 53% "yes" vs 47% "no", with a mean rating of **8.5** for recommenders vs **2.4** for non-recommenders.

---

## 3. Airline Performance Varies Widely
Among the 10 largest airlines by review count:

| Airline | Mean Rating | Reviews |
|---|---|---|
| All Nippon Airways | **7.95** | 258 |
| EVA Air | 7.42 | 281 |
| Qatar Airways | 7.20 | 1,624 |
| Japan Airlines | 7.10 | 201 |
| Singapore Airlines | 6.54 | 972 |
| Korean Air | 6.49 | 187 |
| Cathay Pacific | 6.17 | 744 |
| Emirates | 4.67 | 1,350 |
| Air France | 4.64 | 798 |
| Turkish Airlines | **3.68** | 1,685 |

Turkish Airlines has both the **most reviews** and the **lowest mean rating** — a significant signal. Emirates and Air France also score below average despite large volumes.

---

## 4. Travel Class Has a Clear Gradient
Higher cabin class consistently yields higher satisfaction:

| Class | Mean Overall Rating |
|---|---|
| First Class | 7.60 |
| Business Class | 6.65 |
| Premium Economy | 5.97 |
| Economy Class | 5.18 |

Economy comprises **68% of all reviews**, so the dataset is heavily weighted toward the most critical passengers.

---

## 5. Traveller Type: Solo Leisure Rates Highest
| Traveller Type | Mean Rating |
|---|---|
| Solo Leisure | 6.07 |
| Couple Leisure | 5.48 |
| Business | 5.38 |
| Family Leisure | 5.14 |

Family travellers rate experiences lowest — likely due to higher practical demands (seat arrangements, children's meals, IFE).

---

## 6. Sub-Score Means Are All Below Midpoint
All five sub-scores average between **3.1 and 3.6** out of 5, indicating **broadly mediocre** service perceptions across the board. Value For Money (3.15) is the weakest sub-score on average, consistent with its high correlation with overall dissatisfaction.

---

## Exceptions & Caveats
- **Verified field is inconsistent** (mixed TRUE/FALSE/NotVerified/unstructured text entries) — treat verification-based splits with caution.
- ANA and EVA Air have relatively small review counts (200–280); their high ratings may reflect selection bias.
- The 5-point sub-scores are relatively coarse and may compress meaningful variance.

---

## Summary: What to Concentrate On
1. **Value For Money** is the make-or-break dimension — it overwhelmingly explains overall ratings.
2. **Turkish Airlines, Emirates, and Air France** are the primary drag on aggregate scores despite high review volumes.
3. The **bimodal distribution** means average metrics can mislead — segment analysis (by airline and class) tells a clearer story.
4. **Economy Class passengers** (68% of data) are the most critical group and rate significantly lower than upper-cabin travellers.
