import pandas as pd
import re
from pathlib import Path

# Quality facet keywords
facets = {
    'taste_flavor': ['taste', 'flavor', 'flavour', 'delicious', 'yummy', 'bland', 'sweet', 'salty', 'sour', 'bitter', 'medicinal'],
    'texture': ['texture', 'chewy', 'soft', 'crispy', 'crunchy', 'firm', 'mushy', 'sticky', 'smooth'],
    'freshness': ['fresh', 'stale', 'quality', 'condition', 'expired', 'old', 'new'],
    'packaging': ['packaging', 'wrapped', 'pack', 'box', 'bottle', 'container', 'damaged', 'securely packed'],
    'value_price': ['price', 'value', 'deal', 'expensive', 'cheap', 'cost', 'worth'],
    'health_nutrition': ['healthy', 'nutritious', 'diet', 'calories', 'protein', 'ingredient', 'natural', 'organic', 'digestive'],
    'product_variety': ['variety', 'assortment', 'flavors', 'flavours', 'selection', 'different'],
    'consistency_reliability': ['consistent', 'reliable', 'always', 'every time', 'expected'],
    'comparison_brand': ['brand', 'compared', 'better', 'worse', 'expensive brand', 'premium'],
    'delivery_service': ['delivery', 'shipping', 'arrived', 'received', 'fast', 'quick', 'order']
}

def extract_facets(text):
    """Extract which quality facets are mentioned in the review text."""
    if not isinstance(text, str):
        return {facet: False for facet in facets.keys()}

    text_lower = text.lower()
    result = {}

    for facet, keywords in facets.items():
        # Check if any keyword for this facet appears in the text
        result[facet] = any(keyword in text_lower for keyword in keywords)

    return result

# Read the input CSV
input_path = Path('/Users/wangzhuo/Documents/MSRA/SADA/benchmark/augment_table/amazon_fine_food_review/concept_food_quality_facets/_agentic/substrate-claude-haiku-4-5/input.csv')
df = pd.read_csv(input_path)

# Extract facets for each review
print("Extracting quality facets from reviews...")
facet_data = df['Text'].apply(extract_facets)

# Create columns for each facet
for facet in facets.keys():
    df[f'facet_{facet}'] = facet_data.apply(lambda x: x[facet])

# Convert boolean to int for cleaner output
for facet in facets.keys():
    df[f'facet_{facet}'] = df[f'facet_{facet}'].astype(int)

# Write to augment.csv
output_path = Path('/Users/wangzhuo/Documents/MSRA/SADA/benchmark/augment_table/amazon_fine_food_review/concept_food_quality_facets/_agentic/substrate-claude-haiku-4-5/augment.csv')
df.to_csv(output_path, index=False)

print(f"Successfully created augment.csv with {len(df)} rows and {len(df.columns)} columns")
print(f"Added {len(facets)} quality facet columns:")
for facet in facets.keys():
    count = df[f'facet_{facet}'].sum()
    print(f"  - facet_{facet}: {count} reviews mention this aspect")
