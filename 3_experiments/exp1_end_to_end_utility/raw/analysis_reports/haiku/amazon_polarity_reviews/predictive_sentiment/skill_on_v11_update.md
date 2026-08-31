---
dataset: amazon_polarity_reviews
scenario: predictive_sentiment
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "label_pos"
query: "How do review facets differ by sentiment label?"
source_table: augment_table/amazon_polarity_reviews/predictive_sentiment/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:09:17.090573+00:00
wall_seconds: 56.26
---

# Review Facets by Sentiment Label: Analysis Report

## Executive Summary

Negative and positive reviews in the Amazon Polarity dataset exhibit strongly differentiated facet patterns across all four measured dimensions. Positive reviews show consistent endorsement indicators, while negative reviews predominantly feature problem identification and dissatisfaction signals. The differences are statistically pronounced and actionable for understanding sentiment drivers.

## Dataset Overview

- **Total reviews**: 250 (perfectly balanced)
- **Negative reviews (label=0)**: 125 (50%)
- **Positive reviews (label=1)**: 125 (50%)

## Key Findings by Facet

### 1. Quality Defect Presence

**Clear sentiment differentiation**: Negative reviews contain substantially more identified defects than positive reviews.

| Defect Type | Negative Reviews | Positive Reviews |
|---|---|---|
| Performance Failure | 16 (12.8%) | 1 (0.8%) |
| Durability Failure | 13 (10.4%) | 0 (0.0%) |
| Design Flaw | 10 (8.0%) | 4 (3.2%) |
| Manufacturing Defect | 5 (4.0%) | 1 (0.8%) |
| Material Issue | 4 (3.2%) | 2 (1.6%) |
| **Total with Defects** | **48 (38.4%)** | **8 (6.4%)** |

**Insight**: Negative reviews are 6× more likely to explicitly mention quality defects. Performance and durability failures dominate negative reviews, indicating these are primary dissatisfaction drivers. Positive reviews rarely cite defects; when they do, design flaws and material issues are most common.

### 2. Expectation Gap Type

Negative reviews extensively identify mismatches between expectations and reality, while positive reviews rarely do.

**Expectation Gap Presence**:
- **Negative**: 69 reviews (55.2%) contain identified gaps
- **Positive**: 13 reviews (10.4%) contain identified gaps

| Gap Type | Negative | Positive |
|---|---|---|
| Quality Below Price | 44 (35.2%) | 6 (4.8%) |
| Different Than Described | 12 (9.6%) | 2 (1.6%) |
| Feature Missing | 8 (6.4%) | 3 (2.4%) |
| Poor vs. Alternatives | 3 (2.4%) | 2 (1.6%) |

**Insight**: Over half of negative reviews stem from explicit expectation gaps, with "quality below price" being the dominant complaint (35.2% of negatives). Positive reviews show minimal expectation mismatch, suggesting satisfied customers found value delivered as expected or better.

### 3. Explicit Recommendation

**Stark recommendation divergence** across sentiment labels.

| Recommendation | Negative Reviews | Positive Reviews |
|---|---|---|
| Advise Against | 90 (72.0%) | 2 (1.6%) |
| Strongly Advise Against | 15 (12.0%) | 0 (0.0%) |
| Neutral Stance | 15 (12.0%) | 10 (8.0%) |
| Recommend | 3 (2.4%) | 82 (65.6%) |
| Strongly Recommend | 0 (0.0%) | 29 (23.2%) |
| Not Stated | 2 (1.6%) | 2 (1.6%) |

**Insight**: Negative reviews contain no "strongly recommend" endorsements; instead, 84% explicitly counsel against purchase. Positive reviews show 88.8% active recommendation (recommend + strongly recommend), with only 1.6% cautioning against purchase. This binary recommendation pattern is highly predictive of sentiment.

### 4. Usage Fit Assessment

Sentiment shows clear alignment with product-audience fit judgments.

| Usage Fit | Negative Reviews | Positive Reviews |
|---|---|---|
| Poor Fit for Stated Use | 92 (73.6%) | 3 (2.4%) |
| Good for Intended Use | 6 (4.8%) | 96 (76.8%) |
| Good for Specific Niche | 7 (5.6%) | 18 (14.4%) |
| Not Discussed | 13 (10.4%) | 5 (4.0%) |
| Not for Everyone | 5 (4.0%) | 2 (1.6%) |
| Other | 2 (1.6%) | 1 (0.8%) |

**Insight**: Negative reviews predominantly classify products as "poor fit for stated use" (73.6%), indicating fundamental product-use misalignment. Positive reviews overwhelmingly indicate "good for intended use" (76.8%), reflecting successful product-audience matching.

## Sentiment Facet Profile Summary

**Negative Review Facet Profile**:
- Quality defects identified in ~38% of reviews
- Expectation gaps present in 55% of reviews (primarily price-quality mismatch)
- 84% explicitly advise against purchase (12% strongly)
- 74% classified as poor fit for stated use
- Strong consensus on product problems and misalignment

**Positive Review Facet Profile**:
- Quality defects identified in only 6% of reviews
- Expectation gaps present in only 10% of reviews
- 89% actively recommend (23% strongly)
- 77% classified as good for intended use
- Strong consensus on product satisfaction and utility

## Conclusions

Review facets exhibit **highly consistent differentiation by sentiment**:

1. **Quality defects** appear 6× more frequently in negative reviews, with performance/durability failures as leading issues
2. **Expectation gaps** (55% vs. 10%) are a defining characteristic of negative sentiment, driven primarily by value perception
3. **Recommendation strength** shows binary polarization: negative reviews counsel against (84%), positive reviews endorse (89%)
4. **Usage fit assessment** is the strongest categorical differentiator: 74% vs. 77% split on opposite outcomes

The facet patterns suggest that **negative sentiment is driven by identifiable quality/reliability problems and perceived value gaps**, while **positive sentiment reflects successful product-use alignment without significant defect identification**. These facets provide interpretable, explainable indicators of sentiment and could inform product improvement prioritization.
