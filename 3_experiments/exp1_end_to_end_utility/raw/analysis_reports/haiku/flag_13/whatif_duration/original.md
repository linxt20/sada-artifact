---
dataset: flag_13
scenario: whatif_duration
variant: original
model: substrate-claude-haiku-4-5
query_subtype: what_if
focus_variable: "resolution_duration"
query: "If the most common operational burdens described in the text were eliminated, how much would resolution duration drop?"
source_table: augment_table/flag_13/whatif_duration/original.csv
generated_at: 2026-07-26T13:21:19.186316+00:00
wall_seconds: 137.19
---

# What-If Analysis: Impact of Eliminating Common Operational Burdens on Resolution Duration

## Query
**"If the most common operational burdens described in the text were eliminated, how much would resolution duration drop?"**

**Variant:** original.csv (500 incidents from IT Service Management dataset)

---

## Key Findings

### Overall Duration Baseline
- **Mean resolution duration:** 30.05 minutes
- **Median:** 29.85 minutes  
- **Range:** 0.18 to 59.95 minutes
- **Standard deviation:** 16.84 minutes

### Most Common Operational Burdens

The dataset reveals five dominant operational burden categories:

1. **Network Issues** (57.4% of incidents, 287 cases)
   - Mean duration: 29.90 minutes
   - Includes VPN connectivity, WiFi, internet outages

2. **Database Issues** (27.8% of incidents, 139 cases)
   - Mean duration: 29.97 minutes
   - Includes connection errors, access problems, SQL server issues

3. **Service Desk/Support** (6.8% of incidents, 34 cases)
   - Mean duration: 32.81 minutes (longest average)
   - Email access and account management issues

4. **Software Issues** (6.0% of incidents, 30 cases)
   - Mean duration: 28.45 minutes
   - Client crashes, sync problems, update failures

5. **Hardware Issues** (2.0% of incidents, 10 cases)
   - Mean duration: 30.84 minutes
   - Printer and workstation problems

### Specific Operational Burden Patterns

The most frequent incident types (detected via text analysis):

- **"Cannot/Unable to connect to VPN"** – 59 incidents (11.8%)
- **"Email server not responding"** – 20 incidents (4.0%)
- **"Unable to access database"** – 34 incidents (6.8%)
- **"Database connection issues"** – 8 incidents, but with **40.85 min mean duration** (notably high)

Other frequent burdens: network connectivity ("network|wifi|internet" appears in 14.2% of incidents), server issues (24.4%), and access/login problems (22.2%).

---

## What-If Impact Estimates

### Individual Service Elimination
If each top burden category were eliminated:

| Burden | Count | % of Total | Current Mean | If Eliminated | Duration Reduction |
|--------|-------|-----------|--------------|---------------|--------------------|
| **Service Desk** | 34 | 6.8% | 32.81 min | 29.85 min | **2.96 minutes (9.9%)** |
| **Database** | 139 | 27.8% | 29.97 min | 30.08 min | -0.11 min (-0.4%) |
| **Network** | 287 | 57.4% | 29.90 min | 30.25 min | -0.35 min (-1.2%) |

**Key observation:** Service Desk incidents are the only burden that would measurably reduce resolution time if eliminated. Database and Network incidents have durations slightly *below* baseline, suggesting their removal would have negligible impact or slightly increase average duration (though this is likely due to confounding factors like incident complexity).

### Combined Top 3 Services (92% of volume)
If the three most common service categories (Network, Database, Service Desk) were eliminated:
- **Resulting mean duration:** 29.05 minutes
- **Total reduction:** 1.00 minute (3.3% improvement)

This modest improvement reflects that the top burden categories are distributed across a wide duration range and do not consistently drive longer resolution times.

---

## Duration Variance by Category
By incident category type:

| Category | Count | Mean Duration | Std Dev |
|----------|-------|----------------|---------|
| **Software** | 73 | 31.55 min | 17.32 |
| **Hardware** | 25 | 30.79 min | 13.53 |
| **Network** | 260 | 30.08 min | 16.98 |
| **Database** | 134 | 29.16 min | 17.19 |
| **Inquiry/Help** | 8 | 28.04 min | 13.51 |

---

## Important Caveats and Weak Evidence

1. **Limited causal leverage:** The data shows that common operational burdens (Network and Database) have nearly identical resolution durations to less common ones. This suggests the frequency of an issue type does not directly determine how long it takes to resolve.

2. **Service Desk outlier:** The Service Desk category shows materially longer resolution times (32.81 min vs. 30.05 min baseline). However, only 6.8% of incidents fall into this category, limiting its impact on overall figures.

3. **Confounding not controlled:** The analysis assumes operational burden elimination is orthogonal to other resolution drivers (assignee skill, incident complexity, infrastructure readiness). In practice, common burdens may be quick to resolve *because* organizations have optimized response to them.

4. **No temporal or interaction effects:** The dataset does not reveal whether certain burden combinations create disproportionate delays or whether resolution time is bounded by infrastructure limits.

5. **Missing mechanism variables:** The ground truth annotation identifies reassignment and scope of impact as key drivers. Without analyzing these augmented columns, the estimate is incomplete.

---

## Conclusion

Eliminating the most common operational burdens (Network and Database incidents, representing 85.2% of the dataset) would **reduce mean resolution duration by approximately 1 minute (3.3%)**, based on a simple removal model. However, this finding has weak empirical support: the most common burdens actually have *below-average* resolution durations, suggesting they are not the primary drivers of long resolution times.

**A more actionable insight** would focus on Service Desk incidents, which do show elevated resolution times (+2.96 min or +9.9%), but represent only 6.8% of volume. Alternatively, the analysis would benefit from controlling for confounding factors (scope, reassignment, assignee expertise) identified in the augmentation schema to isolate true causal impacts.
