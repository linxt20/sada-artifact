---
dataset: airlines_review
scenario: causal_qatar_business
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "non_recommendation_outcome"
query: "Explain why some Qatar Airways Business-Class flights receive a non-recommended (Recommended = no) result."
source_table: augment_table/airlines_review/causal_qatar_business/haiku__skill_off_update.csv
generated_at: 2026-07-28T12:57:00.269624+00:00
wall_seconds: 59.88
---

# Analysis Report: Non-Recommended Qatar Airways Business-Class Flights

## Executive Summary

Of 592 Qatar Airways Business-Class reviews in the dataset, 127 (21.5%) received a non-recommended (Recommended = no) result. The primary driver is **poor perceived value for money**, which severely impacts the recommendation decision despite mixed satisfaction with service and comfort elements.

## Key Findings

### 1. Dominant Factor: Value For Money Crisis

**Value For Money is the critical differentiator:**
- Non-recommended flights have a mean Value For Money rating of **2.22/5**, compared to **4.29/5** for recommended flights
- **54.3% of non-recommended flights** (69/127) received a rating of 1-2 for Value For Money
- Non-recommended flights with low overall ratings (< 5) show a particularly severe Value For Money score of **1.88/5**

This metric overwhelmingly influences the recommendation outcome. Common complaints in these reviews cite excessive ticket pricing, unexpected upgrade fees, or perceived pricing that does not align with service quality delivered.

### 2. Overall Service Quality Paradox

Interestingly, non-recommended flights show **adequate but unremarkable ratings** across individual service categories:

| Category | Non-Recommended Mean | Recommended Mean |
|----------|---------------------|-----------------|
| Seat Comfort | 3.87 | 4.01 |
| Staff Service | 4.01 | 4.39 |
| Food & Beverages | 3.85 | 3.94 |
| Inflight Entertainment | 4.16 | 4.12 |
| **Overall Rating** | **3.82** | **8.43** |

The large gap in Overall Rating suggests customers weigh the **value proposition** heavily in their global assessment, independent of individual service elements.

### 3. Secondary Drivers: Inconsistency and Complaints

**Multiple pain points:**
- **65.4% of non-recommended flights** (83/127) have an Overall Rating < 5
- **51.2%** show high rating variance (> 1.5 standard deviation), indicating inconsistent experiences across flight aspects
- **29.1%** contain documented major complaints (equipment issues, lost baggage, downgrades, service failures)
- **73.2%** have at least one category rated 1-2, showing concentration of low scores

Flights with major complaints show a compounded effect: mean Overall Rating of 2.84 and Value For Money of 2.03, demonstrating that specific service failures compound dissatisfaction.

### 4. Specific Complaint Patterns

Evidence from review texts reveals:

- **Pricing dissatisfaction**: High-cost tickets ("fare was through the roof") with dated aircraft or reduced amenities (e.g., standard A350 instead of Qsuites)
- **Operational issues**: Long check-in waits, downgrade situations with inadequate compensation
- **Service-product misalignment**: Premium pricing not matched by expected service standards (stressed staff, limited food offerings)
- **Unresolved customer service**: Refund and compensation disputes

These issues directly impact the Value For Money perception and Overall Rating.

## Weak Evidence / Exceptions

- **Seat Comfort** is not a primary driver: Only 15.0% of non-recommended flights rate Seat Comfort 1-2; many have 4-5 ratings despite non-recommendation
- **Positive individual ratings with recommendation=no**: Some reviews show high satisfaction in specific areas (e.g., Inflight Entertainment 5/5) yet still non-recommended due to value or overall context
- **Mixed experiences**: A subset (29.1%) has multiple low ratings across categories, suggesting systemic issues rather than isolated dissatisfaction

## Conclusion

Qatar Airways Business-Class flights are recommended primarily based on **perceived value for money relative to service and experience quality**. Non-recommended flights cluster around:

1. **High pricing without commensurate service delivery** (primary factor)
2. **Low overall experience ratings** (< 5) driven by inconsistency or specific failures
3. **Major operational/service complaints** that degrade confidence

Individual service dimensions (comfort, food, entertainment) are often adequate but insufficient to overcome poor value perception or significant service failures. The recommendation decision operates as a holistic assessment where pricing expectations and overall satisfaction heavily outweigh component-level ratings.
