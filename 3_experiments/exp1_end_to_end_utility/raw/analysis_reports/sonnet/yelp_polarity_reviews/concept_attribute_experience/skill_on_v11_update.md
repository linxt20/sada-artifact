---
dataset: yelp_polarity_reviews
scenario: concept_attribute_experience
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "satisfaction_and_complaint_facets"
query: "What satisfaction and complaint themes appear in Yelp reviews?"
source_table: augment_table/yelp_polarity_reviews/concept_attribute_experience/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:23:51.317622+00:00
wall_seconds: 48.59
---

# Satisfaction & Complaint Themes in Yelp Reviews

## Dataset Overview
- **250 reviews**, balanced 50/50 between positive (`label_pos=1`) and negative (`label_pos=0`).
- Six attribute columns capture experience facets: `service_quality`, `staff_attitude`, `food_taste_rating`, `value_perception`, `ambiance_atmosphere`, and `standout_item_mention`.

---

## Satisfaction Themes (Positive Reviews)

### 1. Service Quality — Strongest Satisfaction Driver
`service_quality` is the most discriminating column. Among positive reviews:
- **excellent**: 53 of 54 total → nearly exclusively positive
- **good**: 47 of 50 → strongly positive
- **mixed**: only 11 of 45 → associated with dissatisfaction

### 2. Staff Attitude — Clear Praise Signal
- **friendly_welcoming**: 51 of 62 (82%) are positive reviews
- Staff friendliness is a top satisfaction theme, appearing in ~25% of all positive reviews

### 3. Food Quality — Key for Food-Centric Reviews
- **excellent** food rating: 46 of 47 are positive
- **good** food: 29 of 37 are positive
- Food quality emerges as a major satisfaction theme, though `not_present` in 106 reviews (many non-restaurant businesses)

### 4. Value & Ambiance as Secondary Boosters
- **great_value**: 14 of 14 positive (100%); **fair_value**: 9 of 9 positive — pricing satisfaction perfectly predicts positive sentiment when mentioned
- **pleasant** ambiance: 29 of 36 (81%) positive

### 5. Standout Item Mentions
- 98 reviews (39%) mention a standout item; these skew positive and signal enthusiastic satisfaction

---

## Complaint Themes (Negative Reviews)

### 1. Poor Service Quality — Top Complaint
- **poor** service: 80 of 81 (99%) are negative — the single strongest complaint signal in the dataset
- **mixed** service: 34 of 45 (76%) are negative

### 2. Rude or Indifferent Staff
- **rude_dismissive** attitude: 42 of 43 (98%) negative
- **indifferent** staff: 21 of 21 (100%) negative
- Together these account for ~63 negative reviews; staff behavior is the second most reliable complaint predictor

### 3. Poor Food Quality
- **poor** food rating: 28 of 28 (100%) negative
- **mediocre** food: 28 of 32 (88%) negative

### 4. Pricing Complaints
- **overpriced**: 20 of 24 (83%) negative; **extreme_ripoff**: 2 of 3 negative
- Value complaints appear in ~18% of negative reviews

### 5. Negative Ambiance
- **unpleasant** atmosphere: 9 of 11 (82%) negative; **noisy_or_crowded**: 7 of 10 negative

---

## Co-occurrence Patterns & Exceptions

| Pattern | Evidence |
|---|---|
| Poor service + rude staff = severe complaint | ~40 reviews match both; virtually all negative |
| Mixed service can appear in positive reviews | 11 of 45 mixed-service reviews are positive (nuanced satisfaction) |
| `not_present` across most attribute columns | Value (200/250), ambiance (172/250), food (106/250) are frequently absent — many reviews focus on a single aspect |
| `extreme_ripoff` appears in 1 positive review | Weak exception; likely sarcasm or mixed context |

---

## Summary

The dominant **satisfaction themes** are: excellent/good service quality, friendly staff, strong food quality, and good value. The dominant **complaint themes** are: poor service, rude/indifferent staff, poor food quality, and overpricing. Service quality and staff attitude are the most reliable binary discriminators across both poles. Ambiance and value play supporting roles. Because attribute columns are frequently `not_present`, conclusions about those dimensions apply only to the subset of reviews where they were mentioned.
