---
dataset: amazon_polarity_reviews
scenario: focus_inference
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What different aspects of their purchase are Amazon reviewers actually talking about?"
source_table: augment_table/amazon_polarity_reviews/focus_inference/original.csv
generated_at: 2026-07-26T12:58:53.090777+00:00
wall_seconds: 82.39
---

# Amazon Polarity Reviews – Focus Inference: What Are Reviewers Actually Talking About?

**Dataset:** `original.csv` | **N = 250** reviews (125 positive `label_pos=1`, 125 negative `label_pos=0`)  
**Columns:** `review_id`, `label_pos`, `title`, `content`

---

## Overview

The dataset covers a wide range of Amazon product categories — books, music/albums, films, physical goods (skincare, toys, apparel, electronics, food, etc.). Reviewers discuss many different aspects of their purchases. The `label_pos` column (binary: 0 = negative, 1 = positive) tracks overall sentiment, but the *content* of reviews spans multiple distinct aspects.

---

## Aspect Breakdown

Keyword-based analysis of titles + review text identified the following dominant aspects (reviews can belong to multiple categories):

| Aspect | Positive Reviews | Negative Reviews | Total Mentions |
|---|---|---|---|
| **Entertainment / Story / Content** | 83 | 68 | **151** |
| **Effectiveness / Performance** | 41 | 57 | **98** |
| **Taste / Smell / Feel / Texture** | 35 | 31 | **66** |
| **Value / Price** | 16 | 30 | **46** |
| **Product Quality / Durability** | 15 | 18 | **33** |
| **Fit / Size** | 9 | 15 | **24** |
| **Shipping / Delivery** | 11 | 12 | **23** |
| **Customer Service / Returns** | 6 | 10 | **16** |

> Note: Counts reflect co-occurrence of aspect keywords, not mutually exclusive bins. ~21 reviews (8%) fell outside all defined keyword buckets (e.g., abstract opinions, identity/representation commentary).

---

## Key Findings by Aspect

### 1. Entertainment / Story / Content (most common, ~60% of reviews)
The largest single category. Covers books, music albums, films, and media. Reviewers focus on:
- **Narrative quality** (plot, characters, pacing) for books and films
- **Musical quality** (lyrics, production, depth of emotion) for albums
- **Packaging / curation** for special editions (e.g., Criterion collections)

Both positive and negative reviews are heavily represented here, suggesting polarization within media/entertainment products.

*Example negative:* "Skip it." (Anne Lamott book — too much political commentary, not enough personal writing)  
*Example positive:* "Criterion presents a great package of a great film."

### 2. Effectiveness / Performance (~39% of reviews)
The second-largest aspect, skewed slightly toward **negative** reviews (57 neg vs. 41 pos). Reviewers discuss whether a product "works" — skincare results, exercise programs, electronics functioning correctly.

*Example negative:* "Pass on this Pilates Workout"  
*Example positive:* "Keeps skin clear" (long-term skin product use)

### 3. Taste / Smell / Feel / Texture (~26% of reviews)
Prominent for consumables (food, supplements) and physical goods (lotions, bath products, apparel). Sensory experience drives both praise and complaints.

### 4. Value / Price (~18% of reviews)
More common in **negative** reviews (30 neg vs. 16 pos), suggesting price disappointment is a meaningful driver of low ratings. Reviewers flag "overpriced" items or poor value-for-money.

### 5. Product Quality / Durability (~13%)
Covers defects, breakage, and construction quality. Evenly split between polarities, but negative reviewers are more likely to describe specific failures ("broke after one use," "cheap materials").

### 6. Fit / Size (~10%)
Mostly apparel/footwear. Negative reviews more commonly cite sizing issues (10 neg vs. 9 pos with some overlap). 

### 7. Shipping / Delivery (~9%)
Roughly evenly split. Covers arrival time, packaging damage, and seller fulfillment. Not a primary focus but appears as a **secondary complaint** in otherwise mixed reviews.

### 8. Customer Service / Returns (~6%)
Least common but disproportionately negative (10 neg vs. 6 pos). When reviewers mention returns or seller contact, it usually signals a problem.

---

## Exceptions and Weak Evidence

- **Uncategorized reviews (~8%):** Some reviews address representation/identity concerns (e.g., lack of Black baby dolls in toy stores), personal anecdotes, or are too short to categorize reliably.
- **Aspect overlap is high:** A single review frequently touches multiple aspects (e.g., effectiveness *and* value), so the counts above overcount total reviews.
- **Category labels are inferred** — the dataset does not include a product-category column, so aspect assignment relies on keyword heuristics and may misclassify some reviews.
- **Entertainment aspect dominance** may reflect sampling bias toward media products in the dataset, not necessarily a signal that media is inherently more reviewed.

---

## Summary

Amazon reviewers in this dataset primarily discuss **content/entertainment quality** (for media products) and **functional effectiveness** (for physical goods). Secondary concerns include **sensory experience**, **price-value perception**, and **product durability**. Negative reviews are particularly concentrated around **poor effectiveness** and **price disappointment**, while positive reviews most often celebrate **content quality** and **long-term product performance**. Operational concerns (shipping, customer service) appear but are rarely the *primary* focus.
