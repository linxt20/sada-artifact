---
dataset: flag_20
scenario: predictive_declined
variant: original
model: substrate-claude-haiku-4-5
query_subtype: predictive_feature_engineering
focus_variable: "state_declined"
query: "What signals suggest a travel expense will be declined?"
source_table: augment_table/flag_20/predictive_declined/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_20__predictive_declined/analyses/original/analysis.md
wall_seconds: 124.27
---

## Travel decline signals

The focus variable is `state`, especially whether a row ends in `Declined`.

### Strongest patterns

- **`category = Travel` is the biggest signal in the full table.** Travel is 146 of 500 rows (29%), but it makes up 61 of 84 declined rows (73%). Travel entries are therefore heavily overrepresented among declines.
- **Within travel, decline is common once a final decision exists.** There are 113 finalized travel rows: 61 `Declined` and 52 `Processed`, so about $54\%$ are declined.
- **Department matters inside travel.** Among finalized travel rows:
  - `IT`: 6 of 8 declined ($75\%$) — high rate, but small sample.
  - `Customer Support`: 35 of 60 declined ($58\%$) — strongest by volume.
  - `Sales`: 18 of 35 declined ($51\%$).
  - `Finance`: 1 of 4 declined ($25\%$).
  - `Development`: 0 of 4 declined — too small to treat as stable.
- **Travel rows that look like systems/assets are more decline-prone than ordinary trip items.**
  - Text containing **`system`** appears in 7 finalized travel rows, 6 declined ($86\%$).
  - Text containing **`travel kit`** appears in 6 finalized travel rows, 4 declined ($67\%$).
  - Text containing **`hardware`** appears in 15 finalized travel rows, 9 declined ($60\%$).
  Visible examples include items such as `Travel Management System V2`, `Travel Booking System`, and other travel-coded equipment or asset records.

### Amount pattern

Amount is a signal, but **not** in a simple “higher amount means more decline” way. In finalized travel rows:

- `$0$–$1999`: 16 of 26 declined ($62\%$)
- `$2000$–$3999`: 15 of 33 declined ($45\%$)
- `$4000$–$5999`: 21 of 33 declined ($64\%$)
- `$6000$–$9999`: 9 of 21 declined ($43\%$)

The highest band is **not** the most decline-prone. Low and mid-range travel amounts, especially `$4000$–$6000`, decline more often here.

### Exceptions and weak evidence

- **Common travel item words are mixed.** `laptop` is near baseline (9 of 17 declined, $53\%$). `luggage` is lower (7 of 17, $41\%$). `dell` is also lower (7 of 17, $41\%$). These are weak standalone signals.
- **Airfare/booking language is not consistently negative.** The table contains both declined and processed/submitted examples for tickets, flights, and bookings.
- **Timing effects are weak.** Travel declines are somewhat higher for rows opened between 12:00 and 18:00 ($54\%$) and on Monday ($52\%$), but this looks more like operational noise than a reliable rule.
- **`type` gives no signal** because it is null for all rows.
- **`processed_date` is not a predictive feature.** It is populated for `Processed` rows and missing for `Declined`/`Pending`/`Submitted`, so it reflects workflow status rather than a pre-decision signal.

### Decision-ready takeaway

A travel expense in this table is more likely to be declined when it is:

1. **in the `Travel` category at all** relative to the rest of the dataset,
2. **from `Customer Support` or `IT`** within travel,
3. **described like a travel-related system, kit, hardware item, or asset record** rather than a straightforward trip expense,
4. **in a low or mid amount band**, not necessarily at the highest amounts.

The strongest evidence is for **category**, **department**, and **system/asset-like description content**. Amount helps somewhat. Timing and generic item names are weak signals and should not be overused.
