---
dataset: flag_9
scenario: eda_hardware
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: exploratory_data_analysis
focus_variable: "hardware_incident"
query: "What in an incident's description tends to signal it's a hardware problem?"
source_table: augment_table/flag_9/eda_hardware/original.csv
generated_at: 2026-07-26T13:44:42.862834+00:00
wall_seconds: 79.08
---

# EDA: Hardware Incident Signal Analysis

**Dataset:** `original.csv` — 600 IT incidents, 13 columns  
**Focus variable:** `category` (target = `Hardware`, n = 182 / 600 = 30.3%)  
**Key text field:** `short_description`

---

## 1. Dataset Overview

| Category | Count | Share |
|---|---|---|
| Hardware | 182 | 30.3% |
| Software | 130 | 21.7% |
| Inquiry / Help | 108 | 18.0% |
| Database | 102 | 17.0% |
| Network | 78 | 13.0% |

All 182 hardware incidents are routed to the `Hardware` assignment group — making `assignment_group` a perfect post-classification signal, but circular for prediction from description alone.

---

## 2. Device / Component Keywords (Strongest Signals)

The table below shows word frequency in hardware descriptions vs. all other categories (lift = relative prevalence ratio):

| Keyword | HW occurrences | Non-HW occurrences | Lift |
|---|---|---|---|
| **printer** | 81 | 0 | ~372× |
| **monitor** | 26 | 0 | ~119× |
| **keyboard** | 24 | 0 | ~110× |
| **computer** | 11 | 0 | ~51× |
| **screen** | 9 | 0 | ~41× |
| **mouse** | 7 | 0 | ~32× |
| **hard / hard drive** | 7 | 0 | ~32× |
| **fan** | 4 | 0 | ~18× |
| **desktop** | 18 | 3 | ~12× |

**Naming a physical device is the single strongest predictor.** These words appear exclusively (or near-exclusively) in hardware incidents.

---

## 3. Action / State Phrases (Secondary Signals)

| Phrase | HW count |
|---|---|
| malfunction / malfunctioning | 38 + 22 = 60 |
| not working | 33 |
| not functioning | 24 |
| not responding | 16 |
| failure | 10 |
| not turning on | 7 |
| faulty | 6 |
| flickering | 6 |
| not displaying | 4 |
| overheating | 3 |
| unable to boot | 2 |

These phrases describe **physical failure modes** — power, display, responsiveness, and thermal issues. They almost always appear alongside a device name (e.g., *"Printer not responding"*, *"Monitor flickering"*, *"Fan not working in desktop computer"*).

The word **"not"** alone appears in 92/182 hardware descriptions (50%) vs. 16/418 non-hardware (4%), confirming that **negation + device noun is a near-definitive pattern**.

---

## 4. Typical Description Structures

Hardware descriptions follow a small set of templates:

1. **`<Device> not <verb>-ing [properly/correctly]`** — e.g., *"Printer not functioning correctly"*
2. **`<Device> malfunction[ing] [in <location>]`** — e.g., *"Printer malfunctioning in office 4B"*
3. **`<Device> failure [on/in <machine type>]`** — e.g., *"Hard drive failure in office desktop machine"*
4. **`Unable to <boot/power on> <device>`** — e.g., *"Unable to boot laptop"*
5. **`Faulty <device> needs replacement`** — e.g., *"Faulty server hardware needs replacement"*

---

## 5. Priority Profile

Hardware incidents skew higher-severity than average:

| Priority | Hardware | Non-Hardware |
|---|---|---|
| 1 - Critical | 8.8% | 10.3% |
| **2 - High** | **79.7%** | **60.3%** |
| 3 - Moderate | 11.5% | 29.2% |

~80% of hardware incidents are `2 - High` priority — somewhat above non-hardware (60%). This is a weak secondary signal; priority alone cannot distinguish hardware from software or network incidents.

---

## 6. Exceptions and Weak Evidence

- **"Hardware"** as a literal word appears in only 10/182 descriptions (~5%); most hardware tickets do **not** self-label as "hardware."
- **"computer"** and **"desktop"** appear occasionally outside the Hardware category (3 non-HW occurrences each); the device-noun signal is strong but not infallible.
- **"not working"** is the phrase most at risk of false positives — it can appear in software or network complaints, but the combination with a physical device name is reliable.
- Location identifiers (e.g., *"office 4B"*, *"Finance department"*) appear in some printer/hardware descriptions but are not independently predictive.

---

## 7. Decision-Ready Summary

> **An incident description signals a hardware problem when it names a physical device (printer, monitor, keyboard, mouse, hard drive, fan, desktop, laptop) combined with a failure verb (not working, not functioning, not responding, malfunctioning, failure, flickering, overheating, unable to boot, faulty).** The device name alone is almost sufficient — none of the 10 highest-lift device words appeared in non-hardware tickets. Absence of both a physical device noun and a physical failure phrase makes a hardware classification very unlikely.
