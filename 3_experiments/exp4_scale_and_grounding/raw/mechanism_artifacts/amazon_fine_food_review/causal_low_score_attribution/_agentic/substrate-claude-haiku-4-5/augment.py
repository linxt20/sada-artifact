import pandas as pd
import numpy as np
import re

df = pd.read_csv('input.csv')

# 1. Text length features
df['summary_length'] = df['Summary'].fillna('').str.len()
df['text_length'] = df['Text'].fillna('').str.len()

# 2. Negative word indicators (common complaint patterns)
negative_keywords = [
    'broken', 'damaged', 'defective', 'not work', 'disappointed', 'waste',
    'terrible', 'horrible', 'awful', 'bad', 'poor', 'useless', 'cheap',
    'taste bad', 'doesn\'t work', 'stopped working', 'fell apart',
    'tastes bad', 'not fresh', 'stale', 'expired', 'moldy', 'dirty',
    'missing', 'incorrect', 'wrong', 'not as advertised', 'misleading'
]
negative_pattern = '|'.join(negative_keywords)
df['has_negative_words'] = df['Text'].fillna('').str.lower().str.contains(
    negative_pattern, regex=True, na=False
).astype(int)

# 3. Quality/positive word indicators
positive_keywords = [
    'great', 'excellent', 'love', 'amazing', 'wonderful', 'fantastic',
    'perfect', 'best', 'highly recommend', 'satisfied', 'happy', 'delighted',
    'fresh', 'quality', 'good', 'tasty', 'yummy', 'delicious'
]
positive_pattern = '|'.join(positive_keywords)
df['has_positive_words'] = df['Text'].fillna('').str.lower().str.contains(
    positive_pattern, regex=True, na=False
).astype(int)

# 4. Helpfulness ratio (when denominator > 0)
df['helpfulness_ratio'] = np.where(
    df['HelpfulnessDenominator'] > 0,
    df['HelpfulnessNumerator'] / df['HelpfulnessDenominator'],
    np.nan
)
# Fill NaN with 0 (no votes) for consistency
df['helpfulness_ratio'] = df['helpfulness_ratio'].fillna(0)

# 5. Contains comparison/complaint structure (e.g., "but", "however", "unfortunately")
df['has_complaint_markers'] = df['Text'].fillna('').str.lower().str.contains(
    r'(but |however|unfortunately|instead|only problem|didn\'t|not|complaint)',
    regex=True, na=False
).astype(int)

# 6. Uppercase usage (aggressive tone indicator)
def uppercase_ratio(text):
    text = str(text) if pd.notna(text) else ''
    if len(text) == 0:
        return 0
    letters = sum(1 for c in text if c.isalpha())
    if letters == 0:
        return 0
    uppercase = sum(1 for c in text if c.isupper())
    return uppercase / letters

df['uppercase_ratio'] = df['Text'].apply(uppercase_ratio)

# 7. Exclamation mark density (passion indicator)
df['exclamation_count'] = df['Text'].fillna('').str.count('!')
df['question_count'] = df['Text'].fillna('').str.count(r'\?')

# 8. Is low score (binary indicator)
df['is_low_score'] = (df['Score'] <= 2).astype(int)

# Save the augmented CSV
df.to_csv('augment.csv', index=False)
print(f"Augmented CSV created with {len(df)} rows and {len(df.columns)} columns")
print(f"New columns added: {len(df.columns) - 13}")
print("Columns:", df.columns.tolist())
