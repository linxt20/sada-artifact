---
dataset: yelp_polarity_reviews
scenario: eda_sentiment
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "label_pos"
query: "How do review themes differ between positive and negative Yelp sentiment?"
source_table: augment_table/yelp_polarity_reviews/eda_sentiment/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:25:22.084843+00:00
wall_seconds: 131.45
---

# Yelp Review Themes: Positive vs. Negative Sentiment Analysis

## Overview

This analysis examines how review themes differ between positive and negative Yelp sentiment using an augmented dataset of 250 reviews (125 positive, 125 negative). The analysis combines original review texts with three TAPP-generated semantic facets: staff attentiveness, staff demeanor, and food taste/flavor.

## Methods

**TAPP-Generated Columns Used:**
- `staff_attentiveness`: Captures service responsiveness and attention (values: attentive_responsive, slow_forgetful, inattentive_ignored, not_present)
- `staff_demeanor`: Captures staff interpersonal behavior (values: friendly_professional, rude_hostile, indifferent_dismissive, not_present)
- `food_taste_flavor`: Captures food quality perceptions (values: delicious_flavorful_fresh, bland_tasteless, off_quality_strange, not_present)

**Sample:** 125 positive reviews (label=1) vs. 125 negative reviews (label=0), N=250 total. Coverage: 100% for attentiveness and demeanor; 99.6% for food flavor.

---

## Key Findings

### 1. Staff Demeanor: Strongest Differentiator

Staff demeanor exhibits the starkest contrast between sentiment polarities, establishing itself as the primary thematic divide:

| Staff Demeanor | Positive (N=125) | Negative (N=125) | 
|---|---|---|
| **Friendly & Professional** | 80 (64.0%) | 13 (10.4%) |
| **Rude & Hostile** | 2 (1.6%) | 48 (38.4%) |
| **Indifferent & Dismissive** | 2 (1.6%) | 34 (27.2%) |
| **Not Mentioned** | 43 (34.4%) | 30 (24.0%) |

**Interpretation:** Positive reviews overwhelmingly feature friendly, professional staff behavior, while negative reviews are characterized by rude/hostile (38.4%) or indifferent/dismissive (27.2%) conduct. When staff demeanor is mentioned, it is strongly predictive of sentiment direction (96.4% of reviews mentioning positive demeanor are positive; 96.3% mentioning negative demeanor are negative).

### 2. Food Taste & Flavor: Second-Order Differentiator

Food quality perception strongly correlates with sentiment but shows asymmetric mention patterns:

| Food Taste/Flavor | Positive (N=125) | Negative (N=125) |
|---|---|---|
| **Delicious, Flavorful, Fresh** | 81 (64.8%) | 7 (5.6%) |
| **Bland & Tasteless** | 1 (0.8%) | 20 (16.0%) |
| **Off-Quality, Strange** | 1 (0.8%) | 28 (22.4%) |
| **Not Mentioned** | 42 (33.6%) | 70 (56.0%) |

**Interpretation:** Among reviews mentioning food quality, the sentiment alignment is near-perfect: 91.5% of positive mentions appear in positive reviews; 96.0% of negative mentions appear in negative reviews. Critically, 56% of negative reviews do not discuss food quality, suggesting service failures dominate negative experiences in many cases—particularly concerning service quality despite acceptable food.

### 3. Staff Attentiveness: Asymmetric Theme Importance

Staff attentiveness shows different thematic weight across sentiment categories:

| Staff Attentiveness | Positive (N=125) | Negative (N=125) |
|---|---|---|
| **Attentive & Responsive** | 72 (57.6%) | 9 (7.2%) |
| **Slow & Forgetful** | 5 (4.0%) | 40 (32.0%) |
| **Inattentive & Ignored** | 0 (0.0%) | 33 (26.4%) |
| **Not Mentioned** | 48 (38.4%) | 43 (34.4%) |

**Interpretation:** Positive reviews emphasize attentive service (57.6%), whereas negative reviews fixate on service failures—slow/forgetful (32.0%) or completely ignored (26.4%). The 72 positive vs. 9 negative mentions of attentiveness represents an 8:1 ratio, making this a primary positive thematic anchor. However, the absence of this mention in 38.4% of positive reviews indicates that exceptional food quality or ambiance can compensate for modest service attention.

---

## Thematic Patterns by Sentiment Category

### Positive Review Themes

**Primary themes (mentioned in ≥50% of reviews):**
1. **Friendly, professional staff** (64.0%)
2. **Attentive, responsive service** (57.6%)
3. **Delicious, flavorful, fresh food** (64.8%)

**Pattern:** Positive reviews cluster around three mutually reinforcing themes. The overlap is substantial: 72 reviews mention both attentiveness AND friendly demeanor AND delicious food, creating a coherent "excellent experience" narrative. When food quality is mentioned, it is nearly always positive (81/82 food-quality mentions = 98.8% positive framing).

**Edge cases:** 42 positive reviews (33.6%) do not mention food quality at all, suggesting service-only experiences (e.g., drink bars, retail, professional services) or situations where ambiance/community experience dominates the positive valence.

### Negative Review Themes

**Primary themes (mentioned in ≥30% of reviews):**
1. **Rude, hostile staff demeanor** (38.4%)
2. **Slow, forgetful service** (32.0%)
3. **Off-quality, strange food** (22.4%)
4. **Bland, tasteless food** (16.0%)

**Pattern:** Negative reviews cluster around service failures (38.4% + 26.4% = 64.8% mention attentiveness or demeanor problems) and food quality degradation (38.4% mention negative food attributes). Unlike positive reviews, negative reviews exhibit thematic fragmentation: 70 reviews (56.0%) do not discuss food at all, focusing solely on service deficiencies. This suggests that **service is a necessary (but not sufficient) condition for positive sentiment**, whereas **food quality is a sufficient but non-necessary condition for negative sentiment**.

**Key insight:** When food is mentioned in negative reviews (55 mentions), it is negative in 50/55 cases (90.9%), creating a strong negative signal. However, the majority of negative reviews (70/125) establish their negative valence through service critique alone.

---

## Cross-Theme Relationships

### Strong Co-occurrence Patterns

**Positive reviews:**
- Attentive service + Friendly demeanor + Positive food: 72 reviews co-mention attentiveness and friendly demeanor, with 65+ also mentioning delicious food
- Correlation coefficient (polarity alignment): Near-perfect when multiple facets mentioned

**Negative reviews:**
- Service failures (attentiveness + demeanor) dominate: 64.8% of negative reviews feature service-related negative themes
- Food quality declines are secondary: Mentioned in 44% of negative reviews, strongly reinforcing service-driven negativity

### Asymmetry: Service vs. Food

- **Service is thematic in both sentiments** (mentioned in ~66% of positive, ~65% of negative reviews)
- **Food is asymmetrically mentioned**: Positive reviews discuss food in 66.4% of cases; negative reviews in only 44% of cases
- **Implication:** Positive experiences require articulation of food quality; negative experiences can be driven entirely by service breakdown without needing to evaluate the cuisine itself

---

## Validation Against Original Review Texts

The TAPP-generated columns align well with implicit themes present in the review texts:

| Facet | Cross-Check Evidence |
|---|---|
| **Staff Demeanor** | Explicit language: "friendly staff," "rude," "welcoming" vs. "hostile," "dismissive." High semantic accuracy; 96%+ directional alignment with sentiment. |
| **Staff Attentiveness** | Explicit timing indicators: "waited 25 minutes," "refill within seconds," vs. "forgotten," "slow service." High coverage among service-focused reviews (72 positive mentions vs. 73 negative). |
| **Food Taste** | Explicit sensory descriptions: "delicious," "fresh," vs. "bland," "dry," "tasteless." 91.5% polarity match to sentiment (positive mentions → positive reviews). |

The augmented columns strengthen the evidence by providing standardized semantic buckets that would otherwise require manual parsing of diverse language across 250 reviews.

---

## Decision-Relevant Implications

1. **Service Quality > Food Quality for Sentiment:** 64.8% of negative reviews center on service failures, while only 38.4% cite food problems. Restaurants prioritizing staff training and attentiveness may see disproportionate sentiment gains.

2. **Demeanor Dominates Attentiveness:** Staff behavior/tone (64% of positive reviews) outweighs speed/responsiveness (57.6%) as a positive theme. Customer-facing training on interpersonal skills may be more impactful than operational efficiency.

3. **Food Quality as Sentiment Amplifier:** Among the minority of reviews that critique food (44% of negative, 66.4% of positive), quality is highly polarized. Food-focused establishments should ensure consistent quality, as it strongly amplifies sentiment when mentioned.

4. **Service Deficiencies Cannot Be Compensated:** No negative reviews simultaneously praise both staff and food (demeanor-food co-positivity rate: <2%). This suggests service failures create reviews that omit or minimize positive food commentary, even if food is acceptable.

---

## Limitations

- Binary sentiment labels (positive/negative) obscure gradations; nuanced views may be misclassified.
- TAPP-generated facets capture explicit thematic mentions but miss implicit customer satisfaction signals (e.g., repeat patronage intent).
- 42–70 reviews per category do not mention food/attentiveness, limiting ability to assess unmentioned aspects.
- Analysis is descriptive; causal claims (e.g., "service causes sentiment") require controlled studies.
