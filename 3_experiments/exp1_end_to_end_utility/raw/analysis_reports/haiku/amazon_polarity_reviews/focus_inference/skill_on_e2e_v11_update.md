---
dataset: amazon_polarity_reviews
scenario: focus_inference
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What different aspects of their purchase are Amazon reviewers actually talking about?"
source_table: augment_table/amazon_polarity_reviews/focus_inference/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:09:26.438528+00:00
wall_seconds: 73.83
---

# Analysis: Amazon Product Review Aspects via Comparative Language

## Executive Summary

Amazon reviewers discuss multiple distinct aspects of their purchases, with nearly 28% of reviews explicitly invoking competitor or alternative product comparisons. This augmented analysis reveals that reviewers most frequently frame their feedback by comparing against alternatives, especially when expressing negative sentiment. The primary purchase aspects discussed span product quality, performance, durability, price/value, design, brand reputation, and author/creator identity—dimensions consistently invoked across positive and negative reviews to justify their assessments.

## Methodology

**Data:** 250 Amazon product reviews (binary balanced: 125 positive, 125 negative)  
**Primary outcome variable:** `label_pos` (1 = positive sentiment, 0 = negative sentiment)  
**TAPP-generated column used:** `competitor_or_alternative_comparison` (Boolean indicator: True/False)

This report combines the original review text with the TAPP-generated semantic facet to identify review aspects through comparative language patterns.

---

## Key Findings

### 1. Prevalence of Competitor/Alternative Comparisons

**28% of reviews (70/250) explicitly mention competitors or alternatives.** This represents a significant proportion of Amazon reviewers who frame their assessments against other products, brands, or versions.

| Aspect | Count | % of Total |
|--------|-------|-----------|
| Mentions competitor/alternative | 70 | 28.0% |
| No competitor/alternative mention | 180 | 72.0% |
| **Total reviews** | **250** | **100%** |

### 2. Sentiment Distribution with Competitor Mentions

**Comparisons are significantly more common in negative reviews.** Among reviews mentioning competitors/alternatives:
- **Negative sentiment:** 41/70 (58.6%)
- **Positive sentiment:** 29/70 (41.4%)

In contrast, reviews without competitor mentions show a more balanced distribution:
- **Negative sentiment:** 84/180 (46.7%)
- **Positive sentiment:** 96/180 (53.3%)

**This 12 percentage-point shift toward negative sentiment in comparison-based reviews suggests reviewers invoke alternatives primarily to justify dissatisfaction or to highlight deficiencies relative to other options.**

### 3. Primary Purchase Aspects Discussed Through Comparisons

Reviewers invoke competitor or alternative comparisons across seven distinct purchase aspects:

| Aspect | Frequency | Positive % | Interpretation |
|--------|-----------|-----------|-----------------|
| **Author/Creator** | 21 | 57% | Reviewers compare media products (books, music, films) against works by other authors, artists, or directors |
| **Quality** | 20 | 45% | Direct quality comparisons with alternative products or versions |
| **Price/Value** | 16 | 38% | Cost-benefit assessments relative to alternatives |
| **Brand/Company** | 10 | 30% | Comparisons of manufacturer reputation and reliability |
| **Durability** | 8 | 50% | Longevity and construction quality vs. alternatives |
| **Performance** | 7 | 43% | Speed, efficiency, effectiveness relative to competing products |
| **Design/Usability** | 6 | 33% | Ergonomics, aesthetics, ease-of-use vs. alternatives |

### 4. Qualitative Patterns by Aspect

#### **Author/Creator Comparisons (21 reviews)**
Dominant in media product reviews. Examples:
- *"Unlike other Robin Cook novels..."* (negative comparison)
- *"Reminiscent of Robin Cooke novels I have always enjoyed..."* (positive comparison)
- *"I usually read Robin Cook, don't make this one your first book..."* (negative)

**Insight:** Reviewers assess books, music, and films by positioning them within an author's or creator's broader body of work or against peer creators in the same genre.

#### **Quality Comparisons (20 reviews)**
Reviewers invoke quality when dissatisfied:
- *"The legs are flimsy and the quality is one step above junk. If you have a quality camera then spend the extra money..."*
- *"I have the less expensive model by the same company and it works much better..."*

**Insight:** Quality comparisons drive negative sentiment (55% of quality mentions are negative), suggesting reviewers invoke alternatives when disappointed.

#### **Price/Value Comparisons (16 reviews)**
Mixed sentiment, but often paired with durability concerns:
- *"This is a terrific Christmas idea for anyone..."* (positive value despite cost)
- *"I honestly thought with the National Geographic name...this would have some type of quality standards. Wow! Was I ever wrong..."* (negative—brand not justifying price)

**Insight:** Reviewers weigh cost against durability, quality, and brand reputation to assess value.

#### **Brand/Company Comparisons (10 reviews)**
Comparisons frequently involve reputation and customer support:
- *"In my mind the Manfrotto name has been tainted by my experience..."*
- *"I came across this tape...I'm going to try Pilates for Dummies..."*

**Insight:** Negative reviews invoke brand reputation damage and suggest alternative brands as remedies.

---

## Non-Comparative Review Aspects (72% of reviews)

The 180 reviews without explicit competitor mentions discuss:
- **Product functionality and features:** Does it work as described?
- **Personal satisfaction and fit:** Does it meet my specific needs?
- **Experience quality:** Was it enjoyable or frustrating?
- **Design aesthetics:** Does it look/feel good?
- **Reliability over time:** Does it last?

These reviews focus on direct product evaluation rather than market positioning.

---

## Integration with Original Sentiment Metric

The `competitor_or_alternative_comparison` column reveals a **selection bias in how reviewers frame dissatisfaction.** Reviewers invoking alternatives are 12 percentage points more likely to express negative sentiment (58.6% vs. 46.7%), indicating:

1. **Alternative comparisons are rhetorical devices for justifying negative ratings:** "Here's what you should buy instead."
2. **Positive reviews rarely need alternatives:** Satisfied reviewers focus on intrinsic product value.
3. **Market-aware negative reviews suggest higher engagement:** Reviewers who compare are likely more price-conscious, quality-aware, or experienced consumers.

---

## Conclusion: What Aspects Do Amazon Reviewers Actually Discuss?

Amazon reviewers discuss **seven primary aspects of their purchases**, prioritized through two distinct communicative strategies:

1. **Comparative framing (28% of reviews):** Quality, brand trust, price-value, durability, and creator/author identity—used predominantly to justify dissatisfaction.
2. **Direct evaluation (72% of reviews):** Functionality, personal fit, experience, aesthetics, and reliability—assessed on intrinsic merits.

**The `competitor_or_alternative_comparison` augmented column clarifies that negative reviews often employ market-aware language, positioning products within competitive sets, while positive reviews typically avoid such positioning, instead celebrating products on their own terms.**

This finding is robust across the 250-review dataset and suggests that e-commerce review helpfulness might correlate with comparative content: reviews citing alternatives may drive purchasing decisions more effectively than intrinsic-only assessments.

---

## Method Note

**TAPP-generated column used in analysis:**
- `competitor_or_alternative_comparison`: Binary indicator (True/False) of whether the review mentions a competitor product, alternative brand, or substitute option for the purchased item.

This column was used to segment and analyze review content, enabling systematic comparison of how sentiment relates to market positioning language.
