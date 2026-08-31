---
dataset: imdb_movie_reviews
scenario: eda_sentiment
variant: original
model: substrate-claude-haiku-4-5
query_subtype: exploratory_data_analysis
focus_variable: "label_pos"
query: "How do review themes differ between positive and negative IMDb sentiment?"
source_table: augment_table/imdb_movie_reviews/eda_sentiment/original.csv
generated_at: 2026-07-26T13:54:00.157856+00:00
wall_seconds: 102.07
---

# IMDb Movie Review Themes: Positive vs. Negative Sentiment Analysis

## Executive Summary

Analysis of 250 IMDb reviews (125 positive, 125 negative) reveals distinct thematic differences between sentiments. **The most striking difference is the prevalence of negative language: 44% of negative reviews explicitly mention negatives vs. only 12% in positive reviews—a 32 percentage point gap.** Beyond negativity markers, reviews differ substantially in focus areas, vocabulary emphasis, and argumentation patterns.

## Key Findings

### 1. Explicit Sentiment Expression (Strongest Signal)

| Marker Type | Positive | Negative | Difference |
|-------------|----------|----------|-----------|
| **Negative language** | 12.0% | 44.0% | −32.0pp |
| **Excellence markers** | 16.8% | 4.0% | +12.8pp |
| **Enjoyment language** | 23.2% | 16.0% | +7.2pp |
| **Disappointment** | — | 16.0% | — |

**Interpretation:** Negative reviews rely heavily on explicit criticism (awful, terrible, waste), appearing in 44% of negative reviews. Positive reviews emphasize quality markers (excellent, masterpiece, brilliant) in 21 reviews and enjoyment/pleasure themes in 29 reviews.

### 2. Thematic Focus Differences

| Theme | Positive | Negative | Gap |
|-------|----------|----------|-----|
| **Plot** | 31.2% | 36.0% | −4.8pp |
| **Acting** | 23.2% | 28.0% | −4.8pp |
| **Characters** | 19.2% | 24.8% | −5.6pp |
| **Quality assessment** | 14.4% | 4.0% | +10.4pp |
| **Entertainment value** | 18.4% | 16.0% | +2.4pp |
| **Emotional impact** | 3.2% | 1.6% | +1.6pp |

**Interpretation:** Both sentiments discuss plot, acting, and characters at similar rates (24–36%), indicating these are universal focus areas. However, positive reviews emphasize quality judgments (excellent, masterpiece) in 14.4% of reviews vs. only 4.0% in negative reviews—a notable signal of positive sentiment direction.

### 3. Characteristic Vocabulary

**Positive reviews emphasize:** great, watch, funny, makes, really, never, pretty, films, story, acting, because

**Negative reviews emphasize:** really, movies, acting, story, think, because, people, should, whole, director, before

**Interpretation:** Positive reviews foreground entertainment quality ("funny," "great"), while negative reviews reflect more analytical/critical framing ("think," "should," "whole"). This suggests negative reviewers adopt a more evaluative tone examining what *should have* happened.

### 4. Review Engagement Patterns

- **Positive reviews:** 113.8 words average (SD: 24.7), median 121 words
- **Negative reviews:** 117.6 words average (SD: 19.5), median 122 words
- **Difference:** Minimal (3.8 words), both show similar effort levels

**Interpretation:** Review length and word count show no meaningful difference, indicating both sentiments receive comparable analytical depth.

### 5. Marker-Based Sentiment Strength

| Positive Markers | Count | % |
|---|---|---|
| Enjoyment (love, enjoy, entertaining) | 29 | 23.2% |
| Excellence (excellent, masterpiece, brilliant) | 21 | 16.8% |
| Recommendation | 15 | 12.0% |

| Negative Markers | Count | % |
|---|---|---|
| Complaint (bad, poor, weak) | 46 | 36.8% |
| Disappointment (disappointed, should) | 20 | 16.0% |
| Waste (boring, tedious, dull) | 17 | 13.6% |
| Terrible (awful, horrible, disgusting) | 16 | 12.8% |

**Interpretation:** Negative reviews show stronger explicit markers—46 reviews (36.8%) use complaint language vs. 29 reviews (23.2%) using enjoyment language in positive reviews. This suggests negative sentiment is more forcefully articulated.

## Important Caveats

1. **Limited emotional vocabulary:** Only 3.2% of positive reviews and 1.6% of negative reviews explicitly mention emotional impact, suggesting reviewers focus more on technical/entertainment aspects than emotional resonance regardless of sentiment.

2. **Overlap in dimensions:** Both sentiments discuss acting, plot, and characters at similar rates, indicating shared evaluation criteria rather than entirely distinct focus areas.

3. **Dialogue frequency equal:** 11.2% of both positive and negative reviews mention dialogue, showing no differentiation here.

## Conclusion

Review themes differ primarily in **sentiment expression intensity** rather than topical scope. Both sentiments analyze plot, acting, and characters, but **negative reviews employ explicit criticism in 44% of cases vs. quality markers in positive reviews (14.4% excellence language).** Positive reviews tend to emphasize entertainment value and enjoyment, while negative reviews adopt a more critical, evaluative stance. The 32-percentage-point gap in negative language prevalence is the strongest differentiator between sentiments.
