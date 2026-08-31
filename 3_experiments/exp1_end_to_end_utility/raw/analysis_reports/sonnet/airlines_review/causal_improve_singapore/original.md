---
dataset: airlines_review
scenario: causal_improve_singapore
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: causal_attribution
focus_variable: "overall_rating_recommendation"
query: "How can Singapore Airlines improve its overall rating and recommendation rate, especially on flights where passengers do not recommend it (Recommended = no)?"
source_table: augment_table/airlines_review/causal_improve_singapore/original.csv
source_report: dataset_portion_2/substrate-claude-sonnet-4-6/airlines_review__causal_improve_singapore/analyses/original/analysis.md
wall_seconds: 118.91
---

# Singapore Airlines: Improving Overall Rating and Recommendation Rate

## 1. Dataset Overview

The dataset contains 255 verified passenger reviews of Singapore Airlines, covering Economy, Premium Economy, Business, and First Class across a wide range of routes and review dates (2020–2024). Each review includes sub-scores for **Seat Comfort**, **Staff Service**, **Food & Beverages**, **Inflight Entertainment (IFE)**, and **Value For Money**, plus an **Overall Rating** (1–10) and a binary **Recommended** (yes/no) label.

Approximately **65–70% of reviews are "yes"** (recommend) and **30–35% are "no"** (do not recommend). The "no" group is the analytical focus for improvement.

---

## 2. What Distinguishes Non-Recommending Reviews

### 2.1 Sub-Score Profile: "no" vs. "yes" Reviews

Scanning the raw data, a clear pattern emerges:

| Sub-dimension | Typical score in "yes" reviews | Typical score in "no" reviews |
|---|---|---|
| Staff Service | 4–5 (strong) | 1–4 (mixed) |
| Seat Comfort | 3–5 | 1–3 (often 1) |
| Food & Beverages | 3–5 | 1–3 |
| Inflight Entertainment | 3–5 | 1–4 |
| **Value For Money** | **4–5** | **1–2 (most consistently low)** |
| Overall Rating | 7–10 | 1–4 |

**Value For Money is the single most consistently low sub-score among non-recommenders**, appearing as 1 or 2 in the vast majority of "no" reviews. This is a cross-class pattern but is especially prominent in Economy and Premium Economy.

### 2.2 Staff Service Is the Bright Spot — Even in "no" Reviews

Notably, **Staff Service scores of 4 or 5 appear in many "no" reviews** (e.g., rows 3, 9, 25, 27, 33, 34, 37, 45, 49, 83, 95, etc.), meaning passengers frequently praise cabin crew warmth even when they decline to recommend the airline. This confirms that **ground service failures, operational problems, and product quality are driving non-recommendation more than cabin crew performance**.

### 2.3 Seat Comfort Is the Dominant In-Cabin Driver of "no"

The second most consistently depressed sub-score in "no" reviews is **Seat Comfort**. Recurring explicit complaints:
- **B737 MAX 8 seat narrowness** (reviews: rows 3, 7, 21) — hard seats, tight armrests, inadequate padding, back pain on flights >2 hours.
- **Staggered Business Class seats** (rows 85, 87, 93, 230, 243) — the angled lie-flat design forces sleeping at an uncomfortable angle; several reviewers explicitly prefer older non-staggered configurations.
- **Economy seat pitch / foot-box obstructions** (rows 128, 136) — boxes under seats reduce leg space.
- **Premium Economy** seat quality perceived as equivalent to Economy, undermining the value proposition (rows 55, 65, 146, 168).

### 2.4 Food & Beverages: Post-COVID Decline Is a Recurring Theme

Food complaints in "no" reviews are among the most narrative-rich. Key patterns:
- **Perceived post-COVID quality decline**: Portion sizes reduced, amenity kits removed, pre-meal drinks and hot towels eliminated (rows 86, 101, 116, 204, 211, 229, 248). Multiple long-tenure passengers explicitly state "this is not the Singapore Airlines I knew."
- **Business Class food not meeting premium expectations**: Rubbery eggs, microscopic cheese plates, limited wine pours, poor wine selection, cardboard box servings on premium cabins (rows 96, 107, 192, 200, 211).
- **Special dietary meal failures**: Gluten-free, vegan, Hindu non-veg, halal meals frequently miscatered or unavailable (rows 83, 103, 176, 213, 225).
- **Short-haul meal stinginess**: Very limited meals on regional flights; no IFE on some short-haul aircraft (rows 31, 231).

### 2.5 Operational and Ground-Service Failures Drive the Most Negative Reviews

The lowest overall ratings (1–2) in "no" reviews almost always involve operational failures rather than purely in-flight experience:
- **Mishandled connection delays / denied compensation** (rows 9, 34, 45, 95, 114, 215)
- **Baggage loss, damage, or delayed delivery with poor follow-up** (rows 44, 69, 70, 75, 173, 184)
- **Customer service inaccessibility** — 1–4 hour phone hold times, unanswered emails, call-centre staff unable to resolve issues (rows 30, 51, 75, 109, 155, 222, 234, 239, 247, 249, 251)
- **Check-in or ground staff errors / rudeness** (rows 25, 37, 119, 133, 162, 167)
- **Overbooking / seat assignment failures** (rows 40, 130, 221)

These ground-side failures generate the most severe "no + Overall Rating ≤ 2" combinations in the data.

---

## 3. Class-Level Breakdown

### Economy Class
- Largest volume of "no" reviews.
- Main drivers: seat comfort (cramped seats on certain aircraft), food quality/quantity decline, Value for Money (premium price, budget-airline execution).
- Notable bright spot: Staff Service scores remain 4–5 in many Economy "no" reviews.

### Premium Economy
- Non-recommenders uniformly cite the **value gap**: food indistinguishable from Economy, same Economy toilets, no amenity kit proactively offered, hard/uncomfortable seats on some A380 PE cabins (rows 55, 65, 146, 168, 174).
- Actionable: PE needs differentiated food, dedicated lavatory access, and proactive amenity distribution to justify the ~50–100% fare premium.

### Business Class
- "No" reviews split between: (a) food/product quality below expectations (the main theme), and (b) operational/billing/service recovery failures.
- Seat comfort complaints specific to staggered configurations on A380 and older regional seats.
- Food perceived as declining severely post-COVID — wine portions, no amenity kits proactively, reduced menu choice.

---

## 4. Factors That Are Evidentially Weak or Ambiguous

- **Inflight Entertainment (IFE)**: Scores are more stable across "yes" and "no" reviews. IFE is rarely the sole driver of non-recommendation; it appears as a secondary complaint only.
- **Wi-Fi**: Mentioned frequently (free for Krisflyer, unreliable in some reviews) but not a primary binary determinant of recommendation.
- **Type of Traveller**: Solo, Couple, Family, and Business travellers all appear in both "yes" and "no" groups. No strong causal pattern by traveller type is visible in the raw data without formal aggregation.
- **Route length**: Long-haul "no" reviews tend to be more severe (more hours to suffer poor seats/food), but there are also severe "no" reviews on short regional routes (mainly due to missing IFE, poor meals, or ground failures).

---

## 5. Prioritised Improvement Recommendations

Based on concrete patterns in the data, ranked by frequency and severity of impact on the "no" group:

### Priority 1 — Restore Perceived Value for Money (cross-class)
- **Value For Money is the #1 driver of non-recommendation.** Restoring pre-COVID amenities (hot towels, amenity kits, proactive drinks runs, printed menus, proper portions) even partially would directly address the most cited gap between brand promise and delivered experience.
- Business Class: Restore course-by-course service standards, proper wine pours, cheese plates with ≥3 options, and proactive amenity kit distribution.

### Priority 2 — Fix Seat Comfort on High-Complaint Aircraft
- **Retire or remediate the B737 MAX 8 seat configuration** for flights >2 hours; its seat narrowness is the leading cause of single-digit ratings on regional routes.
- Address the staggered Business Class lie-flat angle issue — customer communication should clearly explain the configuration; ideally phase in more symmetric flatbeds.
- Premium Economy: Evaluate A380 PE seat redesign; current hard vinyl PE seat on A380 is a documented recommendation-killer.

### Priority 3 — Fix Customer Service Accessibility and Recovery
- **Inaccessible call centres** (1–4 hour hold times, unanswered emails) are the primary driver of the most extreme negative ratings (Overall 1–2, Recommended = no).
- Invest in digital self-service (online rebooking, automated compensation processing) and a responsive complaints escalation path.
- Improve baggage handling response and compensation workflows — lost/damaged baggage with no follow-up is a recurring pattern.

### Priority 4 — Improve Special Dietary Meal Reliability
- Multiple "no" reviews (rows 83, 176, 213, 225) specifically cite dietary meal failures. A gluten-free passenger receiving no suitable food on an 18-hour flight is a recoverable failure that was not recovered.
- Systematic pre-flight verification of special meal loading should be prioritised.

### Priority 5 — Elevate Premium Economy Differentiation
- Premium Economy "no" reviews uniformly describe paying a 50–100% premium for Economy-equivalent food, shared lavatories, and no proactive service. This is a distinct and addressable product gap.

---

## 6. Caveats

- This analysis is based on qualitative review text and ordinal sub-scores; no regression or causal inference was performed. Correlations between sub-scores and recommendation are inferred from visible patterns in the raw data.
- Review sentiment may skew negative (dissatisfied passengers are more motivated to write). The ~65–70% recommendation rate likely underestimates silent satisfied passengers.
- Many high-scoring positive reviews (Overall = 10, Recommended = yes) also note food quality decline or amenity cuts as minor negatives, suggesting even satisfied customers perceive the same trends — making these improvements relevant beyond the "no" group.
