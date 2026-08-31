---
dataset: flag_20
scenario: causal_reduce
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: what_if
focus_variable: "travel_expense_declined_status"
query: "How can we reduce declined travel expenses?"
source_table: augment_table/flag_20/causal_reduce/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_20__causal_reduce/analyses/original/analysis.md
wall_seconds: 119.16
---

# Reducing declined travel expenses

## Key signal in the data

The focus variable is `state`. Travel is the clear problem area:

| `category` | Rows | `Declined` | Decline rate |
|---|---:|---:|---:|
| Travel | 146 | 61 | $41.8\%$ |
| Assets | 281 | 17 | $6.0\%$ |
| Services | 47 | 5 | $10.6\%$ |
| Miscellaneous | 26 | 1 | $3.8\%$ |

Travel expenses are declined far more often than other categories.

## Main patterns linked to travel declines

### 1. Many declined travel rows look like assets, not normal travel spend
Visible `short_description` and `ci` values in declined Travel rows include items such as:

- `Dell Latitude E7470`
- `Global Positioning System Device`
- `Portable Charger Battery Pack`
- `Company SUV Model X`
- `Travel Laptop Dell Inspiron 15`
- `Samsonite Omni PC Luggage`

This suggests a routing problem: asset/equipment purchases are entering `category = Travel`, where they are more likely to be declined.

### 2. Declines are concentrated in a few departments
| `department` | Travel rows | `Declined` | Decline rate |
|---|---:|---:|---:|
| Customer Support | 79 | 35 | $44.3\%$ |
| Sales | 44 | 18 | $40.9\%$ |
| IT | 11 | 6 | $54.5\%$ |
| Finance | 4 | 1 | $25.0\%$ |

Customer Support and Sales account for 53 of 61 travel declines, or about $86.9\%$.

### 3. Low-dollar travel submissions are especially weak
For Travel rows with `amount < 1000`, 9 of 11 were declined ($81.8\%$).

Examples include small equipment-like items rather than core trip costs:
- `Portable Charger Battery Pack`
- `Travel kit item #1`
- `Company Standardized Luggage`
- `Satellite Phone Model XJ2`

This is a strong candidate for a pre-submit screening rule.

### 4. Booking/flight-like travel rows look healthier than equipment-like travel rows
Using `short_description` and `ci` text:

- booking/flight-like rows: 3 declines in 17 rows ($17.6\%$)
- luggage-like rows: 14/35 ($40.0\%$)
- laptop-like rows: 12/35 ($34.3\%$)
- accessory-like rows: 12/31 ($38.7\%$)

The data points to equipment-related travel entries as the bigger source of decline, not standard bookings.

## Recommended actions

1. **Reroute asset-like travel requests before submission.**  
   Use `short_description` and `ci` to detect terms such as laptop, luggage, suitcase, GPS, charger, router, backpack, and vehicle. Send those to an asset/procurement workflow instead of Travel.

2. **Target Customer Support and Sales first.**  
   They drive most travel declines, so department-specific guidance and approval checks should have the largest payoff.

3. **Add a low-value travel exception rule.**  
   For Travel requests under $1000$, require reclassification or manager justification before submission.

4. **Define allowed travel expense types more tightly.**  
   The data supports allowing clearer travel items like tickets and bookings, while challenging equipment-heavy submissions.

## Exceptions and weak evidence

- There is no decline-reason field, so the analysis shows patterns, not confirmed causes.
- `amount` alone is not a reliable driver: declined and processed Travel rows have similar average amounts, aside from the very low-value outliers.
- Some repeated descriptions have small sample sizes, so they are better used as screening cues than hard policy rules.

## Bottom line

To reduce declined travel expenses, the best first move is to **stop asset/equipment purchases from entering the Travel category**, then **tighten review in Customer Support and Sales**, especially for **low-value equipment-like submissions**. The visible data suggests misclassified travel requests are a larger issue than normal booking-related spend.
