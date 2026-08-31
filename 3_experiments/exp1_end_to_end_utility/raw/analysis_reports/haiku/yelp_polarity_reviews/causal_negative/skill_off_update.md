---
dataset: yelp_polarity_reviews
scenario: causal_negative
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "label_pos"
query: "Which factors best explain negative Yelp experiences?"
source_table: augment_table/yelp_polarity_reviews/causal_negative/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:25:11.801220+00:00
wall_seconds: 34.02
---

# Analysis Report: Factors Explaining Negative Yelp Experiences

## Executive Summary

This analysis examines 125 negative Yelp reviews (label_pos=0) to identify which factors best explain poor customer experiences. The data reveals a clear hierarchy of drivers: **service quality and food quality dominate as the primary causal factors**, with cleanliness, price, and ambiance playing secondary roles.

## Primary Factors Explaining Negative Experiences

### 1. **Service Quality** (56% of negative reviews)
- **Prevalence**: Mentioned in 70 of 125 negative reviews
- **Strength of evidence**: Highest frequency; appears as sole complaint in 25 reviews
- **Key patterns**:
  - Long wait times for seating, ordering, and food delivery (explicitly measured: "waited 20 minutes," "waited 45 minutes")
  - Staff inattentiveness, forgetfulness, and rudeness ("forgot we were there," "waiter didn't show up," "told me to F off")
  - Slow service despite low crowding, suggesting understaffing or poor training
  - Inconsistent service recovery attempts; when staff acknowledged problems, customers were sometimes offered compensation but many received no apology

### 2. **Food Quality** (47.2% of negative reviews)
- **Prevalence**: Mentioned in 59 of 125 negative reviews
- **Strength of evidence**: Second-highest frequency; sole complaint in 15 reviews
- **Key patterns**:
  - Poor taste and flavor ("bland," "tasteless," "mediocre")
  - Temperature issues (cold, undercooked, overcooked, or "lukewarm at best")
  - Portion problems (too small or inconsistent with menu photos)
  - Staleness and freshness concerns ("stale bread," "frozen-looking")
  - Specific complaints about inconsistency within menu (e.g., some dishes good, others poor)

### 3. **Cleanliness** (14.4% of negative reviews)
- **Prevalence**: Mentioned in 18 of 125 negative reviews
- **Strength of evidence**: Moderate; rarely sole complaint (only 2 standalone cases)
- **Key patterns**:
  - Dirty tables, chairs, and utensils ("dirt," "gum under chair," "roach")
  - Hygiene issues with specific items ("dirty fork," "rubber band in chips and salsa")
  - Environmental cleanliness ("filthy stained chairs," "smell like urinal cakes")
  - Often co-occurs with service failures (e.g., no attempt to clean)

### 4. **Price/Value** (17.6% of negative reviews)
- **Prevalence**: Mentioned in 22 of 125 negative reviews
- **Strength of evidence**: Moderate; sole complaint in 5 reviews
- **Key patterns**:
  - Overpricing relative to quality and portion ("$23 for inferior pasta," "way overpriced")
  - Hidden or unexpected charges ("bait-and-switch" on advertised pricing)
  - Poor value perception (quality does not justify cost)
  - Often paired with food quality complaints rather than standing alone

### 5. **Ambiance/Atmosphere** (12.8% of negative reviews)
- **Prevalence**: Mentioned in 16 of 125 negative reviews
- **Strength of evidence**: Weakest; rarely sole driver (3 standalone cases)
- **Key patterns**:
  - Noise levels ("so loud," "obnoxiously loud")
  - Cramped or uncomfortable seating arrangements ("crowded," "right next to kitchen")
  - Poor decor or outdated facilities
  - Most often mentioned in conjunction with other failures

## Complaint Multiplicity & Severity

- **Single-factor complaints**: 50 reviews (40%) cite only one problem area
- **Multi-factor complaints**: 75 reviews (60%) mention 2+ issues
- **Emotional intensity**: Most negative reviews (91 of 125, 72.8%) show minimal emotional language despite low ratings, suggesting methodical rather than rage-driven complaints
- **Strongest emotional expressions**: Found in reviews mentioning service rudeness, discrimination, or health/safety concerns

## Causal Mechanisms (Implied Explanations)

Reviewers frequently name underlying operational causes:
- **Understaffing**: "weren't enough staff," "one bartender handling everything"
- **Poor training**: Mispronouncing menu items, not knowing drink inventory, inconsistent execution
- **Management failure**: Lack of service recovery, staff not held accountable
- **Kitchen/prep issues**: Timing problems, poor quality control, ingredient issues

## Minor Exceptions & Qualifications

1. **Venue type variation**: Hotels and nightclubs show higher tolerance for service lapses; restaurants show zero tolerance
2. **Expectation disconfirmation**: Reviews citing "heard great things" or "4+ star rating" show stronger negativity, suggesting disappointment amplifies judgment
3. **Recovery attempts**: A small number of reviews mention compensation (free drinks, cookies) that partially mitigated dissatisfaction, though many note the absence of apologies

## Decision-Ready Insights

**To reduce negative experiences, prioritize in this order:**
1. Service quality training and staffing levels (56% of complaints)
2. Food quality consistency and temperature management (47% of complaints)
3. Cleanliness protocols, especially high-touch surfaces (14% of complaints)
4. Pricing transparency and perceived value (18% of complaints)

**Weakest opportunity**: Ambiance changes alone will not improve negative ratings; it is a secondary factor in isolated venues.

**Strongest evidence**: Service and food quality combined explain negative experiences in ~75% of cases. Addressing these two dimensions would resolve the majority of complaints.
