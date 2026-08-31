---
dataset: airlines_review
scenario: focus_inference
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's in these airline reviews — I'm not sure which aspect is most worth analyzing."
source_table: augment_table/airlines_review/focus_inference/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:04:33.859267+00:00
wall_seconds: 40.18
---

# Airline Reviews Dataset — Analytical Overview

## Dataset at a Glance

| Dimension | Detail |
|---|---|
| Reviews | 900 verified entries |
| Overall Rating (mean / median) | 6.5 / 8.0 (scale 1–10) |
| Recommend rate | 64% yes, 36% no |
| Cabin mix | Economy 63%, Business 26%, Premium Economy 10%, First 2% |
| Traveller type | Solo Leisure 37%, Couple 27%, Family 20%, Business 16% |

---

## Most Analytically Rewarding Aspect: **Service Quality**

The engineered column `service_quality_theme` is the single strongest discriminator in the dataset. It cleanly partitions review sentiment and recommendation behaviour:

| Service Theme | Mean Overall Rating | Recommend Rate | n |
|---|---|---|---|
| `warm_attentive` | **9.2** | **99%** | 408 |
| `professional_efficient` | 8.3 | 87% | 31 |
| `inconsistent` | 5.8 | 59% | 195 |
| `cold_impersonal` | 3.1 | 16% | 129 |
| `absent_neglectful` | **2.3** | **9%** | 122 |

Nearly half of all reviews (45%) describe crew as warm/attentive, yet ~28% fall into the two negative poles (`cold_impersonal` + `absent_neglectful`). The gap in ratings (9.2 vs 2.3) is striking and suggests that **staff behaviour is the primary driver of satisfaction**, not cabin class or hard product.

The `service_decline_signal` flag reinforces this: reviews flagged as signalling decline average **4.5 vs 7.0** for those that do not (179 / 721 reviews, respectively).

---

## Secondary Focus: **Value Perception**

`Value For Money` shows by far the highest correlation with Overall Rating ($r = 0.89$), while the sub-scores for Food, Seat Comfort, Staff Service, and IFE are only weakly correlated individually (all $r < 0.09$). This means customers integrate their experience into a holistic value judgement rather than rating sub-components independently.

The `premium_class_value_perception` column reinforces this:

| Perception | Mean Rating | n |
|---|---|---|
| `value_justified` | 9.6 | 193 |
| `meets_expectation` | 8.6 | 305 |
| `below_expectation` | 4.9 | 171 |
| `poor_value_for_price` | **2.4** | 230 |

Roughly 45% of reviewers signal value disappointment (`below_expectation` + `poor_value_for_price`), concentrated in Economy and Premium Economy cabins.

---

## Other Notable Patterns

- **Food quality** is explicitly rated in only ~72% of reviews (284 "Unknown"), but where it is rated, 38% are `excellent` vs 28% `poor_quality`. Food runs out or is missing in ~2% of cases — small but consistent.
- **Disruption handling** applies to only ~29% of reviews; of those, 54% are rated `poor_reactive` or `absent_ignored`. Proactive handling is rare (41 cases) but correlates with recovery of satisfaction.
- **Ground service issues** appear in ~20% of reviews, led by check-in problems (61) and booking errors (58).
- **Cabin hardware** is mostly adequate (63%), but 13% flag dated/worn interiors, a weak secondary complaint.
- **Cost-cutting perception** is rare (7.6% of reviews), limiting its analytical weight.

---

## Recommendation

> **Focus the analysis on service quality theme** — it provides the clearest signal, covers almost all reviews, and directly explains recommendation behaviour. A secondary lens on **value-for-money perception by cabin class** would yield actionable findings for commercial decisions.

*Caveats:* The dataset skews heavily toward Economy and leisure travellers; First Class has only 14 reviews, making inferences about that segment weak. The `service_quality_theme` labels are model-inferred, so individual misclassifications are possible, though aggregate patterns appear robust.
