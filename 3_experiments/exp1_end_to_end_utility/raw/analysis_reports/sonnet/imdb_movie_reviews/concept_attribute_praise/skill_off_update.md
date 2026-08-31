---
dataset: imdb_movie_reviews
scenario: concept_attribute_praise
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "audience_praise_and_complaints"
query: "What praise and complaints appear in IMDb reviews?"
source_table: augment_table/imdb_movie_reviews/concept_attribute_praise/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:24:00.127577+00:00
wall_seconds: 39.64
---

# IMDb Movie Reviews: Praise and Complaints Analysis

**Dataset:** `sonnet__skill_off_update.csv` — 250 reviews, balanced (125 positive `label_pos=1`, 125 negative `label_pos=0`)  
**Variant:** `skill_off`  
**Focus columns:** `praised_aspects`, `complained_aspects`, `praise_count`, `complaint_count`, `review_sentiment_type`

---

## Overview

| Metric | Value |
|---|---|
| Total reviews | 250 |
| Avg praise count per review | 0.35 |
| Avg complaint count per review | 0.40 |
| Reviews with both praise & complaints | 16 (6.4%) |
| Predominantly praise | 54 (21.6%) |
| Predominantly complaint | 54 (21.6%) |
| Mixed | 11 (4.4%) |
| **Neutral** (no praise/complaint flagged) | **131 (52.4%)** |

---

## Praised Aspects

Among reviews where praise was explicitly tagged (n=27 instances across all reviews):

| Aspect | Count |
|---|---|
| Acting | 17 |
| Direction | 3 |
| Plot | 3 |
| Dialogue | 2 |
| Pacing / Characters | 1 each |

**Acting** is by far the most frequently praised element. It appears predominantly in positive reviews (`label_pos=1`: 13 of 17 acting praise instances), confirming strong alignment between acting praise and overall positive sentiment.

---

## Complained Aspects

Among reviews where complaints were explicitly tagged (n=46 instances):

| Aspect | Count |
|---|---|
| Plot | 16 |
| Acting | 9 |
| Pacing | 7 |
| Dialogue | 6 |
| Characters | 4 |
| Direction | 4 |

**Plot** is the dominant complaint target, appearing in 15 of 16 plot-complaint instances within negative reviews (`label_pos=0`). Acting, though frequently praised, is also the second most complained-about aspect — suggesting it is the most polarizing dimension across the dataset.

---

## Praise vs. Complaint by Review Polarity

| | Positive reviews (label=1) | Negative reviews (label=0) |
|---|---|---|
| Top praised aspect | Acting (13) | Acting (4) |
| Top complained aspect | Pacing (3) | Plot (15) |

Positive reviews rarely generate complaints (only 4 total complaint instances, mostly pacing/plot). Negative reviews rarely generate praise (only 6 instances, weak acting praise). This asymmetry is internally consistent.

---

## Important Caveats

- **52% of reviews are labeled "neutral"** with zero praise or complaint counts. This is the dominant class, suggesting the annotation model (skill_off) frequently abstained from labeling aspects even in sentiment-bearing text. This is a known limitation of the `skill_off` variant and likely undercounts real praise/complaint signal.
- Only **16 reviews (6.4%)** contain both praise and complaint, meaning nuanced mixed assessments are sparsely captured.
- Praised aspect vocabulary is narrow (6 unique aspects); the dataset may miss fine-grained dimensions (e.g., cinematography, soundtrack, pacing in positive reviews).
- Evidence for complaints about **direction** and **characters** is present but thin (4 instances each), so conclusions about those aspects should be treated as weak.

---

## Summary

IMDb reviewers in this dataset most commonly **praise acting** and most commonly **complain about plot**, with pacing, dialogue, and direction as secondary complaint themes. The `skill_off` variant heavily under-annotates reviews (>50% neutral), so measured rates should be interpreted as lower bounds rather than true frequencies.
