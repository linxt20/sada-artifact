---
dataset: amazon_polarity_reviews
scenario: predictive_sentiment
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "label_pos"
query: "How do review facets differ by sentiment label?"
source_table: augment_table/amazon_polarity_reviews/predictive_sentiment/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:09:02.462348+00:00
wall_seconds: 41.14
---

# Review Facet Analysis by Sentiment Label — Amazon Polarity Reviews

**Dataset:** 250 reviews, balanced (125 negative `label_pos=0`, 125 positive `label_pos=1`)

---

## 1. Product Quality Signal

The sharpest discriminator between labels.

| Signal | Negative (%) | Positive (%) |
|---|---|---|
| criticized_quality | **78.7** | 0.0 |
| mixed_quality | 18.9 | 20.8 |
| praised_quality | 2.5 | **79.2** |

Near-perfect polarity. Mixed-quality reviews split almost evenly (~19–21%) across both labels, representing the weakest signal zone.

---

## 2. Recommendation Stance

Strongly aligned with label, with negligible overlap.

| Stance | Negative (%) | Positive (%) |
|---|---|---|
| explicitly_discourages | **36.8** | 0.0 |
| implicitly_discourages | **46.4** | 0.0 |
| explicitly_recommends | 0.8 | **48.0** |
| implicitly_recommends | 1.6 | **38.4** |
| neutral_or_conditional | 12.8 | 13.6 |

Negative reviews rely heavily on implicit discouragement (46%), while positive reviews split between explicit and implicit recommendations. Neutral/conditional stance (~13%) appears in both groups equally — a genuine exception.

---

## 3. Expectation Outcome

| Outcome | Negative (%) | Positive (%) |
|---|---|---|
| completely_failed_expectations | **45.6** | 0.0 |
| below_expectations | **47.2** | 4.8 |
| met_expectations | 4.0 | **62.4** |
| exceeded_expectations | 0.8 | **30.4** |

Negative reviews are dominated by unmet expectations (combined 92.8%). Notably, 4.8% of positive reviews still registered below-expectations outcomes — a weak but real exception suggesting grudging acceptances.

---

## 4. Emotion Types

**Negative emotion** is almost exclusively absent from positive reviews (95.2% `not_present`), while negative reviews distribute across disappointment (43.2%), disgust (21.6%), and anger/frustration (20.8%).

**Positive emotion** mirrors this: 96% of negative reviews have no positive emotion coded. Positive reviews are led by calm_satisfaction (44.0%) and delight_enthusiasm (34.4%), with love_affection at 12.0%.

---

## 5. Defect Type

| Defect | Negative (%) | Positive (%) |
|---|---|---|
| not_present | 7.2 | **93.6** |
| content_quality_flaw | **53.6** | 4.0 |
| hardware_failure | **20.8** | 0.8 |
| durability_breakage | 7.2 | 0.8 |

Content quality flaws and hardware failures account for ~74% of negative-label defect mentions. The 4.0% of positive reviews citing content flaws (and 7.2% of negative reviews with no defect coded) are minor exceptions worth noting.

---

## 6. Review Aspect Domain

Differences here are subtler and less diagnostic.

| Domain | Negative (%) | Positive (%) |
|---|---|---|
| physical_product | 39.2 | 27.2 |
| media_book | 32.0 | 33.6 |
| media_film | 16.0 | 12.0 |
| media_music | 8.8 | **23.2** |
| service_shipping | 0.0 | 1.6 |

Physical products are slightly over-represented in negative reviews. Media music is notably more frequent in positive reviews (23.2% vs. 8.8%), though sample sizes per domain are small, so this should be treated as weak evidence.

---

## 7. Emotional Intensity

Emotional intensity (scale 2–5) shows **minimal differentiation** by label:

| Intensity | Negative (%) | Positive (%) |
|---|---|---|
| 2 (low) | 19.2 | 27.2 |
| 3 (moderate) | 50.4 | 52.8 |
| 4 (high) | 28.8 | 17.6 |
| 5 (very high) | 1.6 | 2.4 |

Negative reviews skew slightly toward higher intensity (intensity 4: 28.8% vs. 17.6%), but the distributions overlap substantially. Intensity alone is a poor predictor of sentiment polarity in this dataset.

---

## Summary

| Facet | Discriminative Power |
|---|---|
| product_quality_signal | ⬛⬛⬛⬛⬛ Very high |
| recommendation_stance | ⬛⬛⬛⬛⬛ Very high |
| expectation_outcome | ⬛⬛⬛⬛⬜ High |
| negative/positive emotion type | ⬛⬛⬛⬛⬜ High |
| defect_type | ⬛⬛⬛⬛⬜ High |
| review_aspect_domain | ⬛⬛⬜⬜⬜ Low |
| emotional_intensity | ⬛⬜⬜⬜⬜ Minimal |

The strongest differentiators are **product quality signal**, **recommendation stance**, and **expectation outcome**. Emotion type and defect type are strong supporting signals. Domain and emotional intensity provide little incremental separation.
