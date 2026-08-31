---
dataset: imdb_movie_reviews
scenario: whatif_complaints
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: what_if
focus_variable: "label_pos"
query: "If films addressed the most common audience complaints, how much would positive sentiment increase?"
source_table: augment_table/imdb_movie_reviews/whatif_complaints/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:25:00.933057+00:00
wall_seconds: 41.43
---

# What-If Analysis: Impact of Addressing Audience Complaints on Positive Sentiment

## Dataset Overview

- **Total reviews:** 250 (125 negative `label_pos=0`, 125 positive `label_pos=1`)
- **Complaint flags:** `poor_writing`, `weak_acting`, `bad_pacing`, `poor_direction`, `shallow_characters`
- **Focus variable:** `sentiment_boost_if_complaints_fixed` — estimated fractional boost to positive sentiment if flagged complaints were resolved

---

## Key Findings

### 1. Estimated Sentiment Boost

| Group | Mean Boost |
|---|---|
| All reviews | **+0.310** |
| Negative reviews only | **+0.543** |
| Positive reviews only | **+0.077** |

If the most common audience complaints were fully addressed, negative reviews are estimated to gain a mean sentiment boost of **~54 percentage points** — a substantial potential shift. Positive reviews see negligible boost, confirming the model correctly localizes the effect to dissatisfied viewers.

### 2. Most Common Complaints

| Complaint | Occurrences (of 250) |
|---|---|
| Poor writing | **126** (50%) |
| Poor direction | 64 (26%) |
| Weak acting | 54 (22%) |
| Bad pacing | 51 (20%) |
| Shallow characters | 33 (13%) |

**Poor writing is by far the most prevalent complaint**, appearing in half of all reviews and in 106 of 125 negative reviews (85%). It is the single highest-leverage factor to address.

### 3. Complaint Severity and Boost Scale Together

The more complaints a film accumulates, the higher the estimated boost if they were all fixed:

| # Complaints | Mean Boost |
|---|---|
| 0 | 0.00 |
| 1 | 0.31 |
| 2 | 0.53 |
| 3 | 0.64 |
| 4 | 0.77 |
| 5 | 0.80 |

Films attracting all five complaint types could recover nearly **+0.80** in sentiment — suggesting that multi-complaint films represent the highest opportunity for improvement.

### 4. Per-Complaint Boost (Among Negative Reviews)

| Complaint | Mean Boost |
|---|---|
| Shallow characters | **0.673** |
| Bad pacing | 0.661 |
| Poor direction | 0.645 |
| Weak acting | 0.621 |
| Poor writing | 0.585 |

Among negative reviews, films flagged for **shallow characters, bad pacing, or poor direction** are associated with the highest conditional boosts — suggesting that when these rarer complaints appear, they correlate with more severe dissatisfaction.

---

## Exceptions and Weak Evidence

- **5 negative reviews have zero complaints flagged** and show zero boost — these films' negativity stems from factors not captured in the five complaint categories (e.g., offensive content, subject matter dislike).
- **27 positive reviews** carry at least one complaint flag but still have low estimated boosts (mean 0.077), indicating that complaint presence alone does not dictate sentiment when other strengths compensate.
- The `sentiment_boost` column is a **model-estimated counterfactual**, not an observed outcome. Real-world sentiment changes from production improvements may differ.

---

## Summary Conclusion

Addressing the most common audience complaints — led by **poor writing** (50% prevalence) — could raise positive sentiment in negative reviews by an estimated **+0.54 on average**. Films with multiple stacked complaints (3–5 types) stand to gain the most (+0.64 to +0.80). The dataset suggests that **writing quality** is the highest-reach intervention, while **fixing shallow characters or bad pacing** yields the highest per-film sentiment recovery when present. Overall, systematic complaint resolution could plausibly convert a meaningful share of negative reviews toward positive territory, though a minority of negative reviews (~4%) have no identifiable complaint signal and would not benefit.
