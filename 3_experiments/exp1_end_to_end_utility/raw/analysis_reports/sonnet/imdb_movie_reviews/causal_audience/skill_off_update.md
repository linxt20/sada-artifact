---
dataset: imdb_movie_reviews
scenario: causal_audience
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "audience_dissatisfaction"
query: "Why are IMDb audiences dissatisfied?"
source_table: augment_table/imdb_movie_reviews/causal_audience/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:23:53.109347+00:00
wall_seconds: 35.16
---

# Why Are IMDb Audiences Dissatisfied?

## Dataset Overview

- **Total reviews:** 250 (125 negative, 125 positive; perfectly balanced)
- **Focus variable:** `label_pos` (0 = negative/dissatisfied, 1 = positive)
- **Augmented signals:** `dissatisfaction_category`, `complaint_intensity`, `mentions_acting_issues`, `mentions_writing_issues`, `wasted_potential`

---

## Primary Causes of Dissatisfaction

Among the 125 negative reviews, the following dissatisfaction categories are observed:

| Category | Count | % of Negative | Avg. Complaint Intensity |
|---|---|---|---|
| `general_dislike` | 39 | 31.2% | 0.54 |
| `bad_writing` | 36 | 28.8% | 0.83 |
| `poor_acting` | 32 | 25.6% | 0.34 |
| `boring_pacing` | 9 | 7.2% | **1.33** |
| `poor_direction` | 7 | 5.6% | 0.57 |
| `disappointment` | 1 | 0.8% | 0.00 |
| `unoriginal` | 1 | 0.8% | 0.00 |

### Key Findings

1. **Writing quality is the leading specific complaint.** `bad_writing` (28.8%) has the second-highest complaint intensity (0.83), suggesting that when audiences identify writing failures, they express them forcefully. In total, **51 of 125 negative reviews (40.8%)** explicitly mention writing issues via `mentions_writing_issues`.

2. **Boring pacing, though rare, drives the strongest dissatisfaction.** `boring_pacing` accounts for only 9 reviews but yields the highest average complaint intensity (1.33), indicating these reviewers are particularly vehement. This is a notable signal despite the small sample.

3. **Acting complaints are widespread but less intense.** `poor_acting` covers 25.6% of negative reviews, and **42 reviews (33.6%)** flag acting issues via `mentions_acting_issues`. However, average complaint intensity is low (0.34), suggesting acting problems are frequently noted but not always the primary driver.

4. **General dislike is the most common category but least informative.** The largest single category (39 reviews, 31.2%) lacks specificity—these reviews express broad displeasure without isolating a single cause.

5. **Co-occurring writing and acting failures amplify dissatisfaction.** 19 reviews cite both acting and writing problems simultaneously, while 32 cite writing alone and 23 cite acting alone—suggesting script and performance issues often reinforce each other.

6. **Wasted potential is rarely flagged.** Only 4 negative reviews (3.2%) mark `wasted_potential = 1`, indicating that audience dissatisfaction stems more from execution failures than from high expectations unmet.

---

## Summary

IMDb audiences are dissatisfied primarily due to **poor writing** (the most intense and frequently cited specific complaint) and **weak acting performances**. **Boring pacing**, though found in fewer reviews, generates the sharpest negative reactions when present. A large share of dissatisfaction is expressed as diffuse general dislike, which may reflect combinations of the above factors. Wasted potential and lack of originality are marginal contributors in this dataset.

> **Caveat:** `complaint_intensity` scores are low overall (mean = 0.62 for negative reviews, max observed = 5), and several augmented categories (`disappointment`, `unoriginal`) have very few samples (n=1), making conclusions for those categories unreliable.
