---
dataset: airlines_review_full
scenario: eda_rating_drivers
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "Overall Rating"
query: "Across Type of Traveller and Class, which review themes are associated with higher vs. lower Overall Rating?"
source_table: augment_table/airlines_review_full/eda_rating_drivers/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-08-03T05:53:03.552457+00:00
wall_seconds: 79.57
---

# Review Themes Associated with Higher vs. Lower Overall Rating
## Across Type of Traveller and Class — Airlines Reviews (n = 8,100)

---

### Method Note

TAPP-generated columns used in this analysis: `crew_service_quality`, `service_responsiveness`, `food_quality`, `ground_service_quality`, `disruption_handling_quality`, `customer_service_resolution`, `class_value_gap`. These were cross-validated against original structured fields (`Value For Money`, `Staff Service`, `Seat Comfort`, `Food & Beverages`, `Value For Money`) and the `Overall Rating` outcome (1–10 scale).

---

## 1. Baseline: Overall Rating by Traveller Type and Class

| Type of Traveller | Mean Rating | n |
|---|---|---|
| Solo Leisure | **6.07** | 3,237 |
| Couple Leisure | 5.48 | 1,899 |
| Business | 5.38 | 1,413 |
| Family Leisure | **5.14** | 1,551 |

| Class | Mean Rating | n |
|---|---|---|
| First Class | **7.60** | 121 |
| Business Class | 6.65 | 2,104 |
| Premium Economy | 5.97 | 371 |
| Economy Class | **5.18** | 5,504 |

Solo Leisure travellers rate highest; Family Leisure lowest. First and Business Class rate markedly higher than Economy and Premium Economy.

**Structural anchor:** `Value For Money` correlates most strongly with Overall Rating ($r = 0.883$), far ahead of `Staff Service` ($r = 0.229$), `Seat Comfort` ($r = 0.210$), `Food & Beverages` ($r = 0.160$), and `Inflight Entertainment` ($r = 0.140$).

---

## 2. Dominant Theme: Crew Service & Responsiveness

`crew_service_quality` and `service_responsiveness` are the strongest semantic drivers of rating.

### Mean Overall Rating by `crew_service_quality`

| Value | Mean Rating | n |
|---|---|---|
| warm_proactive | **8.99** | 3,215 |
| competent_neutral | 6.19 | 1,254 |
| robotic_rushed | 4.73 | 314 |
| rude_inattentive | **2.26** | 3,160 |

The gap between `warm_proactive` (≈9.0) and `rude_inattentive` (≈2.3) is **6.7 points** — the largest single-theme spread in the dataset. This pattern holds uniformly across all traveller types (Family Leisure: 9.11 vs. 2.02; Business: 8.87 vs. 2.37) and all cabin classes (First Class: 9.29 vs. 1.50; Economy: 9.06 vs. 2.02).

### Mean Overall Rating by `service_responsiveness`

| Value | Mean Rating | n |
|---|---|---|
| responsive | **8.89** | 3,552 |
| inconsistent | 5.47 | 946 |
| slow | 4.23 | 354 |
| absent | **2.23** | 3,199 |

`service_responsiveness` mirrors `crew_service_quality`: responsive service drives ratings ~8.9; absent service collapses to ~2.2. This is consistent across Class — Economy responsive: 8.91, absent: 2.11; Business Class responsive: 8.85, absent: 2.80.

> **Key finding:** Crew warmth and responsiveness are the primary high-rating drivers for every traveller segment. Family Leisure travellers are most sensitive to warm/proactive crew (mean 9.11), while Business travellers show the largest absolute drop under rude/inattentive conditions (mean 1.47 when `crew_service_quality = Unknown`, likely reflecting severe incidents).

---

## 3. Value Perception: `class_value_gap`

`class_value_gap` (True = reviewers feel value was delivered; False = felt gap between price/class and experience) is the second-largest rating driver, directly reinforcing the $r = 0.883$ `Value For Money` correlation.

| class_value_gap | Mean Rating | Mean Value For Money | n |
|---|---|---|---|
| True (value delivered) | **8.10** | 4.18 | 3,388 |
| False (value gap) | **3.79** | 2.37 | 4,312 |

This 4.3-point gap is consistent across all traveller types:

| Type of Traveller | False | True |
|---|---|---|
| Family Leisure | 3.21 | **8.29** |
| Solo Leisure | 4.09 | **8.36** |
| Business | 3.78 | 7.57 |
| Couple Leisure | 3.84 | 7.88 |

And across classes:

| Class | False | True |
|---|---|---|
| First Class | 5.27 | **9.20** |
| Business Class | 4.70 | 8.16 |
| Economy Class | 3.48 | 8.05 |
| Premium Economy | 4.47 | 7.85 |

Economy Class passengers have the lowest "False" mean (3.48), indicating they are harshest when value expectations are unmet. First Class passengers who still feel a value gap score 5.27 — higher than other classes, suggesting partial satisfaction offsets.

---

## 4. Food Quality

`food_quality` is relevant where food is mentioned (~58% coverage).

| food_quality | Mean Rating | n |
|---|---|---|
| excellent | **9.16** | 1,716 |
| adequate | 7.68 | 1,559 |
| poor | 4.01 | 1,232 |
| wrong_or_missing_meal | **3.14** | 165 |
| Unknown | 3.64 | 3,428 |

Excellent food is strongly associated with high ratings across all classes (First Class: 9.61; Economy: 9.22). Poor food suppresses ratings to ~4.0 regardless of class. Family Leisure travellers show the highest rating boost from excellent food (9.33) and the sharpest drop from wrong/missing meals (2.28 vs. overall mean of 3.14), suggesting food matters most to families.

---

## 5. Ground Service

`ground_service_quality` covers ~56% of reviews with meaningful values.

| ground_service_quality | Mean Rating | n |
|---|---|---|
| positive | **9.03** | 1,378 |
| adequate | 7.29 | 252 |
| poor_unhelpful | 2.52 | 2,222 |
| rude_aggressive | **2.09** | 657 |

Rude/aggressive ground staff (mean 2.09) is nearly as damaging as rude cabin crew. Family Leisure travellers score rude ground staff 1.82 — the lowest of any segment — consistent with check-in/boarding stress for families. Business travellers are relatively less sensitive (2.32), possibly due to lounge/priority access buffering.

---

## 6. Disruption Handling

`disruption_handling_quality` applies to ~40% of reviews (disruptions present).

| disruption_handling_quality | Mean Rating | n |
|---|---|---|
| proactive_helpful | **9.30** | 406 |
| reactive_adequate | 6.32 | 158 |
| passive_unhelpful | 2.19 | 2,383 |
| actively_obstructive | **1.52** | 323 |
| not_applicable | 7.28 | 4,830 |

`actively_obstructive` handling is the lowest mean rating in the entire dataset (1.52). Economy Class bears the most disruptions (274 actively_obstructive cases vs. 40 in Business Class). Business travellers with proactive disruption handling rate 9.32 — close to the maximum — suggesting that when airlines recover well, Business travellers reward disproportionately.

---

## 7. Customer Service Resolution

`customer_service_resolution` applies to ~25% of reviews.

| customer_service_resolution | Mean Rating | n |
|---|---|---|
| resolved_satisfactorily | **9.26** | 231 |
| partially_resolved | 3.77 | 163 |
| unresolved_ignored | **1.76** | 1,632 |
| not_contacted | 6.58 | 6,074 |

Unresolved complaints drive ratings to 1.76 — nearly the floor. The effect is consistent across traveller types (Business: 1.86; Family Leisure: 1.63). Resolution satisfaction (9.26) nearly matches the rating of passengers who never needed to complain (6.58 for `not_contacted`), confirming that service recovery can neutralise negative experiences.

---

## 8. Summary: High vs. Low Rating Themes

| Theme (TAPP column) | High-Rating Signal | Low-Rating Signal |
|---|---|---|
| `crew_service_quality` | warm_proactive → **8.99** | rude_inattentive → **2.26** |
| `service_responsiveness` | responsive → **8.89** | absent → **2.23** |
| `class_value_gap` | value delivered → **8.10** | value gap → **3.79** |
| `food_quality` | excellent → **9.16** | wrong/missing → **3.14** |
| `ground_service_quality` | positive → **9.03** | rude_aggressive → **2.09** |
| `disruption_handling_quality` | proactive_helpful → **9.30** | actively_obstructive → **1.52** |
| `customer_service_resolution` | resolved_satisfactorily → **9.26** | unresolved_ignored → **1.76** |
| `Value For Money` (structured) | correlation $r = 0.883$ — strongest single predictor overall |

**Segment-specific highlights:**
- **Family Leisure** is most sensitive to food quality and ground staff rudeness; scores lowest overall (5.14).
- **Business travellers** show disproportionate reward when disruption is handled proactively, but also the harshest outcomes when crew interactions fail (mean 1.47 for `Unknown` crew quality — likely severe incidents).
- **Economy Class** (n = 5,504) dominates the dataset; passengers here have the steepest rating drop when value expectations are unmet (False `class_value_gap` mean = 3.48 vs. 4.70 in Business Class).
- **First Class** (n = 121, mean 7.60) shows the highest baseline but still drops sharply under rude crew (1.50) or obstructive disruption handling (1.50), confirming premium travellers have zero tolerance for service failures.
