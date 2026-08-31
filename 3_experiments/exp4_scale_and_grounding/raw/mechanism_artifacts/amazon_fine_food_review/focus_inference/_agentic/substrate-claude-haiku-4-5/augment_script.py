import pandas as pd
import re

df = pd.read_csv('input.csv')

# 1. Review Length: longer reviews often contain more actionable detail
df['review_length'] = df['Text'].fillna('').apply(len)

# 2. Sentiment (derived from Score): groups reviews into positive/neutral/negative
def categorize_sentiment(score):
    if score >= 4:
        return 'Positive'
    elif score == 3:
        return 'Neutral'
    else:
        return 'Negative'

df['sentiment'] = df['Score'].apply(categorize_sentiment)

# 3. Helpfulness Ratio: reviews marked helpful by readers are often more actionable/informative
df['helpfulness_ratio'] = df.apply(
    lambda row: round(row['HelpfulnessNumerator'] / row['HelpfulnessDenominator'], 2)
    if row['HelpfulnessDenominator'] > 0 else 0.0,
    axis=1
)

# 4. Has Criticism or Issue: text contains common complaint keywords
criticism_keywords = [
    'not', 'poor', 'bad', 'broken', 'defect', 'problem', 'issue', 'fail',
    'disappointed', 'waste', 'useless', 'wrong', 'complaint', 'damage',
    'disappointed', 'disappoint', 'never', 'don\'t like', 'doesn\'t work',
    'quality', 'mislead', 'false', 'error', 'mistake'
]

def has_criticism(text):
    if pd.isna(text):
        return False
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in criticism_keywords)

df['has_criticism'] = df['Text'].apply(has_criticism)

# 5. Engagement Level: based on text and summary length combined
df['engagement_level'] = df.apply(
    lambda row: 'High' if (pd.notna(row['Text']) and len(row['Text']) > 500)
                else ('Medium' if (pd.notna(row['Text']) and len(row['Text']) > 150) else 'Low'),
    axis=1
)

# Write the augmented dataset
df.to_csv('augment.csv', index=False)

print(f"Augmented dataset written to augment.csv")
print(f"Original columns: {len(df.columns) - 5}")
print(f"New columns added: 5")
print(f"Total rows: {len(df)}")
print("\nNew columns:")
print("  - review_length: Character count of review text")
print("  - sentiment: Positive/Neutral/Negative based on score")
print("  - helpfulness_ratio: Proportion of readers who found review helpful")
print("  - has_criticism: Boolean flag for presence of complaint language")
print("  - engagement_level: Low/Medium/High based on review length")
