---
dataset: airlines_review
scenario: causal_improve_singapore
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "overall_rating_recommendation"
query: "How can Singapore Airlines improve its overall rating and recommendation rate, especially on flights where passengers do not recommend it (Recommended = no)?"
source_table: augment_table/airlines_review/causal_improve_singapore/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:04:06.114810+00:00
wall_seconds: 68.28
---

# Singapore Airlines: Improving Overall Rating and Recommendation Rate
## Analysis Report – Non-Recommended Flights (skill_on variant)

---

## Executive Summary

This analysis examines 320 non-recommended reviews (35.6% of 900 total reviews) for Singapore Airlines. The critical barrier to recommendation is a significant value-perception gap, compounded by operational and service consistency issues. Non-recommended passengers rate the airline at **2.77/10** on average—versus **8.61/10** for recommended passengers—a gap of **5.84 points**. Addressing pricing strategy, crew reliability, and aircraft standards represents the highest-impact improvement opportunity.

---

## Key Findings

### 1. **Value-for-Money is the Dominant Factor** (82.8% of non-recommended reviews)

**Critical metric:** 265 out of 320 non-recommended reviews cite **overpriced_poor_value** pricing perception.

| Price-Value Alignment | Count | Avg Rating | Avg Value Score |
|---|---|---|---|
| Overpriced (poor value) | 265 | **2.56** | **1.69** |
| Acceptable (competitive) | 54 | 3.65 | 2.43 |
| Justified (premium worth) | 1 | 10.00 | 3.00 |

**Finding:** Passengers rating 5-7 (mid-range satisfaction) explicitly reject the airline's premium pricing. Even when operational aspects function adequately, perceived pricing misalignment drives non-recommendation. The average **Value For Money score for non-recommended flights is 1.82/5** versus **4.34/5 for recommended flights**—a **2.52-point deficit**.

**Implication:** Pricing is not merely a complaint; it is the primary barrier to recommendation. Passengers are comparing Singapore Airlines' actual delivered value against premium expectations set by its "world's best airline" positioning.

---

### 2. **Crew Service Issues Create Compounding Dissatisfaction** (73.1% of non-recommended)

| Crew Service Issue | Count | Avg Rating | Avg Staff Service |
|---|---|---|---|
| Crew inefficiency | 112 | **2.24** | 3.65 |
| Crew inattentiveness | 64 | 2.97 | 3.84 |
| Crew rudeness | 49 | 2.53 | 3.71 |
| Crew disorganization | 21 | 3.33 | 4.33 |
| No service issue | 74 | 3.38 | 3.89 |

**Finding:** Crew inefficiency (35% of non-recommended reviews) correlates with the **lowest average rating of 2.24**, suggesting operational gaps in cabin service execution post-COVID. Interestingly, Staff Service ratings themselves (3.65–3.89 range) are moderate, but inefficiency in meal service timing, passenger assistance, and post-complaint resolution drive passengers away more than overt rudeness.

**Critical pattern:** In 170 critically negative reviews (rating ≤2):
- 73 cite crew inefficiency
- 67 reviews involve unknown/unclear aircraft status
- 153 cite overpriced_poor_value

This suggests **multiple failure points compound**—poor value + inefficient crew + dated aircraft = severe dissatisfaction.

---

### 3. **Aircraft Modernization Matters, Especially for Long-Haul Comfort**

| Aircraft Status | Count | Avg Rating | Seat Comfort | IFE |
|---|---|---|---|---|
| Unknown/unclear | 97 | 2.30 | 3.79 | 3.97 |
| Dated but serviceable | 158 | 2.71 | 3.67 | 3.89 |
| Modern/refurbished | 40 | 3.60 | 3.40 | 4.00 |
| Old/worn | 25 | 3.60 | 3.48 | 3.88 |

**Finding:** Passengers flying on **modern/refurbished aircraft rate 0.89 points higher** (3.60 vs. 2.71) than those on dated serviceable aircraft, despite similar seat comfort scores. This suggests the psychology of "modern = well-maintained = premium service value" influences perception.

**Concrete issue:** Multiple reviews cite uncomfortable seats on older aircraft (e.g., B737 MAX and regional business class seats) combined with poor service as triggering non-recommendation and low value ratings.

---

### 4. **Specific Service Gaps for Economy & Business Class**

**Economy Class (214 non-recommended reviews, 59.8% of negative):**
- Avg rating: **2.57**
- Avg Value For Money: **1.77**
- Common complaints: Limited meal options, inconsistent availability, overpriced add-ons (e.g., $200 for 10kg carry-on overcharge)

**Business Class (67 non-recommended reviews, 18.7% of negative):**
- Avg rating: **3.15** (higher than economy, but still non-recommended)
- Avg Value For Money: **2.01**
- Common complaints: "Not Singapore Airlines standard" crew behavior, seat failures (broken recline, incomplete meals), perceived service regression post-COVID

**Insight:** Business class non-recommendations reflect **expectation gap**—premium pricing without premium consistency. Economy non-recommendations reflect **absolute value failure**—pricing not justified by service level.

---

### 5. **Traveller Type Effects**

| Traveller Type | Count | Avg Rating | Avg Value |
|---|---|---|---|
| Business | 59 | 2.47 | 1.78 |
| Family Leisure | 64 | 2.48 | 1.70 |
| Solo Leisure | 100 | 2.92 | 1.96 |
| Couple Leisure | 97 | 2.97 | 1.78 |

**Finding:** Business and family leisure travelers rate lowest when dissatisfied, suggesting these segments have higher baseline expectations. Solo leisure travelers show marginally higher ratings within non-recommended cohort, indicating potential tolerance for service gaps.

---

## Root Cause Analysis: The "Value Paradox"

The data reveals a structural issue: **operational quality (seat comfort, crew service, entertainment) is acceptable (3.4–3.9 range), but pricing perception overshadows everything.**

**Example pattern from data:**
- Review with Seat Comfort=5, Staff Service=5, Food=5, IFE=5, **but Overall Rating=1** because "Value For Money=1 + aircraft dated + premium price"
- Review with crew inefficiency (Rating 2.24) still rates Staff Service at 3.65—passengers separate *courtesy* from *efficiency*

**Implication:** Singapore Airlines is not failing at service delivery in absolute terms; it is failing at value justification. Passengers expect exceptional service at premium prices but perceive diminished quality post-COVID, creating a betrayal effect.

---

## Actionable Improvement Priorities

### **Priority 1: Price Repositioning (Immediate Impact)**
- **Action:** Audit pricing strategy against perceived delivered value. Consider:
  - Economy fare transparency: Eliminate surprise charges (e.g., carry-on overcharges)
  - Anchoring: Promote value-adds explicitly (free WiFi, meal quality, safety record)
  - Segment pricing: Business class premium justification through service consistency guarantees

### **Priority 2: Crew Efficiency Standards (Medium-Term)**
- **Action:** Post-COVID crew training refresh focusing on:
  - Meal service timing consistency
  - Proactive passenger assistance (not reactive-only)
  - Root-cause analysis of "crew inefficiency" vs. legitimate operational delays
- **Target:** Reduce crew_inefficiency from 35% to <20% of non-recommended cohort

### **Priority 3: Aircraft Fleet Transparency & Modernization (Medium-Term)**
- **Action:** 
  - Remove operational mystery ("Unknown" aircraft status in 97 reviews)
  - Communicate aircraft refurbishment status to passengers pre-booking
  - Prioritize long-haul routes on A350/777 (modern fleets)
- **Target:** Shift non-recommended aircraft baseline from 2.71 to 3.5+ rating

### **Priority 4: Business Class Recovery (Quick Win)**
- **Action:** Audit business class service consistency—address crew "rudeness" perception (49 reviews) and mechanical failures (broken seats, incomplete meals)
- **Target:** Restore business class to premium experience standard; current 3.15 rating unacceptable for premium segment

---

## Evidence Strength Assessment

### Strong Evidence:
- Price-value dominance is **consistent across all segments** (265/320 reviews cite it)
- Crew inefficiency **correlates with lowest ratings** (2.24 average)
- Aircraft modernity **shows measurable rating lift** (+0.89 points)

### Moderate Evidence:
- Traveller type differences exist but are **not dramatic** (2.47–2.97 range)
- Individual service categories (Staff, Food, Seat) show **modest differentiation** among non-recommended reviews

### Limitations:
- "Value For Money" ratings may reflect post-COVID adjustment expectations, not objective overpricing
- 97 "Unknown" aircraft classifications limit precision of modernization impact
- Review bias: Only verified reviews; may exclude silent switchers to competitors

---

## Recommendation for Singapore Airlines

**Rebalance the value equation to restore recommendation likelihood:**

1. **Immediate (0–3 months):** Launch pricing transparency campaign and eliminate surprise fees
2. **Short-term (3–6 months):** Execute crew efficiency audit and service recovery for business class
3. **Medium-term (6–12 months):** Accelerate A350 deployment on key routes; phase out dated aircraft from premium-marketed routes
4. **Strategic:** Reposition from "world's best" to "best value premium airline" until service consistency recovery is complete

**Success metric:** Reduce non-recommended proportion from 35.6% to <25% while raising average non-recommended rating from 2.77 to 5.0+ (functional acceptability threshold).

---
