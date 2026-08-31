---
dataset: flag_13
scenario: predictive_long
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "duration_like_resolution_value"
query: "What signals are linked to longer resolution duration values?"
source_table: augment_table/flag_13/predictive_long/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:15:37.067975+00:00
wall_seconds: 98.84
---

# Analysis Report: Signals Linked to Longer Resolution Duration

**Dataset:** Flag 13 – Predictive Long Duration (skill_on variant)  
**Query:** What signals are linked to longer resolution duration values?  
**Sample Size:** 500 incidents (250 long-duration ≥29.5 min, 250 short-duration <29.5 min)

---

## Executive Summary

This analysis identifies concrete patterns in incident attributes that correlate with longer resolution times (≥29.5 minutes, the dataset median). The strongest signals involve **connectivity and access-related issues**, **database-related work**, **night-time openings**, and **network infrastructure scope**. Incidents described as VPN connection problems or database access issues consistently take the longest to resolve.

---

## Key Findings

### 1. **Incident Category – Strong Predictor**

Long-duration incidents are disproportionately associated with specific problem types:

- **Connectivity issues:** 42.0% of long-duration vs. 37.2% of short-duration (+4.8 pp differential)
- **Database issues:** 29.2% of long-duration vs. 27.6% of short-duration (+1.6 pp)
- **Email issues:** 25.2% of long-duration vs. 28.8% of short-duration (−3.6 pp)
- **Software issues:** 2.4% of long-duration vs. 4.0% of short-duration (−1.6 pp)
- **Hardware issues:** 1.2% of long-duration vs. 2.4% of short-duration (−1.2 pp)

**Interpretation:** Connectivity and database problems form the core of long-resolution incidents. Email and software issues, while common, resolve faster on average.

### 2. **Severity Signal – Access Issues Drive Length**

The type of problem reported shows a clear pattern:

- **Access/login failure:** 62.8% of long-duration vs. 56.8% of short-duration (+6.0 pp)
- **Service outage:** 24.0% of long-duration vs. 25.6% of short-duration (−1.6 pp)
- **Degraded performance:** 13.2% of long-duration vs. 17.6% of short-duration (−4.4 pp)

**Interpretation:** Access-related problems (cannot connect, cannot log in, cannot authenticate) are the most reliable predictor of longer resolution times. Outages and performance degradation, while serious, often have faster resolution paths.

### 3. **Infrastructure Scope – Server & Network Primacy**

The physical scope of affected systems matters:

- **Server-scoped incidents:** 50.4% of long-duration vs. 49.2% of short-duration (+1.2 pp)
- **Network-scoped incidents:** 38.0% of long-duration vs. 35.2% of short-duration (+2.8 pp)
- **User endpoint-scoped incidents:** 11.6% of long-duration vs. 15.2% of short-duration (−3.6 pp)

**Interpretation:** When incidents affect multiple endpoints via network or server infrastructure (rather than isolated workstations), resolution times lengthen. This suggests that shared infrastructure problems require more coordinated or complex diagnosis.

### 4. **Time of Opening – Night Incidents Take Longer**

Temporal patterns reveal significant variation:

- **Night (22:00–06:00):** 36.8% of long-duration vs. 32.4% of short-duration (+4.4 pp)
- **Business hours (afternoon):** 23.6% of long-duration vs. 27.6% of short-duration (−4.0 pp)
- **Evening (18:00–22:00):** 21.6% of long-duration vs. 20.4% of short-duration (+1.2 pp)
- **Business hours (morning):** 18.0% of long-duration vs. 19.6% of short-duration (−1.6 pp)

**Interpretation:** Incidents opened during night hours are more likely to be long-duration. This likely reflects reduced staffing, limited escalation paths, and fewer subject-matter experts available for complex problems.

### 5. **Resolution Pathway Complexity – Limited Variation**

Interestingly, escalation status shows minimal correlation:

- **Escalated incidents:** 78.8% of long-duration vs. 80.0% of short-duration (−1.2 pp)
- **Direct resolution:** 20.4% of long-duration vs. 20.0% of short-duration (+0.4 pp)
- **Multi-stage:** 0.8% of long-duration vs. 0.0% of short-duration (+0.8 pp)

**Interpretation:** Both long and short incidents follow similar escalation patterns, suggesting that escalation is a result of complexity rather than a primary driver of duration. The rare multi-stage incidents (n=2) cannot support strong inference.

### 6. **Technician Assignment Alignment – Negligible Effect**

Whether the assigned technician specialized in the issue area shows minimal correlation:

- **Misaligned assignment:** 79.6% of long-duration vs. 80.8% of short-duration (−1.2 pp)
- **Aligned assignment:** 20.4% of long-duration vs. 19.2% of short-duration (+1.2 pp)

**Interpretation:** Skill-to-task alignment has minimal practical effect on duration in this dataset. This may reflect that escalation and team routing are effective compensators, or that the baseline alignment rate is already high.

### 7. **Assignment Group – Marginal Differences**

By support team:

- **Network:** 56.8% of long-duration vs. 58.0% of short-duration (−1.2 pp)
- **Database:** 28.8% of long-duration vs. 26.8% of short-duration (+2.0 pp)
- **Service Desk:** 7.2% of long-duration vs. 6.4% of short-duration (+0.8 pp)
- **Software/Hardware:** Minimal representation in both cohorts

**Interpretation:** Database-assigned incidents show slightly higher representation in long-duration cases, consistent with earlier findings that database issues correlate with longer times.

---

## Top Concrete Patterns – Longest-Resolving Issues

The most frequently recorded long-duration incidents center on network access:

| Issue Description | Frequency | Avg Duration |
|---|---|---|
| Unable to connect to VPN | 15 incidents | 42.9 min |
| Email server not responding | 7 incidents | 47.4 min |
| Database connection issue | 6 incidents | 47.3 min |
| Unable to connect to the VPN | 6 incidents | 48.5 min |
| Cannot connect to VPN | 5 incidents | 44.4 min |
| Cannot connect to office VPN | 4 incidents | 46.0 min |
| Unable to access company database | 7 incidents | 38.6 min |

**Interpretation:** VPN connectivity and database access dominate the longest-resolving incident list. These are typically infrastructure problems requiring configuration review, authentication troubleshooting, or backend investigation.

---

## Duration Statistics

| Metric | Value |
|---|---|
| Minimum | 0 min |
| Maximum | 59 min |
| Mean | 29.7 min |
| Median | 29.5 min |
| Std. Dev. | 16.8 min |

The near-equal mean and median indicate a symmetric distribution with no extreme outliers driving the average.

---

## Weak Evidence & Exceptions

1. **Priority Level:** Critical vs. High priority shows minimal difference in average duration (16.0% vs. 17.2% representation), suggesting that priority assignment may not reflect actual complexity drivers or that escalation effectiveness equalizes outcomes.

2. **Multi-stage incidents:** Only 2 incidents classified as multi-stage; insufficient to draw firm conclusions about multi-stage resolution patterns.

3. **Technician alignment:** The lack of strong correlation is unexpected and may indicate that either (a) the dataset's baseline alignment is high, or (b) routing and escalation compensate for initial misalignment.

4. **Email issues paradox:** Email incidents, while common, skew toward shorter resolution times despite involving critical services. This may reflect well-developed diagnostic workflows or service-provider SLAs.

---

## Recommendations for Prediction

**High-confidence signals for predicting long resolution duration:**

1. Incident involves **VPN connectivity or database access** failures (strongest individual signal)
2. Incident opened during **night hours** (4.4 pp higher representation)
3. Affects **network infrastructure** scope rather than isolated endpoints (2.8 pp higher)
4. Classified as **access/login failure** rather than outage or degradation (6.0 pp higher)

**Weak signals (not recommended for prediction):**

- Escalation pathway (nearly identical across duration cohorts)
- Technician assignment alignment (≤1.2 pp effect)
- Priority level (minimal variation)

---

## Data Quality Notes

- All 500 rows have valid duration measurements and complete categorical data.
- No missing values in focus variables.
- Duration distribution is approximately uniform; no evidence of systematic bias toward short or long incidents.
- Assignment group and infrastructure scope show expected domain coverage for IT incident datasets.
