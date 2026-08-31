---
dataset: healthcare_visit_notes
scenario: causal_triage
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: what_if
focus_variable: "triage_and_scheduling_efficiency"
query: "How can clinics improve triage and scheduling?"
source_table: augment_table/healthcare_visit_notes/causal_triage/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:22:01.075578+00:00
wall_seconds: 82.44
---

# Healthcare Clinic Triage and Scheduling Improvement Report
**Dataset:** haiku__skill_on_v11_update | **Variant:** skill_on | **Query:** How can clinics improve triage and scheduling?

---

## Executive Summary

Analysis of 250 clinical visits reveals that current triage and scheduling practices achieve high fidelity in routing (100% emergency alignment, 87.2% routine alignment), but significant improvement opportunities exist in **handling urgent-category variability**, **matching visit duration to complexity**, and **tailoring scheduling by patient population**.

---

## Key Findings

### 1. Current Scheduling Alignment (Strong Foundation)

**Emergency and Routine Triage:**
- ✓ Emergency visits (28 cases, 11.2%) routed correctly to emergency department: **100% adherence**
- ✓ Routine visits (141 cases, 56.4%) placed in standard/preventive slots: **87.2% adherence**
- ⚠ Urgent visits (81 cases, 32.4%) get expedited slots: **70.4% adherence** (9 cases misaligned)

**Implication:** Urgent-category variation is the primary source of scheduling friction. Some urgent cases are not receiving same-day or next-day availability.

---

### 2. Duration Mismatch Between Clinical Complexity and Slot Allocation

**Actual duration patterns by urgency:**
| Urgency | Mean Duration | Range | Scheduled Slots |
|---------|---------------|-------|-----------------|
| Emergency | 45.5 min | 30–60 | Longest, appropriate |
| Routine | 22.6 min | 15–30 | Standard slots |
| Urgent | 23.2 min | 15–35 | Varies (inconsistent) |

**Critical gap:** High-acuity visits (clinical acuity signal ≥4, n=32) require **42.5 min average**—yet current scheduling offers a mix of short and extended slots. Only 13% of visits are high-acuity; these cluster in Emergency (26/32 cases) and Urgent (6/32) categories.

**Recommendation:** Establish acuity-based slot templates rather than urgency alone.

---

### 3. Department-Specific Scheduling Needs

Departments show distinct visit complexity and urgency profiles:

| Department | Visits | Avg Duration | % Urgent | Insight |
|-----------|--------|--------------|----------|---------|
| Cardiology | 42 | 30.1 min | 28.6% | Longest visits (chronic management & procedures) |
| Orthopedics | 39 | 25.9 min | 43.6% | **Highest % urgent** (trauma, sprains, fractures) |
| Pediatrics | 45 | 19.9 min | **47.8%** | **Highest urgency rate** (infections, injuries) |
| Dermatology | 42 | 17.0 min | 38.1% | Shortest visits but moderately urgent |
| GeneralPractice | 54 | 21.9 min | 27.8% | Most balanced workload |
| Emergency | 28 | 45.5 min | 100% | Expected—all acute/trauma |

**Actionable insight:** Pediatrics and Orthopedics need **disproportionate urgent-slot capacity** (47.8% and 43.6% of visits). Cardiology needs **extended time allocations** (30+ minutes typical).

---

### 4. Problem Category → Resource Requirement Mapping

Certain problem types drive resource and scheduling needs:

| Category | Count | Avg Duration | Typical Urgency | Scheduling Strategy |
|----------|-------|--------------|-----------------|---------------------|
| **Chronic Management** | 65 | 26.0 min | Routine (85%) | Longitudinal continuity slots (60/250 visits) |
| **Trauma/Emergency** | 44 | 37.5 min | Emergency/Urgent (88%) | Extended slots; ED referral for 56% |
| **Preventive Screening** | 43 | 20.6 min | Routine (93%) | Annual preventive slots; efficient (20 min) |
| **Acute Infection** | 30 | 20.5 min | **100% Urgent** | Same-day availability critical |
| **Procedural Intervention** | 39 | 21.4 min | Mixed (72% routine) | Pre-procedure prep coordination |

**Critical insight:** All acute infection cases (100%, n=30) are urgent but short duration—these are ideal candidates for **rapid same-day walk-in or short-notice booking**.

---

### 5. Complex Patient Populations Require Coordinated Scheduling

**Complex patients** (n=69, 27.6%):
- Multiple chronic conditions, post-surgical status, special pediatric/geriatric needs, or polypharmacy
- Average duration: 24.1 min (slightly longer than pure routine cases at 22.6 min)
- Key flag: **85% of longitudinal continuity slots** serve complex patients—suggests effective clustering of follow-up appointments

**Age-related patterns:**
| Age | Visits | % Urgent | Avg Duration |
|-----|--------|----------|--------------|
| 0–17 (Pediatric) | 46 | 47.8% | 19.9 min |
| 18–39 | 57 | 29.8% | 23.5 min |
| 40–59 | 60 | 28.3% | 25.3 min |
| 60+ (Geriatric) | 87 | 28.7% | **29.5 min** |

**Finding:** Pediatric population is 1.6× more likely to be urgent; geriatric population needs longest visits (+30% vs. young adults). Current scheduling appears to accommodate these, but age-specific resource pre-positioning is not explicit.

---

### 6. Scheduling Action Recommendations—Current Utilization

Top scheduling categories show appropriate complexity matching:

| Action | Count | Avg Duration | Role |
|--------|-------|--------------|------|
| **Longitudinal Continuity Slot** | 60 | 24.2 min | Chronic disease follow-up (85% complex cases) |
| **Scheduled Procedure + Prep** | 39 | 22.1 min | Procedures & diagnostics with prep coordination |
| **Emergency Department Immediate** | 37 | 40.4 min | All high-acuity (100% signal ≥4) |
| **Preventive Maintenance Annual** | 32 | 20.2 min | Health maintenance screening |
| **Same-Day Available Slot** | 27 | 20.2 min | Acute infections, injuries (low complexity) |
| **Specialist Referral Needed** | 16 | 25.6 min | Requires coordination; 31% high-acuity |

**Weak point:** Nine urgent visits are not routed to expedited slots, suggesting triage classification inconsistency at intake.

---

## Recommendations for Improvement

### 1. **Refine Urgent Category Triage Rules** (Priority: High)
- **Current state:** 70.4% of urgent cases get expedited slots; 29.6% miss expedited routing
- **Action:** Implement decision rules based on *clinical acuity signal* + *intervention intensity* rather than urgency label alone
  - Signal ≥3 + intervention ≥2 → same-day or next-day slot
  - This would capture **trauma, acute infections, and complex evaluations** systematically
- **Expected impact:** Improve urgent scheduling alignment from 70.4% to 90%+

### 2. **Allocate Department-Specific Slot Capacity** (Priority: High)
- **Pediatrics:** Reserve 45–50% of capacity for urgent/same-day (current: 47.8% need)
- **Orthopedics:** Reserve 40–45% for urgent (current: 43.6% need)
- **Cardiology:** Allocate 30+ min standard slots (current avg: 30.1 min; well-matched)
- **Dermatology:** Optimize 15–20 min slots for routine (current avg: 17.0 min; appropriate)

### 3. **Fast-Track Acute Infection Pathway** (Priority: Medium)
- All 30 acute infection visits are urgent but average only 20.5 min
- **Action:** Create urgent walk-in or rapid-booking slots (15–20 min blocks) for respiratory, urinary, skin, and ENT infections
- Partner with triage intake to auto-route confirmed/suspected infections to this pathway
- **Expected impact:** Reduce waits, free longer appointments for complex cases

### 4. **Implement Complexity-Adjusted Time Allocation** (Priority: Medium)
- High-acuity cases (n=32, avg 42.5 min) currently mixed with routine cases (avg 22.6 min)
- **Action:** Create booking template that doubles availability duration when clinical acuity ≥4 or intervention intensity ≥3
- Reserve ~5–10% of total appointment slots (12–15 per week in typical clinic) for these extended visits
- **Expected impact:** Reduce provider overruns and patient wait cascades

### 5. **Coordinate Geriatric and Pediatric Pre-Arrival** (Priority: Low)
- Pediatric visits average 19.9 min but urgency rate is 47.8% (vs. 28.7% elderly)
- Geriatric visits average 29.5 min (30% longer than pediatric)
- **Action:** Assign clinic staff to pre-screen pediatric and 60+ visits during scheduling; flag comorbidities and prepare coordination contacts (e.g., school, home health)
- **Expected impact:** Reduce appointment delays and improve care continuity; modest (2–3 min per visit)

### 6. **Standardize Procedure Pre-Coordination** (Priority: Low)
- 39 scheduled_procedure_with_prep visits occur; 31% high-acuity
- **Current:** These appear well-allocated (22.1 min avg)
- **Action:** Create checklist ensuring labs, imaging, consents, and supply requisitions are confirmed **48 hours pre-visit**; flag any high-acuity procedures (signal ≥3) for senior clinician pre-review

---

## Data Quality Notes

- **Strengths:** Complete urgency classification, consistent visit duration recording, well-defined scheduling actions, clear problem categorization
- **Limitations:** 
  - Clinical acuity signal ranges 1–5 but lacks explicit clinical definitions (appears ordinal); recommend validation with clinical protocol
  - No explicit "reason for visit" → urgency mapping rules visible in data; triage intake logic is implicit
  - 9 urgent–standard slot misalignments cannot be traced to root cause (classification vs. capacity)
  - Comorbidity flag categories show some redundancy (e.g., "not_present" vs. "no_comorbidity")

---

## Conclusion

Clinics can improve triage and scheduling by:
1. **Tightening urgent case routing** (add acuity-based rules)
2. **Right-sizing slot duration** by clinical complexity, not just urgency label
3. **Allocating capacity** to departments with high urgent-visit burden (Pediatrics, Orthopedics)
4. **Creating fast tracks** for low-complexity urgent cases (acute infections)
5. **Pre-coordinating** geriatric and pediatric visits to reduce delays

These changes are data-supported, require modest system adjustments, and directly address the 29.6% of urgent cases currently not receiving expedited scheduling.
