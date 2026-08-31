---
dataset: customer_support_tickets
scenario: focus_inference
variant: original
model: substrate-claude-haiku-4-5
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What are the main kinds of issues these support tickets are about?"
source_table: augment_table/customer_support_tickets/focus_inference/original.csv
generated_at: 2026-07-26T13:05:33.988866+00:00
wall_seconds: 38.28
---

# Customer Support Tickets: Main Kinds of Issues Analysis

## Overview
This analysis examines 250 customer support tickets to identify the primary categories of issues customers encounter. The tickets span a wide range of priorities (Low to Critical) across multiple support channels (email, chat, phone, in-app).

## Main Categories of Issues

### 1. **Performance & Scalability Issues (High Frequency)**
- Degraded query/search performance (CS-0012, CS-0022, CS-0057, CS-0077, CS-0112, CS-0162, CS-0192, CS-0232, CS-0237)
- Application slowdowns and lag (CS-0042, CS-0082, CS-0087, CS-0117, CS-0122, CS-0182, CS-0212, CS-0217, CS-0247)
- Memory leaks and resource exhaustion (CS-0062, CS-0142, CS-0222)
- Timeout and connection pool issues (CS-0052, CS-0152, CS-0172, CS-0197)

### 2. **Platform Outages & Critical System Failures (Critical Priority)**
- Service unavailability and 500/502 errors (CS-0003, CS-0014, CS-0024, CS-0029, CS-0034, CS-0054, CS-0074, CS-0079, CS-0094, CS-0104, CS-0109, CS-0114, CS-0134, CS-0149, CS-0154, CS-0174, CS-0179, CS-0194, CS-0209, CS-0214, CS-0224, CS-0234, CS-0239, CS-0244, CS-0249)
- Authentication/SSO failures (CS-0009, CS-0019, CS-0047, CS-0084, CS-0097, CS-0139, CS-0159, CS-0164, CS-0199, CS-0204, CS-0207, CS-0224)
- Data loss or inaccessibility (CS-0039, CS-0054, CS-0089, CS-0102, CS-0109, CS-0214, CS-0249)

### 3. **Data Integrity & Billing Issues**
- Duplicate charges and billing discrepancies (CS-0001, CS-0032, CS-0049, CS-0090, CS-0144, CS-0184, CS-0204)
- Invoice and payment errors (CS-0001, CS-0017, CS-0032, CS-0144)
- Data consistency problems (CS-0043, CS-0053, CS-0063, CS-0143)
- Missing or corrupted data (CS-0005, CS-0057, CS-0102, CS-0170, CS-0210)

### 4. **Bug Reports & UI/UX Issues**
- Session & login problems (CS-0002, CS-0020, CS-0040, CS-0047, CS-0080, CS-0100, CS-0113, CS-0120, CS-0130, CS-0160, CS-0200, CS-0207, CS-0230, CS-0240)
- UI rendering glitches (CS-0013, CS-0016, CS-0023, CS-0030, CS-0036, CS-0046, CS-0070, CS-0076, CS-0083, CS-0096, CS-0103, CS-0106, CS-0116, CS-0126, CS-0133, CS-0136, CS-0143, CS-0146, CS-0156, CS-0166, CS-0173, CS-0176, CS-0183, CS-0186, CS-0193, CS-0196, CS-0202, CS-0203, CS-0206, CS-0213, CS-0216, CS-0226, CS-0233, CS-0236, CS-0243, CS-0246)
- Mobile-specific issues (CS-0008, CS-0026, CS-0073, CS-0110, CS-0153, CS-0193, CS-0230, CS-0242)

### 5. **Integration & API Failures**
- Third-party integration failures (CS-0014, CS-0024, CS-0044, CS-0099, CS-0124, CS-0127, CS-0159, CS-0169, CS-0229)
- Webhook delivery issues (CS-0014, CS-0043, CS-0127, CS-0169)
- API call failures and rate limiting (CS-0024, CS-0037, CS-0127, CS-0160, CS-0194, CS-0203, CS-0209)

### 6. **Security & Access Control Issues**
- Permission and visibility problems (CS-0013, CS-0033, CS-0053, CS-0058, CS-0068, CS-0093, CS-0123, CS-0133, CS-0139, CS-0207, CS-0210, CS-0223, CS-0244)
- Authentication configuration errors (CS-0006, CS-0009, CS-0033, CS-0067, CS-0097, CS-0124, CS-0139, CS-0159, CS-0189, CS-0199, CS-0204, CS-0234, CS-0244)
- Data exposure and access issues (CS-0054, CS-0068, CS-0150, CS-0189, CS-0219, CS-0244)

### 7. **Feature Requests & Enhancements (Low Priority)**
- UI/UX improvements (CS-0004, CS-0011, CS-0018, CS-0021, CS-0028, CS-0031, CS-0036, CS-0038, CS-0041, CS-0048, CS-0058, CS-0061, CS-0071, CS-0078, CS-0081, CS-0086, CS-0088, CS-0091, CS-0098, CS-0101, CS-0108, CS-0111, CS-0118, CS-0121, CS-0128, CS-0131, CS-0138, CS-0141, CS-0145, CS-0148, CS-0151, CS-0158, CS-0161, CS-0168, CS-0171, CS-0178, CS-0181, CS-0185, CS-0188, CS-0191, CS-0198, CS-0201, CS-0205, CS-0208, CS-0211, CS-0215, CS-0218, CS-0221, CS-0225, CS-0228, CS-0231, CS-0235, CS-0238, CS-0241, CS-0245, CS-0248)
- Integration enhancements (CS-0018, CS-0028, CS-0128, CS-0148)

### 8. **Configuration & Setup Problems**
- SSO/SAML configuration (CS-0006, CS-0009, CS-0033, CS-0047, CS-0059, CS-0067, CS-0097, CS-0124, CS-0139, CS-0227, CS-0234)
- Workspace settings and metadata (CS-0027, CS-0214)
- Domain and certificate issues (CS-0019, CS-0067, CS-0094, CS-0167)

## Distribution by Priority

| Priority | Estimated Count | Primary Issue Types |
|----------|-----------------|---------------------|
| **Critical** | ~35 | Outages, auth failures, data loss, security breaches |
| **High** | ~80 | Performance, billing, integration failures, SSO issues |
| **Medium** | ~95 | Bugs, UI glitches, config problems, data discrepancies |
| **Low** | ~40 | Feature requests, enhancements, questions |

## Key Patterns

1. **Operational Urgency**: ~40% of tickets (Critical + High) represent urgent production issues requiring immediate attention, primarily system outages and authentication failures.

2. **Quality Issues**: ~38% of tickets (Medium priority) are bug reports indicating product stability concerns, particularly UI/UX glitches and data consistency problems.

3. **Enhancement Requests**: ~16% (Low priority) are feature requests and questions, reflecting customer demand for additional capabilities and clarifications on billing/compliance.

4. **Root Causes**: Common underlying causes include recent deployments, schema/config changes, integration issues, and scaling problems related to workload growth.

## Notable Exceptions

- Several tickets (CS-0089, CS-0109, CS-0119, CS-0164, CS-0199) indicate **process failures** beyond technical issues (e.g., delayed account recovery, missing documentation).
- A small cluster of tickets (CS-0189, CS-0219, CS-0244) indicate **security incidents** requiring incident response escalation.
- A subset of tickets involves **compliance and billing** ambiguity (CS-0015, CS-0025, CS-0035, CS-0045, CS-0055, CS-0065, CS-0075, CS-0085, CS-0095, CS-0105, CS-0115, CS-0135, CS-0145, CS-0155, CS-0165, CS-0175, CS-0185, CS-0205, CS-0215, CS-0225, CS-0235, CS-0245), suggesting documentation and contract clarity gaps.

## Conclusion

The main kinds of issues are: **(1) Critical system outages and authentication failures**, **(2) Performance degradation and scalability problems**, **(3) Data integrity and billing discrepancies**, **(4) UI bugs and user experience inconsistencies**, and **(5) Integration and API failures**. Low-priority feature requests comprise the smallest segment. The distribution suggests a mature SaaS product experiencing both reliability challenges at scale and customer demand for expanded capabilities.
