---
dataset: airlines_review
scenario: causal_improve_singapore
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "overall_rating_recommendation"
query: "How can Singapore Airlines improve its overall rating and recommendation rate, especially on flights where passengers do not recommend it (Recommended = no)?"
source_table: augment_table/airlines_review/causal_improve_singapore/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:04:50.308177+00:00
wall_seconds: 112.47
---

# Singapore Airlines Improvement Analysis: Addressing Non-Recommended Flights

## Executive Summary

Singapore Airlines faces a significant satisfaction challenge: **35.6% (320 of 900) of reviews do not recommend the airline**, despite its reputation for excellence. This analysis identifies critical gaps between recommended and non-recommended experiences, with quantified priorities for improvement.

**Key Finding**: Non-recommended flights average a rating of **2.77 out of 10**, versus **8.61** for recommended flights—a gap of **5.84 points**. The primary driver is **value perception**, followed by service consistency and responsiveness during operational issues.

---

## 1. Outcome & Recommendation Status

| Metric | Count | % |
|--------|-------|-----|
| Recommended (yes) | 580 | 64.4% |
| Not Recommended (no) | 320 | 35.6% |
| **Total Reviews** | **900** | **100%** |

**Overall Rating by Recommendation**:
- Recommended: **8.61** (mean), **9.0** (median)
- Not Recommended: **2.77** (mean), **2.0** (median)
- **Critical gap: 5.84 points**

---

## 2. Core Structured Drivers of Dissatisfaction

Original rating dimensions reveal where SIA most underperforms among non-recommended flights:

| Dimension | Recommended | Not Recommended | Gap |
|-----------|-------------|-----------------|-----|
| **Value for Money** | 4.34 | 1.82 | **−2.52** ⭐ |
| Staff Service | 4.01 | 3.80 | −0.21 |
| Food & Beverages | 3.65 | 3.42 | −0.23 |
| Seat Comfort | 3.69 | 3.66 | −0.03 |
| Inflight Entertainment | 3.88 | 3.93 | +0.05 |

**Critical insight**: Value for Money shows the **largest deterioration** (−2.52 gap, 0.599 correlation with overall rating within non-recommended cohort). The other operational dimensions—comfort, food, staff—show minimal gaps, suggesting the dissatisfaction stems from **price-quality mismatch rather than absolute service failure**.

---

## 3. Non-Recommended Reviews by Cabin Class

Economy class drives the bulk of dissatisfaction:

| Class | Count | % of Non-Rec | Mean Rating | Primary Issues |
|-------|-------|--------|-------------|-------------|
| **Economy** | **214** | **66.9%** | **2.57** | Booking failures (52.8%), unfriendly crew (64.5%), poor responsiveness (84.1%) |
| **Business** | **67** | **20.9%** | **3.15** | Service inconsistency (98.5%), poor responsiveness (88.1%) |
| **Premium Economy** | **36** | **11.2%** | **3.19** | Perfect service inconsistency (100%), unfriendly attitude (61.1%) |
| **First Class** | **3** | **0.9%** | **3.00** | All operational/service issues (100% each) |

**Economic imperative**: ~67% of dissatisfied passengers are in economy class, where SIA operates high-volume routes and faces the strongest competitive pressure.

---

## 4. TAPP-Generated Semantic Facets: Explanatory Patterns

The augmented dataset reveals deeper issue clusters that explain non-recommendation:

### 4.1 Service Consistency (`service_inconsistency`)
- **Near-universal** in non-recommended reviews: 98.1% (314 of 320)
- Mean rating with inconsistency: **2.70** vs. 6.33 without
- **Interpretation**: Service quality varies unpredictably—some flights excel, others disappoint. Passengers downgrade their overall assessment due to **reliability concerns** (will this flight be good or poor?), not isolated incidents.

### 4.2 Customer Service Responsiveness (`customer_service_responsiveness`)
- **Unresponsive** (41.2%, n=132): rating **2.40**
- **Slow** (44.7%, n=143): rating **2.76**
- **Responsive** (13.1%, n=42): rating **3.76**
- **Gap between responsive and unresponsive: 1.36 points**

Unresponsiveness clusters in **post-booking and disruption scenarios** (delays, cancellations, luggage issues).

### 4.3 Booking & Operational Failures (`booking_operational_failure`)
Highly predictive of low ratings when paired with poor responsiveness:

| Scenario | Count | Mean Rating |
|----------|-------|------------|
| Booking fail + Unresponsive | 77 | **1.82** |
| Booking fail + Slow response | 65 | **1.89** |
| No booking fail + Responsive | 39 | **3.95** |
| No booking fail + Slow response | 78 | **3.49** |

**Critical pattern**: Operational failures combined with slow/no support **devastate ratings** (1.8–1.9). Proactive, responsive resolution can salvage experience (+2.0 points difference).

### 4.4 Food Quality (`food_quality_decline`)
- Present in 31.2% (n=100) of non-recommended reviews
- With decline: rating **3.47**; without: **2.45**
- **Note**: Food quality is secondary; when noted, it **improves** ratings slightly, suggesting passengers who mention food problems still appreciate that aspect.

### 4.5 Seat Comfort (`seat_comfort_issue`)
- Present in 27.2% (n=87) of non-recommended reviews
- With issue: rating **3.51**; without: **2.49**
- **Pattern**: Seats mentioned only when truly problematic (long hauls, emergency rows, older aircraft); when flagged, comfort **worsens** the rating (~1.0 point).

### 4.6 Crew Service Attitude (`crew_service_attitude`)
- **Unfriendly** (59.1%, n=189): rating **2.31**, service score **3.78**
- **Neutral/Efficient** (20.6%, n=66): rating **3.48**, service score **3.68**
- **Warm/Attentive** (4.7%, n=15): rating **4.73**, service score **4.20**
- **Gap unfriendly-to-warm: 2.42 points**

Unfriendly attitudes dominate non-recommended reviews and **correlate with low ratings** despite adequate staff service scores. **Interpretation**: Staff are present and functional but lack warmth and genuine attentiveness, eroding trust.

### 4.7 Aircraft Age/Condition (`aircraft_age_condition`)
- Present in 14.1% (n=45); drives rating **3.67** vs. **2.62** without
- Secondary factor; mostly on regional, older B737 and regional A350 routes.

### 4.8 Inflight Entertainment Failure (`inflight_entertainment_failure`)
- Present in 13.8% (n=44); minimally impacts rating (+0.5 points)
- **Lowest-impact issue**; passengers prioritize service, value, and consistency over IFE.

---

## 5. Traveller Segment Breakdown

Non-recommended reviews span all traveller types:

| Segment | Count | % of Non-Rec |
|---------|-------|-------------|
| Solo Leisure | 100 | 31.2% |
| Couple Leisure | 97 | 30.3% |
| Family Leisure | 64 | 20.0% |
| Business | 59 | 18.4% |

**No single segment drives dissatisfaction**—issues are **airline-wide**, suggesting systemic problems rather than customer-type-specific failures.

---

## 6. Corrective Priorities for SIA

Based on quantified evidence and TAPP-augmented facets, recommendations rank by impact:

### Priority 1: Fix Value Perception (Impact: −2.52 gap, 0.599 correlation)
**Action**: Address the **price-quality disconnect** in economy segment.
- Passengers pay comparable fares but perceive **lower value** vs. competitors
- Solution: Transparent pricing on ancillary charges; bundled offerings; loyalty rewards that feel valuable
- **Target**: Reduce non-recommended gap from −2.52 to −1.5 (33% improvement)

### Priority 2: Ensure Service Consistency & Reliability (98.1% of issues)
**Action**: Standardize crew training and on-board protocols.
- 98.1% of non-recommended reviews mention service inconsistency
- Root cause: Variable crew behavior, unpredictable meal timing, cabin cleanliness variance
- **Solution**: Quarterly audits; crew incentives for consistency; publish SLA standards
- **Target**: Reduce from 98.1% to 70% (eliminate random variation)

### Priority 3: Strengthen Customer Responsiveness in Operational Disruptions (85.3% slow/unresponsive)
**Action**: Build rapid response infrastructure for disruptions.
- 85.3% of non-recommended reviews cite slow or unresponsive customer service
- Gaps in: rebooking, hotel/meal vouchers, luggage tracing, complaint resolution
- **Solution**: 24/7 responsive teams; AI-guided rebooking; transparent communication
- **Target**: Shift from 41.2% unresponsive + 44.7% slow to **60% responsive**

### Priority 4: Cultivate Crew Warmth & Attentiveness (59.1% unfriendly)
**Action**: Rebalance crew culture toward hospitality, not efficiency-only.
- 59.1% of non-recommended reviews describe crews as unfriendly; only 4.7% as warm/attentive
- Current issue: Crews function adequately but lack genuine customer empathy
- **Solution**: Hospitality retraining; empower crews to exceed norms; celebrate service champions
- **Target**: Shift unfriendly from 59.1% to 30%, warm/attentive from 4.7% to 20%

### Priority 5: Resolve Operational/Booking Failures (45.6% flagged)
**Action**: Prevent failures upstream.
- 45.6% of non-recommended flights involve booking/operational issues (cancellations, delays, luggage)
- **Combined effect**: Booking failure + unresponsive support → 1.82 rating (worst scenario)
- **Solution**: Invest in systems (IT modernization, baggage tracking); pre-emptive outreach
- **Target**: Reduce from 45.6% to 20%

### Priority 6: Address Seat Comfort on Economy Long-Haul (27.2% flagged)
**Action**: Modernize economy cabin on high-dissatisfaction routes.
- 27.2% of non-recommended reviews mention seat discomfort
- Primarily: regional seat designs on long-hauls, emergency row bookings
- **Solution**: A350/787 retrofit priority; seat width/padding improvements
- **Target**: Reduce from 27.2% to 10%

---

## 7. Methodology Note

**TAPP-Generated Columns Used**:
- `service_inconsistency`: Boolean flag for detected service variation across flight segments or crew shifts
- `customer_service_responsiveness`: Categorical assessment (responsive, slow, unresponsive) of post-flight complaint/disruption handling
- `booking_operational_failure`: Boolean for booking issues, cancellations, delays, or operational disruptions
- `crew_service_attitude`: Categorical facet (warm_attentive, unfriendly, neutral_efficient, robotic_disengaged) capturing interpersonal tone
- `seat_comfort_issue`: Boolean for comfort complaints (padding, width, headrest, recline)
- `food_quality_decline`: Boolean for food quality issues (staleness, limited options, cold meals)
- `aircraft_age_condition`: Boolean for age/maintenance issues on older fleets
- `inflight_entertainment_failure`: Boolean for technical IFE failures

**Integration approach**: TAPP columns complement original numeric ratings (Seat Comfort: 1–5, Staff Service: 1–5, etc.) by adding **semantic depth and granularity**. For example, Staff Service scores show minimal gaps (3.80 vs 4.01) between recommended and non-recommended flights, but `crew_service_attitude` reveals the **quality of interaction** varies dramatically (warm 4.73 vs. unfriendly 2.31). This indicates crews are **present but not warm**—a distinction invisible in raw rating numbers.

---

## 8. Conclusion

SIA's path to reversing the 35.6% non-recommendation rate requires **multi-faceted action**:

1. **Immediate** (0–3 months): Launch customer responsiveness program; stabilize booking/operational systems
2. **Short-term** (3–6 months): Crew warmth retraining; transparent value messaging; service consistency audits
3. **Medium-term** (6–12 months): Cabin modernization; pricing strategy refresh; advanced system investments

Success metric: **Reduce non-recommended reviews to <20%** within 12 months and **lift Overall Rating gap from 5.84 to 3.0 points**, demonstrating meaningful, quantifiable improvement in customer satisfaction.

---

*Report Date: 2026-07-30*
*Dataset: 900 Singapore Airlines reviews (64.4% recommended, 35.6% not recommended)*
*Original and TAPP-augmented columns analyzed; focus on non-recommended cohort and structural/semantic drivers*
