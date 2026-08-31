---
dataset: yelp_polarity_reviews
scenario: predictive_low
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "label_pos"
query: "What review signals predict low Yelp user satisfaction?"
source_table: augment_table/yelp_polarity_reviews/predictive_low/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:26:11.159403+00:00
wall_seconds: 159.48
---

# Analysis: Review Signals Predicting Low Yelp User Satisfaction

## Executive Summary

This analysis identifies the review signals most predictive of low (1-star/negative) Yelp satisfaction among 250 restaurant and service reviews. TAPP-generated semantic annotations reveal that **product quality (poor taste/flavor) and service failures (staff inattention/rudeness) are the dominant predictors** of low satisfaction, with odds ratios exceeding 18:1 compared to high-satisfaction reviews. Notably, 75% of low-satisfaction reviews contain at least one semantic signal, yet 25% stem from non-staff, non-food issues (pricing disputes, facility problems, disorganization).

---

## Data Overview

| Metric | Value |
|--------|-------|
| Total Reviews Analyzed | 250 |
| Low Satisfaction (label_pos=0) | 125 (50.0%) |
| High Satisfaction (label_pos=1) | 125 (50.0%) |
| TAPP-Generated Columns Used | 5 |
| Average TAPP Flags per Low-Satisfaction Review | 1.02 |

---

## Findings: Predictors of Low Satisfaction

### 1. **Product Quality Issues (Poor Taste/Flavor)** — Strongest Predictor

**Odds Ratio: 54.16×** (present in 38 low-satisfaction vs. 1 high-satisfaction review)

| Metric | Value |
|--------|-------|
| Prevalence in low-satisfaction reviews | 30.4% (38/125) |
| Prevalence in high-satisfaction reviews | 0.8% (1/125) |
| Difference | **29.6 percentage points** |
| Sample Size (low-sat occurrences) | 38 reviews |

**Interpretation:** When a review identifies poor taste, flavor, or food quality issues, it is **54 times more likely to be a low-satisfaction review**. This is the single strongest semantic signal.

**Sample Evidence:**
- *"The sushi wasn't great... The service was slow. If you're just going for a drink and edamame, this place fits the bill. Anything more and I suggest you go elsewhere." (YLP-0007)*
- *"...the orange chiken tasted like a sugar chiken... I almost thought I was eating a dessert." (YLP-0047)*
- *"First of all portions are so small their microscopic... If you want real sushi go to sushi kata." (YLP-0017)*

---

### 2. **Staff Inattention or Neglect** — Second Strongest Predictor

**Odds Ratio: 27.11×** (present in 50 low-satisfaction vs. 3 high-satisfaction reviews)

| Metric | Value |
|--------|-------|
| Prevalence in low-satisfaction reviews | 40.0% (50/125) |
| Prevalence in high-satisfaction reviews | 2.4% (3/125) |
| Difference | **37.6 percentage points** |
| Sample Size (low-sat occurrences) | 50 reviews |

**Interpretation:** Staff inattention—including being ignored, overlooked, or receiving poor table service—is mentioned in 40% of low-satisfaction reviews and almost never in positive reviews.

**Sample Evidence:**
- *"We were seated for 25 minutes. No one came to take our order. The waitress was cleaning tables and walked right by us several times... I will never go back." (YLP-0008)*
- *"...they'd seated us in a area reserved for a private party... they had thus forgotten we were there... So we were moved to another spot. Where they took our order and then disappeared. Again..." (YLP-0002)*

---

### 3. **Staff Rudeness or Indifference** — Third Strongest Predictor

**Odds Ratio: 18.86×** (present in 55 low-satisfaction vs. 5 high-satisfaction reviews)

| Metric | Value |
|--------|-------|
| Prevalence in low-satisfaction reviews | 44.0% (55/125) |
| Prevalence in high-satisfaction reviews | 4.0% (5/125) |
| Difference | **40.0 percentage points** |
| Sample Size (low-sat occurrences) | 55 reviews |

**Interpretation:** Rude or dismissive behavior by staff (or management) appears in nearly half of low-satisfaction reviews.

**Sample Evidence:**
- *"The woman works around the kiosk was very rude!!!!!" (YLP-0021)*
- *"I called in to see if they were free... the guy rudely responded no as if I were supposed to already know... I don't even understand what you are saying... What kind of ignorant piece of junk is this place hiring." (YLP-0019)*

---

### 4. **Staff Forgot or Ignored Table** — Fourth Predictor

**Odds Ratio: 12.28×** (present in 29 low-satisfaction vs. 3 high-satisfaction reviews)

| Metric | Value |
|--------|-------|
| Prevalence in low-satisfaction reviews | 23.2% (29/125) |
| Prevalence in high-satisfaction reviews | 2.4% (3/125) |
| Difference | **20.8 percentage points** |
| Sample Size (low-sat occurrences) | 29 reviews |

**Interpretation:** Being forgotten or having orders ignored is more actionable than general inattention; it carries a 12× odds ratio.

**Sample Evidence:**
- *"We had a 20 minutes to get my food order!... [Food runner helped] while all 3 MANAGERS are standing at the counter... Not once did one stop by, ask or give an apology." (YLP-0035)*
- *"We placed out order... 10...15...20....25 Minutes go by and no food." (YLP-0068)*

---

### 5. **Excessive Wait or Slow Service** — Weakest Semantic Signal

**Odds Ratio: 5.09×** (present in 29 low-satisfaction vs. 7 high-satisfaction reviews)

| Metric | Value |
|--------|-------|
| Prevalence in low-satisfaction reviews | 23.2% (29/125) |
| Prevalence in high-satisfaction reviews | 5.6% (7/125) |
| Difference | **17.6 percentage points** |
| Sample Size (low-sat occurrences) | 29 reviews |

**Interpretation:** Wait times and slow service appear less consistently predictive than staff attitude/attentiveness. Some high-satisfaction reviews tolerate waits if quality is excellent.

---

## Co-Occurrence Patterns

**Coverage of TAPP Signals in Low-Satisfaction Reviews:**

| Number of Flags Present | Count | Percentage |
|-------------------------|-------|-----------|
| 0 flags | 31 | 24.8% |
| 1 flag | 41 | 32.8% |
| 2 flags | 20 | 16.0% |
| 3 flags | 14 | 11.2% |
| 4 flags | 17 | 13.6% |
| 5 flags (all) | 2 | 1.6% |
| **At least 1 flag** | **94** | **75.2%** |

**Most Common Combinations (Low-Satisfaction Reviews):**

| Signal Combination | Count | % of Low-Sat |
|-------------------|-------|-------------|
| [No flags] | 31 | 24.8% |
| Poor taste/flavor only | 25 | 20.0% |
| All 4 service flags (rudeness, wait, inattention, forgot) | 15 | 12.0% |
| Staff rudeness only | 15 | 12.0% |
| Rudeness + inattention | 11 | 8.8% |

**Key Insight:** The most severe low-satisfaction experiences often combine multiple service failures (rudeness, wait, inattention, being forgotten), suggesting systemic staff/operational breakdowns.

---

## Neutral Zone: Low Satisfaction Without TAPP Signals (24.8%)

A substantial minority of low-satisfaction reviews contain no staff rudeness, inattention, wait time, product quality, or forgetfulness flags. These reviews cite:

- **Pricing disputes** (holiday brunch pricing not disclosed online)
- **Facility/infrastructure issues** (construction disruption)
- **Overcrowding or poor atmosphere** (excessive noise)
- **Cleanliness concerns** (separate from service)
- **Policy disagreements** (dress codes, payment minimums)

These reviews indicate that **venue environment, transparency, and management decisions drive satisfaction independently of direct staff/food quality issues**.

---

## Contrast: High-Satisfaction Reviews

TAPP semantic signals are rare in positive reviews:

| Signal | Prevalence in High-Satisfaction Reviews |
|--------|--------------------------------------|
| Staff rudeness/indifference | 4.0% (5/125) |
| Excessive wait/slow service | 5.6% (7/125) |
| Staff inattention/neglect | 2.4% (3/125) |
| Poor taste/flavor | 0.8% (1/125) |
| Staff forgot/ignored table | 2.4% (3/125) |

Even when present, these signals appear in contextualized positive narratives, suggesting recovery or overall excellence outweighing isolated lapses.

---

## Method Note: TAPP-Generated Columns

**Columns used in this analysis:**
1. `staff_rudeness_or_indifference` (24.0% coverage; 44.0% in low-satisfaction reviews)
2. `excessive_wait_or_slow_service` (14.4% coverage; 23.2% in low-satisfaction reviews)
3. `staff_inattention_or_neglect` (21.2% coverage; 40.0% in low-satisfaction reviews)
4. `poor_taste_or_flavor` (15.6% coverage; 30.4% in low-satisfaction reviews)
5. `staff_forgot_or_ignored_table` (12.8% coverage; 23.2% in low-satisfaction reviews)

These TAPP facets successfully capture semantically distinct service and product failure modes. They demonstrate high discriminative power (odds ratios 5–54×) and co-occur meaningfully in severe dissatisfaction episodes. The columns are used **complementarily with the raw review text**, not as replacements.

---

## Conclusions & Implications

1. **Two-factor model of low satisfaction:**
   - **Product/quality dimension:** Poor taste/flavor is the single strongest predictor (OR 54.16×), driving isolated negative reviews.
   - **Service dimension:** Staff inattention (OR 27.11×), rudeness (OR 18.86×), and forgetfulness (OR 12.28×) cluster together and dominate systemic dissatisfaction.

2. **Service failures more severe when compounded:** The most damaging reviews combine multiple service signals, indicating that **isolated delays are recoverable but systemic staff disengagement is catastrophic**.

3. **Significant "non-TAPP" dissatisfaction (25%):** Pricing transparency, facility conditions, policies, and overcrowding represent a meaningful driver of low satisfaction, aligning more with **business model and venue design** than operational staff execution.

4. **Actionability ranking for improvement:**
   1. **Urgent:** Staff training on attentiveness and politeness
   2. **High:** Quality control on food/beverage taste and consistency
   3. **Medium:** Wait time management and order execution tracking
   4. **Important but distinct:** Facility design, pricing transparency, and operational policies

---

**Analysis Date:** 2026-07-30  
**Dataset:** Yelp Polarity Reviews (Predictive Low)  
**Model:** Substrate Claude Haiku 4.5  
**Framework:** TA++ v11 Augmentation
