---
dataset: flag_13
scenario: eda_duration
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "resolution_duration"
query: "How does resolution duration vary across incident category and priority?"
source_table: augment_table/flag_13/eda_duration/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:15:32.069009+00:00
wall_seconds: 108.68
---

# Analysis Report: Resolution Duration Across Incident Category and Priority

## Query
How does resolution duration vary across incident category and priority?

## Method Note

**TAPP-Generated Columns Used in Analysis:**
- `resolution_complexity` (Reassigned vs. Single Assignment)
- `incident_severity_signal` (Type of technical impact: connectivity_interruption, access_denial, server_outage_level, single_system, etc.)
- `incident_repeat_pattern` (Recurring Issue vs. Isolated Incident)
- `affected_service_domain` (Business service domain affected)

These augmented columns enriched understanding of resolution drivers beyond structural category and priority variables.

---

## Executive Summary

Across 500 incidents from 2023, **resolution duration is remarkably stable across priority levels** (30.3 min critical, 29.9 min high, 31.5 min moderate), indicating that priority classification does not strongly predict actual time to resolution. **Incident category explains more variance**: connectivity issues take longest (32.1 min mean), while database (29.7 min) and email (28.9 min) incidents resolve faster. **Resolution complexity**—captured by the TAPP-generated `resolution_complexity` field—emerges as a key driver: single-assignment incidents take ~2–6 minutes longer than reassigned ones, particularly for VPN access (+5.8 min) and connectivity issues (+4.6 min). Incident severity signal and repeat pattern provide additional explanatory power in select categories.

---

## 1. Priority-Level Analysis

### 1.1 Resolution Duration by Priority (All 500 Incidents)

| Priority | Count | Mean Duration (min) | Median | Std Dev |
|----------|-------|---------------------|--------|---------|
| **1 - Critical** | 83 | 30.3 | 32.0 | 16.6 |
| **2 - High** | 391 | 29.9 | 29.6 | 17.1 |
| **3 - Moderate** | 24 | 31.5 | 29.2 | 14.9 |
| **4 - Low** | 2 | 25.0 | 25.0 | 7.1 |

**Finding:** Priority labels correlate weakly with resolution speed. Critical incidents (n=83) resolve at 30.3 minutes, only marginally slower than high-priority incidents (29.9 min). This suggests that priority classification may reflect business impact rather than technical complexity or time-to-fix.

---

## 2. Incident Category Analysis

### 2.1 Resolution Duration by Category (All Incidents)

| Category | Count | Mean (min) | Median | Std Dev | Range |
|----------|-------|-----------|--------|---------|-------|
| **Connectivity** | 82 | 32.1 | 33.9 | 17.6 | 0.9–59.4 |
| **Printing** | 7 | 33.7 | 24.8 | 18.1 | 16.6–58.2 |
| **Software** | 13 | 30.8 | 28.0 | 13.8 | 8.7–52.2 |
| **VPN Access** | 109 | 30.3 | 30.3 | 16.7 | 1.2–59.0 |
| **Email** | 135 | 28.9 | 27.1 | 16.9 | 0.4–59.2 |
| **Database** | 134 | 29.7 | 30.0 | 17.1 | 0.2–60.0 |

**Finding:** Connectivity issues are the most time-consuming (32.1 min mean, 82 incidents), 11% longer than email incidents. Database and email—the largest categories (134 and 135 incidents respectively)—resolve within ~29 minutes, suggesting familiarity and standardized procedures.

---

## 3. Category × Priority Interaction

### 3.1 Mean Resolution Duration (minutes) by Category and Priority

|  | 1 - Critical | 2 - High | 3 - Moderate | 4 - Low |
|---|---|---|---|---|
| **Connectivity** | 45.6 | 31.4 | 29.1 | — |
| **VPN Access** | 36.3 | 30.1 | 24.2 | — |
| **Database** | 33.1 | 28.9 | 32.8 | 30.0 |
| **Email** | 25.0 | 30.0 | 39.5 | 20.0 |
| **Software** | 52.2 | 28.2 | 37.7 | — |
| **System Performance** | 35.3 | 24.0 | 25.2 | — |

**Critical-Priority Anomalies:**
- **Software (Critical):** 52.2 min (n=1) – single incident; longest overall.
- **Connectivity (Critical):** 45.6 min (n=5) – highly elevated; represents 9% longer than non-critical connectivity issues.
- **VPN Access (Critical):** 36.3 min (n=7) – 21% slower than high-priority VPN issues.

**Moderate-Priority Anomaly:**
- **Email (Moderate):** 39.5 min (n=8) – counter-intuitively slower than both critical (25.0 min) and high (30.0 min) email incidents.

---

## 4. Resolution Complexity (TAPP-Generated `resolution_complexity`)

### 4.1 Complexity Distribution and Duration

| Complexity | Count | Mean (min) | Median | Std Dev |
|---|---|---|---|---|
| **Reassigned** | 319 | 29.1 | 28.0 | 17.1 |
| **Single Assignment** | 181 | 31.7 | 33.4 | 16.3 |

**Finding:** Single-assignment incidents take **2.6 minutes longer** on average (+8.9% more time). This likely reflects higher complexity requiring fewer escalations, or simpler issues resolved immediately by first responder.

### 4.2 Complexity × Priority Interaction

| Priority | Reassigned (min) | Single Assignment (min) | Δ |
|---|---|---|---|
| **1 - Critical** | 29.8 | 31.1 | +1.3 |
| **2 - High** | 29.0 | 31.6 | +2.6 |
| **3 - Moderate** | 28.3 | 35.8 | +7.5 |

**Finding:** The complexity gap widens for moderate-priority incidents, suggesting that lower-urgency single-assignment cases may face longer queues or less structured resolution procedures.

### 4.3 Complexity by Major Categories

| Category | Reassigned | Single Assign | Δ | Insight |
|---|---|---|---|---|
| **Email** | 29.0 min | 28.8 min | −0.25 | Minimal complexity effect; streamlined procedures |
| **Database** | 28.9 min | 31.0 min | +2.14 | Single assignment slightly slower |
| **VPN Access** | 28.4 min | 34.2 min | +5.83 | **Largest gap**; single assignments face obstacles |
| **Connectivity** | 30.6 min | 35.2 min | +4.58 | Single handlers slower than escalation teams |

---

## 5. Incident Severity Signal (TAPP-Generated `incident_severity_signal`)

### 5.1 Mean Duration by Severity Signal (All Incidents)

| Signal | Count | Mean (min) | Median |
|---|---|---|---|
| **Multi-System Impact** | 3 | 34.8 | 32.2 |
| **Performance Degradation** | 20 | 31.5 | 31.2 |
| **Connectivity Interruption** | 169 | 30.6 | 30.7 |
| **Access Denial** | 133 | 30.3 | 30.0 |
| **Server Outage Level** | 42 | 29.9 | 30.7 |
| **Single System** | 122 | 29.1 | 28.1 |
| **User Workstation** | 11 | 27.3 | 22.3 |

**Finding:** Multi-system impact (rare, n=3) takes longest, but reliability is low. Among high-volume signals (>100), **connectivity interruption** (169 incidents, 30.6 min) slightly exceeds **access denial** (133 incidents, 30.3 min), suggesting networked issues have marginally higher friction than authorization problems.

### 5.2 Severity Signal in Major Categories

**Email incidents (n=135):**
- Single System: 27.4 min (n=83, 61%)
- Access Denial: 32.4 min (n=24, 18%)
- Difference: +5.0 min (+18%)

**Database incidents (n=134):**
- Access Denial: 29.9 min (n=101, 75%)
- Single System: 30.5 min (n=18, 13%)
- Difference: +0.6 min (+2%) — minimal gap

**Finding:** Email's severity signal explains more variance (18% difference) than database's (2% difference), suggesting email issues with access-denial semantics (e.g., "unable to access email") are genuinely harder to troubleshoot than single-system email problems.

---

## 6. Incident Repeat Pattern (TAPP-Generated `incident_repeat_pattern`)

### 6.1 Overall Impact

| Repeat Pattern | Count | Mean (min) | Median |
|---|---|---|---|
| **Recurring Issue** | 360 | 30.3 | 30.3 |
| **Isolated Incident** | 140 | 29.5 | 29.1 |

**Finding:** Recurring issues are **0.8 minutes slower** (+2.7%), suggesting either institutional inertia or that root causes of recurring problems remain unresolved.

### 6.2 Repeat Pattern by Major Categories

| Category | Recurring (n) | Isolated (n) | Recurring Mean | Isolated Mean | Δ |
|---|---|---|---|---|---|
| **Email** | 78 | 57 | 29.9 min | 27.6 min | +2.3 min (+8.2%) |
| **Database** | 127 | 7 | 29.6 min | 31.5 min | −1.9 min (−6.1%) |
| **VPN Access** | 108 | 1 | 30.2 min | 47.9 min | −17.8 min (−37%) |

**Finding:** For email, recurring issues are 8% slower, suggesting repeated failures warrant improved preventive measures. For VPN, the one isolated incident took much longer (47.9 min), but n=1 makes generalization unreliable. Database shows no meaningful repeat-pattern effect.

---

## 7. Affected Service Domain (TAPP-Generated `affected_service_domain`)

### 7.1 Duration by Service Domain

| Domain | Count | Mean (min) | Median | Std Dev |
|---|---|---|---|---|
| **System Availability** | 27 | 32.3 | 34.5 | 16.9 |
| **Network Infrastructure** | 138 | 31.5 | 31.1 | 16.9 |
| **Data Platform** | 136 | 29.6 | 30.0 | 17.1 |
| **Identity & Access** | 46 | 29.6 | 30.4 | 17.0 |
| **Communication Platform** | 134 | 29.0 | 27.1 | 16.9 |
| **Client Application** | 19 | 28.0 | 22.3 | 14.7 |

**Finding:** System availability and network infrastructure are the slowest domains (~31–32 min), while client applications are fastest (28 min). This aligns with incident distribution: network infrastructure incidents (connectivity, VPN) are inherently slower than email (communication platform).

---

## 8. Correlation Summary: Key Drivers of Resolution Duration

### Rank of Effect Sizes (Largest to Smallest):
1. **Incident Category** (email 28.9 min → connectivity 32.1 min; **3.2 min range**)
2. **Service Domain** (client application 28.0 min → system availability 32.3 min; **4.3 min range**)
3. **Resolution Complexity** (reassigned 29.1 min → single assignment 31.7 min; **2.6 min difference**)
4. **Priority** (critical 30.3 min → high 29.9 min → moderate 31.5 min; **1.6 min range, non-monotonic**)
5. **Repeat Pattern** (recurring 30.3 min → isolated 29.5 min; **0.8 min difference**)
6. **Severity Signal** (workstation 27.3 min → multi-system 34.8 min; **7.5 min range**, but multi-system n=3)

**Critical Insight:** Priority is a weak direct predictor of resolution speed; **incident category and technical complexity** (captured by both original `category` field and TAPP-generated `resolution_complexity`) are stronger drivers.

---

## 9. Detailed Profiles: Top 3 Categories

### Email Incidents (n=135, 27%)

- **Priority Distribution:** 43 Critical, 83 High, 8 Moderate, 1 Low
- **Mean Duration by Priority:** Critical 25.0 min → High 30.0 min → Moderate 39.5 min (non-monotonic)
- **Complexity:** Reassigned 29.0 min (n=83) vs. Single 28.8 min (n=52) — minimal difference
- **Severity Signal:** Single-System dominant (n=83); fastest at 27.4 min; Access-Denial slower at 32.4 min
- **Repeat Pattern:** Recurring 29.9 min (n=78) vs. Isolated 27.6 min (n=57)

**Takeaway:** Email is fastest overall; single-system issues streamlined; recurring problems suggest need for better triage.

### Database Incidents (n=134, 27%)

- **Priority Distribution:** 21 Critical, 108 High, 4 Moderate, 1 Low
- **Mean Duration by Priority:** Critical 33.1 min → High 28.9 min → Moderate 32.8 min
- **Complexity:** Reassigned 28.9 min (n=80) vs. Single 31.0 min (n=54)
- **Severity Signal:** Access-Denial dominant (n=101, 75%); mean 29.9 min
- **Repeat Pattern:** Recurring 29.6 min (n=127) dominates; Isolated rare (n=7)

**Takeaway:** Database resolution shows critical-priority anomaly (slower than high); access-denial issues (connection problems) are standard fare; high repetition suggests unresolved root causes.

### VPN Access Incidents (n=109, 22%)

- **Priority Distribution:** 7 Critical, 100 High, 2 Moderate
- **Mean Duration by Priority:** Critical 36.3 min → High 30.1 min → Moderate 24.2 min (inverse pattern)
- **Complexity:** Reassigned 28.4 min (n=72) vs. Single 34.2 min (n=37) — **largest 5.8 min gap**
- **Severity Signal:** Connectivity Interruption universal (n=109, 100%)
- **Repeat Pattern:** Recurring 30.2 min (n=108); Isolated 47.9 min (n=1, unreliable)

**Takeaway:** VPN single-assignment incidents are significantly slower (+5.8 min), suggesting complex authentication issues benefit from escalation. Moderate-priority incidents resolve fastest, likely selection bias (non-urgent, simple issues).

---

## 10. Actionable Observations

1. **Priority Misalignment:** Priority labels do not predict resolution speed. Critical connectivity issues (45.6 min) take 50% longer than critical email issues (25.0 min). Recommend re-calibrating priority matrix to reflect technical complexity rather than pure business impact.

2. **Complexity Matters:** Single-assignment resolution, especially for VPN (+5.8 min) and connectivity (+4.6 min), suggests frontline handlers lack tools or authority to resolve network issues. Cross-training or escalation path optimization may reduce duration.

3. **Recurring Issues:** Email recurring problems average 8.2% longer than isolated incidents; database and VPN show weaker or reversed patterns. For email, root-cause analysis on top repeat patterns (e.g., "Outlook not syncing") could prevent future escalations.

4. **Service Domain Trade-offs:** System availability and network infrastructure are inherently slower; communication platform and client application incidents are faster. Staffing and SLA targets should account for domain-specific complexity, not uniform time budgets.

5. **Severity Signal Relevance:** For email, severity signal explains 18% of variance (single-system vs. access-denial); for database, only 2%. Severity classification is category-dependent and should inform triage logic selectively.

---

## Conclusion

Resolution duration varies across incident category and priority, but **not in the expected way**. Priority is a weak direct predictor; **incident category** (connectivity > VPN access > database ≈ email) and **resolution complexity** (single assignment ~2.6 min slower on average, up to +5.8 min for VPN) are stronger drivers. TAPP-generated augmentations—particularly `resolution_complexity`, `incident_severity_signal`, and `incident_repeat_pattern`—clarify that technical factors and workflow design (reassignment patterns) have larger effects than administrative severity labels. Organizations should use these semantic signals to optimize escalation policies and staffing allocation rather than relying solely on priority-based SLAs.
