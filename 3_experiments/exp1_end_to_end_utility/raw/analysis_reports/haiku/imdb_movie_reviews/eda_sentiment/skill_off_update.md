---
dataset: imdb_movie_reviews
scenario: eda_sentiment
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "label_pos"
query: "How do review themes differ between positive and negative IMDb sentiment?"
source_table: augment_table/imdb_movie_reviews/eda_sentiment/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:24:13.178878+00:00
wall_seconds: 45.97
---

# Review Themes and Sentiment Analysis: IMDb Movie Reviews

## Overview

This analysis examines how review themes differ between positive and negative IMDb sentiment across 250 balanced movie reviews (125 positive, 125 negative). The dataset captures detected themes, sentiment word frequencies, and sentiment descriptions to identify patterns in how reviewers discuss films differently based on satisfaction.

## Key Findings

### Theme Distribution by Sentiment

**Positive Reviews** prioritize performance and entertainment:
- **Acting (21.0%)**: Dominant theme—reviewers celebrate specific performances
- **Plot (16.1%)**: Story quality frequently praised
- **Directing (13.7%)**: Directorial vision highlighted
- **Entertainment (11.3%)**: Enjoyment value emphasized
- **Emotions (3.2%)**: Emotional impact matters for satisfaction

**Negative Reviews** spread criticism across craft elements:
- **Acting (19.1%)**: Primary failure point, though slightly less dominant
- **Plot (18.0%)**: Structural narrative problems emphasized (+1.9% vs. positive)
- **Directing (16.0%)**: Most prominent craft criticism (+2.3% vs. positive)
- **Character Depth (10.5%)**: Shallow characterization noted (+1.2% vs. positive)
- **Dialogue (9.8%)**: Poor writing cited (+1.7% vs. positive)

### Critical Differences

1. **Craft Specificity**: Negative reviews emphasize directing deficiencies, dialogue quality, and character development more frequently, suggesting reviewers focus on *what fails* when dissatisfied.

2. **Emotional Resonance**: Emotions appear 1.6x more often in positive reviews (3.2% vs. 2.0%), indicating emotional impact is a key satisfaction driver.

3. **Categorical vs. Specific**: "General" themes are 1.5x higher in positive reviews (9.3% vs. 6.2%), suggesting satisfied reviewers offer broader endorsements rather than granular critiques.

4. **Entertainment Framing**: While both discuss entertainment (11.3% vs. 9.0%), positive reviewers celebrate delivery while negative reviewers critique failure to entertain.

### Sentiment Word Evidence

Linguistic patterns validate theme patterns:
- **Positive words**: Positive reviews use 2x more (1.21 vs. 0.60 mean)
- **Negative words**: Negative reviews use 4.5x more (0.86 vs. 0.19 mean)
- **Sentiment ratio**: Positive reviews: 0.386; Negative reviews: 0.177

This sharp divergence confirms positive reviewers employ substantially more positive language with minimal criticism, while negative reviewers rely heavily on negative descriptors with limited praise.

## Reviewers' Focus by Sentiment

**Satisfied viewers** discuss:
- Specific acting excellence and performance quality
- Entertainment satisfaction and enjoyment
- Emotional resonance and impact
- Overall directorial/technical competence

**Dissatisfied viewers** discuss:
- Acting failures and miscasting
- Plot structure problems and narrative confusion
- Directorial missteps and poor pacing
- Dialogue/script quality and character shallowness
- Technical failures (effects, cinematography)

## Notable Exceptions

- **Visual Quality**: Mentioned at similar rates (8.1% vs. 9.4%), suggesting both positive and negative reviewers engage with production values, but frame them differently.
- **General Category**: Higher in positive reviews, indicating satisfied reviewers may default to broader approval language.
- **Dialogue Quality**: Gains salience in negative reviews, pointing to weak writing as a noticeable failure point.

## Conclusion

Positive and negative reviews differ fundamentally in *what they prioritize*: satisfied reviewers focus on **performance excellence and entertainment delivery**, while dissatisfied reviewers focus on **structural craft defects** (plot, dialogue, character development, direction). The 2x differential in positive sentiment word usage versus 4.5x differential in negative words confirms this pattern linguistically. Both sentiments engage acting as a primary theme, but frame it as either a strength or failure. Emotional resonance emerges as a key positive discriminator, appearing 1.6x more in satisfied reviews, suggesting reviewers' emotional engagement is central to satisfaction.
