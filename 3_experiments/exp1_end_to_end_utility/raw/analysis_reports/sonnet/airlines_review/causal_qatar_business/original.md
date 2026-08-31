---
dataset: airlines_review
scenario: causal_qatar_business
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: causal_attribution
focus_variable: "non_recommendation_outcome"
query: "Explain why some Qatar Airways Business-Class flights receive a non-recommended (Recommended = no) result."
source_table: augment_table/airlines_review/causal_qatar_business/original.csv
source_report: dataset_portion_2/substrate-claude-sonnet-4-6/airlines_review__causal_qatar_business/analyses/original/analysis.md
wall_seconds: 102.48
---

# Why Some Qatar Airways Business-Class Flights Receive a Non-Recommended Result

## 1. Overview

The dataset contains passenger reviews of Qatar Airways Business Class flights. The target variable `Recommended` is binary (`yes`/`no`). Despite Qatar Airways being widely praised as a world-class carrier, a meaningful minority of Business-Class reviews result in a **"no"** recommendation. Based on a systematic review of all visible columns — `Seat Comfort`, `Staff Service`, `Food & Beverages`, `Inflight Entertainment`, `Value For Money`, `Overall Rating`, and the free-text `Reviews` — five recurring causal clusters emerge.

---

## 2. Primary Causal Drivers of Non-Recommendation

### 2.1 Poor Customer Service & Unresolved Compensation Disputes (Strongest Driver)

The single most common reason for a "no" recommendation is a **failure of ground/post-flight customer service**, often triggered by an operational problem that the airline then fails to resolve fairly.

| Row | Issue | Value For Money | Overall Rating |
|-----|-------|-----------------|----------------|
| Row 22 | 17-hr rebooking delay, generic refusal to compensate | 1 | 1 |
| Row 6 | Lost bag, no reimbursement after months | 3 | 4 |
| Row 105 | Promised refund never paid, calls hung up | 1 | 1 |
| Row 111 | Paid seats not provided on two trips; 6-month refund chase | 1 | 1 |
| Row 202 | COVID vouchers not processed for 18 months | 1 | 1 |
| Row 89 | Ground staff treated business booking unprofessionally; complaint ignored | 1 | 1 |
| Row 196 | Rigid flight-change rules, charged €1,500 for a Doha–Riyadh change | 1 | 1 |
| Row 231 | Bonus miles denied after COVID-cancelled rebooking | 1 | 1 |

**Pattern:** `Value For Money` scores of **1** and `Overall Rating` of **1** appear almost exclusively in reviews where a dispute arose post-flight and was not resolved. In-flight scores (Seat Comfort, Staff Service, Food) are often **4–5** in the same reviews, indicating that the onboard product was acceptable but ground/customer-service failures were decisive. Reviews explicitly cite ignored emails, call-center hold times exceeding 1.5 hours, and generic replies.

---

### 2.2 Aircraft Downgrade (QSuite Promised, Legacy Seat Delivered)

A high-frequency structural complaint is being placed on an older aircraft — particularly a legacy **2-2-2 Boeing 777** — after booking a QSuite product.

| Row | Situation | Seat Comfort | Value For Money | Overall Rating |
|-----|-----------|-------------|-----------------|----------------|
| Row 15 | Aircraft changed to old 777, QSuite removed; refund ignored | 5 | 1 | 1 |
| Row 28 | Doha–Jakarta downgraded to non-QSuite 4 weeks before flight | 3 | 1 | 4 |
| Row 31 | Athens–Doha changed to non-QSuite; $989 seat-selection fee dispute | 4 | 3 | 2 |
| Row 46 | Downgraded twice; Doha-Zurich informed only 6 hours before departure | 2 | 1 | 3 |
| Row 61 | Ancient 2-2-2 instead of QSuite, seat comfort suffered | 4 | 2 | 2 |
| Row 258 | LA–Male: downgraded to non-QSuite, no notification, no compensation offered | 5 | 2 | 4 |
| Row 268 | LHR–BAN, DOH–Gatwick: no QSuite, no orange juice; price identical | 5 | 3 | 3 |
| Row 274 | HKG–Doha: expected QSuite, got 777 2-2-2; no prior notice | 4 | 1 | 3 |
| Row 276 | DOH–HKG: QSuite advertised, aged 2-2-2 delivered; no notification | 3 | 2 | 2 |
| Row 277 | DOH–BKK 2-2-2: "is this the world's best business class?" | 1 | 3 | 6 |

**Pattern:** `Value For Money` collapses to **1–3** whenever passengers pay a QSuite premium but receive a legacy seat. `Seat Comfort` scores split: passengers who still received a lie-flat seat rate comfort at 4–5, but those on older angled beds or 2-2-2 configurations rate it 1–3. These reviews consistently invoke "unacceptable" value and the absence of any notification or compensation.

---

### 2.3 Operational Failures with No Adequate Support (Missed Connections, Long Delays, Lost Baggage)

Operational disruptions alone rarely cause a "no" if the airline manages recovery well. Non-recommendation arises when **recovery is absent or perceived as inadequate**.

| Row | Failure | Resolution Offered | Overall Rating |
|-----|---------|--------------------|----------------|
| Row 45 | Missed connection, rerouted 7.5 hrs later, hotel refused | 0 – none | 2 |
| Row 112 | Missed connection, 20 hrs in Doha, economy rebook | Token offer | 1 |
| Row 134 | Bags lost at Doha; no response via WhatsApp or live chat | 0 | 3 |
| Row 135 | >24-hr delay in Doha, no visa guidance, economy-only seats for family | Budget hotel | 1 |
| Row 68 | 3-hr delay → missed connection; airline denied compensation | 0 | 5 |
| Row 243 | 13-hr delay; complaint ignored for weeks | 0 | 5 |
| Row 180 | Flight cancelled 9 days into holiday; bags lost day one | Refund only | 2 |

---

### 2.4 Low Staff Service Scores

Several "no" reviews cite **disengaged or aggressive cabin crew** as the proximate cause. Unlike the onboard-product drivers above, these cases do not involve aircraft downgrades; the failure is purely in-flight service quality.

| Row | Specific Complaint | Staff Service | Overall Rating |
|-----|-------------------|---------------|----------------|
| Row 17 | Crew ignored passenger, no refills, no greeting/goodbye | 1 | 3 |
| Row 47 | IFE didn't work; ground staff bad in NYC | 1 | 1 |
| Row 155 | Service slowed dramatically once airborne; crew unresponsive | 5 | 4 |
| Row 171 | Food portions tiny, FA told passenger off for using a washroom | 4 | 1 |
| Row 172 | Food poor, wrong lounge directed, business lounge closed | 5 | 1 |

**Pattern:** A `Staff Service` score of **1** combined with `Food & Beverages` ≤ 2 strongly predicts "no." Exceptions exist (Row 8 has Staff=1 but is "yes"), suggesting that staff failure alone is tolerated if other dimensions compensate.

---

### 2.5 Low Value for Money (Price-Product Mismatch)

Even where individual sub-scores are moderate, a `Value For Money` score of **1** is nearly always associated with "no" regardless of other scores. This captures cases where passengers feel the **price paid was unjustified by the experience received** (especially when a premium was paid for QSuite or a specific experience that was not delivered).

- Row 60: Seat changed without notice — VFM=1, Overall=2, Recommended=**no**
- Row 81: Air Canada downgrade on a Qatar-sold business ticket — VFM=3, Overall=6, Recommended=**no**
- Row 129: Flight changed multiple times, QSuite removed — VFM=3, Overall=2, Recommended=**no**
- Row 230: Buy-up upgrade excluded lounge access (hidden in fine print) — VFM=1, Overall=2, Recommended=**no**

---

## 3. Score Thresholds Separating "No" from "Yes"

Aggregating across all non-recommended reviews:

| Metric | Typical "no" range | Typical "yes" range |
|--------|-------------------|---------------------|
| Overall Rating | **1–4** (majority ≤ 3) | **7–10** |
| Value For Money | **1–3** (almost always ≤ 3) | **3–5** |
| Staff Service | Often **1–3**; can be 5 if other factors dominate | **3–5** |
| Seat Comfort | Wide range (1–5); less predictive alone | 3–5 |
| Food & Beverages | Often ≤ 3 when co-occurring with other issues | 3–5 |

`Value For Money = 1` is the single most reliable column-level predictor of "no." `Overall Rating ≤ 3` follows closely.

---

## 4. Notable Exceptions and Weak Evidence

- **High-scoring "no" reviews exist**: Row 38 (VFM=3, Overall=7, no), Row 38 reviewer explicitly says the product was "very good" but does not recommend — possibly a quirk in labelling or threshold.
- **Staff Service = 5 + Recommended = "no"**: Multiple cases (Rows 89, 111, 202) where in-flight staff were praised but ground failures were decisive. Staff service alone cannot prevent a "no."
- **Some aircraft-downgrade reviews are "yes"**: If the alternative seat was still lie-flat (e.g., non-QSuite 787 with 1-2-1), passengers often still recommended — the product gap matters more than the label.
- **Verified vs. unverified**: Most "no" reviews are by verified passengers (`Verified = True`), suggesting these are genuine experiences rather than outliers.

---

## 5. Causal Summary

```
Non-recommendation in Qatar Airways Business Class is driven by a hierarchy of failures:

1. Customer-service failures post-flight (refund refused, complaint ignored) 
   → Value For Money = 1, Overall Rating = 1 → Recommended = no

2. Aircraft downgrade from QSuite to legacy seat without notice/compensation 
   → Value For Money ≤ 2, seat comfort drops 
   → Recommended = no

3. Operational disruption (delay/cancellation/lost bags) with inadequate recovery 
   → Overall Rating collapses 
   → Recommended = no

4. Poor in-flight staff service (unresponsive, rude crew) 
   → Staff Service = 1, Overall Rating ≤ 4 
   → Recommended = no (less reliably than factors 1–2)
```

Factors 1 and 2 are the dominant causal paths. The onboard product — seat hardware and in-flight service — is rarely the sole reason for non-recommendation. Ground-side failures and broken product promises are the decisive causal mechanism.
