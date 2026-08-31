---
dataset: imdb_movie_reviews
scenario: causal_audience
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "audience_dissatisfaction"
query: "Why are IMDb audiences dissatisfied?"
source_table: augment_table/imdb_movie_reviews/causal_audience/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:23:06.721672+00:00
wall_seconds: 78.99
---

# Analysis: Why Are IMDb Audiences Dissatisfied?

## Overview

This analysis examines 250 balanced IMDB movie reviews (125 negative, 125 positive) to identify the primary drivers of audience dissatisfaction. The dataset includes both original review text and TAPP-generated semantic facet annotations, enabling quantified assessment of dissatisfaction causes.

## Key Finding: Originality Failure Dominates

**IMDb audiences are dissatisfied primarily due to lack of originality, manifesting as formulaic, derivative, or clichéd storytelling.** This single factor is the strongest differentiator between negative and positive reviews.

### Originality/Novelty: The Central Dissatisfaction Driver

**68% of negative reviews (85/125)** explicitly feature deficiencies in originality_or_novelty, compared to only **13.6% of positive reviews (17/125)**—a difference of 54.4 percentage points. This is the largest gap across all TAPP-generated dimensions.

Within negative reviews exhibiting this issue:
- **Formulaic plots dominate:** 73 reviews (58.4% of all negative reviews) cite formulaic storytelling as a core complaint
- **Derivative work:** 10 reviews (8.0%) specifically note unoriginal or copied material
- **Clichéd elements:** 2 reviews (1.6%) label stories as worn-out

**Evidence from text:** The word "bad" appears in 28.0% of negative reviews, and reviewers commonly describe plots as "obvious," "predictable," and "by-the-numbers," indicating audiences recognize and resent familiar narrative templates.

## Secondary Drivers: Genre Mismatch and Structural Issues

### Genre-Audience Misalignment (60% of negative reviews)

**60% of negative reviews (75/125)** involve genre_audience_mismatch problems, versus only 6.4% of positive reviews—a 53.6 pp difference. The most prevalent subtype:

- **Marketed vs. Delivered Genre (44.8% of negative reviews, 56 cases):** Audiences feel deceived when promotional material promises one genre but the film delivers another (e.g., a film marketed as action but delivered as melodrama). This violation of expectations directly undermines satisfaction.
- **Inappropriate for Target Audience (8.0%, 10 reviews):** Content mismatch with intended audience demographics
- **Derivative Genre Execution (7.2%, 9 reviews):** Unoriginal treatment within a genre

### Narrative Structure Deficiencies (40% of negative reviews)

**40% of negative reviews (50/125)** feature narrative_structure_issue problems, compared to 4.8% of positive reviews—a 35.2 pp gap. This manifests as:

- **Weak or Thin Structure (32.0%, 40 reviews):** Insufficient plot development, lack of coherence, or insufficient story substance. Reviewers complain of underdeveloped arcs and meandering narratives.
- **Incoherent or Confusing Structure (8.0%, 10 reviews):** Confusing plot progression or disjointed storytelling that alienates viewers.

Sample complaint: "This movie took a concept and made it watchable" (IMDB-0037)—indicating the story itself was weak despite an interesting premise.

## Tertiary Drivers: Tone/Consistency and Cliché Reliance

### Tonal Inconsistency (32.8% of negative reviews)

**tone_or_consistency_issue** appears in 32.8% of negative reviews versus 8.8% of positive reviews (24.0 pp difference). Audiences resent:

- **Wrong genre fit within film:** 15.2% of negative reviews cite genre misalignment at the tonal level (inconsistent_tone)
- **Mismatched attempts at appeal:** 5.6% feature misaligned attempts to attract multiple audiences
- **Genre-level mismatch:** 15.2% cite wrong_genre_fit (narrative tone doesn't match genre promise)

### Reliance on Clichés (44.8% of negative reviews)

**44.8% of negative reviews (56/125)** cite reliance_on_clich_s problems versus 17.6% of positive reviews—a 27.2 pp difference. Common forms:

- **Hackneyed Plot Devices (26.4%, 33 reviews):** Overused narrative tropes (chosen ones, betrayals, convenient coincidences)
- **Stock Characters (12.0%, 15 reviews):** One-dimensional archetypes without depth
- **Overused Themes (6.4%, 8 reviews):** Tired thematic material explored without novelty

## Interconnected Dissatisfaction Patterns

Dissatisfaction rarely stems from a single isolated issue. Analysis of feature co-occurrence reveals:

- **48.8% of negative reviews** exhibit BOTH originality_or_novelty AND genre_audience_mismatch failures
- **39.2%** cite BOTH originality failures AND cliché reliance
- **30.4%** simultaneously exhibit originality, genre, and cliché problems
- **Only 19.2%** of negative reviews show just one TAPP-identified issue; most exhibit multiple compounding defects

This suggests audiences evaluate films holistically: a formulaic plot combined with genre misalignment creates compounded dissatisfaction.

## Summary of Dissatisfaction Hierarchy

| Issue | Negative Reviews | Positive Reviews | Difference | Rank |
|-------|------------------|------------------|-----------|------|
| Originality/Novelty Deficiency | 68.0% | 13.6% | 54.4 pp | **1st** |
| Genre-Audience Mismatch | 60.0% | 6.4% | 53.6 pp | **2nd** |
| Narrative Structure Weakness | 40.0% | 4.8% | 35.2 pp | **3rd** |
| Cliché Reliance | 44.8% | 17.6% | 27.2 pp | **4th** |
| Tonal Inconsistency | 32.8% | 8.8% | 24.0 pp | **5th** |

## Method Note

**TAPP-Generated Columns Used:**
This analysis employs the following TAPP-augmented columns from the dataset:
- `narrative_structure_issue` (weak_or_thin, incoherent_or_confusing)
- `originality_or_novelty` (formulaic, derivative, clichéd)
- `tone_or_consistency_issue` (wrong_genre_fit, inconsistent_tone, mismatched_attempted_appeal)
- `genre_audience_mismatch` (marketed_vs_delivered_genre, inappropriate_for_audience, derivative_genre)
- `reliance_on_clich_s` (hackneyed_plot_device, stock_characters, overused_theme)

All quantitative claims cite exact counts, percentages, and sample sizes. TAPP-generated facets serve as explanatory supplements to the original review texts, clarifying semantic relationships that text analysis alone would obscure.

## Conclusion

IMDb audiences express dissatisfaction through a consistent pattern: they demand **originality within expected genres**, delivered with **coherent narrative structure** and **fresh character development**. When films default to formulaic plots, misalign marketing with content, or rely on hackneyed devices, audiences respond negatively—particularly when multiple deficiencies compound. The dominance of originality/novelty as a dissatisfaction driver (68% of negative reviews) underscores that audiences prioritize storytelling innovation as the foundation of satisfaction, above all other film attributes.
