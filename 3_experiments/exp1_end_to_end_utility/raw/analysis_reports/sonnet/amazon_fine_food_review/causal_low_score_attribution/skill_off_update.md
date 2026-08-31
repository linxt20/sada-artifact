---
dataset: amazon_fine_food_review
scenario: causal_low_score_attribution
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "low_review_score"
query: "What factors explain low review scores?"
source_table: augment_table/amazon_fine_food_review/causal_low_score_attribution/sonnet__skill_off_update.csv
generated_at: 2026-07-28T12:59:30.724139+00:00
wall_seconds: 32.9
---

# Factors Explaining Low Review Scores — Amazon Fine Food Reviews

## Dataset Overview
- **Total reviews:** 10,000 | **Low-score reviews (Score ≤ 2):** 1,522 (15.2%)  
- Score distribution is heavily skewed positive (Score 5: 61.8%; Scores 1–2: 15.2%).
- `is_low_score` flags reviews with Score ≤ 2 and serves as the focus variable.

---

## Key Factors (by Correlation Strength)

### 1. Reviewer Harshness (`reviewer_is_harsh`) — Strongest Factor
The single strongest predictor ($r = 0.97$). Among reviews flagged as "harsh reviewers," **99.1% are low-score**, while only 0.6% of non-harsh reviewers leave low scores. This indicates that **habitual low-raters are responsible for the vast majority of low scores**, rather than isolated product failures.

| | Low Score | High Score |
|---|---|---|
| Harsh reviewer | 99.1% | 0.9% |
| Non-harsh reviewer | 0.6% | 99.4% |

### 2. User Average Score (`user_avg_score`) — $r = -0.87$
Low-score reviewers have a mean historical score of **1.46**, vs. **4.62** for high-score reviewers. This mirrors `reviewer_is_harsh` and confirms that persistent negative raters dominate low scores.

### 3. Score vs. Product Average (`score_vs_product_avg`) — $r = -0.77$
Low-score reviews fall on average **−2.1 points** below their product's average score; high-score reviews sit **+0.4 points** above. This gap could reflect either genuine product defects or the outlier nature of harsh reviewers.

### 4. Product Average Score (`product_avg_score`) — $r = -0.42$
Products receiving low reviews have a mean product-level score of **3.48** vs. **4.25** for high-score products. Some products genuinely attract worse ratings across all reviewers, not just harsh ones.

### 5. Sentiment Signals
- **Negative word count:** low-score reviews average **0.84** negative words vs. **0.18** for high-score reviews ($r = 0.35$).  
- **Positive word count:** low-score reviews average **0.87** positive words vs. **1.80** for high-score reviews ($r = -0.22$).  
- **Sentiment ratio:** low-score reviews score **0.50** vs. **0.68** for high-score reviews ($r = -0.43$). Lexical sentiment aligns with scores but is a weaker predictor than reviewer identity.

### 6. Question Usage (`has_question`) — $r = 0.10$
Low-score reviews are more likely to contain questions (11.9% vs. 5.2%), possibly reflecting confusion or complaints about product misrepresentation.

### 7. Exclamation Usage (`has_exclamation`) — $r = -0.09$
High-score reviews use exclamations more (37.2% vs. 25.6%), consistent with enthusiastic positive feedback.

### 8. Review Length
Low-score reviews are slightly **longer** (476 chars / 87 words vs. 404 chars / 74 words), suggesting dissatisfied customers write more to explain their complaints.

---

## Weak or Absent Evidence
- **Helpfulness ratio** shows virtually no difference (0.38 vs. 0.40, $r ≈ -0.01$): community vote patterns do not distinguish low from high scores.
- **Caps ratio** is nearly identical across groups ($r = 0.02$): "shouting" in text is not a meaningful signal.

---

## Summary
Low review scores are **primarily driven by reviewer-level behavior** (harsh reviewers account for ~96.6% of low-score reviews) rather than product quality alone. Secondary contributors include genuinely lower-rated products and predictably negative lexical sentiment. Product-level effects are real but secondary. Interventions aimed at understanding low scores should first distinguish systematic harsh reviewers from genuine product complaints.
