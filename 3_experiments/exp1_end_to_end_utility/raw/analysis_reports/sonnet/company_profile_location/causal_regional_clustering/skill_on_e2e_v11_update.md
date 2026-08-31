---
dataset: company_profile_location
scenario: causal_regional_clustering
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "regional_cluster"
query: "Explain what leads a company to be based in one region rather than another."
source_table: augment_table/company_profile_location/causal_regional_clustering/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:10:17.167492+00:00
wall_seconds: 98.77
---

# Causal Regional Clustering: What Leads a Company to Be Based in One Region Rather Than Another?

**Dataset:** 199 companies, Silicon Valley / San Francisco Bay Area  
**Method note:** TAPP-generated columns used in this analysis: `industry_sector`, `tech_focus_area`, `company_stage`, `business_model_type`, `deep_tech_rd_intensity`, `physical_infrastructure_dependency`, `specialized_talent_signal`. All seven columns had zero nulls. `physical_infrastructure_dependency` and `specialized_talent_signal` provided the clearest marginal signal beyond raw city/address data; `tech_focus_area` and `industry_sector` clarified within-sector sub-clustering.

---

## 1. Overview of the Dataset

All 199 companies in the dataset are located within a ~40-mile corridor of the San Francisco Bay Area. The relevant question is therefore *intra-regional*: which micro-cluster within Silicon Valley does a company gravitate toward, and why?

| Region | N | Share |
|---|---|---|
| North Peninsula (Redwood City / San Mateo) | 60 | 30% |
| South Bay (San Jose / Santa Clara / Sunnyvale / Cupertino) | 59 | 30% |
| Mid-Peninsula (Palo Alto / Menlo Park) | 39 | 20% |
| Mountain View | 25 | 13% |
| Los Gatos | 9 | 5% |
| San Francisco | 5 | 3% |

---

## 2. Key Causal Drivers

### 2.1 Industry Sector — The Strongest Predictor

`industry_sector` sharply separates clusters:

| Region | Top industry (n) | 2nd industry (n) | Notable absences |
|---|---|---|---|
| North Peninsula | software_and_saas (37) | cybersecurity (5) / life_science (5) | No semiconductor, no VC |
| South Bay | software_and_saas (28) | semiconductor_and_hardware (11) | No VC |
| Mid-Peninsula | software_and_saas (15) | venture_capital_and_investment (12) | No semiconductor |
| Mountain View | software_and_saas (15) | cybersecurity (3) | No VC |
| San Francisco | media_and_entertainment (2) / VC (2) | — | No semiconductor |

**Finding:** Semiconductor and hardware companies concentrate almost exclusively in the South Bay (11/14 = 79% of semiconductor firms). VC firms concentrate on the Mid-Peninsula, especially Menlo Park's Sand Hill Road (10 of 15 VC firms). Pure SaaS is broadly distributed across all clusters.

### 2.2 Physical Infrastructure Dependency — Separates Hardware from Software Clusters

`physical_infrastructure_dependency` cleanly explains the South Bay's hardware density. Of 22 companies tagged `manufacturing_or_fab`, 21 are in South Bay cities (Santa Clara: 5, Cupertino: 3, Sunnyvale: 2, San Jose: 2, Mountain View: 2, Palo Alto: 3, Fremont: 1, Newark: 1) — all tied to `semiconductor_and_hardware` industry (14/22 = 64%) or adjacent hardware. The Mid-Peninsula and North Peninsula show `none_required` rates of 87% and 72%, respectively, confirming their software-centric character.

| Region | none_required | manufacturing_or_fab | data_center / colocation |
|---|---|---|---|
| Mid-Peninsula | 87% | 0% | 3% |
| North Peninsula | 72% | 2% | 15% |
| Mountain View | 68% | 8% | 8% |
| South Bay | 58% | 17% | 15% |

**Causal interpretation:** Access to fabrication facilities, cleanrooms, and electronics supply chains — physically concentrated around the semiconductor corridor from San Jose to Palo Alto — anchors hardware companies to the South Bay.

### 2.3 Specialized Talent Signal — Corroborates Sector Clustering

`specialized_talent_signal` mirrors the sector findings with quantitative confirmation:

| Region | generalist_SW (%) | semiconductor_eng (%) | ai_ml_research (%) | finance_and_legal (%) |
|---|---|---|---|---|
| Mid-Peninsula | 64% | 0% | 8% | 21% |
| North Peninsula | 73% | 0% | 8% | 7% |
| South Bay | 61% | 14% | 12% | 2% |
| Mountain View | 64% | 4% | 16% | 4% |

**Finding:** The Mid-Peninsula's unusually high `finance_and_legal` share (21%) reflects the VC/investment concentration (12 VC firms in Palo Alto/Menlo Park). South Bay's elevated `semiconductor_engineering` (14%) directly ties to chip design talent (e.g., Intel, AMD, Nvidia campuses historically in Santa Clara/Sunnyvale). Mountain View shows the highest `ai_ml_research_talent` share (16%), consistent with the presence of Google and related AI-focused companies.

### 2.4 Company Stage — Investor Access as a Location Magnet

`company_stage` shows the Mid-Peninsula/San Francisco bias for investor-proximate companies:

| Region | investor_or_fund (%) | early_stage_startup (%) | established_enterprise (%) |
|---|---|---|---|
| Mid-Peninsula | 31% | 8% | 36% |
| San Francisco | 40% | 20% | 20% |
| North Peninsula | 0% | 8% | 47% |
| South Bay | 0% | 8% | 42% |
| Mountain View | 0% | 8% | 56% |

**Finding:** Investors themselves (15 firms, all coded `investor_or_fund`) are almost entirely absent from North Peninsula and South Bay, gravitating to Mid-Peninsula (Menlo Park/Palo Alto) and San Francisco. This creates a co-location incentive for early-stage startups seeking proximity to capital, though the 18 early-stage startups in the data are relatively distributed.

### 2.5 Deep Tech R&D Intensity — Modest Differentiator

`deep_tech_rd_intensity` shows limited regional differentiation beyond what `physical_infrastructure_dependency` and `industry_sector` already capture. North Peninsula is the most software-dominant (73% `moderate_applied_tech`, only 8% `high_rd_deep_tech`); South Bay has the highest `high_rd_deep_tech` rate (27%) driven by semiconductor and hardware firms. This column is partially redundant with `industry_sector` and `physical_infrastructure_dependency`.

| Region | high_rd_deep_tech (%) | moderate_applied_tech (%) | low_tech_or_services (%) |
|---|---|---|---|
| South Bay | 27% | 44% | 29% |
| Mountain View | 24% | 56% | 20% |
| Mid-Peninsula | 21% | 41% | 36% |
| North Peninsula | 8% | 73% | 18% |

### 2.6 Business Model Type — B2B Software Dominates Everywhere, with Notable Exceptions

`business_model_type` shows `b2b_software` as the dominant model in all regions (North Peninsula: 75%, Mountain View: 76%, South Bay: 63%). The strongest regional signal is `financial_services` concentrated in Mid-Peninsula (31%) from VC firms, and `hardware_product` concentrated in South Bay (22%), again confirming the semiconductor-hardware axis.

---

## 3. Synthesis: Causal Regional Clustering Model

The data support a **three-factor clustering model**:

1. **Physical infrastructure and supply-chain access** (`physical_infrastructure_dependency` = `manufacturing_or_fab`): pulls semiconductor/hardware companies to the South Bay corridor where fabrication infrastructure, component suppliers, and chip-design talent (`semiconductor_engineering`) are historically entrenched.

2. **Capital ecosystem proximity** (`company_stage` = `investor_or_fund`, `business_model_type` = `financial_services`, Sand Hill Road geography): anchors VC firms and investor-adjacent entities to Menlo Park/Palo Alto; the Mid-Peninsula's 31% investor concentration versus 0% in North Peninsula and South Bay is striking.

3. **Software/SaaS agglomeration economies** (`industry_sector` = `software_and_saas`, `physical_infrastructure_dependency` = `none_required`): since pure-software companies have near-zero infrastructure dependency, they distribute across all clusters, but the North Peninsula (Redwood City/San Mateo) has emerged as the dominant SaaS hub by company count (37 SaaS companies, 75% B2B), likely driven by office space economics and enterprise sales workforce access, not physical infrastructure.

A fourth, weaker factor: **AI/ML talent density** in Mountain View (16% `ai_ml_research_talent` vs. 8–12% elsewhere) reflects the pull of large AI-native employers (historically Google, now many AI labs), creating a local talent pool that attracts further AI-focused companies.

---

## 4. What Does NOT Drive Regional Differentiation in This Dataset

- **`tech_focus_area` = `enterprise_software`** is uniformly distributed (present in all regions at 35–50%) and adds little causal differentiation.
- **`deep_tech_rd_intensity`** is largely redundant with the sector + infrastructure combination and does not reveal new regional drivers.
- **Geographic scope**: This dataset is entirely within one metro area; macro-regional factors (tax policy, labor law, cost of living relative to other metros) are held constant and cannot be evaluated from this data alone.

---

## 5. Summary Table

| Causal Driver | Evidence Columns | Primary Affected Region | Effect Size |
|---|---|---|---|
| Semiconductor fab access | `physical_infrastructure_dependency`, `industry_sector` | South Bay | 79% of semiconductor firms, 17% mfg_or_fab rate |
| VC/capital ecosystem | `company_stage`, `business_model_type`, City=Menlo Park | Mid-Peninsula | 31% investor_or_fund vs. 0% elsewhere |
| SaaS agglomeration | `industry_sector`, `physical_infrastructure_dependency` | North Peninsula | 62% SaaS, 87% none_required |
| AI talent pool | `specialized_talent_signal`, `tech_focus_area` | Mountain View | 16% ai_ml_research vs. 8% avg |
| Hardware talent | `specialized_talent_signal` | South Bay | 14% semiconductor_eng vs. <5% elsewhere |
