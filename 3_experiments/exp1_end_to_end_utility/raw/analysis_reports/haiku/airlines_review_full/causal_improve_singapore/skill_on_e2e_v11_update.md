---
dataset: airlines_review_full
scenario: causal_improve_singapore
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "overall_rating_recommendation"
query: "How can Singapore Airlines improve its overall rating and recommendation rate, especially on flights where passengers do not recommend it (Recommended = no)?"
source_table: augment_table/airlines_review_full/causal_improve_singapore/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-08-03T05:50:36.285848+00:00
wall_seconds: 164.94
---

# Singapore Airlines Improvement Strategy: Addressing Non-Recommended Passengers

## Executive Summary

This analysis examines 8,100 Singapore Airlines passenger reviews to identify strategic levers for improving overall rating and recommendation rates, with focus on the 3,813 non-recommended reviews (47.1% of sample). The data reveals that unfavorable recommendations are driven primarily by **cold/robotic crew service**, **poor perceived value**, and **communication failures**, combined with insufficient service recovery practices. Key improvement opportunities are actionable and quantifiable.

## Key Findings

### 1. Scale and Severity of Non-Recommendation

- **Non-recommended reviews**: 3,813 (47.1% of 8,100 reviews)
- **Mean Overall Rating (non-recommended)**: 2.37 / 10
- **Mean Overall Rating (recommended)**: 8.53 / 10
- **Rating gap**: 6.16 points—a critical divergence indicating distinct experience quality levels

### 2. Top Driver: Crew Service Quality and Warmth

The most pronounced difference between recommended and non-recommended passengers appears in the **crew_service_quality** TAPP-generated facet:

| Crew Service | Not Recommended | Recommended |
|---|---|---|
| Cold/Robotic | 84.6% (3,227 cases) | 7.5% |
| Attentive/Friendly | 4.9% (188 cases) | 83.6% |

**Cross-check with structured data**: Mean *Staff Service* rating is 3.23 for non-recommended vs. 3.87 for recommended (—0.64 point gap), confirming semantic segmentation validity.

**Impact**: Non-recommended passengers perceiving cold crew average 1.89 rating when combined with communication failure (59.8% of non-rec), compared to 4.96 for those perceiving responsive crew across all passenger categories.

### 3. Value Perception Crisis

Value For Money emerges as the most severe problem:

| Value Rating | Non-Rec Count | % of Non-Rec | Avg Overall Rating |
|---|---|---|---|
| 1 (Extremely poor) | 2,093 | 54.9% | **1.49** |
| 2 | 833 | 21.8% | 2.82 |
| 3 | 667 | 17.5% | 3.84 |

Of the 2,093 passengers rating value as 1/5, **92.8% perceive cold/robotic crew behavior**. This suggests that poor crew warmth directly degrades perceived value, not just price-quality ratio.

**Structured evidence**: Mean Value For Money rating is 1.75 for non-recommended vs. 4.39 for recommended (—2.64 point gap—the largest gap among all dimensions).

### 4. Communication Failure as Amplifying Factor

**Communication Failure** (TAPP-generated) appears in 2,512 of 3,813 non-recommended reviews (65.9%):

- **Communication Failure + Cold Crew co-occurrence**: 2,279 cases (59.8% of non-rec)
  - Average Overall Rating: **1.89**
  - This represents the worst single combined problem
- **Communication Failure alone (among non-rec)**: 65.9%

**Interpretation**: Passengers do not feel informed, heard, or engaged. Combined with perceived crew indifference, this creates a compounding negative effect on ratings.

### 5. Ground Service and Escalation Failures

**Ground Service Failure** (TAPP-generated) is prevalent in non-recommended:

- **Ground Service Failure = True**: 2,767 cases (72.6% of non-rec)
- **Ground Service Failure + Unresponsive Customer Service**: 1,712 cases (44.9% of non-rec)
  - Average Overall Rating: **2.08**

This suggests check-in, baggage handling, and transfer management issues are compounded by inadequate customer service response, preventing remediation.

### 6. Operational Reliability Issues

**Operational Reliability** (TAPP-generated) failures affect 30.6% of non-recommended:

| Issue Type | Count | % of Non-Rec | Avg Rating |
|---|---|---|---|
| Major delay / missed connection | 515 | 13.5% | 1.72 |
| Cancellation | 355 | 9.3% | 1.72 |
| Baggage failure | 296 | 7.8% | 1.72 |
| Minor delay | 274 | 7.2% | — |

Even among non-recommended passengers with on-time reliable operations (51.4%, n=1,960), the average rating is only 2.74—suggesting that crew and service issues persist even when operations are sound.

### 7. Service Class Variations

Recommendation rates vary by class:

| Service Class | Recommendation Rate |
|---|---|
| Economy | 47.0% |
| Premium Economy | 56.6% |
| Business Class | 66.4% |
| First Class | 76.9% |

Among **non-recommended Economy** (2,918 cases):
- Cold/robotic crew: 88.1%
- Value For Money = 1: 57.5%
- Communication failure: 69.9%

Among **non-recommended Business** (706 cases):
- Cold/robotic crew: 73.4% (still majority, but lower than Economy)
- Value For Money = 1: 44.8%
- Communication failure: 53.7%

**Business class passengers tolerate product limitations better if crew is warm; Economy passengers do not.**

### 8. Route Complexity Impact

Recommendation rates decline sharply with route complexity:

| Route Type | Recommendation Rate |
|---|---|
| Hub transfer (Istanbul risk) | 7.5% |
| Single connection | 46.5% |
| Multi-leg tight | 52.1% |
| Long haul direct | 65.8% |
| Short haul direct | 67.3% |

Complex itineraries suffer from compounded operational and ground service failures. Among non-recommended passengers, communication failures increase on connection routes (difficulty tracking baggage, rebooking clarity, etc.).

### 9. Passenger Segment Disparities

| Segment | Recommendation Rate |
|---|---|
| Solo Leisure | 59.4% |
| Business | 50.1% |
| Couple Leisure | 48.8% |
| Family Leisure | 46.8% |
| Vulnerable/Elderly/Mobility | 0.0% (n=2) |

**Family Leisure** passengers (826 non-recommended) report disproportionate ground service failures (seat allocation, meal availability, crew inattention with children). **Business** segment non-recommended are primarily driven by customer service responsiveness and communication failures (complex rebooking needs, schedule changes).

### 10. Service Recovery Gap

Only 2.4% of non-recommended passengers (91 cases) received adequate service recovery:

- **Service Recovery = True**: Average Rating 3.52
- **Service Recovery = False**: Average Rating 2.32
- **Difference**: +1.20 points (52% improvement in perceived rating)

However, 97.5% of non-recommended passengers did not receive recovery, suggesting SIA is failing to capitalize on post-failure intervention opportunities.

---

## Product Quality and Physical State

**Product Quality** (TAPP-generated) distribution in non-recommended:

| State | Count | Avg Rating |
|---|---|---|
| Modern/Clean/Functional | 106 | 4.35 |
| Dated/Worn/Dirty | 615 | 2.79 |
| Broken/Malfunctioning | 97 | 2.19 |
| Adequate/Acceptable | 2,845 | 2.26 |

The bulk of non-recommended (74.6%) are categorized as "adequate/acceptable" in product state, yet still rate 2.26—revealing that physical product is insufficient compensation for poor crew behavior and communication. Conversely, the small cohort with modern/functional product reaches 4.35 despite other issues.

---

## Structural Recommendations

Based on TAPP semantic analysis combined with original structured evidence, Singapore Airlines should prioritize:

### **Priority 1: Crew Warmth & Engagement (Immediate Impact)**
- **Target**: Reduce "cold/robotic" crew rating from 84.6% to ≤50% of non-recommended reviews
- **Mechanism**: Crew training refresh on interpersonal warmth, proactive passenger engagement, consistency across fleet/routes
- **Expected outcome**: Moving 188 non-recommended cases to "attentive_friendly" level could shift average rating from 2.37 to ~3.5 (1.13-point gain)
- **Measurement**: Staff Service rating trend; crew_service_quality semantic tags in post-implementation reviews

### **Priority 2: Value Perception Through Transparency (High ROI)**
- **Target**: Reduce "Value = 1" cases (54.9%) by communicating pre-flight value propositions and in-flight service consistency
- **Mechanism**: 
  - Manage expectations on Economy: emphasize meal/beverage service, entertainment, cleanliness
  - Premium/Business: reinforce personalization, recovery protocols, lounge access
  - Communicate pricing rationale (fuel, route, seasonality) to business segment
- **Expected outcome**: Shifting 10% of "Value = 1" cases to "Value = 2" could add 0.5–1.0 point on overall rating
- **Measurement**: Value For Money trend; qualitative coding for pricing/expectation mentions

### **Priority 3: Communication & Information Access (Systemic)**
- **Target**: Reduce communication_failure from 65.9% to ≤40% of non-recommended
- **Mechanism**: 
  - Proactive SMS/app notifications for delays, baggage, rebooking
  - Ground staff training on consistent messaging
  - Clear signage/digital info at hub transfers (especially for tight connections)
  - Pre-flight clarity on meal/entertainment/amenity options
- **Expected outcome**: 59.8% with combined communication + cold crew could improve 0.5–1.0 point if communication improves alone
- **Measurement**: communication_failure semantic tag; support ticket volume for "I didn't know" complaints

### **Priority 4: Ground Service & Escalation (Operational Rigor)**
- **Target**: Reduce ground_service_failure from 72.6% to ≤50% of non-recommended; escalation_difficult from 29.7% to ≤15%
- **Mechanism**: 
  - Seat allocation: honor paid selections; real-time rebooking logic must preserve family/couple groupings
  - Baggage: RFID tracking, proactive customer updates, no-cost delivery for delays >8 hours
  - Escalation: empower frontline managers (airport, customer care) to approve vouchers/rebooking without 24-hour delay
- **Expected outcome**: 44.9% with ground + unresponsive could improve 0.5–0.8 point if escalation responsiveness increases
- **Measurement**: ground_service_failure semantic tag; baggage delay complaints; first-contact resolution rate

### **Priority 5: Service Recovery Protocol (Tactical)**
- **Target**: Increase service_recovery_adequacy from 2.4% to ≥15% of non-recommended (achievable post-failure)
- **Mechanism**: 
  - Mandatory recovery offer framework: seat/equipment issue → seat upgrade or voucher; operational delay >2 hrs → meal/lounge voucher + rebooking priority; missed connection → hotel + rebooking + meal
  - Crew authority to offer on-board recovery (beverage upgrade, seat move, dining priority)
  - Follow-up within 48 hours for all major complaints
- **Expected outcome**: Each recovered case moves from 2.32 to 3.52 (1.20-point gain); scaling to 15% would lift non-recommended average by 0.15–0.20 points
- **Measurement**: service_recovery_adequacy semantic tag; complaint resolution rate; NPS change in post-recovery cohorts

### **Priority 6: Route/Complexity-Specific Protocols**
- **Target**: Improve recommendation rate on hub transfers from 7.5% to ≥25% and single connections from 46.5% to ≥60%
- **Mechanism**: 
  - Enhanced ground coordination in Singapore (baggage automation, priority transfer lane for misconnects)
  - Dedicated crew training for multi-segment itineraries (clear rebooking info, baggage reassurance)
  - Predictive rebooking for tight connections (offer rebooking 24 hrs pre-flight if risk detected)
- **Expected outcome**: Hub transfer improvements could lift 400–500 reviews into recommended category (~0.6–0.8 overall rating points at scale)
- **Measurement**: route_complexity_and_transfer_risk semantic tag; connection success rate; baggage delivery on-time rate

### **Priority 7: Economy Segment Customization**
- **Target**: Improve Economy recommendation rate from 47.0% to ≥55% (8-point lift)
- **Mechanism**: 
  - Product quality investment: refresh interiors on B737 MAX (currently rated lowest), upgrade IFE systems
  - Crew: assign most experienced/warm staff to Economy (currently 88.1% cold perception vs. 73.4% Business)
  - Meal: guarantee variety (chicken, fish, vegetarian) with pre-selection option
- **Expected outcome**: Economy serves 2,918 non-recommended passengers (76% of non-rec base); 8% shift = 234 moved to recommended, ~0.2 point overall gain
- **Measurement**: Seat Comfort, Staff Service, Food & Beverages trend; crew_service_quality tag for Economy

---

## Method Note

**TAPP-Generated Columns Used in Analysis**:
- `crew_service_quality` – Classifies crew demeanor: attentive/friendly vs. cold/robotic vs. inconsistent
- `customer_service_responsiveness` – Classifies responsiveness: responsive/proactive vs. unresponsive/dismissive vs. escalation_difficult
- `communication_failure` – Binary indicator: True if passengers report being uninformed or unclear on policies/procedures
- `ground_service_failure` – Binary indicator: True if check-in, baggage, or transfer issues reported
- `service_recovery_adequacy` – Binary indicator: True if airline offered remedy (voucher, upgrade, rebooking) that passenger deemed sufficient
- `operational_reliability` – Classifies operational outcome: on_time_reliable, minor_delay, major_delay_missed_connection, cancellation, baggage_failure
- `product_quality` – Classifies aircraft/cabin state: modern_clean_functional, adequate_acceptable, dated_worn_dirty, broken_malfunctioning
- `seat_comfort_deficiency` – Binary indicator: True if seat comfort issues noted in review
- `food_beverage_quality_deficiency` – Binary indicator: True if meal/beverage quality issues noted
- `passenger_segment` – Classifies traveler type: solo_leisure, couple_leisure, family_leisure, business, vulnerable_elderly_mobility
- `service_class` – Ticket class: economy_class, premium_economy, business_class, first_class
- `route_complexity_and_transfer_risk` – Classifies route type: short_haul_direct, long_haul_direct, single_connection, multi_leg_tight, hub_transfer_istanbul_risk

These columns were used to **identify semantic clusters** of failure modes and their co-occurrence, then validated against original structured ratings (Seat Comfort 1–5, Staff Service 1–5, Value For Money 1–5, Overall Rating 1–10, Recommended yes/no) to ensure accuracy and non-redundancy.

---

## Conclusion

Singapore Airlines' non-recommendation rate (47.1%) is primarily driven by a **combination of crew warmth, perceived value, and communication gaps**—not product defects. The most damaging pattern is **cold/robotic crew (84.6%) combined with communication failure (59.8%)**, yielding an average rating of 1.89. 

By prioritizing crew engagement training, value communication transparency, information accessibility, and service recovery protocols—while maintaining operational reliability—SIA can realistically move **600–1,000 non-recommended passengers per quarter into the recommended category**, lifting overall recommendation rate from 52.9% to 57–60% within 12 months. This would restore SIA's "world's best airline" positioning among high-satisfaction cohorts while defending against budget-carrier encroachment in Economy.
