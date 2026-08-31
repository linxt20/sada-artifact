---
dataset: airlines_review
scenario: causal_improve_singapore
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "overall_rating_recommendation"
query: "How can Singapore Airlines improve its overall rating and recommendation rate, especially on flights where passengers do not recommend it (Recommended = no)?"
source_table: augment_table/airlines_review/causal_improve_singapore/haiku__skill_off_update.csv
generated_at: 2026-07-28T12:57:03.137904+00:00
wall_seconds: 62.75
---

# Singapore Airlines: Analysis of Non-Recommended Reviews and Improvement Opportunities

## Executive Summary

Singapore Airlines faces a significant challenge with **35.6% of reviews being non-recommended** (320 out of 900 reviews). Non-recommended passengers rate the airline an average of **2.77/10**, compared to 8.61/10 for recommended passengers. The primary driver of dissatisfaction is **perceived poor value for money** (1.82/10 vs. 4.34/10 for recommended passengers), creating a critical 2.52-point gap that directly correlates with recommendation likelihood.

## Key Findings

### 1. **Value for Money is the Dominant Pain Point** (43% of critical issues)
- **138 of 320 non-recommended reviews** cite "Value for Money" as the lowest-rated service dimension
- Non-recommended passengers rate Value for Money at **1.82/10** compared to **4.34/10** for recommended passengers
- This 2.52-point gap is by far the largest differential across any service dimension
- Notably, other service dimensions (Seat Comfort: 3.66, Staff Service: 3.80, Food & Beverages: 3.42) are relatively consistent between recommended and non-recommended passengers, suggesting the value perception issue is distinct

### 2. **Economy Class Bears the Brunt** (67% of non-recommended reviews)
- **214 non-recommended reviews** are from Economy Class passengers
- Economy passengers rate overall experience at **2.57/10** when not recommending
- Value for Money rating for non-recommended Economy: **1.77/10** (lowest among all segments)
- Represents a significant profitability risk, as Economy typically comprises the highest volume

### 3. **Secondary Issues Create Compounding Dissatisfaction**
Beyond value, distinct critical issues emerge with specific service breakdowns:

| Critical Issue Type | Count | Primary Weakness | Avg Overall Rating |
|---|---|---|---|
| Value Issue | 91 | Value for Money: 1.35/10 | 2.56 |
| Seat Comfort Issue | 65 | Seat Comfort: 1.51/10 | 2.58 |
| Food Issue | 64 | Food & Beverages: 1.44/10 | 2.95 |
| Staff Service Issue | 53 | Staff Service: 1.34/10 | 2.75 |

- When seat comfort problems occur, passengers also report low value perception (1.89/10)
- Food quality issues compound with low value ratings (1.69/10)
- Staff service failures correlate with lowest overall ratings

### 4. **Severity: 67% of Non-Recommended Reviews are Highly Negative**
- **215 of 320 non-recommended reviews** (67%) rate the experience 1-3/10
- Only **2.5%** of non-recommended reviews achieve ratings of 7 or higher
- This indicates deep dissatisfaction rather than marginal preference for alternatives

### 5. **Business and Leisure Segments Equally Affected**
- Non-recommended distribution: Solo Leisure (31%), Couple Leisure (30%), Family Leisure (20%), Business (18%)
- High-value customer segment shows only slightly better: 3.17/10 overall rating vs. 2.58/10 for economy segment
- No segment is immune to the value-for-money perception problem

## Actionable Improvement Recommendations

### Priority 1: Address Value Perception in Economy Class
**Concrete Actions:**
- Review pricing strategy relative to perceived service delivery—the 2.52-point gap in Value for Money ratings suggests customers feel prices exceed actual benefits
- Implement transparent pricing communication highlighting included services, extra amenities, or loyalty value
- Consider tiered pricing or clearer unbundling to align expectations with purchase

### Priority 2: Fix Seat Comfort in Economy/Premium Economy
- 65 non-recommended reviews cite seat comfort as the critical issue
- Seat Comfort ratings of 1.51/10 when this is the problem indicate operational or product failure
- Audit current seat configuration, padding, and legroom against passenger feedback in reviews

### Priority 3: Improve Food & Beverage Quality
- 64 reviews flag food as the critical issue, with ratings dropping to 1.44/10
- This affects perceptions across cabin classes and traveler types
- Quality control or menu refresh recommended

### Priority 4: Staff Training on Service Recovery
- Staff Service issues (53 reviews) often co-occur with low value perception (1.89/10)
- Empowered staff recovery protocols could mitigate negative experiences before they result in non-recommendation

## Data Confidence Notes

- The analysis is based on **320 verified non-recommended reviews**, providing robust visibility into dissatisfaction drivers
- The Value for Money metric clearly delineates non-recommended from recommended passengers (2.52-point gap)
- Secondary issues (seat comfort, food, staff) show distinct, measurable breakdowns within their respective categories
- **Weak signal:** 33 non-recommended reviews had no critical issue flagged but still resulted in non-recommendation, suggesting some dissatisfaction stems from combination effects rather than single failure points

## Conclusion

Singapore Airlines' recommendation rate is constrained primarily by perceived **poor value for money in Economy Class**, which manifests as deeply negative overall ratings. Addressing pricing transparency, seat quality, and food standards in Economy offers the highest leverage to improve recommendation rates. Secondary service failures in seat comfort and staff service amplify dissatisfaction and should be addressed systematically alongside the primary value-perception issue.
