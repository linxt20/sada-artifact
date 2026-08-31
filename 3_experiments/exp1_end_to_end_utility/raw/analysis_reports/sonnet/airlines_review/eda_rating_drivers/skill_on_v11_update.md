---
dataset: airlines_review
scenario: eda_rating_drivers
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "Overall Rating"
query: "Across Type of Traveller and Class, which review themes are associated with higher vs. lower Overall Rating?"
source_table: augment_table/airlines_review/eda_rating_drivers/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:03:57.111179+00:00
wall_seconds: 59.25
---

# Review Themes Associated with Higher vs. Lower Overall Ratings
**Dataset:** Airlines Review — 900 verified reviews  
**Dimensions:** Type of Traveller × Class × Augmented Theme Tags  
**Focus Variable:** Overall Rating (1–10, mean = 6.5)

---

## 1. Theme-Level Rating Drivers (Global)

The seven augmented theme columns each show strong differentiation in Overall Rating:

| Theme | High-Rating Signal | Mean OR | Low-Rating Signal | Mean OR |
|---|---|---|---|---|
| **crew_service_quality** | `attentive_warm` | **9.0** | `inattentive_rude` | **3.0** |
| **value_for_money_perception** | `exceeds_expectation` | **9.6** | `poor_value` | **2.3** |
| **food_quality** | `excellent` | **9.4** | `poor` | **4.0** |
| **seat_cabin_hardware_condition** | `new_excellent` | **8.9** | `broken_defective` | **3.9** |
| **service_decline_signal** | `False` (no decline) | **8.2** | `True` (decline noted) | **3.6** |
| **disruption_handling_quality** | `proactive_excellent` | **9.4** | `no_response` | **1.4** |
| **family_child_accommodation** | `True` | **6.6** | `False` | **6.5** |

**Key finding:** `crew_service_quality` and `value_for_money_perception` are the two strongest discriminators, spanning ~6–7 rating points between their best and worst categories. `disruption_handling_quality` has the most extreme low end (`no_response` → 1.4), but affects only 23 reviews.

---

## 2. Patterns by Type of Traveller

Overall mean ratings: Solo Leisure (6.9) > Family Leisure (6.6) > Couple Leisure (6.4) > Business (6.0).

### Crew Service Quality
All traveller types follow the same hierarchy (`attentive_warm` → high, `inattentive_rude` → low), but Business travellers show slightly lower tolerance — their `professional_neutral` scores average ~5.7 vs. 6.0+ for leisure segments.

### Service Decline Signal
The `service_decline_signal = True` flag cuts ratings by ~5 points uniformly across all traveller types:

| Traveller Type | No Decline (mean OR) | Decline Present (mean OR) |
|---|---|---|
| Solo Leisure | 8.4 | 3.9 |
| Couple Leisure | 8.2 | 3.8 |
| Family Leisure | 8.2 | 3.1 |
| Business | 8.0 | 3.1 |

Family Leisure and Business travellers rate disruptions more harshly (mean ~3.1) than leisure individuals.

### Family & Child Accommodation
`family_child_accommodation = True` is almost exclusive to Family Leisure reviews (48 records total). Interestingly, when this flag is present in non-family segments (Couple, Business, Solo), it correlates with very high ratings (8–10), suggesting positive surprise. Within Family Leisure, the flag yields mean OR of 6.4, only slightly above the group average — weak positive signal, possibly because baseline expectations are higher.

---

## 3. Patterns by Class

Overall mean ratings: First Class (7.9) > Business Class (7.1) > Economy Class (6.4) > Premium Economy (5.8).

### Value for Money
`poor_value` is rated equally harshly across all classes (~2.0–2.8), but the *frequency* of `exceeds_expectation` is higher in Business Class, boosting its average. Premium Economy suffers from a relatively high share of `below_expectation` and `poor_value` signals — explaining why it trails Economy Class in mean OR despite higher fares.

### Food Quality
`excellent` food lifts ratings consistently across classes (~9.2–9.7). `poor` food depresses ratings similarly across classes (~4.0), with the exception of First Class (`poor` → 6.0, n=2, weak evidence).

### Seat & Cabin Hardware
`broken_defective` is most damaging in Economy and Premium Economy (~3.9). `new_excellent` elevates ratings in all classes, most notably First Class (9.9, n=7).

### Disruption Handling
`poor_reactive` and `no_response` are devastating across all classes (mean OR 1.4–4.0). Economy Class has the highest exposure (n=102 `poor_reactive`). Proactive handling (`proactive_excellent`) strongly recovers satisfaction in Business and Economy (means ~9.4–9.5).

---

## 4. Combined Theme Interactions

- **Best-case profile** (`attentive_warm` + `excellent` food + `exceeds_expectation` VFM + no service decline) → OR typically 9–10 across all classes and traveller types.
- **Worst-case profile** (`inattentive_rude` + `poor_value` + `service_decline_signal = True`) → OR typically 1–3 across all segments.
- **Premium Economy anomaly:** Despite being a premium fare class, Premium Economy reviews skew negative on VFM, dragging mean OR below Economy Class — a consistent pattern independent of traveller type.
- **Business travellers** are most sensitive to service quality perception: `professional_neutral` (not warm, not rude) still yields only ~5.9 mean OR, suggesting mere competence is insufficient for this segment.

---

## 5. Caveats & Weak Evidence

- **First Class** has only 14 reviews — all sub-group means for this class are indicative only.
- **`family_child_accommodation`** has minimal variance (48 True vs. 852 False) and negligible effect on Overall Rating overall (6.6 vs. 6.5); not a reliable driver.
- **`disruption_handling_quality`** is coded `not_applicable` for 77% of reviews; conclusions on disruption handling are limited to the subset with actual disruptions.
- Theme columns are model-augmented (not directly passenger-rated), so they reflect inferred sentiment rather than explicit sub-scores.

---

## Summary

| Theme | Direction | Strength |
|---|---|---|
| Crew warmth (`attentive_warm`) | ↑ Higher OR | **Very strong** |
| Value for money exceeding expectations | ↑ Higher OR | **Very strong** |
| Excellent food | ↑ Higher OR | Strong |
| New/excellent seat & cabin hardware | ↑ Higher OR | Strong |
| Proactive disruption handling | ↑ Higher OR (recovery) | Strong (niche) |
| Inattentive/rude crew | ↓ Lower OR | **Very strong** |
| Poor value for money | ↓ Lower OR | **Very strong** |
| Service decline signal | ↓ Lower OR | Strong (universal) |
| No disruption response | ↓ Lower OR (extreme) | Strong (niche) |
| Broken/defective cabin hardware | ↓ Lower OR | Moderate |
| Family child accommodation | ↔ Neutral | Weak |
