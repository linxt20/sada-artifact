---
dataset: flag_12
scenario: eda_efficiency
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "resolution_efficiency"
query: "How does incident resolution efficiency vary across category, priority, and assignment group?"
source_table: augment_table/flag_12/eda_efficiency/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:14:04.190604+00:00
wall_seconds: 71.54
---

# Incident Resolution Efficiency Analysis
## Query: How does incident resolution efficiency vary across category, priority, and assignment group?

---

### Method Note

The analysis uses all 500 incidents in the augmented table. Resolution time (hours) was computed as `closed_at − opened_at`. TAPP-generated columns examined: `incident_category`, `failure_symptom_type`, `self_resolved_by_assignee`, `software_trigger_present`, and `requires_replacement`. The column `affected_asset_type` was correlated with `incident_category` and did not add independent signal; it is noted but not centered. All 500 records had valid, positive resolution durations.

---

### 1. Overall Resolution Efficiency

| Metric | Value |
|--------|-------|
| Total incidents | 500 |
| Median resolution time | **173.2 hours (~7.2 days)** |
| Mean resolution time | 178.4 hours |
| 25th percentile | 87.3 hours |
| 75th percentile | 252.7 hours |

The distribution is moderately right-skewed (std ≈ 109 h), indicating a long tail of slow-resolving cases.

---

### 2. Resolution Efficiency by Category

| Category | Count | Median (h) | Mean (h) |
|----------|------:|----------:|--------:|
| Software | 33 | **148.0** | 153.6 |
| Hardware | 406 | 175.4 | 181.4 |
| Database | 19 | 177.6 | 172.4 |
| Inquiry / Help | 20 | 182.7 | 182.1 |
| Network | 22 | 186.4 | 161.6 |

**Software incidents resolve ~18% faster** than the overall median (148 h vs. 173 h). Hardware dominates volume (81% of all tickets) and resolves near the mean. Network has the highest median (186 h) but a lower mean (162 h), suggesting occasional fast resolutions alongside many slow ones.

**TAPP `incident_category` refinement:** Within the dominant Hardware category, sub-types vary substantially:

| incident_category | Count | Median (h) |
|-------------------|------:|----------:|
| network_connectivity | 28 | 144.4 |
| monitor_display | 71 | 145.6 |
| software_application | 52 | 155.4 |
| server_hardware | 41 | 173.5 |
| input_device | 70 | 175.4 |
| printer_hardware | 203 | 181.6 |
| storage_hardware | 14 | **205.5** |

Printer hardware (n=203, the single largest sub-type) resolves slower than average, while network connectivity and display issues are resolved roughly 25% faster than printer/storage types.

---

### 3. Resolution Efficiency by Priority

| Priority | Count | Median (h) | Mean (h) |
|----------|------:|----------:|--------:|
| 4 - Low | 2 | 32.6 | 32.6 |
| 3 - Moderate | 77 | 164.2 | 177.8 |
| 1 - Critical | 27 | 164.7 | 167.0 |
| 2 - High | 394 | **176.6** | 180.0 |

Priority ordering does **not** follow the expected escalation pattern for the bulk of incidents. 2 - High (79% of volume) actually has the *highest* median resolution time (177 h), while 1 - Critical resolves marginally faster (165 h median). The two 4 - Low incidents are too few for inference.

**Priority × Category cross-tab (median hours):**

| Priority | Database | Hardware | Network | Software |
|----------|--------:|--------:|--------:|--------:|
| 1 - Critical | 393.6 (n=2) | 164.7 | 161.1 | 24.0 (n=1) |
| 2 - High | 150.9 | 181.8 | 211.6 | 152.0 |
| 3 - Moderate | 189.0 | 156.4 | 136.8 | 92.4 |

Notable outliers: Critical Database incidents have a 394 h median (only 2 cases); Critical Software resolves in 24 h but is a single observation. High-priority Network incidents (212 h) are the slowest cross-segment combination.

---

### 4. Resolution Efficiency by Assignment Group

| Assignment Group | Count | Median (h) | Mean (h) | Self-Resolved Rate |
|-----------------|------:|----------:|--------:|------------------:|
| Software | 33 | **148.0** | 153.6 | 24.2% |
| Network | 23 | 161.1 | 161.6 | 30.4% |
| Hardware | 405 | 175.6 | 181.5 | 20.5% |
| Database | 20 | 178.9 | 178.3 | 30.0% |
| Service Desk | 19 | 179.5 | 176.4 | 10.5% |

The **Software group is the most efficient** (median 148 h), 18% faster than the overall median. The **Hardware group** handles 81% of volume and sets the organizational pace (176 h). **Service Desk** has the lowest self-resolution rate (10.5%) and is among the slowest, consistent with its role as a routing/escalation group.

The TAPP column `self_resolved_by_assignee` shows that self-resolved incidents (n=106) resolve in 171 h vs. 174 h for escalated ones — the difference is minimal (< 2%), indicating that the self-resolution pathway does not materially accelerate resolution time in this dataset.

---

### 5. TAPP Semantic Facets as Additional Explanatory Variables

**`software_trigger_present` (n=54 True):**  
Incidents with a software trigger resolve in 157 h median vs. 175 h for those without — a ~10% efficiency advantage. This effect is concentrated in 2 - High priority incidents (154 h vs. 182 h). The facet adds modest signal beyond the raw category.

**`failure_symptom_type`:** Provides useful within-category signal:

| Symptom | Count | Median (h) |
|---------|------:|----------:|
| overheating | 6 | 128.1 |
| crash_or_freeze | 6 | 82.2 |
| update_failure | 24 | 150.0 |
| display_anomaly | 51 | 145.6 |
| connectivity_failure | 46 | 175.1 |
| malfunction_general | 310 | 175.0 |
| not_responding | 39 | **205.7** |
| power_failure | 9 | 227.2 |

"Not responding" and "power failure" symptoms are the slowest (206–227 h); "crash or freeze" is fastest (82 h, small sample). Power failure and overheating are infrequent but diagnostically important.

**`requires_replacement` (n=14 True):**  
Only 14 incidents require hardware replacement; median resolution is 158 h vs. 175 h for non-replacement cases. The small sample limits inference; this facet is not a primary driver.

---

### 6. Key Findings and Decision-Ready Takeaways

| Finding | Evidence |
|---------|----------|
| **Priority does not drive faster resolution** | Critical (165 h) and High (177 h) resolve at similar speeds; no strong SLA differentiation is visible |
| **Software & Network assignment groups are most efficient** | 148 h and 161 h median vs. 176 h for Hardware |
| **Printer hardware is the largest bottleneck** | 203 incidents (41% of total) at 182 h median — above average |
| **Storage hardware is the slowest sub-category** | 206 h median, though low volume (n=14) |
| **High-priority Network incidents are the worst combination** | 212 h median — warrants SLA attention |
| **Software triggers slightly accelerate resolution** | ~10% faster, especially at High priority |
| **"Not responding" and "power failure" symptoms signal slow cases** | 206–227 h median; early flag for extended timelines |

---

### Caveats

- All incidents are Closed or Resolved (no open backlog), so the sample reflects completed work only.
- Priority 4 - Low (n=2) is statistically negligible.
- Several TAPP facets (`self_resolved_by_assignee`, `requires_replacement`) show weak effects and should not be prioritized in process interventions.
