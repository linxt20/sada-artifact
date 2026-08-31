---
dataset: amazon_polarity_reviews
scenario: predictive_negative
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "label_pos"
query: "What review signals predict negative Amazon product satisfaction?"
source_table: augment_table/amazon_polarity_reviews/predictive_negative/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:08:57.030335+00:00
wall_seconds: 40.71
---

# Predictive Signals of Negative Amazon Product Reviews

## Executive Summary

This analysis examines 250 Amazon product reviews (125 negative, 125 positive) to identify review signals that predict negative satisfaction (label_pos=0). Five key linguistic and sentiment signals were annotated and evaluated for their predictive strength.

**Key Finding:** Regret sentiment emerges as the strongest predictor of negative satisfaction, present in 84% of negative reviews. When combined with strong negative language and value concerns, these signals reliably distinguish dissatisfied customers.

---

## Predictive Signals Ranked by Strength

### 1. **Regret Sentiment** (Strongest Predictor)
- **Prevalence in negative reviews:** 105/125 (84.0%)
- **Prevalence in positive reviews:** 3/125 (2.4%)
- **Predictive lift:** 35.0x
- **Odds ratio:** 213.5x

Regret sentiment is the most reliable indicator of negative satisfaction. Common regret expressions include:
- **Waste of money** (38 negative reviews): "This product is total junk," "money wasted," "not worth the purchase price"
- **Would not recommend** (36 reviews): "Don't buy this," "avoid this product"
- **Waste of time** (20 reviews): "biggest waste of my time," "not worth watching"
- **Regret/remorse** (11 reviews): Direct expressions of buyer's remorse

**Pattern:** Negative reviewers explicitly articulate regret about their purchase decision, distinguishing them from positive reviewers who show satisfaction or acceptance of trade-offs.

### 2. **Strong Negative Language** (Second Strongest)
- **Prevalence in negative reviews:** 118/125 (94.4%)
- **Prevalence in positive reviews:** 12/125 (9.6%)
- **Predictive lift:** 9.8x
- **Odds ratio:** 158.7x

Nearly all negative reviews employ emphatic or casual negative language:
- **Emphatic negative** (75 reviews): "WORST," "HATE," "HORRIBLE," "absolute junk," "appallingly shallow," "disgusting"
- **Casual negative** (43 reviews): Milder criticism such as "not very good," "disappointed," "lacking"

**Pattern:** The intensity and prevalence of negative language strongly correlates with dissatisfaction. Emphatic negatives appear twice as frequently as casual negatives in negative reviews, suggesting language intensity may indicate severity of dissatisfaction.

### 3. **Value Concern** (Third Strongest)
- **Prevalence in negative reviews:** 63/125 (50.4%)
- **Prevalence in positive reviews:** 1/125 (0.8%)
- **Predictive lift:** 63.0x
- **Odds ratio:** 126.0x

Nearly all value concerns express explicit judgment that products are not worth purchasing:
- **Not worth it** (50 negative reviews): "not worth the money," "not worth buying," "don't waste your money"
- **Poor value** (9 reviews): "overpriced for quality," "bad value for price"
- **Overpriced** (4 reviews): Explicit criticism of pricing relative to quality

**Pattern:** Value concerns frequently appear alongside defect complaints, indicating that poor quality combined with price awareness drives dissatisfaction.

### 4. **Unmet Expectation** (Fourth)
- **Prevalence in negative reviews:** 86/125 (68.8%)
- **Prevalence in positive reviews:** 11/125 (8.8%)
- **Predictive lift:** 7.8x
- **Odds ratio:** 22.9x

Unmet expectations manifest as three distinct disappointments:
- **Not as described** (44 reviews): Product differs from advertising or description ("claimed to be waterproof but isn't," "colors don't match")
- **Expected better** (26 reviews): Anticipation exceeded reality ("thought with this brand name it would be better," "expected higher quality")
- **False advertising** (16 reviews): Explicit misrepresentation ("warranty claims unfounded," "false specs")

**Pattern:** Unmet expectations often combine with defects or value concerns, creating compound dissatisfaction.

### 5. **Defect or Failure** (Weakest Signal)
- **Prevalence in negative reviews:** 49/125 (39.2%)
- **Prevalence in positive reviews:** 3/125 (2.4%)
- **Predictive lift:** 16.3x
- **Odds ratio:** 26.2x

Defects and failures appear in fewer negative reviews than other signals, but when present, strongly indicate dissatisfaction:
- Durability issues ("broke after 2 months," "completely fell apart")
- Functional failures ("won't produce power," "doesn't work even with new batteries")
- Design flaws ("too flimsy," "hard to set up")

**Pattern:** Tangible product failures predict dissatisfaction with high confidence, but absence of defects does not guarantee satisfaction—many dissatisfied customers cite poor value or unmet expectations rather than failures.

---

## Signal Combinations and Patterns

### Co-occurrence Strength
Negative reviews exhibit multiple signals simultaneously:
- **5 signals present:** 35 reviews (28.0%) — maximum dissatisfaction
- **4 signals present:** 25 reviews (20.0%)
- **3 signals present:** 35 reviews (28.0%)
- **2 signals present:** 17 reviews (13.6%)
- **1 signal present:** 7 reviews (5.6%)
- **0 signals present:** 6 reviews (4.8%) — exceptions requiring review-text analysis

### Typical Negative Review Profile
The most common negative review (56% of cases) contains 3–5 signals, typically combining:
1. Strong negative language (emphatic)
2. Regret sentiment (waste of money or would not recommend)
3. Unmet expectation (not as described or expected better)

This combination signals both emotional dissatisfaction and rational criticism.

---

## Exceptions and Weak Evidence

### Edge Cases (6 reviews, 4.8% of negative reviews)
Six negative reviews exhibit none of the five annotated signals. Analysis of one example ("I had to read it twice") reveals criticism in narrative content not captured by the signal schema—the reviewer describes character weaknesses without explicit negative language or value judgments. These cases suggest the signal set is approximately 95% comprehensive for textual negation patterns.

### Positive Reviews with Negative Signals
Three positive reviews contain regret sentiment, and 12 contain negative language. These likely reflect qualified praise ("good for the price despite minor flaws") or thematic discussion of critical topics within otherwise positive reviews.

---

## Conclusion

Five linguistic and sentiment signals reliably predict negative Amazon product satisfaction:

1. **Regret sentiment** (84% in negative reviews) is the strongest single predictor
2. **Strong negative language** (94% in negative reviews) is nearly universal
3. **Value concerns** (50% in negative reviews) indicate deliberate cost-benefit judgment
4. **Unmet expectations** (69% in negative reviews) reveal gap between promise and delivery
5. **Defect/failure** (39% in negative reviews) marks tangible product problems

The predictive model's strength derives from combining these signals: 95% of negative reviews exhibit at least one clear signal, with most combining three or more. This multi-signal pattern enables robust automated detection of customer dissatisfaction from review text alone.

**Decision Guidance:** Reviews exhibiting regret sentiment + strong negative language + value concern present high-confidence negative satisfaction signals. Reviews with only defects may reflect acceptance or trade-off tolerance; additional context is needed when defects appear without regret or value criticism.
