import pandas as pd
import re

df = pd.read_csv("input.csv")

def product_info_score(text):
    """Score how much detailed product information is in the review text."""
    if not isinstance(text, str):
        return 0
    text_lower = text.lower()

    # Product attribute mentions: ingredients, nutrition, dimensions, specs
    attribute_patterns = [
        r'\b(ingredient|contain|made (from|with|of)|composition)\b',
        r'\b(calorie|protein|fat|carb|sodium|fiber|sugar|vitamin|mineral|nutrient)\b',
        r'\b(size|weight|dimension|ounce|oz\b|pound|lb\b|gram|kg|ml|liter|gallon|quart)\b',
        r'\b(flavor|taste|texture|smell|aroma|consistency|color|colour)\b',
        r'\b(package|packaging|label|bottle|can|bag|box|container|seal)\b',
        r'\b(price|cost|value|expensive|cheap|afford|deal|discount)\b',
        r'\b(brand|manufacturer|company|product line|series|version|edition)\b',
        r'\b(organic|natural|artificial|preservative|additive|gmo|gluten|dairy|vegan)\b',
        r'\b(expir|shelf life|fresh|stale|date)\b',
        r'\b(comparison|compar|versus|vs\.?|alternative|similar|different|better than|worse than)\b',
    ]

    score = 0
    for pattern in attribute_patterns:
        if re.search(pattern, text_lower):
            score += 1

    # Bonus for specific measurements or numbers with units
    if re.search(r'\d+\s*(oz|lb|g|kg|ml|l\b|mg|kcal|cal)', text_lower):
        score += 1

    # Bonus for quoting product specs or label info
    if re.search(r'(says|states|claims|advertised|listed|labeled|description)', text_lower):
        score += 1

    return score

def product_info_detail_level(score):
    """Categorize detail level."""
    if score == 0:
        return "none"
    elif score <= 2:
        return "low"
    elif score <= 4:
        return "medium"
    else:
        return "high"

combined_text = df["Summary"].fillna("") + " " + df["Text"].fillna("")

df["product_info_score"] = combined_text.apply(product_info_score)
df["product_info_detail_level"] = df["product_info_score"].apply(product_info_detail_level)

# Counterfactual: estimated HelpfulnessNumerator if review had high product detail
# Based on the correlation between detail score and helpfulness in the dataset
# We compute average helpfulness rate per detail level (among reviews with votes)
has_votes = df[df["HelpfulnessDenominator"] > 0].copy()
has_votes["helpfulness_rate"] = has_votes["HelpfulnessNumerator"] / has_votes["HelpfulnessDenominator"]

# Average helpfulness rate by detail level
avg_by_level = has_votes.groupby("product_info_detail_level")["helpfulness_rate"].mean()

# For counterfactual: what would HelpfulnessNumerator be if detail_level were "high"
# We estimate by scaling: counterfactual_numerator = HelpfulnessDenominator * avg_rate_high
high_rate = avg_by_level.get("high", avg_by_level.max())

def counterfactual_numerator(row):
    denom = row["HelpfulnessDenominator"]
    if denom == 0:
        # No votes yet; use observed detail score to estimate expected votes
        # Assume 1 vote expected for reviews with detail, 0 otherwise
        return 1.0 * high_rate if row["product_info_score"] > 0 else high_rate
    return round(denom * high_rate, 2)

df["counterfactual_helpfulness_numerator_high_detail"] = df.apply(counterfactual_numerator, axis=1)

# Delta: counterfactual minus actual
df["helpfulness_numerator_delta_if_high_detail"] = (
    df["counterfactual_helpfulness_numerator_high_detail"] - df["HelpfulnessNumerator"]
).round(2)

df.to_csv("augment.csv", index=False)
print("Done. Shape:", df.shape)
print("\nDetail level distribution:")
print(df["product_info_detail_level"].value_counts())
print("\nAvg helpfulness rate by detail level:")
print(avg_by_level.round(4))
print("\nHigh detail rate used for counterfactual:", round(high_rate, 4))
print("\nSample delta stats:")
print(df["helpfulness_numerator_delta_if_high_detail"].describe())
