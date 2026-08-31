---
dataset: amazon_fine_food_review
scenario: focus_inference
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's in these food-product reviews and what's worth attention or actionable."
source_table: augment_table/amazon_fine_food_review/focus_inference/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:00:58.433833+00:00
wall_seconds: 48.99
---

# Amazon Fine Food Reviews — Analysis Report

## Dataset Overview

| Dimension | Value |
|---|---|
| Total reviews | 10,000 |
| Columns | 17 (raw + 7 augmented features) |
| Star-score range | 1–5 |
| Date of analysis | 2026-07-28 |

Augmented features of interest: `sentiment_label`, `helpfulness_ratio`, `review_length_bucket`, `issue_flags`, `repeat_buy_signal`, `exclamation_count`, `caps_ratio`.

---

## 1. Rating & Sentiment Distribution

The corpus is **heavily positive**: 5-star reviews account for **61.8 %** of all reviews, and 4-star add another 14.3 %. Combined, 76 % of reviews carry a positive sentiment label.

| Score | Count | % |
|---|---|---|
| 5 | 6,183 | 61.8 % |
| 4 | 1,433 | 14.3 % |
| 3 | 862 | 8.6 % |
| 2 | 590 | 5.9 % |
| 1 | 932 | 9.3 % |

> **Note:** `sentiment_label` maps perfectly onto score bands (1–2 → negative, 3 → neutral, 4–5 → positive), so it adds no independent signal beyond the numeric score. Both columns are effectively redundant for further modeling.

---

## 2. What Issues Are Driving Negative Reviews?

`issue_flags` is a multi-label field. Across all 10,000 reviews **taste dominates every issue combination**:

- **`taste`** appears in the flags of ~7,600+ reviews (as sole or co-occurring flag).
- Among 1–2 star reviews specifically, `taste` is the single most common flag (467 out of 1,522 negative reviews), followed by `none` (192 — no flagged issue despite low score) and `taste|repeat_buy` (121).
- **Shipping** complaints appear in ~1,000 reviews total, concentrated in negative/neutral bands.
- **Quality** flags are meaningful but less frequent (~950 total).
- **Value** flags cluster in mid-to-low scores.

**Actionable:** Taste dissatisfaction is the primary driver of low ratings and is consistently co-flagged with other issues. Products with `shipping|taste` co-flags may indicate fulfillment damage affecting perceived taste — worth investigating separately.

---

## 3. Repeat-Buy Signal

Somewhat counter-intuitively, **repeat-buy signals are slightly higher in low-rating reviews** (23.6 % for 1-star, 23.2 % for 2-star) than in 5-star reviews (17.1 %).

This likely reflects reviewers who *previously* bought the product loyally and are now disappointed — a high-churn-risk segment. The 1-star + repeat-buy combination (~220 reviews) represents customers who gave up after initial loyalty and is a priority group for retention analysis.

---

## 4. Helpfulness Ratio

Only **5,122 of 10,000 reviews** have a non-null helpfulness ratio (the rest received zero votes). Among those rated:

| Sentiment | Mean helpfulness ratio |
|---|---|
| Positive | **0.856** |
| Neutral | 0.597 |
| Negative | 0.551 |

Positive reviews are rated more helpful by readers. However, among highly helpful reviews (ratio ≥ 0.8), **negative and neutral reviews still make up ~16 %** (375 of 2,469). These are the most credible critical voices in the corpus and warrant qualitative attention for product improvement signals.

---

## 5. Review Length

Most reviews are **medium-length** (6,523; ~65 %), with long reviews at 32 % and short at only 2.8 %. Short reviews skew toward extremes (very positive or very negative with little nuance) — less useful for diagnostic purposes.

---

## 6. Stylistic Signals (Caps & Exclamations)

- **Exclamation count:** Mean 0.73, median 0; highly skewed. A small set of reviews (high-exclamation outliers, max = 32) are likely emotionally charged.
- **Caps ratio > 0.15:** Only 129 reviews (~1.3 %). These are candidates for shouting/emphasis in complaints or enthusiasm — a minor but filterable noise source.

---

## 7. Key Takeaways & Recommended Actions

| Priority | Finding | Action |
|---|---|---|
| 🔴 High | Taste is the #1 complaint flag across all negative reviews | Prioritize product taste/formulation reviews; flag affected ProductIds |
| 🔴 High | Repeat buyers leaving 1–2 star reviews (~220 reviews) | Investigate product quality changes or fulfillment issues over time |
| 🟡 Medium | ~1,000 negative reviews with no issue flag (`none`) | Manual review or re-labeling; may contain implicit quality/service issues |
| 🟡 Medium | Shipping co-flags in negative reviews (~1,000 total) | Logistics/packaging review, especially for taste-sensitive products |
| 🟢 Low | High-helpfulness negative reviews (375 reviews) | Use as seed set for product improvement qualitative analysis |
| 🟢 Low | Sentiment label is score-redundant | Drop from feature engineering; use `Score` directly |

> **Caveat:** `helpfulness_ratio` has a 49 % missingness rate (zero-vote reviews), so helpfulness-based conclusions apply only to the rated subset and may not generalize to the full corpus.
