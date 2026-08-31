---
dataset: amazon_polarity_reviews
scenario: predictive_sentiment
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "label_pos"
query: "How do review facets differ by sentiment label?"
source_table: augment_table/amazon_polarity_reviews/predictive_sentiment/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:02:48.615761+00:00
wall_seconds: 51.45
---

# Review Facets by Sentiment Label: Analysis Report

## Executive Summary

This analysis examines how linguistic and stylistic facets of Amazon product reviews differ between positive (label=1) and negative (label=0) sentiment labels. The dataset contains 250 reviews (125 positive, 125 negative) with six engineered linguistic features capturing emotional intensity, content complexity, and sentiment word usage.

## Key Findings

### 1. Sentiment Word Distribution (Primary Differentiator)

**Praise Words: Most Distinctive Feature**
- Positive reviews average **0.83 praise words per review** vs. negative reviews at **0.29**
- This represents a **+189% increase** for positive reviews
- Positive reviews show more variability in praise word usage (std=0.85) compared to negative reviews (std=0.51)
- 40.8% of positive reviews contain praise words, while only 26.4% of negative reviews do

**Criticism Words: Strong Negative Signal**
- Negative reviews contain **0.49 criticism words per review** vs. positive reviews at **0.11**
- Criticism word usage is **77% lower** in positive reviews
- Negative reviews have more consistent criticism signals (std=0.79 vs. 0.36)
- 33.6% of negative reviews contain criticism words, compared to just 9.6% of positive reviews

**Mixed Sentiment Rarity**
- Only 8.8% of negative reviews contain both criticism and praise words
- Only 4.8% of positive reviews contain both
- This suggests reviews tend to have dominant sentiment tone rather than balanced mixed opinions

### 2. Capitalization & Emphasis Patterns

**Capitalized Words: Indicator of Intensity**
- Negative reviews use **1.19 capitalized words on average** vs. positive reviews at **0.55**
- Capitalization is **54% more prevalent** in negative reviews
- Negative reviews show higher variability in emphasis patterns, suggesting variable emotional intensity

**Interpretation**: ALL-CAPS emphasis appears more frequently in complaint-focused reviews, likely for emphasis and frustration signaling.

### 3. Question Usage: Question Rarity in Positive Reviews

**Questions per Review**
- Negative reviews: **0.15 questions per review**
- Positive reviews: **0.04 questions per review**
- Questions are **74% less common** in positive reviews

**Interpretation**: Negative reviews occasionally use rhetorical questions or expressions of confusion ("Why does this happen?", "How could they...?"), while positive reviews rarely employ questioning structures.

### 4. Exclamation Marks: Minimal Differentiation

**Exclamation Counts**
- Negative reviews: 0.68 per review
- Positive reviews: 0.66 per review
- Difference: **-2.4% (statistically negligible)**

**Interpretation**: Both positive and negative reviews use exclamation marks at similar rates, suggesting this feature captures emotional intensity across both sentiments rather than differentiating them. Exclamations serve different functions: emphasizing frustration in negative reviews vs. conveying enthusiasm in positive reviews.

### 5. Review Length & Sentence Structure

**Overall Review Length**
- Negative reviews: **373.6 characters** on average
- Positive reviews: **363.9 characters** on average  
- Difference: **-2.6%** (minimal distinction)

**Sentence Length**
- Negative reviews: **15.56 words per sentence**
- Positive reviews: **14.67 words per sentence**
- Negative reviews use slightly longer, more complex sentence structures (-5.7% shorter in positive)

**Interpretation**: Negative reviewers show modestly higher verbosity and structural complexity, though the difference is small. This suggests review length is not a strong discriminator of sentiment.

## Facet Summary Table

| Feature | Negative (Label=0) | Positive (Label=1) | Difference | Interpretation |
|---------|-------------------|--------------------|------------|-----------------|
| Praise Words | 0.29 | 0.83 | +189% | **Strong positive signal** |
| Criticism Words | 0.49 | 0.11 | -77% | **Strong negative signal** |
| Caps Words | 1.19 | 0.55 | -54% | Emphasis in negatives |
| Question Count | 0.15 | 0.04 | -74% | Questioning in negatives |
| Exclamation Count | 0.68 | 0.66 | -2% | Weak differentiator |
| Avg Sentence Length | 15.56 | 14.67 | -6% | Slight complexity |
| Review Length (chars) | 373.6 | 363.9 | -3% | Weak differentiator |

## Notable Patterns & Exceptions

### Strong Evidence
- **Sentiment word balance** is the dominant distinguishing feature, with praise/criticism ratios providing clear signal separation
- **Capitalization patterns** show consistent divergence, indicating emotional intensity correlates with negative sentiment

### Weak/No Evidence
- **Exclamation marks** show minimal difference; enthusiasm and frustration both employ exclamations
- **Overall review length** is not informative; both positive and negative reviewers write comparably long reviews
- **Sentence complexity** differs marginally; both sentiment groups use similar linguistic structures

### Data Limitations
- The "skill_off_update" variant indicates this may be augmented data without model-based skill adjustment
- Some reviews (especially positive) contain implicit praise without explicit praise words
- Dataset is balanced (125-125 split), which may not reflect real-world sentiment distribution

## Conclusion

Review facets differ most substantially in **sentiment word composition** (praise vs. criticism) and **emotional emphasis markers** (capitalization, questions). These engineered features effectively capture the distinction between positive and negative reviews. However, surface-level stylistic metrics like length and sentence structure provide limited discriminative power, suggesting that **content semantics** (what sentiment words appear) matters far more than **structural form** (how long or complex the review is).

For predictive modeling, the most reliable signals are:
1. Presence and frequency of praise words (+189% in positive)
2. Presence and frequency of criticism words (-77% in positive)  
3. Capitalization patterns (-54% in positive)
4. Question usage (-74% in positive)

The near-identical exclamation mark counts across sentiments highlight that emotional intensity is expressed differently by positive and negative reviewers, requiring semantic understanding beyond simple punctuation analysis.
