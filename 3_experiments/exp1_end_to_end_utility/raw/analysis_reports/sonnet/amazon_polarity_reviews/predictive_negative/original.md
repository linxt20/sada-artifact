---
dataset: amazon_polarity_reviews
scenario: predictive_negative
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: predictive_feature_engineering
focus_variable: "label_pos"
query: "What review signals predict negative Amazon product satisfaction?"
source_table: augment_table/amazon_polarity_reviews/predictive_negative/original.csv
source_report: dataset_portion_2/substrate-claude-sonnet-4-6/amazon_polarity_reviews__predictive_negative/analyses/original/analysis.md
wall_seconds: 86.63
---

# Amazon Product Review Signals Predicting Negative Satisfaction
**Dataset:** `amazon_polarity_reviews__predictive_negative.csv` (250 reviews, `label_pos`: 0 = negative, 1 = positive)

---

## 1. Dataset Overview

The dataset contains 250 Amazon product reviews across diverse categories (electronics, books, media, physical goods, toys, etc.). Each review has:
- `label_pos`: binary label (0 = negative satisfaction, 1 = positive satisfaction)
- `title`: short headline written by the reviewer
- `content`: free-text body of the review

Approximately **half** the sample is negative (label_pos = 0). The focus variable is predicting when a review signals **negative** product satisfaction.

---

## 2. Key Signals Predicting Negative Reviews (label_pos = 0)

### 2.1 Title-Level Signals

**Negative titles use direct warning imperatives and extreme evaluations.** Highly reliable title patterns in negative reviews include:

| Title Pattern | Example (Review ID) |
|---|---|
| Explicit "DO NOT BUY" / "Skip it" / "Avoid" | AMZ-0002 ("Skip it."), AMZ-0205 ("DO NOT BUY"), AMZ-0033 ("DO NOT waste your money") |
| "Worst" superlatives | AMZ-0018 ("Worst Movie of All Time"), AMZ-0057 ("The worst movie I have ever seen.") |
| "Terrible" / "Horrible" | AMZ-0040 ("Terrible"), AMZ-0059 ("Horrible Movie!!!") |
| "Disappointing" / "Disappointed" | AMZ-0032 ("VERY DISAPPOINTING!"), AMZ-0121 ("VERY VERY DISAPPOINTED") |
| "Rip Off" / "Rip-Off" | AMZ-0064 ("RIP OFF!!"), AMZ-0113 ("Total RIP-OFF") |
| "Waste" of time/money | AMZ-0035 ("Soon You Will Understand..."), AMZ-0138 ("Waste of time.") |
| Quality degradation words: "poor," "cheap," "junk" | AMZ-0090 ("Poor Quality."), AMZ-0207 ("Cheap China Junk!") |
| Durability failures: "broke," "broken," "didn't last" | AMZ-0107 ("Latches broke after two days"), AMZ-0036 ("didn't last long") |

**Positive titles** by contrast use superlatives of praise ("Great," "Best," "Excellent," "Love," "Wonderful," "Awesome"), or simply describe the product neutrally.

---

### 2.2 Content-Level Signals

#### 2.2.1 Expressed Emotions and Evaluative Language

Negative reviews cluster around specific emotional and evaluative vocabulary in the body text:

- **Disappointment language**: "disappointed," "disappointing," "let down," "not what I expected" (AMZ-0026, AMZ-0058, AMZ-0115, AMZ-0121, AMZ-0226)
- **Non-recommendation language**: "I would not recommend," "don't buy," "stay away," "save your money," "save your dollars" (AMZ-0022, AMZ-0033, AMZ-0115, AMZ-0121)
- **Regret/waste language**: "waste of my time," "waste of money," "rip off," "feel totally ripped off" (AMZ-0057, AMZ-0213, AMZ-0064)
- **Explicit hate or disgust**: "I HATE this product," "I absolutely HATED this movie" (AMZ-0093, AMZ-0059)

#### 2.2.2 Product Failure Themes

The most consistent negative signal is **product malfunction or early failure**:
- Stopped working quickly: AMZ-0036 ("lasted maybe 4 months"), AMZ-0133 ("battery quit" after 4–5 months), AMZ-0150 ("worked for about a week then quit"), AMZ-0193 ("broke within a day")
- Defective out of the box: AMZ-0124 (displays "f76" error on first use), AMZ-0204 ("did not work" on hookup), AMZ-0250 ("Disc doesn't play on any DVD player")
- Physical breakage under normal use: AMZ-0107 (latch broke after two uses), AMZ-0189 ("wooden rod... broke once I filled it with clothes"), AMZ-0205 (gear shifter "broke off into my spokes")
- Performance falls short of advertised specs: AMZ-0062 (outputs 6V instead of 3V), AMZ-0245 (only 36.45 MB available, not 64 MB), AMZ-0133 (performance not impressive even when working)

#### 2.2.3 Poor Customer / Warranty Support

Negative reviews frequently escalate from product failure to **support failure**, amplifying dissatisfaction:
- AMZ-0085: warranty numbers "no longer in service," Amazon unable to help
- AMZ-0029: dealer changed return reason to avoid paying shipping; Amazon did not intervene
- AMZ-0124: Panasonic phone support "kept ringing busy"
- AMZ-0204: customer service put on hold twice

#### 2.2.4 Mismatch Between Expectations and Reality

Many negative reviews cite a gap between **marketing/description and actual product**:
- AMZ-0026: clock "said it comes set with time and date but mine didn't"; "impossible to read from any distance"
- AMZ-0116: humidifier leaked and destroyed hardwood floors despite a "mold free" claim
- AMZ-0165: humidifier is "definitely not mold free" despite product claim
- AMZ-0131: battery shipped was lower MAH than listed (bait and switch)
- AMZ-0044: hand warmers "do not heat" or produce minimal heat
- AMZ-0242: received fewer tracks than represented

#### 2.2.5 Content/Media Quality Complaints

For books, movies, music, and games, negative signal concentrates on:
- **Pacing problems**: "boring," "too slow," "dragged on" (AMZ-0063, AMZ-0238, AMZ-0215)
- **Shallow or one-dimensional characters**: AMZ-0103, AMZ-0111, AMZ-0151
- **Story/plot problems**: "doesn't make sense," "weak story" (AMZ-0022, AMZ-0122)
- **Not genre-appropriate**: AMZ-0091 ("expecting a romantic COMEDY... nothing funny"), AMZ-0038 ("not for the whole family")
- **Inferior to prior editions or related works**: AMZ-0226 (DVD missing key scenes vs. earlier edition), AMZ-0249 (album inferior to artist's prior work)

---

### 2.3 Structural / Linguistic Signals

- **All-caps usage** in content or title appears more often in negative reviews expressing strong frustration (AMZ-0033, AMZ-0040, AMZ-0121, AMZ-0211, AMZ-0218).
- **Very short content** (1–2 sentences) can go either way, but extremely terse dismissals are negatively associated: AMZ-0018 ("There are not enough bad things I can say..."), AMZ-0188 ("This movie just Stinks. The best thing about this movie, is the box.").
- **Comparative references to better alternatives** appear prominently in negatives: "get the electric one instead" (AMZ-0053), "There are far better books" (AMZ-0174), "much better resources on the web" (AMZ-0187).
- **Prior positive history followed by contrast** ("I usually like," "I've read every one of her books," "I loved the original"): Signals that the current product broke an established positive relationship (AMZ-0212, AMZ-0066, AMZ-0032).

---

## 3. Signal Summary Table

| Signal | Strength | Notes |
|---|---|---|
| Warning imperatives in title ("DO NOT BUY," "Avoid," "Skip") | **Strong** | Near-certain negative predictor |
| "Disappointing"/"Disappointed" in title or first sentence | **Strong** | Very frequent in negatives |
| Product stopped working / early failure described | **Strong** | Consistently negative |
| "Waste" of time/money in content | **Strong** | Highly reliable |
| Non-recommendation phrasing ("I would not recommend") | **Strong** | Reliable |
| Negative superlatives ("worst," "terrible," "horrible") in title | **Strong** | Reliable |
| Explicit "hate" or "absolutely hated" language | **Strong** | Reliable |
| Physical breakage under normal use | **Moderate–Strong** | Product-category dependent |
| Expectation–reality gap narrative | **Moderate** | Requires context to detect |
| Boredom/pacing complaints (media) | **Moderate** | Media category specific |
| All-caps frustration markers | **Moderate** | Noisy; also appears in positive hyperbole |
| Comparative alternatives ("try X instead") | **Moderate** | Reliable when combined with negatives |
| Prior positive + contrast narrative | **Moderate** | Useful contextual signal |

---

## 4. Exceptions and Weak Evidence

- **Ambiguous short titles**: Some titles like "my opinion" (AMZ-0053, negative) or "Refreshing" (AMZ-0249, negative) are not inherently negative and would mislead a title-only classifier.
- **Complimentary elements within negative reviews**: Some negative reviews acknowledge partial positives ("I gave it two stars because it did have a few funny parts" – AMZ-0038; "the only good thing... is the pictures" – AMZ-0186), making binary classification from sentiment alone imperfect.
- **Positively-titled negative reviews**: AMZ-0127 ("Great Sci-Fi British Camp Film") and AMZ-0128 ("Perfect, low-cost solution for low volume") carry label_pos = 0 despite warm-sounding titles — indicating the title alone is insufficient.
- **Weak or off-topic content**: AMZ-0095 (label = 0) is a plot summary with mild critique; AMZ-0149 (label = 0) is a request for author lists — not a product failure narrative.
- **Length is not decisive**: Long reviews appear in both classes; very short reviews similarly span both labels.

---

## 5. Decision-Ready Summary

The strongest predictors of **negative Amazon product satisfaction** (label_pos = 0) are:

1. **Title-level warning language** — imperative warnings ("DO NOT BUY," "Avoid"), failure descriptors ("broke," "didn't last"), or extreme negative evaluations ("worst," "terrible," "horrible," "disappointing").
2. **Reported product malfunction or early failure** in the review body — especially cessation of function after days to months, or defective-on-arrival experience.
3. **Explicit non-recommendation language** and waste framing ("waste of time/money," "rip off," "save your dollars").
4. **Expectation–reality mismatches** driven by misleading product descriptions or marketing claims.
5. **Escalation to support failure** — inability to get warranty or customer service resolution compounds and confirms negative sentiment.

A classifier combining title sentiment (negative keywords), content non-recommendation phrases, and product-failure descriptions would capture the dominant signal. Edge cases (mislabeled-seeming titles, partial positivity within negatives, off-topic reviews) constitute a meaningful minority (~10–15% of negatives observed) and represent the ceiling on simple lexical approaches.
