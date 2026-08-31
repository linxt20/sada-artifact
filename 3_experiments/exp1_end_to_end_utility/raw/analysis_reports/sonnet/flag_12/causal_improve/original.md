---
dataset: flag_12
scenario: causal_improve
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: what_if
focus_variable: "incident_resolution_efficiency"
query: "How can we improve incident resolution efficiency?"
source_table: augment_table/flag_12/causal_improve/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_12__causal_improve/analyses/original/analysis.md
wall_seconds: 84.95
---

# Incident resolution efficiency analysis

## Focus variable
Resolution time was derived from the visible timestamp columns as $closed\_at - opened\_at$ for 500 incidents.

- Median resolution time: **173.2 hours** (~7.2 days)
- Mean resolution time: **178.4 hours**
- 75th percentile: **252.7 hours** (~10.5 days)
- 95th percentile: **375.3 hours** (~15.6 days)

The main opportunity is to reduce the long tail of slow incidents, not the already-fast cases.

## What the data suggests

### 1. Improve the Hardware workflow first
- **Hardware** is **406/500 incidents (81.2%)**.
- It is also slower than several smaller categories:
  - Hardware: **181.4h**
  - Inquiry / Help: **182.1h** *(similar, but only 20 cases)*
  - Database: **172.4h**
  - Network: **161.6h**
  - Software: **153.6h**
- `assignment_group` almost perfectly matches `category` already, so the main issue does **not** appear to be routing. It is more likely queue throughput, standardization, or capacity inside Hardware.

### 2. Reduce Friday/weekend handoff delay
Mean resolution time is lower for tickets opened earlier in the workweek and higher near the weekend:

- Monday: **163.8h**
- Wednesday: **168.2h**
- Friday: **195.7h**
- Saturday: **189.7h**

This pattern is consistent with backlog buildup or weaker handoffs across Friday/weekend periods.

### 3. Standardize assignee practices and balance load
Resolution time varies materially by `assigned_to`:

- Fred Luddy: **165.0h**
- Beth Anglin: **172.4h**
- Howard Johnson: **175.5h**
- Charlie Whitherspoon: **178.8h**
- Luke Wilson: **195.5h**

The spread between fastest and slowest assignees is about **30.5 hours**. That supports reviewing workload mix, queue assignment, and repeatable handling practices.

### 4. Tighten prioritization inside the very large “High” queue
Priority distribution is heavily concentrated in `2 - High`:

- `2 - High`: **394**
- `3 - Moderate`: **77**
- `1 - Critical`: **27**
- `4 - Low`: **2**

Resolution times are not very separated between High and Moderate:

- Critical: **167.0h**
- High: **180.0h**
- Moderate: **177.8h**

If most tickets are marked High, priority may not be creating enough operational separation for faster handling.

### 5. Actively manage aging tickets
The slowest incidents reach **428-514 hours**, and the top slow cases are mostly Hardware incidents. A visible aging trigger would likely help more than focusing only on average performance.

## Recommended actions

1. **Run a Hardware-focused improvement sprint**
   - standard troubleshooting playbooks,
   - spare-parts/access readiness,
   - daily review of aging Hardware tickets,
   - faster escalation for unresolved desktop/printer/device issues.

2. **Add end-of-week backlog controls**
   - Friday triage sweep,
   - explicit weekend ownership/handoff,
   - Monday review of tickets older than 5-7 days.

3. **Standardize and rebalance assignee workflows**
   - compare handling steps used by faster assignees,
   - spread heavy queues more evenly,
   - monitor aging by assignee, not only ticket count.

4. **Improve triage discipline**
   - reduce overuse of `2 - High`,
   - use aging or customer-impact rules to escalate stalled tickets earlier.

## Important limits
- Category-to-group routing is already very clean, so the data does **not** support routing errors as the main bottleneck.
- Assignee differences may partly reflect case mix; the table does not include complexity, reopen rate, or dependency/parts delays.
- Evidence is weaker for small groups such as Low priority and the smaller non-Hardware categories.
