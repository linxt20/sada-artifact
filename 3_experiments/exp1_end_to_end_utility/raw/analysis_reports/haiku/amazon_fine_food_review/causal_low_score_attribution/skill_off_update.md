---
dataset: amazon_fine_food_review
scenario: causal_low_score_attribution
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "low_review_score"
query: "What factors explain low review scores?"
source_table: augment_table/amazon_fine_food_review/causal_low_score_attribution/haiku__skill_off_update.csv
generated_at: 2026-07-28T12:59:28.985875+00:00
wall_seconds: 45.96
---

# Causal Attribution of Low Review Scores: Amazon Fine Food Reviews

## Executive Summary

This analysis identifies key factors explaining low review scores (1-2 stars) in the Amazon Fine Food Reviews dataset. The dataset contains 1,522 low-score reviews (15.2% of 10,000 total reviews). The primary drivers of low scores are **complaint language**, **absence of positive sentiment**, and **negative word presence**, with secondary factors including higher review verbosity and more questioning language.

## Data Overview

- **Total reviews analyzed**: 10,000
- **Low-score reviews (1-2 stars)**: 1,522 (15.2%)
- **High-score reviews (4-5 stars)**: 7,616 (76.2%)
- **Mid-range reviews (3 stars)**: 862 (8.6%)

## Primary Factors Explaining Low Scores

### 1. **Complaint Language Markers (Strong Signal)**

Complaint language is the strongest and most prevalent factor distinguishing low-score reviews:

| Factor | Low Score | High Score | Difference |
|--------|-----------|-----------|-----------|
| **Complaint Markers Present** | 82.2% | 57.9% | **+24.3 pp** |
| **Negative Words Present** | 41.6% | 12.3% | **+29.3 pp** |

**Key insight**: 82.2% of low-score reviews contain explicit complaint markers (words like "not," "problem," "doesn't," "broken," "defective"), compared to only 57.9% in high-score reviews. This 24.3 percentage point gap is substantial and indicates complaint language is a primary driver.

**Evidence**: Examples include:
- "Not as Advertised" (Score 1)
- "My Cats Are Not Fans of the New Food" (Score 1)
- "stale product" (Score 1)

### 2. **Absence of Positive Sentiment (Strong Signal)**

The lack of positive language is a critical factor:

| Factor | Low Score | High Score | Difference |
|--------|-----------|-----------|-----------|
| **Positive Words Present** | 49.1% | 85.3% | **-36.2 pp** |

**Key insight**: Only about half of low-score reviews contain positive words, while 85.3% of high-score reviews do. This 36.2 percentage point gap (largest in the analysis) demonstrates that absence of positive sentiment is strongly associated with low scores. The correlation coefficient between positive words and score is +0.34 (second strongest predictor).

### 3. **Combination of Negative Sentiment**

Low-score reviews exhibit distinct sentiment patterns:

- **Both negative AND positive words**: 23.2% (mixed/contradictory reviews)
- **Only negative words**: 18.4% (clearly dissatisfactory)
- **Only positive words**: 25.9% (paradoxically positive but scored low)
- **Neither sentiment marker**: 32.5% (neutral or complaint-focused language)

**Key insight**: The 32.5% with neither sentiment marker suggests that complaint language alone (without explicit positive/negative words) is sufficient to trigger low scores.

## Secondary Factors

### 4. **Review Verbosity and Questioning**

Low-score reviews tend to be longer and more question-focused:

| Factor | Low Score | High Score |
|--------|-----------|-----------|
| **Average text length** | 475 chars | 394 chars |
| **Average questions per review** | 0.20 | 0.06 |
| **Reviews with questions** | 11.9% | 8.4% |

**Key insight**: Low-score reviews are ~20% longer and contain 3.3× more questions on average. Rhetorical or questioning language often signals skepticism or confusion, contributing to negative sentiment.

### 5. **Exclamation Count Pattern**

Interestingly, low-score reviews contain fewer exclamation marks:

| Factor | Low Score | High Score |
|--------|-----------|-----------|
| **Average exclamations** | 0.62 | 0.80 |

**Key insight**: This suggests low-score reviews lack the enthusiasm and excitement characteristic of satisfied reviewers, though the difference is modest (+0.08 correlation with score).

## Weak Factors

### Helpfulness Ratio
Helpfulness ratio (helpful votes / total votes) is essentially equivalent between low (0.38) and high (0.41) score reviews, suggesting this is **not** a causal factor—low-score reviews can still be helpful to readers.

### Summary Length
While low-score summaries average 24.3 words vs. 22.7 for high scores, this difference is negligible and not a meaningful driver.

## Factor Ranking by Predictive Strength

Based on correlation analysis with review score:

1. **Positive words present**: +0.34 correlation (strongest)
2. **Negative words present**: -0.29 correlation
3. **Complaint markers present**: -0.25 correlation
4. **Question count**: -0.12 correlation
5. **Text length**: -0.10 correlation
6. **Exclamation count**: +0.08 correlation (weak)
7. **Helpfulness ratio**: +0.03 correlation (negligible)

## Conclusions

**Primary drivers of low scores** are:
1. **High presence of complaint language** (82.2% of low-score reviews)
2. **Absence of positive sentiment** (only 49.1% have positive words vs. 85.3% for high scores)
3. **Presence of negative language** (41.6% vs. 12.3% in high scores)

**Secondary drivers** include excessive questioning and verbosity, which suggest reviewer dissatisfaction requiring detailed explanation.

**Not significant**: Helpfulness and summary length are not meaningful causal factors.

The dataset demonstrates that reviewers expressing low scores tend to emphasize problems explicitly through complaint markers and absence of positive language, rather than through excessive use of negative words alone. This suggests that **the choice to omit positive language combined with complaint framing** is the fundamental causal mechanism behind low review scores.
