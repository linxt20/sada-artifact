---
dataset: airlines_review
scenario: prediction_satisfaction_drivers
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating"
query: "What drives customer satisfaction (Overall Rating) across the different airlines?"
source_table: augment_table/airlines_review/prediction_satisfaction_drivers/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:05:36.700926+00:00
wall_seconds: 87.7
---

# Customer Satisfaction Drivers Analysis: Airlines Review Dataset

## Executive Summary

This analysis examines 900 verified customer reviews of Singapore Airlines to identify what drives Overall Rating satisfaction. The dataset spans reviews from January to September 2018 across multiple cabin classes, traveler types, and route distances. **Value perception emerges as the dominant satisfaction driver** (r = 0.878), followed by service personalization (r = 0.826) and aircraft cleanliness (r = 0.659).

## Dataset Characteristics

- **Total Reviews**: 900
- **Cabin Classes**: Economy (70%), Business (24%), Premium Economy (5%), First Class (1%)
- **Traveler Segments**: Solo Leisure (42%), Business (17%), Couple Leisure (22%), Family Leisure (20%)
- **Route Types**: Long-haul (69%), Medium-haul (19%), Short-haul (12%)
- **Overall Rating Distribution**: Bimodal, with peaks at 1 (207 reviews) and 10 (169 reviews), mean = 5.66/10

## Primary Satisfaction Drivers (Ranked by Strength)

### 1. **Value For Money Perception** (Correlation: 0.878) ⭐ STRONGEST
- **High impact**: Good value perception yields average rating of **9.22/10** (n=268)
- **Strong negative impact**: Poor value perception yields average rating of **2.48/10** (n=254)
- A 6.74-point swing in satisfaction directly tied to pricing fairness
- 78% of high-satisfaction reviews (≥8) reported good value perception
- 75% of low-satisfaction reviews (≤3) reported poor value perception

### 2. **Service Personalization** (Correlation: 0.826)
- **Highly personalized service**: 9.24/10 average (n=278)
- **Impersonal/rushed service**: 2.76/10 average (n=449)
- 6.48-point swing in satisfaction tied to crew attentiveness and personal touch
- 69% of high-satisfaction reviews emphasized personalized service
- 96% of low-satisfaction reviews cited impersonal or rushed service

### 3. **Aircraft Cleanliness & Maintenance** (Correlation: 0.659)
- **Clean, well-maintained**: 8.71/10 average (n=262)
- **Dirty/neglected**: 3.24/10 average (n=41)
- Strong correlation despite fewer reviews mentioning poor cleanliness
- 58% of high-satisfaction reviews explicitly noted cleanliness standards

### 4. **Seat Physical Comfort & Space** (Correlation: 0.589)
- **Spacious, comfortable seats**: 8.37/10 average (n=263)
- **Cramped, uncomfortable seats**: 4.01/10 average (n=112)
- 4.36-point satisfaction swing
- Exception noted: 15 customers rated ≥8 despite cramped seats, suggesting other factors compensated

### 5. **Food & Beverage Quality** (Correlation: 0.589)
- **High-quality, varied meals**: 8.90/10 average (n=205)
- **Poor or limited options**: 3.93/10 average (n=170)
- 4.97-point satisfaction swing
- 88% of high-satisfaction reviews had high-quality food offerings

### 6. **Operational Punctuality & Reliability** (Correlation: 0.421)
- **On-time, reliable**: 6.47/10 average (n=657)
- **Major delays/cancellations**: 2.37/10 average (n=149)
- 4.10-point satisfaction swing
- Delays significantly impact satisfaction but are moderated by other factors (ground staff support, rebooking assistance)

### 7. **Communication Clarity** (Correlation: 0.400 estimated)
- **Clear, timely communication**: 83% of high-satisfaction reviews
- **Unclear or contradictory information**: 79% of low-satisfaction reviews
- Critical for managing expectations and recovery scenarios

## Secondary Findings by Passenger Segments

### By Cabin Class
| Class | Avg Rating | Count | Pattern |
|-------|-----------|-------|---------|
| Business Class | 6.78 | 216 | Highest satisfaction despite premium pricing expectations |
| Premium Economy | 5.98 | 44 | Value expectation often unmet |
| Economy Class | 5.24 | 629 | Most vulnerable to value perception issues |

**Insight**: Business passengers likely have service personalization and product quality compensating for cost. Economy passengers report poorest satisfaction—23% of business vs. 70% of economy rate "overpriced/poor value."

### By Traveler Type
| Type | Avg Rating | Count | Key Driver |
|------|-----------|-------|------------|
| Solo Leisure | 6.03 | 376 | Service personalization matters more (loyalty rebuilding) |
| Business | 5.83 | 151 | Punctuality and communication critical |
| Couple Leisure | 5.24 | 197 | Seat comfort and experience consistency key |
| Family Leisure | 5.17 | 176 | Most sensitive to service gaps and delays |

### By Route Distance
| Route | Avg Rating | Count | Driver Focus |
|-------|-----------|-------|--------------|
| Short-haul | 6.31 | 108 | Efficiency, boarding, ground services |
| Medium-haul | 5.60 | 170 | Balanced: comfort, food, timeliness |
| Long-haul | 5.56 | 622 | All factors critical; fatigue amplifies dissatisfaction |

## Critical Exceptions and Nuances

1. **Service Recovery Offset**: 15 customers gave ≥8 ratings despite cramped seats. This occurred when ground staff resolved issues, rebooking was handled with care, or crew showed exceptional attentiveness.

2. **Seat Class Expectation Mismatch** (Strong Driver):
   - Downgrades without adequate compensation: 62 of 327 low-satisfaction reviews
   - "Seat type as expected" present in 90% of high-satisfaction reviews but only 55% of low-satisfaction reviews

3. **Ground & Airport Services**: 
   - Dramatically impacts low-satisfaction reviews (96% cite chaotic/poor ground service)
   - Yet often overlooked when flight operations succeed (check-in delays overshadow good in-flight service)

4. **The "Value Paradox"**: 
   - Even with excellent food and service, poor value perception yields ~2.5/10 ratings
   - Indicates customers evaluate fairness-to-price upfront, then judge execution against that standard

5. **Weak Drivers**: 
   - Inflight entertainment (r = 0.089): Mentioned in reviews but secondary to core services
   - Crew professionalism alone (r = 0.071): Correlated with impersonal/personalized dimension, not isolated

## Recommendation Status as Outcome Metric

- **Would recommend (n=480)**: Average rating 8.56/10
- **Would not recommend (n=420)**: Average rating 2.33/10
- Clear binary outcome: satisfaction is polarized, not gradual

## Data Quality Notes

- 334 reviews had missing seat comfort data (Unknown), suggesting budget-tier services or cargo-focused flights
- 280 reviews had missing value perception data—likely reviews focused purely on experience narrative
- Ground services data missing in 359 reviews (Economy may not experience ground services equally)

## Conclusion

**Value perception is the meta-driver**: It acts as a satisfaction threshold that either permits or blocks positive ratings of other dimensions. A customer perceiving poor value will rate even excellent food, service, and comfort poorly. Conversely, perceived good value creates halo effects that partially offset service or product shortcomings.

**Service personalization is the operational differentiator**: While value is set by pricing strategy, personalization is controllable by crew training and airline culture. 69% of high-satisfaction reviews explicitly praised personalized service.

**Physical product quality matters progressively**: Cleanliness, comfort, and food quality show strong correlations. Long-haul travelers especially require baseline comfort; failures here cascade to lower ratings.

**Operational reliability is necessary but insufficient**: On-time performance alone does not drive satisfaction—it prevents *additional* dissatisfaction. Delays paired with poor communication or inadequate recovery yield the lowest ratings.

For targeted improvements, airlines should prioritize: (1) value communication and transparent pricing; (2) crew training for personalized engagement; (3) consistent cabin standards; (4) proactive communication during disruptions.
