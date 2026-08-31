---
dataset: imdb_movie_reviews
scenario: eda_sentiment
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: exploratory_data_analysis
focus_variable: "label_pos"
query: "How do review themes differ between positive and negative IMDb sentiment?"
source_table: augment_table/imdb_movie_reviews/eda_sentiment/original.csv
generated_at: 2026-07-26T13:54:05.875758+00:00
wall_seconds: 91.93
---

# IMDb Movie Reviews — EDA: Review Theme Differences by Sentiment

**Dataset:** `original.csv` — 250 reviews (125 positive `label_pos=1`, 125 negative `label_pos=0`)

---

## 1. Dataset Overview

| Metric | Positive | Negative |
|---|---|---|
| Count | 125 | 125 |
| Avg. review length (words) | 114 | 118 |

The corpus is perfectly balanced. Review lengths are nearly identical, so length is not a confounding factor in theme comparisons.

---

## 2. Distinguishing Vocabulary (Document-Frequency Ratio)

The table below shows words appearing at markedly different rates across sentiments (measured as share of reviews containing the word).

### Words Significantly More Common in Positive Reviews

| Word | Positive doc-freq | Negative doc-freq | Ratio |
|---|---|---|---|
| wonderful | 10% | 2% | 4.4× |
| performance | 9% | 2% | 2.9× |
| great | 24% | 10% | 2.2× |
| best | 16% | 7% | 2.1× |
| years / nostalgia | 16% | 7% | 2.1× |
| well | 23% | 13% | 1.8× |
| classic | 8% | 5% | 1.6× |

### Words Significantly More Common in Negative Reviews

| Word | Positive doc-freq | Negative doc-freq | Ratio |
|---|---|---|---|
| worst | 2% | 11% | 3.6× |
| nothing | 3% | 12% | 3.1× |
| whole | 2% | 10% | 3.3× |
| didn't | 2% | 8% | 2.6× |
| plot | 8% | 15% | 1.8× |
| every | 6% | 12% | 2.0× |
| only | 15% | 26% | 1.6× |
| scene/scenes | 4–5% | 8–10% | 1.8× |

---

## 3. Thematic Theme Analysis

Using keyword-bucket matching across seven thematic areas:

| Theme | Positive | Negative | Δ |
|---|---|---|---|
| Acting / Performance | 51% | 52% | ≈0 |
| Story / Plot | 37% | 42% | −5 pp |
| Direction / Cinematography | 18% | 18% | ≈0 |
| Humor / Comedy | 20% | 24% | −4 pp |
| Emotion / Drama | 6% | 7% | ≈0 |
| **Nostalgia / Childhood** | **27%** | **19%** | **+8 pp** |
| Horror / Thriller | 9% | 10% | ≈0 |

Key observations:

- **Nostalgia/Childhood** is the clearest thematic differentiator: 27% of positive reviews invoke nostalgia, youth, or long-term memory vs. only 19% of negative reviews. Positive reviewers often frame enjoyment in terms of personal history with a film.
- **Story/Plot critique** skews slightly negative (42% vs. 37%), consistent with the word "plot" appearing ~1.8× more in negative reviews — dissatisfied reviewers focus on narrative failures.
- **Acting/Performance** is mentioned at nearly equal rates (~51–52%), but the *valence* differs sharply: positive reviews use "wonderful" and "performance" approvingly, while negative reviews use generic "acting" in a critical context.
- **Humor/Comedy** mentions appear slightly more in negative reviews (24% vs. 20%), suggesting critics discuss failed comedic execution.
- High-level themes like **direction**, **horror**, and **emotion** show no meaningful split at this granularity.

---

## 4. Qualitative Tone Patterns

- **Positive reviews** employ evaluative superlatives (*best, great, wonderful, classic*) and reflective framing (*years ago, watched again, childhood*). The tone is often personal and enthusiastic.
- **Negative reviews** rely on rhetorical negation (*nothing, didn't, isn't, worst, whole [film]*) and scene-level critique (*every scene, plot, scenes*), suggesting a more analytical, point-by-point dissection of failures.
- Both camps discuss *acting* and *story* with similar frequency, but the lexical context differs: positive reviews praise *performances*, negative ones attack *plot holes* and generic *acting*.

---

## 5. Caveats and Weak Evidence

- The theme bucket analysis uses simple keyword presence; co-occurrence or negation (e.g., "not funny") is not distinguished, so percentages may slightly inflate negative themes in positive reviews and vice versa.
- With only 125 reviews per class, small differences (< 5 pp) should be treated as directional signals rather than robust findings.
- Genre distribution across sentiments is unknown; if negative reviews over-represent a particular genre (e.g., horror), some "theme" differences may reflect genre skew rather than pure sentiment.

---

## Summary

The clearest thematic split is **nostalgia vs. plot critique**: positive reviewers reminisce and praise specific performances with superlative language, while negative reviewers dissect narrative and scene-level failures using negation-heavy, critical vocabulary. Acting and story are discussed across both camps, but the framing is fundamentally different in tone and specificity.
