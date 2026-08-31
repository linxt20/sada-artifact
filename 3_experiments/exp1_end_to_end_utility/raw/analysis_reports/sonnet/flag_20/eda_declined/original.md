---
dataset: flag_20
scenario: eda_declined
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: exploratory_data_analysis
focus_variable: "state_declined"
query: "What signals in a travel-expense description predict whether it will be declined?"
source_table: augment_table/flag_20/eda_declined/original.csv
generated_at: 2026-07-26T13:32:06.804267+00:00
wall_seconds: 90.77
---

# Signals Predicting Travel-Expense Declination

**Dataset:** 500 expense records · **Focus variable:** `state = Declined` (84 total, 16.8%)

---

## 1. Category Is the Dominant Signal

| Category | Declined | Total | Decline Rate |
|---|---|---|---|
| **Travel** | **61** | **146** | **41.8%** |
| Services | 5 | 47 | 10.6% |
| Assets | 17 | 281 | 6.0% |
| Miscellaneous | 1 | 26 | 3.8% |

**Travel category alone accounts for 73% of all declined records.** The category label in the description is therefore the single strongest predictive signal.

---

## 2. Missing `source_id` — A Near-Perfect Travel Marker

Every Travel row (146/146) has a blank `source_id`, while only 26 of 354 non-Travel rows lack it. Because the field is blank for all Travel records whether approved or declined, it does not differentiate within the Travel category — but **the combination of a blank `source_id` and a Travel-themed description virtually guarantees a Travel categorisation**, which in turn raises the decline probability to ~42%.

---

## 3. No `processed_date` for Any Declined Record

Every declined record (84/84) has an empty `processed_date`. While this is partly structural (declined expenses do not get a processing timestamp), it is a reliable label-consistent signal: **if `processed_date` is empty and the description is travel-related, the probability of "Declined" rises sharply.**

Among all rows with no `processed_date` (205 rows total), 84 are Declined, 0 are Processed — confirming the field is informative even before reading the description.

---

## 4. Description Keyword Patterns

Top terms appearing in declined `short_description` values:

| Term | Count in Declined |
|---|---|
| "travel" | 53 |
| "asset" | 54 |
| "equipment" | 23 |
| "automatically generated" | 21 |
| "expense line" | 16 |
| "creation of travel" | 14 |
| "purchase / procurement" | 10 |

**Key phrase clusters that strongly predict decline:**
- *"Automatically generated expense line for creation of travel asset/equipment"* — the most common boilerplate in declined Travel rows (16 of 61 travel declines match this exact template).
- *"Travel-related hardware asset"* — generic descriptions without a business purpose.
- *"Flight booking / airline ticket / business class"* — high-value travel expenditures.
- *"Luggage / suitcase / travel kit"* — discretionary travel equipment purchases.

Phrases that appear in **processed** Travel rows tend to be more specific: "travel accessory asset entry," "office laptop purchased for business travel," or name a concrete item (e.g., "Dell Latitude 7400 for travel").

---

## 5. `ci` (Configuration Item) — Item Type Matters

Declined Travel records reference items such as:
- GPS devices, luggage trackers, suitcases (discretionary accessories)
- Blanket labels: "Travel Equipment 3," "Company provided travel kits," "Aircraft Airbus A320," "Corporate Jet A320"
- Expensive or ambiguous electronics: "Satellite Phone Model XJ2," "Passport Controller"

Processed Travel records tend to reference identifiable, utilitarian items (specific Dell Latitude models, Samsonite Luggage with model numbers, Travel Kit PRO).

The signal: **vague or non-standard `ci` values in travel records correlate with declination.**

---

## 6. Amount — Weak Differentiator

| Amount Range | Declined | Processed |
|---|---|---|
| < $1,000 | 9 | 24 |
| $1k–$3k | 25 | 78 |
| $3k–$5k | 23 | 85 |
| $5k–$8k | 23 | 85 |
| $8k+ | 4 | 23 |

Mean amount for Declined: **$3,912** vs Processed: **$4,284**. Declined expenses are slightly *lower* on average — amount alone is a poor predictor. Very high amounts ($8k+) are proportionally less likely to be declined.

---

## 7. Department — Modest Signal

| Department | Decline Rate |
|---|---|
| HR | 20.0% (1/5) |
| Sales | 18.4% (26/141) |
| Customer Support | 17.6% (48/272) |
| IT | 16.7% (7/42) |
| Product Management | 12.5% (1/8) |
| Finance | 6.2% (1/16) |
| Development | 0.0% (0/16) |

Development and Finance departments have notably low decline rates, but the sample sizes for non-Customer Support departments are small. Department is a secondary signal driven mostly by the concentration of Travel expenses in Customer Support and Sales.

---

## 8. Summary: Decline Prediction Logic

A travel-expense description is most likely to be declined when **all or most** of the following are true:

1. **`category` = Travel** (raises base rate to 42%)
2. **`source_id` is blank** (consistent with Travel category)
3. **`processed_date` is empty** (no processing event recorded)
4. **`short_description` contains boilerplate** language ("automatically generated expense line for creation of travel asset/equipment") without specifying a business need
5. **`ci` names a vague, discretionary, or non-standard item** (luggage, GPS device, generic "Travel Equipment," aircraft)

Exceptions and weak evidence:
- Some automatically-generated Travel descriptions *are* approved (~57% of auto-generated Travel rows were processed).
- Amount does not help discriminate within Travel expenses.
- Non-Travel categories (Assets, Services) have a minority of declines; their patterns are less consistent and involve heterogeneous reasons (server purchases, cloud services, printers) rather than a systematic policy signal.
