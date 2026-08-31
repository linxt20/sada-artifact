---
dataset: flag_19
scenario: causal_reduce
variant: original
model: substrate-claude-haiku-4-5
query_subtype: what_if
focus_variable: "state_declined"
query: "How can we reduce declined expense submissions?"
source_table: augment_table/flag_19/causal_reduce/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_19__causal_reduce/analyses/original/analysis.md
wall_seconds: 101.64
---

# Reducing Declined Expense Submissions

## Bottom line
The clearest reduction opportunity is **IT, especially Asset submissions**. The overall decline rate is **9.2%** ($46/500$), but **IT is 44.2%** ($19/43$) and contributes **41.3% of all declines** ($19/46$). Within IT, **Assets are 56.5% declined** ($13/23$) and alone account for **28.3% of all declines** ($13/46$).

## Highest-value actions

| Priority area | Evidence from visible columns | Recommended action |
|---|---|---|
| **IT → Assets** | `department=IT`, `category=Assets`: **13/23 declined** | Add a mandatory pre-submit check for asset type, business justification, CI accuracy, and approval routing before submission. |
| **IT → Travel** | `department=IT`, `category=Travel`: **3/10 declined** | Apply the same pre-submit review to travel-related hardware/equipment requests. |
| **Customer Support → Travel** | `department=Customer Support`, `category=Travel`: **6/55 declined** | Tighten required fields and examples for travel-related submissions. |
| **Repeat submitters in IT** | `user=Vernon Engelman`: **7/13 declined**; `user=Helene Iberg`: **7/17 declined** | Target coaching or manager review for repeat submitters with multiple declines. |
| **Early-2024 spike** | `opened_at` year 2024: **25/184 declined** (**13.6%**) vs 2023: **21/316** (**6.6%**) | Audit rule or process changes introduced in early 2024, especially around IT asset approval. |

## Supporting patterns
- **Assets** are the largest decline source by count: **27/310 declined** (**8.7%**), which is **58.7% of all declines**.
- **Travel** has a somewhat higher decline rate: **10/94** (**10.6%**), with concentration in **IT** and **Customer Support**.
- **Amount is not a strong lever**. Declined submissions have a **lower mean `amount`** (**3706**) than Processed (**4436**), and decline rates do not rise steadily with larger amounts. A simple high-amount rule is unlikely to help much.
- **Missing `source_id` is only a secondary signal** overall: **13/111 declined** (**11.7%**) when missing vs **33/389** (**8.5%**) when present. It is more relevant in **Customer Support** (**11.3%** missing vs **4.4%** present), but **not** in IT, where present `source_id` rows still decline heavily (**15/30 = 50.0%**).
- `short_description` values containing **“Automatically”** show a modestly higher decline rate (**18/153 = 11.8%**) than other rows (**28/347 = 8.1%**), suggesting automation-generated requests may need stronger validation.

## Exceptions and weak evidence
- **Miscellaneous** has the highest category decline rate (**3/17 = 17.6%**), but the sample is small.
- Some spikes are likely unstable. For example, **IT in Feb 2024** is **5 declines in 6 submissions**, which is actionable for review but too small to treat as a permanent rate.
- `processed_date` is **not** a usable pre-submit driver: it is filled for **Processed** rows and missing for **Declined/Pending/Submitted** rows, so it reflects outcome status rather than a factor available before review.
- Travel and Miscellaneous appear to have **missing `source_id` by design**, so completeness checks alone will not solve those declines.

## Recommended operating plan
1. **Start with IT Asset submissions**, since that is the most concentrated decline cluster.
2. **Add a pre-submit validation step** for IT and travel-related requests, focused on category selection, CI quality, and business justification.
3. **Coach repeat submitters with multiple declines**, starting with the most concentrated IT users.
4. **Review early-2024 approval changes** to explain the higher decline rate in 2024.
5. **Avoid amount-only controls**; the data does not support them as the main reduction tool.

The data suggests declines are **not broadly distributed**. They are concentrated in a small number of **departments, categories, time periods, and submitters**, so targeted process controls should outperform broad policy tightening.
