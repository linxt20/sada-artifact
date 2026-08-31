---
dataset: airlines_review
scenario: prediction_satisfaction_drivers
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating"
query: "What drives customer satisfaction (Overall Rating) across the different airlines?"
source_table: augment_table/airlines_review/prediction_satisfaction_drivers/original.csv
source_report: dataset_portion_2/substrate-claude-sonnet-4-6/airlines_review__prediction_satisfaction_drivers/analyses/original/analysis.md
wall_seconds: 108.9
---

# Customer Satisfaction Drivers in Airline Reviews

## Dataset Overview

The dataset contains passenger reviews across two primary airlines—**Singapore Airlines (SIA/SQ)** and **Qatar Airways (QR)**—covering Economy, Premium Economy, Business, and First Class cabins. The focus variable is `Overall Rating` (1–10 scale). Sub-dimension scores (each 1–5) include: **Seat Comfort**, **Staff Service**, **Food & Beverages**, **Inflight Entertainment**, and **Value For Money**. The binary `Recommended` field serves as a secondary satisfaction signal.

---

## 1. Staff Service Is the Strongest and Most Consistent Driver

Across both airlines, high `Overall Rating` reviews almost universally cite staff/cabin crew positively, and low ratings frequently anchor complaints in staff failures even when hardware was acceptable.

- **High-satisfaction examples**: Rows with Overall Rating 9–10 routinely show Staff Service = 5 and include phrases like *"cabin crew truly went above and beyond"*, *"service was par excellence"*, *"crew is professional, attentive"*, *"exceptional service by the crew"* (e.g., rows 15, 55, 82, 163, 169, 188).
- **Low-satisfaction examples**: Ratings of 1–3 frequently describe crew who were *"not SQ standard"*, *"rude"*, *"unconcerned with passengers"*, or simply absent between services (rows 3, 29, 38, 62, 100, 160).
- **Decoupling**: Critically, several reviews score Staff Service = 5 but still give Overall Rating ≤ 5 when operational failures (baggage loss, delays, ground service, seat defects) dominate the experience. This confirms that good crew service can partially buffer dissatisfaction but does not fully override systemic issues.

**Conclusion**: Staff Service is a necessary but not sufficient condition for high overall satisfaction.

---

## 2. Value for Money Is the Strongest Negative Driver at Low Ratings

The most striking pattern is that `Value For Money` = 1 (lowest score) almost reliably co-occurs with Overall Ratings of 1–3, regardless of other sub-scores.

- Row 6: Seat Comfort 3, Staff 5, Food 1, IFE 1, Value 1 → Overall 1
- Row 7: Seat 1, Staff 4, Food 4, IFE 4, Value 1 → Overall 1
- Row 14: Seat 2, Staff 5, Food 1, IFE 4, Value 1 → Overall 1
- Row 25: Seat 5, Staff 5, Food 2, IFE 2, Value 1 → Overall 1
- Row 38: Seat 2, Staff 5, Food 1, IFE 3, Value 1 → Overall 5

A Value for Money score of 1 is the single feature most consistently associated with the lowest Overall Ratings, cutting across both airlines, all cabin classes, and traveller types. The narrative context shows this reflects: seat/equipment failures, baggage disasters, operational disruptions, or premium-class expectations unmet (e.g., Business Class that felt economy-grade).

Conversely, Value for Money = 4–5 is common in 8–10 rated reviews, though the relationship is more dispersed upward (some reviews with Value 4 still give Overall 7–8).

---

## 3. Food & Beverages: A Prominent Differentiator, Especially in Business Class

`Food & Beverages` emerges as the second most-discussed dimension in review text. It is a strong positive driver when praised and a clear detractor when poor.

- **Positive**: Reviews citing "delicious", "Book the Cook", "great wine list", or "restaurant-style serving" cluster at Overall 8–10 (rows 22, 50–area, 82, 163, 169, 231).
- **Negative**: Reviews highlighting running out of meal choices, poor quality, or inappropriate portions (especially in Business or Premium Economy) pull ratings down to 2–6 (rows 38, 50, 137, 213, 265).
- **Economy vs. Business asymmetry**: Food complaints are more damaging in Business/Premium Economy because passengers set higher expectations relative to the price paid. Economy reviewers often accept moderate food if staff service was warm.

A Food & Beverages score of 1 frequently appears even in 8–9 rated reviews (e.g., rows 12, 18, 23, 55, 57, 84), suggesting food alone rarely tanks satisfaction if other dimensions compensate—but it becomes decisive when compounded with value concerns.

---

## 4. Inflight Entertainment: Hygiene Factor, Not a Satisfaction Driver

`Inflight Entertainment` scores of 4–5 appear in reviews across the full spectrum of Overall Ratings, including very negative ones (rows 3, 7, 13, 34, 35). Conversely, IFE = 1 appears in several 9–10 rated reviews (rows 23, 49, 55, 64, 77, 84). 

This strongly suggests IFE functions as a **hygiene factor**: poor IFE can reduce satisfaction on long-haul flights (e.g., broken screens, outdated content referenced in rows 62, 95, 100, 154), but excellent IFE rarely elevates an otherwise mediocre experience to a high rating.

For very long-haul flights (>10 hours), however, IFE failures are more frequently cited as co-contributors to low ratings, suggesting a route-length moderating effect.

---

## 5. Seat Comfort: Matters Most for Long-Haul and Sleep Flights

Seat comfort complaints (particularly flat-bed issues in Business) appear repeatedly as reasons for low ratings despite high Staff and IFE scores:

- Row 3: Staff 1 (unusual), Seat 5 cited as "really uncomfortable" → Overall 2
- Row 50: Staff 5, Food 5, IFE 4, but seats "most uncomfortable" for sleeping → Overall 5
- Row 29: Multiple service items removed, seats not relevant but combined with poor value → Overall 2

For **Economy** class, Seat Comfort = 4–5 is common even in mid-range (5–7) Overall Ratings, reflecting lower baseline expectations. For **Business Class**, seat failure—especially flat-bed malfunction or old configurations (vs. QSuites/SIA's new beds)—appears to ceiling Overall Rating at 4–7 regardless of crew excellence.

---

## 6. Airline-Level Patterns

### Singapore Airlines (SIA)
- Strong baseline expectation premium: reviewers consistently reference SIA's "world's best airline" reputation, making disappointments more acute (rows 17, 62, 78, 100).
- Staff Service scores are frequently 4–5 across all cabin classes and usually the most praised dimension even in mixed reviews.
- Economy class complaints focus on food portions, amenity cuts (no pillows, no amenity kits unless requested), and inconsistent service during peak COVID-era cost reductions (rows 24, 29, 43).
- High-rating reviews are broadly consistent across cabin classes; Business and Premium Economy reviews tend to be more polarized.

### Qatar Airways (QR)
- QSuite is a recurring marquee positive: reviews mentioning QSuites almost uniformly give Overall 8–10 (rows 131-area, 155, 192, 219, 231, 264).
- **Aircraft inconsistency** is a notable negative driver absent from SIA reviews: passengers who paid for QSuites and received older 2-2-2 or 1-2-1 configurations report sharp drops in satisfaction (rows 141, 165, 166, 206, 239, 247, 258).
- Operational and ground-service failures (baggage delays, missed connections in Doha, compensation disputes) are more frequently cited in negative QR reviews than in SIA reviews (rows 125, 140, 159, 183, 203, 220, 257).
- When Qatar delivers on its full product (QSuites + attentive crew + good food), it generates the highest concentration of 10/10 ratings in the dataset (rows 117, 155, 169, 186, 187, 188, 190, 193, 194, 198).

---

## 7. Operational Factors (Not in Sub-Scores) Are Common Rating Suppressors

Multiple reviews with high sub-dimension scores still give low Overall Ratings due to:
- **Baggage loss/damage** (rows 13, 41, 125, 159, 161, 220)
- **Flight delays and missed connections** (rows 14, 30, 47, 54, 140, 152, 164, 209)
- **Ground staff failures** (rows 62, 218, 229, 267)
- **Customer service non-responsiveness** post-flight (rows 4, 116, 128, 203)

These operational factors are captured only in review text, not in the five sub-scores, yet they clearly suppress Overall Rating and drive `Recommended = no`. This is an important evidence gap: the five sub-scores do not fully account for overall satisfaction variance.

---

## 8. Traveller Type and Class Moderation

- **Business class** reviewers are most sensitive to: seat product quality (flat-bed, QSuite), food and wine level, and consistency of premium experience.
- **Family Leisure** and **Couple Leisure** travellers frequently reference children's handling, seat assignment failures, and baggage issues as key pain points.
- **Solo Leisure** travellers show the widest variance in ratings, suggesting they are more idiosyncratic in what they weight.
- **Business (traveller type)** reviews are typically more critical and specific, often with tighter scoring.

---

## Summary: Satisfaction Driver Hierarchy

| Driver | Role | Evidence Strength |
|---|---|---|
| **Value for Money** | Strongest negative gate; low = almost certain low Overall | Strong |
| **Staff Service** | Strongest positive driver; high = necessary for high Overall | Strong |
| **Food & Beverages** | Major differentiator, especially Business class | Moderate–Strong |
| **Operational reliability** (not in sub-scores) | Key suppressor when things go wrong | Strong (via text) |
| **Seat Comfort** | Decisive for long-haul/sleep flights; hygiene factor in short-haul | Moderate |
| **Inflight Entertainment** | Hygiene factor; failure detracts, excellence rarely elevates | Weak–Moderate |

**Decision-ready insight**: Improving or protecting Value for Money perception and Staff Service quality will have the highest impact on Overall Rating across both airlines. Operational reliability (baggage, connections, compensation) is a hidden but frequent satisfaction killer not captured in the five sub-scores. Qatar Airways' specific risk is product inconsistency (aircraft swaps); Singapore Airlines' specific risk is managing expectation inflation from its premium reputation while maintaining amenity and food standards across cabin classes.
