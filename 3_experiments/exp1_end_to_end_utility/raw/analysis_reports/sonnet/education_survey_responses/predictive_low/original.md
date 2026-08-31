---
dataset: education_survey_responses
scenario: predictive_low
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: predictive_feature_engineering
focus_variable: "satisfaction_1to5"
query: "What open-response signals predict low learning satisfaction?"
source_table: augment_table/education_survey_responses/predictive_low/original.csv
source_report: dataset_portion_2/substrate-claude-sonnet-4-6/education_survey_responses__predictive_low/analyses/original/analysis.md
wall_seconds: 94.8
---

# Open-Response Signals Predicting Low Learning Satisfaction

## Dataset Overview

The dataset contains 250 survey responses (`response_id` ED-0001 to ED-0250) from three respondent roles—**Students**, **Teachers**, and **Parents**—across grade bands (K-5, 6-8, 9-12) and subjects (Math, Science, English, History, Arts). The focus variable is `satisfaction_1to5`. For this analysis, **low satisfaction is defined as scores of 1 or 2**, which accounts for approximately 30% of all records (~75 responses). Patterns were extracted by reading every open-response entry and cross-referencing with the numeric score.

---

## Key Signal Categories from Open Responses

### 1. Technology Failures and Platform Friction
**Strength: Very strong predictor of low satisfaction (1–2)**

The most frequent language in low-scoring responses references platform breakdowns that interrupt instruction:

- *"My camera freezes whenever Mr. Patel tries to share his whiteboard, and by the time it loads he's already three problems ahead."* (ED-0001, score 2)
- *"The platform logs her out repeatedly, the teacher can't tell when she's lost."* (ED-0003, score 1)
- *"The teacher writes on a tablet but the strokes lag and I get confused."* (ED-0038, score 2)
- *"The platform is glitchy, and assignments stack up unmarked."* (ED-0134, score 1)

**Signal words to watch:** *freezes, lag, glitchy, logs out, camera issues, can't unmute, audio cuts, internet stops.*

Teachers at the K-5 level (ED-0008, ED-0062, ED-0071, ED-0141) and students in math (ED-0001, ED-0038, ED-0046, ED-0157) most frequently cite these issues. However, technology problems also appear in some **mid-range** responses (scores of 3), so they are a necessary but not always sufficient condition for low satisfaction.

---

### 2. Absence of Interaction, Peer Learning, and Community
**Strength: Strongest consistent signal across all roles**

Low-satisfaction responses overwhelmingly describe a collapse of classroom social dynamics:

- *"Cameras off, microphones muted, and the chat is silent. I feel like I'm performing to a wall."* (ED-0005, Teacher, score 2)
- *"The novel discussions are silent, the writing prompts feel disconnected."* (ED-0041, Parent, score 2)
- *"No debates, no group projects, no field trips. I used to love history and now I just click through assignments."* (ED-0009, Student, score 2)
- *"We can't sing together because of the lag so we just mouth along to a recording. It feels pointless."* (ED-0029, Student, score 1)
- *"There's no community, no excitement about ideas."* (ED-0182, Parent, score 2)

High-satisfaction responses (4–5) frequently mention the **opposite**: active chats, breakout rooms, discussion forums, peer collaboration, and teacher-initiated community building. The contrast is sharp and reliable.

**Signal words/phrases:** *silent, cameras off, nobody talks, no debates, alone, no group projects, no peer interaction, dead.*

---

### 3. Passive-Only Instructional Format ("Worksheets + Videos with No Engagement")
**Strength: Strong predictor, especially for parents and older students**

Low-scoring open responses frequently describe a format reduced to uploading files with minimal live or interactive instruction:

- *"The history class is just worksheets uploaded with no instruction. The teacher rarely responds to emails within a week."* (ED-0020, Parent, score 1)
- *"The teacher posts readings and quizzes and that's it. No lectures, no discussions, no projects."* (ED-0106, Student, score 1)
- *"Assigned readings with no instruction. My son is teaching himself the entire course."* (ED-0086, Parent, score 1)
- *"We read silently, answer questions, repeat."* (ED-0058, Student, score 1)

This pattern is most prevalent in **History** and **English** classes at the 9-12 level and in **Science** at 6-8 and 9-12 where labs should occur.

**Signal words/phrases:** *just worksheets, no instruction, posts and moves on, rarely responds, silence, click through assignments.*

---

### 4. Loss of Hands-On or Physical Components
**Strength: Strong for STEM and Arts subjects; moderate overall**

A consistent low-satisfaction pattern appears when the subject intrinsically requires physical work that cannot translate to video:

- *"Kindergarten science needs sensory exploration that simply cannot happen on a tablet."* (ED-0071, Teacher, score 1)
- *"Chemistry without a real lab is just memorization."* (ED-0076, Student, score 2)
- *"AP Chemistry without a real lab is a hollow course."* (ED-0129, Teacher, score 1)
- *"He's lost interest in pursuing art beyond high school… without a studio."* (ED-0113, Parent, score 2)
- *"Sculpture class without a studio is just watching videos and submitting drawings instead."* (ED-0091, Student, score 1)
- *"Band class is unworkable remotely… she's talking about quitting after years of dedication."* (ED-0051, Parent, score 1)

**Subjects most affected:** Science (lab-based), Arts (performing arts—choir, band, theater, ceramics, studio art), and early-grade Math (manipulatives).

**Important exception:** Several **digital-native Arts** courses (digital photography, film, digital music, animation) score **4–5** even in remote settings (ED-0014, ED-0047, ED-0077, ED-0199), because the subject format aligns with the virtual medium. Hands-on loss predicts low satisfaction only when the course fundamentally requires physical materials or ensemble presence.

---

### 5. Teacher Disengagement or Inadequate Feedback
**Strength: Moderate-to-strong; often co-occurs with other signals**

Low-satisfaction responses frequently cite unresponsive or absent teachers:

- *"The teacher rarely responds to emails within a week."* (ED-0020, score 1)
- *"Her teacher rarely returns essays with comments. He used to love reading."* (ED-0041, score 2)
- *"The teacher rushes through concepts, doesn't respond to emails."* (ED-0095, score 2)
- *"Feedback is minimal, and her interest is dying."* (ED-0197, score 2)
- *"Assignments stack up unmarked."* (ED-0134, score 1)

Conversely, high-satisfaction responses universally praise **timely, detailed, personalized feedback** and teacher responsiveness. Teacher engagement is the clearest dividing factor between mid (3) and low (1–2) scores in many records.

**Signal words/phrases:** *rarely responds, no feedback, weeks late, grades late, never lectures, disengaged.*

---

### 6. Grade-Level Vulnerability: K-5 as a High-Risk Group
**Strength: Strong contextual signal**

A disproportionate share of score-1 records come from **K-5**, particularly in Math, Science, and English:

- ED-0003 (K-5, English, 1), ED-0008 (K-5, Math, 1), ED-0016 (K-5, Math, 1), ED-0071 (K-5, Science, 1), ED-0080 (K-5, Math, 1), ED-0115 (K-5, Science, 1), ED-0146 (K-5, English, 1), ED-0164 (K-5, Arts, 1), ED-0169 (K-5, History, 1)

Open responses from K-5 parents and teachers describe developmental mismatches: young children cannot self-regulate attention, cannot unmute reliably, require proximity for literacy and numeracy coaching, and show visible emotional distress (*"cries before every session"*, *"I want to go back to my real classroom"*).

**Signal phrases specific to K-5:** *can't unmute, wanders off, cries, can't see my paper, can't sit still, needs proximity, kindergarten chaos.*

---

### 7. Student/Parent Expressions of Prior Love and Current Loss
**Strength: Moderate signal; emotionally diagnostic**

A notable linguistic pattern in low-scoring responses is the explicit contrast between past engagement and current disengagement:

- *"I used to love history and now I just click through assignments."* (ED-0009, score 2)
- *"He used to love reading and now he hides his Kindle."* (ED-0041, score 2)
- *"I used to write stories for fun and now I can barely finish the assigned essays."* (ED-0058, score 1)
- *"She used to want to major in history; now she's reconsidering."* (ED-0197, score 2)
- *"He's been playing violin for ten years and this format makes me want to quit."* (ED-0121, score 2)

This "I used to love…now…" construction is a reliable emotional marker of deep dissatisfaction and potential long-term disengagement risk.

---

## Summary Table of Signals

| Signal | Reliability | Roles Most Affected | Subjects Most Affected |
|---|---|---|---|
| Technology failures (lag, logouts, freezes) | High | Students, Parents | Math, English, K-5 subjects |
| No peer/community interaction (silent cameras, no discussions) | Very High | All roles | English, History, Arts |
| Passive format only (worksheets/quizzes, no live instruction) | High | Parents, Students | History, English (9-12) |
| Loss of hands-on/physical component | High | Teachers, Students | Science (labs), Arts (studio/performance) |
| Teacher disengagement or missing feedback | Moderate-High | Parents, Students | History, English |
| K-5 developmental mismatch | High | Parents, Teachers | Math, Science, English |
| "I used to love…now…" framing | Moderate | Students, Parents | English, History, Arts |

---

## Exceptions and Weak Evidence

- **Subject alone is not determinative.** Math, Science, and Arts all have high-satisfaction records (4–5) when teachers adapted creatively (digital tools, mailed kits, adaptive software). Subject predicts risk only when combined with format mismatch signals.
- **Grade level is context, not destiny.** Several K-5 teachers report scores of 4–5 by using puppets, small-group video, mailed materials, and gamification (ED-0044, ED-0081, ED-0119, ED-0132, ED-0159).
- **Technology problems alone yield mixed outcomes.** ED-0007 (score 4) mentions audio cuts but still enjoys class. Technology friction is amplifying but rarely the sole cause of very low scores.
- **The dataset is self-reported and likely skewed** toward more engaged respondents, so true low-satisfaction rates among disengaged learners (e.g., students who stopped attending) may be underrepresented.

---

## Decision-Ready Summary

The open-response language that most reliably predicts low learning satisfaction (1–2) is the co-occurrence of:
1. **Absent or collapsed interactivity** (silent chats, cameras off, no discussion)
2. **Passive-only instructional format** (worksheets/quizzes without live engagement)
3. **Unresponsive or invisible teachers** (delayed feedback, no email replies)
4. **Physical-format mismatch** (labs, ensemble music, early-grade manipulatives attempted over video without creative substitutes)

The highest-risk profiles are **K-5 students in Math and Science**, **middle and high school students in lab-based Science and studio/performance Arts**, and any course where the teacher has not replaced in-person interaction with an active digital equivalent. Screening open responses for phrases like *"just worksheets," "cameras off," "no instruction," "rarely responds," "I used to love…now,"* and *"can't see/hear"* would reliably flag low-satisfaction cases before numeric scores are analyzed.
