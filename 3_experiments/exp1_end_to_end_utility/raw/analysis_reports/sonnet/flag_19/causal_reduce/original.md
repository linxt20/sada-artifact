---
dataset: flag_19
scenario: causal_reduce
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: what_if
focus_variable: "state_declined"
query: "How can we reduce declined expense submissions?"
source_table: augment_table/flag_19/causal_reduce/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_19__causal_reduce/analyses/original/analysis.md
wall_seconds: 91.09
---

# Reducing declined expense submissions

## Bottom line

The clearest reduction opportunity is **not broad policy tightening**. It is a **targeted fix to IT asset-related submissions**, plus lighter controls for **travel** and **incomplete records**.

- The dataset has **500 submissions** in `state`:
  - **46 Declined** ($9.2\%$ of all submissions)
  - **333 Processed**
  - **121 still open** (`Pending` or `Submitted`)
- On resolved items only (`Processed` + `Declined`), the decline rate is **$46 / 379 = 12.1\%$**.

## Main patterns tied to declines

### 1. `department = IT` is the strongest concentration
- IT has **19 declines out of 43 submissions**: **44.2%**
- On resolved IT items, the decline rate is **19 / 35 = 54.3%**
- IT alone contributes **19 of 46 declines**: **41.3%** of all declines

This is far above other departments:
- Customer Support: **16 / 267 = 6.0%**
- Sales: **6 / 122 = 4.9%**
- Finance: **2 / 22 = 9.1%**

**Implication:** a focused IT workflow change should reduce declines more than a company-wide rule change.

### 2. `category = Assets` drives the largest share of declines
- Assets has **27 declines out of 310 submissions**: **8.7%**
- Assets accounts for **58.7% of all declines** because it has the most volume

The sharper finding is the intersection:

- **IT + Assets = 13 declines out of 23 submissions**: **56.5%**
- This single segment contributes **13 of 46 declines**: **28.3%** of all declines

Many declined rows in this segment have `short_description` values like **"Automatically generated..."** and repeated hardware/laptop `ci` values such as **"Dell Latitude 7490"**.

**Implication:** the biggest win is likely in the IT asset submission flow, especially automated or hardware-creation entries.

### 3. Travel is a secondary problem area
- `category = Travel`: **10 / 94 = 10.6%** declined
- On resolved travel items: **10 / 67 = 14.9%**

Travel is not as severe as IT Assets, but it is the **second-largest decline source**:
- Customer Support + Travel: **6 declines**
- IT + Travel: **3 declines**

Some declined travel rows look like hardware/equipment requests rather than classic travel reimbursement, based on `short_description` and `ci` values such as **Pocket WiFi**, **GPS device**, and **travel equipment asset**.

**Implication:** travel-related equipment may need clearer routing or category rules.

### 4. Missing `source_id` is associated with somewhat higher declines
- `source_id` present: **33 / 389 = 8.5%** declined
- `source_id` missing: **13 / 111 = 11.7%** declined
- On resolved items:
  - present: **11.0%**
  - missing: **16.5%**

This suggests incomplete linkage may matter.

**Important exception:** in IT, missing `source_id` is **not** the main issue; IT submissions with a present `source_id` still decline heavily. So this is a **general hygiene signal**, not the root cause of the IT problem.

### 5. Amount is not the main decline driver
Declines are **not concentrated in the highest amounts**:

- `amount <= 500`: **16.7%** declined
- `$5000 < amount <= 10000$`: **6.7%** declined

Declined submissions also have a lower mean `amount` than processed ones:
- Declined mean: **3705.8**
- Processed mean: **4436.2**

**Implication:** stricter review only for large claims is unlikely to address most declines.

## Recommended actions

| Priority | Action | Data basis |
|---|---|---|
| 1 | Add a pre-submit validation/review step for **IT Asset** submissions | IT Assets decline at **56.5%** |
| 2 | Audit the **automated asset-generation workflow** and mapping rules | Declined IT asset rows frequently show **"Automatically generated..."** descriptions |
| 3 | Review repeat decline clusters tied to **specific submitter workflows** | **Vernon Engelman** and **Helene Iberg** account for **14 of 46 declines**; both are concentrated in IT asset/travel/service requests |
| 4 | Tighten category guidance for **travel-related equipment** | Travel declines are **10.6%**, with several equipment-like requests inside Travel |
| 5 | Require or auto-fill `source_id` where possible | Missing `source_id` has a higher resolved decline rate: **16.5% vs 11.0%** |

## What not to overclaim

- **User names are likely proxies for workflow or role**, not proof of individual behavior problems.
- `Miscellaneous` shows a high decline rate (**17.6%**), but that is only **17 rows**, so evidence is weak.
- Month and hour spikes exist, but sample sizes are modest; they are weaker than the department/category patterns.
- Repeated Dell/laptop `ci` values suggest a hardware workflow issue, but the data does **not** show the actual decline reason.

## Decision-ready conclusion

To reduce declined expense submissions, focus first on **IT asset requests**, especially **automated hardware-entry flows**. That segment is the most concentrated decline source by far. Next, clean up **travel-related equipment routing** and improve **record completeness** such as `source_id`. A broad amount-based or company-wide approval crackdown is less supported by this dataset.
