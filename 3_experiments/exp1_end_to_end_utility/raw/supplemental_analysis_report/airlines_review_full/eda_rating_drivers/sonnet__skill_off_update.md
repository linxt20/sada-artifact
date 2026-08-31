---
dataset: airlines_review_full
scenario: eda_rating_drivers
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "Overall Rating"
query: "Across Type of Traveller and Class, which review themes are associated with higher vs. lower Overall Rating?"
source_table: augment_table/airlines_review_full/eda_rating_drivers/sonnet__skill_off_update.csv
generated_at: 2026-08-03T05:41:24.570808+00:00
wall_seconds: 49.3
---

# Review Theme Drivers of Overall Rating: Airline Reviews Analysis

## Dataset Overview

- **8,100 reviews** across 4 traveller types and 4 cabin classes  
- **Overall Rating** range: 1–10, mean **5.63**, bimodal distribution (many 1s and 10s)  
- Eight binary review themes extracted: crew service, seat comfort, food quality, entertainment, punctuality, value for money, cleanliness, boarding

---

## Overall Theme Associations

The table below shows the mean Overall Rating when a theme **is** vs. **is not** mentioned:

| Theme | Mentioned (mean) | Not Mentioned (mean) | Lift |
|---|---|---|---|
| **Food Quality** | 6.68 | 3.95 | **+2.73** |
| **Crew Service** | 5.96 | 3.68 | **+2.29** |
| **Entertainment** | 6.70 | 4.92 | **+1.77** |
| **Seat Comfort** | 6.39 | 4.67 | **+1.72** |
| **Cleanliness** | 6.23 | 5.50 | +0.73 |
| **Boarding** | 5.46 | 6.25 | **−0.79** |
| **Punctuality** | 5.26 | 5.94 | −0.68 |
| **Value for Money** | 4.27 | 6.25 | **−1.98** |

**Positive-rating themes:** Food quality, crew service, entertainment, and seat comfort are strongly associated with higher ratings when mentioned — likely because satisfied passengers proactively praise these aspects.

**Negative-signal themes:** Value for money and boarding mentions are associated with *lower* ratings, suggesting these topics arise primarily when passengers are dissatisfied (complaints about poor value or boarding problems).

> **Caution:** Mention ≠ positive sentiment. The theme flags capture topic presence, not valence. The positive lift for food/crew likely reflects that happy reviewers discuss these freely; value/boarding mentions skew negative because dissatisfied reviewers raise them as grievances.

---

## By Type of Traveller

Mean Overall Rating by traveller type:

| Type | Mean Rating |
|---|---|
| Solo Leisure | 6.07 |
| Couple Leisure | 5.48 |
| Business | 5.38 |
| Family Leisure | 5.14 |

**Theme lift (mention vs. not) across traveller types is directionally consistent** — all types show the same positive/negative pattern — but magnitudes differ:

- **Food quality** is the strongest positive driver across all groups; lift is highest for **Family Leisure (+2.91)** and **Solo Leisure (+2.79)**, suggesting meals are especially impactful for these travellers.
- **Crew service** lift is highest for **Solo Leisure (+2.40)**, possibly because solo travellers rely more on staff interaction.
- **Entertainment** shows notably higher lift for **Family Leisure (+2.34)** vs. Couple Leisure (+1.34) and Business (+1.68), consistent with families valuing in-flight entertainment more (children).
- **Value for money** is the strongest negative signal for **Family Leisure (−2.26)**, reflecting price sensitivity.
- **Punctuality and boarding** are universally negative signals (lift −0.65 to −0.86), consistent across all traveller types — these themes surface mainly in complaints.

---

## By Cabin Class

Mean Overall Rating by class:

| Class | Mean Rating |
|---|---|
| First Class | 7.60 |
| Business Class | 6.65 |
| Premium Economy | 5.97 |
| Economy Class | 5.18 |

**Theme lift by class highlights:**

- **Food quality** is a strong positive driver in all classes, with the largest lift in **First Class (+2.87)** and **Economy (+2.81)**. Economy passengers who mention food are comparatively very satisfied; First Class passengers have high expectations that, when met, drive high ratings.
- **Crew service** lift is highest in **First Class (+2.92)**, where personalised service is a key differentiator.
- **Seat comfort** lift is much larger in **Economy (+1.75)** and **First Class (+1.82)** than in **Business Class (+1.06)** or **Premium Economy (+0.66)** — comfort is a more decisive factor at the extremes.
- **Entertainment** strongly lifts Economy ratings (+2.08) but shows minimal lift in Business (+1.01) and Premium Economy (+0.53), suggesting IFE matters more when other amenities are limited.
- **Value for money** is the most negative signal in **First Class (−3.40)**, indicating that when First Class passengers question value, ratings collapse dramatically; lift is milder in Premium Economy (−0.84).
- **Boarding** is a negative signal in Economy (−1.02) and Business (−0.50), but near-neutral in First Class (+0.25) — premium passengers may experience expedited boarding and mention it positively.
- **Cleanliness** shows meaningful positive lift in **First Class (+1.76)** and **Economy (+1.03)**, but negligible lift in Business Class (+0.06).

---

## Key Takeaways

1. **Food quality and crew service are the top positive rating drivers** across virtually all traveller types and classes — airlines improving these aspects are most likely to see overall rating gains.
2. **Value for money is the dominant negative signal**, especially for Family Leisure travellers and First Class passengers (where expectations are highest).
3. **Entertainment matters most for Economy passengers and families** — a weaker differentiator in premium cabins.
4. **Boarding and punctuality mentions signal dissatisfaction** across the board; they function as complaint markers rather than satisfaction drivers.
5. Differences across segments are **directional, not absolute** — no theme flips from positive to negative across traveller type, but magnitude varies meaningfully (e.g., food for families, crew for First Class, entertainment for Economy).
