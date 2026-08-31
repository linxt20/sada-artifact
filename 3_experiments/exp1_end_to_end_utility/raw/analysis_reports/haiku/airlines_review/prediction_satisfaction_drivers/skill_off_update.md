---
dataset: airlines_review
scenario: prediction_satisfaction_drivers
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating"
query: "What drives customer satisfaction (Overall Rating) across the different airlines?"
source_table: augment_table/airlines_review/prediction_satisfaction_drivers/haiku__skill_off_update.csv
generated_at: 2026-07-28T12:58:57.819915+00:00
wall_seconds: 57.33
---

# Satisfaction Drivers Analysis: Airlines Review Dataset

## Executive Summary

This analysis identifies the key factors driving customer satisfaction (Overall Rating) across airlines based on 900 reviews. **Value For Money** emerges as the dominant satisfaction driver, with an exceptionally strong correlation (r=0.878) with overall ratings. Service consistency and the absence of poorly-rated dimensions are also significant negative drivers when problematic.

## Primary Satisfaction Drivers

### 1. **Value For Money (Dominant Factor)**
- **Correlation with Overall Rating: 0.878** (strongest predictor)
- **Impact Magnitude:** Reviews rating Value For Money ≥4 average **8.57** overall rating, while those rating it ≤2 average **2.92** overall rating
- **Threshold Effect:** Clear bifurcation at Value For Money rating ≥4 separates highly satisfied from dissatisfied customers
- **Business Implication:** Pricing strategy and perceived value are critical to satisfaction outcomes

### 2. **Average Service Rating (Secondary Driver)**
- **Correlation with Overall Rating: 0.567**
- **Pattern:** Moderate positive relationship indicating cumulative service quality matters
- Reviews with high ratings across seat comfort, staff service, and beverages show stronger overall satisfaction

### 3. **Service Consistency (Negative Driver)**
- **Correlation with Overall Rating: -0.314**
- **Finding:** High variance in service dimensions (inconsistent quality) undermines satisfaction
- Reviews with Service Consistency >1.5 average only **4.75** overall rating
- Customers prefer uniform service quality over spotty excellence

### 4. **Poor Dimensions Count (Negative Driver)**
- **Correlation with Overall Rating: -0.509**
- **Clear Gradient Effect:**
  - 0 poor dimensions: Average rating **7.90**
  - 1 poor dimension: Average rating **6.13**
  - 2+ poor dimensions: Average rating drops to **4.33** or lower
- **Implication:** Any weak service area significantly impacts overall satisfaction

## Service Dimensions (Individual Ratings)

When analyzed individually, service dimensions show weaker direct correlations:

| Dimension | Correlation | Pattern |
|-----------|------------|---------|
| **Staff Service** | 0.206 | Moderate weak correlation |
| **Seat Comfort** | 0.205 | Moderate weak correlation |
| **Food & Beverages** | 0.130 | Weak correlation |
| **Inflight Entertainment** | 0.089 | Minimal correlation |

**Key Finding:** Individual service elements are less predictive than **overall value perception** or the **absence of weaknesses**. High satisfaction (Rating ≥9) requires strong ratings across multiple dimensions:
- High satisfaction group (Rating ≥9): Value For Money avg **4.63**, Staff Service avg **3.94**
- Low satisfaction group (Rating ≤3): Value For Money avg **1.50**, Staff Service avg **3.17**

## Satisfaction Patterns by Segment

### By Cabin Class
- **Business Class:** Highest average rating (**6.78**) with higher Value For Money scores (3.52)
- **Economy Class:** Lowest average rating (**5.24**) with lowest Value For Money perception (2.99)
- **Premium Economy:** Mid-range (**5.98**) despite highest Seat Comfort (3.84)

**Insight:** Business class passengers perceive better value despite higher prices, while economy passengers rate value poorly.

### By Traveler Type
- **Solo Leisure:** Highest satisfaction (**6.03**)
- **Business:** Moderate satisfaction (**5.83**)
- **Couple/Family Leisure:** Lower satisfaction (**5.24–5.17**)

### Recommendation Status (Strong Indicator)
- **Recommended "yes":** Average rating **8.56**, Value For Money **4.36**
- **Recommended "no":** Average rating **2.33**, Value For Money **1.75**

## Cumulative Effect of Multiple Quality Issues

- **21.9% of reviews** have all key dimensions (Seat Comfort, Staff Service, Value For Money) rated ≥4: Average rating **8.75**
- **5.4% of reviews** have all key dimensions rated ≤2: Average rating **1.90**
- One single poorly-rated dimension in an otherwise adequate review typically reduces satisfaction from ~6.5 to ~4.3 range

## Important Exceptions and Limitations

1. **Low Intercorrelation Among Service Dimensions** (range: 0.067–0.199): Service quality areas operate largely independently, suggesting distinct operational challenges. A strong staff service rating does not guarantee good seat comfort.

2. **Non-Linear Relationships:** The relationship between Value For Money and overall rating shows a sharp threshold effect rather than gradual progression, indicating emotional/expectation-driven responses to pricing perceptions.

3. **Weak Individual Dimension Predictors:** Seat comfort and staff service individually show modest correlations (0.205, 0.206), but become powerful when combined with value perception.

4. **Limited Actionability from Review Length:** Longer reviews correlate with lower ratings (r=-0.183), suggesting dissatisfied customers write more detailed explanations rather than extended positive feedback.

## Recommendations for Satisfaction Improvement

1. **Prioritize Value Perception:** Address pricing strategy and perceived value over isolated service improvements
2. **Ensure Consistency:** Minimize variance in service quality across all dimensions—one weak area significantly damages overall satisfaction
3. **Segment Strategies:** Economy passengers need stronger value messaging; business-class retention focuses on premium positioning
4. **Multi-Dimension Excellence:** Avoid over-investing in single service areas; target simultaneous improvements across seat comfort, staff service, and amenities

## Dataset Characteristics

- **Sample Size:** 900 reviews
- **Overall Rating Distribution:** Bimodal, concentrated at extremes (1-3 and 9-10), with mean 5.66
- **Premium Class:** 28.9% of sample
- **Verified Reviews:** 75.9% of sample
- **Coverage:** 820 unique routes, reviews from 2023–2024
