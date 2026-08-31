---
dataset: airlines_review_full
scenario: concept_key_focus_points
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "airline_service_quality"
query: "Help me understand the key points in this table — what should I concentrate on?"
source_table: augment_table/airlines_review_full/concept_key_focus_points/sonnet__skill_on_v11_update.csv
generated_at: 2026-08-03T05:51:18.157650+00:00
wall_seconds: 49.15
---

# Airlines Review Dataset — Key Focus Points

## Dataset Overview
- **8,100 verified passenger reviews** across 10+ airlines, spanning Economy through First Class.
- **Overall Rating** ranges 1–10; mean **5.6**, median **6** — roughly symmetric but polarized (25th pct = 2, 75th pct = 9).
- **53% recommend** their airline, 47% do not — a nearly even split indicating no strong industry-wide satisfaction.

---

## 1. Value for Money Is the Dominant Driver of Overall Rating
Correlation with Overall Rating:

| Sub-rating | Correlation |
|---|---|
| **Value For Money** | **0.88** |
| Staff Service | 0.23 |
| Seat Comfort | 0.21 |
| Food & Beverages | 0.16 |
| Inflight Entertainment | 0.14 |

Value for Money overwhelmingly drives the overall score. All other sub-dimensions are secondary. Improvements in staff, comfort, or food matter, but will move the needle less unless perceived value aligns.

---

## 2. Staff Interaction Quality Is the Clearest Differentiator
Staff quality separates high-rated from low-rated experiences sharply:

| Staff Interaction | Avg Overall Rating |
|---|---|
| Friendly & Attentive | 9.1 |
| Professional/Neutral | 6.1 |
| Mixed | 5.2 |
| Unhelpful/Indifferent | 2.2 |
| Rude/Hostile | 1.9 |

Rude or indifferent staff (nearly 2,900 reviews combined) pulls ratings to near-floor levels. This is the single biggest controllable quality lever.

---

## 3. Disruption Handling Strongly Separates Extremes
Among the ~2,774 reviews involving a disruption:

| Handling Quality | Avg Rating |
|---|---|
| Proactive & Effective | 9.3 |
| Adequate | 7.3 |
| Inadequate/Poor | **2.0** |

Poor disruption handling (2,321 reviews) is catastrophic for ratings. The gap between proactive and poor handling is ~7 rating points. Most disruption cases (84%) are handled poorly or just adequately — a major area of weakness across the industry.

---

## 4. Airline Performance Is Highly Uneven

| Airline | Avg Rating | Review Count |
|---|---|---|
| All Nippon Airways | 7.95 | 258 |
| EVA Air | 7.42 | 281 |
| Qatar Airways | 7.20 | 1,624 |
| Japan Airlines | 7.10 | 201 |
| Singapore Airlines | 6.54 | 972 |
| Emirates | 4.67 | 1,350 |
| Air France | 4.64 | 798 |
| Turkish Airlines | **3.68** | 1,685 |

Turkish Airlines and Air France have the largest review volumes among low-performers — meaning many passengers are dissatisfied. ANA and EVA Air lead on quality but have smaller sample sizes (weaker evidence for broad conclusions).

---

## 5. Cabin Class Matters, but Economy Dominates Volume

| Class | Avg Rating | Count |
|---|---|---|
| First Class | 7.6 | 121 |
| Business Class | 6.7 | 2,104 |
| Premium Economy | 6.0 | 371 |
| **Economy Class** | **5.2** | **5,504** |

Economy comprises 68% of reviews and scores lowest. Improving economy-class value perception would have the broadest impact on aggregate satisfaction.

---

## 6. Unresolved Complaints Are Prevalent
- **2,183 reviews** (27%) report complaints that went **unresolved or ignored**.
- Only **307** (4%) were resolved satisfactorily.
- **1,490 reviews** report a booking/policy issue (rebooking difficulty, refund denial, lost seat reservations).

This signals a systemic gap in post-issue customer care — compounding initial service failures.

---

## 7. Haul Type and Service Consistency
- Short-haul flights average **6.5** vs. long-haul **5.5** — likely reflecting higher expectations on longer flights.
- **70% of reviews have no service consistency baseline** (first-time flyers), limiting trend analysis. Among repeat flyers, 83% report consistent high quality vs. 17% declining — but this sub-group is small (n ≈ 2,400).

---

## Key Takeaways for Decision-Making

1. **Fix value perception** — it is the top predictor of overall satisfaction by a wide margin.
2. **Address staff conduct** — rude/indifferent staff is the fastest path to near-zero ratings.
3. **Improve disruption protocols** — the majority of disruptions are handled poorly; proactive handling yields near-perfect scores.
4. **Focus on economy class and high-volume low-performers** (Turkish Airlines, Emirates, Air France) — that is where the most dissatisfied passengers are concentrated.
5. **Close the complaint resolution loop** — unresolved complaints represent a large recoverable segment of dissatisfied customers.

> **Caveats:** ANA/EVA ratings come from smaller samples. Service consistency trends are limited to ~30% of reviewers. Correlations are associative, not causal.
