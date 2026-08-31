---
dataset: amazon_polarity_reviews
scenario: predictive_sentiment
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: exploratory_data_analysis
focus_variable: "label_pos"
query: "How do review facets differ by sentiment label?"
source_table: augment_table/amazon_polarity_reviews/predictive_sentiment/original.csv
source_report: dataset_portion_2/substrate-claude-sonnet-4-6/amazon_polarity_reviews__predictive_sentiment/analyses/original/analysis.md
wall_seconds: 72.21
---

# Review Facets by Sentiment Label — Amazon Polarity Reviews

## Dataset Overview

The dataset contains **250 Amazon reviews** (AMZ-0001 to AMZ-0250) spanning a wide range of product categories (books, movies/DVDs, music/CDs, electronics, toys, clothing, food, and more). Each review has four fields:

| Column | Description |
|--------|-------------|
| `review_id` | Unique ID |
| `label_pos` | Sentiment label: **1 = Positive**, **0 = Negative** |
| `title` | Short review headline |
| `content` | Full review body |

A rough count of the visible records shows the two classes are **approximately balanced**, with both labels well-represented across the 250 rows (~120–130 per class based on sampling).

---

## 1. Title Tone and Style

**Positive reviews (label = 1)** tend to have titles that are brief, enthusiastic affirmations:
- e.g., *"Great Book"*, *"Fun!"*, *"Excellent!!!"*, *"Love these!"*, *"Best of the three solo records"*, *"Awesome"*
- Superlatives and exclamation marks are common.
- Titles frequently match the content sentiment without hedging.

**Negative reviews (label = 0)** show markedly different title patterns:
- Direct warnings or imperatives: *"DO NOT BUY"*, *"DO NOT waste your money"*, *"Skip it."*, *"Avoid this cheap product!"*
- Emphatic disappointment markers: *"VERY DISAPPOINTING!"*, *"VERY VERY DISAPPOINTED"*, *"Total RIP-OFF"*, *"Horrible Movie!!!"*
- Sarcastic titles that appear positive but signal irony in context: *"Great for a year then disconnects"* (AMZ-0020), *"Good marketing. Bad product"* (AMZ-0165), *"Perfect, low-cost solution for low volume"* (AMZ-0128 — a complaint about audio volume).
- All-caps emphasis appears almost exclusively in negative titles.

> **Exception**: A small number of negative reviews have neutrally-worded titles (e.g., *"Shower caps"*, AMZ-0052; *"my opinion"*, AMZ-0053), suggesting title sentiment is not a perfect signal on its own.

---

## 2. Content Length and Elaboration

**Positive reviews** vary widely in length:
- Short positive endorsements are common: *"As always Martha has done her self justice..The Receipts are accurate and varied for all tastes.."* (AMZ-0010); *"great for all ages keeps you reading till the end."* (AMZ-0179).
- Longer positive reviews tend to focus on **what the reviewer enjoyed** — characters, plot, sound quality, durability, taste — with specific and affectionate detail.

**Negative reviews** also vary in length, but a notable pattern emerges:
- Many negative reviews are **elaborately detailed in their complaints**, listing multiple failure points: broken parts, warranty issues, incorrect specifications, product degradation over time (e.g., AMZ-0085 on a generator, AMZ-0116 on a humidifier, AMZ-0124 on a receiver, AMZ-0133 on a robotic cleaner).
- Some negative reviews are very short and blunt: *"It never works..."* (AMZ-0233); *"NO GOOD! the Disc doesn't play on any DVD player."* (AMZ-0250).

---

## 3. Linguistic Markers

### Positive (label = 1) content patterns:
- **Affective verbs**: *love*, *enjoy*, *recommend*, *impressed*, *pleased*, *thrilled*, *delight*
- **Amplifiers**: *excellent*, *outstanding*, *wonderful*, *fantastic*, *perfect*, *superb*
- **Personal endorsement phrasing**: *"I would recommend to everyone"*, *"can't put it down"*, *"well worth the money"*
- **Narrative engagement**: Reviewers often share anecdotes about friends, family, or repeat purchases (e.g., AMZ-0004 passing cream to family; AMZ-0139 noting 20 years of use).

### Negative (label = 0) content patterns:
- **Warning imperatives**: *"Stay away"*, *"Don't buy"*, *"Save your money"*, *"avoid"*
- **Disappointment/failure framing**: *"waste of time/money"*, *"did not work"*, *"broke after X days"*, *"not worth it"*, *"terrible"*, *"lousy"*
- **Comparative downgrading**: Negative reviews frequently compare unfavorably: *"not as good as"*, *"not worth the price"*, *"much better options exist"* (e.g., AMZ-0007 comparing models; AMZ-0187 preferring free web resources; AMZ-0155 preferring another author).
- **Explicit emotional distress**: *"I HATE this product"* (AMZ-0093); *"my blood pressure was off the scale"* (AMZ-0043).

---

## 4. Product/Category Facets

The dataset spans multiple categories. Within the observable records:

| Category | Positive label examples | Negative label examples |
|---|---|---|
| Books | Detail on characters, plot, writing style | Slow pacing, biased content, incorrect info |
| Movies/DVDs | Cast praise, story engagement | Waste of time, poor plot, production issues |
| Music/CDs | Musical quality, specific track praise | Disappointing compared to prior albums |
| Electronics/Hardware | Durability, performance, ease of use | Broken quickly, poor customer support, defective units |
| Toys/Gifts | Kids loved it, good value | Broke quickly, didn't work as advertised |
| Physical products (clothing, tools) | Fit, material quality | Poor construction, short lifespan |

**Cross-category pattern**: The fundamental facet distinction is **performance vs. expectation**. Positive reviews confirm or exceed expectations; negative reviews describe a gap — the product/content failed to meet what was promised or implied.

---

## 5. Review Reliability and Specificity

**Positive reviews** range from highly specific (detailed description of features, anecdotal evidence of long-term use) to very brief and generic (*"great"*, *"love it"*, *"good"*). The very short positive reviews may present weaker evidence of quality.

**Negative reviews** are generally more specific in their criticism. Reviewers name exact failure modes (e.g., *"f76 flashing on the screen"*, AMZ-0124; *"gear shifter boke off into my spokes"*, AMZ-0205; *"lens refused to retract"*, AMZ-0197). This specificity makes negative reviews more informative as signals of genuine product defect.

> **Notable exception**: Several reviews labeled negative contain mixed or ambiguous signals — e.g., AMZ-0127 (*"Great Sci-Fi British Camp Film"*) is labeled 0 but reads as nostalgic appreciation with mild caveats; AMZ-0128 (*"Perfect, low-cost solution for low volume"*) is labeled 0 despite appearing to describe a problem solved. These cases indicate the label `label_pos = 0` may capture 3-star "mixed" reviews that the dataset binarizes as negative.

---

## 6. Summary of Key Differentiating Facets

| Facet | Positive (label = 1) | Negative (label = 0) |
|---|---|---|
| **Title tone** | Affirming, short, exclamatory | Warning, disappointed, sarcastic or emphatic |
| **Emotional register** | Joy, satisfaction, enthusiasm | Frustration, anger, regret, disappointment |
| **Specificity of praise/complaint** | Ranges from vague to detailed | Generally specific about failure modes |
| **Temporal framing** | Past positive use, ongoing use, gift-giving | Short lifespan, regression over time, never worked |
| **Recommendation intent** | Recommend, buy, must-have | Warn, avoid, return/refund |
| **Comparative framing** | Exceeds expectations, better than alternative | Below expectations, prefer cheaper/different option |
| **Product interaction narrative** | Smooth experience, continued use | Defect, support failure, workarounds required |

---

## Decision-Ready Conclusion

The clearest predictive facets for `label_pos` are: (1) **title sentiment and warning language**, (2) **recommendation vs. deterrence phrasing** in the content, and (3) **temporal narratives of failure** (broke after N days/weeks) which are strongly concentrated in negative reviews. Mixed or hedged reviews do exist (primarily labeled 0), so models should be cautious about treating all non-enthusiastic language as definitively negative.
