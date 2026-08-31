---
dataset: company_profile_location
scenario: causal_regional_clustering
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: causal_attribution
focus_variable: "regional_cluster"
query: "Explain what leads a company to be based in one region rather than another."
source_table: augment_table/company_profile_location/causal_regional_clustering/original.csv
generated_at: 2026-07-26T13:00:54.701177+00:00
wall_seconds: 121.6
---

# Causal Regional Clustering: What Leads a Company to Be Based in One Region Rather Than Another?

## Dataset Overview

The dataset contains **199 companies** with addresses, coordinates, and descriptions, all located within a narrow geographic band in the **San Francisco Bay Area / Silicon Valley** (latitude 37.20–37.79, longitude −122.43 to −121.75). All cities fall within a ~50-mile corridor. The analysis therefore focuses on *intra-regional* placement — why companies cluster in specific sub-zones rather than others.

---

## Key Sub-Regions and Their Concentrations

| Sub-Region | Cities | # Companies | Share |
|---|---|---|---|
| South Bay | San Jose, Santa Clara, Cupertino, Fremont | ~55 | 28% |
| Mid-Peninsula | Redwood City, San Mateo, Menlo Park, Palo Alto | ~93 | 47% |
| Central Corridor | Mountain View, Sunnyvale, Los Gatos | ~46 | 23% |
| San Francisco | San Francisco | 5 | 2% |

The Mid-Peninsula dominates numerically, with **Redwood City** (36 companies) being the single most-populated city, followed by Mountain View (25), Palo Alto (23), San Jose (22), and San Mateo (20).

---

## Factor 1: Industry Identity and Sector Clustering

### Venture Capital → Menlo Park / Sand Hill Road
The strongest sector-specific clustering in the dataset is VC firms on **Sand Hill Road, Menlo Park**:
- Andreessen Horowitz, Sequoia Capital, Khosla Ventures, Lightspeed Venture Partners, Greylock Partners, Menlo Ventures, Accel, 5AM Ventures, Shasta Ventures, Storm Ventures, TriplePoint Capital — **all on Sand Hill Road**.

**Causal mechanism:** VC firms co-locate to access deal flow, co-investors, and portfolio monitoring in person. Sand Hill Road functions as a self-reinforcing prestige address — being there signals legitimacy to founders and LPs, which attracts more firms, which reinforces the effect.

### Semiconductor & EDA → Santa Clara / San Jose
Hardware-intensive companies cluster in the South Bay:
- AMD, Intel, NVIDIA, Marvell → **Santa Clara**
- Broadcom, Cisco, Cadence Design Systems → **San Jose**
- Synopsys → **Mountain View**

**Causal mechanism:** Legacy industrial infrastructure, proximity to Stanford and UC research pipelines, and deep pools of chip-engineering talent created self-reinforcing agglomeration. Manufacturing zoning in Santa Clara and San Jose also accommodates larger campuses and fabrication support.

### Major Consumer Tech Brands — Follows Founding History
| Company | City | Notable |
|---|---|---|
| Apple | Cupertino | Founded in garage nearby |
| Google | (not in dataset, but neighbors present) | — |
| Facebook | Menlo Park | Relocated from Palo Alto garage |
| Netflix | Los Gatos | Founded there |
| Oracle | Redwood City | Long-tenured HQ |
| Adobe | San Francisco | Anomaly — SF proper |

**Causal mechanism:** Founding location and early office leases tend to persist; once a campus is built, relocation costs and employee retention risks discourage moves.

---

## Factor 2: Address Corridors as Institutional Attractors

Several streets show concentrated clusters:
- **Sand Hill Road, Menlo Park** — 12 companies (exclusively investment/VC)
- **Seaport Blvd, Redwood City** — Branch, C3.ai, Course Hero, Delphix, HeartFlow, Informatica, Sizmek (SaaS/data analytics cluster)
- **Great America Pkwy, Santa Clara** — Arista, Brillio, GlobalFoundries, Tata Consultancy Services (enterprise tech and IT services)

These corridors act as micro-ecosystems: landlords package amenities, campus-style offices, and subleasing options that attract similar-stage or similar-type firms.

---

## Factor 3: Company Stage and Real Estate Availability

- **Redwood City** has the highest raw count (36) despite not being a historical prestige address. This likely reflects newer office developments (Seaport Blvd waterfront), competitive rents vs. Palo Alto, and good highway access (US-101).
- **San Mateo** (20 companies) similarly offers mid-priced office space between San Francisco and Silicon Valley's core — attractive to mid-size SaaS companies (Apttus, Armory, Benevity, AlienVault).
- **Palo Alto** (23 companies) skews toward startups and investors seeking proximity to Stanford University and prestige.

---

## Factor 4: Talent Access and University Proximity

- **Stanford University** (Palo Alto) creates a gravitational pull for startups: many companies in Palo Alto and Menlo Park cite Stanford affiliations or AI/ML research lineages in descriptions (e.g., Ambient.ai: "team of Stanford graduates").
- The **University Ave corridor** (Palo Alto → East Palo Alto) contains Amazon's Bay Area office alongside several startups.
- **Sunnyvale and Mountain View** attract companies with strong engineering needs (Baidu USA R&D, BlueJeans, Coursera) — close to Google and NASA Ames talent pools.

---

## Factor 5: Sector-Specific Regulatory and Infrastructure Needs

- **Life sciences** companies (23andMe in Mountain View; Codexis in Redwood City; HeartFlow in Redwood City) tend to locate near life science parks with lab zoning rather than pure office districts.
- **Cybersecurity** companies (AlienVault → San Mateo, Anomali → Redwood City, Avast → Redwood City, Barracuda → Campbell) are spread across the corridor with no single dominant cluster, suggesting their location driver is talent availability and cost rather than peer proximity.

---

## Exceptions and Weak Evidence

- **San Francisco** is nearly absent from this dataset (only 5 companies: Adobe, GoodRx, Redpoint Ventures, Spark Capital, TuneIn). This is a dataset artifact — SF has a large tech ecosystem not captured here, so absence should not be interpreted causally.
- **Staffing and IT services firms** (Adecco, Mindsource, Palo Alto Staffing) locate near their clients rather than forming their own cluster; their city names sometimes reflect brand rather than physical cluster logic.
- The "Other Tech" residual category dominates every city, limiting sector-specific causal inference. With description-based classification, many SaaS and platform companies resist clean categorization.
- The dataset contains no founding year, company size, or rent data, so cost and stage-of-growth hypotheses cannot be tested directly from the columns provided.

---

## Summary: What Causes Regional Placement

| Driver | Evidence Strength | Primary Beneficiary Cities |
|---|---|---|
| **Sector identity / peer clustering** | Strong (VC on Sand Hill; semis in SJ/SC) | Menlo Park, Santa Clara, San Jose |
| **Founding history / campus inertia** | Strong (Apple, Netflix, Oracle) | Cupertino, Los Gatos, Redwood City |
| **Office corridor attractiveness** | Moderate (Seaport, Great America) | Redwood City, Santa Clara |
| **University proximity / talent** | Moderate (Stanford → Palo Alto/MP) | Palo Alto, Menlo Park, Mountain View |
| **Real estate cost/availability** | Plausible but not directly measurable | Redwood City, San Mateo |
| **Regulatory/zoning fit** | Weak (only a few life science hints) | Redwood City, Mountain View |

The dominant pattern is **industry-specific agglomeration**: companies place themselves where their sector's ecosystem — investors, talent, peers, and institutional knowledge — is already concentrated. The Sand Hill Road / Menlo Park VC cluster is the clearest single causal example. For hardware companies, it is the South Bay corridor around Santa Clara. For SaaS startups, the Mid-Peninsula offers balanced access to capital, talent, and office space at competitive (relative to SF) costs.
