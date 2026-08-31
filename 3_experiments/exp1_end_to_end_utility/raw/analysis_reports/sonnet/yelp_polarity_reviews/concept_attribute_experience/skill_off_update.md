---
dataset: yelp_polarity_reviews
scenario: concept_attribute_experience
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "satisfaction_and_complaint_facets"
query: "What satisfaction and complaint themes appear in Yelp reviews?"
source_table: augment_table/yelp_polarity_reviews/concept_attribute_experience/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:25:49.573559+00:00
wall_seconds: 38.11
---

# Satisfaction and Complaint Themes in Yelp Reviews

## Dataset Overview

- **Total reviews:** 250 (125 positive `label_pos=1`, 125 negative `label_pos=0`)
- **Key augmented columns:** `satisfaction_themes`, `complaint_themes`, `sentiment_intensity`, `theme_count`
- Sentiment intensity spans five levels: *very_positive → very_negative*

---

## Satisfaction Themes (Positive Drivers)

| Theme | Count (all) | Primarily in Positive Reviews |
|---|---|---|
| `none` (no explicit theme) | 150 | 58 of 125 positive |
| `food_quality` | 38 | 26 positive, 12 negative |
| `ambiance_atmosphere` | 18 | 8 positive, 10 negative |
| `service_quality` | 10 | 8 positive |
| `speed_efficiency` | 8 | 6 positive |
| `value_for_money` | 7 | 5 positive |

**Key observations:**
- **Food quality** is the dominant explicit satisfaction driver, appearing in ~21% of positive reviews. It also appears in some negative reviews, suggesting reviewers sometimes praise food while complaining about other aspects.
- **Ambiance/atmosphere** is notably split — it appears almost equally across positive and negative reviews (8 vs. 10), indicating it is raised both as praise and as context for disappointment.
- **Service quality, speed, and value** are secondary but consistent satisfaction signals, mostly concentrated in positive reviews.
- A large share of positive reviews (58/125, ~46%) carry `none` for satisfaction themes, meaning praise was often general/diffuse rather than theme-specific — a possible annotation gap or genuinely mixed writing style.

---

## Complaint Themes (Negative Drivers)

| Theme | Count (all) | Primarily in Negative Reviews |
|---|---|---|
| `none` | 195 | 82 of 125 negative |
| `poor_service` | 16 | 14 negative |
| `food_quality_issues` | 12 | 8 negative |
| `cleanliness_issues` | 11 | 8 negative |
| `overpriced` | 11 | 8 negative |
| `food_quality_issues\|overpriced` (combo) | 2 | 2 negative |

**Key observations:**
- **Poor service** is the leading specific complaint (14/125 negative reviews, ~11%), consistent with service failures being the most salient and memorable negative experience.
- **Cleanliness, food quality issues, and price** appear with roughly equal frequency (~8 each in negative reviews), forming a secondary cluster of complaint themes.
- Complaint co-occurrences are rare (only 5 multi-theme entries), suggesting most negative reviews tend to focus on a single pain point.
- **82/125 negative reviews (~66%) show `none` for complaint themes** — indicating that many negative reviews express general dissatisfaction without mapping to a specific tagged theme. This is a limitation: either the complaints were subtle/indirect, or the augmentation scheme missed them.

---

## Sentiment Intensity Distribution

| Intensity | Count |
|---|---|
| positive | 72 |
| mildly_negative | 63 |
| negative | 50 |
| mildly_positive | 45 |
| very_negative | 12 |
| very_positive | 8 |

- Moderate sentiments dominate; extreme sentiments (`very_positive`, `very_negative`) are rare (combined ~8%).
- The asymmetry between `very_negative` (12) and `very_positive` (8) suggests strongly negative experiences are slightly more likely to generate emphatic language.

---

## Summary

**Top satisfaction themes:** food quality → ambiance → service quality → speed → value  
**Top complaint themes:** poor service → food quality issues ≈ cleanliness ≈ overpriced

The dataset reveals a **food-centric satisfaction narrative** (quality of food is the clearest positive signal) contrasted with a **service-centric complaint narrative** (poor service is the single most-tagged negative theme). Price sensitivity and cleanliness are secondary but meaningful complaint dimensions. A notable caveat is the high `none` rate for both columns (60% satisfaction, 78% complaint), indicating many reviews were not mapped to a specific theme — results should be interpreted as indicative rather than exhaustive.
