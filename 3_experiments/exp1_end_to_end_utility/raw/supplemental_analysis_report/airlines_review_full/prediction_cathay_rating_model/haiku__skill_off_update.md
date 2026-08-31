---
dataset: airlines_review_full
scenario: prediction_cathay_rating_model
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating_gt7"
query: "(Cathay MD) Build a model to organise/optimise routes and service so Overall Rating > 7."
source_table: augment_table/airlines_review_full/prediction_cathay_rating_model/haiku__skill_off_update.csv
generated_at: 2026-08-03T05:43:11.416926+00:00
wall_seconds: 91.38
---

# Cathay Pacific Airways: Route and Service Optimization Model to Achieve Overall Rating > 7

**Analysis Date:** 2026-08-03  
**Dataset:** Airlines Review (744 Cathay Pacific Airways reviews)  
**Objective:** Build a model to organize and optimize routes and service delivery to achieve Overall Rating > 7

---

## Executive Summary

Currently, **46.8%** (348 of 744 reviews) achieve ratings above 7, indicating substantial opportunity for improvement. The analysis reveals that **Value For Money** is the dominant predictor of high ratings (r=0.877), followed by service quality consistency. Optimization requires simultaneous focus on three dimensions: route selection, service class positioning, and value-price alignment.

---

## Key Findings

### 1. Critical Success Factor: Value For Money

**Value For Money** is the dominant driver of ratings > 7, with clear behavioral separation:
- **High ratings (>7):** 94.0% scored Value For Money ≥4 (avg: 4.51)
- **Low ratings (≤7):** Only 17.7% scored Value For Money ≥4 (avg: 2.29)
- **Correlation with Overall Rating:** 0.877 (strongest of all factors)

**Implication:** Pricing strategy must align perceived service quality to ticket cost. Premium services without premium pricing gain highest satisfaction.

### 2. Route Performance Patterns

**Short-haul regional routes** outperform long-haul:
- **Short-haul (Asia-focused):** Avg rating 6.70, Value For Money avg 3.58
- **Long-haul (intercontinental):** Avg rating 5.92, Value For Money avg 3.20
- **Top-performing routes:** Bangkok↔Hong Kong (6.86/10), Singapore→Bangkok (6.83/10), Manila→Hong Kong (7.10/10)

**Evidence:** Short routes show 0.78 rating points higher, suggesting complexity management and operational consistency challenges on long-haul extend across service delivery.

### 3. Class-Based Segmentation

Significant performance variance by cabin class:
- **Business Class:** Avg 7.09 (highest), 195 reviews
- **First Class:** Avg 7.38, but limited data (16 reviews)
- **Premium Economy:** Avg 6.09
- **Economy Class:** Avg 5.73 (lowest), 438 reviews

**Key insight:** Business and First class achieve >7 ratings despite high expectations. Economy class struggles primarily on value perception (3.21/5), not service quality per se (3.55 Staff Service is reasonable).

### 4. Service Quality vs. Value Perception Gap

The **Service-to-Value Gap** metric reveals critical insight:
- **Negative gap (service > value):** 346 reviews averaging **8.41** rating
- **Positive gap (value > service):** 351 reviews averaging **3.74** rating

This indicates that when passengers perceive service delivery exceeds price, ratings soar. Conversely, when price expectations exceed service, satisfaction collapses even if service quality is adequate.

### 5. Secondary Success Factors

**Seat Comfort & Staff Service** support but don't drive ratings:
- Seat Comfort ≥4: 67.3% of >7 ratings vs. 51.4% of <7 ratings (+16pp)
- Staff Service ≥4: 65.1% of >7 ratings vs. 55.9% of <7 ratings (+9pp)
- **Correlation with rating:** 0.156 and 0.110 respectively (weak)

These are **threshold factors**—meeting baseline standards is necessary but insufficient without value alignment.

### 6. Recommendation Rate as Success Indicator

- **For ratings >7:** 99.7% would recommend the airline
- **For ratings ≤7:** Only 24.2% would recommend

This 75-point gap confirms that >7 represents a true satisfaction inflection point where passengers become advocates.

---

## Route Optimization Recommendations

### High-Priority Routes (Optimize for >7)
1. **Bangkok-Hong Kong corridor:** Consistent performer (6.86/10). Maintain current operations; use as training benchmark.
2. **Manila-Hong Kong:** 7.10 avg, 10 reviews. Expand service on this profitable, well-performing route.
3. **Singapore-Bangkok:** 6.83 avg, 6 reviews. Small volume suggests underutilized route with demand.

### Underperforming Routes (Require Intervention)
1. **Sydney-Hong Kong:** 4.43 avg (50 reviews—largest low-rated volume)
2. **New York-Hong Kong:** 3.38 avg (8 reviews)
3. **Hong Kong-Los Angeles:** 4.60 avg (5 reviews)

**Action:** Long-haul routes show structural challenges. Investigate crew fatigue policies, meal quality consistency, and seat maintenance standards on >12-hour flights.

---

## Service Delivery Model for >7 Ratings

### Tier 1: Value-Price Alignment (Critical)
- Ensure ticket pricing reflects actual service level delivered
- For Economy: Consider tiered pricing (Basic/Standard/Premium Economy) to segment value perception
- For long-haul: Premium-priced seats must include measurable differentiators (seat pitch ≥32", premium catering, priority services)
- **Target:** 90%+ of passengers perceive Value For Money ≥4

### Tier 2: Baseline Service Standards (Required)
- **Seat Comfort:** Target ≥4 in 70% of bookings (requires aircraft fleet modernization and configuration audits)
- **Staff Service:** Achieve ≥4 in 70% of flights (crew training on attentiveness and proactive assistance)
- **Food & Beverages:** Achieve ≥4 in 60%+ (menu consistency, portion quality, dietary accommodation)

### Tier 3: Route-Specific Optimization
- **Short-haul (<4 hours):** Focus on on-time performance, seat comfort, and ground service efficiency
- **Medium-haul (4-8 hours):** Balanced emphasis on catering and IFE quality
- **Long-haul (>8 hours):** Prioritize cabin cleanliness, lavatories maintenance, crew service consistency, and sleep comfort

---

## Evidence of Implementation Gaps

1. **Inconsistent execution:** Reviews frequently mention excellent service on one leg, poor service on another (same route)
2. **Cabin maintenance:** Multiple reports of dirty lavatories on long-haul flights; crew cleaning protocols appear inadequate
3. **Crew attentiveness gaps:** Economy class reviews note crews "disappear" after meal service; premium classes report consistent presence
4. **Aircraft age perception:** Modern A350 aircraft receive significantly higher ratings than older 777/330 configurations
5. **Pricing transparency:** Complaints concentrated on seat selection fees and baggage rules, undermining value perception despite service quality

---

## Weak Evidence & Exceptions

- **Inflight Entertainment:** Minimal correlation (0.089) despite high availability. Paradox: IFE described as "excellent" in high-rated reviews, but doesn't drive ratings independently
- **Business vs. Leisure:** Business travelers rate slightly lower (5.83 vs. 6.68 for solo leisure), contrary to expectation that higher-paying segments would rate higher
- **Route Complexity:** Longer, more complex routes show *lower* ratings (r=-0.170), but causality unclear—may reflect route difficulty rather than planning failure

---

## Quantified Model Inputs

| Factor | Weight (Correlation) | Threshold for >7 | Current Performance |
|--------|----------------------|------------------|---------------------|
| Value For Money | 0.877 | ≥4 (94% required) | 2.29 avg (below <7 ratings) |
| Service Quality Score | 0.214 | ≥3.5 | 3.57 avg overall |
| Seat Comfort | 0.156 | ≥4 | 3.84 high ratings |
| Service-to-Value Gap | -0.748 | <0 (service exceeds value) | +0.24 avg (misaligned) |
| Staff Service | 0.110 | ≥4 | 3.76 high ratings |

---

## Actionable Optimization Strategy

**Phase 1 (Immediate): Price-Service Alignment**
- Audit current pricing against service delivery metrics
- Implement dynamic pricing that reflects aircraft type, route, and service quality
- For economy: Introduce tiered offerings (Standard/Premium Economy) to align expectations

**Phase 2 (0-6 months): Short-Haul Excellence**
- Prioritize Bangkok, Manila, Singapore, Taipei routes for >7 achievement
- Standardize crew protocols for high-satisfaction routes as templates
- Target: 70% of short-haul bookings to achieve >7 ratings

**Phase 3 (6-12 months): Long-Haul Recovery**
- Replace oldest aircraft (777/330) on underperforming long-haul routes
- Implement mandatory cabin cleanliness audits every 4 hours on flights >10 hours
- Expand premium options (add extra legroom, dedicated meal selections)
- Target: Reduce long-haul average rating gap to <0.5 from current 0.78 difference

**Phase 4 (12+ months): Systemic Consistency**
- Standardize service delivery across all flights regardless of crew
- Implement passenger feedback loops for per-route continuous improvement
- Goal: 60%+ of all flights achieve >7 ratings (up from current 46.8%)

---

## Risk Factors

1. **Operational cost inflation:** Premium service and fleet modernization require significant capex
2. **Market sensitivity:** Long-haul routes may not sustain higher pricing without competitor pressure
3. **Crew retention:** Service quality depends on stable, trained crew; post-pandemic hiring challenges persist
4. **External factors:** Routes like Sydney-London show consistent underperformance; may reflect competitive saturation rather than operational failure

---

## Conclusion

Achieving Overall Rating > 7 for Cathay Pacific requires primacy focus on **Value For Money alignment**, supported by consistent baseline service standards and strategic route prioritization. Short-haul Asian routes demonstrate the airline is capable of >7 performance; long-haul routes and economy class segments require targeted intervention. The data indicates that perceived value—not absolute service quality—is the limiting factor, suggesting that pricing strategy and transparent service differentiation merit equal investment to operational service improvements.

**Current Target:** Move 348/744 (46.8%) to 470+/744 (63%+) achieving >7 ratings within 12-18 months.
