---
dataset: airlines_review_full
scenario: causal_qatar_business
variant: original
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "non_recommendation_outcome"
query: "Explain why some Qatar Airways Business-Class flights receive a non-recommended (Recommended = no) result."
source_table: augment_table/airlines_review_full/causal_qatar_business/original.csv
generated_at: 2026-08-03T05:39:24.670339+00:00
wall_seconds: 88.9
---

# Qatar Airways Business-Class Non-Recommendation Analysis

## Executive Summary

Among 592 Qatar Airways Business-Class reviews in this dataset, 127 (21.5%) were marked as non-recommended. The primary driver of non-recommendations is **poor perceived value for money**, followed by **low overall satisfaction ratings**. While individual service metrics (seat comfort, staff service, food) show relatively modest differences between recommended and non-recommended cases, the cumulative experience and perceived cost-value trade-off emerge as the decisive factors.

## Key Findings

### 1. Value For Money is the Strongest Differentiator

The most striking difference between non-recommended and recommended flights is in the **Value For Money** rating:

- **Non-Recommended average: 2.22/5** (median: 2)
- **Recommended average: 4.29/5** (median: 5)  
- **Difference: -2.07 points**

Among non-recommended cases, **54.3% (69 out of 127)** rated Value For Money at 2 or below. This is corroborated by correlation analysis: Value For Money shows the second-strongest correlation with recommendation status (r = 0.658), nearly matching the correlation of Overall Rating (r = 0.666).

### 2. Low Overall Satisfaction Drives Decisions

Overall Rating is the strongest predictor of recommendation:

- **Non-Recommended average: 3.82/10** (median: 3)
- **Recommended average: 8.43/10** (median: 9)
- **Difference: -4.61 points**

A striking **75.6% of non-recommended cases (96 out of 127)** had Overall Ratings of 5 or below, indicating fundamentally unsatisfactory experiences despite potentially acceptable individual service components.

### 3. Service Attributes Show Weaker Direct Association

Individual service quality metrics show surprisingly modest differences:

| Metric | Non-Rec Avg | Rec Avg | Difference | Correlation |
|--------|-----------|---------|-----------|------------|
| **Seat Comfort** | 3.87 | 4.01 | -0.14 | 0.047 |
| **Staff Service** | 4.01 | 4.39 | -0.38 | 0.141 |
| **Food & Beverages** | 3.85 | 3.94 | -0.09 | 0.028 |
| **Inflight Entertainment** | 4.16 | 4.12 | +0.03 | -0.013 |

These modest differences suggest that passengers do not withdraw recommendations solely due to minor deficiencies in comfort or amenities. Rather, issues must accumulate or trigger broader dissatisfaction.

### 4. Notable Exceptions: Premium Experience + Poor Value

The analysis reveals 22 non-recommended cases with Overall Ratings ≥ 7, suggesting that passengers may withhold recommendations even when experiencing objectively good service—primarily due to value concerns. Examples include:

- Positive overall assessment (7/10 rating) but perceived mediocre value
- Excellent new Q-suite product (10/10 rating) withheld recommendation due to cost concerns
- Strong service reviews offset by moderate value ratings (3/5)

These exceptions indicate that **value perception operates independently** from service quality and can override positive experiences.

### 5. Specific Problem Patterns in Non-Recommended Reviews

Qualitative analysis of review titles and content reveals recurring issues:

**Operational/Service Failures:**
- Downgrades to lower cabin configurations (11 mentions of "downgrade")
- Flight delays and ground operations (19 mentions of "delay")
- Uncomfortable seating/equipment defects ("seat wouldn't stay up")
- Ground services failures (bus rides instead of stairs, lounge quality issues)

**Financial/Compensation Issues:**
- Complaints about excessive ancillary fees (22 mentions of "paid")
- Perceived inadequate compensation for service failures (15 mentions of "compensation")
- Refund disputes and partial reimbursements
- Unexpected upgrade costs

**Product/Quality Degradation:**
- Aircraft downgrade from new Q-suites to older configurations
- Crew quality concerns ("crew level has come down")
- Food quality issues ("sub par")
- Aging aircraft products

### 6. Traveller Type Variations

Business travelers constitute a disproportionate share of non-recommendations relative to their overall representation:

- Non-Recommended: 36.2% Business travelers (46/127)
- Recommended: 20.6% Business travelers (96/465)

This suggests business travelers may have higher expectations or clearer price-sensitivity thresholds for perceived value.

## Weak Evidence / Important Caveats

1. **Individual service quality is not the primary issue:** Seat Comfort, Food & Beverages, and Entertainment show almost no correlation with recommendation status (r < 0.05). Most non-recommended cases still rate these aspects at 4+ out of 5.

2. **Some high-quality experiences go unrecommended:** 22 cases (17.3% of non-recommended) had Overall Ratings of 7+, indicating that even materially good experiences can be deemed unrecommendable if perceived value is poor.

3. **Inverse cases exist but are rare:** Only 14 recommended cases (3% of recommended) had Overall Ratings ≤ 3, suggesting the Overall Rating-Recommendation link is strong but not absolute.

4. **Unverified reviews show similar patterns:** 20 of 127 non-recommended cases are unverified, but the distribution of issues is consistent with verified reviews.

## Conclusion

Qatar Airways Business-Class flights receive non-recommended status primarily due to a perceived **mismatch between price paid and experience delivered**. While specific operational failures (downgrades, delays, equipment issues) and financial frictions (high fees, compensation disputes) trigger negative recommendations, the underlying pattern is one of unmet value expectations.

Service quality attributes (comfort, food, entertainment, staff) are generally maintained at acceptable levels even in non-recommended cases, but they do not offset poor value perception. Business travelers appear most sensitive to this value proposition, and issues like aircraft downgrades or premium-to-standard cabin reassignments significantly amplify recommendation withdrawal.

The data indicates that improving recommendation rates requires addressing **value delivery and cost transparency**, not just incremental improvements to already-adequate service amenities.
