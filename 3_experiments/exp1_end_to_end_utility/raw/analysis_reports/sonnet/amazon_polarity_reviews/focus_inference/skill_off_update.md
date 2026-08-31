---
dataset: amazon_polarity_reviews
scenario: focus_inference
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What different aspects of their purchase are Amazon reviewers actually talking about?"
source_table: augment_table/amazon_polarity_reviews/focus_inference/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:02:29.934122+00:00
wall_seconds: 39.95
---

# Amazon Reviewer Aspects Analysis
**Dataset:** `sonnet__skill_off_update.csv` | **Variant:** `skill_off` | **N = 250 reviews**

---

## What Aspects Are Reviewers Talking About?

Amazon reviewers in this dataset span a wide range of product categories (physical goods, books, music, etc.), resulting in eight distinct aspects being tagged. The distribution is highly skewed toward a few dominant topics.

### Aspect Frequency (multi-label, % of all reviews)

| Aspect | Reviews Mentioning It | % of Total | Primary Aspect Count |
|---|---|---|---|
| **Content / Narrative** | 151 | 60.4% | 142 |
| **Product Quality** | 108 | 43.2% | 52 |
| **Features / Functionality** | 97 | 38.8% | 29 |
| **Price / Value** | 47 | 18.8% | 7 |
| **Ease of Use** | 40 | 16.0% | 9 |
| **Aesthetics / Design** | 31 | 12.4% | 4 |
| **Customer Service** | 18 | 7.2% | 3 |
| **Shipping / Delivery** | 11 | 4.4% | 4 |

### Key Findings

1. **Content/Narrative dominates.** 60% of reviews mention it and it is the single most common *primary* aspect (142/250 = 56.8%). This reflects the heavy presence of media products (books, music, video) in the Amazon Polarity dataset, where reviewers judge story, writing quality, or artistic merit rather than a tangible object.

2. **Product Quality is the runner-up for physical goods.** It appears in 43% of reviews but is the *primary* aspect in only 52 reviews — suggesting it is frequently raised as a secondary concern alongside features or functionality.

3. **Features/Functionality is mentioned often but rarely the headline.** 38.8% mention it, yet only 29 reviews treat it as the primary focus. Reviewers tend to raise features in support of a quality or usability judgment.

4. **Price/Value, Ease of Use, and Aesthetics are secondary concerns.** Each appears in 12–19% of reviews and is seldom the primary driver (≤9 reviews each as primary aspect).

5. **Shipping/Delivery and Customer Service are rare.** Together they account for fewer than 30 mentions (≤8% each) and almost never lead a review. This dataset likely underrepresents post-purchase logistics complaints.

### Sentiment Patterns

| Aspect (primary) | Negative (label=0) | Positive (label=1) |
|---|---|---|
| Content / Narrative | 62 | 80 |
| Product Quality | 37 | 15 |
| Features / Functionality | 13 | 16 |
| Ease of Use | 5 | 4 |
| Price / Value | 2 | 5 |

- **Product Quality drives negative reviews disproportionately** (37 negative vs. 15 positive as primary), indicating quality disappointment is a major complaint driver.
- **Content/Narrative is more balanced** but skews slightly positive (80 vs. 62), consistent with readers more often completing and reviewing books/music they enjoyed.
- Negative reviewers tend to mention slightly more aspects on average (2.19 vs. 1.83), suggesting dissatisfied customers elaborate more broadly.

### Caveats

- The `skill_off` variant may have suppressed some aspect-detection skill, potentially undercounting aspects in borderline cases — the 42% of reviews with zero or one aspect tagged may be higher than in a full-skill run.
- The dataset mixes very different product categories (toys, books, skincare, music), so the dominance of `content_narrative` is a category-mix artifact, not a universal finding about all Amazon shoppers.

### Summary

Amazon reviewers in this dataset primarily discuss **what the product *is* or *says*** (content/narrative for media) and **whether it works as expected** (product quality and features/functionality for physical goods). Price, usability, aesthetics, and logistics are secondary concerns raised alongside the primary judgment rather than as standalone topics.
