---
dataset: company_profile_location
scenario: predictive_region
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "regional_cluster"
query: "What features can be extracted from a company's business description to predict its regional cluster?"
source_table: augment_table/company_profile_location/predictive_region/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:10:27.753237+00:00
wall_seconds: 84.48
---

# Predicting Regional Cluster from Company Business Descriptions
**Dataset:** `sonnet__skill_on_v11_update.csv` | 199 companies | Silicon Valley geography

---

## 1. Overview

The dataset covers companies across the San Francisco Bay Area, spanning five loosely-defined regional clusters: **Mid Peninsula** (Palo Alto, Menlo Park, Redwood City – 74 firms), **South Peninsula** (Mountain View, Sunnyvale, Santa Clara – 58 firms), **South Bay** (San Jose, Los Gatos – 36 firms), **North Peninsula** (San Mateo – 22 firms), and **SF/North** (San Francisco – 7 firms). Six augmented categorical features are derived from the company description: `industry_vertical`, `company_type`, `cloud_infra_signal`, `target_market_segment`, `deployment_model`, and `business_model_type`.

---

## 2. Features Extractable from Business Descriptions

### 2.1 Industry Vertical
The strongest single discriminator. Descriptions that convey specific domain vocabulary map cleanly to verticals, which in turn correlate with region:

| Industry Vertical | Top Region | Notes |
|---|---|---|
| `venture_capital_finance` | Mid Peninsula | 13 of 15 VC firms in Palo Alto / Menlo Park |
| `semiconductor_hardware` | South Peninsula | 7 of 9 firms in Santa Clara / Mountain View / Cupertino |
| `enterprise_software` | Mid Peninsula & South Bay | Distributed; less discriminating alone |
| `data_analytics` | Mid + North Peninsula | Moderate concentration |
| `life_sciences_health` | South Peninsula | 6 of 12 firms |
| `edtech_learning` | South Peninsula | 5 of 9 firms |
| `cybersecurity` | South Peninsula | 7 of 15 firms |

**Signal keywords in descriptions:** phrases like *"semiconductor," "chip," "EDA," "hardware"* → South Peninsula/South Bay; *"venture capital," "portfolio companies," "fund"* → Mid Peninsula; *"health," "clinical," "genomics"* → South Peninsula.

### 2.2 Company Type
- **`venture_capital_firm`**: Near-exclusive Mid Peninsula predictor (11/15 in Menlo Park, 2/2 in Palo Alto). Descriptions using *"invest," "founders," "fund," "portfolio"* trigger this classification reliably.
- **`staffing_consulting`**: Overrepresented in South Bay (7/14 total); descriptions emphasizing *"training," "consulting," "placement," "staffing"* point away from Mid Peninsula.
- **`incubator_accelerator`**: Both instances in South Bay (San Jose); small sample, weak signal.
- **`growth_stage_tech`**: Concentrates in Mid Peninsula (27/53) and North Peninsula (10/53), suggesting mid-stage SaaS language correlates with those corridors.
- **`large_enterprise_public`**: Broadly distributed; limited regional discriminating power alone.

### 2.3 Deployment Model
- **`hardware_device`** (n=25): Strongly associated with South Peninsula (Santa Clara, Cupertino, Sunnyvale). Descriptions referencing *"device," "chip," "silicon," "hardware"* are key.
- **`saas_cloud_delivered`** (n=125): Dominant everywhere; not regionally discriminating by itself, but combined with other features it narrows location.
- **`professional_services`** (n=19): South Bay over-indexed (services/consulting language).

### 2.4 Business Model Type
- **`investor_capital_allocator`** (n=13): 11 in Mid Peninsula — strong predictor.
- **`research_development`** (n=12): Concentrates in South Peninsula (7/12), consistent with semiconductor and life sciences presence.
- **`services_consulting`** (n=22): Elevated in South Bay (11/22). Descriptions with *"training," "outsourcing," "managed services"* are indicators.
- **`platform_ecosystem`**: Distributed; moderate concentration in Mid Peninsula (13/32).

### 2.5 Target Market Segment
- **`consumer_b2c`** (n=37): Spread across all regions; limited discriminating power alone.
- **`enterprise_b2b`** (n=142): Dominant everywhere.
- **`developer_community`** (n=5): All in Mid Peninsula or South Peninsula; *"API," "SDK," "open source"* vocabulary.

### 2.6 Cloud Infrastructure Signal
- **`cloud_native_platform`** (n=35): Slight concentration in Mid Peninsula and North Peninsula; descriptions with *"cloud," "infrastructure," "platform-as-a-service"*.
- **`not_present`** (n=153): Majority; not regionally informative.

---

## 3. Combined Feature Patterns for Regional Prediction

| Predicted Region | Key Feature Combination |
|---|---|
| **Mid Peninsula** | `venture_capital_finance` + `investor_capital_allocator` **OR** `growth_stage_tech` + `platform_ecosystem` |
| **South Peninsula** | `semiconductor_hardware` + `hardware_device` + `research_development` **OR** `cybersecurity`/`edtech` + `startup_early_stage` |
| **South Bay** | `staffing_consulting` + `services_consulting` **OR** `large_enterprise_public` + `enterprise_software` (legacy tech) |
| **North Peninsula** | `enterprise_software` + `growth_stage_tech` + `data_analytics` (weak signal; overlaps Mid Peninsula) |

---

## 4. Exceptions and Weak Evidence

- **`enterprise_software`** is the largest vertical (68 firms) but is uniformly distributed across all regions, making it a poor standalone predictor.
- **North Peninsula** (San Mateo) is statistically under-differentiated — its feature profile (software, growth-stage, B2B) closely mirrors Mid Peninsula. Description-only features are unlikely to reliably separate these two.
- **SF/North** has only 7 companies, making any pattern there statistically fragile.
- **Consumer internet** firms are scattered broadly (Redwood City, Palo Alto, San Jose, San Mateo), reducing its predictive value for sub-regional clusters.
- `cloud_infra_signal = not_present` for 77% of companies; this feature adds marginal lift only when positive.

---

## 5. Decision-Ready Summary

The most predictive features extractable from business descriptions are, in rough order of regional discriminating power:

1. **Funding/investment language** → `venture_capital_finance` / `investor_capital_allocator` → **Mid Peninsula**
2. **Hardware/semiconductor vocabulary** → `semiconductor_hardware` + `hardware_device` + `research_development` → **South Peninsula**
3. **Staffing/consulting language** → `staffing_consulting` + `services_consulting` → **South Bay**
4. **Growth-stage SaaS + data/analytics framing** → moderate signal for **Mid & North Peninsula**
5. **Cloud-native infrastructure terms** → weak supplemental signal for Mid Peninsula

A classifier combining `industry_vertical`, `company_type`, and `business_model_type` from description NLP would likely achieve reasonable macro-accuracy on the three largest clusters (Mid Peninsula, South Peninsula, South Bay) while struggling to separate North Peninsula from Mid Peninsula due to feature overlap.
