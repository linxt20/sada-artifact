---
dataset: yelp_polarity_reviews
scenario: eda_sentiment
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "label_pos"
query: "How do review themes differ between positive and negative Yelp sentiment?"
source_table: augment_table/yelp_polarity_reviews/eda_sentiment/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:24:04.040358+00:00
wall_seconds: 53.17
---

# Review Theme Differences Between Positive and Negative Yelp Sentiment

**Dataset:** 250 Yelp reviews (125 positive `label_pos=1`, 125 negative `label_pos=0`), balanced split.  
**Query:** How do review themes differ between positive and negative Yelp sentiment?

---

## Method Note

TAPP-generated columns used in this report: `service_staff_conduct`, `food_quality_signal`, `food_praised_highlight`, `atmosphere_ambiance_signal`, `return_recommend_intent`. All five columns were cross-tabulated against the original outcome variable `label_pos`. No TAPP column substituted for raw text evidence; all claims are quantified against `label_pos`.

---

## Key Findings Summary

| Theme | Positive Signal (pos count / neg count) | Negative Signal (pos count / neg count) |
|---|---|---|
| **Service** | Friendly/positive: 53 / 6 | Rude/dismissive: 0 / 27; Indifferent: 0 / 17 |
| **Food quality** | Excellent standout: 46 / 1 | Poor/bland: 0 / 27; Mediocre: 4 / 24 |
| **Food highlight** | Specific dish praised: 52 / 4 | (no positive equivalent in neg) |
| **Atmosphere** | Positive (lively/special): 25 / 5 | Noisy/run-down: 3 / 17 |
| **Return intent** | Explicit return yes: 31 / 1 | Explicit return no: 0 / 35; Warn others: 0 / 13 |

---

## 1. Service & Staff Conduct — The Dominant Differentiator

`service_staff_conduct` shows the sharpest separation between sentiment classes:

- **42% of positive reviews** mention friendly/attentive staff (`friendly_positive`: 53/125) vs. only 5% of negatives (6/125).
- **Negative reviews concentrate hostile staff signals exclusively absent in positives:** `rude_dismissive` (27 neg, 0 pos) and `indifferent_inattentive` (17 neg, 0 pos) together account for 35% of all negative reviews.
- `mixed` conduct appears in 24% of negatives vs. 6% of positives, signalling that even ambiguous service tilts toward dissatisfaction.

**Staff conduct is the single strongest thematic separator** — rude or inattentive staff is a near-sufficient predictor of a negative label.

---

## 2. Food Quality & Specific Dish Praise

`food_quality_signal` and `food_praised_highlight` together characterize food-centric reviews:

- **Positive reviews heavily feature food excellence:** `excellent_standout` (46 pos vs. 1 neg, 37% vs. 1%) and `good_solid` (29 pos vs. 8 neg, 23% vs. 6%).
- **Negative reviews concentrate food failures:** `poor_bland` (27 neg, 0 pos, 22%) and `mediocre_average` (24 neg, 4 pos, 19% vs. 3%).
- `food_praised_highlight = specific_dish_excellent` appears in 52 positive reviews (42%) vs. only 4 negatives (3%), confirming that naming a beloved dish is a strong positive-review signature.
- `freshness_flavor_praised` and `overall_variety_praised` are almost exclusively positive (0–1 neg occurrences).

---

## 3. Atmosphere & Ambiance

`atmosphere_ambiance_signal` is less frequently coded (most reviews = `not_present`: 76% pos, 82% neg), but directionally clear:

- Positive atmosphere signals (`positive_lively_enjoyable` + `positive_unique_special`): **25 pos vs. 5 neg** (20% vs. 4%).
- Negative atmosphere signals (`noisy_uncomfortable` + `run_down_dated`): **3 pos vs. 17 neg** (2% vs. 14%).
- Atmosphere is a secondary differentiator — important when mentioned, but most reviews don't foreground it.

---

## 4. Return & Recommend Intent — The Outcome Articulation

`return_recommend_intent` captures reviewers explicitly stating their loyalty decision:

- **`explicit_return_yes`:** 31 pos vs. 1 neg (25% vs. 1%) — positive reviewers frequently articulate intent to return.
- **`explicit_return_no`:** 35 neg vs. 0 pos (28% vs. 0%) — negative reviewers are equally explicit about not returning.
- **`explicit_warn_others`:** 13 neg vs. 0 pos (10% vs. 0%) — a uniquely negative-review behavior.
- 72% of positive reviews and 58% of negative reviews lack an explicit return statement (`not_present`), showing that most sentiment is implicit in description rather than explicit declaration.

---

## 5. Thematic Profile Summary

**Positive reviews** cluster around three reinforcing themes: friendly staff (`service_staff_conduct = friendly_positive`), standout food with specific dish callouts (`food_quality_signal = excellent_standout`, `food_praised_highlight = specific_dish_excellent`), and pleasant atmosphere — often closing with explicit intent to return.

**Negative reviews** are dominated by staff failures (rude or inattentive service, 35%), food disappointment (poor/bland/mediocre food, 41%), physical environment complaints (14%), and explicit deterrence statements (warn others + no return, 38%).

The asymmetry is notable: positive reviews praise across multiple dimensions simultaneously, while negative reviews tend to anchor on a single catastrophic failure (especially service) sufficient to condemn the entire experience.

---

## Coverage Note

`atmosphere_ambiance_signal` had low coverage (≥76% `not_present` in both groups), limiting its standalone analytical weight. `food_praised_highlight` was highly sparse in negatives, making it a reliable positive-only signal rather than a bidirectional differentiator.
