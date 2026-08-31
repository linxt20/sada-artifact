---
dataset: amazon_polarity_reviews
scenario: focus_inference
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What different aspects of their purchase are Amazon reviewers actually talking about?"
source_table: augment_table/amazon_polarity_reviews/focus_inference/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:08:53.762153+00:00
wall_seconds: 41.37
---

# Amazon Review Aspects: Focus Inference Analysis

**Dataset:** 250 Amazon reviews across 10 product categories  
**Focus variable:** What aspects of a purchase are reviewers actually discussing?

---

## Overview

The augmented dataset captures three primary dimensions of reviewer focus: **functional/performance outcomes**, **content/creative quality**, and **comparative framing**. These dimensions largely partition by product type, with minimal overlap between them.

---

## 1. Functional Performance — Physical Products

**83 reviews** (33%) contain a functional performance verdict, almost exclusively for physical goods (electronics, home/kitchen, health/beauty, toys, apparel, sports).

| Verdict | Count | Sentiment skew |
|---|---|---|
| `works_as_advertised` | 27 | Positive (26/27 are positive reviews) |
| `partial_functionality` | 30 | Negative (23/30 are negative) |
| `does_not_work` | 19 | All negative |
| `intermittent_failure` | 7 | Mostly negative (6/7) |

**Key pattern:** Functional failure is strongly tied to negative sentiment. Reviewers discussing whether a product works or breaks are almost always complaining. Praise in this dimension is rarer and centres on products performing exactly as promised.

---

## 2. Creative/Content Quality — Media Products

**129 reviews** (52%) surface a content quality dimension, dominant among books (84 reviews), music CDs (40), and DVDs (36).

| Content Dimension | Count | Sentiment skew |
|---|---|---|
| `narrative_plot` | 41 | Balanced (20 neg / 21 pos) |
| `performance_acting_singing` | 37 | Mostly positive (27/37 pos) |
| `writing_style` | 24 | Skews negative (16/24 neg) |
| `production_audio_video` | 10 | Slightly negative |
| `accuracy_factual` | 7 | All negative |
| `character_development` | 7 | Mostly positive |
| `pacing` | 3 | Mixed |

**Key pattern:** Reviewers of books focus heavily on writing style and plot; music/DVD reviewers foreground performance quality. `accuracy_factual` complaints (all negative) stand out as a distinct dimension for non-fiction books. Performance/singing praise is the single strongest positive signal in media reviews.

---

## 3. Comparative Framing — Context Reviewers Use

**93 reviews** (37%) explicitly frame their assessment by comparison.

| Comparison Type | Count | Top categories |
|---|---|---|
| `compared_to_genre_standard` | 34 | music_cd, book |
| `compared_to_competing_product` | 32 | home/kitchen, electronics, music_cd |
| `compared_to_same_series_or_sequel` | 16 | book, dvd_film |
| `compared_to_prior_version` | 11 | electronics, health/beauty |

**Key pattern:** Physical product reviewers often benchmark against competitors (value/feature comparison), while media reviewers benchmark against genre conventions or earlier works in a series. Prior-version comparisons are a notable niche for electronics and reformulated consumer goods.

---

## 4. Dimension Co-occurrence

Only **5 reviews** simultaneously exhibit both a functional verdict and a content quality label, confirming these are structurally distinct discourse modes tied to product type rather than review style.

**167 reviews** (67%) have no functional verdict, and **121 reviews** (48%) have no content quality dimension — these "not_present" cases cluster where the review's focus is purely experiential, emotional, or comparative without explicit attribute evaluation.

---

## 5. Exceptions and Weak Evidence

- **`physical_product_health_beauty`** (10 reviews) shows the highest rate of competitor comparisons relative to its size, but the small n limits confidence.
- **`physical_product_sports_outdoor`** (3 reviews) is too sparse to draw conclusions.
- The `comparison_reference_type` dimension applies across both physical and media products, but its meaning differs: for physical goods it is feature/price benchmarking; for media it is aesthetic/quality benchmarking. The single column conflates these.
- Two rows are categorised as `Unknown` product category and cannot be reliably placed in either functional or content quality frameworks.

---

## Summary

Amazon reviewers discuss purchases along three largely non-overlapping axes:

1. **Does it work?** — the dominant frame for physical products, with failure strongly correlated to negative sentiment.
2. **Is the creative content good?** — the dominant frame for books, music, and film, with sub-dimensions (plot, performance, writing style, accuracy) that vary by medium.
3. **How does it compare?** — a cross-cutting frame applied by ~37% of reviewers, referencing competitors, genre norms, or prior versions to anchor their judgement.
