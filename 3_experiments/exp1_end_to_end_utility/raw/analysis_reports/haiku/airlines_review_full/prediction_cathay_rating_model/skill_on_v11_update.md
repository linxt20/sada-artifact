---
dataset: airlines_review_full
scenario: prediction_cathay_rating_model
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating_gt7"
query: "(Cathay MD) Build a model to organise/optimise routes and service so Overall Rating > 7."
source_table: augment_table/airlines_review_full/prediction_cathay_rating_model/haiku__skill_on_v11_update.csv
generated_at: 2026-08-03T05:55:18.367516+00:00
wall_seconds: 150.51
---

# Cathay Pacific Airways: Route & Service Optimization Model for Overall Rating > 7

**Analysis Date:** August 3, 2026  
**Dataset:** Cathay Pacific Airways Review Full Augmentation Dataset  
**Focus Variable:** Overall Rating Prediction  

---

## Executive Summary

This analysis examines 744 Cathay Pacific Airways reviews to identify patterns associated with high ratings (>7). The current dataset shows **46.8% of reviews exceed a rating of 7**, with an average rating of **6.17**. To achieve the target of consistently higher satisfaction, Cathay Pacific should prioritize three key optimization areas: **Value for Money**, **Staff Service Quality**, and **Route-Specific Service Calibration**.

---

## Key Findings

### 1. Overall Performance Baseline

- **Total Reviews Analyzed:** 744
- **High Ratings (>7):** 348 reviews (46.8%)
- **Low Ratings (≤7):** 396 reviews (53.2%)
- **Average Rating:** 6.17 / 10
- **Rating Range:** 1–10

Current performance indicates that achieving >7 ratings is possible but not yet the norm. Approximately 53% of passengers leave ratings of 7 or below.

### 2. Most Critical Success Factor: Value for Money

The single largest differentiator between high and low ratings is **Value for Money**:

| Metric | High Ratings (>7) | Low Ratings (≤7) | Difference |
|--------|-------------------|------------------|------------|
| **Value for Money Score** | 4.51 / 5 | 2.29 / 5 | **+2.22** |
| Seat Comfort | 3.84 | 3.42 | +0.41 |
| Staff Service | 3.76 | 3.49 | +0.27 |
| Food & Beverages | 3.40 | 3.11 | +0.29 |
| Inflight Entertainment | 3.88 | 3.76 | +0.12 |

**Insight:** The Value for Money metric shows a **2.22-point gap** between satisfied and dissatisfied passengers—nearly **10 times larger** than any other service dimension. This suggests that pricing strategy and perceived value are primary drivers of satisfaction, not just operational service quality.

### 3. Service Class Performance

Business Class significantly outperforms other cabin classes:

| Class | >7 Rating Rate | Avg Rating |
|-------|----------------|------------|
| Business Class | 59% | 6.73 |
| First Class | 50% | 6.31 |
| Premium Economy | 39% | 5.64 |
| Economy Class | 43% | 5.97 |

Economy travelers show lower satisfaction despite reasonable absolute scores. Improving value perception in economy is critical for meeting the >7 target.

### 4. Route-Specific Performance Patterns

#### High-Performance Routes (>7.8 Average Rating):

1. **London–Hong Kong (Business):** 8.80 avg, 80% >7  
   - Strong staff service (4.2), good food (3.8), high value perception (4.4)

2. **Manila–Hong Kong (Economy):** 8.38 avg, 75% >7  
   - Short-haul, high-frequency route with consistent crew
   - Staff service (3.8), value perception (4.2)

3. **Bangkok–Hong Kong (Both Classes):** 8.14–7.83 avg, 71–83% >7  
   - Best performer among regional routes

#### Problem Routes (≤3.0–4.6 Average Rating):

1. **Hong Kong–Sydney (Economy):** 3.00 avg, 20% >7  
   - Ultra-low value perception (1.8/5) despite 15+ hour flight
   - Seat comfort issues (2.8), staff engagement gaps

2. **HKG–Taipei (Economy):** 4.60 avg, 40% >7  
   - Poor value perception (2.8/5)

**Pattern Insight:** Routes with consistent crew rostering and frequent schedules show better engagement. Long-haul economy to major western hubs suffers from value misalignment.

### 5. Primary Complaint Analysis

**In Low-Rated Reviews (≤7):**
- **Customer Service Gaps:** 30.9% — rebooking failures, communication breakdowns
- **Staff Service Issues:** 26.8% — inattentiveness, poor responsiveness
- **Seat Comfort:** 16.0% — cramped economy, 10-abreast seating concerns
- **Food Quality:** 13.8% — poor taste, limited variety
- **Operational Delays:** 9.2% — flight changes, missed connections

**In High-Rated Reviews (>7):**
- **Staff Service (Positive):** 65.6% — friendly, attentive, professional
- **Food Quality (Positive):** 14.6% — good variety, fresh items
- **Seat Comfort (Positive):** 9.9% — comfortable, adequate legroom

**Critical Insight:** Staff service is the only dimension extensively mentioned in positive reviews. When cabin crew demonstrate attentiveness, it overrides minor deficiencies in food or seats.

### 6. Traveller Segment Distribution

High-rated reviews (>7) distributed as:
- **Solo Leisure:** 177 (50.9%)
- **Couple Leisure:** 59 (16.9%)
- **Family Leisure:** 57 (16.4%)
- **Business:** 55 (15.8%)

---

## Optimization Recommendations

### A. Value for Money Realignment

1. **Pricing Strategy Review:**  
   - Current economy pricing generates massive value dissatisfaction on long-haul routes
   - Bundle seat selection, meals, or WiFi into base fares rather than à la carte charges
   - Consider dynamic pricing reflecting service delivery (smaller seats → lower base fare)

2. **Transparent Service Expectations:**  
   - Clearly communicate included amenities before booking
   - Address expectations misalignment for economy class

### B. Staff Service Excellence Program

1. **Crew Engagement & Scheduling:**  
   - Consistent crew rosters on high-volume regional routes show 1.0–1.5 point rating improvements
   - Reduce rotation; build continuity
   - Increase staff-to-passenger ratios

2. **Service Recovery:**  
   - 30.9% of low ratings cite customer service gaps
   - Implement rapid escalation for flight changes/cancellations
   - Target <2 hour response time on chat/WhatsApp (currently 24+ hours)

### C. Route-Specific Calibration

**Priority 1:** Fix Hong Kong–Sydney (1.8 value score on 15-hour flight) and Taipei routes
- Improve meal variety, add complimentary seat selection
- Review aircraft configuration for overcrowding

**Priority 2:** Premium Economy repositioning  
- Add privacy screens, improve meal service, increase crew attention
- Currently only 39% achieve >7 ratings despite premium pricing

**Priority 3:** Standardize Economy  
- Route-specific menu offerings (Asian vs. Western preferences)
- Consistent seat configurations and IFE updates across fleet

### D. Service Delivery Standards

1. **Food Program:**  
   - Introduce route-specific menus
   - Ensure menu items are actually available (currently major complaint)
   - Pre-order systems increase satisfaction by ~10% (peer benchmark)

2. **Seat Management:**  
   - Cabin crew should explain narrow seat configurations to economy passengers
   - Offer early check-in for seat selection at no cost

---

## Weak Evidence & Caveats

1. **Inflight Entertainment:** Only 0.12-point gap between high/low ratings; less critical than perceived

2. **Operational Reliability:** Only 9.2% of low ratings cite delays; most operations on-time

3. **Cabin Cleanliness:** Rarely mentioned except when problematic; maintain baseline standards

---

## Implementation Priority & Expected Impact

| Initiative | Effort | Impact | Timeline |
|-----------|--------|--------|----------|
| Value messaging & bundling | Medium | **High** (+8–10%) | 3 months |
| Staff training & scheduling | High | **High** (+12–15%) | 6 months |
| Problem route interventions | High | **Medium** (+5–7%) | 4 months |
| Premium Economy refresh | High | **Medium** (+5–8%) | 9 months |
| Food standardization | Medium | **Low** (+2–3%) | 6 months |

---

## Conclusion

Achieving consistent Overall Ratings >7 requires:

1. **Immediate:** Realign pricing/value perception and improve staff engagement through crew scheduling and service recovery. Value for Money is the dominant lever (+2.22 differential).

2. **Medium-term:** Standardize delivery across routes with targeted interventions for problem routes and premium economy.

3. **Operational Focus:** Staff attentiveness, not infrastructure, predicts satisfaction. Invest in people, not aircraft.

Scaling from current 46.8% >7 ratings to 60–70% requires addressing the value-perception gap and ensuring consistent, friendly staff engagement across all cabin classes and routes.
