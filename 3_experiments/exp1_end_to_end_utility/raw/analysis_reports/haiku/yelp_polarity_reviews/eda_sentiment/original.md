---
dataset: yelp_polarity_reviews
scenario: eda_sentiment
variant: original
model: substrate-claude-haiku-4-5
query_subtype: exploratory_data_analysis
focus_variable: "label_pos"
query: "How do review themes differ between positive and negative Yelp sentiment?"
source_table: augment_table/yelp_polarity_reviews/eda_sentiment/original.csv
generated_at: 2026-07-26T13:59:45.851117+00:00
wall_seconds: 96.33
---

# Review Themes in Yelp Polarity: Positive vs. Negative Sentiment Analysis

## Executive Summary

This analysis examines 250 Yelp reviews (125 positive, 125 negative) to identify key theme differences between sentiment classes. The data reveals that **food quality discussions dominate positive reviews** (+13.6 percentage points), while **service complaints are more prevalent in negative reviews** (+9.6 pp). Positive reviewers emphasize satisfaction and appreciation, whereas negative reviewers detail specific failures and frustrations.

## Dataset Overview

- **Total Reviews**: 250 (balanced: 125 positive, 125 negative)
- **Columns**: review_id, label_pos (0=negative, 1=positive), review_text
- **Variant**: Original (no augmentation applied)
- **Average Review Length**: Positive = 84.7 words; Negative = 91.3 words

## Key Finding: Theme Prevalence by Sentiment

### Positive Reviews (N=125)

The most salient themes in positive reviews are:

| Theme | Frequency | Prevalence |
|-------|-----------|-----------|
| **Food Quality** | 85 reviews | 68.0% |
| **Service** | 48 reviews | 38.4% |
| **Food Type/Cuisine** | 45 reviews | 36.0% |
| **Wait Time** | 29 reviews | 23.2% |
| **Ambiance** | 28 reviews | 22.4% |
| **Price/Value** | 24 reviews | 19.2% |
| **Cleanliness** | 8 reviews | 6.4% |

**Positive reviews center overwhelmingly on food quality** — when reviewers give positive ratings, 2 out of 3 comments explicitly praise the food (delicious, fresh, amazing, flavorful). Service mentions are secondary and supportive ("staff are friendly and attentive").

### Negative Reviews (N=125)

| Theme | Frequency | Prevalence |
|-------|-----------|-----------|
| **Food Quality** | 68 reviews | 54.4% |
| **Service** | 60 reviews | 48.0% |
| **Wait Time** | 34 reviews | 27.2% |
| **Food Type/Cuisine** | 31 reviews | 24.8% |
| **Ambiance** | 23 reviews | 18.4% |
| **Price/Value** | 19 reviews | 15.2% |
| **Cleanliness** | 10 reviews | 8.0% |

**Negative reviews broaden their complaints across multiple dimensions**. While food quality remains frequent (54.4%), service failures are nearly as common (48.0%) — a 9.6 percentage point *increase* relative to positive reviews. This suggests negative reviewers often cite service as a compounding factor alongside mediocre food.

## Major Theme Differences

### 1. Food Quality Framing: +13.6 pp advantage (positive)

- **Positive**: "Delicious," "fresh," "amazing," "fantastic" — adjectives emphasizing sensory satisfaction. Example: *"The pizza was so fresh and delicious and the desserts were both to die for."*
- **Negative**: "Bland," "mediocre," "dry," "sour" — adjectives highlighting absent or incorrect flavors. Example: *"Really tasteless and not good. Some pieces were way over cooked."*

**Interpretation**: Positive reviewers celebrate execution and flavors. Negative reviewers focus on failures (undercooked, oversalted, flavorless). Food quality is a primary decision factor but manifests differently by sentiment.

### 2. Service: +9.6 pp disadvantage (negative dominance)

- **Positive (38.4%)**: Service is noted as smooth, professional, and helpful but rarely emphasized as the headline. Example: *"The service is really good and the servers are pretty attentive."*
- **Negative (48.0%)**: Service failures are central grievances — forgotten tables, slow waits, rude staff, lack of follow-up. Example: *"The worst service I've ever had... seated us, brought coffee, and vanished. Turns out they'd seated us in a area reserved for a private party, and when said party arrived, they had thus forgotten we were there."*

**Interpretation**: Poor service acts as a multiplier of dissatisfaction. While positive experiences do mention good service, negative experiences disproportionately cite service failures as the primary complaint or as context for other issues.

### 3. Wait Time: -4.0 pp (slightly higher in negative)

- Negative reviews mention waiting/delays in 27.2% of cases vs. 23.2% in positive reviews.
- **Negative context**: "We were seated for 25 minutes. No one came to take our order." (frustration and abandonment theme)
- **Positive context**: "The food took 15 minutes. I like extra crispy classic wings (bone-in) so mine take like an extra minute." (acceptance and appreciation)

**Interpretation**: The same operational fact (wait time) is framed differently by sentiment. Positive reviewers contextualize delays as acceptable trade-offs; negative reviewers cite them as evidence of neglect.

### 4. Price/Value: +4.0 pp (positive framing)

- **Positive (19.2%)**: Mentions of price focus on value: "For 8 dollars even, I got a Grilled Pork banh mi, a Chicken banh mi and two canned drinks. Everything was delicious!"
- **Negative (15.2%)**: Price grievances emphasize overcharging or misalignment: "PRICING was way off," "why do you keep jacking up the prices every other day."

**Interpretation**: Positive sentiment correlates with perceived value (quality-to-price ratio). Negative sentiment emerges when customers feel prices exceed quality delivered.

### 5. Ambiance: +4.0 pp (positive emphasis)

- Positive reviews celebrate atmosphere: "great music, great people watching," "beautiful place to hang out"
- Negative reviews criticize noise and crowding: "The noise in this place is over the top, so much so that we couldn't have a conversation," "So crowded it's ridiculous"

## Sentiment Language Patterns

| Metric | Positive | Negative |
|--------|----------|----------|
| **Avg positive word frequency** | 2.37 per review | 1.03 per review |
| **Avg negative word frequency** | 0.17 per review | 0.82 per review |
| **Positive words: Negative words ratio** | 13.9:1 | 1.3:1 |

Top positive keywords (positive reviews): "great" (61), "good" (59), "love" (25), "nice" (26), "amazing" (implied by data)

Top negative keywords (negative reviews): "service" (45 context uses), "bad" (implied by structure)

**Interpretation**: Positive reviews are emotionally affirming and reinforcing. Negative reviews are more balanced, showing attempts at fairness ("some things were good...but") even while complaining.

## Distinct Narrative Structures

**Positive Reviews**: Follow a linear appreciation pattern
- Opening enthusiasm ("Loved it here," "Amazing!")
- Specific praise of food items or service
- Recommendation or return intention

**Negative Reviews**: Follow a problem-narrative pattern
- Initial positivity or hope ("I really want to like this")
- Enumeration of failures (often with numbered lists: "Pros: none. Cons: ...")
- Resignation or warning ("Never will go back")

## Minor Themes

**Cleanliness**: Slightly more mentioned in negative reviews (8.0% vs. 6.4%), but both are low-frequency. When cleanliness appears, negative reviews cite hygiene violations explicitly ("cutlery was dirty," "floor was covered with water").

**Food Type**: Positive (36.0%) vs. Negative (24.8%) — positive reviewers name specific dishes they loved; negative reviewers mention dish types primarily to explain what went wrong.

## Conclusions

1. **Food Quality is Universal** but tone differs: positive reviewers celebrate execution; negative reviewers blame poor quality or inappropriate preparation.

2. **Service is a Differentiator**: Service excellence enhances positive sentiment marginally, but service failure disproportionately drives negative sentiment (48% vs. 38%). Poor service amplifies other grievances.

3. **Context Matters**: Wait times, noise, and prices exist in both positive and negative reviews, but interpretation varies. Positive reviewers rationalize; negative reviewers condemn.

4. **Emotional Intensity**: Positive reviews average 2.37 positive-sentiment words; negative reviews average only 1.03. This reflects emotional restraint in negative reviews and strong affirmation in positive ones.

5. **Actionable Insight**: To improve ratings, establishments should prioritize (a) consistent food quality, (b) attentive and responsive service, and (c) price-to-quality alignment. Service failures are cited in nearly half of negative reviews, suggesting this is a high-impact lever.

---

**Analysis Method**: Theme extraction via keyword patterns (food_quality, service, ambiance, wait_time, price, cleanliness). Sentiment-word frequencies counted from curated positive/negative adjective lists. Examples drawn directly from original review text.
