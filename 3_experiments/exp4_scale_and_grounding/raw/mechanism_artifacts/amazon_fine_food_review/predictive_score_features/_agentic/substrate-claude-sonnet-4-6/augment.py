import pandas as pd
import re

df = pd.read_csv("input.csv")

# 1. Review text length
df["text_length"] = df["Text"].fillna("").apply(len)

# 2. Word count in review text
df["word_count"] = df["Text"].fillna("").apply(lambda x: len(x.split()))

# 3. Helpfulness ratio (NaN-safe; 0 when denominator is 0)
df["helpfulness_ratio"] = df.apply(
    lambda r: r["HelpfulnessNumerator"] / r["HelpfulnessDenominator"]
    if r["HelpfulnessDenominator"] > 0 else 0.0,
    axis=1,
)

# 4. Summary length
df["summary_length"] = df["Summary"].fillna("").apply(len)

# 5. Exclamation mark count in text (enthusiasm signal)
df["exclamation_count"] = df["Text"].fillna("").apply(lambda x: x.count("!"))

# 6. Question mark count in text (uncertainty/complaint signal)
df["question_count"] = df["Text"].fillna("").apply(lambda x: x.count("?"))

# 7. Uppercase word ratio (shouting / emphasis)
def uppercase_ratio(text):
    words = text.split()
    if not words:
        return 0.0
    upper = sum(1 for w in words if w.isupper() and len(w) > 1)
    return upper / len(words)

df["uppercase_ratio"] = df["Text"].fillna("").apply(uppercase_ratio)

# 8. Contains positive keywords
positive_words = {"great", "excellent", "amazing", "love", "best", "wonderful",
                  "fantastic", "delicious", "perfect", "awesome"}
def positive_keyword_count(text):
    tokens = re.findall(r"[a-z]+", text.lower())
    return sum(1 for t in tokens if t in positive_words)

df["positive_keyword_count"] = df["Text"].fillna("").apply(positive_keyword_count)

# 9. Contains negative keywords
negative_words = {"terrible", "horrible", "awful", "worst", "bad", "disgusting",
                  "disappointed", "disappointing", "poor", "waste"}
def negative_keyword_count(text):
    tokens = re.findall(r"[a-z]+", text.lower())
    return sum(1 for t in tokens if t in negative_words)

df["negative_keyword_count"] = df["Text"].fillna("").apply(negative_keyword_count)

# 10. Year extracted from Unix timestamp
df["review_year"] = pd.to_datetime(df["Time"], unit="s").dt.year

df.to_csv("augment.csv", index=False)
print("Done. Shape:", df.shape)
print("New columns:", df.columns.tolist()[9:])
