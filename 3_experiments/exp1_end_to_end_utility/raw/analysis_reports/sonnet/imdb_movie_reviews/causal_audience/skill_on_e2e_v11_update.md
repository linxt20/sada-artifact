---
dataset: imdb_movie_reviews
scenario: causal_audience
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "audience_dissatisfaction"
query: "Why are IMDb audiences dissatisfied?"
source_table: augment_table/imdb_movie_reviews/causal_audience/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:22:48.012501+00:00
wall_seconds: 56.22
---

# Why Are IMDb Audiences Dissatisfied?

**Query:** Why are IMDb audiences dissatisfied?  
**Dataset:** 250 IMDb reviews (125 negative `label_pos=0`, 125 positive `label_pos=1`)  
**Method note:** Three TAPP-generated columns were used in this analysis: `writing_quality_issue`, `plot_originality_rating`, and `character_development_quality`. All three showed strong signal and are cited below alongside the original `label_pos` outcome column.

---

## Key Finding

IMDb audience dissatisfaction is driven by **poor writing craft**, **underdeveloped characters**, and **unoriginal plots**. These three factors compound each other and are strongly concentrated in negative reviews.

---

## 1. Writing Quality Is the Dominant Differentiator

`writing_quality_issue` is the clearest separator between satisfied and dissatisfied audiences.

| Writing Issue | Negative Reviews (n=125) | Positive Reviews (n=125) |
|---|---|---|
| `not_present` | 37 (29.6%) | 121 (96.8%) |
| `weak_screenplay` | 64 (51.2%) | 3 (2.4%) |
| `clichéd_script` | 11 (8.8%) | 1 (0.8%) |
| `incoherent_plot` | 7 (5.6%) | 0 (0.0%) |
| `stilted_dialogue` | 6 (4.8%) | 0 (0.0%) |

- **70.4%** of negative reviews flag a writing quality problem vs. only **3.2%** of positive reviews.
- `weak_screenplay` alone accounts for 51% of all negative reviews — the single largest driver of dissatisfaction.
- `incoherent_plot` and `stilted_dialogue` appear **exclusively** in negative reviews, indicating they are sufficient (if not necessary) causes of dissatisfaction.

---

## 2. Poor Character Development Strongly Predicts Dissatisfaction

Among the 167 reviews where `character_development_quality` was annotated (coverage: 99/125 negative, 68/125 positive):

| Metric | Negative (n=99) | Positive (n=68) |
|---|---|---|
| Mean score | 1.74 / 5 | 4.01 / 5 |
| Median score | 2 | 4 |
| Score ≤ 2 ("poor") | **87 / 99 (87.9%)** | **3 / 68 (4.4%)** |

The gap is stark: nearly 9 in 10 dissatisfied reviewers rated character development as poor (≤2/5), vs. fewer than 1 in 20 satisfied reviewers. Flat, wooden, or one-dimensional characters are a core grievance in negative reviews.

---

## 3. Lack of Plot Originality Amplifies Dissatisfaction

`plot_originality_rating` has lower coverage (78/250, 31%), but where available the signal is strong:

| Metric | Negative (n=50 rated) | Positive (n=28 rated) |
|---|---|---|
| Mean score | 1.72 / 5 | 4.07 / 5 |
| Median score | 2 | 4 |
| Score ≤ 2 | 45 / 50 (90%) | 1 / 28 (3.6%) |

Dissatisfied audiences overwhelmingly found plots derivative or formulaic. No negative review in the rated sample scored plot originality above 4; no positive review scored below 3 (one exception). The low annotation coverage (~40% of negatives, ~22% of positives) means this facet reinforces but does not independently explain dissatisfaction.

---

## 4. Compound Effect: All Three Facets Together

The majority of dissatisfied reviewers are penalized on multiple fronts simultaneously — weak scripts paired with underdeveloped characters and recycled plots. Positive reviews, by contrast, are characterized by `not_present` writing issues, high character development scores (median 4/5), and high originality scores (median 4/5).

---

## Summary

| Driver | Negative Reviews | Positive Reviews | Signal Strength |
|---|---|---|---|
| Writing quality issue (`writing_quality_issue`) | 70.4% flagged | 3.2% flagged | **Very strong** |
| Poor character development (`character_development_quality` ≤2) | 87.9% | 4.4% | **Very strong** |
| Low plot originality (`plot_originality_rating` ≤2) | 90% (of rated) | 3.6% (of rated) | **Strong (low coverage)** |

**IMDb audiences are dissatisfied primarily because films and shows fail at fundamental craft: screenplays are weak or clichéd, characters are poorly developed, and plots are unoriginal.** Writing quality (`weak_screenplay` in particular) is the single most prevalent complaint, present in over half of all negative reviews, while character shallowness and formulaic storytelling compound the dissatisfaction.
