---
dataset: imdb_movie_reviews
scenario: eda_sentiment
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "label_pos"
query: "How do review themes differ between positive and negative IMDb sentiment?"
source_table: augment_table/imdb_movie_reviews/eda_sentiment/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:23:10.636955+00:00
wall_seconds: 56.92
---

# Review Theme Differences Between Positive and Negative IMDb Sentiment

## Overview

The augmented dataset contains **250 IMDb reviews** with balanced sentiment labels: 125 positive (`label_pos=1`) and 125 negative (`label_pos=0`). The analysis combines original structured columns with TAPP-generated semantic facets to characterize how themes differ between sentiment groups.

**Method note — TAPP-generated columns used:** `overall_craft_verdict`, `script_writing_quality`, `plot_originality`, `acting_quality`, `reviewer_emotional_response`, `rewatch_intent`, `comparative_benchmark`, `explicit_recommendation`, `genre_expectation_met`.

---

## 1. Craft Quality: The Dominant Dividing Theme

`overall_craft_verdict` shows near-perfect separation between sentiment groups:

| Verdict | Negative (n=125) | Positive (n=125) |
|---|---|---|
| poor | 66 (52.8%) | 0 |
| unwatchable | 18 (14.4%) | 0 |
| mixed | 38 (30.4%) | 28 (22.4%) |
| good | 3 (2.4%) | 84 (67.2%) |
| masterpiece | 0 | 13 (10.4%) |

Negative reviews concentrate overwhelmingly on craft failure (67.2% "poor/unwatchable"); positive reviews celebrate quality (77.6% "good/masterpiece"). The "mixed" tier straddles both groups and represents the gray area (30.4% of negatives vs. 22.4% of positives).

---

## 2. Script Writing and Plot Originality

`script_writing_quality` is a strong discriminating dimension:

| Script Quality | Negative | Positive |
|---|---|---|
| poor_incoherent | 82 (65.6%) | 1 (0.8%) |
| cliched_formulaic | 31 (24.8%) | 3 (2.4%) |
| adequate | 11 (8.8%) | 74 (59.2%) |
| sharp_clever | 0 | 17 (13.6%) |
| not_present (not discussed) | 1 | 30 (24.0%) |

Two-thirds of negative reviews explicitly call out poor or incoherent writing. Positive reviewers either praise the script as adequate/clever (72.8%) or simply don't dwell on it (24%), suggesting positive reviews move the conversation toward other themes.

`plot_originality` shows a similar pattern among reviews that address it: 47 negative reviews flag derivative/incoherent plots vs. 3 positive; 27 positive reviews highlight originality vs. 2 negative. However, 53 negative and 57 positive reviews don't mention plot — this facet is less universal.

---

## 3. Acting Quality

`acting_quality` is discussed in roughly half of reviews per group (58 negative, 62 positive mention it). Among those:

| Acting | Negative (n=58) | Positive (n=62) |
|---|---|---|
| poor_wooden | 46 (79.3%) | 1 (1.6%) |
| uneven_mixed | 10 (17.2%) | 4 (6.5%) |
| competent_solid | 2 (3.4%) | 24 (38.7%) |
| excellent_standout | 0 | 33 (53.2%) |

When acting is mentioned, negative reviews focus almost exclusively on wooden performances; positive reviews celebrate standout or solid acting. Negative reviews are more likely to cite acting as a specific failure theme.

---

## 4. Reviewer Emotional Response

`reviewer_emotional_response` captures the affective texture of the review narrative:

| Emotional Response | Negative (%) | Positive (%) |
|---|---|---|
| strong_negative_disgust_anger | 44.8 | 0.0 |
| mild_negative_boredom | 44.0 | 2.4 |
| neutral_detached | 6.4 | 7.2 |
| mild_positive_entertainment | 4.8 | 60.0 |
| strong_positive_awe_joy | 0.0 | 30.4 |

Negative reviews split almost evenly between active disgust/anger (44.8%) and passive boredom (44.0%) — two distinct negative themes. Positive reviews are dominated by entertainment satisfaction (60.0%), with 30.4% expressing awe or joy. The near-zero overlap confirms emotional vocabulary is a highly diagnostic feature.

---

## 5. Rewatch Intent and Explicit Recommendation

Both facets are highly aligned with sentiment — acting as proxy confirmation rather than adding new explanatory variance:

| Rewatch Intent | Negative | Positive |
|---|---|---|
| would_not_rewatch | 80 (64.0%) | 1 (0.8%) |
| neutral | 37 (29.6%) | 19 (15.2%) |
| implicit_positive_engagement | 2 (1.6%) | 95 (76.0%) |
| explicit_rewatch_desire | 0 | 10 (8.0%) |

| Recommendation | Negative | Positive |
|---|---|---|
| strong_advise_against | 46 (36.8%) | 1 (0.8%) |
| mild_advise_against | 50 (40.0%) | 2 (1.6%) |
| mild_recommend | 1 (0.8%) | 53 (42.4%) |
| strong_recommend | 1 (0.8%) | 46 (36.8%) |

Negative reviewers almost universally discourage watching (76.8% combined advise-against); positive reviewers recommend broadly (79.2% combined recommend). These facets are largely redundant with the outcome label but confirm internal consistency.

---

## 6. Genre Expectation and Comparative Benchmarking

`genre_expectation_met` is strikingly clean:

| Expectation | Negative | Positive |
|---|---|---|
| failed_expectations | 88 (70.4%) | 1 (0.8%) |
| partially_met_expectations | 31 (24.8%) | 19 (15.2%) |
| met_expectations | 2 (1.6%) | 47 (37.6%) |
| exceeded_expectations | 0 | 57 (45.6%) |

Failing genre expectations is the dominant negative theme (70.4%). Positive reviewers split between "met" and "exceeded" — suggesting positive sentiment hinges on delivering on genre promise or surpassing it.

`comparative_benchmark` is less frequent (only ~24% of reviews use comparisons) but directional: negative reviews reference unfavorable peer or classic comparisons (31/125 = 24.8%), while positive reviews reference favorable comparisons (23/125 = 18.4%). The facet adds semantic color but is not a primary driver.

---

## 7. Summary: Key Thematic Contrasts

| Theme Dimension | Dominant in Negative Reviews | Dominant in Positive Reviews |
|---|---|---|
| **Craft verdict** (`overall_craft_verdict`) | poor / unwatchable (67.2%) | good / masterpiece (77.6%) |
| **Writing** (`script_writing_quality`) | poor_incoherent / cliché (90.4%) | adequate / sharp_clever (72.8%) |
| **Emotion** (`reviewer_emotional_response`) | disgust-anger + boredom (88.8%) | entertainment + awe (90.4%) |
| **Expectation** (`genre_expectation_met`) | failed expectations (70.4%) | met or exceeded (83.2%) |
| **Acting** (`acting_quality`, when mentioned) | wooden / uneven (96.6%) | solid / excellent (91.9%) |
| **Recommendation** (`explicit_recommendation`) | advise against (76.8%) | recommend (79.2%) |

**Core finding:** Negative reviews are thematically organized around failure across multiple craft axes simultaneously — bad writing, poor acting, unmet genre expectations, and strong negative affect (disgust or boredom). Positive reviews tend to celebrate overall quality and emotional satisfaction, with notably fewer explicit discussions of craft details (e.g., 24% of positives don't comment on script at all), suggesting appreciation is sometimes holistic rather than analytical.
