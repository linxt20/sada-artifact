---
dataset: amazon_fine_food_review
scenario: concept_food_quality_facets
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "food_quality"
query: "What distinct aspects of food quality do reviewers focus on?"
source_table: augment_table/amazon_fine_food_review/concept_food_quality_facets/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:00:06.936090+00:00
wall_seconds: 36.21
---

# Food Quality Facets in Amazon Fine Food Reviews

## Overview

The dataset contains **10,000 reviews** annotated across eight food-quality facets, with a `primary_quality_facet` label indicating each review's dominant concern.

---

## Facet Prevalence

| Facet | # Reviews Mentioning | % of Total |
|---|---|---|
| **Taste** | 5,607 | 56.1% |
| **Packaging / Quantity** | 4,834 | 48.3% |
| **Ingredients / Nutrition** | 2,598 | 26.0% |
| **Texture** | 2,009 | 20.1% |
| **Appearance** | 1,646 | 16.5% |
| **Consistency / Brand** | 1,333 | 13.3% |
| **Freshness** | 1,124 | 11.2% |
| **Smell / Aroma** | 478 | 4.8% |

**Taste** is by far the most commonly mentioned facet, followed closely by **Packaging/Quantity** — notable because packaging is a logistical/value concern rather than an intrinsic sensory property.

---

## Primary Facet Distribution

When a single dominant facet is assigned, the ranking shifts only slightly:

| Primary Facet | # Reviews |
|---|---|
| Taste | 3,065 |
| Packaging / Quantity | 2,161 |
| Ingredients / Nutrition | 1,130 |
| Texture | 691 |
| Appearance | 579 |
| Consistency / Brand | 552 |
| Freshness | 467 |
| Smell / Aroma | 133 |
| None | 1,222 |

**1,222 reviews (12.2%)** could not be mapped to any quality facet, suggesting generic or off-topic reviews.

---

## Key Patterns

### 1. Taste Dominates Sensory Evaluation
Taste is the primary quality driver, appearing in 56% of reviews and leading as a primary facet. It co-occurs most with **Packaging/Quantity** (2,775 pairs) and **Ingredients/Nutrition** (1,661 pairs), indicating reviewers often contextualize taste alongside value and composition.

### 2. Packaging/Quantity Is a First-Class Concern
Nearly half of all reviews mention packaging or quantity, and it ranks second as a primary facet — higher than intrinsic sensory facets like texture or appearance. This reflects that Amazon shoppers weigh value-for-money heavily alongside taste.

### 3. Texture and Appearance Are Secondary Sensory Facets
Texture (20%) and appearance (16.5%) are consistently present but rarely dominate. The texture–taste co-occurrence (1,387) suggests they are usually supporting evidence, not standalone complaints.

### 4. Freshness and Smell/Aroma Are Niche but Impactful
Freshness (11%) and smell/aroma (4.8%) are the least common facets. Aroma has the **lowest average review score (3.88)** of any facet, suggesting that when smell is mentioned, it is often a complaint.

### 5. Multi-Facet Reviews Are the Norm
Only 28% of reviews focus on a single facet; **57% mention 2–4 facets simultaneously**, reflecting holistic product assessments rather than single-dimensional feedback.

---

## Score by Primary Facet

| Primary Facet | Avg. Score |
|---|---|
| Texture | 4.32 |
| Freshness | 4.21 |
| Ingredients / Nutrition | 4.19 |
| Taste | 4.11 |
| Consistency / Brand | 4.09 |
| Packaging / Quantity | 4.07 |
| Appearance | 4.03 |
| Smell / Aroma | 3.88 |

Reviews centered on **smell/aroma** average 3.88 stars — the lowest — while **texture-primary** reviews average 4.32 — the highest. Smell complaints appear to be particularly dissatisfaction-driven.

---

## Summary of Distinct Quality Aspects

Reviewers focus on **eight distinct facets**, which fall into natural clusters:

- **Sensory** (intrinsic): Taste, Texture, Smell/Aroma, Appearance
- **Freshness/Safety**: Freshness
- **Compositional**: Ingredients & Nutrition
- **Extrinsic/Value**: Packaging & Quantity, Consistency & Brand reliability

The most actionable insight is that **taste and packaging/quantity together account for the bulk of primary concerns**, while **smell/aroma is rare but disproportionately negative** when it does appear.

---

*Based on 10,000 reviews; facets are binary-coded by model annotation (sonnet, skill_off variant).*
