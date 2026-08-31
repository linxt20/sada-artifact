---
dataset: amazon_fine_food_review
scenario: predictive_score_features
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "review_score"
query: "What features can be extracted to train a model to predict a review's score?"
source_table: augment_table/amazon_fine_food_review/predictive_score_features/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:01:12.225814+00:00
wall_seconds: 52.89
---

# Predictive Features for Amazon Fine Food Review Score Prediction

## Overview
This analysis identifies extractable features to train a model predicting a review's score (1-5 rating) in the Amazon Fine Food Reviews dataset. The dataset contains 10,000 reviews with 21 total features, including original metadata and derived linguistic features.

## Score Distribution
The target variable (Score) is heavily skewed toward positive ratings:
- **Score 5**: 6,183 reviews (61.8%)
- **Score 4**: 1,433 reviews (14.3%)
- **Score 3**: 862 reviews (8.6%)
- **Score 2**: 590 reviews (5.9%)
- **Score 1**: 932 reviews (9.3%)

Mean score: 4.13 (SD: 1.33)

## Primary Predictive Features

### 1. **Sentiment Polarity Features** (Strongest Predictors)
- **Negative word count** (|r| = 0.333): Strong inverse relationship; low-score reviews average 1.77 negative words (Score 1) vs. 0.56 for high-score reviews (Score 5)
- **Positive word count** (|r| = 0.261): Moderate positive relationship; high-score reviews average 1.90 positive words (Score 5) vs. 0.76 for low-score reviews (Score 1)
- **Positive-to-negative ratio**: Clear separation by score; Score 1 reviews show 0.31 ratio vs. 1.45 for Score 5

**Implication**: Text sentiment composition is the strongest discriminator for score prediction.

### 2. **Review Verbosity Features** (Moderate Predictors)
- **Question mark count** (|r| = 0.121): Higher in negative reviews; Score 1 averages 0.23 question marks vs. 0.06 for Score 5
- **Text length / Word count** (|r| = 0.100): Slight inverse relationship; longer reviews tend to have lower scores
  - Score 1-3: ~88-95 words average
  - Score 5: ~72 words average

**Implication**: Users expressing doubt or uncertainty (via questions) and lengthier complaints correlate with lower scores.

### 3. **Emphasis and Tone Markers** (Weak Predictors)
- **Capitalized word count** (|r| = 0.092): Slight inverse relationship; suggests emphasis in critical reviews
- **Exclamation count** (|r| = 0.082): Non-linear; both very negative and very positive reviews use more exclamations

**Implication**: Capitalization patterns suggest urgency in complaints; exclamation usage is ambiguous without sentiment context.

### 4. **Auxiliary Features** (Limited Predictive Value)
- **Avg word length** (r = 0.015): Minimal relationship
- **Has product mention** (r = 0.022): Not predictive of score
- **Helpfulness ratio** (r = 0.034): Weak signal; Score 1 reviews slightly more helpful (0.403) than Score 3 (0.322)

## Important Limitations and Caveats

### Weak Evidence
The strongest feature (negative_word_count) explains only ~11% of score variance ($r^2 = 0.11$). Combined, all engineered linguistic features explain <15% of variance, indicating:
1. **Score determination is multidimensional**: Product quality, personal expectations, and subjective experience dominate over textual features
2. **Feature interactions likely matter**: Sentiment polarity + review length combinations may be more predictive than individual features
3. **No augmented semantic features**: The dataset lacks sophisticated semantic annotations (sentiment intensity, aspect-based sentiment, complaint types) present in the ground truth schema but not implemented in this variant

### Data Skew Bias
The severe class imbalance (61.8% 5-star reviews) means any model must address:
- Inherent difficulty discriminating positive vs. neutral (Score 4-5)
- Natural tendency toward majority class prediction

### Text-Based Limitations
- Reliance on lexicon-based features (positive/negative word lists) is prone to context misses
- Sarcasm, qualifications ("decent for the price"), and domain-specific food terminology are not captured
- Profile name, user ID, and time features provide limited evidence independent of review text

## Recommended Feature Engineering Strategy

### High Priority (Strong Discriminative Value)
1. Sentiment score (lexicon-based or neural)
2. Aspect-based sentiment extraction (taste, freshness, value, delivery)
3. Complaint type classification (quality, mislabeling, safety, value)
4. Emotion intensity (strong vs. mild sentiment)

### Medium Priority (Supporting Features)
5. Hedge language detection (tentative language: "seem," "might," "somewhat")
6. Recommendation intent signal (repurchase language)
7. Review-to-summary coherence
8. Product mention patterns (what products are praised/criticized)

### Low Priority (Exploratory Value)
9. User review history statistics (is this reviewer consistently harsh?)
10. Temporal patterns (seasonal products, price changes)
11. Review length normalized by sentiment

## Conclusion

The visible feature set provides **moderate predictive signals** for score prediction, with **sentiment polarity being the strongest and most reliable indicator**. However, the low correlation magnitudes suggest that effective score prediction requires either:
- Deeper semantic feature extraction (aspects, complaint types, intensity levels as specified in augmentation schema)
- Multi-modal approaches incorporating non-text signals (product metadata, user history)
- Supervised feature selection with machine learning to identify feature interactions

The dataset's heavy positive skew (62% 5-star) necessitates stratified evaluation and class-weighted training approaches.
