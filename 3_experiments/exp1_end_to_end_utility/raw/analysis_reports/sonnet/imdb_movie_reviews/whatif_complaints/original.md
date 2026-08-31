---
dataset: imdb_movie_reviews
scenario: whatif_complaints
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: what_if
focus_variable: "label_pos"
query: "If films addressed the most common audience complaints, how much would positive sentiment increase?"
source_table: augment_table/imdb_movie_reviews/whatif_complaints/original.csv
generated_at: 2026-07-26T13:56:00.046362+00:00
wall_seconds: 83.87
---

# What-If Analysis: Addressing Common Audience Complaints → Positive Sentiment Increase

**Dataset:** IMDB Movie Reviews — `original.csv` (250 reviews)
**Focus variable:** `label_pos` (1 = positive sentiment, 0 = negative)

---

## Baseline

| Metric | Value |
|---|---|
| Total reviews | 250 |
| Positive reviews | 125 (50.0%) |
| Negative reviews | 125 (50.0%) |

---

## Most Common Audience Complaints (from Negative Reviews)

Negative reviews were scanned for recurring complaint themes using keyword matching:

| Complaint Theme | Negative Reviews Affected | Share of Negatives |
|---|---|---|
| Pacing / boring / tedious | 14 | 11.2% |
| Bad acting / wooden performances | 10 | 8.0% |
| Disappointing / waste of time | 9 | 7.2% |
| Poor script / writing / dialogue | 5 | 4.0% |
| Plot holes / incoherent story | 4 | 3.2% |
| Low budget / poor production | 1 | 0.8% |

**Reviews with at least one identifiable, addressable complaint:** 40 out of 125 negative reviews (32.0%).

---

## Projected Sentiment Shift

Assuming films fully resolved their most common complaints, the addressable negative reviews could flip to positive:

| Scenario | New Positives | New Positive Rate |
|---|---|---|
| **Baseline (no change)** | 125 / 250 | **50.0%** |
| **Optimistic** — all 40 complaint-driven negatives become positive | 165 / 250 | **+16 pp → 66.0%** |
| **Conservative** — top 2 themes addressed (pacing + acting: 24 reviews) | 149 / 250 | **+9.6 pp → 59.6%** |

---

## Key Observations

- **Pacing** is the single most cited complaint (11.2% of negatives), suggesting tighter editing has the greatest addressable impact.
- **Acting quality** (8%) and **script/dialogue** (4%) follow; these are intertwined — weak writing often produces poor performances.
- Many negative reviews (68% of negatives) express **general displeasure** without pinpointing a specific, fixable complaint (e.g., vague disappointment, dislike of genre, or subjective taste). Resolving technical deficiencies would not capture this segment.

## Caveats & Limitations

- Keyword matching is a proxy — some complaints may be expressed without trigger words, and the 32% figure is likely a **lower bound** on complaint-driven negatives.
- The sentiment label reflects overall reaction; a film could address one complaint yet still receive a negative review for unrelated reasons.
- The "waste of time / disappointed" category (7.2%) overlaps strongly with other themes and may not represent independently addressable issues.
- No counterfactual data exists to validate what fraction of complaint-driven negatives would actually flip to positive upon improvement.

---

## Summary

If films addressed their most common audience complaints — especially **pacing, acting quality, and weak writing** — the data suggests positive sentiment could increase by roughly **+10 to +16 percentage points**, lifting the positive rate from **50% to an estimated 60–66%**. The strongest lever is pacing/boredom (the most frequently cited flaw), followed by acting. However, the majority of negative sentiment in this dataset stems from factors that are either subjective or not easily categorizable as fixable production complaints, capping realistic upside well below 66%.
