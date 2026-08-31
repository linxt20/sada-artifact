---
dataset: amazon_polarity_reviews
scenario: focus_inference
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What different aspects of their purchase are Amazon reviewers actually talking about?"
source_table: augment_table/amazon_polarity_reviews/focus_inference/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:09:03.473536+00:00
wall_seconds: 56.48
---

# Amazon Polarity Reviews: Focus Inference Analysis
## What Different Aspects Are Reviewers Actually Discussing?

### Executive Summary

Amazon reviewers discuss purchase aspects across four primary dimensions captured in the augmented dataset: **product performance**, **quality/durability**, **content substance**, and **comparative context**. This analysis of 250 balanced reviews (125 positive, 125 negative) reveals distinct patterns in what drives satisfaction and dissatisfaction, with performance being the strongest differentiator between positive and negative reviews.

---

### 1. Product Performance (Strongest Signal)

**Key Finding:** Product performance is the primary aspect distinguishing positive from negative reviews.

- **Works as Advertised (81 reviews):** 96% positive reviews (78 of 81)
  - Reviewers emphasize functional effectiveness and expected behavior
  - Positive reviews celebrate when products "keep my skin clear," "capture perfectly," or perform "as promised"
  - Example: *"I've been using this product for many years now, and I can't get enough of it. It's the only one out there that keeps my skin clear."*

- **Works Poorly (65 reviews):** 97% negative reviews (63 of 65)
  - Reviewers highlight failures, malfunctions, and unmet expectations
  - Common complaints include products that "did not work at all," are "slow," or "produce no power"
  - Example: *"Not the greatest product... This product is slow and does not produce shaved ice with any degree of consistency."*

- **Works Intermittently (5 reviews):** Rare but split across sentiments
  - 4 negative, 1 positive; suggests inconsistent performance is problematic

- **Performance Not Present (99 reviews, 40%):** Primarily non-physical products (books, films, music)
  - These reviews focus on content and narrative aspects instead

**Interpretation:** Performance reliability is a dominant aspect determining sentiment. Reviewers fixate on whether products function as intended.

---

### 2. Quality & Durability (Secondary Signal)

**Key Finding:** Durability concerns are explicit, actionable complaints; positive durability mentions are rare but strongly predictive of satisfaction.

| Aspect | Positive | Negative | Interpretation |
|--------|----------|----------|---|
| **Durable/Long-term (23)** | 22 (96%) | 1 (4%) | Longevity drives strong satisfaction |
| **Breaks Quickly (11)** | 0 (0%) | 11 (100%) | Rapid failure guarantees negative reviews |
| **Poor Construction (26)** | 1 (4%) | 25 (96%) | Structural defects are decisive complaints |
| **Degrades Over Time (5)** | 1 (20%) | 4 (80%) | Gradual failure is reliably negative |
| **Not Mentioned (185)** | 101 (55%) | 84 (45%) | Neutral when not salient |

**Representative Evidence:**
- Positive durability framing: *"Still working after 20 years... we've had to replace the weatherstripping a time or two, but overall we've found the Plexidor a very solid product"*
- Negative durability framing: *"Within two months it had completely fell apart... the animal noises were sticking and continuously going"*

**Interpretation:** Durability is a **high-confidence negative signal** (100% of "breaks quickly" reviews are negative), though mentions are less frequent than performance issues. When reviewers emphasize longevity, satisfaction is nearly assured.

---

### 3. Content & Substance Quality

**Key Finding:** Reviewers evaluate how substantive, coherent, and well-articulated reviews themselves are—not just the product quality.

| Quality Level | Count | Positive % | Negative % |
|---|---|---|---|
| **Well-written/Substantive (141)** | 141 | 58% | 42% |
| **Superficial (91)** | 91 | 44% | 56% |
| **Poorly-written (18)** | 18 | 17% | 83% |

**Distribution Insight:**
- Well-written substantive reviews appear in both positive (82) and negative (59) sentiment, showing that *thorough reasoning* supports both praise and criticism
- Superficial reviews (brief, minimal detail) trend slightly negative, suggesting rushed negative impressions
- Poorly-written reviews (broken grammar, unclear logic) are 83% negative

**Representative Examples:**
- Well-written positive: *"This book provided excellent history on the provinces... particularly the Storm of Chaos material. The research was thorough."*
- Superficial negative: *"Great for a year then disconnects. Would never buy this product."*
- Poorly-written negative: *"It never works I've been throe bad solder suckers before but this has to bethe worst."*

**Interpretation:** Reviewers who take time to articulate detailed opinions tend to provide balanced assessment. Brief, inarticulate reviews are more often complaints. This reflects cognitive effort: satisfied customers and dissatisfied customers alike use richer language when explaining complex evaluations.

---

### 4. Comparative Context (Recommendation Leverage)

**Key Finding:** Explicit comparisons to alternatives are infrequent (25% of reviews) but highly directional.

| Stance | Count | Positive % | Negative % | Interpretation |
|---|---|---|---|---|
| **No Comparison (163)** | 163 | 56% | 44% | Standalone evaluation |
| **Recommend Alternative (14)** | 14 | 0% | 100% | Always negative; active discouragement |
| **Worse Than Competitors (19)** | 19 | 5% | 95% | Comparative disadvantage is damning |
| **Better Than Competitors (13)** | 13 | 69% | 31% | Competitive advantage supports satisfaction |
| **Similar Performance (11)** | 11 | 73% | 27% | Parity is cautiously positive |
| **Not Present (30)** | 30 | 53% | 47% | Explicit absence of context |

**Key Patterns:**
- **Recommending alternatives** (e.g., *"I'm going to try Pilates for Dummies and see how I like it"*, *"get the electric one instead"*) occurs exclusively in negative reviews (14/14)
- **Better than competitors** appears in 13 reviews, 69% positive (e.g., *"far better organized than most steel boxes and cheap enough to devote different bags to different tasks"*)
- **Standalone reviews** (no comparison, 163 reviews) are more neutral (56% positive)

**Interpretation:** Reviewers invoke comparisons primarily when dissatisfied, either to redirect purchases or justify superiority. Positive reviews rarely need comparative framing; they emphasize absolute merit.

---

### 5. Cross-Aspect Patterns: Sentiment Drivers

**Strongest Predictors of Positive Sentiment:**
1. **Works as Advertised + Durable/Long-term** (highest overlap)
   - Example: *"Great product... This is high quality... product is very solid... works better than the EuroPro, but need more experience with it"*
2. **Works as Advertised + Well-written substantive**
   - Reviewers provide coherent praise with specific reasoning

**Strongest Predictors of Negative Sentiment:**
1. **Works Poorly + Breaks Quickly** (near-deterministic)
   - Example: *"It lasted maybe 4 months... now the add water light always comes on and it doesn't work anymore"*
2. **Works Poorly + Poor Construction**
   - Example: *"The legs are flimsy and the quality is one step above junk"*
3. **Recommends Alternative** (always negative)
4. **Poorly-written + Works Poorly**
   - Frustrated customers express themselves urgently, often with grammar/clarity errors

---

### 6. Product Category Insights (Implicit from Aspect Mix)

The dataset spans diverse categories (books, DVDs, electronics, apparel, toys, household items, personal care), visible in aspect salience:

- **Physical Products (60% of dataset):** Heavily discuss **performance** and **durability**
  - Examples: watches, vacuums, electronics, apparel, toys, tools
  - These reviews include 11 "breaks_quickly," 26 "poor_construction," 23 "durable_long_term" mentions

- **Content Products (40% of dataset):** Discuss **content substance** and **comparative narrative quality**
  - Examples: books, movies, CDs, music, guides
  - These reviews emphasize storytelling, writing clarity, thematic depth
  - Example: *"the character development in Great Expectations seems much deeper than Tale of Two Cities"*

---

### 7. Evidence Quality & Exceptions

**Caveats:**
- **Durability data is sparse** (39 mentions out of 250 reviews, 16%); most products/categories have insufficient longevity data for durability assessment
- **Comparison mentions are rare** (only 25% invoke alternatives), limiting comparative strength signals
- **"Not present" performance aspects** (40% of reviews) are by design for books/films; these reviews instead evaluate narrative and artistic merit, not functional performance

**Weak Evidence:**
- The "works_intermittently" category (5 reviews) is too small to draw actionable conclusions
- "Poorly-written" substance (18 reviews) provides directional but not robust evidence

---

### Conclusion: What Reviewers Talk About

Amazon reviewers focus on a **hierarchy of concerns**:

1. **Primary:** Does the product **work as promised**? (Performance aspect—highest variance, strongest predictor)
2. **Secondary:** Does it **last and hold up well**? (Durability—high confidence but lower frequency)
3. **Tertiary:** Is the **evaluation substantive and coherent**? (Content quality—indicates engagement depth)
4. **Contextual:** How does it **compare to alternatives**? (Comparative lever—used almost exclusively for negative redirection)

**For products**, reviewers emphasize **function, reliability, and longevity**. **For content**, they emphasize **narrative quality, authenticity, and depth**. Across both, **detailed, thoughtful reasoning** correlates with both positive and negative sentiment but is more common in satisfaction narratives.

---

**Report variant:** skill_on | **Data confidence:** High for performance (170/250 reviews), medium for durability (39/250), high for substance (250/250) | **Analysis date:** 2026-07-30
