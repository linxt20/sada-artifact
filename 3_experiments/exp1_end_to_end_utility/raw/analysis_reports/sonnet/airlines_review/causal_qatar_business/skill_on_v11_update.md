---
dataset: airlines_review
scenario: causal_qatar_business
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "non_recommendation_outcome"
query: "Explain why some Qatar Airways Business-Class flights receive a non-recommended (Recommended = no) result."
source_table: augment_table/airlines_review/causal_qatar_business/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:03:41.134396+00:00
wall_seconds: 43.29
---

# Why Some Qatar Airways Business-Class Flights Receive a Non-Recommended Result

## Dataset Overview
- **Total reviews:** 592 (Qatar Airways, Business Class)
- **Recommended = yes:** 465 (78.5%)
- **Recommended = no:** 127 (21.5%)

---

## Primary Driver: Poor Value for Money

The single strongest differentiator is **Value For Money (VFM)**. Non-recommended reviews score an average of **2.22 / 5** versus **4.29 / 5** for recommended reviews. Among the 127 non-recommended reviews, 69 (54%) gave VFM a score of 1 or 2. This is particularly notable because other service metrics (seat comfort, staff service, food) are only modestly lower in the non-recommended group, meaning passengers who are otherwise somewhat satisfied still withhold a recommendation when they feel the price is unjustified.

| Metric | Recommended = no | Recommended = yes |
|---|---|---|
| Overall Rating | 3.82 | 8.43 |
| Value For Money | 2.22 | 4.29 |
| Staff Service | 4.01 | 4.39 |
| Seat Comfort | 3.87 | 4.01 |
| Food & Beverages | 3.85 | 3.94 |

---

## Contributing Factor 1: Cabin Crew Service Quality

Non-recommended reviews show markedly weaker crew ratings:
- **49.6%** rated crew as merely `adequate` (vs. 23.9% in recommended group)
- **30.7%** rated crew as `indifferent_or_absent` (vs. only 4.3% in recommended)
- Only **6.3%** described crew as `proactive_excellent` (vs. 71.0% in recommended)

Crew service is a hallmark of Qatar's Business Class brand. When crews are perceived as indifferent or absent, the premium proposition collapses, reinforcing the non-recommendation.

---

## Contributing Factor 2: Service Inconsistency Across Sectors

**74.0%** of non-recommended reviews are tagged `variable_by_sector`, and a further **19.7%** are `consistent_low`. Only **3.9%** reported `consistent_high` service (vs. 61.5% of recommended reviews). Multi-leg itineraries through Doha expose inconsistency: a strong outbound experience paired with poor service on the connecting leg frequently drives the overall non-recommendation.

---

## Contributing Factor 3: Onboard Amenity Gaps

**78.0%** of non-recommended reviews are coded `partial_omission` for onboard amenity quality — meaning amenities advertised as part of Business Class were absent or incomplete. In contrast, **70.3%** of recommended reviews report `full_premium` amenity delivery. Missing items (amenity kits, bedding, premium dining elements) undercut the perceived value and directly compound the VFM penalty.

---

## Contributing Factor 4: Seat Hardware Problems

Seat hardware is less critical than service/value, but still meaningful:
- **14.2%** of non-recommended reviews note `cramped_config`
- **6.3%** note `full_flat_defective` seats (e.g., seats that won't stay reclined)
- Combined, ~20% of non-recommended reviews involve substandard seat hardware

By contrast, **83.4%** of recommended reviews report `full_flat_functional` seating.

---

## Contributing Factor 5: Downgrade Notification Failure

**13.4%** of non-recommended reviews involve a `downgrade_notification_failure` — passengers who were not properly informed of a downgrade or product change — versus only **1.7%** in recommended reviews. This represents a trust/transparency failure that strongly signals non-recommendation despite being a relatively rare event.

---

## Weak Evidence / Exceptions

- A small minority (**3.9%**) of non-recommended reviews still report `consistent_high` service and `full_flat_functional` seats, suggesting that even objectively good hard/soft product is sometimes insufficient if price expectations are not met.
- **30.7%** of non-recommended reviews have `Unknown` seat hardware quality and **16.5%** have `Unknown` amenity quality, which limits the precision of hardware-based conclusions for those cases.
- Some non-recommended reviews (e.g., Auckland–Doha) note partially positive experiences with scores around 7/10 overall — these edge cases likely reflect price sensitivity rather than systemic failure.

---

## Summary

Non-recommended Qatar Airways Business-Class reviews are overwhelmingly driven by **poor perceived value for money**, amplified by **indifferent or inconsistent cabin crew**, **partial amenity delivery**, and **service that varies markedly between flight sectors**. Seat hardware defects and downgrade notification failures are secondary but directionally consistent contributors. The data shows no single absolute failure mode; rather, a clustering of service shortfalls against a premium price point produces the non-recommendation outcome.
