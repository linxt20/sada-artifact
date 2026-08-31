---
dataset: airlines_review
scenario: eda_rating_drivers
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "Overall Rating"
query: "Across Type of Traveller and Class, which review themes are associated with higher vs. lower Overall Rating?"
source_table: augment_table/airlines_review/eda_rating_drivers/sonnet__skill_off_update.csv
generated_at: 2026-07-28T12:58:00.739520+00:00
wall_seconds: 60.47
---

# Review Theme Drivers of Overall Rating: Airlines Dataset
**Dataset:** 900 reviews · Focus variable: `Overall Rating` (1–10, mean 6.5)

---

## 1. Global Theme Signal (All Reviews)

| Theme | Absent → Present Δ Rating | Direction |
|---|---|---|
| `theme_entertainment` | +1.74 | ↑ Strong positive |
| `theme_staff_service` | +1.50 | ↑ Strong positive |
| `theme_food_quality` | +1.22 | ↑ Positive |
| `theme_seat_comfort` | +0.89 | ↑ Positive |
| `theme_cleanliness` | +0.63 | ↑ Moderate positive |
| `theme_punctuality` | +0.18 | ↑ Weak positive |
| `theme_boarding` | +0.15 | ↑ Weak positive |
| `theme_value_for_money` | **−1.45** | ↓ **Negative** |

**Key finding:** Mentions of entertainment, staff service, and food quality consistently associate with *higher* ratings, while `theme_value_for_money` is the only theme negatively associated with overall rating — meaning it surfaces predominantly in *complaints* about poor value.

This is confirmed by rating-group prevalence: `theme_value_for_money` appears in 26% of low-rated reviews (1–4) but only 12% of high-rated reviews (8–10).

---

## 2. By Type of Traveller

| Type of Traveller | Avg Rating | Strongest positive theme | Strongest negative theme |
|---|---|---|---|
| Solo Leisure (n=332) | 6.87 | food_quality (+1.29) | value_for_money (−0.93) |
| Family Leisure (n=180) | 6.57 | entertainment (+2.10) | value_for_money (−1.17) |
| Business (n=146) | 5.99 | entertainment (+2.74) | value_for_money (−2.85) |
| Couple Leisure (n=242) | 6.37 | staff_service (+2.03) | punctuality (−0.40) |

**Notable patterns:**
- **Business travellers** show the largest penalty for value-for-money mentions (−2.85 pts), suggesting they have high expectations relative to cost. Interestingly, entertainment mentions lift their ratings by +2.74 — likely reflecting satisfaction with premium IFE on long-haul routes.
- **Family Leisure** travellers are strongly driven by entertainment (+2.10); this segment appears highly responsive to IFE quality when travelling with children.
- **Couple Leisure** is the only segment where `theme_punctuality` is mildly *negative* (−0.40), a weak signal that may reflect unmet expectations around scheduling. Staff service is their top positive driver (+2.03).
- **Solo Leisure** has the highest baseline rating (6.87) and is lifted most by food quality (+1.29), suggesting pragmatic satisfaction focused on comfort and meals.

---

## 3. By Cabin Class

| Class | Avg Rating | Strongest positive theme | Strongest negative theme |
|---|---|---|---|
| First Class (n=14) | 7.93 | boarding (+2.55), food (+2.79), staff (+2.29) | value_for_money (−4.58) |
| Business Class (n=237) | 7.10 | staff_service (+1.11) | value_for_money (−2.18) |
| Economy Class (n=563) | 6.37 | entertainment (+2.22) | value_for_money (−1.30) |
| Premium Economy (n=86) | 5.83 | punctuality (+1.17) | cleanliness (−0.43) |

**Notable patterns:**
- **Economy Class** shows the highest positive lift from entertainment (+2.22) and staff service (+1.77) — these are the decisive themes separating satisfied from dissatisfied economy passengers.
- **First Class** has the highest average rating but also the steepest value-for-money penalty (−4.58). When premium passengers feel prices don't match experience, their ratings collapse sharply. *Note: n=14 — treat this figure as directional only.*
- **Business Class** seat comfort and cleanliness show near-zero Δ (−0.04 and −0.06), suggesting these are baseline expectations at that cabin level — failing them doesn't hurt as much as it would in economy because it's rarer, but meeting them doesn't reward either.
- **Premium Economy** is the lowest-rated cabin on average (5.83) and is uniquely hurt by cleanliness mentions (−0.43), pointing to a gap between price expectations and actual experience quality in this cabin.

---

## 4. Cross-cutting Summary

| Theme | Consistent driver of **high** ratings? | Consistent driver of **low** ratings? |
|---|---|---|
| Staff service | ✅ Yes — across all segments | — |
| Entertainment | ✅ Yes — especially Economy, Family, Business travellers | — |
| Food quality | ✅ Yes — especially Solo, Family, First Class | — |
| Value for money | — | ✅ Yes — strongest in Business travellers and First/Business class |
| Seat comfort | ✅ Economy and First Class | Neutral in Business Class |
| Boarding | ✅ First Class (weak evidence) | Neutral elsewhere |
| Cleanliness | ✅ Economy, Business travellers | Weak negative in Premium Economy |
| Punctuality | Weak/mixed | Weak negative for Couple Leisure |

---

## 5. Caveats
- Theme variables are binary (mentioned/not mentioned) and do not distinguish *positive* vs. *negative* review mentions. The negative association of `theme_value_for_money` strongly implies it appears in complaints, but this is inferred, not directly coded.
- First Class (n=14) and Premium Economy (n=86) findings should be treated as indicative only.
- Themes are not mutually exclusive; reviews often mention multiple themes simultaneously.
