---
dataset: amazon_fine_food_review
scenario: predictive_score_features
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: predictive_feature_engineering
focus_variable: "review_score"
query: "What features can be extracted to train a model to predict a review's score?"
source_table: augment_table/amazon_fine_food_review/predictive_score_features/original.csv
source_report: dataset_portion_2/substrate-claude-sonnet-4-6/amazon_fine_food_review__predictive_score_features/analyses/original/analysis.md
wall_seconds: 66.11
---

# Feature Extraction for Predicting Amazon Fine Food Review Score

## Dataset Overview

The dataset is the **Amazon Fine Food Reviews** corpus. The visible columns are:

| Column | Type | Description |
|--------|------|-------------|
| `Id` | Integer | Row identifier |
| `ProductId` | String | Amazon product ASIN |
| `UserId` | String | Reviewer's user ID |
| `ProfileName` | String | Reviewer's display name |
| `HelpfulnessNumerator` | Integer | Number of users who found the review helpful |
| `HelpfulnessDenominator` | Integer | Total users who voted on helpfulness |
| `Score` | Integer (1–5) | **Target variable** — star rating |
| `Time` | Unix timestamp | Date review was posted |
| `Summary` | String | Short title of the review |
| `Text` | String | Full review body |

The target variable is **`Score`** (1–5 stars). A wide score distribution is visible in the sample: scores of 1, 2, 3, 4, and 5 all appear, though 5-star reviews appear most frequently, consistent with known positive-bias in voluntary review datasets.

---

## Extractable Feature Groups

### 1. Text-Based Features (from `Text` and `Summary`)

These are the richest source of signal:

- **Bag-of-Words / TF-IDF**: Word frequency vectors from `Text` and/or `Summary`. High-signal words like "terrible," "mushy," "stale," "delicious," "love," "great" co-occur strongly with extreme scores (1 or 5).
- **Sentiment scores**: Pre-trained lexicon-based (VADER, AFINN) or model-based (transformer) sentiment polarity scores. Reviews with score=1 use negative language ("nasty," "no flavor," "don't like it," "terrible diarrhea") while score=5 reviews use positive language ("wonderful," "amazing," "love," "best ever").
- **Review length** (character/word count of `Text`): Longer, more detailed reviews may correlate with extreme or more considered scores.
- **Summary length** and **sentiment of Summary**: The one-line title often directly encodes sentiment ("Stale product," "Great!," "Cough Medicine").
- **Presence of negations**: "not," "never," "disappointing" shift polarity.
- **Exclamation marks / punctuation count**: Enthusiasm markers common in 5-star reviews.
- **All-caps ratio**: Observed in some low-scoring reviews ("NASTY," "I WAS VISITING") as well as some enthusiastic 5-star reviews.
- **Use of HTML tags** (`<br />`): Signals a longer/structured review; may weakly correlate with helpfulness and moderate scores.
- **Word embeddings / dense text representations**: Word2Vec, GloVe, or sentence transformers applied to `Text` for semantic classification.

### 2. Helpfulness Features (from `HelpfulnessNumerator` / `HelpfulnessDenominator`)

- **Raw helpfulness numerator**: Reviews with more helpful votes may be more informative/extreme.
- **Helpfulness ratio** = `HelpfulnessNumerator / HelpfulnessDenominator` (where denominator > 0): Proportion of voters finding the review useful. High-helpfulness reviews with score=1 (e.g., Row 33: 19/19 helpful, score=4; Row 51: 0/7 helpful, score=1) show this ratio varies independently of score.
- **Denominator (total votes)**: Proxy for review popularity/visibility.
- **Note**: Many rows have denominator=0, making the ratio undefined. This is a data sparsity issue and these rows may need to be treated as a separate category (e.g., `never_voted = True`).

### 3. Temporal Features (from `Time`)

- **Review timestamp** (Unix → calendar date): Decoded as year, month, day of week.
- **Seasonal patterns**: May reflect holiday buying spikes.
- **Recency**: Older vs. newer reviews—product quality may shift over time (e.g., formula changes triggering low-score waves, as seen in rows 12–14 for Felidae Platinum).
- **Weak evidence**: Temporal features alone are unlikely to be strong predictors but may add marginal value as auxiliary signals.

### 4. User-Level Features (from `UserId`, `ProfileName`)

- **User mean score**: Reviewer-level average historical score — a strong prior if a user consistently rates high or low.
- **User review count**: Prolific reviewers may show distinct tendencies.
- **Caveat**: These are identity-based features that may not generalize to cold-start users.

### 5. Product-Level Features (from `ProductId`)

- **Product mean score**: Average rating across all reviews for the same product.
- **Product review count**: More-reviewed products may have more stable score distributions.
- **Product score variance**: High variance products suggest divided opinions (e.g., spicy foods in rows 54–55, 69, 130–132).
- **Caveat**: Also a cold-start problem for new products.

---

## Key Patterns Observed

- **Sentiment in `Summary` is highly predictive**: Summaries like "Stale product" → Score=1; "Best ever" → Score=5; "Not as Advertised" → Score=1. Short title sentiment aligns with full score in the overwhelming majority of visible rows.
- **Extreme language in `Text`**: Reviews scoring 1 contain language of complaint, disappointment, or harm ("terrible diarrhea," "so stale I could not eat any," "no flavor at all"). Score=5 reviews contain superlatives and recommendation language ("highly recommend," "you will never want to use any other").
- **Helpfulness ratio is noisy**: Some score=1 reviews have high helpfulness (Row 51: 0/7 = 0.0 helpfulness, score=1; Row 33: score=4, 19/19 helpful). Helpfulness and score are not redundant.
- **Score=3 reviews often express ambivalence**: "It is okay," "mushy," "same as other brands," "could take it up a notch" — moderate language provides distinct signal from 1 or 5.

---

## Recommended Feature Priority

| Priority | Feature | Rationale |
|----------|---------|-----------|
| ⭐⭐⭐ | TF-IDF / Embeddings on `Text` | Core semantic signal |
| ⭐⭐⭐ | Sentiment score on `Text` + `Summary` | Strongly aligned with Score |
| ⭐⭐ | `Summary` text features | Short, often explicit sentiment |
| ⭐⭐ | Helpfulness ratio (when denominator > 0) | Independent proxy for review quality |
| ⭐⭐ | Product-level mean score | Strong contextual prior |
| ⭐ | User-level mean score | Useful but cold-start limited |
| ⭐ | Temporal features | Weak signal; marginal utility |
| ⭐ | Review length | Correlates loosely with engagement |

---

## Important Caveats

- **Class imbalance**: Score=5 is visually dominant; any model should account for class weighting or resampling.
- **Leakage risk**: Helpfulness votes and product/user aggregates are computed from the full dataset and must be split carefully to avoid data leakage.
- **Cold-start**: User-level and product-level features require historical data and will be unavailable for new users/products at inference time.
- **`HelpfulnessDenominator = 0`** for many rows (i.e., no one voted) — helpfulness ratio must be handled with a fallback or imputed.
- **Text quality varies widely**: Some reviews are a single sentence; others are multi-paragraph essays. Feature extraction must be robust to this range.
