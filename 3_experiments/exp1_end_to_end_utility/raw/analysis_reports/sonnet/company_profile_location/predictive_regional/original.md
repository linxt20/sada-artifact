---
dataset: company_profile_location
scenario: predictive_regional
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: exploratory_data_analysis
focus_variable: "regional_cluster"
query: "What company traits explain regional clustering?"
source_table: augment_table/company_profile_location/predictive_regional/original.csv
source_report: dataset_portion_2/substrate-claude-sonnet-4-6/company_profile_location__predictive_regional/analyses/original/analysis.md
wall_seconds: 90.21
---

# Regional Clustering of Silicon Valley Companies: What Company Traits Explain the Patterns?

## Dataset Overview

The dataset contains **≈202 companies** with the following columns: `Company Name`, `Website`, `Address 1`, `City`, `Latitude`, `Longitude`, and `Company Description`. All companies are located in the San Francisco Bay Area / Silicon Valley corridor. There is no explicit labelled "region" column; regional clusters must be inferred from the `City` and coordinate fields. The `Company Description` is the primary source of company traits (sector, business model, stage).

---

## 1. Observed Regional Sub-Clusters

Based on city labels and latitude/longitude values, five distinct sub-zones emerge:

| Sub-Region | Representative Cities | Approx. Lat Band |
|---|---|---|
| **North (SF)** | San Francisco, San Bruno | 37.63 – 37.79 |
| **Mid-Peninsula** | Burlingame, Belmont, San Mateo, Foster City | 37.54 – 37.60 |
| **Redwood City / San Carlos** | Redwood City, San Carlos | 37.48 – 37.54 |
| **South Bay – Core** | Palo Alto, Menlo Park, Mountain View, Sunnyvale, Santa Clara | 37.33 – 37.46 |
| **Far South** | San Jose, Campbell, Los Gatos, Cupertino, Newark, Fremont | 37.19 – 37.37 |

---

## 2. Company Traits That Predict Sub-Region

### 2.1 Venture Capital / Investment Firms → Menlo Park (Sand Hill Road)
The most striking cluster is **venture capital firms exclusively on Sand Hill Road, Menlo Park** (lat ≈ 37.42, lon ≈ −122.20):

- Andreessen Horowitz (2865 Sand Hill Rd)
- Sequoia Capital (3000 Sand Hill Rd)
- Accel (2500 Sand Hill Rd)
- Greylock Partners (2250 Sand Hill Rd)
- Khosla Ventures (2128 Sand Hill Rd)
- Lightspeed Venture Partners (2200 Sand Hill Rd)
- Shasta Ventures (2440 Sand Hill Rd)
- Menlo Ventures (2884 Sand Hill Rd)
- Katerra (2494 Sand Hill Rd)
- Storm Ventures (3000 Sand Hill Rd)
- TriplePoint Capital (2755 Sand Hill Rd)
- 5AM Ventures (2200 Sand Hill Rd)

**Trait signal:** Descriptions contain "venture capital," "invest," "partner with founders," "early-stage." This is the strongest single-address cluster in the dataset. **Investment stage (VC) is the most reliable predictor of Menlo Park placement.**

### 2.2 Semiconductors / Hardware → Santa Clara
Companies describing themselves as semiconductor, chip design, or hardware:

- AMD (Santa Clara) — "American multinational semiconductor company"
- Intel (Santa Clara) — "cloud computing, data center… chip"
- NVIDIA (Santa Clara) — "graphics processing units"
- Marvell (Santa Clara) — "global semiconductor company"
- Arista (Santa Clara) — networking hardware
- Globalfoundries (Santa Clara) — semiconductor foundry
- EMC Data Domain (Santa Clara) — data deduplication storage hardware

**Trait signal:** Descriptions referencing "semiconductor," "chip," "GPU," "hardware," "EDA," or "network infrastructure" strongly predict Santa Clara (lat ≈ 37.38–37.41, lon ≈ −121.96–121.98). Cadence Design Systems and Synopsys (EDA tools) appear in San Jose and Mountain View respectively, suggesting the hardware-design cluster is wider but centered on Santa Clara.

### 2.3 Enterprise SaaS / Cloud Data → Redwood City
A dense cluster of enterprise software companies appears in Redwood City (lat ≈ 37.48–37.54):

- Oracle (100 Oracle Pkwy)
- Box (900 Jefferson Ave)
- Informatica (2100 Seaport Blvd)
- C3.ai (1300 Seaport Blvd)
- Electronic Arts (209 Redwood Shores Pkwy)
- Equinix (1 Lagoon Dr)
- Carbon, Genomic Health, Imperva, Sumo Logic, Gainsight, Shutterfly, Delphix, etc.

**Trait signal:** Descriptions contain "enterprise cloud," "data management," "SaaS," "platform," "data warehouse." Redwood City appears to attract mid-to-late stage enterprise software companies, possibly influenced by Oracle's anchor presence and available large office campuses along Seaport Blvd/Bridge Pkwy.

### 2.4 Consumer Internet / Social / Media → San Francisco
The few SF-based companies are consumer-facing:

- Adobe (601 Townsend St, SF) — creative/digital experience platform
- GoodRx (577 2nd St, SF) — consumer healthcare savings
- TuneIn (210 King St, SF) — consumer audio streaming
- Spark Capital (332 Pine St, SF) — VC with consumer focus
- Redpoint Ventures (21 S Park St, SF) — consumer/enterprise investor

**Trait signal:** Consumer brand visibility, "stream," "listen," "shop," "help people" language in descriptions. The SF cluster is small in this dataset (≈5 companies), so inference is weak but directionally consistent with broader Bay Area patterns.

### 2.5 Staffing / Consulting / Services → San Mateo Corridor
Several staffing, consulting, and HR-tech companies cluster in San Mateo:

- Adecco Group (San Bruno) — global staffing
- Lohika (San Mateo) — engineering scale-out partner
- Jobvite (San Mateo) — recruiting software
- Mountain View Staffing / Palo Alto Staffing (Palo Alto)
- Intelliswift (Newark) — IT services

**Trait signal:** Descriptions with "staffing," "recruiting," "talent," "consulting," "resourcing." These companies tend to be spread broadly across the mid-peninsula rather than forming a tight sub-cluster.

### 2.6 Life Sciences / Biotech → Redwood City / Menlo Park Edge
Biotech and genomics companies appear near Redwood City:

- Genomic Health (301 Penobscot Dr, Redwood City)
- GenapSys (200 Cardinal Way, Redwood City)
- Codexis (400 Penobscot Dr, Redwood City)
- Proteus Digital Health (2600 Bridge Pkwy, Redwood City)
- DNAnexus (Mountain View)
- 23andMe (Mountain View)

**Trait signal:** Descriptions containing "genomic," "biocatalyst," "clinical," "pharmaceutical," "life science." This cluster is contiguous with but distinct from the pure enterprise-software Redwood City group.

### 2.7 Cybersecurity → Distributed, Slight San Mateo / Mountain View Lean
Cybersecurity companies appear across multiple cities with no tight single-city cluster:

- AlienVault / AT&T Cybersecurity (San Mateo)
- Anomali, Avast (Redwood City)
- Barracuda (Campbell)
- McAfee (Santa Clara)
- Proofpoint (Sunnyvale)
- Symantec (Mountain View)
- SentinelOne (Mountain View)
- Forcepoint (Los Gatos)

**Trait signal:** Descriptions with "cybersecurity," "threat intelligence," "endpoint protection," "malware." The sector is distributed; no single city dominates, which weakens regional-prediction value for this vertical.

---

## 3. Coordinate-Level Patterns

Using latitude as a north–south axis:

- **Higher latitudes (37.6–37.8)**: Corporate offices, staffing/services, consumer apps (SF, San Bruno)
- **Mid latitudes (37.48–37.56)**: Enterprise SaaS, data platforms, storage (Redwood City, San Carlos, San Mateo)
- **Core latitudes (37.38–37.46)**: VC firms, AI/ML startups, semiconductors, platform companies (Menlo Park, Palo Alto, Mountain View, Sunnyvale, Santa Clara)
- **Lower latitudes (37.19–37.37)**: Legacy enterprise, ERP, hardware OEMs, education tech (San Jose, Cupertino, Los Gatos, Fremont)

Longitude separates the **highway-101 / inland corridor** (lon ≈ −121.89 to −121.97, San Jose, Santa Clara) from the **El Camino / Caltrain corridor** (lon ≈ −122.05 to −122.25, Mountain View, Palo Alto, Menlo Park, Redwood City).

---

## 4. Summary of Predictive Traits

| Company Trait | Predicted Sub-Region | Evidence Strength |
|---|---|---|
| Venture capital firm | Menlo Park (Sand Hill Rd) | **Strong** — 12+ firms, same street |
| Semiconductor / chip design | Santa Clara | **Strong** — 6+ majors |
| Enterprise SaaS / cloud data | Redwood City | **Moderate** — dense but mixed with other sectors |
| Life sciences / genomics | Redwood City edge / Mountain View | **Moderate** — small N |
| Consumer internet / media | San Francisco | **Weak** — only ~5 companies |
| Cybersecurity | Distributed | **Weak** — no dominant city |
| Staffing / HR services | Mid-peninsula (San Mateo, San Bruno) | **Weak** — low density |
| Large legacy enterprise (IBM, Oracle, HP) | South corridor (San Jose, Palo Alto, Redwood City) | **Moderate** — consistent with HQ history |

---

## 5. Important Exceptions and Caveats

- **Amazon** appears in East Palo Alto (not Seattle), reflecting a satellite R&D office — not a true HQ signal.
- **Cybersecurity** companies are spread across 8+ cities; sector alone is insufficient to predict location for this vertical.
- The dataset contains **no company age, revenue, employee count, or funding stage columns**, so economic-size explanations are inferred from descriptions only and cannot be quantitatively confirmed.
- **Street address patterns** (e.g., "Sand Hill Road" = VC) are more discriminative than city alone for some clusters.
- Several companies share addresses (e.g., HeartFlow and Branch both at 1400 Seaport Blvd, Redwood City), suggesting shared office buildings rather than independent location choices — this may inflate the Redwood City cluster signal.
- **Los Gatos** hosts a heterogeneous mix: Netflix (consumer streaming), Cradlepoint (networking), Forcepoint (cybersecurity), Sterling Communications (PR), SVG Ventures (agri-VC) — no single-sector explanation.

---

## 6. Decision-Ready Summary

The strongest and most actionable finding is that **company type (VC vs. semiconductor vs. enterprise SaaS) is the primary predictor of sub-regional placement**, not city preference alone. To predict a company's Bay Area sub-region from its profile:

1. **VC/Investment language in description + "Sand Hill" in address → Menlo Park, high confidence.**
2. **Semiconductor/GPU/chip description → Santa Clara, high confidence.**
3. **Enterprise cloud/data platform description → Redwood City, moderate confidence.**
4. **Genomics/biotech description → Redwood City fringe or Mountain View, moderate confidence.**
5. **Consumer app/media → possibly SF, but weak evidence in this dataset.**
6. **Cybersecurity → no reliable regional prediction; additional signals needed.**
