---
dataset: airlines_review_full
scenario: concept_key_focus_points
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "airline_service_quality"
query: "Help me understand the key points in this table — what should I concentrate on?"
source_table: augment_table/airlines_review_full/concept_key_focus_points/sonnet__skill_off_update.csv
generated_at: 2026-08-03T05:40:50.930834+00:00
wall_seconds: 39.54
---

# Key Focus Points: Airline Reviews Dataset

## Dataset Overview
- **8,100 reviews** across 8+ airlines, covering Economy, Business, Premium Economy, and First Class cabins.
- Focus variable: **Overall Rating** (1–10, mean ≈ 5.6) and **Recommended** (yes: 53%, no: 47%).

---

## 1. Value For Money Is the Dominant Driver

Among all sub-ratings, **Value For Money** correlates most strongly with Overall Rating ($r \approx 0.88$), dwarfing Staff Service ($r \approx 0.23$), Seat Comfort ($r \approx 0.21$), Food & Beverages ($r \approx 0.16$), and Inflight Entertainment ($r \approx 0.14$). Passengers who feel they got good value will almost always rate highly — improving other dimensions without addressing pricing perception will have limited impact.

---

## 2. Clear Airline Tier Divide

| Airline | Avg Rating | Recommend Rate |
|---|---|---|
| All Nippon Airways | 7.95 | 83% |
| EVA Air | 7.42 | 77% |
| Qatar Airways | 7.20 | 73% |
| Singapore Airlines | 6.54 | 64% |
| Cathay Pacific | 6.17 | 60% |
| Air France | 4.64 | 40% |
| Emirates | 4.67 | 39% |
| Turkish Airlines | 3.68 | 29% |

Asian carriers (ANA, EVA Air, Qatar) occupy the top tier. Air France, Emirates, and Turkish Airlines are well below average — Turkish Airlines' 3.68 mean rating and 29% recommendation rate are notably severe.

---

## 3. Expectation Gap Is Negative Across All Airlines

The **Expectation_Gap** (Overall Rating minus Airline_Avg_Rating) is negative for every major airline (dataset mean: −1.23), meaning reviewers consistently rate below the airline's own average. The gap is worst for Turkish Airlines (−1.97) and mildest for ANA (−0.37). This suggests a systematic bias toward dissatisfied passengers leaving reviews, or genuine declining service quality over time.

---

## 4. Cabin Class Shapes Experience

| Class | Avg Rating |
|---|---|
| First Class | 7.60 |
| Business Class | 6.65 |
| Premium Economy | 5.97 |
| Economy Class | 5.18 |

Economy reviews (68% of the dataset) pull the overall average down significantly. Economy passengers are the largest voice in this data — their concerns disproportionately shape aggregate scores.

---

## 5. Sentiment Aligns Reliably with Recommendations

- **Positive** sentiment → 93% recommend
- **Negative** sentiment → 91% do NOT recommend
- **Mixed** and **Neutral** lean negative (57% and 68% do not recommend, respectively)

Mixed reviews skewing toward non-recommendation is a key insight: ambivalence is not neutral — it effectively signals dissatisfaction.

---

## 6. Value Perception Is Mostly "Fair"

87% of reviews are rated "Fair" for Value_Perception; only 11% "Good Value" and 2% "Overpriced." This compressed distribution limits its discriminatory power, but it confirms that pricing complaints are not the primary complaint mode for most passengers.

---

## Key Takeaways for Decision-Making

1. **Prioritize Value For Money** improvements above all sub-dimensions — it is by far the strongest predictor of overall satisfaction.
2. **Turkish Airlines, Emirates, and Air France** are underperforming peers in both ratings and recommendation rates and warrant focused attention.
3. **Economy Class** volumes dominate the data; any airline-wide improvement strategy must address economy-class passengers.
4. **Mixed sentiment ≠ neutral** — treat mixed reviews as a warning signal, not a middle ground.
5. The universal negative Expectation_Gap suggests managing customer expectations (marketing, pre-flight communications) may be as important as in-flight improvements.
