---
dataset: airlines_review
scenario: eda_rating_drivers
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: exploratory_data_analysis
focus_variable: "Overall Rating"
query: "Across Type of Traveller and Class, which review themes are associated with higher vs. lower Overall Rating?"
source_table: augment_table/airlines_review/eda_rating_drivers/original.csv
generated_at: 2026-07-26T12:49:50.989788+00:00
wall_seconds: 130.12
---

# Review Theme Drivers of Overall Rating: Airlines Dataset
**Dataset:** 900 reviews | **Focus variable:** Overall Rating (1–10, mean 6.5)

---

## 1. The Dominant Driver: Value For Money

Across all traveller types and cabin classes, **Value For Money** is by far the strongest predictor of Overall Rating (correlation = **0.886**). The other rated dimensions — Seat Comfort (0.01), Staff Service (0.07), Food & Beverages (0.09), and Inflight Entertainment (−0.03) — show negligible linear correlation with Overall Rating.

**Value For Money distribution confirms this cleanly:**

| Rating Tier | VfM = 1 | VfM = 2 | VfM = 3 | VfM = 4 | VfM = 5 |
|---|---|---|---|---|---|
| Low (1–4) | 61.2% | 22.5% | 12.4% | 3.5% | 0.4% |
| Mid (5–7) | 5.1% | 15.3% | 40.9% | 31.2% | 7.4% |
| High (8–10) | 0.0% | 0.2% | 4.7% | 34.1% | 60.9% |

Low-rated reviews are overwhelmingly concentrated at VfM = 1; high-rated reviews at VfM = 4–5.

---

## 2. Review Text Themes: High vs. Low Overall Rating

Keyword analysis of free-text reviews reveals themes that are disproportionately present in high (≥8) vs. low (≤4) scoring reviews:

| Theme | High Rating (≥8) | Low Rating (≤4) | Difference |
|---|---|---|---|
| Inflight Entertainment | 54.7% | 27.1% | **+27.6 pp** |
| Food & Beverages | 75.8% | 52.3% | **+23.4 pp** |
| Staff / Crew | 92.9% | 71.3% | **+21.6 pp** |
| Seat / Comfort | 64.6% | 51.2% | +13.4 pp |
| Cleanliness | 13.1% | 5.0% | +8.1 pp |
| Boarding | 47.4% | 43.4% | +4.0 pp |
| Delay / Punctuality | 29.2% | 32.2% | −3.0 pp |
| Baggage | 13.5% | 17.8% | −4.3 pp |
| Value / Price | 13.1% | 24.4% | **−11.3 pp** |

**Higher-rating themes:** Passengers giving high ratings frequently discuss **crew/staff positively**, praise **food quality**, highlight **entertainment options**, and note **cleanliness**. High-rating reviews average 2.3 positive sentiment words vs. 0.6 in low-rating reviews.

**Lower-rating themes:** Reviews with low ratings over-index on **value/price complaints** (24.4% vs. 13.1%) and **delays/punctuality** (32.2% vs. 29.2%), and contain 3.7× more negative sentiment words (0.93 vs. 0.25 avg per review).

---

## 3. Patterns by Type of Traveller

| Traveller Type | Mean Rating | Rec. Rate | Mean VfM | Dominant Low-rating driver |
|---|---|---|---|---|
| Solo Leisure | **6.87** | 69.9% | **3.66** | Relatively satisfied |
| Family Leisure | 6.57 | 64.4% | 3.43 | — |
| Couple Leisure | 6.37 | 59.9% | 3.31 | — |
| Business | **5.99** | 59.6% | **3.18** | Lowest VfM satisfaction |

**Business travellers** rate the lowest overall (mean 5.99) and have the lowest Value For Money scores (3.18). Their reviews more frequently mention value/price dissatisfaction, likely reflecting higher fare sensitivity or unmet premium service expectations. **Solo Leisure** travellers are the most satisfied segment, rating highest across all dimensions.

Sub-rating means are broadly similar across traveller types (all seat comfort ~3.5–3.7, staff service ~3.9–4.0), suggesting the **overall rating gap is driven primarily by value perception**, not operational service differences.

---

## 4. Patterns by Cabin Class

| Class | Mean Rating | Rec. Rate | Mean VfM | Mean Staff Service |
|---|---|---|---|---|
| First Class | **7.93** | 78.6% | **4.21** | 3.71 |
| Business Class | 7.10 | 71.7% | 3.67 | 4.02 |
| Economy Class | 6.37 | 62.0% | 3.40 | 3.89 |
| Premium Economy | **5.83** | 58.1% | **2.94** | 4.02 |

**First Class** delivers the highest Overall Rating (7.93) driven by the strongest VfM scores (4.21) — passengers feel they get fair value for the premium. **Premium Economy** is the notable outlier: despite comparable staff service scores (4.02), it has the lowest mean VfM (2.94) and lowest overall rating (5.83). Reviews in this class suggest **passengers feel Premium Economy is overpriced relative to the marginal improvement over Economy**, making value disappointment the dominant negative theme.

**Business Class** ratings vary significantly by traveller type: Business travellers in Business Class rate it 6.21, while Couple/Family/Solo Leisure travellers in the same cabin rate it 7.37–7.41, suggesting leisure travellers treat it as a treat while business travellers hold it to higher functional standards.

---

## 5. Interaction: Traveller × Class

| | Business Class | Economy Class | Premium Economy |
|---|---|---|---|
| Business | 6.21 | 6.04 | 4.50 |
| Couple Leisure | 7.40 | 6.06 | 5.37 |
| Family Leisure | 7.41 | 6.30 | 6.73 |
| Solo Leisure | 7.37 | 6.71 | 6.47 |

The **Business traveller × Premium Economy** cell (mean 4.50, n is small) represents the lowest-satisfaction combination — likely a cost-cutting segment that still expects consistent business-grade delivery. The **leisure segments in Business Class** (~7.4) are consistently more positive than Business travellers in the same cabin.

---

## 6. Summary: Key Themes by Rating Direction

| Rating Direction | Primary Drivers |
|---|---|
| **Higher Overall Rating** | High Value for Money score; positive crew/staff mentions; food praise; entertainment satisfaction; cleanliness |
| **Lower Overall Rating** | Low Value for Money score; explicit price/value complaints; delay/punctuality mentions; seat discomfort narratives |
| **Segment risk** | Business travellers (any class), Premium Economy passengers — lowest VfM satisfaction |
| **Weak evidence** | Inflight Entertainment sub-rating shows near-zero correlation with overall score despite text frequency gap; Seat Comfort similarly weak as a numeric predictor |

> **Caveat:** Text theme frequencies reflect mention rates, not sentiment direction. A review mentioning "crew" may praise or criticize staff; the overall pattern holds because high-rating reviews use positive sentiment words 3.9× more often.
