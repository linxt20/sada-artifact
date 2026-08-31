---
dataset: airlines_review
scenario: causal_qatar_business
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "non_recommendation_outcome"
query: "Explain why some Qatar Airways Business-Class flights receive a non-recommended (Recommended = no) result."
source_table: augment_table/airlines_review/causal_qatar_business/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:04:00.795019+00:00
wall_seconds: 62.96
---

# Qatar Airways Business-Class Non-Recommended Flights Analysis

## Executive Summary

Of 592 Qatar Airways Business-Class reviews in this dataset, 127 (21.5%) received a non-recommended classification. The primary driver of non-recommendations is **perceived poor value for money**, which shows the strongest correlation (0.658) with the recommendation decision. However, non-recommendations result from a combination of factors spanning operational, product, and service dimensions.

## Key Findings

### 1. Value for Money as Primary Decision Factor

**Value for Money** is the single strongest predictor of recommendation:

- **Non-recommended reviews**: Mean Value rating = 2.22 out of 10
- **Recommended reviews**: Mean Value rating = 4.29 out of 10
- **49 of 127** (38.6%) non-recommended cases have a Value rating of 1 (poorest possible)

This component shows a Spearman correlation of 0.658 with recommendation status—substantially higher than other service dimensions (Staff Service: 0.141; Seat Comfort: 0.047).

### 2. Distribution of Non-Recommended Reviews

Despite mixed overall quality perceptions, non-recommended reviews span a broad range of Overall Ratings:

| Overall Rating | Count | Mean Value Rating |
|---|---|---|
| 1 | 29 | 1.0 |
| 2 | 22 | 1.9 |
| 3 | 17 | 2.1 |
| 4 | 15 | 2.5 |
| 5-10 | 44 | 3.1 |

**Importantly**, 44 reviews (34.6%) with Overall Ratings of 5 or higher were still marked non-recommended, indicating that strong service delivery alone does not guarantee recommendation when value perception is poor.

### 3. Common Operational and Service Issues

Analysis of review titles and content reveals recurring patterns:

| Issue Category | Frequency | Key Themes |
|---|---|---|
| **Seat/Comfort Issues** | 64% (81 reviews) | Seats not functioning (stuck reclines), worn older aircraft, uncomfortable sleeping |
| **Service Inconsistency** | 49% (62 reviews) | Crew quality decline, slow/unequal service across cabin sections |
| **Delays & Disruptions** | 36% (46 reviews) | Flight delays, missed connections, boarding bottlenecks |
| **Aircraft/Fleet Concerns** | 35% (44 reviews) | Older A350/777 instead of newer Q-Suite, aircraft downgrades, lack of promised seat type |
| **Compensation Disputes** | 25% (32 reviews) | Refund requests ignored, inadequate compensation offers (e.g., avios instead of cash), billing errors |
| **Food/Beverage Issues** | 47% (59 reviews) | Subpar meal quality, limited vegan options, inconsistent standards |
| **Expectations Misalignment** | 32% (41 reviews) | Promised aircraft not delivered, seat reservations changed, "lite" tickets with unexpected restrictions |

### 4. Traveler Segmentation

Non-recommended reviews are distributed across all traveler types:

- **Business Travelers**: 46 (36%)
- **Solo Leisure**: 41 (32%)
- **Couple Leisure**: 30 (24%)
- **Family Leisure**: 10 (8%)

Business travelers represent the largest segment, suggesting high expectations among this cohort regarding service consistency and value delivery.

### 5. Route Profile

Approximately 75% of non-recommended reviews concern **long-haul premium routes**, which typically involve higher fares and greater expectations. Medium-haul widebody routes account for 18%, indicating that value perception issues transcend flight distance.

### 6. Distinction Between Low Overall Ratings vs. Non-Recommendation

A notable finding is that **not all low-rated flights are non-recommended, nor are all non-recommended flights uniformly low-rated**:

- **44 cases** with Overall Ratings ≥5 are still non-recommended (often citing fare premium, aircraft downgrade, or unresolved compensation)
- These cases typically feature moderate-to-good service ratings but explicit frustration with value proposition or unmet expectations

### 7. Weak Correlations for Traditional Service Metrics

Interestingly, individual service component ratings show weak correlation with recommendation status:

- Seat Comfort: 0.047
- Food & Beverages: 0.028
- Inflight Entertainment: -0.013
- Staff Service: 0.141

This indicates that passengers don't necessarily recommend based on isolated service quality metrics; instead, they integrate these with value perception and expectations alignment.

## Root Cause Patterns

Three primary drivers emerge:

1. **Price-to-Quality Mismatch**: High fares combined with aging aircraft, service lapses, or lack of promised amenities (Q-Suite availability) trigger "not worth the cost" sentiment.

2. **Expectation-Reality Gap**: Booking confirmations and website layouts promise specific aircraft/seat configurations; actual delivery differs, eroding trust.

3. **Unresolved Service Failures**: Delays, compensation disputes, and crew issues become recommendation-killers when resolution is inadequate or absent.

## Important Caveats

- **Subjectivity**: Value judgments are passenger-specific; business travelers and leisure passengers may weight cost differently.
- **Temporal Variation**: Data spans multiple years (May 2016–Dec 2023); service standards and fleet composition changed over this period, explaining aircraft-type variability.
- **Selection Bias**: Only passengers motivated to review (either highly satisfied or very dissatisfied) appear in the dataset; average experiences may be underrepresented.

## Conclusion

Qatar Airways Business-Class non-recommendations stem primarily from **perceived poor value for money**—a composite judgment integrating fare level, aircraft modernity, service delivery, and expectation alignment. While individual service components (food, seat comfort, staff) remain important, they are subsidiary to the broader value calculation. Non-recommendations cluster among passengers facing aircraft downgrades, unresolved operational disruptions, or fare premiums without corresponding product differentiation.
