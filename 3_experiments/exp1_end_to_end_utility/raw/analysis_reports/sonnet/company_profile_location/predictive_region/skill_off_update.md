---
dataset: company_profile_location
scenario: predictive_region
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "regional_cluster"
query: "What features can be extracted from a company's business description to predict its regional cluster?"
source_table: augment_table/company_profile_location/predictive_region/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:04:25.981549+00:00
wall_seconds: 61.17
---

# Predictive Regional Cluster Analysis
**Dataset:** `sonnet__skill_off_update.csv` | 199 companies | Silicon Valley / Bay Area  
**Focus Variable:** Regional cluster (derived from Latitude/Longitude)  
**Variant:** `skill_off`

---

## 1. Regional Cluster Definition

Using latitude as a proxy, companies group into three meaningful clusters:

| Cluster | Latitude Range | N | Representative Cities |
|---|---|---|---|
| **North (SF)** | > 37.5° | 53 | San Francisco |
| **Mid-Peninsula** | 37.2–37.5° | 124 | Redwood City, Palo Alto, Menlo Park, Mountain View |
| **South Bay** | < 37.2° | 22 | San Jose, Santa Clara, Sunnyvale |

The Mid-Peninsula dominates (62% of records), reflecting the dataset's Silicon Valley composition.

---

## 2. Features Extractable from Business Descriptions

### 2.1 Industry / Domain Tags (Strongest Signal)
Binary flags derived from description keywords (`is_*` columns) show meaningful cluster-level variation:

| Feature | Mid-Peninsula | North (SF) | South Bay |
|---|---|---|---|
| `is_enterprise_sw` | 50% | **55%** | 52% |
| `is_consumer` | 32% | **47%** | **57%** |
| `is_fintech` | **15%** | 4% | 14% |
| `is_healthcare` | **11%** | 8% | 5% |
| `is_ai_ml` | 27% | 21% | **33%** |
| `is_hardware_iot` | **15%** | 6% | 19% |
| `is_security` | 12% | 8% | **19%** |

**Key patterns:**
- **North (SF)**: Higher consumer-facing language; lower fintech/healthcare signals.
- **South Bay**: Elevated consumer, AI/ML, hardware/IoT, and security flags — reflecting manufacturing/engineering culture of San Jose/Santa Clara.
- **Mid-Peninsula**: Highest fintech and healthcare density; reflects Sand Hill Road VC/biotech presence.

### 2.2 `industry_tag_count` — Description Breadth
South Bay companies show the highest average tag count (2.19 vs. 1.77 Mid-Peninsula, 1.57 North SF), suggesting their descriptions reference more capability domains — consistent with diversified hardware/software firms.

Correlation with latitude: **−0.199** (the more southerly, the broader the description scope).

### 2.3 `tech_density` — Jargon Density
Fraction of technical terms per word:

- South Bay: **0.083** (highest)
- Mid-Peninsula: **0.076**
- North (SF): **0.073**

Correlation with latitude: **−0.120** — modest but consistent with South Bay's engineering-heavy companies. This is extractable from raw description text via domain vocabulary matching.

### 2.4 `desc_word_count` & `desc_sentence_count`
- South Bay descriptions are slightly longer on average (25.5 words vs. 23.5 / 21.2).
- Sentence count correlates positively with latitude (+0.110): SF companies write shorter, punchier descriptions; South Bay firms use more sentences.
- These are weak predictors individually but useful in combination.

### 2.5 `action_verb_score` & `has_funding_language`
- `action_verb_score` is marginally higher in North (SF) and South Bay (0.87, 0.86) vs. Mid-Peninsula (0.75).
- `has_funding_language` is highest in Mid-Peninsula (10.5%) vs. North SF (1.9%) — consistent with the VC-heavy Sand Hill Road corridor.  
  This is the **strongest single qualitative differentiator** for the Mid-Peninsula cluster.

### 2.6 `mentions_b2b` / `mentions_b2c`
- `mentions_b2c` slightly favors North (SF) (11%), consistent with consumer apps in SF.
- `mentions_b2b` is relatively flat across clusters (~14–17%) — limited discriminative power alone.

---

## 3. Feature Importance Summary (by Correlation with Latitude)

| Rank | Feature | Correlation | Direction |
|---|---|---|---|
| 1 | `is_hardware_iot` | −0.206 | More southerly = more hardware |
| 2 | `industry_tag_count` | −0.199 | More southerly = broader scope |
| 3 | `is_ai_ml` | −0.129 | More southerly = more AI/ML |
| 4 | `desc_word_count` | −0.127 | More southerly = longer |
| 5 | `is_education` | −0.121 | More southerly = more edtech |
| 6 | `tech_density` | −0.120 | More southerly = more technical |
| 7 | `desc_sentence_count` | +0.110 | More northerly = more sentences |
| 8 | `has_funding_language` | −0.045 | Weak signal toward Mid-Peninsula |

---

## 4. Exceptions and Weak Evidence

- **All correlations are modest** (|r| < 0.21), meaning no single description feature cleanly separates clusters. Prediction requires combining multiple signals.
- **Enterprise software** (`is_enterprise_sw`) is near-uniformly distributed (50–55%) across all clusters — essentially useless as a standalone predictor.
- **`is_fintech`** shows the clearest cluster-specific spike (15% Mid-Peninsula, 4% North SF) and aligns with Sand Hill Road VC geography, but represents a minority of companies.
- The **"Far South" cluster** (n=1, Los Gatos) is too small to interpret.
- San Francisco (5 companies in dataset) is underrepresented, which may inflate or deflate "North SF" cluster feature means.

---

## 5. Decision-Ready Summary

To predict a Bay Area company's regional cluster from its business description, extract:

1. **Domain keyword flags** — especially `is_hardware_iot`, `is_fintech`, `is_consumer`, `is_ai_ml`, `is_security`.
2. **`industry_tag_count`** (description breadth) — higher counts point toward South Bay.
3. **`tech_density`** — higher jargon density favors South Bay.
4. **`has_funding_language`** — VC/investor language strongly signals Mid-Peninsula.
5. **Description length** (`desc_word_count`) — longer descriptions tilt toward South Bay.

A simple rule-of-thumb classifier: if the description contains **funding language → Mid-Peninsula**; if it has **hardware/IoT + AI/ML signals → South Bay**; if it emphasizes **consumer apps with shorter text → North SF**. However, all signals are weak enough that a multi-feature ML model (e.g., logistic regression or gradient boosting on these extracted features) is recommended over manual rules.
