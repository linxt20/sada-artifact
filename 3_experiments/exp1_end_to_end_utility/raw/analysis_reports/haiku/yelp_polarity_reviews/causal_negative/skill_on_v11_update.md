---
dataset: yelp_polarity_reviews
scenario: causal_negative
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "label_pos"
query: "Which factors best explain negative Yelp experiences?"
source_table: augment_table/yelp_polarity_reviews/causal_negative/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:23:24.483243+00:00
wall_seconds: 38.02
---

# Analysis Report: Factors Explaining Negative Yelp Experiences

## Executive Summary

This analysis examines 125 negative Yelp reviews (ratings of 1–2 stars) from the Yelp Polarity Reviews dataset augmented with causal annotations. The data reveals three primary factors that explain negative dining and service experiences: **expectations misalignment (99%), staff interpersonal issues (58%), and service delivery failures (34%)**.

## Primary Findings

### 1. **Expectations vs. Reality Gaps: The Dominant Factor**

Expectations misalignment appears in **99.2% of negative reviews** (124 of 125 cases), making it nearly universal in negative experiences. This factor encompasses:

- **Marketed Well, Delivered Poorly** (66 instances, 52.8% of negatives): Venues with positive marketing or reputation that fail to meet those standards—e.g., highly-rated restaurants with mediocre food, expensive venues offering poor quality, or establishments that have "fallen off."
  - *Example*: "How this restaurant received 4 stars on yelp is BEYOND me" (poor execution of marketed quality).
  
- **Overhyped, Mediocre** (40 instances, 32%): Establishments that receive unwarranted buzz or inflated reviews relative to actual service/product quality.
  - *Example*: "For all the hype it's not that spectacular" (disappointing reality versus expectations).

- **Not as Described** (16 instances, 12.8%): Direct misrepresentation of offerings, pricing, or terms.
  - *Example*: Surprise surcharges, menu items not available, or services not delivered as promised.

### 2. **Staff Interpersonal Issues: The Secondary Driver**

Staff behavior problems appear in **57.6% of negative reviews** (72 of 125 cases), often compounding other failures:

- **Dismissive or Indifferent Behavior** (40 instances, 32% of negatives): Staff who ignore customers, show lack of concern, or fail to acknowledge problems.
  - *Example*: "Waiter showed up and told us to have a good night" without addressing 25-minute seating and no service.
  
- **Rude or Hostile Behavior** (26 instances, 20.8%): Explicitly hostile, condescending, or disrespectful staff conduct.
  - *Example*: "Manager told me if I wanted to relax and enjoy my meal than I was in the wrong place."
  
- **No Apology** (6 instances, 4.8%): Failures to acknowledge mistakes, contributing to customer frustration.
  - *Example*: Waiter removed a glass without apology and claimed it would be replaced, showing lack of service recovery.

### 3. **Service Quality Failures: The Operational Gap**

Service delivery problems appear in **34.4% of negative reviews** (43 of 125 cases). These are often paired with staff issues:

- **Slow or Inattentive Service** (30 instances, 24% of negatives): Long waits, delayed orders, lack of responsiveness to customer needs.
  - *Example*: "Waiting 20 minutes for a seat next to kitchen noise, then asked for another table and told the restaurant isn't for relaxation."
  
- **Forgotten or Ignored Customers** (7 instances, 5.6%): Customers overlooked entirely or deprioritized.
  - *Example*: "Seated in area for private party, then forgotten when the party arrived. Moved, then forgotten again."
  
- **Disorganization** (6 instances, 4.8%): Operational chaos affecting customer experience.
  - *Example*: Line control issues, uncoordinated staff, unpreparedness for demand.

## Co-Occurrence Patterns

**Strong correlation exists between factors:**
- 37 reviews cite **both** service failures AND staff behavior issues (29.6%)
- 35 reviews cite **only** staff issues (28%)
- 6 reviews cite **only** service failures (4.8%)
- 47 reviews cite **neither** specific failures but still report expectations misalignment (37.6%)

This suggests that expectations gaps can drive negative sentiment independently, but when paired with operational or interpersonal failures, dissatisfaction is compounded.

## Key Insights

1. **Expectations Misalignment Is Universal**: Nearly every negative review involves some gap between perceived promise and actual delivery. This is the foundational complaint—even good service may not overcome overhyped reputations.

2. **Staff Behavior Exceeds Operational Failures in Frequency**: More negative reviews cite staff dismissiveness or rudeness (58%) than cite slow service (34%), indicating that *how* service is delivered may matter more than speed alone.

3. **Weak Evidence for Single-Factor Failures**: Only 6 negative reviews cite *only* service slowness without any staff behavior or expectations gap. This suggests operational issues rarely occur in isolation; they are typically accompanied by other failing factors or unmet expectations.

4. **Expectations Are Set by Marketing/Reputation**: The dominance of "marketed well, delivered poorly" and "overhyped" categories indicates that negative experiences are often relative to external promises or social proof, not absolute quality benchmarks.

## Limitations

- The dataset is limited to restaurants, bars, hotels, and service establishments; findings may not generalize to other industries.
- Annotations rely on human labeling; some nuanced factors may be missed or misclassified.
- Positive reviews were not analyzed in detail; understanding what *prevents* these factors from generating negative sentiment would strengthen recommendations.

## Conclusion

**Negative Yelp experiences are primarily driven by expectations misalignment (99% of cases), compounded by staff interpersonal failures (58%) and operational delays (34%).** Organizations seeking to reduce negative reviews should prioritize: (1) aligning marketing claims with actual delivery quality, (2) training staff in customer-facing professionalism and service recovery, and (3) implementing reliable service speed and attention protocols. Staff behavior is particularly influential—addressing dismissiveness and rudeness appears more impactful than addressing speed alone.
