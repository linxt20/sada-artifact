---
dataset: flag_20
scenario: predictive_declined
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: predictive_feature_engineering
focus_variable: "state_declined"
query: "What signals suggest a travel expense will be declined?"
source_table: augment_table/flag_20/predictive_declined/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_20__predictive_declined/analyses/original/analysis.md
wall_seconds: 77.85
---

# Signals suggesting a travel expense will be declined

## Strongest signals
- `category = Travel` is the clearest dataset-wide marker. Travel records are declined at $61/146 = 41.8\%$, versus $23/354 = 6.5\%$ for all non-travel records.
- Within travel, `department` shows moderate separation:
  - `IT`: $6/11 = 54.5\%$ declined
  - `Customer Support`: $35/79 = 44.3\%$
  - `Sales`: $18/44 = 40.9\%$
  - `Development`: $0/5$, but the sample is too small to treat as a stable exception.
- In `short_description`, travel requests phrased as equipment or asset creation/registration are more decline-prone than average travel requests:
  - `Travel equipment asset registration`: $3/5 = 60.0\%$ declined
  - `Automatically generated expense line for creation of travel equipment`: $2/2 = 100\%$
  - Several similar asset/equipment phrases sit around $50\%$, but with very small counts.

## Weak or mixed signals
- `ci` item names do not show strong repeatable patterns. A few items such as `Garmin GPS Navigator`, `International Travel Adapter`, `Travel Accessories Kit`, and `Dell Latitude 7410 Travel Laptop` are each $1/2$ declined, but that is weak evidence.
- `amount` is not a useful standalone signal. Mean amount is similar for `Declined` ($3,792.9$) and `Processed` ($3,927.9$) travel records.
- `opened_at` timing has some noisy pockets, but no stable pattern strong enough for decision use.

## Important exceptions
- High-volume automated descriptions are not always high-risk. `Automatically generated expense line for creation of travel asset` appears 15 times, but only 5 were declined ($33.3\%$), below the travel baseline.
- Some common travel items were not declined in this sample, including `Samsonite Luggage` ($0/3$) and `Dell Latitude 7490` ($0/4$).
- `processed_date` is missing for all declined travel records, but that is an outcome-stage workflow field, not a pre-decision signal.

## Bottom line
The best practical decline signals are:
1. the record being in `category = Travel`,
2. travel requests from `IT`, `Customer Support`, or `Sales`,
3. `short_description` text that frames the expense as travel equipment or asset registration/creation.

Beyond that, evidence is limited. Item name, amount, and timing do not look like strong standalone predictors in this sample.
