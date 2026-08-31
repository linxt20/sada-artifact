import pandas as pd
import re

df = pd.read_csv('input.csv')

# Extract text length (reviews with more detail may indicate stronger opinions)
df['review_text_length'] = df['Text'].fillna('').str.len()

# Extract summary length
df['summary_length'] = df['Summary'].fillna('').str.len()

# Count exclamation marks (intensity indicator)
df['exclamation_count'] = df['Text'].fillna('').str.count('!')

# Count positive sentiment words
positive_words = ['excellent', 'amazing', 'love', 'great', 'perfect', 'best', 'wonderful', 'delicious', 'fantastic', 'awesome']
def count_words(text, words):
    text_lower = str(text).lower()
    return sum(text_lower.count(word) for word in words)

df['positive_words_count'] = df['Text'].fillna('').apply(lambda x: count_words(x, positive_words))

# Count negative sentiment words
negative_words = ['terrible', 'awful', 'hate', 'bad', 'poor', 'worst', 'horrible', 'disgusting', 'waste']
df['negative_words_count'] = df['Text'].fillna('').apply(lambda x: count_words(x, negative_words))

# Helpfulness ratio (when denominator > 0)
df['helpfulness_ratio'] = df.apply(
    lambda row: row['HelpfulnessNumerator'] / row['HelpfulnessDenominator']
    if row['HelpfulnessDenominator'] > 0 else 0,
    axis=1
)

# Satisfaction proxy: ratio of positive to (positive + negative) words
df['sentiment_score'] = df.apply(
    lambda row: (row['positive_words_count'] - row['negative_words_count'])
    if (row['positive_words_count'] + row['negative_words_count']) > 0 else 0,
    axis=1
)

# High quality review indicator: combines length, helpfulness, and sentiment balance
df['review_quality'] = (
    (df['review_text_length'] > df['review_text_length'].median()).astype(int) * 0.33 +
    (df['helpfulness_ratio'] > df['helpfulness_ratio'].median()).astype(int) * 0.33 +
    (df['sentiment_score'] >= 0).astype(int) * 0.34
)

# Product rating consistency: boolean if score >= 4
df['high_satisfaction'] = (df['Score'] >= 4).astype(int)

# Write augmented CSV with all columns
df.to_csv('augment.csv', index=False)
print(f"Augmented table written to augment.csv with {len(df)} rows and {len(df.columns)} columns")
print(f"New columns added: {len(df.columns) - 10}")  # Original has 10 columns
print("\nNew columns:")
for col in df.columns[10:]:
    print(f"  - {col}")
