---
dataset: airlines_review_full
scenario: focus_inference
variant: original
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's in these airline reviews — I'm not sure which aspect is most worth analyzing."
source_table: augment_table/airlines_review_full/focus_inference/original.csv
generated_at: 2026-08-03T05:41:40.034098+00:00
wall_seconds: 37.48
---

# Airline Reviews Dataset — Exploratory Analysis

## Overview

| Property | Value |
|---|---|
| Rows | 8,100 reviews |
| Airlines covered | 10+ (largest: Turkish Airlines 1,685; Qatar Airways 1,624; Emirates 1,350) |
| Date range | Multi-year, reviews up to early 2024 |
| Recommendation split | 53% Yes / 47% No |

---

## Column Structure

Each review contains:
- **Free text**: `Title`, `Reviews`
- **Metadata**: `Airline`, `Class`, `Type of Traveller`, `Route`, `Month Flown`, `Verified`
- **Sub-ratings (1–5)**: `Seat Comfort`, `Staff Service`, `Food & Beverages`, `Inflight Entertainment`, `Value For Money`
- **Outcome variables**: `Overall Rating` (1–10), `Recommended` (yes/no)

---

## Most Important Aspect: **Value For Money**

The single strongest predictor of `Overall Rating` is `Value For Money`, by a wide margin:

| Sub-rating | Correlation with Overall Rating |
|---|---|
| **Value For Money** | **0.88** |
| Staff Service | 0.23 |
| Seat Comfort | 0.21 |
| Food & Beverages | 0.16 |
| Inflight Entertainment | 0.14 |

This is a striking gap. No other sub-rating breaks 0.25. If you are trying to understand what drives passenger satisfaction or the `Overall Rating`, **Value For Money is the right focus variable**.

> ⚠️ **Caveat**: High correlation does not confirm causation — passengers may anchor their sub-ratings around their overall impression, inflating this correlation. Nevertheless, the pattern is consistent across classes and traveller types.

---

## Class Differences

| Class | Mean Overall Rating | Recommended Rate | Mean Value For Money |
|---|---|---|---|
| First Class | 7.60 | 77% | 3.79 |
| Business Class | 6.65 | 66% | 3.52 |
| Premium Economy | 5.97 | 57% | 3.11 |
| Economy Class | 5.18 | 47% | 2.99 |

Economy Class passengers (68% of reviews) are markedly less satisfied, especially on Value For Money — making them the most analytically rich segment for improvement questions.

---

## Airline Variation

Among the top 10 airlines by review volume, mean Overall Rating ranges from **3.68 (Turkish Airlines)** to **7.95 (All Nippon Airways)**:

| Airline | Mean Overall Rating |
|---|---|
| All Nippon Airways | 7.95 |
| EVA Air | 7.42 |
| Qatar Airways | 7.20 |
| Japan Airlines | 7.10 |
| Singapore Airlines | 6.54 |
| Korean Air | 6.49 |
| Cathay Pacific | 6.17 |
| Emirates | 4.67 |
| Air France | 4.64 |
| Turkish Airlines | 3.68 |

The lower-rated airlines have large review counts, suggesting higher exposure or more dissatisfied customers writing reviews — selection bias is possible.

---

## Traveller Type

Solo Leisure travellers rate airlines highest on average (6.07); Family Leisure travellers lowest (5.14). Business travellers sit near the middle (5.38), which may reflect higher baseline expectations.

---

## Recommendations for Analysis

1. **Primary focus**: Model or explore `Overall Rating` / `Recommended` as outcome variables, with `Value For Money` as the most predictive driver.
2. **Segmentation**: Class (Economy vs. premium) and Airline produce strong variation and are clean categorical splits.
3. **Text mining**: The `Reviews` and `Title` columns are rich for sentiment analysis or aspect extraction, and could validate whether the numeric sub-ratings align with what passengers actually write about.
4. **Weak signal**: `Inflight Entertainment` and `Food & Beverages` have the lowest correlation with outcomes — less worth prioritizing unless the question is specifically about those amenities.
