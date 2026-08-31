import pandas as pd
import re
import math

df = pd.read_csv("input.csv")

# ── 1. is_low_score: binary flag for scores 1-2 ──────────────────────────────
df["is_low_score"] = (df["Score"] <= 2).astype(int)

# ── 2. helpfulness_ratio: fraction of readers who found review helpful ────────
# 0 when nobody voted (denominator=0) to avoid NaN
df["helpfulness_ratio"] = df.apply(
    lambda r: r["HelpfulnessNumerator"] / r["HelpfulnessDenominator"]
    if r["HelpfulnessDenominator"] > 0 else 0.0,
    axis=1,
)

# ── 3. review_length: character count of the review text ─────────────────────
df["review_length"] = df["Text"].fillna("").str.len()

# ── 4. word_count: number of words in review text ────────────────────────────
df["word_count"] = df["Text"].fillna("").str.split().str.len()

# ── 5. has_exclamation: reviewer used exclamation marks (enthusiasm / anger) ──
df["has_exclamation"] = df["Text"].fillna("").str.contains("!").astype(int)

# ── 6. has_question: reviewer asked a question (confusion / complaint signal) ─
df["has_question"] = df["Text"].fillna("").str.contains(r"\?").astype(int)

# ── 7. negative_word_count: count of common negative sentiment words ──────────
NEG_WORDS = re.compile(
    r"\b(bad|terrible|awful|horrible|worst|disgusting|disappointed|disappoint|"
    r"disappointing|poor|defective|broken|waste|nasty|gross|disgusted|rotten|"
    r"stale|fake|wrong|mislead|misleading|false|not as described|expired|"
    r"mold|moldy|smell|smells|inedible|unacceptable|refund|return|never again|"
    r"do not buy|don't buy|avoid)\b",
    re.IGNORECASE,
)
df["negative_word_count"] = df["Text"].fillna("").apply(
    lambda t: len(NEG_WORDS.findall(t))
)

# ── 8. positive_word_count: count of common positive sentiment words ──────────
POS_WORDS = re.compile(
    r"\b(good|great|excellent|amazing|love|loved|loves|wonderful|fantastic|"
    r"perfect|best|delicious|tasty|recommend|recommended|happy|satisfied|"
    r"fresh|quality|superb|outstanding|awesome)\b",
    re.IGNORECASE,
)
df["positive_word_count"] = df["Text"].fillna("").apply(
    lambda t: len(POS_WORDS.findall(t))
)

# ── 9. sentiment_ratio: positive / (positive + negative + 1) ─────────────────
# Higher → more positive language; lower → more negative language
df["sentiment_ratio"] = (df["positive_word_count"] + 1) / (
    df["positive_word_count"] + df["negative_word_count"] + 2
)

# ── 10. summary_length: character count of the review summary ─────────────────
df["summary_length"] = df["Summary"].fillna("").str.len()

# ── 11. caps_ratio: fraction of alphabetic chars that are uppercase ────────────
# High caps ratio may indicate shouting / anger
def caps_ratio(text):
    text = str(text)
    alpha = [c for c in text if c.isalpha()]
    if not alpha:
        return 0.0
    return sum(1 for c in alpha if c.isupper()) / len(alpha)

df["caps_ratio"] = df["Text"].fillna("").apply(caps_ratio)

# ── 12. product_avg_score: mean score for that product across all reviews ──────
prod_avg = df.groupby("ProductId")["Score"].mean().rename("product_avg_score")
df = df.merge(prod_avg, on="ProductId", how="left")

# ── 13. user_avg_score: mean score given by that user across all reviews ───────
user_avg = df.groupby("UserId")["Score"].mean().rename("user_avg_score")
df = df.merge(user_avg, on="UserId", how="left")

# ── 14. score_vs_product_avg: how far this review deviates from product mean ───
# Negative value → reviewer rated it lower than typical for this product
df["score_vs_product_avg"] = df["Score"] - df["product_avg_score"]

# ── 15. reviewer_is_harsh: user whose personal average score is <= 2.5 ─────────
df["reviewer_is_harsh"] = (df["user_avg_score"] <= 2.5).astype(int)

df.to_csv("augment.csv", index=False)
print("Done. Shape:", df.shape)
print("Columns:", list(df.columns))
