---
dataset: imdb_movie_reviews
scenario: causal_audience
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "audience_dissatisfaction"
query: "Why are IMDb audiences dissatisfied?"
source_table: augment_table/imdb_movie_reviews/causal_audience/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:22:32.183069+00:00
wall_seconds: 47.73
---

# Why Are IMDb Audiences Dissatisfied?

## Dataset Overview

The dataset contains **250 IMDb reviews** (125 negative, 125 positive) annotated across three causal dimensions: `writing_quality_issue`, `plot_structural_issue`, and `genre_execution_quality`.

---

## Key Finding: Issue Flags Are Overwhelmingly Concentrated in Negative Reviews

Of the 125 negative reviews, **100 (80%)** carry at least one flagged issue, versus only **6 (4.8%)** of the 125 positive reviews. This strong asymmetry confirms these three dimensions are meaningful causal drivers of dissatisfaction.

---

## Top Causes of Dissatisfaction

### 1. Genre Execution Failure (Most Prevalent)
Genre execution failure is the single most common issue among dissatisfied viewers, appearing in **93 of 125 negative reviews (74.4%)**:

| Genre Failure Type | Count (Negative) | Count (Positive) |
|---|---|---|
| `failed_drama` | 46 | 3 |
| `failed_horror` | 17 | 0 |
| `failed_comedy` | 14 | 1 |
| `failed_action` | 11 | 0 |
| `failed_musical` | 5 | 0 |

Drama is the dominant genre in this corpus, and its failure is the most frequent single complaint. Horror, comedy, and action failures are also exclusively (or near-exclusively) associated with negative sentiment.

### 2. Writing Quality Issues (57 of 125 Negative Reviews, 45.6%)
All writing quality flags appear **exclusively in negative reviews**:

| Writing Issue | Count |
|---|---|
| `poor_dialogue` | 18 |
| `uninspired_writing` | 18 |
| `incoherent_narrative` | 11 |
| `cliched_script` | 10 |

Poor dialogue and uninspired writing are the most cited writing flaws. Zero positive reviews carry any writing quality issue — making this a near-perfect discriminator of dissatisfaction.

### 3. Plot & Structural Issues (53 of 125 Negative Reviews, 42.4%)
Plot failures also appear almost entirely in negative reviews:

| Plot Issue | Count (Negative) | Count (Positive) |
|---|---|---|
| `underdeveloped_characters` | 19 | 1 |
| `no_plot` | 12 | 0 |
| `predictable_plot` | 10 | 2 |
| `illogical_story` | 10 | 0 |
| `plot_holes` | 2 | 1 |

Underdeveloped characters and absent/illogical plots are dominant here. `predictable_plot` is the weakest signal — it appears in 2 positive reviews — suggesting audiences can tolerate predictability when execution is strong.

### 4. Compound Failures
**35 of 125 negative reviews (28%)** are flagged across all three issue dimensions simultaneously, indicating a substantial portion of the most dissatisfied viewers experienced failures in writing, plot, *and* genre execution together.

---

## Exceptions and Caveats

- **25 of 125 negative reviews (20%)** carry no issue flags at all, suggesting additional dissatisfaction drivers exist beyond the three measured dimensions (e.g., pacing, acting, production values — referenced in review text but not captured as structured columns).
- `predictable_plot` is the only issue with any meaningful presence in positive reviews (2 instances), making it a weaker causal signal than others.
- The dataset is balanced (50/50 pos/neg), so base-rate bias is not a concern.

---

## Summary

IMDb audiences are primarily dissatisfied due to **genre execution failure** (especially in drama and horror), **poor or uninspired writing** (particularly dialogue and narrative coherence), and **structural plot weaknesses** (underdeveloped characters, absent plots, illogical storytelling). These three factors are strongly co-occurring and collectively explain dissatisfaction in ~80% of negative reviews.
