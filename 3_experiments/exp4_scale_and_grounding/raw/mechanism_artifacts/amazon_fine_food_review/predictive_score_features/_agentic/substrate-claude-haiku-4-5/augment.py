import csv
import re
from collections import defaultdict

def extract_features(row):
    summary = row['Summary'].strip()
    text = row['Text'].strip()
    helpfulness_num = float(row['HelpfulnessNumerator'])
    helpfulness_denom = float(row['HelpfulnessDenominator'])

    features = {}

    # 1. Text length (longer reviews tend to have more detail)
    features['text_length'] = len(text)

    # 2. Summary length
    features['summary_length'] = len(summary)

    # 3. Exclamation mark count (enthusiasm indicator)
    features['exclamation_count'] = text.count('!')

    # 4. Sentiment lexicon indicators
    positive_words = {
        'good', 'great', 'excellent', 'amazing', 'wonderful', 'perfect', 'love', 'loved',
        'best', 'fantastic', 'awesome', 'brilliant', 'superb', 'delicious', 'highly',
        'recommend', 'satisfied', 'happy', 'impressed', 'fresh', 'quality', 'tasty'
    }
    negative_words = {
        'bad', 'poor', 'terrible', 'awful', 'hate', 'hated', 'waste', 'broken',
        'disappointing', 'disappointed', 'useless', 'worst', 'horrible', 'nasty',
        'disgusting', 'complaint', 'cheap', 'not', 'never', 'wouldn\'t'
    }

    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)

    positive_count = sum(1 for w in words if w in positive_words)
    negative_count = sum(1 for w in words if w in negative_words)

    features['positive_word_count'] = positive_count
    features['negative_word_count'] = negative_count

    # 5. Helpfulness ratio (if denominator > 0)
    if helpfulness_denom > 0:
        features['helpfulness_ratio'] = helpfulness_num / helpfulness_denom
    else:
        features['helpfulness_ratio'] = 0.0

    # 6. Word count in review text
    features['word_count'] = len(words)

    # 7. Average word length
    if words:
        features['avg_word_length'] = sum(len(w) for w in words) / len(words)
    else:
        features['avg_word_length'] = 0.0

    # 8. Question mark count (engagement/queries)
    features['question_mark_count'] = text.count('?')

    # 9. Capitalized words count (emphasis)
    capitalized = sum(1 for w in text.split() if w and w[0].isupper())
    features['capitalized_word_count'] = capitalized

    # 10. Contains product mention (product reference)
    product_id = row['ProductId'].strip()
    features['has_product_mention'] = 1 if product_id.lower() in text_lower else 0

    return features

def main():
    input_path = 'input.csv'
    output_path = 'augment.csv'

    with open(input_path, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)

    # Extract features for all rows
    all_features = []
    for row in rows:
        features = extract_features(row)
        all_features.append(features)

    # Get feature names (sorted for consistency)
    feature_names = sorted(all_features[0].keys()) if all_features else []

    # Write augmented CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = list(rows[0].keys()) + feature_names
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()
        for row, features in zip(rows, all_features):
            combined = {**row, **features}
            writer.writerow(combined)

    print(f"Augmented CSV written to {output_path}")
    print(f"Original columns: {len(rows[0])}")
    print(f"New feature columns added: {len(feature_names)}")
    print(f"Total rows: {len(rows)}")

if __name__ == '__main__':
    main()
