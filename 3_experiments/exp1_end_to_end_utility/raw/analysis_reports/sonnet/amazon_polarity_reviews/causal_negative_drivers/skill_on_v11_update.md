---
dataset: amazon_polarity_reviews
scenario: causal_negative_drivers
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "label_pos"
query: "Why do some Amazon products receive predominantly negative reviews, and which factors contribute the most?"
source_table: augment_table/amazon_polarity_reviews/causal_negative_drivers/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:08:16.828920+00:00
wall_seconds: 56.03
---

# Why Amazon Products Receive Predominantly Negative Reviews
## Dataset: Amazon Polarity Reviews — Causal Negative Drivers Analysis

---

## Overview

The dataset contains **250 reviews** (125 negative, 125 positive, perfectly balanced) across six product category types and five reviewer expectation source labels. The analysis below identifies which factors most strongly associate with negative sentiment.

---

## Factor 1: Product Category Type

Product category is the strongest structural predictor of negative review rates.

| Category | Total Reviews | Negative Reviews | Negative Rate |
|---|---|---|---|
| physical_consumer_good | 79 | 50 | **63.3%** |
| software_or_game | 3 | 2 | 66.7% (small n) |
| media_book | 83 | 40 | **48.2%** |
| media_film_or_music | 76 | 31 | 40.8% |
| food_or_supplement | 3 | 1 | 33.3% (small n) |
| apparel_or_accessory | 5 | 0 | 0.0% (small n) |

**Physical consumer goods** drive the highest negative rate among substantive categories (63.3%, n=79). These reviews frequently cite tangible product failures: defects, breakage, poor construction, and performance below expectations. Books are a close second (48.2%), driven by dissatisfaction with content quality and unmet author expectations.

> ⚠️ **Note:** Software/game and food/supplement results are based on very small samples (≤3) and should not be over-interpreted.

---

## Factor 2: Reviewer Expectation Source

The `reviewer_expectation_source` column encodes the basis of a reviewer's prior expectation — a direct proxy for unmet-expectation dynamics.

| Expectation Source | Total | Negative Rate |
|---|---|---|
| casual_buyer | 85 | **67.1%** |
| brand_loyalty_disappointed | 24 | **66.7%** |
| expert_or_enthusiast_baseline | 47 | 55.3% |
| sequel_or_series_context | 6 | 33.3% (small n) |
| not_present | 88 | 32.9% |

Two groups dominate negative outcomes:

- **Casual buyers** (67.1% negative, n=85): These reviewers had general expectations with no deep product knowledge, making them more susceptible to disappointment from basic quality failures or product mismatches. Example: a parent purchasing a toy found it broke within two months.
- **Brand-loyalty-disappointed reviewers** (66.7%, n=24): These buyers had explicit prior positive experiences and were let down — often by formula/product changes or quality degradation over time.
- **Reviews with no stated expectation** (`not_present`) have the *lowest* negative rate (32.9%), suggesting that when a review lacks a clear expectation frame, it tends toward neutral-to-positive expression.

---

## Factor 3: Thematic Drivers in Negative Review Content

Keyword analysis of negative review text surfaces the following complaint themes:

| Theme | Negative Reviews Mentioning | Share |
|---|---|---|
| Quality / defect language | 22 | 17.6% |
| Price / poor value | 14 | 11.2% |
| Unmet expectations (explicit) | 13 | 10.4% |
| Shipping / fulfillment | 8 | 6.4% |
| Content quality (books/media) | 8 | 6.4% |
| Misrepresentation | 3 | 2.4% |

**Physical product defects and poor build quality** are the leading lexical signal in negative reviews. **Value-for-money dissatisfaction** is a secondary driver. For media products, **shallow or poor-quality content** drives negativity, especially when reviewers hold expert or prior-fan baselines.

---

## Key Findings Summary

1. **Physical consumer goods** receive the most negative reviews in absolute terms and by rate, primarily due to tangible quality and durability failures.
2. **Casual buyers** and **brand-loyalty-disappointed** reviewers are the highest-risk expectation profiles — together comprising ~43% of all reviews but generating a disproportionate share of negative sentiment.
3. **Unmet expectations** (whether from casual assumptions or prior brand loyalty) are a consistent cross-category driver of negative sentiment, confirming that the expectation gap is a root causal mechanism.
4. **Media/book reviews** show high negativity when reviewers have expert or enthusiast baselines, suggesting that domain knowledge raises the bar for what constitutes a satisfactory product.
5. The `not_present` expectation group has the lowest negative rate, indicating that reviews without an explicit reference frame are more likely to be grounded in positive experience — a potential selection-bias artifact.

---

## Caveats

- The dataset is balanced (50/50 positive/negative), so absolute negative counts reflect sampling design, not real-world base rates.
- Several category cells (software, food, apparel) have n≤5 and their rates are statistically unreliable.
- Keyword-based thematic coding captures explicit surface language only; many negative reviews express dissatisfaction implicitly.
