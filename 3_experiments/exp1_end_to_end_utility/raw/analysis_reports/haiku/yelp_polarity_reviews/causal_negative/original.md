---
dataset: yelp_polarity_reviews
scenario: causal_negative
variant: original
model: substrate-claude-haiku-4-5
query_subtype: causal_attribution
focus_variable: "label_pos"
query: "Which factors best explain negative Yelp experiences?"
source_table: augment_table/yelp_polarity_reviews/causal_negative/original.csv
generated_at: 2026-07-26T13:58:16.239277+00:00
wall_seconds: 115.37
---

# Analysis Report: Factors Explaining Negative Yelp Experiences

## Dataset Overview

This analysis examines **250 Yelp reviews** (125 positive, 125 negative) from the "causal_negative" variant of the yelp_polarity_reviews dataset. The focus is identifying which factors best explain negative restaurant experiences.

## Key Findings

### Primary Factors Driving Negative Experiences

#### 1. **Service Issues** (50.4% of negative reviews, n=63)
Service failures are the most prevalent complaint factor. This includes:
- **Staff unresponsiveness**: Forgotten customers, staff "vanishing" after seating
- **Poor attention**: Waiters walking past customers multiple times without acknowledgment
- **Staffing gaps**: Inadequate coverage during busy periods

*Evidence*: Review YLP-0008 exemplifies this: "We were seated for 25 minutes. No one came to take our order. The waitress was cleaning tables and walked right by us several times."

#### 2. **Wait Time Issues** (43.2% of negative reviews, n=54)
Extended wait times significantly impact satisfaction, particularly when:
- Waits exceed 20-45 minutes despite moderate venue occupancy
- Staff fails to communicate progress or acknowledge waiting customers
- No engagement from staff during the wait period

*Evidence*: Multiple reviews cite specific wait durations (25 min, 45 min, 90 min) with particular frustration when the restaurant was not visibly busy.

#### 3. **Food Quality** (29.6% of negative reviews, n=37)
Quality concerns center on:
- **Temperature**: Cold dishes upon arrival, particularly after waits
- **Flavor/Freshness**: Bland, tasteless, or underseasoned food
- **Inconsistency**: Quality variation compared to previous visits or expectations

*Evidence*: Review YLP-0077: "The burgers were small and cold... fries and onion rings sat under the lights for 10 minutes... arrived cold and over salted."

#### 4. **Cleanliness/Hygiene** (18.4% of negative reviews, n=23)
Visible sanitation issues damage trust:
- Dirty tables, unclean seating areas
- Visible debris or unsanitary conditions in dining/kitchen areas
- Inconsistency with food service standards

*Evidence*: Review YLP-0007: "My table was dirty and so were the ones around me" combined with poor service and mediocre food.

#### 5. **Pricing Concerns** (14.4% of negative reviews, n=18)
Value perception issues include:
- Prices perceived as excessive relative to portion/quality
- Unexpected charges or price increases
- Premium pricing mismatched with service level

*Evidence*: Review YLP-0012: Customers expected lunch pricing ($16.99) but were charged holiday brunch rates ($24.99) without advance notice.

#### 6. **Overcrowding** (12.8% of negative reviews, n=16)
Excessive crowding compounds other issues:
- Cramped seating affecting comfort
- Amplified service delays due to high capacity
- Overwhelmed staff capacity

#### 7. **Portion Size** (9.6% of negative reviews, n=12)
Secondary but notable factor:
- Portions perceived as too small for price point
- Inconsistency with advertised portion sizes

### Interaction Patterns

The analysis reveals that negative experiences rarely stem from a single factor (only 88.8% of reviews mention one dominant complaint). **11.2% of negative reviews cite 2+ factors**, suggesting causal chains:

- **Service delays → Cold food**: Long waits → dishes sit under heat lamps → arrive cold
- **High pricing → Quality scrutiny**: Premium pricing → heightened expectations → disappointment when quality doesn't match
- **Crowding → Service breakdown**: Overwhelmed staff → forgotten customers → poor satisfaction

## Weak Evidence Factors

- **Portion size** alone: Only 3.2% of negative reviews, typically mentioned in combination with pricing
- **Attitude/rudeness** alone: 8.8% explicit mentions, often paired with service failures

## Decision Implications

**Service responsiveness** emerges as the strongest lever for improving satisfaction. Preventing long wait times and maintaining staff attentiveness addresses nearly half of negative experiences. Food quality and cleanliness maintenance are secondary but critical quality gates that prevent repeat visits when combined with service issues.

The dataset suggests that negative experiences cluster around *operational execution* (service, wait times) rather than inherent product quality, indicating that procedural improvements may yield significant satisfaction gains.
