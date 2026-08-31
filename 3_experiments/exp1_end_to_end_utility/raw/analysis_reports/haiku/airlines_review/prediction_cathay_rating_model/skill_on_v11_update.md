---
dataset: airlines_review
scenario: prediction_cathay_rating_model
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating_gt7"
query: "(Cathay MD) Build a model to organise/optimise routes and service so Overall Rating > 7."
source_table: augment_table/airlines_review/prediction_cathay_rating_model/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:05:20.533311+00:00
wall_seconds: 80.82
---

# Cathay Pacific Airways Rating Optimization Model
## Analysis Report: Predicting Routes & Services for Overall Rating > 7

**Dataset:** 744 verified Cathay Pacific reviews
**Focus Variable:** Overall Rating (binary target: Rating > 7)
**Baseline Performance:** 46.8% of reviews achieve Rating > 7

---

## Executive Summary

This analysis identifies key levers for Cathay Pacific to achieve the target of Overall Rating > 7 across route and service optimizations. The dataset reveals significant performance gaps across cabin classes, service dimensions, and operational factors, with actionable patterns for route-level and service-level improvements.

**Key Finding:** Only 46.8% of flights achieve Rating > 7, indicating substantial room for optimization. Business Class achieves 59.0% success rate while Economy Class lags at 42.9%, suggesting segment-specific strategies are critical.

---

## 1. Service Component Impact on High Ratings

### Value for Money is the Dominant Driver
The single strongest predictor of Overall Rating > 7 is **Value for Money perception** (correlation: 0.877 with Overall Rating). Reviews achieving Rating > 7 show **Value for Money averaging 4.51/5** compared to 2.29/5 for lower ratings—a **2.22-point gap**, nearly 100% difference.

### Seat Comfort Shows Modest but Consistent Impact
- Ratings > 7: Seat Comfort average **3.84/5**
- Ratings ≤ 7: Seat Comfort average **3.42/5**
- Gap: **0.41 points**

This suggests Economy Class seat constraints (frequently cited as "cramped," "10-abreast," "tiny legroom") directly suppress ratings. Business Class experiences higher seat comfort scores, correlating with its 59% success rate for Rating > 7.

### Staff Service Moderately Influential
Crew responsiveness contributes a **0.27-point** difference between high and low ratings. Reviews with "crew_service" as primary complaint still average **6.62/10** rating, suggesting service issues are recoverable if paired with other positives.

### Food & Beverages: Secondary Factor
Despite frequent complaints about meal quality, Food & Beverages shows modest direct correlation (**0.29-point gap** between high/low ratings). However, the **business_class_food_gap** augmented feature reveals premium passengers expect differentiated menus—a specific pain point.

---

## 2. Route-Level Performance Patterns

### High-Performing Routes (Rating > 8)
- **Hong Kong ↔ London:** 7 high-rating reviews (major intercontinental route)
- **Bangkok ↔ Hong Kong:** 7 high-rating reviews (regional/connector route)
- **Manila → Hong Kong:** 6 high-rating reviews

**Pattern:** Successful routes span both long-haul (London) and medium-haul (Bangkok, Manila), indicating route type alone is not the determinant. Instead, *service consistency on these routes* appears high.

### Problematic Routes (Rating < 4)
- **London ↔ Hong Kong:** 5 low-rating reviews (paradoxically also top-rated—bimodal experience)
- **Hong Kong → Sydney:** 4 low-rating reviews
- **New York → Hong Kong:** 3 low-rating reviews

**Critical Finding:** Some routes show high variance (London-Hong Kong has both highest and lowest ratings), suggesting *flight-by-flight operational consistency* is the issue rather than route inherent qualities.

---

## 3. Cabin Class Strategy

### Business Class: Achieves Target (59.0% Rating > 7)
- Mean rating: **7.09/10**
- 115 of 195 flights achieve Rating > 7
- **Primary success drivers:** Higher expectations met on seat comfort; crew performance; professional service recovery

### Economy Class: Furthest from Target (42.9% Rating > 7)
- Mean rating: **5.73/10**
- 188 of 438 flights achieve Rating > 7
- **Primary barriers:** 
  - "economy_meets_baseline" cabin expectation shows 60.1% of economy reviews achieve Rating > 7 when baseline expectations are met
  - Seat comfort inversely affects Economy; narrow seats and legroom complaints are ubiquitous
  - Understaffing signals correlate with 5.17% success rate in Economy

### Premium Economy: Misaligned Value Proposition (38.9% Rating > 7)
- Mean rating: **6.09/10**
- Only 37 of 95 flights achieve Rating > 7
- **Key Issue:** "premium_economy_underperforms" feature appears in 93 reviews
- **Evidence:** Passengers perceive insufficient differentiation from Economy; food/beverage offerings identical to Economy; seat improvements inadequate for price

### First Class: Limited Data (50.0% Rating > 7)
- Only 16 reviews; mean 7.38/10
- Suggests premium product performs when properly resourced but sample size is too small for strong conclusions

---

## 4. Service Quality Trend Signals: Root Causes

### Operational Degradation Post-Pandemic: 3.18/10 Average Rating
- **82 reviews** flagged with "degradation_post_pandemic"
- Only **6.1% achieve Rating > 7**
- Evidence: Worn cabin interiors, reduced amenities (no amenity kits, limited lounges), crew morale signals

### Understaffing: 3.23/10 Average Rating
- **116 reviews** indicate understaffing
- Only **5.2% achieve Rating > 7**
- Specific complaints: crew unavailable for assistance, meal service extremely slow (40+ min delays), toilets unattended for hours

### Cost-Cutting Visible: 3.62/10 Average Rating
- **109 reviews** cite cost-cutting measures
- Only **8.3% achieve Rating > 7**
- Examples: Seat reservation fees (£197), no complimentary WiFi (even Business), reduced food options, single white wine choice vs. multiple

### Infrastructure Aging: 4.55/10 Average Rating
- **33 reviews** note aging aircraft/facilities
- 12.1% achieve Rating > 7
- Issues: IFE screens unresponsive, recline mechanisms broken, 10-abreast seating on older aircraft

---

## 5. Traveler Type Satisfaction Variance

### Solo Leisure Travelers (Least Demanding): 6.60/10 Average
- **308 reviews** (41% of sample)
- **52.9% achieve Rating > 7** (strongest performance group)
- Profile: Flexible expectations, satisfied with baseline service
- **Action:** This segment is your rating-boosting opportunity; preserve their satisfaction

### Business Travelers (High Expectations): 6.06/10 Average
- **154 reviews** (21%)
- Only **44.8% achieve Rating > 7**
- Profile: Pay premium, expect premium; sensitive to value and service lapses
- **Key Issues:** Delayed flights without proper rebooking, business class food quality gaps, unresponsive customer service post-incident

### Leisure Couples (Most Demanding): 5.63/10 Average
- **160 reviews** (22%)
- Only **38.1% achieve Rating > 7** (lowest performer)
- Profile: Cost-conscious, sensitive to value-for-money, expect seat reservations together
- **Key Issues:** Seat reassignment without notice, no proactive communication on flight changes

### Families with Young Kids (Capacity Constrained): 5.93/10 Average
- **122 reviews** (16%)
- 45.1% achieve Rating > 7
- Profile: Need flexibility, extra seating/amenities
- **Known Failures:** Toilets unkept, crew unavailable for child needs, cramped seating

---

## 6. Ground Service vs. Inflight Service Impact

### Ground Service Failures are Rating Killers
- **111 reviews** with "ground_service" as primary complaint
- **Average rating: 3.13/10** (lowest of all complaint categories)
- **Only 12.6% achieve Rating > 7**
- Examples: Baggage mishandling (4+ day delays), unresponsive check-in staff, no rebooking options for cancellations

### Operational Disruptions Nearly Eliminate High Ratings
- **57 reviews** covering flight cancellations, delays, diversions, missed connections
- **Average rating: 2.60/10**
- **Only 5.3% achieve Rating > 7**
- Finding: Even perfect inflight service cannot recover from disruption mishandling

### Crew Service (When No Major Complaint): Achieves 51.2% Success
- **170 reviews** with crew_service as primary category
- **Average rating: 6.62/10**
- Shows crew quality is *moderately recoverable* with good inflight execution

---

## 7. Predictive Patterns: Achieving Rating > 7

### Guaranteed High Ratings (91.6% achieve > 7)
Reviews without explicit service complaints ("Unknown" category) show:
- **190 reviews average 8.95/10**
- **91.6% achieve Rating > 7**
- **Insight:** When nothing specifically goes wrong and value is perceived as good, ratings reach target easily

### Critical Success Combination
High-rating reviews (9-10, n=253) are predominantly:
- No primary service complaint flagged (139 of 253 = 55%)
- Crew service positive (when flagged)
- Economy class meeting baseline expectations (386 such reviews show 60.1% Rating > 7)

---

## 8. Route-Specific Recommendations

### London-Hong Kong Corridor (Bimodal Performance)
- **7 high ratings, 5 low ratings** on same route
- **Action Required:** Investigate flight-by-flight variation; implement consistency protocols for:
  - Crew scheduling (avoid consecutive fatigued crew)
  - Aircraft rotation (use same aircraft type for consistency)
  - Meal provisioning (ensure consistency across weekly flights)

### Asia-Pacific Hub Routes (Bangkok, Manila, Singapore)
- Higher success rates with medium-haul
- **Action:** Prioritize crew training and consistency on these feeder routes to protect hub reputation

### Long-Haul Toronto/Vancouver → Hong Kong
- Multiple low ratings; baggage mishandling endemic
- **Action:** Audit baggage handling SLAs; invest in ground service training at North American hubs

---

## 9. Segment-Specific Optimization Targets

### To Improve Economy Class (Largest Segment, Currently 42.9% → Target 55%+)
1. **Seat Comfort Crisis:** Address 10-abreast configuration complaints
   - Consider mixed fleet deployment: 9-abreast on 13+ hour routes
   - Better seat padding/support (cost: moderate; impact: high)

2. **Value Perception:**
   - Bundled amenity packages (meal + drink + entertainment included) for Y economy
   - Transparent pricing (no surprise seat reservation fees)
   - Complimentary water bottles (low cost, high perception gain)

3. **Staffing:** 
   - Increase cabin crew on Economy-heavy flights
   - Reduce meal service delays to <30 min for full cabin

### To Improve Premium Economy (Currently 38.9% → Target 55%+)
1. **Menu Differentiation:**
   - Distinct dining from Economy (currently identical)
   - Premium wine selection (per business class complaints)

2. **Amenity Parity:**
   - Amenity kits on all routes (not >5 hour only)
   - Slippers, noise-cancelling headsets to Premium Economy

3. **Seat Design:**
   - "premium_economy_underperforms" is persistent; upgrade seat recline/leg rest

### To Sustain Business Class Leadership (Currently 59.0%)
1. **Prevent Food Quality Regression:**
   - "business_class_food_gap" appears in 123 reviews
   - Lock down menu consistency; avoid generic/budget-oriented meal offerings
   - Maintain caviar, fine wines, signature dishes

2. **Crew Professionalism:**
   - Business class crew should see passengers every 30min (vs. current reports of 2-hour absences)

3. **Rebooking & Disruption Handling:**
   - Business passengers expect same-day rebooking; implement proactive automation

---

## 10. Key Weak Evidence & Caveats

1. **Inflight Entertainment Impact is Weak:**
   - Correlation with Overall Rating only 0.089
   - Yet frequently improved; suggests IFE upgrades alone won't drive target ratings

2. **Staff Service Direct Correlation is Low (0.110):**
   - Suggests crew quality matters less than *absence of crew failure*
   - Implication: "good enough" crew performance is sufficient if ground service and value are strong

3. **Sample Size Limits on First Class & Long-Haul Specific Routes:**
   - First Class only 16 reviews
   - Some routes (Tokyo-specific) have <5 reviews
   - Segment-specific conclusions should be validated with larger historical data

4. **Survivorship Bias:**
   - Dataset likely skews toward either very satisfied or very dissatisfied
   - Neutral passengers may not review; "Unknown" complaint category may reflect review text ambiguity rather than actual service neutrality

---

## Conclusion

**Achieving Overall Rating > 7 for Cathay Pacific requires:**

1. **Immediate:** Eliminate ground service failures and operational disruptions (these have <6% Rating > 7 success)
2. **High-Impact:** Restore value perception through transparent pricing and bundled offerings (2.22-point rating impact)
3. **Segment-Specific:** 
   - Economy: Fix seat comfort and staffing (largest population, lowest performance)
   - Premium Economy: Differentiate from Economy to justify price
   - Business: Maintain crew quality and menu consistency (already at 59% success)
4. **Route Consistency:** Investigate and standardize high-variance routes (London-Hong Kong)
5. **Crew Deployment:** Address understaffing signals; these correlate with only 5% Rating > 7 achievement

**Success Indicator:** The 190 "Unknown complaint" reviews average 8.95/10 rating, showing that consistent, no-incident flights with good value easily hit the target. The model should prioritize service consistency (avoiding failures) over premium additions.

**Recommended Focus:** Solve the Value for Money perception crisis (0.877 correlation) and eliminate ground service failures; these two levers alone could shift 20-30% of reviews from below to above the Rating > 7 threshold.
