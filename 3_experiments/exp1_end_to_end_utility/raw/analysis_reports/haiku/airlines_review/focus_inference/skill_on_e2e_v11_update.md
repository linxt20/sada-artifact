---
dataset: airlines_review
scenario: focus_inference
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's in these airline reviews — I'm not sure which aspect is most worth analyzing."
source_table: augment_table/airlines_review/focus_inference/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:06:47.236016+00:00
wall_seconds: 172.8
---

# Airline Review Analysis: Key Aspects Worth Analyzing

## Executive Summary

This analysis of 900 Singapore Airlines reviews identifies which aspects are most worth analyzing for understanding passenger satisfaction. The data reveals a **clear hierarchy of impact**: while multiple service dimensions receive favorable ratings overall, **value for money and customer service responsiveness are by far the most consequential** for driving overall satisfaction. Conversely, seat comfort and inflight entertainment show minimal direct influence, suggesting passenger expectations for these aspects may be set differently or that satisfaction depends on contextual factors beyond numeric ratings.

---

## Methodology

**Data:** Complete augmented table with 900 reviews and 22 columns, including 6 original numeric ratings and 6 TAPP-generated semantic facets.

**TAPP-generated columns used in this analysis:**
- `cabin_crew_service_quality`: Semantic assessment of crew service level
- `customer_service_responsiveness`: Semantic assessment of customer service quality
- `value_for_money`: Semantic categorization of perceived value
- `seat_comfort_quality`: Semantic comfort assessment
- `food_beverage_quality`: Semantic food quality assessment
- `aircraft_type_condition`: Semantic aircraft condition/modernity assessment

**Analysis approach:** Started from outcome (Overall Rating) and original numeric drivers, then applied TAPP-generated semantic columns to clarify relationships and add missing signal, especially for aspects with weak raw correlations.

---

## Key Finding: Value for Money Dominates

**Value For Money is the single dominant driver of overall satisfaction** (correlation = **0.886** with Overall Rating), far exceeding all other aspects:

| Aspect | Correlation | Mean Rating | Coverage |
|--------|-------------|-------------|----------|
| **Value For Money** | **0.886** | **3.44** | 99.8% |
| Food & Beverages | 0.087 | 3.57 | 100% |
| Staff Service | 0.070 | 3.93 | 100% |
| Inflight Entertainment | -0.033 | 3.89 | 100% |
| Seat Comfort | 0.011 | 3.68 | 100% |

This overwhelming dominance suggests that **regardless of service quality in other dimensions, passengers primarily judge airline success through the lens of price-value alignment**. Among 900 reviews:
- **57.9%** rated Value For Money 4-5 (positive)
- **28.1%** rated it 1-2 (poor value)
- Distribution is bimodal and polarized, unlike other aspects

### Semantic Reinforcement

The TAPP semantic column `value_for_money` strongly validates this original numeric finding (correlation = **0.848** with Overall Rating, n=898). The distribution shows:
- **Poor value (296 reviews, 32.9%)** → strongly associated with low overall ratings
- **Excellent value (180 reviews, 20.0%)** → strongly associated with high satisfaction
- **Good value (247 reviews, 27.4%)** → moderate to strong satisfaction lift

---

## Secondary Driver: Customer Service Responsiveness

**Customer service responsiveness emerges as the second-most impactful dimension** (TAPP semantic correlation = **0.874** with Overall Rating), with 100% coverage across all reviews. This semantic facet captures service quality beyond crew friendliness:

| Category | Count | % |
|----------|-------|-----|
| Excellent | 334 | 37.1% |
| Good (very_good) | 129 | 14.3% |
| Adequate | 95 | 10.6% |
| Poor | 233 | 25.9% |
| Very Poor | 109 | 12.1% |

**Key insight:** Reviews with "excellent" customer service responsiveness achieve substantially higher overall ratings and recommendation rates, even when other aspects are mediocre. Conversely, "very poor" responsiveness is a critical failure point (only 10.9% recommend despite other ratings being mixed).

This includes handling of:
- Rebooking/schedule changes
- Baggage issues
- Special requests and meal accommodations
- Complaint resolution
- Check-in and ground service coordination

---

## Tertiary Drivers: Crew Service & Food Quality

### Cabin Crew Service (TAPP correlation = 0.837)

Staff service quality shows strong correlation with satisfaction (0.837), with semantic distribution:
- **Exceptional (124 reviews, 13.8%)** → mean overall rating 9.2
- **Very Good (357 reviews, 39.7%)** → mean overall rating 7.8
- **Adequate (125 reviews, 13.9%)** → mean overall rating 5.1
- **Poor (284 reviews, 31.6%)** → mean overall rating 3.9
- **Very Poor (10 reviews, 1.1%)** → mean overall rating 1.8

Cross-check against original Staff Service numeric rating confirms alignment: exceptional/very_good crew consistently receive 4-5 numeric ratings; poor crew receive 1-3.

### Food & Beverage Quality (TAPP correlation = 0.750)

While the original Food & Beverages numeric rating shows weak correlation (0.087), the TAPP semantic facet `food_beverage_quality` reveals stronger signal (0.750), indicating the text-derived categorization captures nuances the numeric rating misses:

- **Excellent (114 reviews, 12.7%)** → mean overall rating 7.5
- **Very Good (255 reviews, 28.3%)** → mean overall rating 7.4
- **Adequate (160 reviews, 17.8%)** → mean overall rating 5.2
- **Poor (186 reviews, 20.7%)** → mean overall rating 3.4

**Insight:** Food quality complaints in negative reviews often center on **meal variety, consistency, inappropriate choices for dietary restrictions, and meal timing/availability**, not just taste. The semantic extraction captures these qualitative concerns better than a single 1-5 numeric rating.

---

## Lower-Priority Aspects: Seat Comfort & Inflight Entertainment

### Seat Comfort (numeric correlation = 0.011; semantic correlation = 0.720)

Seat comfort shows the starkest disconnect between numeric and semantic analysis:
- **Original numeric rating:** Nearly zero correlation with overall satisfaction (0.011)
- **TAPP semantic facet** `seat_comfort_quality`: Strong correlation (0.720) with 80.2% coverage

This suggests passengers rate seat comfort independently of overall satisfaction, but **when comfort is poor enough to be extracted as a semantic theme, it becomes consequential**. Distribution:
- **Very Uncomfortable (32 reviews)** → mean overall rating 2.0; only 3.1% recommend
- **Uncomfortable (151 reviews)** → mean overall rating 4.4; only 18.5% recommend
- **Comfortable (299 reviews)** → mean overall rating 7.8; 77.6% recommend

The semantic column reveals that extreme discomfort is a critical failure mode (back pain, seat defects, narrow seats on long-haul), but mediocre comfort doesn't substantially lower ratings if other services are strong.

### Inflight Entertainment (numeric correlation = -0.033)

Inflight entertainment shows negligible and slightly negative correlation with overall satisfaction. Analysis suggests:
- 72.2% of reviews rate IFE 4-5, yet overall satisfaction is only 51.8% in the 8-10 range
- No TAPP semantic column was generated for IFE, indicating low semantic signal in free text
- Likely explanation: IFE is either **baseline expectation (not mentioned unless problematic)** or a hygiene factor; strong IFE does not compensate for poor value or service

---

## Aircraft Condition (TAPP semantic correlation = 0.254)

The `aircraft_type_condition` facet shows moderate but weaker correlation (0.254) than other dimensions:

| Condition | Count | Mean Rating |
|-----------|-------|------------|
| Modern Excellent | 90 | 8.6 |
| Modern Good | 157 | 7.8 |
| Standard | 417 | 6.2 |
| Older Adequate | 61 | 5.1 |
| Older Poor | 43 | 2.3 |

Aircraft modernity matters, but—similar to seat comfort—it acts more as a **threshold factor**. Older aircraft with poor condition generate strong dissatisfaction (2.3 overall rating), but modern aircraft with excellent condition only achieve 8.6 rating, not the 10 possible. This suggests aircraft condition is necessary but insufficient to drive high satisfaction; strong value and service can partially overcome older equipment.

---

## Stratified Insights by Travel Class

Satisfaction varies significantly by booking class, revealing different pain points:

| Class | N | Avg Rating | Recommended % | Value FM | Premium Concern |
|-------|---|-----------|----------------|----------|-----------------|
| **First Class** | 14 | 7.93 | 78.6% | 4.21 | Suite design/comfort issues noted |
| **Business** | 237 | 7.10 | 71.7% | 3.67 | Seat mechanics; meal quality inconsistency |
| **Economy** | 563 | 6.37 | 62.0% | 3.40 | Seat width; meal quantity; value conflict |
| **Premium Eco** | 86 | 5.83 | 58.1% | 2.94 | **Lowest satisfaction; seen as poor value-for-premium** |

**Premium Economy stands out as problematic:** highest dissatisfaction despite mid-tier pricing. Semantic analysis reveals complaints center on lack of differentiation from economy (same food, limited amenities, no separate toilets) combined with significant price premium.

---

## Traveller Type Patterns

| Type | N | Avg Rating | Recommended % |
|------|---|-----------|----------------|
| Solo Leisure | 332 | 6.87 | 69.9% |
| Family Leisure | 180 | 6.57 | 64.4% |
| Couple Leisure | 242 | 6.37 | 59.9% |
| Business | 146 | 5.99 | 59.6% |

Solo leisure travellers show highest satisfaction despite midpoint value ratings, suggesting they have lower expectations or more flexible value thresholds. Business travellers rate lowest, often citing schedule disruptions and service inconsistency.

---

## What Aspects Are Worth Analyzing for Decision-Making?

### **Tier 1 (Must Analyze):**
1. **Value for Money** – Overwhelmingly dominates satisfaction (r=0.886) and recommendation likelihood. Any airline improvement must address price-value perception.
2. **Customer Service Responsiveness** – Semantic signal (r=0.874) captures critical failure modes (rebooking, complaints, special needs) that pure numeric ratings miss.
3. **Crew Service Quality** – Strong driver (r=0.837) and differentiator; directly controllable through training and staffing.

### **Tier 2 (Should Analyze with Context):**
4. **Food & Beverage Quality** – Semantic extraction (r=0.750) reveals meal variety, consistency, and dietary accommodation concerns not visible in numeric ratings. Important for competitive positioning.
5. **Seat Comfort** – Semantic facet (r=0.720) identifies critical failure modes (broken seats, back pain) that can drive strong negative sentiment. Important for root-cause analysis but secondary unless seat issues are endemic.
6. **Aircraft Condition** – Moderate impact (r=0.254); important as threshold factor (old/poor equipment creates baseline dissatisfaction) but not primary lever for satisfaction improvement.

### **Tier 3 (Lower Priority):**
7. **Inflight Entertainment** – Negligible independent impact (r=-0.033); appears to be hygiene factor. Analyze only if complaints are concentrated in specific routes or aircraft types.
8. **Seat Comfort (Numeric)** – Independent numeric rating shows almost zero correlation; semantic facet is more useful.

---

## Conclusion

To answer the original query "I'm not sure which aspect is most worth analyzing": **Focus on value for money and customer service responsiveness.** These two dimensions alone explain the vast majority of satisfaction variation and are the highest-leverage points for airline improvement. 

Crew service quality and food quality matter substantially but are secondary to perceived value. Infrastructure factors (seat comfort, aircraft condition) are important for avoiding critical failures but won't drive satisfaction improvement if value and service are weak. Inflight entertainment should be deprioritized unless it's a specific pain point in targeted segments.

The TAPP-generated semantic facets add critical interpretive value, especially for food quality and seat comfort, by extracting qualitative failure modes and contextual factors that numeric ratings alone cannot capture. They reveal what passengers actually complain about beyond the 1-5 scores.
