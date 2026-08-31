---
dataset: imdb_movie_reviews
scenario: concept_attribute_praise
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: faceted_decomposition
focus_variable: "audience_praise_and_complaints"
query: "What praise and complaints appear in IMDb reviews?"
source_table: augment_table/imdb_movie_reviews/concept_attribute_praise/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:23:02.721608+00:00
wall_seconds: 61.64
---

# IMDb Movie Reviews: Praise and Complaints Analysis

## Method Note
TAPP-generated columns used: `overall_sentiment_polarity`, `praise_dimension`, `complaint_dimension`, `emotional_engagement`, `comparative_reference_type`, `audience_recommendation_stance`. These were cross-checked against the original structured column `label_pos` (0 = negative, 1 = positive) throughout.

---

## Dataset Overview
- **250 reviews** total; perfectly balanced: 125 positive (`label_pos=1`), 125 negative (`label_pos=0`).
- `overall_sentiment_polarity` aligns tightly with `label_pos`: 95 of 125 positive reviews are tagged *positive*, 91 of 125 negative are tagged *negative*, and 61 reviews are *mixed* (split ~50/50 by label).

---

## What Reviewers Praise

**Acting** is the most frequently praised dimension overall (78/250, 31%), and is overwhelmingly concentrated in positive reviews (48 pos vs. 30 neg). Even negative reviews often acknowledge a performance bright spot—but that praise coexists with complaints elsewhere.

| Praise Dimension | Positive reviews | Negative reviews | Total |
|---|---|---|---|
| acting | 48 | 30 | **78** |
| story_plot | 24 | 36 | **60** |
| writing_script | 14 | 27 | **41** |
| direction_cinematography | 14 | 18 | **32** |
| music_soundtrack | 7 | 5 | **12** |
| emotional_resonance | 8 | 1 | **9** |
| originality | 5 | 1 | **6** |
| production_values_sfx | 2 | 4 | **6** |

**Key insight:** `story_plot` is praised more often in *negative* reviews (36 vs. 24). Reviewers of bad films frequently concede an interesting premise but find execution lacking — a pattern confirmed by the complaint data below. `emotional_resonance` and `originality` are almost exclusively positive-review praise (8/9 and 5/6 respectively), suggesting these are differentiating qualities for highly-regarded films.

---

## What Reviewers Complain About

143 of 250 reviews (57%) have **no complaint** detected (`complaint_dimension = not_present`). Of those, 116 are positive reviews and 27 are negative — meaning negative reviews almost always carry an explicit complaint.

| Complaint Dimension | Negative | Positive | Total |
|---|---|---|---|
| not_present | 27 | 116 | **143** |
| writing_script | 33 | 1 | **34** |
| acting | 23 | 1 | **24** |
| story_plot | 14 | 3 | **17** |
| direction_cinematography | 9 | 1 | **10** |
| pacing_too_slow | 5 | 2 | **7** |
| predictability | 4 | 0 | **4** |
| casting_mismatch | 3 | 0 | **3** |
| budget_production_quality | 3 | 1 | **4** |

**Writing/script** is by far the most cited complaint (34 cases, 97% from negative reviews), followed by **acting** (24) and **story/plot** (17). `predictability` and `casting_mismatch` appear exclusively in negative reviews. Notably, **acting** is simultaneously the top praise *and* second-largest complaint dimension — it is the single most debated craft element on IMDb.

---

## Emotional Engagement and Recommendation Stance

`emotional_engagement` is a near-perfect discriminator between positive and negative labels:

| Engagement | Negative | Positive |
|---|---|---|
| strongly_engaging | 0 | **68** |
| moderately_engaging | 18 | 54 |
| flat_unengaging | 43 | 3 |
| off_putting | **64** | 0 |

All 64 "off_putting" reviews are negative; all 68 "strongly_engaging" are positive. `moderately_engaging` skews positive (54 vs. 18), while `flat_unengaging` skews negative.

`audience_recommendation_stance` mirrors this pattern cleanly:

| Stance | Negative | Positive |
|---|---|---|
| strong_avoid | 69 | 0 |
| conditional_avoid | 36 | 3 |
| neutral_or_niche_recommend | 14 | 21 |
| conditional_recommend | 5 | 17 |
| strong_recommend | 1 | **84** |

---

## Comparative References

Only 80 reviews (32%) invoke comparisons. Among those:
- **Favorable comparisons** appear almost exclusively in positive reviews (22/23).
- **Unfavorable comparisons** appear almost exclusively in negative reviews (22/23).
- **Sequel/adaptation comparisons** skew negative (12 neg vs. 7 pos), suggesting adaptation disappointment is a distinct complaint pattern.
- **Genre benchmark references** are evenly split (7 neg, 8 pos) — used both to praise genre excellence and flag genre failure.

---

## Mixed-Sentiment Reviews (n=61)

61 reviews carry `overall_sentiment_polarity = mixed`, split nearly evenly by label (31 neg, 30 pos). In these reviews:
- `story_plot` is the top praise (22/61), suggesting reviewers acknowledge narrative ambition even when overall impressions are divided.
- 38/61 mixed reviews have **no explicit complaint**, indicating many mixed-sentiment reviews praise with reservations rather than balance praise with a direct complaint.
- `pacing_too_slow` (5 cases) and `writing_script` (5 cases) are the dominant complaints when present.

---

## Summary

| Question | Finding |
|---|---|
| **Top praise categories** | Acting (78), Story/Plot (60), Writing/Script (41) |
| **Top complaint categories** | Writing/Script (34), Acting (24), Story/Plot (17) |
| **Most polarizing craft element** | Acting — #1 in both praise and complaints |
| **Praise unique to positive reviews** | Emotional resonance, originality |
| **Complaints unique to negative reviews** | Predictability, casting mismatch |
| **Engagement signal** | `off_putting` → 100% negative; `strongly_engaging` → 100% positive |
| **Comparative framing** | Favorable/unfavorable comparisons cleanly track sentiment polarity |
