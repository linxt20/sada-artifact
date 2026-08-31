---
dataset: company_profile_location
scenario: concept_attribute_focus
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What market-expansion focus should analysts study?"
source_table: augment_table/company_profile_location/concept_attribute_focus/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:09:48.670674+00:00
wall_seconds: 54.58
---

# Market-Expansion Focus Analysis
**Dataset:** Silicon Valley company profiles (199 companies) | **Focus variable:** `growth_lever`

---

## Overview of Growth Levers

| Growth Lever | Count | Share |
|---|---|---|
| `product_led_growth` | 105 | 52.8% |
| `data_driven_expansion` | 24 | 12.1% |
| `network_effects_platform` | 24 | 12.1% |
| `not_present` | 18 | 9.0% |
| `channel_partner_ecosystem` | 17 | 8.5% |
| `training_certification` | 7 | 3.5% |
| `acquisition_integration` | 4 | 2.0% |

**Product-led growth (PLG)** is the dominant market-expansion strategy across the dataset. The next two largest levers—`data_driven_expansion` and `network_effects_platform`—are tied and represent distinct, analyst-worthy secondary strategies.

---

## Key Findings by Dimension

### 1. Product-Led Growth — The Baseline Default
- Captures **53%** of all companies and spans every industry and stage.
- Especially dominant in **enterprise software** (48/77 companies), **cybersecurity** (10/15), and **semiconductors/hardware** (all established names: Apple, AMD, ASUS, Broadcom).
- Prevalent across **enterprise B2B** (67 companies) and **consumer B2C** (20 companies), making it the universal default.

### 2. Data-Driven Expansion — High Opportunity Signal
- **24 companies**, concentrated in **enterprise software** (12), **healthtech** (7), and **cybersecurity** (3).
- Healthtech is disproportionately skewed toward this lever: 7 of 13 healthtech companies (54%) use `data_driven_expansion`, the highest sector share of any non-PLG lever. Companies like 23andMe and genomics/biotech firms are archetypal.
- Skews toward **enterprise B2B** (22/24) and appears at all stages, including **early-stage startups** (6 cases), suggesting it is a deliberate entry strategy—not just a late-stage optimization.
- **Redwood City** and **Mountain View** cluster show the highest raw counts (8 and 6 respectively), possibly reflecting data-rich SaaS corridors.

### 3. Network Effects Platform — Consumer & Marketplace Play
- **24 companies**, dominant in **consumer B2C** (14/24) and marketplace/platform models.
- Leading industries: **other** (6, diverse platforms), **ecommerce/retail** (4/5 companies), **edtech** (3), and **media/entertainment** (3).
- Fintech (Carta, Brex-type companies) and venture-backed marketplaces rely on this lever.
- Notably, this is the **primary non-PLG lever for consumer-facing companies**; enterprise B2B uses it far less (8 cases).

### 4. Channel Partner Ecosystem — Enterprise Incumbent Playbook
- **17 companies**, concentrated in **enterprise software** (8) and **staffing/recruiting** (6/8 companies—the highest sector concentration ratio).
- Also appears in **cybersecurity** (2) and with **established enterprises** (9) and **growth-stage** companies (8).
- Rarely seen in early-stage startups or consumer verticals, confirming it as a mature-market distribution amplifier.

### 5. Acquisition Integration — Small but Notable
- Only **4 companies**, all **established enterprises** in **enterprise software**, all targeting **enterprise B2B**.
- Weak signal numerically, but consistent with large-cap consolidation strategies (e.g., Cisco, Broadcom profile types).

### 6. Training & Certification — Niche Expansion Route
- **7 companies** in **edtech** (6) and enterprise software (1).
- Coursera, Chegg, and similar platforms treat certification as the core growth vector.

---

## Cross-Cutting Patterns for Analysts

| Segment | Primary Lever | Secondary Lever |
|---|---|---|
| Enterprise B2B, early-stage | data_driven_expansion | product_led_growth |
| Consumer B2C | product_led_growth | network_effects_platform |
| Healthtech | data_driven_expansion | product_led_growth |
| Edtech | training_certification | network_effects_platform |
| Staffing/Recruiting | channel_partner_ecosystem | data_driven_expansion |
| Cybersecurity | product_led_growth | channel_partner_ecosystem |
| Venture Capital firms | not_present (14/14) | — |

---

## Exceptions and Weak Evidence

- **Venture capital firms** (14 companies) universally show `not_present` for growth_lever—expected, as they are capital allocators, not product companies. Analysts should exclude them from market-expansion models.
- **Acquisition integration** (n=4) is too small to draw sector-wide conclusions.
- The **`not_present`** group (18 companies) includes a mix of professional services and VC-adjacent firms where growth lever classification is structurally inapplicable.
- Some industry cells have low counts (e.g., mobility/transportation: 5 companies), making patterns there suggestive rather than definitive.

---

## Decision-Ready Summary

Analysts studying market expansion should prioritize **three focus areas**:

1. **Data-driven expansion in healthtech and enterprise SaaS** — the fastest-growing strategic bet among early- and growth-stage companies; signals market entry via proprietary data moats.
2. **Network effects in consumer, edtech, and marketplace verticals** — tied in volume with data-driven expansion; critical for any B2C platform play.
3. **Channel partner ecosystems in cybersecurity and staffing** — under-studied but concentrated; reflects indirect go-to-market at scale for established players.

PLG, while dominant, is the ambient baseline—it differentiates less across companies and is more useful as a control variable than a point of focus.
