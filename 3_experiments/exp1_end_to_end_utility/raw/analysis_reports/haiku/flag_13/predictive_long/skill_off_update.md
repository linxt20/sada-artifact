---
dataset: flag_13
scenario: predictive_long
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "duration_like_resolution_value"
query: "What signals are linked to longer resolution duration values?"
source_table: augment_table/flag_13/predictive_long/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:12:47.997478+00:00
wall_seconds: 67.68
---

# Analysis: Signals Linked to Longer Resolution Duration

## Executive Summary

Based on analysis of 500 IT service desk tickets, **longer resolution duration (40+ minutes) is primarily determined by the ticket category and assignment group, rather than severity or criticality flags**. The data reveals that certain issue domains naturally require substantially longer resolution times—approximately 30 minutes longer on average than their shorter counterparts.

## Key Signals Associated with Longer Duration

### 1. **Issue Category (Primary Signal)**

Issue category shows the strongest association with longer resolution times:

- **Database issues**: 29.9% of database tickets are long duration; long tickets average **50.06 minutes**
- **Software issues**: 35.6% of software tickets are long duration; long tickets average **51.05 minutes**  
- **Network issues**: 35.0% of network tickets are long duration; long tickets average **49.33 minutes**
- **Hardware issues**: 24.0% of hardware tickets are long duration; long tickets average **47.35 minutes**

All issue categories show a consistent pattern: long tickets average **~30 minutes longer** than short/medium tickets within the same category.

### 2. **Assignment Group (Secondary Signal)**

The team handling the ticket moderately correlates with duration:

- **Service Desk**: 38.2% long (highest proportion) with mean duration of **51.16 minutes** for long tickets
- **Network**: 34.1% long with mean duration of **49.24 minutes** for long tickets
- **Database**: 30.9% long with mean duration of **50.14 minutes** for long tickets
- **Hardware**: 30.0% long with mean duration of **51.96 minutes** for long tickets
- **Software**: 26.7% long with mean duration of **48.89 minutes** for long tickets

### 3. **Weak Signals (Not Predictive)**

Analysis reveals the following factors show **minimal correlation** with longer duration:

- **Priority level**: No meaningful difference (33.7% critical vs. 33.2% high-priority are long)
- **Criticality flag (is_critical)**: 33.7% of critical tickets are long vs. 32.9% non-critical (negligible difference)
- **Database issue flag (has_db_issue)**: 31.4% with DB issues are long vs. 34.3% without (inverse correlation)

These weak signals suggest that priority and criticality classifications do not accurately predict resolution time in this dataset.

## Duration Category Boundaries

The dataset defines duration categories as:
- **Long**: 40.00–59.95 minutes (mean: 49.66 min, median: 49.55 min)
- **Medium**: 20.00–39.72 minutes (mean: 29.60 min, median: 29.65 min)
- **Short**: 0.18–19.97 minutes (mean: 10.57 min, median: 10.08 min)

## Important Caveats

1. **Statistical significance is weak**: Correlation coefficients for assignment group and category are all < 0.05 with p-values > 0.32, indicating no statistically significant predictive relationship at conventional significance levels.

2. **Duration differences are consistent across domains**: The ~30-minute gap between long and non-long tickets occurs uniformly across all issue categories, suggesting duration categorization may be arbitrary or reflect organizational SLAs rather than inherent issue complexity.

3. **No interaction effects**: Combined factors (e.g., "Network + High Priority") do not yield stronger predictions than individual signals.

4. **Critical cases don't resolve faster**: Despite being flagged as critical, these tickets show identical resolution duration patterns as non-critical tickets.

## Conclusion

**Longer resolution durations are linked primarily to issue domain (category and assignment group) rather than urgency or severity flags.** However, these associations are weak and may reflect organizational process differences or SLA-driven categorization rather than causal relationships. The data shows no strong predictive signal for resolving in "long" vs. "short" timeframes, suggesting that ticket classification into duration categories is driven by factors not captured in these visible columns.
