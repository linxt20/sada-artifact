---
dataset: flag_19
scenario: concept_attribute_declined
variant: original
model: substrate-claude-haiku-4-5
query_subtype: faceted_decomposition
focus_variable: "declined_expense_reasons"
query: "What reasons or compliance risks appear in declined expenses?"
source_table: augment_table/flag_19/concept_attribute_declined/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_19__concept_attribute_declined/analyses/original/analysis.md
wall_seconds: 73.87
---

# Analysis: reasons and compliance risks in declined expenses

## Main patterns
- There are **46 declined rows out of 500 total**.
- Declines are concentrated in **asset-like expenses**:
  - **Assets:** 27 declined out of 310 total
  - **Travel:** 10 declined out of 94 total
  - **Services:** 6 declined out of 79 total
  - **Miscellaneous:** 3 declined out of 17 total
- The strongest departmental concentration is **IT**:
  - **IT:** 19 declined out of 43 total
  - **Customer Support:** 16 declined out of 267 total
  - **Sales:** 6 declined out of 122 total

## Apparent reasons or compliance risks

### 1. Asset procurement appears to be entering the expense workflow
Most declined rows are in `category = Assets`, and their `short_description` and `ci` fields read like hardware procurement or asset-registration records rather than ordinary employee expenses.

Examples include:
- `Dell Precision WorkStation T3620`
- `Dell OptiPlex 7080`
- `Surface Pro 7 - Asset Purchase`
- `Lenovo ThinkPad T480`
- `Dell Latitude 7390 Laptop Asset`

This pattern suggests a **policy mismatch**: capital equipment or managed hardware may have been submitted through an expense process instead of a procurement or asset-management process. That creates likely compliance risks around:
- bypassing purchasing controls,
- duplicate asset/payment records,
- incomplete capitalization or inventory handling.

### 2. Missing source references are common in declined travel and miscellaneous rows
`source_id` is missing in **13 of 46 declined rows**. More importantly, the missingness is not random:
- **all 10 declined Travel rows** have blank `source_id`
- **all 3 declined Miscellaneous rows** have blank `source_id`

Examples include:
- `Business Class Airline Ticket`
- `Travel Backpack PRO`
- `Pocket WiFi 4G`
- `Meeting Room Projector`

This points to a likely **documentation or audit-trail weakness**. If `source_id` is the originating request or linked record, these declines may reflect missing approval linkage, weak substantiation, or off-workflow submissions.

### 3. Many declined entries look system-generated
Several declined `short_description` values include phrases such as:
- `Automatically generated asset...`
- `Automatically generated expense line...`
- `Automatically registered asset...`
- `Automatically created service asset`

This suggests a possible compliance issue where **system-created lines** entered the approval process without enough business justification, correct categorization, or human verification. It may also indicate duplicate or workflow-generated records.

This is only **suggestive**, not conclusive, because similar auto-generated wording also appears in non-declined rows.

### 4. IT-related service spend may require stricter preapproval
Declined service rows include items such as:
- `Oracle Database 12c Enterprise`
- `SQL Server 2019`
- `Web Hosting Service 1`
- `Web Server Service`
- `AWS EC2 Instance`

Combined with the very high IT decline concentration, this suggests **IT infrastructure and software/service expenses** may face extra compliance requirements, such as procurement review, licensing controls, or manager/preapproval gates that ordinary expense submissions do not satisfy.

## What does **not** look like the main reason
- **Amount alone is not a strong explanation.**
  - Declined amounts range from **258** to **8817**
  - The declined average is **lower** than the non-declined average
- Both low-cost and high-cost items are declined, so the visible pattern is more about **expense type, workflow fit, and documentation** than size.

## Exceptions and limits
- The table has **no explicit denial-reason field**, receipt flag, or policy code.
- The analysis therefore identifies **likely reasons/risk patterns**, not proven causes for each individual decline.
- Customer Support has many declined rows in raw count, but that department also has the largest overall volume. The clearest overrepresentation is still **IT**.

## Decision-ready takeaway
Declined expenses appear to be driven mainly by **policy-fit and documentation issues**, especially:
1. **hardware/asset purchases submitted as expenses**,
2. **travel or miscellaneous entries lacking `source_id` traceability**,
3. **IT service/infrastructure spend that likely needs a different approval path**, and
4. **system-generated lines that may not carry sufficient business justification**.

The highest-value control checks would be:
- tighten routing for **asset and IT procurement**,
- require valid `source_id` or equivalent reference for **travel/miscellaneous** submissions,
- review auto-generated expense lines before they reach final approval.
