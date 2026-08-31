import csv
import re

# Attribute keyword sets
ATTRIBUTE_PATTERNS = {
    "taste_flavor": re.compile(
        r"\b(taste|flavor|flavour|delicious|yummy|yum|bland|savory|sweet|sour|bitter|spicy|salty|rich|mild|strong|fresh|stale|good taste|great taste|bad taste|tastes? (good|great|bad|awful|amazing|terrible|wonderful|horrible))\b",
        re.IGNORECASE,
    ),
    "texture": re.compile(
        r"\b(texture|crunchy|crispy|chewy|soft|hard|smooth|gritty|mushy|tender|tough|fluffy|creamy)\b",
        re.IGNORECASE,
    ),
    "smell_aroma": re.compile(
        r"\b(smell|aroma|scent|odor|fragrance|stinks?|smells? (good|bad|great|awful|wonderful|terrible|nice|fresh|stale))\b",
        re.IGNORECASE,
    ),
    "quality": re.compile(
        r"\b(quality|fresh(ness)?|authentic|genuine|pure|natural|organic|real|fake|artificial|cheap|premium|high.?quality|low.?quality|good quality|great quality|poor quality|bad quality)\b",
        re.IGNORECASE,
    ),
    "packaging": re.compile(
        r"\b(packag(ing|ed|e)|container|bag|box|bottle|jar|can|seal(ed)?|wrap(ping)?|broken|damaged|leaking?|intact)\b",
        re.IGNORECASE,
    ),
    "value_price": re.compile(
        r"\b(price|cost|value|expensive|cheap|afford(able)?|worth|overpriced?|bargain|deal|money)\b",
        re.IGNORECASE,
    ),
    "ingredients": re.compile(
        r"\b(ingredient(s)?|contain(s)?|made (with|from|of)|additive(s)?|preservative(s)?|chemical(s)?|artificial|natural|organic|gmo|gluten|sugar|salt|fat|protein|calorie)\b",
        re.IGNORECASE,
    ),
    "health_nutrition": re.compile(
        r"\b(health(y)?|nutrition(al)?|diet(ary)?|calorie(s)?|vitamin(s)?|mineral(s)?|protein|fiber|fat|carb(s)?|sodium|allerg(y|ies|ic)?|diabetic|low.?fat|low.?sugar|low.?sodium|weight)\b",
        re.IGNORECASE,
    ),
    "size_quantity": re.compile(
        r"\b(size|quantity|amount|portion|serving|large|small|big|tiny|little|too (much|many|little|few)|not enough|plenty|generous|stingy)\b",
        re.IGNORECASE,
    ),
    "shipping_delivery": re.compile(
        r"\b(ship(ping|ped)?|deliver(y|ed|ing)?|arriv(e|al|ed|ing)|fast|slow|quick|late|damaged in|transit|package)\b",
        re.IGNORECASE,
    ),
}

# Positive/negative sentiment words for the review
POSITIVE_WORDS = re.compile(
    r"\b(love|great|excellent|amazing|wonderful|fantastic|perfect|best|awesome|superb|terrific|outstanding|highly recommend|delicious|good|nice|happy|pleased|satisfied|enjoy(ed)?|favourite|favorite)\b",
    re.IGNORECASE,
)
NEGATIVE_WORDS = re.compile(
    r"\b(hate|terrible|awful|horrible|worst|bad|poor|disappointed|disgusting|nasty|gross|never (again|buy)|waste|useless|broken|wrong|not good|not great)\b",
    re.IGNORECASE,
)


def count_matches(pattern, text):
    return len(pattern.findall(text))


def review_length_bucket(text):
    n = len(text.split())
    if n < 30:
        return "short"
    elif n < 100:
        return "medium"
    else:
        return "long"


input_path = "input.csv"
output_path = "augment.csv"

with open(input_path, newline="", encoding="utf-8") as fin, open(
    output_path, "w", newline="", encoding="utf-8"
) as fout:
    reader = csv.DictReader(fin)
    original_fields = reader.fieldnames

    new_fields = (
        list(original_fields)
        + ["mentioned_attributes"]          # comma-separated list of attribute categories mentioned
        + ["attribute_count"]               # total number of distinct attribute categories mentioned
        + [f"attr_{k}" for k in ATTRIBUTE_PATTERNS]  # binary flag per attribute category
        + ["positive_word_count"]           # count of positive sentiment words
        + ["negative_word_count"]           # count of negative sentiment words
        + ["sentiment_ratio"]               # positive / (positive + negative + 1) — skewed high for positive reviews
        + ["review_length_bucket"]          # short / medium / long review
    )

    writer = csv.DictWriter(fout, fieldnames=new_fields)
    writer.writeheader()

    for row in reader:
        combined_text = (row.get("Summary") or "") + " " + (row.get("Text") or "")

        attr_flags = {}
        mentioned = []
        for attr_name, pattern in ATTRIBUTE_PATTERNS.items():
            flag = 1 if pattern.search(combined_text) else 0
            attr_flags[f"attr_{attr_name}"] = flag
            if flag:
                mentioned.append(attr_name)

        pos = count_matches(POSITIVE_WORDS, combined_text)
        neg = count_matches(NEGATIVE_WORDS, combined_text)
        sentiment_ratio = round(pos / (pos + neg + 1), 4)

        row["mentioned_attributes"] = ";".join(mentioned) if mentioned else "none"
        row["attribute_count"] = len(mentioned)
        for k, v in attr_flags.items():
            row[k] = v
        row["positive_word_count"] = pos
        row["negative_word_count"] = neg
        row["sentiment_ratio"] = sentiment_ratio
        row["review_length_bucket"] = review_length_bucket(
            row.get("Text") or ""
        )

        writer.writerow(row)

print("Done. Written to augment.csv")
