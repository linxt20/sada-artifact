---
dataset: imdb_movie_reviews
scenario: predictive_negative
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "label_pos"
query: "What review signals predict negative IMDb audience satisfaction?"
source_table: augment_table/imdb_movie_reviews/predictive_negative/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:24:56.376533+00:00
wall_seconds: 59.35
---

# Predictive Analysis: Review Signals of Negative IMDb Audience Satisfaction

## Executive Summary

This analysis identifies linguistic features that predict negative IMDb audience satisfaction (label_pos=0) in a balanced dataset of 250 reviews (125 negative, 125 positive). **Negative word count emerges as the strongest predictor**, with a moderate negative correlation to satisfaction (r = −0.380) and highly significant association (χ² = 23.92, p < 0.001).

---

## Key Findings

### 1. Negative Word Count: The Dominant Signal

**Strongest predictor of negative reviews:**

- **Negative reviews** average **1.48 negative words** per review (SD = 1.98)
- **Positive reviews** average **0.28 negative words** per review (SD = 0.62)
- **Difference**: +1.20 words (5× higher in negative reviews)

**Distribution reveals stark separation:**
- 78.4% of positive reviews contain **zero negative words**
- 38.4% of negative reviews contain **zero negative words** (38.4%)
- 60.8% of negative reviews contain **≥1 negative word**

**Predictive power:** Reviews with ≥3 negative words have a **96.3% probability** of expressing negative satisfaction, compared to 44.4% for reviews with fewer negative words.

**Statistical significance:** χ² = 23.92 (p < 0.001), Cramér's V = 0.309 (moderate effect size)

---

### 2. Negation Intensifiers: Secondary Signal

**Weak but consistent signal of negativity:**

- **Negative reviews**: Mean 3.33 intensifiers (median = 3.0)
- **Positive reviews**: Mean 2.66 intensifiers (median = 2.0)
- **Correlation**: r = −0.139 (weak negative relationship with satisfaction)

**Pattern**: Higher concentration of negation intensifiers (words like "not," "never," "nothing," adverbial negations) appears in negative reviews, suggesting more emphatic denial or critical language. However, this signal is much weaker than negative word count and overlaps significantly between satisfaction groups.

---

### 3. Exclamation Marks & Capitalization: Negligible Signals

**Surprising finding—minimal predictive value:**

- **Exclamation count**: r = +0.013 (essentially zero correlation)
  - Negative reviews: Mean 0.47 exclamation marks
  - Positive reviews: Mean 0.52 exclamation marks
  
- **Capitalized word count**: r = +0.031 (essentially zero correlation)
  - Negative reviews: Mean 0.86 capitalized words
  - Positive reviews: Mean 0.98 capitalized words

**Interpretation**: Both positive and negative reviews use emphatic punctuation and capitalization at similar rates. Enthusiasm is not uniquely associated with satisfaction; critical reviews can also employ exclamation marks for emphasis (e.g., "This is awful!!!").

---

## Patterns & Insights

### What Drives Negative Predictions

1. **Explicit negative vocabulary** (most decisive)
   - Adjectives: "awful," "terrible," "bad," "horrible," "disgrace," "crap"
   - Verbs: "ruined," "destroyed," "wrecked"
   - Nouns: "failure," "trash," "garbage," "disaster"
   - Example (11 negative words): *"Need a lesson in pure, abject failure? Look no further than 'Wizards of the Lost Kingdom', an abysmal, dirt-poor, disgrace of a flick..."*

2. **Negation patterns** (moderate support)
   - Intensified negations: "not good," "never," "nothing," "no way"
   - Double negatives for emphasis: "wouldn't," "doesn't"
   - Suggests more categorical dismissal in negative reviews

3. **Absence of negative words** (not definitive of positivity)
   - 38.4% of negative reviews avoid explicit negative vocabulary
   - These reviews likely express dissatisfaction through implicit criticism, sarcasm, or structural critique without relying on negative adjectives
   - Example: *"There's no real plot... completely fell apart... dopey parallel characters..."* (lacks strong negative words but clearly critical)

### Weak Signals That Do Not Predict Satisfaction

- **Exclamation marks**: Used equally by satisfied and dissatisfied reviewers; represent enthusiasm or emphasis, not valence
- **Capitalization**: Non-differentiating; found in both praise ("NATURAL," "GREAT") and criticism ("AWFUL," "TERRIBLE")

---

## Data Quality & Limitations

- **Balanced dataset**: 125 negative, 125 positive reviews (50/50 split)
- **Feature coverage**: 
  - 38.4% of negative reviews have zero explicit negative words, suggesting the model may miss implicit or contextual negativity
  - Exclamation marks and capitalization are too noisy to rely upon independently
- **Lexical focus**: Analysis captures surface-level linguistic markers; does not assess narrative structure, coherence, or thematic critique
- **Skill off variant**: This is a "skill_off" augmentation, meaning features are engineered without using external grounding truth—results reflect raw linguistic statistics

---

## Recommendation Summary

**To predict negative audience satisfaction in IMDb reviews:**

1. **Prioritize negative word count** (r = −0.38, p < 0.001)
   - Strong, reliable signal with clear statistical backing
   - 96% precision when ≥3 negative words present

2. **Consider negation intensifiers as supplementary** (r = −0.14, weak)
   - Modest additional signal but substantial overlap with positive reviews
   - Useful as a feature in ensemble models but insufficient alone

3. **Do not rely on exclamation marks or capitalization** alone
   - Near-zero correlation; high false-positive rate
   - These are stylistic choices across both satisfaction groups

4. **Account for implicit negativity**
   - 38% of negative reviews lack explicit negative words
   - Combined with high negative-word reviews, only ~61% of negative satisfaction is flagged by this single feature
   - Recommend combining with structural features (complaint length, narrative pacing criticism, etc.)

---

## Conclusion

Negative word count is a **strong, statistically significant predictor** of negative IMDb satisfaction (p < 0.001), with moderate effect size. Secondary signals like negation intensifiers show weak correlation. Exclamation marks and capitalization do not predict satisfaction. Predictive models should weight negative vocabulary heavily but combine it with additional features to capture the ~40% of negative reviews that avoid explicit negative words.
