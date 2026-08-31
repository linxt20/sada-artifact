---
dataset: education_survey_responses
scenario: causal_low_satisfaction
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: causal_attribution
focus_variable: "satisfaction_1to5"
query: "Why is learning satisfaction low for certain groups, and which factors drive it?"
source_table: augment_table/education_survey_responses/causal_low_satisfaction/original.csv
generated_at: 2026-07-26T13:07:06.752415+00:00
wall_seconds: 60.86
---

# Why Is Learning Satisfaction Low for Certain Groups? — Causal Analysis

**Dataset:** 250 education survey responses (K-12, multiple subjects, roles: Student / Teacher / Parent)  
**Focus variable:** `satisfaction_1to5` (1 = very dissatisfied, 5 = very satisfied)  
**Scope:** Remote/online learning during a disrupted school year

---

## 1. Overview of Satisfaction Distribution

| Score | Count | % of Total |
|-------|-------|-----------|
| 1     | 32    | ~13%      |
| 2     | 52    | ~21%      |
| 3     | 63    | ~25%      |
| 4     | 66    | ~26%      |
| 5     | 37    | ~15%      |

Scores of 1–2 ("low satisfaction") account for **~34%** of responses — a substantial minority with clear common patterns.

---

## 2. Key Groups with Low Satisfaction

### 2a. Grade Level: K-5 (Young Children)
Young children generate a disproportionate share of 1–2 ratings (e.g., ED-0003, ED-0016, ED-0080, ED-0115, ED-0139, ED-0146, ED-0155, ED-0164). Representative quotes:

- *"My second grader cries before every reading session. The platform logs her out repeatedly, the teacher can't tell when she's lost."* (Parent, K-5 English, score 1)
- *"I don't like math on the computer. The numbers move and I can't find my pencil and the teacher can't see my paper. My mom helps but she gets mad when I cry."* (Student, K-5 Math, score 1)
- *"Kindergarten math has become me teaching my child while pretending to work full time."* (Parent, K-5 Math, score 1)

**Why:** Developmental mismatch — young learners need physical proximity, peer co-presence, and adult supervision that video platforms cannot replicate. Attention spans are short and self-regulation is limited.

---

### 2b. Subjects Requiring Physical Materials or Ensemble Practice
**Arts (performing: choir, orchestra, theater, ceramics, sculpture)** and **lab-heavy Sciences (Chemistry, Physics)** show the highest concentration of low scores:

- *"Choir over Zoom is the worst. We can't sing together because of the lag."* (Student, 6-8 Arts, score 1)
- *"Orchestra over video is just impossible… I've been playing violin for ten years and this format makes me want to quit."* (Student, 9-12 Arts, score 2)
- *"Band class is unworkable remotely… Her motivation is gone."* (Parent, 6-8 Arts, score 1)
- *"Chemistry without a real lab is essentially worthless… He says he understands nothing."* (Parent, 9-12 Science, score 2)
- *"AP Studio Art remotely has been a year of compromise after compromise."* (Teacher, 9-12 Arts, score 1)
- *"AP Chemistry without a real lab is a hollow course."* (Teacher, 9-12 Science, score 1)

**Why:** These subjects are fundamentally **embodied** — the learning outcome *is* the physical experience (lab intuition, ensemble playing, studio risk-taking). No digital workaround fully substitutes.

---

### 2c. Teachers and Students in Disengaged Classrooms
Low satisfaction strongly correlates with **absent teacher responsiveness** and **passive pedagogy**:

- *"The history class is just worksheets uploaded with no instruction… The teacher rarely responds to emails within a week."* (Parent, 6-8 History, score 1)
- *"AP World History has become assigned readings with no instruction… We're paying for tutoring."* (Parent, 9-12 History, score 1)
- *"The teacher posts readings and quizzes and that's it. No lectures, no discussions, no projects."* (Student, 9-12 History, score 1)
- *"I've lost half my AP Literature class to disengagement… administrators offer no support."* (Teacher, 9-12 English, score 1)

**Why:** Without proactive teaching (live interaction, timely feedback, relational check-ins), students disengage rapidly. The remote format amplifies teacher passivity — students can invisibly disconnect.

---

### 2d. Math Courses Requiring Collaborative/Visual Work (Geometry, Pre-Algebra)
Geometry and lower-division math repeatedly score 1–2:

- *"Geometry without physical manipulatives and group problem-solving has been brutal… My pass rate has cratered."* (Teacher, 9-12 Math, score 2)
- *"Proofs require drawing alongside the teacher and the screen-share lag makes it impossible."* (Parent, 9-12 Math, score 2)
- *"Pre-algebra requires constant whiteboard interaction and that just doesn't translate."* (Teacher, 6-8 Math, score 1)
- *"Half my students have cameras off and turn in nothing."* (Teacher, 6-8 Math, score 1)

**Why:** Geometry/proof-based math depends on dynamic shared whiteboard interaction and spatial manipulation. Tablet lag and asynchronous formats break the feedback loop essential to conceptual development.

---

### 2e. Middle School Students (Social-Emotional Needs)
6–8 students generating low scores frequently cite **loss of social interaction** as the core driver:

- *"I miss debating with my friends about whether George Washington was overrated."* (Student, 6-8 History, score 2)
- *"No book talks with friends, no acting out scenes, no fun… I used to love reading and now I avoid it."* (Student, 6-8 English, score 2)
- *"Fractions are hard and online is harder… My older brother helps me but he's also got his own classes."* (Student, 6-8 Math, score 2)

**Why:** Peer interaction is central to middle schoolers' engagement. Remote formats strip social motivation, leaving academic content as the only anchor — insufficient for this developmental stage.

---

## 3. Causal Factors Driving Low Satisfaction (Summary)

| Factor | Evidence Strength | Affected Groups |
|--------|------------------|-----------------|
| **Physical/embodied activity impossible online** (labs, ensemble, studio) | Strong | Arts (performing), Science, K-5 |
| **Young children's developmental needs unmet** (attention, proximity, regulation) | Strong | K-5 all subjects |
| **Teacher disengagement / passive pedagogy** (worksheets only, slow feedback, no interaction) | Strong | All grades, esp. History, English |
| **Social isolation / loss of peer learning** | Strong | 6-8 students, Arts, English |
| **Technical barriers** (lag, platform glitches, audio issues) | Moderate | K-5, Math (whiteboard-dependent) |
| **Inequitable home support** (parents unavailable, no materials) | Moderate | K-5 Science, Math |
| **Student disengagement cascade** (cameras off → teacher can't redirect) | Moderate | 6-8 and 9-12 Math, English |

---

## 4. Important Exceptions and Weak Evidence

- **High-performing remote classes exist in every subject**, including Science (AP Chem, AP Environmental, 7th grade life science) and Arts (digital photography, digital media, film). Teacher adaptability is the distinguishing variable, not subject alone.
- **Calculus and Statistics fare better than Geometry and Pre-Algebra** at the 9-12 level — abstract/analytic subjects that already relied heavily on individual problem-solving translate better than visuo-spatial or manipulative-dependent content.
- **Asynchronous formats help introverted or equity-burdened students** in writing and discussion (e.g., ED-0026, ED-0052), meaning low satisfaction is not universal even within struggling subjects.
- **Role differences**: Parents of K-5 children report the most severe dissatisfaction; teacher self-reports at K-5 are also strongly negative; 9-12 student reports are more mixed, reflecting greater self-regulation capacity.
- The sample is **not statistically controlled** — teacher quality, platform quality, and household resources co-vary, making it difficult to isolate any single causal factor with certainty.

---

## 5. Decision-Ready Conclusions

1. **Prioritize K-5 students and performing/studio arts** for earliest return to in-person or hybrid instruction — these groups show the most consistent, cross-role evidence of unmet needs.
2. **Teacher responsiveness is the highest-leverage intervention**: classes with active feedback loops, live interaction, and creative pedagogy consistently score higher regardless of grade or subject.
3. **Lab-dependent STEM courses (Chemistry, Physics, Biology)** require physical access to equipment; simulations are a partial but insufficient substitute, especially at the AP level.
4. **Geometry and manipulative-based math** should receive dedicated whiteboard tools and smaller synchronous groups; passive video instruction is ineffective.
5. **Middle-school social structures** (collaborative projects, peer discussion) need explicit design into remote formats — passive forums do not replace peer motivation.
