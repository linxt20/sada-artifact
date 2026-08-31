---
dataset: flag_9
scenario: concept_attribute_hardware
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: faceted_decomposition
focus_variable: "hardware_hiccups"
query: "What kinds of hardware issues appear in these incidents?"
source_table: augment_table/flag_9/concept_attribute_hardware/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:20:44.750693+00:00
wall_seconds: 58.35
---

# Hardware Issues in Incidents — Analysis Report

**Query:** What kinds of hardware issues appear in these incidents?

---

## Method Note

TAPP-generated column used: **`hardware_scope`** — a semantic facet classifying each incident's hardware involvement into one of four scopes (`individual_device`, `shared_office_device`, `server_infrastructure`, `network_infrastructure`) or `Unknown`. This column adds sub-category granularity within and beyond the structured `category` field.

---

## 1. Dataset Overview

| Metric | Value |
|---|---|
| Total incidents | 600 |
| Incidents with `category = Hardware` | 182 (30.3%) |
| Incidents with a non-Unknown `hardware_scope` | 367 (61.2%) |

The structured `category` column captures 182 explicitly labelled hardware tickets. The `hardware_scope` column extends coverage to 367 incidents by also tagging hardware-touched incidents filed under Database (102), Network (78), and a handful of other categories — reflecting that many infrastructure problems have a hardware dimension even if categorised differently.

---

## 2. Hardware Issue Types

Four distinct hardware scope types emerge from `hardware_scope`, cross-validated against `category` and `short_description`:

| `hardware_scope` | Count | Primary `category` | Representative descriptions |
|---|---|---|---|
| **individual_device** | 90 | Hardware (88), Software (2) | Keyboard keys sticking/malfunctioning, desktop not powering on, laptop unable to boot, monitor issues |
| **shared_office_device** | 83 | Hardware (83) | Printer not working/responding/functioning, shared peripheral failures |
| **server_infrastructure** | 115 | Database (102), Hardware (10), Software/Network (3) | Unable to connect to MySQL/database, SQL Server outage, database access failures linked to server hardware |
| **network_infrastructure** | 79 | Network (77), Hardware (1), Inquiry (1) | VPN connectivity issues, LAN connection failures, unstable internet, network device problems |

**Key finding:** Hardware issues fall into four categories — personal endpoint devices (~25% of hardware-scoped incidents), shared peripherals (~23%), server/database backend infrastructure (~31%), and network infrastructure (~22%).

---

## 3. Severity Profile by Hardware Type

Higher-severity issues cluster in server and network infrastructure:

| `hardware_scope` | 1 - Critical | 2 - High | 3 - Moderate | Total | % Critical |
|---|---|---|---|---|---|
| server_infrastructure | 26 | 84 | 5 | 115 | **22.6%** |
| network_infrastructure | 15 | 61 | 3 | 79 | **19.0%** |
| individual_device | 11 | 67 | 12 | 90 | 12.2% |
| shared_office_device | 1 | 73 | 9 | 83 | 1.2% |

Server infrastructure generates the most Critical-priority tickets (26), reflecting the cascading impact of database/server hardware failures. Shared office device issues (primarily printers) are almost never Critical (1/83 = 1.2%).

---

## 4. Resolution Time by Hardware Type

| `hardware_scope` | Median Resolution (hours) |
|---|---|
| shared_office_device | 146.7 |
| server_infrastructure | 161.1 |
| network_infrastructure | 174.0 |
| individual_device | 200.6 |

Individual device issues take the longest to resolve (median ~201 hours), despite lower criticality, possibly due to logistics of physical device repair/replacement. Network infrastructure tickets resolve faster than might be expected given their higher criticality rate.

---

## 5. Assignment Groups

| Assignment Group | Count (hardware-scoped) |
|---|---|
| Hardware | 182 |
| Database | 103 |
| Network | 78 |
| Service Desk | 2 |
| Software | 2 |

Assignment group aligns closely with `hardware_scope`, validating the TAPP classification: server infrastructure tickets route to Database (102/115 = 89%), network infrastructure tickets route to Network (78/79 = 99%), and individual/shared device tickets route to Hardware.

---

## 6. Summary

The incidents reveal **four hardware issue types**:

1. **Individual endpoint device failures** (90 incidents) — keyboard, desktop, laptop hardware faults; longest resolution time (~201 hrs median).
2. **Shared office peripheral failures** (83 incidents) — predominantly printer malfunctions; lowest severity, fastest resolution (~147 hrs).
3. **Server/database infrastructure failures** (115 incidents) — hardware underpinning database outages; highest absolute count of Critical tickets (26); routed to Database team.
4. **Network device/connectivity failures** (79 incidents) — VPN, LAN, internet hardware; high criticality rate (19%); routed to Network team.

The `hardware_scope` facet adds meaningful signal beyond the raw `category` column by revealing that ~51% of hardware-scoped incidents (server + network, 194/367) are categorised under Database or Network rather than Hardware, and would be missed in a category-only analysis.
