---
dataset: yelp_polarity_reviews
scenario: focus_inference
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What aspects of their experience are Yelp reviewers talking about?"
source_table: augment_table/yelp_polarity_reviews/focus_inference/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:26:55.276627+00:00
wall_seconds: 83.68
---

# Analysis Report: Aspects of Experience in Yelp Polarity Reviews

## Query
**What aspects of their experience are Yelp reviewers talking about?**

**Dataset:** haiku__skill_off_update.csv | **Variant:** skill_off | **Rows:** 250 reviews

---

## Executive Summary

Yelp reviewers primarily discuss **food/product quality** and **service** as the core dimensions of their experience, followed by wait time, price, and facility/atmosphere. Most reviews focus on multiple aspects (mean 2.35), indicating that customer experience perception is multifaceted. However, negative reviews place significantly more emphasis on service failures than positive reviews, while positive reviews lean more heavily on food quality and price value.

---

## Key Findings

### 1. Dominant Experience Aspects (Overall Frequency)

The six measurable aspects reveal a clear hierarchy:

| Aspect | Frequency | % of Reviews |
|---|---|---|
| **Food Quality** | 141 | 56.4% |
| **Service** | 137 | 54.8% |
| **Wait Time** | 99 | 39.6% |
| **Price** | 85 | 34.0% |
| **Ambiance/Atmosphere** | 66 | 26.4% |
| **Cleanliness** | 59 | 23.6% |

**Interpretation:** Food and service are quasi-equal frontrunners, each mentioned in roughly half of all reviews. These form the primary lens through which reviewers evaluate their experience. Wait time emerges as a secondary concern (39.6%), while cleanliness and ambiance are tertiary (24–26%).

### 2. Sentiment Contrast: Positive vs. Negative Reviews

Aspect mention patterns differ markedly by review sentiment (125 positive, 125 negative):

#### Positive Reviews (label_pos = 1)
- **Food Quality:** 60.8%
- **Service:** 47.2%
- **Price:** 40.0%
- **Wait Time:** 39.2%
- **Ambiance:** 28.8%
- **Cleanliness:** 21.6%

#### Negative Reviews (label_pos = 0)
- **Service:** 62.4% ⬆️
- **Food Quality:** 52.0% ⬇️
- **Wait Time:** 40.0% ≈
- **Cleanliness:** 25.6%
- **Price:** 28.0% ⬇️
- **Ambiance:** 24.0%

**Key Observations:**
- **Service problems dominate negative reviews** (+15.2 percentage points vs. positive). Reviewers emphasize rude staff, slow service, forgotten orders, and staff unavailability when dissatisfied.
- **Food quality is more frequently praised** in positive reviews (+8.8 percentage points). Reviewers celebrate taste, freshness, portion size, and creativity when satisfied.
- **Price discussions shift tone:** Positive reviews mention price (40%), often in the context of value; negative reviews mention it less (28%), suggesting pricing complaints are less central to dissatisfaction than service or food quality failures.
- **Wait time and cleanliness remain relatively stable** across sentiment, indicating these are consistent concern areas when they arise, regardless of overall satisfaction.

### 3. Aspect Co-occurrence and Complexity

Most reviews blend multiple aspects:

| Aspects per Review | Count | % |
|---|---|---|
| 0 aspects | 21 | 8.4% |
| 1 aspect | 58 | 23.2% |
| 2 aspects | 54 | 21.6% |
| 3 aspects | 61 | 24.4% |
| 4+ aspects | 56 | 22.4% |

**Average:** 2.35 aspects per review | **Max:** 6 aspects in a single review

**Interpretation:** Only 8.4% of reviews mention no measurable aspect (e.g., policy-focused or non-service reviews like "they don't take coins anymore"). Nearly 77% of reviews cite 2+ aspects, underscoring that customer experience evaluations are inherently multidimensional. Complex reviews (4–6 aspects) comprise 22% of the dataset and often represent detailed critical analyses or comprehensive praise.

### 4. Experience Aspect Priorities by Review Pattern

- **High-intensity reviews** (4+ aspects) most often combine service failures with food/cleanliness issues or facility complaints, suggesting that negative experiences tend to compound across dimensions.
- **Single-aspect reviews** (23.2%) are most common for food-only or service-only praise, reflecting focused positive feedback ("the fries were great," "staff was wonderful").
- **Zero-aspect reviews** (21 reviews, 8.4%) include policy discussions, general impressions, or non-hospitality businesses (e.g., retail, healthcare, auto services) where the standard aspect taxonomy is less applicable.

---

## Concrete Evidence from Text Examples

### Food Quality Focus
> "Mac and cheese is splendid.... Succulent fried chicken..... A hit!!!" *(positive, food-only)*

> "The sushi wasn't great, my table was dirty and so were the ones around me, and the service was slow." *(negative, multi-aspect: food, cleanliness, service)*

### Service Focus
> "Michelle at Fore Peaks is a true professional. She has assisted many mutual clients find homes in and around Fountain Hills." *(positive, service-only)*

> "The worst service I've ever had. We were seated, they vanished. Turns out they'd seated us in an area reserved for a private party and forgotten us." *(negative, multi-aspect: service, wait)*

### Price Value
> "For 8 dollars even, I got a Grilled Pork banh mi, a Chicken banh mi and two canned drinks. Everything was delicious!" *(positive, price emphasized as good value)*

> "Charged me an extra $1.65 for guacamole. That's like another 2 burritos from Taco Bell, what a ripped off and never coming back." *(negative, price as grievance)*

### Wait Time & Atmosphere
> "Waited at the bar for 45 minutes to order food... nice place, food looks great. Wouldn't know how it tasted." *(negative, wait + implicit appetite dampening from atmosphere delay)*

---

## Limitations and Caveats

1. **No aspect mentions for ~21 reviews:** These are edge cases (generic statements, policy concerns, non-food businesses) where the six-aspect framework does not apply. Analysis is robust for the 229 reviews with ≥1 aspect.

2. **Service and Food quality near-equal but context-dependent:** While both are ~55%, their *impact* differs: negative food reviews often include a silver lining (e.g., "food was bad, but service was great"), whereas negative service reviews rarely find compensation. This suggests service failures may have higher perceived severity.

3. **Cleanliness and Ambiance are lower-frequency:** These aspects are taggable and actionable but emerge as concerns in ~24% and ~26% of reviews respectively, making them secondary drivers of satisfaction/dissatisfaction compared to the core food and service dimensions.

4. **Variant Limitation:** The `skill_off` label indicates this augmentation was generated with a lower-capability model or without specialized skill injection, so aspect precision may vary. Reviews relying on implicit references to aspects (e.g., "they took forever" without explicit "wait") might be undertagged.

---

## Conclusion

Yelp reviewers conceptualize their experience primarily through **food/product quality and service**, two nearly equiprobable lenses that together appear in ~75% of all reviews. **Service problems are the primary driver of negative ratings**, while **food quality and perceived value drive positive ratings**. Secondary concerns—wait time (40% of reviews), price (34%), and facility cleanliness/ambiance (24–26%)—act as modifiers that either compound dissatisfaction or enhance satisfaction, but rarely stand alone as the sole focus.

This multidimensional, sentiment-asymmetric structure suggests that:
- **For positive experiences:** Food quality and fair pricing are the anchors; good service is expected but not mentioned as often.
- **For negative experiences:** Service failures, food disappointments, and hygiene/cleanliness issues drive reviews; reviewers often layer complaints across dimensions.

Future interventions should prioritize service reliability and food quality consistency, as these are the primary conversation drivers, with cleanliness and wait-time management as important secondary levers.
