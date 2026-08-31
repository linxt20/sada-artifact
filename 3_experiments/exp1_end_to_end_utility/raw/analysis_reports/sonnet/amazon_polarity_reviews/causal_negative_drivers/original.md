---
dataset: amazon_polarity_reviews
scenario: causal_negative_drivers
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: causal_attribution
focus_variable: "label_pos"
query: "Why do some Amazon products receive predominantly negative reviews, and which factors contribute the most?"
source_table: augment_table/amazon_polarity_reviews/causal_negative_drivers/original.csv
generated_at: 2026-07-26T12:57:33.159615+00:00
wall_seconds: 99.66
---

# Causal Analysis of Negative Amazon Product Reviews

**Dataset:** `amazon_polarity_reviews / causal_negative_drivers / original`  
**Records:** 250 reviews (125 negative `label_pos=0`, 125 positive `label_pos=1`)  
**Columns analysed:** `review_id`, `label_pos`, `title`, `content`

---

## 1. Overview

The dataset is perfectly balanced: exactly 50% negative and 50% positive reviews. Negative reviews span a wide range of product/media categories — books, DVDs/films, CDs, physical consumer goods (toys, appliances, fitness equipment), and food/health items. No single category dominates, suggesting that drivers of dissatisfaction are cross-category rather than niche-specific.

Average review length is nearly identical across sentiment classes (~374 chars for negative, ~364 for positive), so verbosity alone is not a distinguishing factor.

---

## 2. Key Negative-Review Drivers (Ranked by Frequency)

| Factor | Neg. Reviews Affected | % of Negatives |
|---|---|---|
| **Product quality / defects** | 23 | 18.4% |
| **Poor content / story quality** (media) | 19 | 15.2% |
| **Durability failure** | 18 | 14.4% |
| **Unmet expectations / disappointment** | 16 | 12.8% |
| **Customer service / fulfillment issues** | 10 | 8.0% |
| **Poor value for money** | 7 | 5.6% |
| **Misleading / false advertising** | 1 | 0.8% |

> Note: categories are not mutually exclusive; a single review can cite multiple drivers.

---

## 3. Factor Deep-Dives

### 3.1 Product Quality & Defects (Top Factor — 18.4%)
Physical goods are the most common source of objective, verifiable complaints. Reviewers cite items that broke immediately or stopped functioning:

- *"Within two months it had completely fell apart."* (AMZ-0014, toy)
- *"This product is total junk and didn't work at all, even though we tried with 4–5 different sets of new batteries."* (AMZ-0029)
- *"I've had one leg adjustment stop break twice."* (AMZ-0033, tripod)

Defect complaints are written with high confidence and often include advice to avoid the product entirely, making them influential to other shoppers.

### 3.2 Poor Content / Story Quality (15.2%) — Media-Specific
Books, films, and music albums that fail to meet artistic expectations form the second-largest cluster. Reviewers criticise weak narratives, poor acting, shallow lyrics, or stale performances:

- *"Third day's new record stinks."* (AMZ-0040)
- *"This 'book' was a complete waste of time, money and paper."* (AMZ-0035)
- *"She breezed through the exercises! She looked wobbly and uncoordinated."* (AMZ-0006)

Media reviews frequently reflect **subjective taste mismatches** rather than objective failures, yet they still register as strongly negative.

### 3.3 Durability Failures (14.4%)
A distinct sub-pattern from general defects: products that initially perform adequately but fail within weeks or months:

- *"Great for a year then disconnects"* — modem developing internal clock bug (AMZ-0020)
- *"it lasted maybe 4 months. Now the add-water light always comes on."* (AMZ-0036)

Short product lifespan is a strong predictor of negative sentiment and is often paired with regret language.

### 3.4 Unmet Expectations / Disappointment (12.8%)
Reviews where the product or content simply did not match what was communicated in marketing, description, or prior reputation:

- *"Not as it appears!"* — clock radio with poor readability (AMZ-0026)
- *"This album does not represent the true Gato by any stretch."* (AMZ-0032)

This factor bridges objective shortcomings and subjective perception.

### 3.5 Customer Service & Fulfillment (8.0%)
A smaller but notable cluster cites poor seller behaviour, problematic returns, or Amazon Marketplace issues:

- *"Amazon Marketplace dealer changed the return reason … so that they don't have to pay return shipping."* (AMZ-0029)

These complaints are often compounded onto existing product complaints, amplifying the negativity signal.

### 3.6 Poor Value for Money (5.6%)
Overpricing relative to quality is cited explicitly in roughly 1-in-18 negative reviews. The overlap with quality/durability complaints is high.

---

## 4. Qualitative Patterns

- **Strong-signal titles** (e.g., "Worst Movie of All Time", "DO NOT waste your money", "SUCKS", "Worthless") appear in **~22% of negative reviews**, indicating reviewers actively flag dissatisfaction in the headline — useful as a fast-signal feature.
- **Media products** (books, DVDs, CDs) account for ~54% of negative reviews by category inference, while **physical goods** account for ~22%. The higher media share reflects the dataset's breadth of Amazon categories.
- **Barely any reviews cite misleading advertising** (0.8%) as a standalone driver — deception is typically embedded within quality or expectation complaints rather than called out explicitly.

---

## 5. Exceptions & Weak Evidence

- **False advertising** appears almost negligible as a standalone category (1 case), though it may be underrepresented because reviewers conflate it with "unmet expectations."
- Some negative reviews (e.g., AMZ-0039 — *Mikado* DVD; AMZ-0011 — linguistics book) are **nuanced and mixed**, acknowledging partial quality while criticising specific aspects (e.g., audio quality, target audience mismatch). These borderline cases suggest the label boundary is not always sharp.
- Review length does **not** reliably distinguish sentiment in this dataset, limiting its causal utility.

---

## 6. Summary & Decision-Ready Takeaways

| Priority | Driver | Actionable Signal |
|---|---|---|
| 🔴 High | Product quality & defects | Defect mentions (`broke`, `junk`, `doesn't work`) are strong classifiers |
| 🔴 High | Content/story quality | Subjective dissatisfaction is equally prevalent for media products |
| 🟠 Medium | Durability failures | Time-to-failure language is a distinct negative sub-pattern |
| 🟠 Medium | Unmet expectations | Gap between promise and reality is cross-category |
| 🟡 Low | Customer service | Amplifier rather than primary driver |
| 🟡 Low | Value for money | Usually co-occurs with quality complaints |

**Bottom line:** Negative Amazon reviews in this dataset are primarily driven by **objective product failures** (defects, durability) and **subjective quality shortfalls** (poor content for media). Expectation mismatch bridges both. Customer service and pricing play supporting rather than leading roles. Any predictive model or product-improvement effort should prioritise defect reduction for physical goods and content/curation quality signals for media categories.
