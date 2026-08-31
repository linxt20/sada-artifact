---
dataset: airlines_review_full
scenario: causal_improve_singapore
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "overall_rating_recommendation"
query: "How can Singapore Airlines improve its overall rating and recommendation rate, especially on flights where passengers do not recommend it (Recommended = no)?"
source_table: augment_table/airlines_review_full/causal_improve_singapore/haiku__skill_on_v11_update.csv
generated_at: 2026-08-03T05:49:08.393084+00:00
wall_seconds: 77.05
---

# Singapore Airlines: Improving Overall Rating and Recommendation Rate

## Executive Summary

This analysis examines 8,100 Singapore Airlines reviews (3,813 non-recommended, 4,287 recommended) to identify drivers of non-recommendation and actionable improvement strategies. The data reveals a stark performance gap: non-recommended passengers rate the airline 2.37/10 on average, while recommended passengers rate it 8.53/10. Critically, **value for money emerges as the dominant factor**, with a Pearson correlation of **r=0.829** with recommendation status—far exceeding other service metrics.

---

## Key Findings

### 1. **Value For Money is the Primary Driver**
- Non-recommended passengers rate value at **1.75/5** vs. 4.39/5 for recommended passengers (difference: 2.64 points)
- **2,093 of 3,813** non-recommended reviews (54.8%) scored value at the lowest level (1/5)
- Value perception directly maps to recommendation: only 39 of 3,813 non-recommended reviews gave value a maximum score (5/5)

**Implication**: Pricing strategy and perceived value alignment are more critical than individual service components.

### 2. **Crew Service Quality is Severely Problematic**
Among non-recommended passengers:
- **Rude/Dismissive**: 1,520 reviews (40%)
- **Inattentive/Perfunctory**: 1,149 reviews (30%)
- **Professional/Warm**: only 173 reviews (4.5%)

In contrast, 83% of recommended passengers experienced "professional_warm" service.

**Implication**: Interpersonal service standards have collapsed for a significant portion of non-recommended flights, suggesting training or staffing issues.

### 3. **Economy Class Bears Disproportionate Non-Recommendation (53.2%)**
- 2,846 of 5,348 economy reviews were non-recommended
- Average rating: 2.17/10
- Average value rating: 1.70/5
- Average seat comfort: 3.08/5

**Implication**: Economy passengers perceive poor seat quality and insufficient value, making this the highest-risk segment.

### 4. **Family Travelers are Particularly Dissatisfied (53.4% non-recommendation)**
- 812 family-traveling passengers were non-recommended
- Average rating: 2.01/10 (lowest among segments)
- Average value: 1.64/5
- Likely drivers: seating discomfort for children, limited accommodation, unmet needs

**Implication**: Family-specific amenities and service standards require urgent review.

### 5. **Aircraft Condition Shows Measurable Impact**
Non-recommended passengers experienced:
- **Old/Worn/Dirty**: 428 cases vs. 232 for recommended
- **Modern/Well-Maintained**: only 264 cases vs. 2,132 for recommended

This correlates with Seat Comfort ratings (3.13/5 for non-recommended vs. 3.67/5 for recommended).

### 6. **Ground Staff Service Deficiency Compounds Problems**
Non-recommended experiences involved:
- **Disorganized/Unhelpful**: 1,933 cases (51%)
- **Rude/Dismissive**: 1,339 cases (35%)
- **Efficient/Helpful**: only 90 cases (2.4%)

This pre-flight friction amplifies dissatisfaction through the customer journey.

---

## Secondary Service Gaps (Weaker Evidence)
While statistically significant, the following show smaller effect sizes:
- **Staff Service**: r=0.207 (moderate correlation)
- **Seat Comfort**: r=0.192
- **Food & Beverages**: r=0.148
- **Inflight Entertainment**: r=0.116

These are *symptoms* of value-related dissatisfaction rather than independent drivers.

---

## Recommended Improvement Strategy

### **Tier 1: High-Impact Interventions (Immediate)**
1. **Value Reassessment**: Audit pricing against competitor benchmarks and service delivery levels. Non-recommended passengers at 1.75/5 on value indicate systematic misalignment.
2. **Crew Training Overhaul**: Implement immediate retraining on customer service quality. 70% of non-recommended passengers experienced poor/rude service.
3. **Ground Staff Protocol**: Standardize check-in and boarding processes to reduce friction for dissatisfied passengers.

### **Tier 2: Segment-Specific Fixes**
4. **Economy Relaunch**:
   - Upgrade seat comfort (currently 3.08/5)
   - Consider seat width/padding improvements on regional aircraft
   - Price transparently to align expectations
5. **Family Travel Program**:
   - Dedicated family seating zones
   - Enhanced child accommodations
   - Service training for family interactions

### **Tier 3: Asset Management**
6. **Fleet Renewal**: Prioritize retirement of "old_worn_dirty" aircraft perceived by 1.5x more non-recommended passengers.

---

## Caveats and Limitations
- Text-based review analysis shows recency bias toward recent negative experiences
- "Unknown" labels on crew/ground staff quality (67-1,501 cases per dimension) represent incomplete data attribution
- Causality assumed but not proven: value perception may follow from overall experience rather than preceding it
- No temporal trend analysis—cannot distinguish systemic degradation from seasonal variation

---

## Conclusion
Singapore Airlines' recommendation gap is **primarily a value-perception crisis**, exacerbated by crew service inconsistency. The airline must address pricing-to-service alignment before expecting recommendation rate improvements. Economy and family segments are most vulnerable. Without intervention in value alignment and crew quality, the current 47% non-recommendation rate will persist.
