---
dataset: yelp_polarity_reviews
scenario: eda_sentiment
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "label_pos"
query: "How do review themes differ between positive and negative Yelp sentiment?"
source_table: augment_table/yelp_polarity_reviews/eda_sentiment/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:23:48.194375+00:00
wall_seconds: 39.84
---

# Yelp Review Theme Differences by Sentiment

## Dataset Overview

- **250 reviews** (125 positive `label_pos=1`, 125 negative `label_pos=0`), balanced by design.
- Four augmented theme columns: `service_staff_behavior`, `food_quality_signal`, `food_freshness_issue`, `return_intent`.

---

## Key Theme Differences

### 1. Service & Staff Behavior

| Category | Negative (%) | Positive (%) |
|---|---|---|
| `rude_hostile` | **43.5** | 1.4 |
| `indifferent_neglectful` | **41.3** | 1.4 |
| `friendly_attentive` | 10.9 | **82.9** |
| `professional_helpful` | 0.0 | 8.6 |

Staff behavior is the **strongest differentiator**. Negative reviews are dominated by hostility or indifference (~85% combined), while positive reviews are overwhelmingly associated with friendly or professional staff (~91%).

---

### 2. Food Quality Signal

| Category | Negative (%) | Positive (%) |
|---|---|---|
| `excellent_standout` | 1.6 | **38.4** |
| `good_solid` | 5.6 | **21.6** |
| `poor_disappointing` | **22.4** | 0.0 |
| `mediocre_average` | **18.4** | 1.6 |
| `not_assessed` | 51.2 | 38.4 |

Positive reviews frequently call out excellent or solid food (~60% assessed positively), while negative reviews cluster around poor/mediocre quality (~40% assessed negatively). A large share of both polarities did not explicitly assess food, suggesting many reviews focus primarily on service.

---

### 3. Food Freshness Issues

| Category | Negative (%) | Positive (%) |
|---|---|---|
| `fresh_well_prepared` | 3.2 | **55.2** |
| `not_present` (no signal) | **84.8** | 44.0 |
| `stale_old` / `hygiene` / `temperature` | ~9.6 | ~0.8 |

Freshness signals are sparse in negative reviews—most simply omit them—but when present in positive reviews, they strongly reinforce satisfaction. Freshness complaints are a minority signal in negative reviews, implying they are a secondary theme.

---

### 4. Return Intent

| Category | Negative (%) | Positive (%) |
|---|---|---|
| `explicit_will_return` | 0.0 | **21.6** |
| `likely_will_return` | 0.0 | 4.0 |
| `unlikely_will_return` | 8.0 | 0.0 |
| `explicit_will_not_return` | **24.0** | 0.0 |
| `neutral_uncertain` | 68.0 | 74.4 |

Return intent is polarized cleanly: positives express intent to return, negatives express the opposite. However, **~70% of both groups are neutral/uncertain**, limiting this as a standalone classifier.

---

## Summary of Theme Patterns

| Theme | Positive Reviews | Negative Reviews |
|---|---|---|
| **Service** | Friendly, professional | Rude or indifferent |
| **Food quality** | Excellent/good (when assessed) | Poor/mediocre (when assessed) |
| **Freshness** | Fresh & well-prepared | Mostly not flagged (secondary theme) |
| **Return intent** | Explicit return intent | Explicit avoidance (but majority neutral) |

## Caveats & Weak Evidence

- **Freshness complaints** are sparse even in negatives (~9%), so this dimension is a weak discriminator alone.
- **~50% of negative reviews** and ~38% of positive reviews omit explicit food quality signals, suggesting service experience often drives the overall rating regardless of food.
- The dataset is perfectly balanced (125/125), which limits inference about real-world base rates.
