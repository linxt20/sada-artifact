---
dataset: flag_13
scenario: concept_attribute_operational
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: faceted_decomposition
focus_variable: "operational_burden"
query: "What operational burdens appear in incident descriptions?"
source_table: augment_table/flag_13/concept_attribute_operational/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_13__concept_attribute_operational/analyses/original/analysis.md
wall_seconds: 91.24
---

## Operational burdens in incident descriptions

The dataset shows a **service-restoration workload**, not a help/request workload. The strongest burdens in `short_description` are repeated failures to **connect to or access shared infrastructure**, and this aligns with `category`, `priority`, and `assignment_group`.

### Main burden areas

| Burden area | Evidence from visible columns | Operational implication |
|---|---|---|
| **VPN / remote access** | Top descriptions include `Unable to connect to VPN` (28), `Cannot connect to VPN` (18), `Unable to connect to the VPN` (13), plus many close variants such as office/company VPN access failures | Repeated remote-access disruption; likely steady support load on connectivity operations |
| **Email service availability** | `Email server not responding` (20), `Email server is not responding` (8), `Email client not syncing` (6), `Unable to access email` (6), plus many `down/outage/not working` variants | Messaging reliability is a recurring operational burden, spanning both server-side and client-sync symptoms |
| **Database access/connectivity** | `Unable to access company database` (13), `Unable to access database` (12), `Unable to access the database` (9), `Database connection issue` (8), plus SQL/MySQL/server variants | Core data systems generate repeated access and connection incidents, not isolated one-offs |
| **General network / internet / Wi‑Fi** | `category = Network` is 260/500 (52%); descriptions include unstable internet, Wi‑Fi failures, network drive/internal network access issues | Basic connectivity support is the largest burden area |
| **Server performance / outages** | Descriptions mention `server not responding`, `server outage`, `high CPU usage`, `high latency`, `slowdowns`, `unexpected shutdown` | Burden includes keeping underlying infrastructure available, not just end-user access |
| **Software / device support** | `category = Software` is 73/500; descriptions include update/install failures and application access issues. Hardware is 25/500, mostly printer-related | Secondary burden area; smaller than connectivity/service availability but still recurring |

### Why this reads as an operational burden

- **Incident mix is infrastructure-heavy.** `Network` (260) and `Database` (134) together make up **394/500 incidents (78.8%)**.
- **Severity is high.** `priority` is **391 High + 83 Critical = 474/500 (94.8%)**, which is consistent with production-facing service disruption rather than minor user assistance.
- **Routing matches ops ownership.** `assignment_group` is led by `Network` (287) and `Database` (139). This supports the reading that the burden falls on operational support teams.
- **Critical work is concentrated in core services.** Network has 48 critical tickets and Database 19, so these two categories account for **67/83 critical incidents**.

### Notable secondary patterns

- **Cross-team spillover exists.** Software incidents are split across `Software` (29), `Service Desk` (28), and `Network` (13), suggesting application issues often overlap with infrastructure or access problems.
- **Some hardware work is really connectivity-adjacent.** Hardware has only 25 incidents, but 13 are assigned to `Network`, which fits printer/network-device issues rather than standalone hardware repair.
- **Location-specific burdens appear, but weakly.** A small set of descriptions references floors, buildings, departments, meeting rooms, or offices. These suggest occasional localized outages, but they are not the dominant pattern.

### Important limits and exceptions

- The evidence is based on **short symptom descriptions**, not root-cause notes or business-impact fields. It supports claims about **what operations teams repeatedly respond to**, but not exact downtime cost or staffing effort.
- Description wording is **not normalized**. There are 270 unique `short_description` values across 500 rows, and many are obvious phrasing variants of the same issue. This means exact string counts likely **understate** how concentrated the VPN, email, and database burdens are.
- `Inquiry / Help` is only **8 incidents**, so this dataset does **not** mainly reflect training, how-to support, or low-stakes requests.

### Bottom line

The visible operational burdens are concentrated on **keeping shared enterprise access and infrastructure working**: especially **VPN connectivity, email availability, database access, and general network/Wi‑Fi/internet stability**. Smaller but real burdens appear in **server performance/outages, software updates/installations, and printer/device support**. The evidence is strong for recurring operational disruption, but weaker for claiming specific root causes or business impact beyond those symptoms.
