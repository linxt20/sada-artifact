---
dataset: flag_13
scenario: focus_inference
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's worth attention in these incident descriptions."
source_table: augment_table/flag_13/focus_inference/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:12:37.840459+00:00
wall_seconds: 97.64
---

# Incident Description Analysis: Focus Inference Report
**Dataset:** haiku__skill_off_update (500 incidents, Jan 2023 – Jan 2024)  
**Variant:** skill_off  
**Query:** Help me understand what's worth attention in these incident descriptions.

---

## Executive Summary

Analysis of incident descriptions reveals that **priority level and service type are the strongest predictors of attention-worthiness**, with critical outages—particularly in Email and Database services—commanding highest scrutiny. The dataset shows clear stratification by urgency and business impact: Critical incidents average attention scores of **4.51/5**, while High-priority issues score **2.68/5**. Network connectivity and data access problems dominate (78% of incidents), signaling infrastructure as a key risk area.

---

## Key Patterns Worth Attention

### 1. **Priority Level as Primary Attention Driver**
- **Critical (1):** 83 incidents (16.6% of total) → Average attention: **4.51/5**  
  - 52 contain explicit outage signals (62.7%)
  - Descriptions emphasize total service loss: *"down," "outage," "unable," "server not responding"*
  
- **High (2):** 391 incidents (78.2% of total) → Average attention: **2.68/5**  
  - Mixed impact: connectivity failures, access issues, performance degradation
  - Descriptions reflect partial or intermittent failures
  
- **Moderate/Low (≤3):** 26 incidents (5.2% of total) → Average attention: **1.18/5**  
  - Localized issues: printer malfunctions, software updates, single workstation problems

**Implication:** Priority field is a strong but *incomplete* filter. Some High-priority incidents achieve attention scores of 5, indicating additional contextual factors drive severity beyond formal priority assignment.

---

### 2. **Affected Service Distribution and Attention Patterns**

| Service Type | Count | % of Total | Avg Attention | Notable Pattern |
|---|---|---|---|---|
| **Email** | 131 | 26.2% | **3.46** | Highest individual service attention; server outages/responsiveness emphasized |
| **Database** | 128 | 25.6% | **3.17** | Connectivity & access failures; production environment mentions amplify concern |
| **VPN** | 108 | 21.6% | **2.99** | Consistent connectivity friction; lower variance in attention |
| **Network (WiFi/Connectivity)** | 71 | 14.2% | **2.51** | Floor/location-specific issues scored lower |
| **Other/Software/Printer** | 62 | 12.4% | **1.52–1.60** | Low attention; non-critical services |

**Evidence:** Email and Database services, which directly block business-critical workflows, receive elevated attention despite sometimes identical descriptions to lower-attention issues. Example: *"Email server outage"* scores 5 when Critical priority; scores 2–3 when High priority or flagged as Software category.

---

### 3. **Outage Signals and Scope Language**

Incidents explicitly mentioning outage characteristics receive higher attention:

- **High-attention language patterns:**
  - Total failure: *"server down," "unable to access," "outage," "not responding," "crash"*
  - Urgency/breadth: *"org-wide," "all users," "entire," "production,"* location specifics (e.g., *"building 123,"* *"5th floor"*)
  - Explicit impact: *"service disruption," "connectivity failure"*

- **Lower-attention patterns:**
  - Partial/intermittent: *"unstable," "slow," "issues with," "need assistance"*
  - Localized/singular: *"workstation," "printer,"* single-user problems

**Quantitative evidence:** 52 of 83 Critical incidents (62.7%) include `contains_outage_signal=1`. However, 37% of Critical incidents do *not* trigger outage detection, suggesting descriptions sometimes downplay severity or use passive language.

---

### 4. **Category vs. Issue Type Mismatches**

A notable weak signal: **Category and Issue Type do not always align**, and the mismatch correlates with attention variance:

- Email issues categorized as *Hardware* (vs. Network) or *Software* (vs. Network):  
  Example: *"Email server not responding"* with `category=Hardware, issue_type=Email`  
  → Attention scores: 0–4 (high variance)

- Database issues with `category=Hardware` or `category=Software`:  
  → Attention typically **1–2** (deprioritized despite potential severity)

**Implication:** Misclassification or ambiguous categorization *reduces* attention scoring, suggesting that clear, explicit service identification in descriptions is critical for proper triage.

---

### 5. **Severity Intensity Markers**

Descriptions flagged with `has_critical_keyword=1` (n=22 incidents) average attention **3.95/5**, vs. **2.81/5** for those without. However, critical keywords are present in only 4.4% of incidents—many high-severity issues rely on *implicit* severity cues:

- Database issues with "production" or "server" language → Higher attention
- VPN/connectivity with "unable" + "connect" + specific scope (vs. generic "connection issue") → Higher attention
- Email with "down" or "outage" + Critical priority → Attention = 5

---

### 6. **Notable Exceptions and Weak Evidence**

**Weak evidence:**
- Attention score 0–1 assigned to 53 incidents (10.6%), mostly in Moderate/Low priority or Hardware/Printer categories. These suggest **baseline attention floor**, not true non-issues.
- VPN connectivity issues are consistently lower-attention (avg 2.99) despite high frequency (21.6% of dataset), implying **user expectation of intermittent VPN friction** or routing to specialized team.
- Some High-priority Software category incidents (e.g., *"software update required"*) score 1–2, indicating **category can override priority** in attention calculation.

---

## Decision-Ready Insights

### For Triage and Routing:
1. **Prioritize incidents where:**
   - Priority = Critical **AND** (Service is Email or Database)
   - Descriptions contain: *"outage," "down," "unable to access,"* with explicit scope (*"all,"* *"org-wide,"* *"production"*)
   
2. **Escalate automatically if:**
   - Priority = Critical **AND** `contains_outage_signal = 1`
   - Or: Database/Email + Critical + production/organization-wide scope language

3. **Routine handling if:**
   - Priority = High + single issue type (VPN, Network, Printer, Software update)
   - Descriptions use qualifier language: *"unable," "unstable," "issues with"* (vs. absolute failure)

### For Incident Description Standardization:
- Require explicit service identification (not category ambiguity)
- Encode scope breadth in description: *"unable to access"* → include whether user, floor, building, or org-wide
- Avoid passive/deflection language for Critical priority incidents; favor active failure states

### Coverage Limitations:
- 37% of Critical incidents lack outage signal detection, suggesting descriptions sometimes use indirect language
- Network category issues (52% of dataset) show lower attention despite high frequency—may indicate either well-managed baseline or insufficient escalation of widespread connectivity issues

---

## Conclusion

**In incident descriptions, what's worth attention boils down to:**

1. **Explicit priority assignment** (Critical >> High >> Moderate)
2. **Service criticality** (Email, Database >> VPN, Network >> Others)
3. **Failure mode clarity** (total outage/down >> partial/intermittent >> localized)
4. **Scope breadth** (org-wide/production >> floor/department >> workstation)
5. **Keyword precision** (industry terms like "outage," "production" elevate; vague "issues" reduce)

The `attention_score` column itself reflects a compound signal: it is *not* deterministic from priority alone, but strongly weighted by service type and failure language. Incidents that are Critical *AND* Email/Database *AND* contain outage language reliably score 4–5. Misclassifications, passive descriptions, and low-severity services reliably score 1–2 despite sometimes matching High priority.

**Actionable recommendation:** Use this report to calibrate incident routing rules and description templates to improve triage efficiency and reduce false negatives in critical service outages.
