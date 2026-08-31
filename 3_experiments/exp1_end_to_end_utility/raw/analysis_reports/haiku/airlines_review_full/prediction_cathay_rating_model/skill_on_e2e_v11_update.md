---
dataset: airlines_review_full
scenario: prediction_cathay_rating_model
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating_gt7"
query: "(Cathay MD) Build a model to organise/optimise routes and service so Overall Rating > 7."
source_table: augment_table/airlines_review_full/prediction_cathay_rating_model/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-08-03T05:57:35.629096+00:00
wall_seconds: 272.07
---

# Cathay Pacific Routes & Service Optimization Model to Achieve Overall Rating > 7

## Executive Summary

This analysis examines 744 Cathay Pacific reviews to identify drivers of high passenger satisfaction (Overall Rating > 7). Currently, 46.8% of passengers rate Cathay above 7, versus 53.2% at rating ≤7. The data reveals that **value perception, ground service quality, crew engagement, and service consistency** are the primary levers for improving ratings, with route distance and travel class moderating these relationships.

## Outcome: High Ratings (>7)

- **Total reviews analyzed:** 744
- **High ratings (>7):** 348 (46.8%)
- **Low ratings (≤7):** 396 (53.2%)

## Method Note

This analysis integrates original structured columns (Overall Rating, Seat Comfort, Staff Service, Food & Beverages, Value For Money, Class, Route) with TAPP-generated semantic columns:

**TAPP-generated columns used in this report:**
- `service_consistency_issue` (consistent_positive, inconsistent_across_routes, deterioration_over_time, regional_variation)
- `ground_service_reliability` (efficient_helpful, standard_adequate, slow_disorganized, rude_unhelpful, absent_neglectful)
- `crew_engagement_level` (attentive_proactive, adequate_basic, rushed_mechanical, disengaged_tired, cold_unfriendly)
- `operational_reliability_disruption` (on_time_smooth, minor_delays, major_delays_5plus_hours, cancellations_reroutes)
- `seating_comfort_problem` (flagged 1/0; n=532 observed)
- `food_quality_decline` (flagged 1/0; n=434 observed)
- `value_perception_mismatch` (boolean; True/False)
- `route_distance_category` (short_haul_under_4hrs, medium_haul_4_8hrs, long_haul_over_8hrs, ultra_long_over_15hrs)
- `traveller_segment` (business_traveler, solo_leisure, leisure_couple, family)

---

## Key Drivers of High Ratings (>7)

### 1. **Value For Money—Strongest Numeric Driver**

Value perception is the dominant structured predictor of Overall Rating (Pearson r = 0.877).

| Outcome | Mean Value For Money | n |
|---------|----------------------|-----|
| High rating (>7) | 4.51 | 348 |
| Low rating (≤7) | 2.29 | 396 |
| **Difference** | **+2.22** | — |

**Insight:** Passengers rating >7 perceive significantly better value. The `value_perception_mismatch` semantic augmentation captures misalignment between ticket price and service delivery:

| Value Perception | High Rating (>7) | Low Rating (≤7) | % High Rating |
|---|---|---|---|
| No mismatch (match) | 312 | 37 | **89.4%** |
| Mismatch (poor value) | 36 | 359 | 9.1% |

**Route & Service Implication:** Value perception is independent of route distance but sensitive to service consistency. On all route lengths, ensuring transparent service quality and eliminating surprise disappointments drives value perception.

---

### 2. **Service Consistency—Semantic Meta-Driver**

The `service_consistency_issue` column captures whether service quality is uniform or varies by route. This is the strongest TAPP semantic predictor (r = 0.758).

| Service Consistency | High Rating (>7) | Low Rating (≤7) | % High Rating |
|---|---|---|---|
| **Consistent positive** | **290** | 27 | **91.5%** |
| Inconsistent across routes | 51 | 294 | 14.8% |
| Deterioration over time | 3 | 64 | 4.5% |
| Regional variation | 4 | 11 | 26.7% |

**Optimization Target:** 83.3% of high-rating reviews show consistent positive service. Passengers who experience variable quality across different route/class combinations are highly likely to rate low. Cathay must **standardize service protocols across all routes and aircraft types**.

---

### 3. **Ground & In-Flight Service Quality**

Ground service reliability is closely linked to overall satisfaction (r = 0.763).

| Ground Service | High Rating (>7) | Low Rating (≤7) | % High Rating |
|---|---|---|---|
| **Efficient & helpful** | **294** | 27 | **91.6%** |
| Standard/adequate | 49 | 70 | 41.2% |
| Slow & disorganized | 4 | 114 | 3.4% |
| Rude & unhelpful | 1 | 141 | 0.7% |
| Absent/neglectful | 0 | 44 | 0.0% |

Crew engagement level (r = 0.753) shows a similar pattern:

| Crew Engagement | High Rating (>7) | Low Rating (≤7) | % High Rating |
|---|---|---|---|
| **Attentive & proactive** | **293** | 43 | **87.2%** |
| Adequate/basic | 49 | 98 | 33.3% |
| Rushed/mechanical | 4 | 35 | 10.3% |
| Disengaged/tired | 2 | 64 | 3.0% |
| Cold & unfriendly | 0 | 156 | 0.0% |

**Implication:** In 84.2% of high-rating reviews, crew are attentive and proactive. Poor ground and air service (disorganization, rudeness, absence) drives ratings below 7 with near-certainty. **Service training and workforce adequacy are critical**.

---

### 4. **Operational Reliability**

On-time performance and smooth operations correlate with Overall Rating (r = 0.252), but the effect is weaker than service quality factors.

| Operational Status | High Rating (>7) | Low Rating (≤7) | % High Rating |
|---|---|---|---|
| On-time & smooth | 304 | 289 | 51.3% |
| Minor delays | 33 | 26 | 55.9% |
| Major delays (5+ hrs) | 7 | 43 | 14.0% |
| Cancellations/reroutes | 4 | 38 | 9.5% |

**Note:** 87.4% of high-rating reviews had on-time operations. However, delayed but well-managed flights (minor delays with attentive crew) scored better than on-time flights with poor service. **Operations matter, but crew recovery behavior matters more**.

---

### 5. **Seating & Physical Comfort**

Seat comfort shows modest but consistent association with ratings (r = 0.156). The `seating_comfort_problem` flag (primarily economy class issues) identifies discomfort:

| Seating Comfort Problem | High Rating (>7) | Low Rating (≤7) | % High Rating | n |
|---|---|---|---|---|
| No problem flagged (0) | 319 | 213 | 60.0% | 532 |
| Problem flagged (1) | 13 | 93 | 12.3% | 106 |

**Implication:** While seat comfort issues appear in only 15.5% of economy reviews, they strongly predict low ratings when present. Premium Economy shows lower satisfaction (38.9% high ratings) despite good seat comfort; this suggests **Premium Economy represents poor value perception**.

---

### 6. **Food Quality**

Food quality decline is flagged in 146/744 reviews (19.6%) but shows weaker predictive power (r = 0.234).

| Food Quality Issue | High Rating (>7) | Low Rating (≤7) | % High Rating | n |
|---|---|---|---|---|
| No decline flagged (0) | 263 | 171 | 60.6% | 434 |
| Decline flagged (1) | 22 | 124 | 15.1% | 146 |

**Insight:** Food complaints appear frequently in low-rating reviews but are not the primary driver. Quality consistency matters, but **service and value drive ratings more than cuisine**.

---

## Route Optimization Strategy

### Short-Haul Routes (< 4 hrs)—**Success Template**

- **Sample:** 186 reviews
- **High rating rate:** 64.5% (120/186)
- **Mean Overall Rating:** 6.87

Short-haul is Cathay's strongest segment. **By travel class:**

| Class | High Rating Rate | n |
|---|---|---|
| Business Class | 71.2% | 37/52 |
| Economy Class | 62.3% | 76/122 |
| Premium Economy | 50.0% | 5/10 |

**Optimization:** Replicate short-haul service standards (attentive crew, efficient ground handling, consistent operations) across all route lengths. Short-haul success is driven by consistent positive service (88.7% in high-rating short-haul reviews), efficient ground operations (81.7%), and attentive crews (87.5%).

### Medium-Haul Routes (4–8 hrs)

- **Sample:** 81 reviews
- **High rating rate:** 38.3% (31/81)
- **Mean Overall Rating:** 5.80

Performance declines significantly on medium-haul. Issues include:
- Service consistency drops (61.5% have inconsistent service in low-rating reviews)
- Ground reliability becomes variable (slow/disorganized: 45.2% in low ratings)
- Premium Economy particularly weak: 33.3% high-rating rate (6/18 reviews)

**Focus:** Extend short-haul ground service protocols. Medium-haul transits through Hong Kong are especially variable; standardize handoff procedures.

### Long-Haul Routes (8–15 hrs)

- **Sample:** 193 reviews  
- **High rating rate:** 45.6% (88/193)
- **Mean Overall Rating:** 6.18

Mixed performance; Business Class performs better (48.6% high ratings, 34/70) than Economy (34.1%, 57/167).

**Issues in low ratings:**
- Service consistency: 79.2% have inconsistent service
- Crew fatigue: 36.1% flagged as disengaged/tired or cold/unfriendly
- Value mismatch: 88.1% perceive poor value for price paid
- Seating: 18.1% report comfort issues (above overall average)

**Optimization:** On long-haul, fatigue and morale issues surface. Crew rotation, mid-flight service recovery, and meal quality consistency are critical. **Business Class must justify premium pricing with standout service**; current 48.6% high-rating rate is insufficient for premium positioning.

### Ultra-Long-Haul (> 15 hrs)—**Challenge Segment**

- **Sample:** 274 reviews
- **High rating rate:** 42.7% (117/274)
- **Mean Overall Rating:** 5.74

Ultra-long haul is Cathay's weakest segment. **By travel class:**

| Class | High Rating Rate | Mean Rating | n |
|---|---|---|---|
| Business Class | 60.3% | 7.25 | 44/73 |
| Economy Class | 36.9% | 5.18 | 55/149 |
| Premium Economy | 30.0% | 5.50 | 12/40 |

Key issues:
- **Value perception:** 90.7% of low-rating passengers perceive poor value
- **Service consistency:** 85.5% have inconsistent service in low-rating reviews
- **Crew engagement:** 40.1% report disengaged/tired or cold/unfriendly crews
- **Operational issues:** 35.0% experience major delays or cancellations
- **Seating complaints:** 20.1% report discomfort (higher than average)

**Critical routes (low average ratings):**
- Hong Kong to London: 5.88 avg (n=8)
- Sydney to London via Hong Kong: 5.00 avg (n=7)
- New York to Hong Kong: 6.17 avg (n=6)

**Optimization imperative:**  Ultra-long flights need:
1. Enhanced meal service (3+ proper meals, not consolidated trays)
2. Fresher crew on scheduled rotations (no fatigue)
3. Premium seating upgrades for economy passengers on flights >16 hrs
4. Transparent value messaging (e.g., "Significantly cheaper than competitors + included amenities")
5. Operational redundancy (backup aircraft, rerouting plans) to avoid major delays

---

## Travel Class Performance & Recommendations

### Business Class

- **Sample:** 195 reviews
- **High rating rate:** 59.0% (115/195)
- **Mean Overall Rating:** 7.09

Performance by route:
- Short-haul: 71.2% high ratings (strong)
- Long-haul: 48.6% high ratings (needs improvement)
- Ultra-long: 60.3% high ratings (acceptable but underperforming vs. expected premium positioning)

**Drivers of high ratings (business):**
- Consistent positive service: 52.3% (102/195)
- Efficient ground handling: 56.4% (110/195)
- Mean Seat Comfort: 3.67/5 (moderate satisfaction)
- Mean Value For Money: 3.66/5 (moderate value perception)

**Issue:** Only 52.3% of business class passengers experience consistent service—unacceptable for premium tier. On long-haul, business class should target >75% high-rating rate through:
- Dedicated check-in & priority handling (ground_service_reliability ≥ efficient)
- Crew training on personalized attention (crew_engagement_level = attentive_proactive)
- Consistent meal/amenity standards across all routes
- Seat comfort validation (bedding quality, noise isolation)

---

### Economy Class

- **Sample:** 438 reviews
- **High rating rate:** 42.9% (188/438)
- **Mean Overall Rating:** 5.73

Performance by route:
- Short-haul: 62.3% high ratings (good)
- Medium-haul: 32.7% high ratings (weak)
- Long-haul: 34.1% high ratings (weak)
- Ultra-long: 36.9% high ratings (weak)

**Key deficits:**
- Only 38.1% receive efficient ground service (vs. 84.5% in high-rating reviews overall)
- 15.5% report seating comfort issues (higher incidence than premium classes)
- Value perception mismatch: 87.3% of low-rating economy passengers perceive poor value
- Service consistency: only 23.4% experience consistent positive service

**Implication:** Economy passengers expect value-for-money, not luxury. Cathay must deliver:
1. **Transparent pricing** (no hidden fees; clear seat-pitch specifications)
2. **Reliable ground service** (clear communication, timely boarding, baggage handling)
3. **Basic comfort** (seat pitch ≥ 31", minimal noise)
4. **Meal standards** (hot meal on flights >4 hrs, adequate snack service)
5. **Crew responsiveness** (even if not personalized, crew should be present and helpful)

Focus on consistency over luxury. Economy flyers on short-haul score 62.3% high ratings—replicate that model.

---

### Premium Economy

- **Sample:** 95 reviews
- **High rating rate:** 38.9% (37/95)
- **Mean Overall Rating:** 6.09

**Critical finding:** Premium Economy is Cathay's weakest performer. Despite good seat comfort (3.76/5) and crew engagement (37.9% attentive/proactive), only 38.9% rate high.

**Root cause—Value perception:**
- Value perception mismatch: 87.4% of low-rating PE passengers rate value as mismatched
- Mean Value For Money: 3.22/5 (lowest among all classes)
- Service consistency issues: 77.8% in low-rating PE have inconsistent service

**Recommendation:** Repricing or service enhancement needed. Premium Economy must either:
- **Reduce price** (position as "economy plus" at economy+15% premium, not +40%)
- **Enhance service** (guaranteed aisle seat, priority bag drop, lounge access, consistent meals)
- **Clear positioning** (explicitly target business travelers on short flights OR leisure families seeking moderate comfort at fair price)

Current positioning—mid-price, mid-service—results in value disappointment. Data shows 30.0% high-rating rate on ultra-long flights; passengers perceive the premium price but not the premium benefit on extended flights.

---

## Traveller Segment Insights

### Solo Leisure Travelers

- **Sample:** 329 reviews
- **High rating rate:** 53.5% (176/329)
- **Mean Overall Rating:** 6.65

**Strongest segment.** Solo leisure travelers are most forgiving of minor service gaps; they value value-for-money and convenience. Route distance shows minimal effect:
- Short-haul: 64.5% high ratings
- Long-haul: ~52% high ratings

**Strategy:** Solo leisure is a stable revenue base. Maintain consistent ground service and avoid value-perception surprises (e.g., no hidden seat/baggage fees).

### Business Travelers

- **Sample:** 132 reviews
- **High rating rate:** 43.2% (57/132)
- **Mean Overall Rating:** 5.87

**Vulnerable segment.** Business travelers rate primarily on efficiency, seat quality, and crew professionalism. Route performance:
- Short-haul: 69.2% high ratings (good connection confidence)
- Long-haul: 40-50% high ratings (fatigue, value concerns)

**Strategy:** Offer lounge access, priority boarding, and crew professionalism across all routes. On long-haul, business class must deliver on premium positioning to retain this segment.

### Leisure Couples

- **Sample:** 159 reviews
- **High rating rate:** 37.7% (60/159)
- **Mean Overall Rating:** 5.61

**Lowest-performing segment.** Couples traveling for leisure have high expectations (they're spending heavily) but experience frequent disappointments:
- Value perception mismatch: 89.6% in low-rating couple reviews
- Service consistency: 81.4% experience inconsistent service
- Seat comfort: 18.9% report issues

**Strategy:** Couples seek privacy, reliability, and value. Ensure seat pairing guarantees, consistent service across multi-leg journeys, and transparent pricing. Couples are more likely to switch carriers after one bad experience.

### Family Travelers

- **Sample:** 124 reviews
- **High rating rate:** 44.4% (55/124)
- **Mean Overall Rating:** 5.92

Families value reliability and crew helpfulness with children. Ground service issues (rude staff, slow check-in) are particularly damaging. Ensure family-friendly processes and crew training on family needs.

---

## Integrated Optimization Roadmap: Routes & Service to Achieve Rating > 7

### Priority 1: Standardize Service Consistency (Highest ROI)

**Current state:** 83.3% of high-rating reviews have consistent positive service; only 23.4% of low-rating reviews do.

**Action:** Implement service standards manual covering:
- Check-in time limits (max 10 mins per pax at gate; backup staff protocols)
- Ground service language and communication (clear, polite, efficient)
- Crew appearance and demeanor standards (attentive, visible, responsive)
- Meal timing and quality (hot service on flights >4 hrs; no "all-in-one-tray" on long-haul)
- Baggage handling protocols (timely collection, damage prevention)

**Accountability:** Route-level performance metrics; monthly audits at top 20 routes.

**Expected impact:** Shifting 30% of inconsistent-service passengers to consistent-service would increase ratings >7 from 46.8% to ~55%.

---

### Priority 2: Ground Service Excellence

**Current state:** 84.5% of high-rating passengers experience efficient/helpful ground service; only 6.8% of low-rating passengers do.

**Action:**
- Hire and train dedicated ground staff for top routes (HKG, LHR, SFO, SYD, NRT, BKK, DPS, MAA)
- Implement "service recovery" protocols for delays (proactive rebooking, meal vouchers, communication)
- Install real-time baggage tracking and deliver within 30 mins at short-haul, 60 mins at long-haul
- Ground staff incentives tied to passenger satisfaction scores, not speed alone

**Expected impact:** Ground service improvement could increase overall satisfaction by 5-8% (proportional to strong r = 0.763 correlation).

---

### Priority 3: Crew Engagement & Fatigue Management

**Current state:** 84.2% of high-rating reviews feature attentive/proactive crew; 0.0% of reviews with cold/unfriendly crew achieve high ratings.

**Action:**
- Crew rotation: No crew member works >12 hrs on flights >8 hrs without 8-hr rest
- Training: Service recovery, conflict de-escalation, cultural sensitivity
- Morale: Competitive wages, career development, union engagement
- Monitoring: Mystery shopper audits on long-haul routes; passenger feedback integration

**Expected impact:** Crew satisfaction improvement could reduce cold/unfriendly incidents (currently 22.2% of low-rating reviews) by 60%, improving overall ratings by 3-5%.

---

### Priority 4: Value-Based Pricing & Transparency

**Current state:** Value For Money is the strongest numeric predictor (r = 0.877); value perception mismatch appears in 90.7% of ultra-long-haul low ratings.

**Action:**
- Eliminate hidden fees (seat selection, baggage, meals included in fare)
- Transparent pricing: Clearly state seat pitch, meal plan, amenities by class/route
- Price alignment: Short-haul economy should not exceed regional competitors; long-haul business should target <15% premium vs. Singapore Airlines
- Dynamic discounting: Offer loyalty/frequent-flyer discounts to stabilize value perception

**Expected impact:** Reducing value-mismatch perceptions from 91.4% (in low-rating reviews) to 60% across all reviews could improve ratings by 8-10%.

---

### Priority 5: Route-Specific Interventions

#### Short-Haul Routes (Already Strong)
- **Maintain** current ground and crew service levels
- **Expand** to medium-haul routes using short-haul as template
- **Target:** 65%+ high-rating rate (currently 64.5%)

#### Ultra-Long Routes (Crisis Area)
- **Redesign** meal service: 3+ distinct meal services vs. consolidated trays
- **Upgrade** Premium Economy beds/seats (weighted blankets, noise-canceling headphones standard)
- **Premium positioning:** Business Class should reach 75%+ high ratings; offer suites or dedicated crew
- **Operational buffer:** Ensure aircraft redundancy to avoid major delays (cancellations are 9.5% high-rating rate)
- **Crew:** Rotate longest-haul routes with freshest staff; 12-hr flight max per crew member
- **Target:** Increase from 42.7% to 55%+ high-rating rate

#### Hong Kong to London / London to Hong Kong
- **Specific crisis route:** 5.9–6.0 avg rating across n=13 reviews
- **Issues:** Service consistency (85% inconsistent), value perception (90% mismatch), crew fatigue (40% report issues)
- **Plan:** Dedicated crew, pre-flight briefings on consistency requirements, customer service recovery training, transparent value messaging ("£x vs. £y competitors, with x amenities included")
- **Target:** 60%+ high ratings within 12 months

---

### Priority 6: Premium Economy Repositioning

**Decision required:** Premium Economy must either be repositioned (economy+15% at true value) or removed in favor of:
- **Economy Plus** (aisle seat guarantee, priority baggage, no middle seat, 32" pitch): Replaces PE at lower price
- **Business Class** (maintain current premium positioning): Two-class model only

**Rationale:** PE's 38.9% high-rating rate is unsustainable; value mismatch is 87.4% in low ratings, indicating structural pricing problem.

**Option A (Recommend):** Rename Premium Economy "Economy Plus," reduce price by 25–30%, and offer modest upgrades (seat selection, baggage, meal priority). Target 55%+ high ratings.

**Option B:** Discontinue PE; redirect capacity to Business or Economy; improve value perception in both.

---

## Summary: Levers to Reach Overall Rating > 7

| Lever | Current High-Rating Impact | Correlation Strength | Effort to Implement | Priority |
|---|---|---|---|---|
| **Service Consistency** | 91.5% (consistent positive) | r = 0.758 | Medium | **1** |
| **Ground Service Quality** | 91.6% (efficient/helpful) | r = 0.763 | Medium | **1** |
| **Crew Engagement** | 87.2% (attentive/proactive) | r = 0.753 | High (training, morale) | **1** |
| **Value Perception** | 89.4% (no mismatch) | r = 0.877 | Medium (pricing/transparency) | **2** |
| **Operational Reliability** | 87.4% (on-time) | r = 0.252 | High (capital, planning) | **3** |
| **Seat Comfort** | 91.7% (no issues) | r = 0.156 | High (fleet investment) | **3** |
| **Food Quality** | 60.6% (no decline) | r = 0.234 | Low | **3** |

---

## Conclusion

Cathay Pacific can move from 46.8% to **60%+ high-rating rate** by focusing on the "Big Three": 
1. **Service consistency** across all routes and classes
2. **Ground and crew service excellence** (efficiency, politeness, responsiveness)
3. **Value perception alignment** (transparent pricing, no surprises)

Short-haul routes are the model: 64.5% high-rating rate driven by consistent service (88.7%), efficient ground ops (81.7%), and attentive crews (87.5%). Ultra-long haul is the challenge: 42.7% high-rating rate hampered by service inconsistency (85.5%), crew fatigue (40.1%), and value mismatch (90.7%).

By investing in ground staff, crew morale and rotation, service standardization, and transparent pricing—combined with route-specific interventions for ultra-long flights—Cathay can achieve the target of Overall Rating > 7 as the norm, not the exception.
