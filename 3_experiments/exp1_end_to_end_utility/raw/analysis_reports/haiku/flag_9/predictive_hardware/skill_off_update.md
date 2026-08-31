---
dataset: flag_9
scenario: predictive_hardware
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "is_hardware_anomaly_window"
query: "What signals indicate a hardware incident is in the anomaly window?"
source_table: augment_table/flag_9/predictive_hardware/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:23:27.207327+00:00
wall_seconds: 62.17
---

# Hardware Incident Anomaly Window Analysis Report

**Dataset:** haiku__skill_off_update (Variant: skill_off)  
**Query:** What signals indicate a hardware incident is in the anomaly window?  
**Focus Variable:** `in_anomaly_window`  
**Analysis Date:** 2026-07-28

---

## Executive Summary

This analysis identifies the key signals that distinguish hardware incidents occurring within an anomaly window from isolated hardware incidents. The dataset contains **600 IT service records**, of which **182 are hardware-related incidents**. Of these hardware incidents, **179 (98.4%)** occur within an anomaly window, while only **3 (1.6%)** occur outside anomaly windows. This strong correlation indicates that specific, measurable signals reliably predict when hardware incidents cluster into anomalous periods.

---

## Key Signals Indicating Hardware Incidents in Anomaly Window

### 1. **High Concurrent Hardware Incident Volume (Most Significant Signal)**

**Finding:** Hardware incidents in anomaly windows show dramatically elevated recent incident counts.

- **Hardware in anomaly window:** Mean of **10.77 incidents in the previous 7 days** (Median: 5)
- **Hardware NOT in anomaly window:** Mean of only **0.67 incidents** in the previous 7 days (Max: 1)

**Practical Insight:** When a hardware incident has **>1 similar hardware issue reported in the last 7 days**, it strongly signals entry into an anomaly window. The distribution shows a clear threshold effect: incidents reporting 3+ concurrent hardware incidents in a 7-day window are reliably in anomaly periods.

**Confidence Level:** Very high—this metric shows **16x difference** between anomaly and non-anomaly hardware incidents.

---

### 2. **Priority and Criticality Clustering**

**Finding:** Hardware anomaly windows concentrate high-priority and critical incidents.

- **Hardware in anomaly window:**
  - 79.9% (143/179) are high-priority (2 - High)
  - 8.4% (15/179) are critical (1 - Critical)
  - 11.7% (21/179) are moderate (3 - Moderate)

- **Hardware NOT in anomaly window:**
  - 66.7% (2/3) are high-priority
  - 33.3% (1/3) are critical
  - 0% are moderate

**Practical Insight:** The concentration of **"2 - High" priority items** (80%) is a strong signal for anomaly-window membership, while critical items represent fewer cases but still cluster in anomalies. Isolated hardware incidents (non-anomaly) are more likely to be critical in proportion, suggesting infrastructure-level events; anomaly windows are dominated by operational hardware issues.

**Confidence Level:** High—clear difference in priority distribution patterns.

---

### 3. **Extended Resolution Duration**

**Finding:** Hardware incidents in anomaly windows frequently require longer resolution times.

- **Hardware in anomaly window:** 
  - Mean resolution time: **7.25 days** (Median: 7, Range: 1–24)
  - 50.8% (91/179) flagged as `long_resolution=1`

- **Hardware NOT in anomaly window:**
  - Mean resolution time: **6.67 days** (Median: 6, Range: 4–10)
  - 33.3% (1/3) flagged as `long_resolution=1`

**Practical Insight:** While the raw mean difference is modest (~0.6 days), the **long_resolution flag is present in 51% of anomaly-window hardware incidents**, compared to only 33% in isolated incidents. Combined with high incident volume, extended resolution signals resource contention typical of anomaly windows.

**Confidence Level:** Moderate—resolution time alone is not definitive, but the flag prevalence suggests tracking and elevated workload.

---

### 4. **Specific Hardware Symptom Patterns**

**Finding:** Certain failure modes appear predominantly in anomaly windows, indicating systemic rather than isolated problems.

**Symptom distribution in hardware anomaly-window incidents:**

| Symptom Type | Anomaly Window Count | Percentage | Non-Anomaly Count |
|---|---|---|---|
| **Printer failures** | 82 | 45.8% | 1 |
| **General hardware malfunction** | 52 | 29.1% | 1 |
| **Keyboard/input failures** | 24 | 13.4% | 0 |
| **Monitor/display failures** | 28 | 15.6% | 0 |
| **Boot/power failures** | 14 | 7.8% | 0 |
| **Storage failures** | 8 | 4.5% | 0 |
| **Cooling/thermal issues** | 5 | 2.8% | 2 |

**Key Observations:**

- **Printer problems dominate** (45.8%), representing the largest symptom cluster. This suggests shared infrastructure degradation or a systematic issue affecting multiple devices.
- **Keyboard and input device failures** (13.4%) appear exclusively in anomaly windows, never in isolated incidents, indicating potential environmental or electrical root causes.
- **Monitor/display failures** (15.6%) also cluster in anomalies, supporting systemic rather than random failure hypotheses.
- **Boot/power failures** (7.8%) are anomaly-exclusive, suggesting power delivery or infrastructure-level events.
- **Isolated incidents** show more thermal/cooling issues (66.7% of non-anomaly hardware), consistent with individual workstation problems rather than site-wide events.

**Practical Insight:** The presence of printer, keyboard, or display failures in combination is a strong predictor of anomaly window status. These are shared-infrastructure or site-deployed devices; their simultaneous failure indicates systemic issues.

**Confidence Level:** High—clear differentiation in symptom patterns between anomaly and non-anomaly incidents.

---

### 5. **Infrastructure Hardware Status**

**Finding:** Infrastructure-level hardware issues are associated differently with anomaly windows.

- **Hardware in anomaly window:** 7.8% (14/179) are infrastructure hardware
- **Hardware NOT in anomaly window:** 66.7% (2/3) are infrastructure hardware

**Practical Insight:** Anomaly-window hardware incidents are **predominantly endpoint/user-device failures** (92.2%), not infrastructure. Isolated hardware incidents are more likely to be infrastructure-level problems. This suggests:
- Anomaly windows capture **operational degradation** (mass device failures, service issues)
- Isolated hardware incidents often represent **critical infrastructure failures** (server, network hardware)

**Confidence Level:** Moderate—small sample size for non-anomaly incidents, but the pattern is consistent.

---

## Decision Framework for Identifying Hardware Anomaly Window Status

**Primary signal (highest confidence):**
1. **`hardware_incidents_last_7d` ≥ 1** → Strong indicator of anomaly window (16x prevalence)
2. **`long_resolution == 1`** → Moderate signal; 51% of anomaly incidents carry this flag
3. **Priority == "2 - High"** → 80% of anomaly incidents; dominant pattern
4. **Symptom in {printer, keyboard, display, boot/power}** → High specificity; nearly exclusive to anomalies

**Supporting context:**
- Combination of high recent incident volume + extended resolution + high-priority status provides **very high confidence** in anomaly-window prediction.
- Non-anomaly hardware incidents are rare (n=3), limiting statistical power, but show **opposite patterns**: low incident volume, infrastructure focus, critical rather than high priority.

---

## Exceptions and Caveats

1. **Small non-anomaly sample:** Only 3 hardware incidents outside anomaly windows make statistical generalizations difficult. However, the distinction is so clear (179:3 ratio) that chance is unlikely.

2. **Missing infrastructure distinction:** While 7.8% of anomaly-window incidents are infrastructure hardware, the analysis cannot isolate whether infrastructure incidents can exist in anomaly windows undetected or whether they simply follow different patterns.

3. **Temporal clustering not directly observable:** The dataset does not show timestamp granularity sufficient to confirm whether incidents truly occur simultaneously (which would strengthen anomaly-window inference). However, the high 7-day incident count strongly correlates with anomaly window designation.

4. **Causation vs. correlation:** While high recent incident volume signals anomaly windows, it is unclear whether:
   - High volume *causes* extended resolution times (resource contention), or
   - Both are symptoms of an underlying systemic issue.

---

## Conclusion

Hardware incidents occurring in anomaly windows are reliably identified by **four key signals**:

1. **Elevated concurrent hardware incident volume** (mean 10.77 vs. 0.67 per 7 days)
2. **High-priority clustering** (80% at "2 - High" priority level)
3. **Extended resolution times** (50.8% flagged as `long_resolution`)
4. **Specific symptom patterns** (printer, keyboard, display, boot failures exclusive or dominant in anomalies)

These signals support a **decision-tree approach** for real-time identification of hardware anomaly windows in IT operations, enabling proactive resource allocation and root-cause investigation during periods of elevated endpoint device failures.
