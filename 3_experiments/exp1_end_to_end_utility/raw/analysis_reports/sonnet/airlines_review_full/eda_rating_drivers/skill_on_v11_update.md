---
dataset: airlines_review_full
scenario: eda_rating_drivers
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "Overall Rating"
query: "Across Type of Traveller and Class, which review themes are associated with higher vs. lower Overall Rating?"
source_table: augment_table/airlines_review_full/eda_rating_drivers/sonnet__skill_on_v11_update.csv
generated_at: 2026-08-03T05:52:27.191836+00:00
wall_seconds: 69.03
---

# Review Themes vs. Overall Rating: Across Type of Traveller and Class

**Dataset:** 8,100 airline reviews | **Overall Rating range:** 1–10 (mean 5.6)

---

## 1. Baseline: Ratings by Segment

| Segment | Mean Rating |
|---|---|
| **First Class** | 7.6 |
| **Business Class** | 6.7 |
| **Premium Economy** | 6.0 |
| **Economy Class** | 5.2 |
| **Solo Leisure** | 6.1 |
| **Business** travellers | 5.4 |
| **Couple Leisure** | 5.5 |
| **Family Leisure** | 5.1 |

Within the Traveller × Class interaction, **Solo Leisure in First Class** scores highest (8.2) and **Business travellers in Economy** lowest (5.0). Family Leisure consistently underperforms vs. other traveller types in the same cabin.

---

## 2. Theme-Level Drivers (all segments)

### 2a. Cabin Crew Sentiment — strongest single driver

| Theme Value | Mean Rating | N |
|---|---|---|
| `warm_proactive` | **9.1** | 2,980 |
| `professional_adequate` | 6.8 | 1,021 |
| `inconsistent` | 5.6 | 649 |
| `poor_rude` | **2.4** | 2,986 |
| `Unknown` (not mentioned) | 2.1 | 464 |

This pattern is **uniform across all traveller types and cabin classes** — the mean for `warm_proactive` varies only from 8.9 (Business travellers) to 9.2 (Family Leisure), and from 8.9 (Business Class) to 9.3 (First Class). Positive crew interactions are the single most consistent positive theme.

**Distribution note:** Family Leisure has the highest rate of `poor_rude` crew mentions (44%), while Solo Leisure has the lowest (31%). First Class has the highest `warm_proactive` rate (64%); Economy the lowest (32%).

---

### 2b. Value for Class Perception

| Theme Value | Mean Rating | N |
|---|---|---|
| `exceeds_expectations` | **9.4** | 2,112 |
| `meets_expectations` | 8.0 | 1,754 |
| `below_expectations` | 4.2 | 1,597 |
| `poor_value` | **1.9** | 2,635 |

`poor_value` accounts for 35–39% of reviews for **Family Leisure** and **Business travellers** — notably higher than for Solo Leisure (28%). First Class reviews have the lowest `poor_value` rate (13%) and highest `exceeds_expectations` share (51%), while Economy has the highest `poor_value` rate (38%).

---

### 2c. Class Product Expectation Gap

| Theme Value | Mean Rating | N |
|---|---|---|
| `exceeded` | **9.3** | 2,351 |
| `met` | 7.9 | 1,573 |
| `below_expectation` | **2.7** | 4,174 |

`below_expectation` applies to a majority of reviews (51%) and drives the dataset mean down. The gap effect is consistent across classes (Economy `below_expectation` → 2.4; Business Class → 3.5), but Business and Premium Economy reviewers rate slightly higher when expectations are unmet, suggesting some tolerance buffer.

---

### 2d. Service Consistency

| Theme Value | Mean Rating |
|---|---|
| `consistent_high` | **9.3** |
| `inconsistent_by_leg` | 6.0 |
| `inconsistent_by_crew` | 5.8 |
| `consistent_low` | **2.0** |

Inconsistency (whether by leg or crew member) clusters around the midpoint (~5.9), acting as a moderate detractor rather than a catastrophic one. This is especially relevant for **multi-leg itineraries** common among Business and Solo Leisure travellers.

---

### 2e. Disruption Handling

| Theme Value | Mean Rating | N |
|---|---|---|
| `proactive_excellent` | **9.3** | 316 |
| `adequate` | 7.1 | 147 |
| `not_applicable` | 6.9 | 5,457 |
| `poorly_handled_dismissive` | **1.9** | 2,180 |

`poorly_handled_dismissive` is catastrophic for ratings. **Family Leisure** has the highest exposure (36% of reviews mention disruption poorly handled vs. 23% for Solo Leisure), making disruptions a particularly strong negative lever for that segment.

---

### 2f. Food Quality Sentiment

| Theme Value | Mean Rating |
|---|---|
| `positive` | **9.0** |
| `adequate` | 7.1 |
| `negative` | 3.9 |
| `Unknown` | 3.8 |

Food is mentioned positively in 28% of reviews; when negative it drags ratings to near-poor levels. Its impact is secondary to crew and value themes but still meaningful.

---

### 2g. Seat Comfort

| Theme Value | Mean Rating |
|---|---|
| `comfortable_spacious` | **8.8** |
| `adequate` | 6.6 |
| `cramped_narrow` | 4.4 |
| `broken_defective` | 3.5 |

Seat comfort complaints (`cramped_narrow`, `broken_defective`) are more prevalent in Economy, compounding its lower baseline rating.

---

### 2h. Service Decline Perception

| Theme Value | Mean Rating | N |
|---|---|---|
| `False` (no decline noted) | 5.8 | 7,481 |
| `True` (decline noted) | 4.2 | 619 |

Only 8% of reviews note perceived service decline, but it meaningfully depresses ratings. Business travellers (who may have a longer reference history) are among those flagging this.

---

## 3. Cross-Segment Summary

| Theme | Higher Rating Associated With | Lower Rating Associated With |
|---|---|---|
| Cabin crew | `warm_proactive` (avg 9.1) | `poor_rude` (avg 2.4) |
| Value perception | `exceeds_expectations` (9.4) | `poor_value` (1.9) |
| Product expectation gap | `exceeded` (9.3) | `below_expectation` (2.7) |
| Service consistency | `consistent_high` (9.3) | `consistent_low` (2.0) |
| Disruption handling | `proactive_excellent` (9.3) | `poorly_handled_dismissive` (1.9) |
| Food | `positive` (9.0) | `negative` / unknown (3.8–3.9) |
| Seat comfort | `comfortable_spacious` (8.8) | `broken_defective` (3.5) |

**Key segment-specific notes:**
- **Solo Leisure** has the most favourable theme distribution (most `warm_proactive`, least `poor_value`) → highest traveller-type average (6.1).
- **Family Leisure** is most exposed to `poor_rude` crew, `poor_value`, and `poorly_handled_dismissive` disruptions → lowest average (5.1).
- **First Class** dominates positive outcomes due to high `warm_proactive` and `exceeds_expectations` rates, but its small n (121) warrants caution.
- **Economy Class** suffers from the highest `poor_value` and `consistent_low` rates, anchoring it at 5.2 despite being the largest group.

---

## 4. Caveats

- Several theme values have `Unknown` (untagged) categories with low ratings (2.1–3.8), suggesting negative reviews may omit themes rather than explicitly label them — these should not be treated as a distinct positive signal.
- First Class has only 121 reviews; its statistics are directionally consistent but should not be over-weighted.
- Themes are AI-derived from review text and may conflate causes; correlation with Overall Rating does not establish independent causal contribution.
