---
dataset: company_profile_location
scenario: predictive_region
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "regional_cluster"
query: "What features can be extracted from a company's business description to predict its regional cluster?"
source_table: augment_table/company_profile_location/predictive_region/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:10:34.163880+00:00
wall_seconds: 90.69
---

# Predicting Regional Cluster from Company Business Description
**Dataset:** 199 Bay Area companies · 16 columns (7 original + 9 TAPP-generated)  
**Outcome variable:** Regional cluster derived from `City`, `Latitude`, and `Longitude`

---

## 1. Regional Cluster Definition

Five sub-regions were defined from the structured `City`, `Latitude`, and `Longitude` columns:

| Region | Cities | N | Mean Lat | Mean Lon |
|---|---|---|---|---|
| Mid_Peninsula | Redwood City, San Mateo, Menlo Park, Palo Alto area north | 73 | 37.504 | −122.246 |
| South_Bay | San Jose, Santa Clara, Fremont, Newark | 43 | 37.389 | −121.940 |
| MV_Sunnyvale | Mountain View, Sunnyvale, Cupertino | 40 | 37.392 | −122.054 |
| Palo_Alto_Area | Palo Alto, Los Altos, Los Gatos, Campbell | 34 | 37.375 | −122.090 |
| North_Peninsula | San Francisco, San Bruno, Burlingame | 7 | 37.734 | −122.399 |

These five clusters are geographically separable; longitude is the strongest single numeric predictor (South_Bay mean −121.94 vs. North_Peninsula −122.40, a 0.46° spread).

---

## 2. Method Note

TAPP-generated columns used in this analysis: `industry_sector`, `company_type`, `company_maturity`, `core_tech_domain`, `cloud_infra_signal`, `market_segment`, `customer_type`, `delivery_model`, `hardware_software_signal`. All nine columns were evaluated; six (`industry_sector`, `company_type`, `company_maturity`, `core_tech_domain`, `delivery_model`, `hardware_software_signal`) show meaningful regional signal; three (`cloud_infra_signal`, `market_segment`, `customer_type`) are weak-to-moderate differentiators and are noted as such.

---

## 3. Features with Strong Regional Signal

### 3.1 Industry Sector (`industry_sector`)

| Region | enterprise_software | semiconductor_hardware | venture_capital_finance | data_analytics | life_science_health |
|---|---|---|---|---|---|
| Mid_Peninsula | **35.6%** | 0.0% | **15.1%** | 15.1% | 6.8% |
| South_Bay | 30.2% | **18.6%** | 0.0% | 7.0% | 2.3% |
| MV_Sunnyvale | 17.5% | 5.0% | 0.0% | 15.0% | 12.5% |
| Palo_Alto_Area | 29.4% | 2.9% | 5.9% | 5.9% | 2.9% |
| North_Peninsula | 14.3% | 0.0% | **28.6%** | 0.0% | 14.3% |

**Key signal:** Semiconductor/hardware descriptions are a strong predictor of South_Bay (8/11 semiconductor companies, 18.6% of that cluster vs. ≤5% elsewhere). Venture-capital language is concentrated in Mid_Peninsula (15.1%) and North_Peninsula (28.6%). Enterprise-software descriptions skew Mid_Peninsula and South_Bay.

### 3.2 Company Type (`company_type`)

| Region | startup_product | established_tech_corporation | venture_capital_investor |
|---|---|---|---|
| Mid_Peninsula | **61.6%** | 21.9% | **15.1%** |
| South_Bay | 30.2% | **51.2%** | 0.0% |
| MV_Sunnyvale | **60.0%** | 30.0% | 0.0% |
| Palo_Alto_Area | 38.2% | 35.3% | 8.8% |
| North_Peninsula | 42.9% | 14.3% | **28.6%** |

**Key signal:** Descriptions signalling a VC/investor identity (`venture_capital_investor`) strongly predict Mid_Peninsula or North_Peninsula. Descriptions signalling an `established_tech_corporation` predict South_Bay (51.2% vs. ~22–35% in other clusters). Mid_Peninsula and MV_Sunnyvale are both startup-dense (≥60%).

### 3.3 Company Maturity (`company_maturity`)

| Region | growth_stage | established_public_or_large | early_stage |
|---|---|---|---|
| Mid_Peninsula | **56.2%** | 31.5% | 9.6% |
| MV_Sunnyvale | 47.5% | 35.0% | 10.0% |
| Palo_Alto_Area | **52.9%** | 38.2% | 5.9% |
| South_Bay | 23.3% | **48.8%** | 18.6% |
| North_Peninsula | 14.3% | 42.9% | **42.9%** |

**Key signal:** Growth-stage language (scaling, Series funding, expanding teams) predicts Mid_Peninsula/Palo_Alto_Area (53–56%). Established/large-company language predicts South_Bay (48.8%). Early-stage language over-indexes in North_Peninsula (42.9% vs. 6–19% elsewhere).

### 3.4 Core Tech Domain (`core_tech_domain`) and Hardware/Software Signal (`hardware_software_signal`)

| Region | semiconductor_chip_design | autonomous_vehicles_robotics | networking_communications | artificial_intelligence_ml | hw_sw_hybrid (%) |
|---|---|---|---|---|---|
| South_Bay | **18.6%** | 0.0% | 16.3% | 2.3% | **23.3%** |
| MV_Sunnyvale | 2.5% | **10.0%** | 15.0% | **17.5%** | **27.5%** |
| Mid_Peninsula | 0.0% | 0.0% | 13.7% | 8.2% | 6.8% |
| Palo_Alto_Area | 0.0% | 5.9% | 11.8% | 2.9% | 17.6% |

**Key signal:** Chip/semiconductor language in `core_tech_domain` and `hardware_software_signal` = `hardware_software_hybrid` or `pure_hardware` predicts South_Bay (18.6% semiconductor, 11.6% pure hardware). Autonomous vehicles/robotics language predicts MV_Sunnyvale (10% vs. 0% Mid_Peninsula). Pure-software descriptions predict Mid_Peninsula (72.6% pure_software vs. 48.8% South_Bay).

### 3.5 Delivery Model (`delivery_model`)

| Region | saas_platform | hardware_device | investment_funding | professional_services |
|---|---|---|---|---|
| Mid_Peninsula | **74.0%** | 2.7% | **13.7%** | 4.1% |
| MV_Sunnyvale | 70.0% | **17.5%** | 0.0% | 10.0% |
| South_Bay | 41.9% | **27.9%** | 0.0% | 23.3% |
| Palo_Alto_Area | 50.0% | 17.6% | 8.8% | **20.6%** |
| North_Peninsula | 57.1% | 0.0% | **28.6%** | 14.3% |

**Key signal:** Investment/funding language predicts Mid_Peninsula (13.7%) and North_Peninsula (28.6%). Hardware-device descriptions predict South_Bay (27.9%) and MV_Sunnyvale (17.5%). High SaaS framing predicts Mid_Peninsula (74%).

---

## 4. Weak or Redundant Features

- **`cloud_infra_signal`**: Mid_Peninsula has the highest cloud-native rate (57.5%) but differences across clusters are moderate (28–58%); this adds marginal signal beyond `delivery_model`.
- **`market_segment`**: enterprise_b2b dominates all regions (70–80%); offers little discriminating power beyond confirming non-consumer orientation.
- **`customer_type`**: Majority-technology-companies across all clusters (42–70%); limited differentiation.

---

## 5. Composite Feature Importance Summary

| Feature (from description) | Extraction Signal | Strongest Region Prediction |
|---|---|---|
| `industry_sector` | Semiconductor, VC, enterprise-software keywords | South_Bay (semi), Mid/North (VC) |
| `company_type` | VC/investor language vs. product/corp language | North+Mid_Peninsula (VC); South_Bay (corp) |
| `company_maturity` | Scaling/funding language vs. Fortune-500 language | Mid_Peninsula/Palo_Alto (growth); South_Bay (established) |
| `core_tech_domain` | Chip design, AV/robotics, AI/ML keywords | South_Bay (chip); MV_Sunnyvale (AV, AI) |
| `hardware_software_signal` | Physical product vs. pure SaaS language | South_Bay (hw hybrid/pure); Mid_Peninsula (pure software) |
| `delivery_model` | SaaS, hardware-device, investment descriptions | Mid_Peninsula (SaaS+investment); South_Bay (hardware) |
| `Latitude`/`Longitude` (structured) | Direct — strongest single predictor | All regions separable by coordinates |

---

## 6. Key Conclusions

1. **Geographic coordinates** (`Latitude`, `Longitude`) directly encode region and are the strongest single predictor (longitude spread ~0.46°). All text-derived features are proxies for this.

2. **Semiconductor / hardware product language** in a business description is the single most discriminating text signal, predicting **South_Bay** with high precision (8/11 semi companies, 18.6% of that cluster).

3. **VC/investor framing** ("we partner with founders", "capital", "portfolio") strongly predicts **Mid_Peninsula** (Sand Hill Road corridor) and **North_Peninsula**.

4. **Growth-stage startup language** (Series A/B, scaling, expanding) predicts Mid_Peninsula and MV_Sunnyvale; large-corporation language predicts South_Bay.

5. **AI/ML and autonomous-vehicle language** in `core_tech_domain` predicts MV_Sunnyvale over South_Bay (17.5% vs. 2.3% AI; 10% vs. 0% AV).

6. A combined feature set of `industry_sector` + `company_type` + `company_maturity` + `hardware_software_signal` extracted from description text provides the best text-only predictors of regional cluster, especially for distinguishing South_Bay from the Mid-Peninsula corridor.
