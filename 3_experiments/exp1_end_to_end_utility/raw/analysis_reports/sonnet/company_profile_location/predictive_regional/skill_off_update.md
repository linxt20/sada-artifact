---
dataset: company_profile_location
scenario: predictive_regional
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "regional_cluster"
query: "What company traits explain regional clustering?"
source_table: augment_table/company_profile_location/predictive_regional/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:04:29.196052+00:00
wall_seconds: 43.26
---

# Regional Clustering Analysis — Company Profile Location Dataset
**Variant:** `skill_off` | **Dataset:** 199 companies across 7 Bay Area geo-clusters

---

## 1. Cluster Overview

| Geo-Cluster | N | Dominant Industry | Notable Company Types |
|---|---|---|---|
| South Bay (Sunnyvale/Santa Clara/Mountain View) | 72 | Cloud/Enterprise Software | Investors (8), Public Co. (4) |
| Peninsula (Redwood City/San Mateo) | 48 | Cloud/Enterprise Software | Mobile (8), Cybersecurity (5) |
| Other Bay Area | 32 | Cloud/Enterprise Software | Private Co. (27) |
| San Jose | 27 | Cloud/Enterprise Software | Semiconductor/HW (4) |
| South Santa Clara County (Los Gatos/Campbell) | 10 | Cybersecurity | Mixed small-co. |
| San Francisco | 7 | Other Technology | Evenly spread |
| East Bay (Fremont/Newark) | 3 | Other Technology / Cloud | Too small for inference |

---

## 2. Traits That Explain Regional Clustering

### Industry Sector
**Cloud/Enterprise Software** is the dominant sector across nearly all clusters, but its concentration differs:
- **South Bay** houses the broadest industry mix, including a notable **Venture Capital/Finance** cohort (10 firms), and is the only cluster with a meaningful **Investor** company-type presence (8). This aligns with Sand Hill Road–anchored VC culture.
- **Peninsula** skews toward **Mobile** (8) and **Cybersecurity** (5), alongside Cloud, suggesting a mid-corridor tech-services profile.
- **San Jose** is distinctive for **Semiconductor/Hardware** (4), reflecting its legacy chip-industry geography.
- **South Santa Clara County** shows unusual **Cybersecurity** dominance for its small size (2 of 10), plus a disproportionate share of **EdTech** and **Mobile** — possibly a suburban small-firm effect.

### Company Type
Private Company dominates every cluster (≥85% in most), so **company_type alone is not a strong regional differentiator**. The key exception is **South Bay**, which concentrates nearly all **Investor** firms (8 of 10 total), reinforcing its role as the region's VC hub.

### Tech Focus Level
- High tech-focus firms are most concentrated in **South Bay** (11) and **Peninsula** (8), consistent with those clusters hosting the most technology-intensive firms.
- Low tech-focus firms are spread broadly, with no cluster being entirely "low-tech." **San Francisco** leans low-to-medium, fitting its mix of Other Technology and service-oriented firms.
- **East Bay** has zero High-focus firms (n=3, interpret cautiously).

### Description Length
- Medium-length descriptions dominate everywhere, offering limited discriminatory power.
- **South Bay** has the most Long-description companies (4) alongside the most Short (13), suggesting a wider variety of firm communication styles — consistent with its heterogeneous mix of startups, VC firms, and large incumbents.

---

## 3. Key Patterns and Interpretation

| Signal | Strength | Notes |
|---|---|---|
| VC/Investor concentration → South Bay | **Strong** | 8 of 10 Investors cluster in South Bay |
| Semiconductor/HW → San Jose | **Moderate** | 4 firms vs. 0–2 elsewhere |
| Mobile tech → Peninsula | **Moderate** | 8 firms concentrated here |
| Cybersecurity → Peninsula + South Bay | **Moderate** | 5 and 6 respectively |
| Cloud/Enterprise Software ubiquity | **Weak differentiator** | Dominant everywhere; does not distinguish clusters |
| Company type (Private Co.) | **Non-differentiating** | Nearly universal across all clusters |

---

## 4. Exceptions and Weak Evidence

- **San Francisco** (n=7) and **East Bay** (n=3) are too small for reliable pattern inference.
- **tech_focus_level** and **description_length** show no sharp cluster-specific signatures beyond South Bay's slight High-focus lead.
- The **"Other Bay Area"** cluster is geographically diffuse by definition, making its patterns less actionable.

---

## 5. Decision-Ready Summary

Regional clustering in this dataset is most strongly explained by **investor/VC presence** (South Bay), **legacy hardware industry affinity** (San Jose), and **mobile/cybersecurity specialization** (Peninsula). Industry sector — specifically the sub-sector beyond the Cloud/Enterprise Software baseline — is the most predictive company trait. Company type and tech focus level provide secondary signals, with investor type being the most regionally concentrated. Description length adds minimal discriminatory value.
