---
dataset: amazon_polarity_reviews
scenario: focus_inference
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What different aspects of their purchase are Amazon reviewers actually talking about?"
source_table: augment_table/amazon_polarity_reviews/focus_inference/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:09:03.321624+00:00
wall_seconds: 48.73
---

# Amazon Polarity Reviews – What Aspects Do Reviewers Actually Discuss?

**Query:** What different aspects of their purchase are Amazon reviewers actually talking about?

---

## Method Note

Original structured columns used: `review_id`, `label_pos`, `title`, `content`.  
TAPP-generated columns used: **`product_category`**, **`functional_performance_issue`**, **`content_creative_quality`**.  
Dataset: 250 reviews, balanced 125 positive / 125 negative.

---

## 1. What Reviewers Are Buying (Product Domain)

`product_category` reveals two dominant purchase types across the 250 reviews:

| Category | N | Positive Rate |
|---|---|---|
| `media_book` | 83 | 52% |
| `physical_product` | 78 | 37% |
| `media_music` | 39 | 74% |
| `media_video` | 37 | 43% |
| `apparel` | 5 | 100% |
| `food_supplement` | 3 | 67% |
| `software_game` | 3 | 33% |

Books (33%) and physical products (31%) together account for nearly two-thirds of reviews. Media categories (book, music, video) total 63% of all reviews; tangible/physical goods account for the remainder. Music reviews are notably more positive (74%) than physical products (37%), suggesting satisfaction norms differ sharply by category.

---

## 2. Two Distinct Aspect Clusters: Functional Performance vs. Creative Quality

The TAPP columns cleanly partition the review corpus into two near-mutually-exclusive aspect dimensions (only 11/250 reviews have both):

- **`functional_performance_issue`** – applies almost exclusively to physical/tangible products (91% coverage for `physical_product`, ~5–8% for media).  
- **`content_creative_quality`** – applies almost exclusively to media (88–95% coverage for books, music, video; 0% for physical products).

This split mirrors the underlying product domains: **reviewers of tangible goods talk about whether it works; reviewers of media talk about creative merit.**

---

## 3. Aspect A – Functional Performance (Physical Products)

`functional_performance_issue` is coded for 94 reviews (38% of corpus). It is a near-perfect predictor of sentiment:

| Functional Issue Label | N | Positive Rate |
|---|---|---|
| `exceeds_expectations` | 8 | **100%** |
| `performs_as_advertised` | 21 | **95%** |
| `works_partially_or_intermittently` | 11 | 18% |
| `underperforms_expectations` | 40 | **5%** |
| `does_not_work_at_all` | 14 | **0%** |
| `not_present` (no functional issue raised) | 156 | 60% |

The 40 `underperforms_expectations` reviews are the single largest negative driver in the functional dimension. **Whether the product works as described is the dominant aspect for physical goods and directly determines star polarity.**

---

## 4. Aspect B – Content & Creative Quality (Media Products)

`content_creative_quality` is coded for 140 reviews (56% of corpus), covering media categories. Sub-aspects and their sentiment profiles:

| Creative Aspect | N | Positive Rate |
|---|---|---|
| `musical_quality` | 40 | **75%** |
| `plot_or_story` | 37 | 54% |
| `accuracy_or_depth` | 24 | 58% |
| `writing_style` | 21 | 33% |
| `character_development` | 8 | 50% |
| `production_quality` | 5 | 20% |
| `pacing` | 5 | 20% |

Music reviews that discuss `musical_quality` are strongly positive (75%), consistent with the category-level positive rate (74%). In contrast, `writing_style` (33%), `pacing` (20%), and `production_quality` (20%) are associated with negative reviews — these aspects arise when reviewers find something actively wrong with craft execution. `plot_or_story` and `accuracy_or_depth` cluster near neutral (50–58%), indicating they appear in both positive and negative reviews.

---

## 5. Cross-Cutting Findings

- **No functional issue raised** (`not_present`, N=156) still yields 60% positive — these are reviews focused on overall impression, value, or personal recommendation, not diagnosing a specific failure or creative flaw.
- **Apparel** (N=5, 100% positive) shows 100% functional coverage and no creative facet, but sample is too small to generalize.
- The two TAPP facets together account for coverage in ~97% of non-Unknown product categories, providing strong semantic signal beyond the raw text.

---

## 6. Summary Answer

Amazon reviewers in this corpus discuss **two primary purchase aspects**, cleanly segmented by product type:

1. **Functional performance** — dominates reviews of physical products. Reviewers ask: *Does it work? Does it do what was advertised?* Failure to work (or underperformance) is the overwhelming driver of negative polarity.

2. **Creative/content quality** — dominates reviews of books, music, and video. Reviewers focus on musical quality, plot, writing style, accuracy/depth, pacing, and production. Musical quality drives satisfaction; weak writing style and pacing drive dissatisfaction.

The raw `label_pos` signal strongly aligns with both TAPP facets: functional performance explains polarity nearly deterministically for physical goods, while creative sub-aspects show more nuanced sentiment patterns for media. Neither facet is redundant with the other or with raw category labels alone.
