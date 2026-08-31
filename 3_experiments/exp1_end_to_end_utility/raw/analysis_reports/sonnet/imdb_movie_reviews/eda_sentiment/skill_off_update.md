---
dataset: imdb_movie_reviews
scenario: eda_sentiment
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "label_pos"
query: "How do review themes differ between positive and negative IMDb sentiment?"
source_table: augment_table/imdb_movie_reviews/eda_sentiment/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:24:19.506390+00:00
wall_seconds: 43.81
---

# Review Theme Differences Between Positive and Negative IMDb Sentiment

## Dataset Overview

- **250 reviews** (125 positive `label_pos=1`, 125 negative `label_pos=0`), perfectly balanced.
- Columns available: dominant theme, aspect scores (acting, plot, direction, music, humor, emotion, special effects, nostalgia), sentiment word counts, sarcasm signal, and review length.

---

## 1. Dominant Theme Distribution

| Theme | Negative (%) | Positive (%) |
|---|---|---|
| **Acting** | **35.2** | 26.4 |
| **Direction** | 20.8 | **32.8** |
| **Plot** | **21.6** | 16.8 |
| Humor | 8.8 | 8.0 |
| General | 7.2 | 5.6 |
| Nostalgia/Childhood | 2.4 | 4.0 |
| Music | 2.4 | 3.2 |
| Emotion | 1.6 | 2.4 |
| Special Effects | 0.0 | 0.8 |

**Key finding:** Negative reviews disproportionately center on **acting** (35% vs. 26%) and **plot** (22% vs. 17%), while positive reviews are more likely to foreground **direction** (33% vs. 21%). This suggests that dissatisfied viewers blame poor performances and weak storytelling, whereas satisfied viewers praise the filmmaking craft.

---

## 2. Aspect Mention Rates (Score > 0)

| Aspect | Positive | Negative |
|---|---|---|
| Direction | **0.59** | 0.55 |
| Acting | 0.49 | **0.54** |
| Plot | 0.41 | **0.56** |
| Humor | 0.22 | 0.24 |
| Emotion | 0.15 | 0.12 |
| Nostalgia | 0.16 | 0.15 |
| Special Effects | 0.06 | 0.08 |
| Music | 0.13 | 0.12 |

Negative reviews mention **plot** noticeably more often (56% vs. 41%), reinforcing that story failures are a primary complaint. Acting is cited slightly more in negative reviews. Direction is mentioned at near-equal rates but drives the dominant theme more heavily in positive reviews.

---

## 3. Sentiment Word Usage

| | Positive Reviews | Negative Reviews |
|---|---|---|
| Mean positive word count | **1.02** | 0.39 |
| Mean negative word count | 0.26 | **1.28** |
| Mean sentiment word ratio | **0.34** | 0.11 |

The sentiment lexicon cleanly separates the two groups. Negative reviews carry ~3× more negative words; positive reviews carry ~2.6× more positive words. The `sentiment_word_ratio` (positive / total sentiment words) is ~3× higher for positive reviews (0.34 vs. 0.11), confirming strong lexical alignment with label.

---

## 4. Sarcasm Signal

Both groups show an identical, near-zero sarcasm rate (0.008 — just 1 review each), so sarcasm cannot explain sentiment divergence in this dataset. This is a weak signal and should not be relied upon.

---

## 5. Summary of Thematic Contrasts

| Dimension | Negative Reviews | Positive Reviews |
|---|---|---|
| **Central complaint/praise** | Weak acting, poor plot | Strong direction/craft |
| **Dominant theme** | Acting (35%) | Direction (33%) |
| **Most-cited aspect** | Plot (56% mention rate) | Direction (59% mention rate) |
| **Lexical tone** | Negatively loaded | Positively loaded |

---

## Caveats

- Aspect scores are integer-coded and likely model-generated, so ties in dominant theme assignment could introduce noise.
- The difference in mention rates for most aspects is modest (< 10 pp), except for **plot** (−15 pp for positive vs. negative) and the dominant theme shift toward **direction** in positive reviews — these are the most reliable signals.
- Music, emotion, special effects, and nostalgia themes are rare in both groups and offer limited discriminative power.
