---
dataset: imdb_movie_reviews
scenario: focus_inference
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What aspects of the films are reviewers focusing on?"
source_table: augment_table/imdb_movie_reviews/focus_inference/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:23:00.488648+00:00
wall_seconds: 44.87
---

# IMDB Movie Reviews — Reviewer Focus Analysis

**Dataset:** 250 reviews · **Variant:** skill_on_v11_update

---

## Key Finding: Plot/Story and Directing Dominate Reviewer Attention

| Focus Dimension | Reviews Mentioning It | Praised | Criticized | Mixed |
|---|---|---|---|---|
| **Plot / Story** | 234 (94%) | 81 | 93 | 60 |
| **Directing / Craft** | 187 (75%) | 64 | 101 | 22 |
| **Acting / Performance** | 107 (43%) | 58 | 39 | 10 |
| **Writing / Script** | 88 (35%) | 16 | 67 | 5 |
| **Technical / Production** | 71 (28%) | 20 | 39 | 12 |

### 1. Plot & Story — Near-Universal Focus (94%)
Plot is the most broadly covered dimension. Sentiment here tracks strongly with overall review polarity:
- **Negative reviews (label_pos=0):** 92 criticized, 27 mixed, only 3 praised plot.
- **Positive reviews (label_pos=1):** 78 praised, 33 mixed, only 1 criticized plot.

This near-perfect split suggests plot satisfaction is a primary driver — or at least a primary *articulation point* — of overall sentiment.

### 2. Directing / Craft — Wide Coverage, Skewed Negative (75%)
Directing is mentioned in three-quarters of reviews, but criticism dominates (101 criticized vs. 64 praised). In negative reviews, 98/125 mention directing critically; in positive reviews, 62/125 praise it. Reviewers clearly see direction as a differentiator worth naming.

### 3. Acting — Selective but Balanced (43%)
Acting is invoked selectively — only in about 4 in 10 reviews — but when present, praise slightly outweighs criticism (58 vs. 39). It is not a default talking point; reviewers reach for it when performance stands out (positively or negatively).

### 4. Writing / Script — Mentioned Less, Criticized More (35%)
When writing is discussed, it skews heavily negative (67 criticized vs. 16 praised). Reviewers tend to call out bad scripting explicitly but are less likely to single out good writing as a standalone merit.

### 5. Technical / Production — Least Common Focus (28%)
Technical aspects are the least-discussed dimension. Criticism still leads (39 vs. 20 praised), suggesting reviewers mostly invoke production quality when something is noticeably poor.

---

## Emotional Engagement
- **Moderate engagement:** 133 reviews (53%)
- **Strong positive:** 61 (24%)
- **Strong negative:** 56 (22%)

Emotional tone is fairly evenly distributed between strong positive/negative, with a majority landing in the moderate range — indicating most reviewers engage analytically rather than reactively.

---

## Comparative References (83% absence)
Most reviews (167/250, 67%) make no comparative reference. When comparisons occur, they favor **other films** (37) and **genre canon** (27), suggesting reviewers ground their judgments in genre expectations or peer films rather than source material or director filmographies.

---

## Audience Framing
Most reviews default to a **general audience** frame (149/250, 60%). Niche-specific and adult/genre-fan framing accounts for ~36%, relevant for exploitation and genre films in the corpus.

---

## Summary
Reviewers most reliably focus on **plot and directing**, which together appear in over 75% of reviews and map cleanly onto overall sentiment. **Acting and writing** are secondary and selective. **Technical production** is a weak, often negative signal. The dominant pattern is: *plot dissatisfaction → negative review; plot + directing praise → positive review*, with writing criticism serving as a secondary negative marker.

> **Exception / Weak evidence:** A small number of positive reviews (13) lack any plot focus — these tend to be genre fan reviews (adult/exploitation) where atmosphere, cast, or aesthetics substitute for narrative judgment.
