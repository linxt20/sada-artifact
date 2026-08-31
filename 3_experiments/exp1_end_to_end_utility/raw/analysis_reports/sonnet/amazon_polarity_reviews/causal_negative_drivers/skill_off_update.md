---
dataset: amazon_polarity_reviews
scenario: causal_negative_drivers
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "label_pos"
query: "Why do some Amazon products receive predominantly negative reviews, and which factors contribute the most?"
source_table: augment_table/amazon_polarity_reviews/causal_negative_drivers/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:01:50.480501+00:00
wall_seconds: 40.99
---

# Why Amazon Products Receive Predominantly Negative Reviews

## Dataset Overview

The dataset contains **250 reviews** evenly split between negative (`label_pos = 0`, n = 125) and positive (`label_pos = 1`, n = 125). Each review is augmented with seven binary negative-theme flags, a `negative_theme_count`, and a `negative_intensity_score`.

---

## Key Causal Factors

### 1. Poor Quality — Strongest Discriminator
`negative_theme_poor_quality` appears in **14.4%** of negative reviews vs. only **0.8%** of positive reviews — the largest gap of any single theme (~18× rate). Reviewers explicitly describe materials, construction, or performance falling below acceptable standards.

### 2. General Disappointment
`negative_theme_disappointment` is present in **12.8%** of negative vs. 7.2% of positive reviews. This captures expectation mismatches — the product failed to deliver on its promise, even when no specific defect is named.

### 3. Product Defect / Malfunction
`negative_theme_product_defect` flags **10.4%** of negative reviews vs. 6.4% of positive reviews. While the gap is modest, defect mentions are functionally distinct from general quality complaints and represent hard failures (broken on arrival, stopped working, etc.).

### 4. Customer Service
`negative_theme_customer_service` appears in **9.6%** of negative reviews vs. 2.4% of positive reviews (~4× rate). Poor post-purchase support amplifies negative sentiment beyond the product itself.

### 5. Misleading Descriptions
`negative_theme_misleading` is rare overall (2.4% of negatives, 0% of positives), but entirely absent from positive reviews — a clean signal when it appears.

---

## Weak or Surprising Evidence

| Factor | Negative % | Positive % | Interpretation |
|---|---|---|---|
| Shipping issues | 9.6% | **11.2%** | *Higher* in positive reviews — suggests fulfillment problems are not reliably predictive of final sentiment |
| Pricing | 6.4% | 4.0% | Small gap; pricing complaints alone rarely drive a negative rating |

**Shipping issues** is the clearest counter-intuitive finding: positive reviewers mention it as much or more than negative ones, possibly because fast delivery boosted satisfaction or buyers forgave minor delays.

---

## Intensity & Theme Count

- The average `negative_intensity_score` is modestly higher for negative reviews (3.10 vs. 2.59), but the difference is small and the distribution is heavily right-skewed (max = 71 in negative reviews, driven by a handful of very irate reviews).
- **52%** of negative reviews (65/125) carry **zero** tagged negative themes, meaning the majority of negative ratings are expressed through tone and word choice rather than explicit complaint keywords — pointing to a signal gap in keyword-based tagging.

---

## Summary: Causal Driver Ranking

1. **Poor quality** — strongest and most reliable causal factor
2. **Expectation mismatch / disappointment** — broad, second-most prevalent
3. **Product defect / malfunction** — concrete hard failures
4. **Customer service failures** — amplifier of negativity
5. **Misleading descriptions** — rare but highly specific to negative outcomes

> **Caveat:** More than half of negative reviews carry no tagged theme, so these percentages underestimate true driver prevalence. The analysis describes tagged signals; qualitative reading of `content` would likely surface additional patterns (e.g., taste/style mismatch for books/music that defy product-defect framing).
