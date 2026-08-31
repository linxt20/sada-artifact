---
dataset: airlines_review_full
scenario: focus_inference
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's in these airline reviews — I'm not sure which aspect is most worth analyzing."
source_table: augment_table/airlines_review_full/focus_inference/sonnet__skill_on_v11_update.csv
generated_at: 2026-08-03T05:52:52.728841+00:00
wall_seconds: 42.46
---

# Airline Reviews Dataset — Exploratory Analysis

## Dataset Overview

- **8,100 reviews** across 9 airlines (Turkish Airlines, Qatar Airways, Emirates dominating ~57% of records)
- 16 original columns: ratings, traveller type, class, route, plus free-text reviews
- 9 **augmented inference columns** added by the model: `cabin_crew_attitude`, `food_quality_signal`, `amenity_and_product_gap`, `premium_cabin_value_judgment`, `disruption_handling_quality`, `cs_resolution_quality`, `service_decline_perception`, `airline_decline_narrative`, `ground_service_quality`
- Overall ratings are **bimodally distributed** (mean 5.6, median 6): reviews skew toward extremes — 47% recommend, 53% do not

---

## Most Analytically Valuable Focus Variable: **Cabin Crew Attitude**

The augmented variable `cabin_crew_attitude` shows the **strongest, most monotonic relationship** with Overall Rating of any variable in the dataset:

| Cabin Crew Attitude | Mean Overall Rating | N |
|---|---|---|
| `friendly_proactive` | **9.05** | 3,105 |
| `neutral_professional` | 6.47 | 677 |
| `mixed` | 5.20 | 1,208 |
| `cold_robotic` | 3.58 | 455 |
| `rude_dismissive` | **1.90** | 2,113 |

This near-linear gradient (1.9 → 9.1 across five categories) makes crew attitude the single most discriminating factor for overall satisfaction. It also affects 94% of reviews (only 6.7% are `Unknown`).

---

## Secondary Focus Variables

### Food Quality Signal
Nearly as predictive as crew attitude, with a clean split:

| Food Quality | Mean Rating |
|---|---|
| `excellent` | 9.16 |
| `adequate` | 7.60 |
| `poor_quality` | 4.00 |
| `meal_not_served` / `special_meal_failure` | ~3.1–3.7 |

**Caveat:** 42% of reviews have `Unknown` food signal — likely short/domestic flights or reviews that don't mention food — with a very low mean rating (3.6), suggesting unhappy reviewers who focus on other grievances.

### Amenity & Product Gap
Strong signal, essentially binary in effect: `full_amenities_provided` → mean 9.1 vs. `amenities_absent` → mean 2.4. The `partial_on_request` middle group (mean 6.3) is a useful nuance worth exploring.

### Premium Cabin Value Judgment
Applies to ~37% of reviews (non-`not_applicable`). Among premium passengers, `exceeds_expectations` yields mean 9.4 vs. `poor_value` at 2.3. This is the highest-stakes satisfaction driver for Business/First class analysis.

### Disruption Handling
Affects ~23% of reviews. `negligent_no_support` (n=1,796) averages just 1.7 — the lowest mean of any category in the entire dataset. When things go wrong, poor handling devastates scores.

---

## Weaker / Niche Signals

- **`service_decline_perception`** and **`airline_decline_narrative`** (binary flags) are `True` in only ~6% of reviews each. Effect on rating exists (~1.4 point drop) but insufficient volume for robust analysis.
- **`cs_resolution_quality`**: 80% of reviewers never contacted customer service (`not_contacted`). When they did, poor resolution (n=1,005) far outweighs satisfactory resolution (n=206) — worth noting as a severity filter but not a general analytical lens.
- **`ground_service_quality`**: Mostly `Unknown` — likely not captured reliably enough from review text to use confidently.

---

## Recommended Analytical Direction

**Start with cabin crew attitude**, which is the dominant driver of overall satisfaction across all travel classes and traveller types. Cross-tabulate with:
- **Class** (Economy = 68% of data; crew expectations differ by cabin)
- **Airline** (Turkish Airlines and Qatar Airways each have 1,600+ reviews — sufficient for airline-level crew comparisons)
- **Food quality** as a secondary axis, since food and crew attitude together likely explain the majority of variance in Overall Rating

For premium-focused analysis, `premium_cabin_value_judgment` combined with `amenity_and_product_gap` provides a tighter lens on Business/First class expectations.
