---
dataset: education_survey_responses
scenario: predictive_low
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "satisfaction_1to5"
query: "What open-response signals predict low learning satisfaction?"
source_table: augment_table/education_survey_responses/predictive_low/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:09:20.995086+00:00
wall_seconds: 92.22
---

# Analysis Report: Open-Response Signals Predicting Low Learning Satisfaction

**Dataset:** education_survey_responses (augmented with signal extraction)  
**Query:** What open-response signals predict low learning satisfaction?  
**Focus Variable:** satisfaction_1to5 (1-2 = low satisfaction)  
**Total Responses:** 250 (74 low satisfaction, 75 mid, 101 high satisfaction)

---

## Executive Summary

Low learning satisfaction is predicted by seven key open-response signal categories, with **isolation/disconnection** and **engagement loss** showing the strongest predictive power. Notably, 31% of low-satisfaction responses contain *no automatically flagged signal*, indicating that human interpretation of qualitative text is essential. The strongest signals appear in specific pedagogical contexts: ensemble/performance-based courses, foundational mathematics for young learners, and structured lecture-based subjects without interactive components.

---

## Primary Predictive Signals

### Signal Strength Ranking (Risk Ratios vs. High Satisfaction)

| Signal | Low Sat (%) | High Sat (%) | Risk Ratio | Interpretation |
|--------|------------|-------------|-----------|-----------------|
| **Isolation/Disconnection** | 23.0% | 1.0% | **23.2x** | Strongest single predictor; loss of peer interaction and classroom community |
| **Technical Issues** | 14.9% | 1.0% | **15.0x** | Platform lag, connectivity failures, device problems severely undermine engagement |
| **Instruction Quality Gaps** | 17.6% | 2.0% | **8.9x** | Unclear teaching, inadequate explanation, or minimal teacher-student interaction |
| **Engagement Complaints** | 21.6% | 4.0% | **5.5x** | Boredom, loss of motivation, perception that learning is drudgery |
| **Parent Stress/Burden** | 20.3% | 13.9% | **1.5x** | Parental workload spillover; however, also present in 14% of high satisfaction |
| **Hands-On Learning Missing** | 9.5% | 0.0% | Infinite | Present only in low satisfaction; specific to arts and sciences |
| **Young Learner Struggle** | 9.5% | 0.0% | Infinite | K-5 specific challenges; cannot replicate teacher proximity and supervision |

---

## Thematic Breakdown from Open Responses

### 1. **Isolation and Disconnection (23.0% of low-sat responses)**

**Definition:** Loss of peer interaction, classroom community, and collaborative learning opportunities.

**Evidence:**
- Teacher (ED-0005): "Cameras off, microphones muted, and the chat is silent. I feel like I'm performing to a wall."
- Student (ED-0082): "No debates, no group projects with friends, no inside jokes about Shakespeare."
- Teacher (ED-0035): "Half my students have cameras off and turn in nothing."

**Context:** Particularly acute in subjects requiring ensemble work (choir, band, theater) and discussion-based courses (literature, history).

---

### 2. **Boredom and Lost Engagement (23.0% of low-sat responses)**

**Definition:** Perceived loss of learning joy; school reduced to task completion rather than meaning-making.

**Evidence:**
- Student (ED-0009): "I used to love history and now I just click through assignments to keep my GPA from tanking."
- Student (ED-058): "The teacher rarely calls on us and the chat is dead. I used to write stories for fun and now I can barely finish the assigned essays."
- Student (ED-0220): "English online is dead. We read silently, write essays, post in forums that nobody reads."

**Mechanism:** Passive consumption (watching slides, reading alone, submitting work) replaces active, social meaning-making. Particularly damaging when coupled with weak teacher presence.

---

### 3. **Hands-On and Practical Learning Missing (9.5% of low-sat responses)**

**Definition:** Impossibility of performing lab work, manipulating objects, or practicing physical/artistic skills.

**Evidence:**
- Student (ED-0029): "Choir over Zoom is the worst. We can't sing together because of the lag so we just mouth along to a recording. It feels pointless."
- Parent (ED-0051): "Band class is unworkable remotely. My daughter practices alone, sends recordings, and never plays with her ensemble."
- Student (ED-0076): "Chemistry without a real lab is just memorization. I can balance equations but I don't understand why anything actually happens."

**Context:** Over-represented in Arts (32.6% low satisfaction rate) and Math (34.0%), where procedural understanding requires embodied practice or ensemble performance.

---

### 4. **Instruction Quality Gaps (17.6% of low-sat responses)**

**Definition:** Teachers provide minimal explanation, rarely respond to student questions, or give delayed feedback.

**Evidence:**
- Parent (ED-0020): "The history class is just worksheets uploaded with no instruction... teacher rarely responds to emails within a week."
- Student (ED-0046): "The teacher moves fast, I can't ask quick clarifying questions without interrupting, and tutoring fills up within minutes."
- Parent (ED-0209): "Teacher rarely interacts, feedback is months late."

**Mechanism:** Online asynchronous formats magnify the cost of passive instruction. Without real-time clarification or responsive feedback loops, students cannot recover from confusion.

---

### 5. **Technical Issues (14.9% of low-sat responses)**

**Definition:** Platform lag, connectivity failures, audio/video problems that disrupt learning flow.

**Evidence:**
- Student (ED-0001): "My camera freezes whenever Mr. Patel tries to share his whiteboard, and by the time it loads he's already three problems ahead."
- Parent (ED-0027): "Screen-share lag makes it impossible" for a visual learner to understand geometry proofs.
- Student (ED-0029): "We can't sing together because of the lag."

**Impact:** While present in only 1% of high satisfaction responses, technical issues create friction that amplifies other barriers (e.g., already-disconnected students give up further when tech fails).

---

### 6. **Young Learner Struggles (9.5% of low-sat responses)**

**Definition:** K-5 students unable to manage self-directed learning, teachers unable to redirect off-task behavior, and manipulatives/fine motor instruction impossible at distance.

**Evidence:**
- Teacher (ED-0008): "Half can't unmute, parents hover anxiously, and manipulatives don't translate. I dread Monday morning logins now."
- Student (ED-0016): "The numbers move and I can't find my pencil and the teacher can't see my paper. My mom helps but she gets mad when I cry."
- Parent (ED-0080): "Kindergarten math has become me teaching my child while pretending to work full time."

**Severity:** These respondents show no high-satisfaction counterparts (0% in high satisfaction), indicating near-universal challenge in K-5 remote instruction for some learner types.

---

## Signal Patterns: Single vs. Multiple Barriers

**Distribution in low satisfaction:**
- **31%** (23/74) report *no automatically flagged signal* but still express low satisfaction  
- **37%** (27/74) report *exactly 1 signal*  
- **32%** (24/74) report *2+ signals* (often compounding barriers)

**Key observation:** The absence of a flagged signal in nearly one-third of low-satisfaction cases reveals that loss of joy, disconnection to meaningful learning, or subtle pedagogical misalignment often cannot be reduced to a single data column. Qualitative depth is essential.

---

## By Respondent Role

| Role | Low Satisfaction Rate | Most Common Signals |
|------|----------------------|-------------------|
| **Student** (27/89) | 30.3% | Isolation (23%), Engagement loss (22%), Instruction gaps (15%) |
| **Teacher** (24/81) | 29.6% | Engagement loss (21%), Isolation (19%), Instruction gaps (17%) |
| **Parent** (23/80) | 28.7% | Young learner struggle (26%), Parent burden (39%), Isolation (22%) |

**Insight:** Teachers express low satisfaction around inability to create engagement; parents around their own unsupported role and young children's struggles.

---

## By Subject

| Subject | Low Sat Rate | Key Barriers |
|---------|-------------|--------------|
| **Math** | 34.0% | Hands-on (visual/spatial learning), pacing, tutoring inaccessibility |
| **Arts** | 32.6% | Ensemble impossibility, studio community loss, fine motor limits |
| **English** | 28.0% | Peer discussion loss, engagement erosion, limited synchronous interaction |
| **History** | 28.3% | Debate/role-play loss, passive lecture fatigue, discussion forums ineffective |
| **Science** | 25.5% | Lab work loss, simulations insufficient, equipment/materials challenges |

---

## By Grade Band

- **K-5:** 30.3% low satisfaction | Driven by young learner struggle, teacher proximity needs, parental burden
- **6-8:** 28.9% low satisfaction | Driven by isolation/peer disconnection, subject-specific barriers (lab sciences, performance arts)
- **9-12:** 29.6% low satisfaction | Driven by engagement erosion ("used to love this subject"), advanced subject depth loss

---

## Predictive Accuracy and Limitations

**Model Performance:**
- **33 responses flagged** as predicted low satisfaction  
- **26 true positives** (78.8% precision among flagged)  
- **Recall:** 26/74 = 35% (misses 64% of actual low satisfaction cases)

**Why recall is low:** Many low-satisfaction responses lack an explicit signal phrase and instead express subtler forms of dissatisfaction: nostalgia for in-person learning, loss of joy, perception of meaninglessness, or adaptive resignation ("I'm getting decent grades but I haven't enjoyed a single book this year").

---

## Actionable Insights

### Highest-Leverage Interventions

1. **Restore peer interaction** (addresses 23% of low-sat cases)  
   - Implement breakout room structures with clear collaborative tasks  
   - Build asynchronous community forums with facilitation  
   - Schedule optional peer study/social sessions

2. **Improve teacher responsiveness** (addresses 18% of low-sat cases)  
   - Reduce asynchronous response time SLA to <24 hours  
   - Provide real-time chat office hours (not just recorded content)  
   - Implement quick-response feedback mechanisms (polls, screencasts)

3. **Subject-specific support** (addresses 9.5% of low-sat cases)  
   - MATH: Provide shared whiteboard sessions, visual step-by-step demos, shortcut tutoring appointments  
   - ARTS: Enable ensemble breakout rooms (e.g., peer recording, multitrack collaboration)  
   - SCIENCES: Deliver hands-on experiment kits with video guidance for at-home replication  

4. **K-5 intensive support** (addresses 9.5% of low-sat cases)  
   - Smaller synchronous groups (5-8 students max) for young learners  
   - Structured parent partner protocols; reduce parental teaching load  
   - Hands-on manipulatives kits; explicit modeling of self-regulation cues

### Weak Evidence of Issues

- **Technical issues** (15% low satisfaction) are important *conduits* for dissatisfaction but alone do not drive low satisfaction when teaching is strong  
- **Parent stress** appears in both low (20%) and high satisfaction (14%), suggesting that parental burden is acceptable when learning outcomes are perceived as strong

---

## Conclusion

Low learning satisfaction in this dataset is most reliably predicted by **isolation/disconnection (23x risk)** and **technical issues (15x risk)**, followed by **engagement loss** and **instruction quality gaps**. However, roughly one-third of low-satisfaction responses carry no explicit signal, indicating that qualitative interpretation must extend beyond checklist signals to capture erosion of joy, meaningful connection to content, and loss of identity as a learner ("I used to love this").

The variant **skill_off** (soft skills emphasis in signal extraction) reveals that the absence of peer collaboration, classroom community, and live engagement represents the largest predictive cluster, even more than academic content gaps. Interventions should prioritize restoring **synchronous interaction**, **teacher responsiveness**, and **subject-appropriate pedagogy** over technology fixes alone.
