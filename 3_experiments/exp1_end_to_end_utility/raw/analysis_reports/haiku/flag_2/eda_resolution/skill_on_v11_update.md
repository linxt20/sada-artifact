---
dataset: flag_2
scenario: eda_resolution
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "resolution_time"
query: "How does resolution time vary across category, priority, and assignment group?"
source_table: augment_table/flag_2/eda_resolution/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:17:16.156106+00:00
wall_seconds: 85.77
---

# Resolution Time Analysis: Variant Label "skill_on"

## Executive Summary

This analysis examines how resolution time varies across category, priority, and assignment group using 500 IT service incidents (372 with valid resolution times). The dataset reveals substantial variation in resolution times, with assignment group being a particularly strong differentiator. Mean resolution time is **1,043 hours (43 days)**, with a range of 24 to 2,206 hours.

A critical finding is that **technician assignment continuity significantly impacts resolution times**: incidents with continuous assignment average 1,594 hours, versus 595 hours without continuity—a 2.7x difference. This suggests that fragmented assignments substantially delay resolution.

---

## Key Findings by Dimension

### Category Impact

Resolution times are relatively consistent across categories (min: 955 hours, max: 1,105 hours):

- **Hardware**: 1,105 hours (n=18) — slowest; small sample size warrants caution
- **Network**: 1,079 hours (n=269) — large category, ~36 days average
- **Software**: 1,051 hours (n=86)
- **Inquiry / Help**: 958 hours (n=11) — fastest
- **Database**: 955 hours (n=116) — fastest among large categories

**Interpretation**: Category differences are modest (±10% from mean). Database and Inquiry/Help categories resolve 5-10% faster than Hardware and Network, but the effect is small. Sample size imbalance (269 Network vs. 11 Inquiry/Help) means category-level conclusions should be treated cautiously.

### Priority Impact

Priority shows weak effect on resolution time:

- **3 - Moderate**: 1,121 hours (n=41)
- **1 - Critical**: 1,119 hours (n=79)
- **2 - High**: 1,019 hours (n=380)

**Interpretation**: Moderate and Critical priorities resolve *slower* than High priority (9-10% longer), suggesting potential misalignment between priority labels and actual urgency, or that Critical and Moderate issues are inherently more complex. The majority of incidents (76%) are labeled "High priority," yet they resolve slightly faster than higher labels. This counterintuitive pattern warrants investigation into priority assignment practices.

### Assignment Group Impact

Assignment group shows the **strongest differentiation**:

- **Openspace**: 1,853 hours (n=1) — extreme outlier, ignore
- **Service Desk**: 1,102 hours (n=41) — 17% above mean
- **Network**: 1,074 hours (n=300) — large group, near mean
- **Software**: 1,028 hours (n=32) — 2% below mean
- **Database**: 947 hours (n=121) — **12% below mean**, fastest large group
- **Hardware**: 926 hours (n=5) — fastest, but small sample

**Interpretation**: Database assignment group resolves incidents 12-15% faster than average, while Service Desk handles incidents 17% slower. The Database group's efficiency may reflect specialized skill concentration and routine issue patterns. Network group's large volume (60% of dataset) and near-mean performance suggests network issues are heterogeneous in complexity.

---

## Interaction Effects: Notable Combinations

### Slowest Resolutions (n ≥ 5)

1. **Database + Critical + Database group**: 1,244 hours (n=13)
   - Critical database issues handled by database team take longest
   - Possible: high stakes, complex root cause analysis required

2. **Software + Moderate + Service Desk**: 1,168 hours (n=9)
   - Software issues with moderate priority sent to Service Desk
   - Suggests potential skill mismatch or assignment inefficiency

3. **Network + Moderate + Network group**: 1,165 hours (n=6)
   - Moderate network issues take as long as critical issues
   - Small sample; possible data collection or severity labeling issues

### Fastest Resolutions (n ≥ 5)

1. **Database + Moderate + Database group**: 817 hours (n=5)
   - Faster than any other major combination
   - Small sample limits confidence

2. **Database + High + Database group**: 910 hours (n=68)
   - Database group's bread-and-butter work
   - Well-practiced, consistent resolution

3. **Software + High + Software group**: 913 hours (n=19)
   - Software team handles High-priority issues efficiently
   - Suggests good skill/assignment alignment

---

## The "Technician Assignment Continuity" Factor

A critical non-requested finding emerged during analysis:

| Continuity | Mean Resolution | Median | n |
|------------|-----------------|--------|---|
| **No** (False) | 595 hours | 535 hours | 205 |
| **Yes** (True) | 1,594 hours | 1,579 hours | 167 |

**Interpretation**: This counterintuitive reversal suggests data quality issues:
- The "technician_assignment_continuity" column may be a proxy for unresolved incidents or escalations
- Incidents with `True` may represent those requiring handoffs, reviews, or multiple intervention cycles
- This field is confounded with resolution complexity, not pure assignment continuity benefit

**Implication**: This dataset cannot isolate the true effect of assignment continuity without understanding the variable's underlying definition and temporal dynamics.

---

## Resolution Completion Status

All 372 records with valid resolution times have `resolution_completion_status = True`, indicating complete resolution. No variance to analyze; this field provides no discrimination.

---

## Data Quality Observations

1. **Missing Resolution Times**: 128 of 500 incidents (25.6%) lack resolution times, potentially representing:
   - Incomplete incidents
   - Ongoing incidents at data collection time
   - Data entry errors
   These exclusions bias analysis toward completed incidents

2. **Sample Imbalances**:
   - Network category dominates (269/500, 54%)
   - Service Desk and Software groups are small (32-41 each)
   - Openspace group has only 1 incident
   Small groups should not drive decision-making

3. **Priority Distribution**: 76% of incidents are "High" priority, suggesting either actual high incident severity or label inflation

---

## Conclusions and Recommendations

1. **Category Effect (Weak)**: Resolution time varies only ±5-10% by category. Database issues resolve fastest; investment in database team expertise may be returning value.

2. **Priority Effect (Weak, Counterintuitive)**: Moderate and Critical priorities take longer than High priority. Audit priority labeling practices and consider remapping severity thresholds.

3. **Assignment Group Effect (Moderate)**: 
   - Database group outperforms average by ~12%; benchmark their processes
   - Service Desk lags by ~17%; investigate skill gaps or task routing inefficiencies
   - Network group's scale (60% of incidents) masks diversity; disaggregate by issue type

4. **Critical Unaddressed Factor**: Technician assignment continuity shows a 2.7x resolution time difference, but direction is counterintuitive. Require domain expertise to interpret this field correctly before drawing conclusions.

5. **Data Completeness**: 26% missing resolution times warrants investigation into tracking processes.

---

## Limitations

- Analysis is restricted to closed/resolved incidents with valid timestamps; ongoing issues excluded
- Cross-dimensional combinations often have small sample sizes (n=1-10), limiting statistical confidence
- The dataset does not capture business context (SLA targets, priority mappings, skill levels, or queue dynamics)
- Temporal patterns (time-of-day, day-of-week) not examined
- No statistical significance testing performed due to confounding and small subgroup sizes
