---
dataset: company_profile_location
scenario: causal_regional_clustering
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "regional_cluster"
query: "Explain what leads a company to be based in one region rather than another."
source_table: augment_table/company_profile_location/causal_regional_clustering/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:09:37.861859+00:00
wall_seconds: 66.33
---

# Regional Location Drivers for Silicon Valley Companies

## Dataset Overview

The dataset contains 202 companies all located within the greater San Francisco Bay Area, concentrated across four sub-regions:

| Region | n | % of total |
|---|---|---|
| Peninsula (Redwood City, San Mateo, Menlo Park, Palo Alto…) | ~97 | ~48% |
| South Bay (Mountain View, Sunnyvale, Santa Clara, San Jose…) | ~82 | ~41% |
| Los Gatos | 9 | ~4% |
| San Francisco | 5 | ~2% |

Because all companies are within a single metro area, "region" here means sub-district choice within Silicon Valley rather than a broader national or global comparison.

---

## Key Drivers of Sub-Regional Location

### 1. Talent Ecosystem Dependency — Strongest Differentiator

`talent_ecosystem_dependency` is the single most consistently structured variable across regions.

| Region | software_engineering % | deep_tech_research % | clinical_scientific % |
|---|---|---|---|
| San Francisco | 80% | 20% | 0% |
| Peninsula | 64% | 29% | 4% |
| South Bay | 48% | 40% | 5% |

- **San Francisco** skews almost entirely toward software/SaaS talent pools.
- **South Bay** draws a meaningfully higher share of **deep_tech_research** firms (40%), consistent with the presence of major semiconductor and hardware campuses (Intel, Nvidia, AMD in Santa Clara/San Jose).
- **Peninsula** is the most balanced but still software-dominant.

### 2. Industry Sector — Venture Capital Clusters on Sand Hill Road

Venture capital firms concentrate almost exclusively on the **Peninsula** (Menlo Park / Palo Alto), where Sand Hill Road is located:

- 14 of 18 VC firms (78%) are Peninsula-based — all on or near Sand Hill Road (Menlo Park, Palo Alto).
- Peninsula VC share: **15%** of its companies vs. **1%** in South Bay.

This reflects a self-reinforcing pattern: portfolio companies (software, biotech) locate nearby to maintain investor proximity.

### 3. Physical Infrastructure Dependency — Manufacturing Pulls to South Bay

Companies with `physical_infrastructure_dependency = manufacturing_fab` overwhelmingly cluster in the **South Bay**:

- 18 of 24 manufacturing/fab-dependent companies (75%) are in South Bay cities (Santa Clara, Mountain View, Cupertino, San Jose, Sunnyvale, Fremont).
- South Bay manufacturing share: **22%** vs. **4%** Peninsula.

This reflects proximity to semiconductor fabrication facilities, component suppliers, and logistics corridors (I-880, Port of Oakland).

`data_center_colocation` firms (n=8) also lean South Bay (6/8), consistent with existing data-center infrastructure in Santa Clara.

### 4. Core Technology Focus — Semiconductors Anchor in South Bay

| Region | semiconductors_hardware % | AI/ML % | cloud_data % |
|---|---|---|---|
| South Bay | 11% | 12% | 17% |
| Peninsula | 1% | 8% | 16% |
| San Francisco | 0% | 0% | 20% |

Hardware/semiconductor companies (n=21) locate almost entirely in South Bay cities, driven by established chip-design ecosystems and proximity to fabs. AI/ML firms are more evenly spread.

### 5. Company Stage — Early-Stage Startups vs. Investment Firms

- **Early-stage startups** (n=25) favor South Bay (15/25 = 60%) — lower rents relative to SF, proximity to engineering talent pipelines (Stanford, SJSU, UC Santa Cruz).
- **Investment firm / incubators** (n=15) favor the Peninsula (13/15 = 87%), anchored to Sand Hill Road.
- **Established enterprises** are distributed broadly across both regions.

### 6. Regulatory Domain — Minimal Geographic Signal

`regulatory_compliance_domain` shows weak regional patterning. Most companies (77%) are `none_unregulated` regardless of location. `cybersecurity_govtech` firms (n=17) slightly concentrate in South Bay (9) vs. Peninsula (5), possibly near defense/government contractors, but sample sizes are small.

`healthcare_hipaa` firms (life sciences, n=14) split across Peninsula and South Bay with no strong concentration, weakening any simple "biotech corridor" hypothesis for this dataset.

---

## Summary of Causal Pathways

```
Talent type needed
  ├─ software_engineering → Peninsula (Sand Hill proximity) or San Francisco
  └─ deep_tech / semiconductor → South Bay (existing hardware ecosystems)

Physical infrastructure needed
  ├─ manufacturing_fab / data_center → South Bay (industrial land, existing facilities)
  └─ none_digital_only → any sub-region (firm chooses on other factors)

Capital access
  └─ VC-backed / investment firm → Peninsula (Sand Hill Road concentration)

Company stage
  ├─ early startup → South Bay (cost, talent pipeline)
  └─ investment firm → Peninsula
```

---

## Caveats and Weak Evidence

- The dataset is **entirely within one metro area**; findings describe intra-Bay-Area clustering, not broader regional choice (e.g., why Silicon Valley vs. Austin vs. Boston).
- **San Francisco** has only 5 companies — patterns there (100% digital, 80% software talent) are illustrative but not statistically robust.
- **Los Gatos** (n=9) is dominated by one major employer cluster (hardware/media); generalizations are unreliable.
- Causal direction is inferred from co-occurrence patterns; no temporal data is available to confirm whether infrastructure attracted firms or firms attracted infrastructure.
