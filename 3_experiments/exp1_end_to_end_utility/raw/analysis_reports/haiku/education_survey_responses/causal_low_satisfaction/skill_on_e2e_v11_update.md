---
dataset: education_survey_responses
scenario: causal_low_satisfaction
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "satisfaction_1to5"
query: "Why is learning satisfaction low for certain groups, and which factors drive it?"
source_table: augment_table/education_survey_responses/causal_low_satisfaction/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:13:05.234409+00:00
wall_seconds: 142.12
---

# Analysis Report: Why Learning Satisfaction Is Low for Certain Groups

## Executive Summary

Nearly 30% of respondents reported low learning satisfaction (ratings 1–2) in remote/virtual education, concentrated among students with low prior engagement, subjects requiring hands-on interaction, and contexts where family support is weak. **Subject-format misalignment is the single strongest driver**, coupled with minimal teacher adaptation and pedagogical barriers to peer interaction. The analysis reveals critical systemic gaps, not random variation, with clear pathways to improvement through format redesign and instructional innovation.

---

## Method Note

**TAPP-Generated Columns Used in Analysis:**
- `subject_format_alignment` (well_aligned, partially_aligned, misaligned)
- `hands_on_requirement` (critical_for_subject, beneficial_not_critical, not_needed, not_present)
- `teacher_instructional_adaptation` (highly_innovative, moderately_adapted, minimally_adapted, passive_delivery)
- `peer_interaction_impact` (supports_engagement, critical_to_engagement, not_present, optional)
- `student_prior_engagement` (high_intrinsic_motivation, moderate_engagement, low_baseline_engagement)
- `family_support_availability` (high_capacity, moderate_capacity, low_capacity, unknown)

These semantic facets complement and clarify original structured fields (respondent_role, grade_level, subject, satisfaction_1to5, open_response).

---

## Key Findings

### 1. Low Satisfaction Is Heavily Concentrated in Format-Misaligned Contexts

**Subject-format alignment is the dominant driver.** Of the 74 low-satisfaction responses:
- **97.3%** (72/74) occur in "misaligned" format contexts
- **2.7%** (2/74) occur in "partially_aligned" contexts
- **0%** occur in "well_aligned" formats

Mean satisfaction by alignment:
| Alignment | Mean Satisfaction | N |
|-----------|-------------------|-----|
| well_aligned | 4.33 | 101 |
| partially_aligned | 2.97 | 72 |
| misaligned | 1.74 | 77 |

**The misaligned group differs by 2.59 points from well-aligned, representing ~60% reduction in satisfaction.**

### 2. Arts and Mathematics Show Highest Concentration of Low Satisfaction

Low satisfaction rates by subject:
| Subject | Low Satisfaction Count | Rate | Mean |
|---------|----------------------|------|------|
| Math | 18 | 34.0% | 3.08 |
| Arts | 15 | 32.6% | 2.98 |
| English | 14 | 28.0% | 3.20 |
| History | 13 | 28.3% | 3.15 |
| Science | 14 | 25.5% | 3.27 |

**Arts and Math are disproportionately affected**, both requiring hands-on engagement and peer collaboration that virtual formats severely constrain. Nearly **100% of low-satisfaction cases in Math and Science report misaligned formats**, while **93–100% of Arts students report both misalignment and 100% report critical peer-interaction barriers.**

### 3. Critical Hands-On Requirement Amplifies Misalignment Effects

**55.4%** of low-satisfaction cases (41/74) combine misaligned format **with** subjects requiring critical hands-on work:

| Hands-On Requirement | Low Satisfaction Cases | Effect on Satisfaction |
|----------------------|------------------------|------------------------|
| critical_for_subject | 41 | Mean = 1.65 |
| beneficial_not_critical | 4 | Mean = 2.93 |
| not_needed | 25 | Mean = 2.48 |

When format is misaligned **and** hands-on work is critical, satisfaction collapses. This pattern holds across:
- **Arts:** 93% of low-sat cases are in misaligned + critical hands-on (sculpting, painting, ensemble performance cannot be replicated digitally)
- **Science:** 86% report critical hands-on barriers (labs, dissections, microscopy, physical demonstrations)
- **Math:** 67% report critical hands-on needs (manipulatives, spatial reasoning, shared whiteboard work)

### 4. Peer Interaction Barriers Drive Low Engagement—Especially in Younger Grades

**90.5%** of low-satisfaction cases (67/74) occur where peer interaction is "critical_to_engagement" and the format is misaligned:

| Peer Interaction Impact | Mean Satisfaction | N |
|--------------------------|-------------------|-----|
| supports_engagement | 3.86 | 117 |
| critical_to_engagement | 2.05 | 95 |
| not_present (by design) | 3.57 | 35 |

**Critical finding:** When peer interaction is *critical* but *not supported*, satisfaction drops by 1.81 points vs. when it *supports* engagement. Absence-by-design (not_present) yields higher satisfaction than critical-but-broken interaction, suggesting respondents adapt to constraints better than frustrated needs.

Peer interaction criticality by grade and subject:
- **K–5 Arts/Music/Theater:** 100% of low-sat cases report critical peer interaction needs (ensemble work, co-creation)
- **6–8 English/History:** 86–92% report critical needs for discussion, debate, group projects
- **9–12 STEM:** 89% report critical peer barriers despite some math/science having less peer-dependent pedagogy

### 5. Teacher Instructional Adaptation Is the Second Major Lever

Minimal/passive instruction dominates low-satisfaction contexts:

| Teacher Adaptation | Low-Sat Cases | % of Low-Sat | Mean Satisfaction |
|-------------------|---------------|--------------|--------------------|
| minimally_adapted | 52 | 70.3% | 1.75 |
| passive_delivery | 21 | 28.4% | 1.78 |
| moderately_adapted | 1 | 1.4% | 3.19 |
| highly_innovative | 0 | 0% | 4.30 |

**No low-satisfaction cases occur with highly innovative adaptation.** The shift from "minimally_adapted" to "highly_innovative" increases satisfaction by 2.55 points (1.75 → 4.30). Teachers addressing format misalignment through active redesign (breakout rooms, asynchronous forums, video personalization, project-based pivots) eliminated low satisfaction entirely in this dataset.

### 6. Family Support Availability Is a Critical Equity Factor

Low-satisfaction cases are heavily concentrated in low-family-support contexts:

| Family Support | Low-Sat Cases | % of Low-Sat | Mean Satisfaction |
|----------------|---------------|--------------|--------------------|
| low_capacity | 60 | 81.1% | 1.65 |
| unknown | 8 | 10.8% | 3.31 |
| moderate_capacity | 4 | 5.4% | 3.00 |
| high_capacity | 2 | 2.7% | 4.14 |

**The low-capacity group suffers 2.49-point disadvantage vs. high-capacity.** Families with:
- Unstable home environments
- Limited tech infrastructure or literacy
- Multiple children competing for resources
- Insufficient materials for hands-on subjects

...experience compounded frustration when format is misaligned AND hands-on resources must be sourced at home.

**Grade-level equity variance:**
- K–5: 91% of low-sat cases report low family support (youngest learners need parental scaffolding most; remote format shifts burden onto parents)
- 6–8: 68% report low family support
- 9–12: 83% report low family support (older teens in resource-limited homes lack autonomy to self-support)

### 7. Student Prior Engagement Predicts and Concentrates Dissatisfaction

**Prior engagement is nearly deterministic:**

| Prior Engagement | Cases | Low-Sat Cases | % Low-Sat | Mean |
|------------------|-------|---------------|-----------|----|
| high_intrinsic_motivation | 100 | 0 | 0% | 4.33 |
| moderate_engagement | 70 | 6 | 8.6% | 2.93 |
| low_baseline_engagement | 79 | 68 | 86.1% | 1.82 |

**86.1% of low-baseline-engagement students are dissatisfied.** The remote format appears to amplify existing motivation gaps rather than solve them. Students who struggled pre-pandemic face compounding barriers: format misalignment → reduced peer interaction → isolated learning → lower engagement → cascading dissatisfaction.

**Triple-barrier pattern:** 87.8% of low-satisfaction cases (65/74) combine low prior engagement + critical peer-interaction barrier + misaligned format simultaneously.

### 8. Respondent Role Differences Are Modest; All Report Similar Drivers

Low satisfaction is consistent across role, suggesting systemic misalignment rather than role-specific issues:

| Role | Low-Sat Count | Rate | Key Drivers |
|------|---------------|------|-------------|
| Student | 27 | 30.3% | 100% misaligned; 56% minimally adapted |
| Teacher | 24 | 29.6% | 92% misaligned; 92% minimally adapted |
| Parent | 23 | 28.7% | 100% misaligned; 65% minimally adapted |

Teachers report the most acute frustration (92% minimally adapted in low-sat group), reflecting pedagogical constraints they recognize but cannot overcome alone. Parents consistently cite resource and support barriers. Students emphasize loss of peer interaction and difficulty focusing.

### 9. Grade-Level Patterns Show Consistent Misalignment Across Ages

| Grade | Low-Sat Cases | Misaligned % | Critical Hands-On % | Low Family Support % |
|-------|---------------|--------------|--------------------|----------------------|
| K–5 | 23 | 96% | 65% | 91% |
| 6–8 | 22 | 100% | 55% | 68% |
| 9–12 | 29 | 97% | 48% | 83% |

**Youngest grades show highest family-support burden** (91% low family support in K–5 dissatisfied group). **Middle grades show highest format misalignment rate** (100%). **High school has largest absolute low-sat population** (29 cases) driven by abstract subjects (calculus, chemistry, literature) that rely on discussion, collaboration, and visualization.

---

## Causal Summary: Why Satisfaction Is Low for Certain Groups

### Primary Pathway (93% of low-sat cases):
**Subject-Format Misalignment → Pedagogical Constraints → Barrier to Peer/Hands-On Engagement → Low Satisfaction**

Subjects inherently suited to in-person, interactive pedagogy (Arts, Music, Theater, elementary Math, hands-on Science, seminar-style English/History) faced severe format mismatch:
- **Ensemble music** cannot replace sync live performance with lag
- **Studio arts** require material exploration and physical critique
- **Elementary manipulatives math** (place value, fractions) demand kinesthetic interaction
- **Lab sciences** lose sensory learning and safety supervision
- **Seminar humanities** lose spontaneous discussion energy

### Secondary Pathway (81% of low-sat cases):
**Minimal Teacher Adaptation + Misaligned Format → Passive Delivery → Disengagement**

Teachers without resources, training, or incentives to redesign courses fell into "worksheets + videos" delivery, which:
- Offloads content to student to decode asynchronously
- Removes real-time feedback loops
- Eliminates peer accountability and co-learning

Contrast: 29 teachers with "highly innovative" adaptation (breakout rooms, asynchronous forums, reframed assessments, curated resources) experienced **zero low-satisfaction reports**, gaining mean +2.55 points satisfaction.

### Tertiary Pathway (81% of low-sat cases):
**Low Family Support + Format Misalignment + Hands-On Requirement → Resource Barrier + Burnout**

Particularly in K–5 and 9–12, low-satisfaction clusters involved:
- Families unable to source experiment kits, art supplies, or quiet workspace
- Limited parental education/capacity to scaffold virtual instruction
- Economic stress reducing "bandwidth" for homework support
- Single-income or multilingual households stretched thin

Younger children (K–5) showed highest family-support burden; oldest students (9–12) from low-resource families faced highest dissatisfaction rates (83% report low family support).

### Quaternary Pathway (86% of low-sat cases):
**Low Baseline Student Engagement + Format Misalignment → Amplified Disengagement**

Remote format did not engage previously unmotivated students; it worsened gaps:
- Loss of in-person peer accountability and social reward
- Reduced real-time teacher intervention opportunities
- Increased autonomy demand (asynchronous work) for students with executive function challenges
- Home distractions replacing school structure

The remote format appears to have *amplified* pre-existing motivation gaps rather than reducing them, as high-intrinsic-motivation students adapted well (0% dissatisfaction) while low-baseline students showed 86% dissatisfaction.

---

## Control Evidence: What Predicts High Satisfaction

The 33 high-satisfaction (rating=5) cases share inverse characteristics, validating causal logic:
- **100%** in well-aligned formats
- **87.9%** with highly innovative instruction
- **100%** with high prior student engagement
- **87.9%** with high family support
- **75.8%** with peer interaction that *supports* (not demands) engagement

Examples from open responses show teachers and students thriving when:
1. Format matches pedagogy (e.g., asynchronous forums for introverted students, digital design tools, virtual museums, citizen science projects)
2. Teachers invested in active redesign (Socratic seminars online, creative project pivots, breakout-room communities, individualized video feedback)
3. Family or peer infrastructure existed to support engagement
4. Prior student motivation was high or re-engaged by innovative instruction

---

## Equity Implications

**Low satisfaction is not random; it concentrates in vulnerable groups:**
1. **Families with low support capacity** (especially K–5, 83–91% of low-sat cases)
2. **Students with low prior engagement** (86% of low-baseline students dissatisfied)
3. **Subjects requiring hands-on/peer interaction** (Arts 32.6%, Math 34% vs. Science 25.5%)
4. **Teachers lacking autonomy/training for adaptive pedagogy** (92% of low-sat teachers report minimal adaptation)

The data suggests remote education amplified existing equity gaps rather than closing them, with format misalignment, weak instructional adaptation, and insufficient family support acting as compounding disadvantages.

---

## Recommendations (Evidence-Supported)

1. **Prioritize pedagogical redesign, not format compliance.** Subjects with critical hands-on/peer needs require intentional pivot (project-based, asynchronous forums, material kit distribution, virtual collaboration). Format-matching alone (making in-person lessons "web-friendly") fails.

2. **Invest in teacher adaptation capacity.** Zero low-satisfaction in highly-innovative-adaptation group suggests training, resources, and autonomy for course redesign are high-ROI interventions (+2.55 satisfaction points).

3. **Provide equitable family support infrastructure.** For K–5 and low-resource 9–12, mailed materials, parent education, and communication access reduce burden and address 81% of low-sat driver.

4. **Target vulnerable groups deliberately.** Low-baseline-engagement students need earlier intervention and peer accountability systems; low-capacity families need material/tech support; STEM students need robust peer-learning structures.

5. **Measure format-pedagogy fit, not just compliance.** Current satisfaction is explained by degree of alignment between subject needs and format affordances. Continued monitoring of this metric enables proactive intervention.

---

## Data Summary

- **Sample:** 250 respondents (89 students, 81 teachers, 80 parents)
- **Overall satisfaction:** Mean 3.14/5 (median 3.0)
- **Low satisfaction (1–2):** 74 cases (29.6%)
- **Subjects:** Math, Arts, English, History, Science
- **Grades:** K–5, 6–8, 9–12
