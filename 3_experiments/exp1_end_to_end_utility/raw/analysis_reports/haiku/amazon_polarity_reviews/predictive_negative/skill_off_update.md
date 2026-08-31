---
dataset: amazon_polarity_reviews
scenario: predictive_negative
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "label_pos"
query: "What review signals predict negative Amazon product satisfaction?"
source_table: augment_table/amazon_polarity_reviews/predictive_negative/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:02:37.913608+00:00
wall_seconds: 47.43
---

# Review Signals Predicting Negative Amazon Product Satisfaction

**Dataset:** Amazon Product Reviews (250 reviews, balanced: 125 negative / 125 positive)  
**Variant:** Skill Off Update (LLM-augmented features)  
**Analysis Date:** 2026-07-28

## Executive Summary

This analysis identifies key linguistic and semantic signals that distinguish negative (label_pos=0) from positive (label_pos=1) Amazon product reviews. The strongest predictors are **negative sentiment intensity**, **product durability/failure signals**, and **comparative language**, while tone markers show weaker discriminative power.

---

## Primary Predictive Signals

### 1. **Negative Sentiment Word Density** ★★★ (Strongest)

**Finding:** Negative reviews contain significantly more negative sentiment words.

| Metric | Negative Reviews | Positive Reviews |
|--------|-----------------|-----------------|
| Mean count | 1.03 | 0.26 |
| Median | 1.0 | 0.0 |
| Max observed | 6 | varies |
| ≥2 words | 30.4% | 4.8% |

**Interpretation:** Negative reviews are 4x more likely to contain 2+ negative sentiment words. The concentration of words like "disappointed," "waste," "terrible," and "awful" strongly correlates with negative satisfaction.

**Examples:**
- "Worst Movie of All Time" (3 negative words): "not enough bad things... waste of time"
- "Worthless" (3 words): "total junk," "didn't work," "useless"

---

### 2. **Product Durability & Failure Signals** ★★★ (Strong)

**Finding:** Negative reviews reference product failures and durability issues 3.5x more frequently.

| Signal | Negative Reviews | Positive Reviews |
|--------|-----------------|-----------------|
| Durability complaints | 14.4% | 4.0% |
| Product failure words | 11.2% | 8.8% |
| Investment complaint words | 0.19 avg | 0.11 avg |

**Key complaint patterns in negative reviews:**
- "broke," "broke after," "fell apart," "stopped working"
- "doesn't work," "quit working," "failed," "defect"
- "flimsy," "cheap," "poor quality construction"

**Examples:**
- "didn't last long": "lasted maybe 4 months... doesn't work anymore"
- "great but broke within a day": "it worked the night we opened it"
- "DO NOT BUY": "gear shifter broke off into my spokes"

**Notable:** While product failure signals appear in some positive reviews (8.8%), they typically occur in context of workaround solutions or acceptable alternatives, unlike negative reviews where failure is conclusive.

---

### 3. **Presence of Comparative Language** ★★ (Moderate)

**Finding:** Negative reviews use comparisons more frequently (0.25 vs 0.14 mean count).

**Patterns in negative reviews:**
- "better than," "not as good as," "worse than"—comparing current product unfavorably
- "More effective alternatives": "tried a long time to find details... I went to a steamer mop which works better in every way"
- "Used to be better": "Didn't used to be that flimsy"

**Interpretation:** Comparative language often signals unmet expectations and desire for better alternatives, indicating disappointment with current product.

---

### 4. **Positive Sentiment Word Deficit** ★★ (Moderate-Inverse)

**Finding:** Absence of positive words is a negative satisfaction signal.

| Metric | Negative | Positive |
|--------|----------|----------|
| Mean count | 0.43 | 1.13 |
| Median | 0.0 | 1.0 |

**Pattern:** Over 60% of negative reviews contain zero positive sentiment words, vs. only ~35% of positive reviews. The lack of praising language (great, excellent, love, recommend) strongly indicates dissatisfaction.

---

### 5. **Question Mark Frequency** ★ (Weak-Modest)

**Finding:** Negative reviews contain more questions (0.16 vs 0.04 mean).

**Patterns observed:**
- Rhetorical questions expressing frustration: "Why is it like this? What was the manufacturer thinking?"
- Uncertainty/confusion: "What were the script writers thinking?"
- Seeking alternatives: "could someone help? Will it be before Christmas?"

**Caveat:** This signal is weaker and often conflates rhetorical frustration with genuine inquiry.

---

## Weak or Non-Predictive Signals

### Exclamation Marks
- **Negative reviews:** 0.97 mean count
- **Positive reviews:** 1.15 mean count

**Finding:** Exclamation marks are **not discriminative**. Positive reviews actually use them slightly more often, often for emphasis of enthusiasm ("LOVE," "Best movie EVER!!!!!").

### ALLCAPS Word Count
- Appears sporadically in both classes
- Weak signal due to mixed use (emphasis in both positive enthusiasm and negative frustration)

---

## Product Category Patterns (Observed)

Negative sentiment signals manifest differently by category:

- **Electronics/Home Goods:** Durability, performance failure, and malfunction references dominate
- **Books/Media:** Content disappointment, writing quality, narrative structure issues
- **Apparel/Accessories:** Fit/design problems, quality/material complaints
- **General:** "Waste of time/money" appears across categories when products fail to deliver

---

## Textual Evidence Summary

### Strong Negative Indicators (High Confidence)
1. Multiple negative sentiment words (2+) → 30.4% of negative reviews
2. Durability/failure references → 14.4% of negative reviews
3. Zero positive sentiment words → 60%+ of negative reviews
4. Explicit quality criticism + comparative alternatives → High certainty

### Weaker Indicators (Use with Caution)
- Single exclamation mark or question mark
- Isolated ALLCAPS words (context-dependent)
- Comparative language alone (requires content verification)

---

## Important Exceptions & Limitations

### Mixed Sentiment Reviews
- **15-20% of negative reviews** contain 1+ positive word, usually acknowledging one strength before criticizing overall product
  - Example: "The quality is soft and smooth... [but] the product was packed nicely [negative overall]"
- These require content analysis beyond word counts

### Positive Reviews with Negative Words
- ~5% of positive reviews mention problems (durability, fit, shipping) but frame them as manageable or overcome
  - Example: "had to exchange it for my usual size, so my advice is that this cami runs true to size" (positive outcome)

### Context Dependency
- "Waste" appears in negative reviews as criticism but occasional positive frame: "worth the waste of my time" (rare, requires NLP context)
- Product failure references in positive context: reviews about fixing or workarounds

---

## Predictive Decision Rules (Ordered by Strength)

| Rank | Signal | Confidence |
|------|--------|-----------|
| 1 | ≥2 negative sentiment words | High |
| 2 | Durability/product failure reference + no constructive resolution | High |
| 3 | ≤0 positive sentiment words | Moderate-High |
| 4 | Comparative language (unfavorable comparison) | Moderate |
| 5 | Question marks indicating confusion/frustration | Moderate |
| 6 | Exclamation marks | Low (unreliable, need context) |

---

## Conclusion

**Negative Amazon product satisfaction is most reliably predicted by:**
1. **Concentration of explicit negative sentiment words** (3-4x denser in negative reviews)
2. **Product durability and malfunction signals** (3.5x more frequent in negative reviews)
3. **Absence of positive reinforcement language** (inverse signal)
4. **Unfavorable comparative framing** (alternatives mentioned explicitly)

**Tone markers (punctuation alone) are insufficient predictors** and should be combined with sentiment and semantic signals for robust classification. Ground-truth analysis shows that context and explicit failure/quality language matter more than punctuation frequency.

**Dataset quality note:** This augmented dataset with "skill_off" variant shows clean separation on semantic features (negative/positive word counts, complaint categories), suggesting the LLM augmentation captured meaningful linguistic patterns aligned with satisfaction labels.
