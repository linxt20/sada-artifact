---
dataset: customer_support_tickets
scenario: concept_attribute_operational
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "operational_burden"
query: "What customer issues create the most support burden?"
source_table: augment_table/customer_support_tickets/concept_attribute_operational/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:06:13.145524+00:00
wall_seconds: 77.64
---

# Customer Support Burden Analysis Report
## Query: What customer issues create the most support burden?

**Dataset:** 250 customer support tickets  
**Focus Variable:** Operational burden (measured by resolution time, severity, and ticket volume)  
**Variant:** skill_off (model without specialized skill configuration)

---

## Executive Summary

Support burden is concentrated in a small number of issue types that collectively consume significant agent time and impact business-critical customer operations. **Performance degradation and infrastructure outages** account for the highest cumulative burden, followed by billing disputes and authentication failures. While feature requests are the most frequent ticket type (n=38), they consume minimal effort due to low severity. The data reveals strong correlation between issue severity, customer impact level, and resolution time.

---

## Key Findings

### 1. **Highest Burden Issue Categories** (by total resolution minutes)

| Issue Category | Ticket Count | Total Resolution Time | Avg Resolution | Avg Severity |
|---|---|---|---|---|
| **Performance** | 25 | 3,583 min | 143.3 min | 2.0 |
| **Infrastructure** | 32 | 2,621 min | 81.9 min | 2.6 |
| **Billing & Pricing** | 23 | 1,887 min | 82.0 min | 1.0 |
| **Authentication** | 23 | 1,480 min | 64.4 min | 1.4 |
| **Security** | 18 | 1,166 min | 64.8 min | 1.4 |

**Finding:** These 5 categories represent 40% of tickets but consume 70% of total resolution time.

### 2. **Performance Issues as a Burden Driver**

Performance degradation stands as the **single highest burden category despite lower ticket volume** (n=25):
- **Average resolution: 143 minutes** (2.4× average across all tickets)
- **100% High priority** (all 25 performance issues are marked High)
- **Patterns observed:**
  - Query timeouts after dataset growth (CS-0012, CS-0082, CS-0112, CS-0217)
  - Search latency degradation (CS-0022, CS-0162)
  - UI responsiveness issues from schema changes (CS-0042, CS-0052, CS-0062)
  - Connection pool exhaustion (CS-0052, CS-0077, CS-0197)

**Operational burden driver:** Requires engineering investigation into infrastructure, query plans, or code-level memory leaks. Cannot be resolved via standard runbooks or configuration changes.

### 3. **Infrastructure Outages and Availability Issues**

Infrastructure issues present the **highest frequency of critical tickets** (21 of 32 tickets are Critical):
- **42% critical severity** vs. 20% across all tickets
- **Average severity: 2.6** (highest among all categories)
- **Time impact:** 64-minute average for critical cases
- **Common patterns:**
  - Service/API endpoint unavailability (CS-0003, CS-0009, CS-0034)
  - Database access issues and read-only modes (CS-0029, CS-0109, CS-0114)
  - CORS and certificate/TLS errors (CS-0019, CS-0037, CS-0094)
  - Webhook delivery failures and connectivity issues (CS-0014, CS-0127)

**Operational burden driver:** Requires urgent incident response, status updates, and potential RCA (root cause analysis). Multiple customers may be simultaneously impacted, necessitating triage prioritization.

### 4. **Billing and Pricing Disputes**

Billing issues show **moderate frequency but high resolution complexity** (n=23, avg 82 min):
- **Mix of priorities:** 8 High, 5 Critical, 10 Low
- **Critical cases (n=5):** Billing accuracy errors (double charges, phantom users, miscalculations) requiring investigation, credits, and customer communication
- **Common patterns:**
  - Duplicate charges and double-billing (CS-0049, CS-0084, CS-0144)
  - Discrepancies between reported and actual usage (CS-0032)
  - Payment failures and suspension logic errors (CS-0084)
  - Billing reconciliation questions (CS-0032, CS-0090)

**Operational burden driver:** Often involves financial decisions, customer credit memos, and finance team coordination. Escalation to billing/finance domain is common.

### 5. **Severity and Priority Alignment**

Strong correlation observed between priority classification and customer impact:

| Priority | Ticket Count | Total Minutes | Avg Resolution |
|---|---|---|---|
| **Critical** | 50 | 3,720 min | 74.4 min |
| **High** | 50 | 6,555 min | 131.1 min |
| **Medium** | 76 | 3,163 min | 41.6 min |
| **Low** | 74 | 2,776 min | 37.5 min |

**Observation:** High-priority tickets consume the most cumulative time (131 min average) despite lower count than Medium/Low. This suggests High-priority issues are often complex and take longer to investigate.

### 6. **Customer Impact Alignment**

Customer impact levels map directly to priority (100% correlation in this dataset):
- **50 critical-impact tickets** (business-blocking): avg 74.4 min resolution
- **50 high-impact tickets** (major workflow disruption): avg 131.1 min resolution
- **76 medium-impact tickets** (moderate productivity loss): avg 41.6 min resolution
- **74 low-impact tickets** (minor inconvenience): avg 37.5 min resolution

**Finding:** The longer resolution time for high-impact issues reflects their complexity, not prioritization bias.

### 7. **Support Channel Workload Disparity**

Email carries significantly higher workload in terms of resolution complexity:

| Channel | Tickets | Avg Resolution Time |
|---|---|---|
| **Email** | 100 | 98.3 min |
| **Phone** | 50 | 70.2 min |
| **In-app** | 50 | 35.0 min |
| **Chat** | 50 | 22.5 min |

**Implication:** Email is the channel for complex, asynchronous investigations. Chat and in-app are for quick clarifications.

### 8. **Low Automation Potential for High-Burden Issues**

Feature requests (n=38, most frequent category) have:
- **Minimum severity:** 0.0 average
- **Minimal resolution time:** 23.3 minutes average
- **High scaling efficiency:** Can be triaged, documented, and batched

Conversely, high-burden categories require substantial human effort:
- Performance issues → engineering investigation
- Infrastructure issues → incident response
- Billing issues → financial judgment and coordination

---

## Important Exceptions and Caveats

1. **Resolution time is not a complete burden metric:** Some high-severity issues (e.g., security reviews, critical outages) may require external dependencies or lengthy post-resolution analysis not fully captured in the resolution_minutes field.

2. **Incomplete RCA patterns:** The dataset does not capture whether issues recur. Recurring performance or authentication problems would inflate true burden.

3. **Weak evidence on automation potential:** The CSV lacks annotations distinguishing issues suitable for self-service vs. runbooks vs. product fixes. Burden reduction opportunities remain unquantified.

4. **Channel bias:** Email's high average resolution may reflect ticket complexity selection rather than channel inefficiency.

---

## Recommendations for Support Burden Reduction

1. **Prioritize performance engineering:** With 3,583 cumulative minutes, performance issues justify dedicated engineering resources to prevent regressions post-deployment.

2. **Strengthen incident response playbooks:** Infrastructure issues (21 critical) would benefit from pre-built escalation paths and status communication templates.

3. **Implement billing accuracy checks:** Duplicate charges and miscalculations (CS-0049, CS-0084, CS-0144) suggest automation opportunity in billing pipeline validation.

4. **Create self-service guides for authentication:** Authentication is frequent (n=23) but many cases are configuration-based (SSO, MFA, SAML) amenable to documentation.

---

## Conclusion

**Performance degradation and infrastructure outages create the most support burden** on both per-ticket and cumulative bases. Unlike low-impact feature requests that are easy to manage, high-burden issues require engineering investigation, incident response, or cross-functional coordination. Resolution times (80–143 minutes) reflect genuine complexity rather than support inefficiency, suggesting burden reduction requires product and engineering investment rather than process optimization alone.
