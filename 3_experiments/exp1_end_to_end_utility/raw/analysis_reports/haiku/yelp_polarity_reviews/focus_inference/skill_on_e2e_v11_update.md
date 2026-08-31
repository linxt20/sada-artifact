---
dataset: yelp_polarity_reviews
scenario: focus_inference
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What aspects of their experience are Yelp reviewers talking about?"
source_table: augment_table/yelp_polarity_reviews/focus_inference/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:24:33.452347+00:00
wall_seconds: 75.2
---

# Analysis Report: Yelp Reviewer Experience Aspects

**Query:** What aspects of their experience are Yelp reviewers talking about?

**Dataset:** 250 Yelp reviews (125 positive, 125 negative)  
**Augmented Columns Used:** `service_sentiment`, `service_failure_type`, `food_product_sentiment`, `product_quality_dimension`, `value_pricing_sentiment`

---

## Method Note

This analysis uses the following TAPP-generated augmented columns:
- **service_sentiment**: categorical classification of staff service sentiment (positive, negative, neutral, not_present)
- **service_failure_type**: specific service failure categories when negative (rude_dismissive, slow_service, inattentive, unavailable_staff, disorganized_seating, forgotten_by_staff, not_present)
- **food_product_sentiment**: sentiment about food/product quality (positive, negative, neutral, not_present)
- **product_quality_dimension**: specific quality dimension mentioned (flavor_taste, preparation_technique, temperature, portion_size, freshness, not_present)
- **value_pricing_sentiment**: judgment about pricing value (positive_value, overpriced, reasonable, not_present)

These augmented columns extract semantic signals from the review text to identify and classify the primary experience aspects reviewers discuss, enabling quantified analysis of what matters most to reviewers.

---

## Key Findings

### 1. Service/Staff Interaction Dominates Reviewer Attention

**Service is the most universally mentioned aspect**, appearing in **248 of 250 reviews (99.2%)**. This establishes service quality as the baseline lens through which reviewers evaluate their experience.

- **Positive reviews (n=125):** 111 mention positive service sentiment (88.8%)
- **Negative reviews (n=125):** 110 mention negative service sentiment (88.0%)

When service is criticized in negative reviews, reviewers specify failure types:
- **Rude or dismissive staff**: 17 reviews
- **Slow service**: 12 reviews  
- **Inattentive staff**: 12 reviews
- **Unavailable/absent staff**: 11 reviews
- **Disorganized seating**: 5 reviews
- **Forgotten by staff**: 1 review

**Insight:** Staff conduct, speed, and attentiveness are the primary service drivers. Staff rudeness (34% of service failures) and slow service (24%) are disproportionately salient in negative experiences.

---

### 2. Food/Product Quality Is the Secondary Primary Aspect

**Food and product quality is discussed in 203 of 250 reviews (81.2%)**, making it the second most common focus, with meaningful variance by polarity:

- **Positive reviews (n=125):** 92 discuss positive food sentiment (73.6%)
- **Negative reviews (n=125):** 83 discuss negative food sentiment (66.4%)

When quality is discussed, **flavor and taste dominate** as the evaluated dimension:
- **Flavor/taste**: 109 reviews (53.7% of all reviews)
- **Preparation technique**: 6 reviews
- **Portion size**: 4 reviews
- **Temperature**: 4 reviews
- **Freshness**: 2 reviews

**Insight:** Reviewers are taste-focused when discussing food. Positive reviews praise flavor; negative reviews blame bland, poorly cooked, or stale offerings. Structural concerns (portions, temperature, technique) are less frequently highlighted but appear in ~11% of food-focused reviews.

---

### 3. Price and Value Are Selectively Salient, Primarily in Negative Contexts

**Value/pricing is mentioned in only 77 of 250 reviews (30.8%)**, showing it is a secondary concern that emerges when triggered:

- **Positive reviews (n=125):** 51 mention pricing (40.8%)—predominantly "positive_value" (44 reviews)
- **Negative reviews (n=125):** 26 mention pricing (20.8%)—predominantly "overpriced" (23 reviews)

**Polarity ratio:** Among price-mentioning reviews, **overpriced judgments appear 5.4× more often in negative reviews (23/26) than positive reviews (5/51)**. Conversely, "good value" judgments appear **8.8× more often in positive reviews (44/51) than negative reviews (2/26)**.

**Insight:** Reviewers use price primarily as a dissatisfaction amplifier when service or food disappoints. Positive reviews highlight good value as a secondary satisfaction driver. Price concerns alone rarely trigger negative reviews; they compound other failures.

---

### 4. Aspect Co-Occurrence: Multi-Aspect vs. Single-Aspect Reviews

**Reviewers typically invoke multiple aspects in a single review:**
- **Service + Food mentioned**: 203 reviews (81.2%)—the backbone structure
- **Service + Price mentioned**: 77 reviews (30.8%)
- **Food + Price mentioned**: 68 reviews (27.2%)
- **All three aspects mentioned**: 68 reviews (27.2%)

**Insight:** The modal review structure combines service and food feedback. Price enters primarily when reviewers feel overcharged or conversely see genuine value. This reflects realistic customer priorities: service quality and product quality are non-negotiable; price is negotiated in context of the other two.

---

### 5. Polarity Patterns by Aspect

| Aspect | Positive Reviews | Negative Reviews | Ratio (Pos:Neg) |
|--------|------------------|------------------|-----------------|
| Service Positive | 111/125 | 2/125 | 55.5:1 |
| Service Negative | 1/125 | 110/125 | 1:110 |
| Food Positive | 92/125 | 1/125 | 92:1 |
| Food Negative | 1/125 | 83/125 | 1:83 |
| Price Positive Value | 44/125 | 2/125 | 22:1 |
| Price Overpriced | 5/125 | 23/125 | 1:4.6 |

**Insight:** Service and food sentiments are highly predictive of overall review polarity (positive or negative). Price judgments are less deterministic but still show strong association: overpriced judgments skew negative, good value skews positive. The small number of mixed-polarity aspect mentions (e.g., "good food, bad service") in single reviews reflects the strong sentiment coherence within reviews.

---

### 6. Experience Aspect Intensity and Elaboration

**Review length varies slightly by aspect focus**, suggesting reviewers invest more words when discussing pricing concerns:
- **Average review length (all)**: 478 characters
- **Reviews with service focus**: 478 characters (no variation)
- **Reviews with food focus**: 473 characters (baseline)
- **Reviews with price focus**: 503 characters (+5.4% longer)

**Insight:** Price-conscious reviewers write more elaborate explanations, likely because they feel obligated to justify their value judgment (e.g., "for $X, the quality should be better") or explain unexpected charges. Service and food are more straightforward to evaluate and require less justification.

---

## Synthesis: The Reviewer Experience Hierarchy

Yelp reviewers structure their feedback in a clear priority order:

1. **Service quality (99.2% mention rate)**: Universal lens. Staff friendliness, speed, and attentiveness determine whether reviewers feel valued and whether the experience is tolerable.

2. **Food/product quality (81.2% mention rate)**: Core outcome. Flavor and taste drive satisfaction when evaluated. Most reviews pair service and food assessment.

3. **Price/value (30.8% mention rate)**: Conditional amplifier. Reviewers invoke price when either:
   - The service or food is poor, and price seems unjustified ("for $X, I expected better")
   - The value is exceptional, enhancing goodwill despite minor flaws

**Decision-Ready Implication:** Businesses should prioritize staff conduct and food quality as the primary levers. Price transparency and value-matching (charging appropriately for quality) is a secondary lever that amplifies satisfaction when the first two are strong, or dissatisfaction when they are weak.
