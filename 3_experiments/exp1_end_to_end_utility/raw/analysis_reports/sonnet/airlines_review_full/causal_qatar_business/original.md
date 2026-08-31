---
dataset: airlines_review_full
scenario: causal_qatar_business
variant: original
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "non_recommendation_outcome"
query: "Explain why some Qatar Airways Business-Class flights receive a non-recommended (Recommended = no) result."
source_table: augment_table/airlines_review_full/causal_qatar_business/original.csv
generated_at: 2026-08-03T05:38:56.974049+00:00
wall_seconds: 61.2
---

# Why Some Qatar Airways Business-Class Flights Receive a Non-Recommended Result

## Dataset Overview

The dataset contains **592 Qatar Airways Business-Class reviews**. Of these, **127 (21.5%)** are marked `Recommended = no` and **465 (78.5%)** are marked `Recommended = yes`. All records are in Business Class, so the analysis focuses on distinguishing factors within that cabin.

---

## Primary Drivers of Non-Recommendation

### 1. Low Overall Rating (Strongest Signal)

Overall Rating is the single strongest correlate with recommendation (`r = 0.67`). The distributions are starkly different:

| Rating | Not Recommended | Recommended |
|--------|----------------|-------------|
| 1–3    | 68 (53.5%)     | 14 (3.0%)   |
| 4–6    | 37 (29.1%)     | 62 (13.3%)  |
| 7–10   | 22 (17.3%)     | 389 (83.7%) |

Most non-recommended reviews cluster at ratings 1–5, indicating a fundamentally poor perceived experience.

### 2. Poor Value For Money (Equally Strong Signal)

Value For Money is the second strongest correlate (`r = 0.66`) and arguably the most distinguishing sub-score:

- **Not recommended mean VFM: 2.22** vs. **Recommended mean VFM: 4.29**
- **54% of non-recommended reviews** (69/127) gave VFM ≤ 2, compared to only **5.4%** (25/465) in the recommended group.

Passengers paying premium Business-Class fares hold exceptionally high expectations. When the product, service, or ground experience falls short, the perceived value gap is acute. Common themes in reviews:
- Paying for upgrades and receiving degraded seats (broken recline, outdated aircraft)
- Flight disruptions, rebookings, or downgrades without compensation
- Ground-side failures (lost luggage, poor handling) devaluing the overall price paid

### 3. Staff Service Disappointments

Mean Staff Service for non-recommended reviews is **4.01 vs. 4.39** for recommended. While many non-recommended passengers still gave staff high scores (70/127 gave Staff Service = 5), those rating staff ≤ 3 (36/127, 28%) describe issues such as inattentiveness, rude interactions, and inconsistent service across different aircraft legs.

### 4. Seat Comfort and Aircraft Configuration Complaints

Mean Seat Comfort is slightly lower in non-recommended reviews (3.87 vs. 4.01), but the qualitative pattern is clear: **inconsistent fleet/product** is a recurring complaint. Specific issues:
- **Boeing 777 2-2-2 middle-seat configuration** frequently criticised by solo travellers
- Older aircraft assigned on long-haul legs while newer QSuites appear only on select routes
- Uncomfortable bed positions despite comfortable sitting positions
- Seat mechanical failures (e.g., self-reclining seats)

### 5. Ground and Operational Failures

Several non-recommended reviews have moderate-to-high inflight scores but report failures at touchpoints Qatar controls off-plane:
- Lounge quality outside Doha rated poorly (third-party Priority Pass lounges in Europe)
- Long tarmac waits and bus transfers at Doha
- Billing disputes, call-centre failures, and missing upgrades
- Passengers bumped or rerouted without adequate notice

These ground-side failures push otherwise satisfactory flyers to decline recommending the airline.

---

## Edge Cases and Weak Evidence

- **22 non-recommended reviews have Overall Rating ≥ 7**, demonstrating that a small but notable group of passengers rate the inflight experience adequately but still decline to recommend—typically due to ground operations, pricing disappointments, or inconsistent multi-leg experiences.
- **Inflight Entertainment** shows almost zero correlation with recommendation (`r = -0.01`); it is not a meaningful driver.
- **Food & Beverages** correlation is also very weak (`r = 0.03`), suggesting food quality alone rarely determines recommendation.
- **Traveller type**: Business travellers are disproportionately represented in non-recommended reviews (36% of non-rec vs. 21% of recommended), possibly reflecting higher baseline expectations and sensitivity to operational failures.

---

## Summary

Non-recommendation among Qatar Airways Business-Class passengers is primarily explained by:

1. **Poor perceived value for money**—the dominant factor—driven by pricing, product inconsistency, or operational failures that undermine the premium price paid.
2. **Low overall satisfaction** reflected in ratings of 1–5, usually tied to broken/outdated seats, unresponsive service, or serious operational incidents.
3. **Ground-side and operational failures** (lounge quality, lost bags, last-minute aircraft swaps, bumping) that damage the end-to-end experience even when inflight service is acceptable.
4. **Fleet inconsistency**: passengers expecting QSuite but receiving older 777 or economy-comparable configurations feel misled and are unlikely to recommend.

Food, entertainment, and seat comfort are relatively minor independent contributors—poor value perception and overall disappointment are the decisive factors.
