---
dataset: flag_12
scenario: concept_attribute_inefficiency
variant: original
model: substrate-claude-haiku-4-5
query_subtype: faceted_decomposition
focus_variable: "incident_inefficiency_reasons"
query: "What recurring issues drive resolution inefficiency?"
source_table: augment_table/flag_12/concept_attribute_inefficiency/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_12__concept_attribute_inefficiency/analyses/original/analysis.md
wall_seconds: 106.53
---

# Resolution inefficiency: recurring issue patterns

## Scope
This dataset contains **500 incidents**. Resolution time is derived as $closed\_at-opened\_at$.

- **Overall mean resolution time:** **178.4 hours**
- **Overall median resolution time:** **173.2 hours**

## Main findings

### 1. Repeated **hardware peripheral** incidents, especially **printer** tickets, are the clearest recurring driver
The dataset is dominated by hardware work:

- **Hardware category:** **406 / 500**
- **Hardware assignment group:** **405 / 500**

Within that hardware-heavy mix, printer complaints recur most often and run slightly slower than the overall baseline:

- **Printer-related theme:** **202 cases** (**40.4%** of all incidents), **183.6 mean hours**
- Repeated printer descriptions include:
  - **“Printer not working properly”** — **30 cases**, **211.6 mean hours**
  - **“Printer not functioning properly”** — **26 cases**, **179.2 mean hours**
  - **“Printer is not working properly”** — **14 cases**, **174.3 mean hours**
  - **“Printer not responding”** — **11 cases**, **185.7 mean hours**

This combination of **high frequency** and **often above-average duration** makes printer incidents the strongest practical source of resolution inefficiency.

### 2. **Keyboard** issues appear less often than printer issues, but are also slow
Keyboard incidents are another repeated slow cluster:

- **Keyboard-related theme:** **56 cases**, **187.0 mean hours**
- Repeated descriptions include:
  - **“Keyboard not functioning properly”** — **5 cases**, **256.8 mean hours**
  - **“Keyboard not responding”** — **6 cases**, **202.7 mean hours**
  - **“Keyboard malfunctioning”** — **5 cases**, **201.2 mean hours**

These are not as common as printer tickets, but they are consistently slower and likely add queue drag inside hardware support.

### 3. Some **software installation/help** requests can be slow, but evidence is mixed
Software overall is **not** the main inefficiency driver:

- **Software category:** **33 cases**, **153.6 mean hours** — faster than the dataset average
- **Service Desk / inquiry-help** work is also not clearly slower overall

However, one repeated description stands out:

- **“Need assistance with software installation”** — **7 cases**, **247.6 mean hours**

That said, evidence is not fully consistent:

- **“Need help with software installation”** — **4 cases**, **45.8 mean hours**

So software-install requests may contain a specific slow subpattern, but the dataset does **not** support a broad claim that software incidents generally drive inefficiency.

## Supporting operational patterns

### 4. Inefficiency is more associated with **queue/process location** than with stated severity
Priority does not explain the slowdown well:

- **2 - High:** **394 cases**, **180.0 mean hours**
- **1 - Critical:** **27 cases**, **167.0 mean hours**

If severity were the main driver, critical incidents would be expected to take longer, but they do not. This points more toward **recurring issue type and handling process** than formal priority.

### 5. Hardware-heavy handling paths look slower
Mean resolution time varies across handlers:

- **Assigned to Luke Wilson:** **116 cases**, **195.5 mean hours**
- **Assigned to Fred Luddy:** **90 cases**, **165.0 mean hours**

And by update source:

- **sys_updated_by = system:** **160 cases**, **198.9 mean hours**
- **admin:** **174 cases**, **173.9 mean hours**
- **employee:** **166 cases**, **163.4 mean hours**

These are correlations only, but they reinforce the pattern that slower cases are concentrated in certain handling paths, especially around recurring hardware work.

## Important exceptions

- **Monitor/display issues** are common (**71 cases**) but not clearly inefficient: **173.3 mean hours**, near the dataset median.
- **Network** incidents are not a major inefficiency source here: **22 cases**, **161.6 mean hours**.
- Several very slow repeated descriptions have **small counts** and should be treated cautiously, such as:
  - **“The company printer is malfunctioning”** — **3 cases**, **282.0 mean hours**
  - **“Unable to connect to VPN”** — **3 cases**, **203.1 mean hours**

## Bottom line
The strongest recurring driver of resolution inefficiency is a **large volume of hardware peripheral tickets**, especially **printer issues**, with **keyboard issues** as a secondary slow cluster. The pattern is strengthened by slower averages in the **hardware queue** and some handler/process signals, while **priority**, **network**, and most **software** work do not explain the inefficiency as well.

## Limits
This file does not include reopen counts, transfer counts, SLA breaches, or workflow history. The evidence supports **pattern identification**, not a causal proof of why those tickets take longer.
