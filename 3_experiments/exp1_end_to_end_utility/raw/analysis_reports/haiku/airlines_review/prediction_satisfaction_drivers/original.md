---
dataset: airlines_review
scenario: prediction_satisfaction_drivers
variant: original
model: substrate-claude-haiku-4-5
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating"
query: "What drives customer satisfaction (Overall Rating) across the different airlines?"
source_table: augment_table/airlines_review/prediction_satisfaction_drivers/original.csv
source_report: dataset_portion_2/substrate-claude-haiku-4-5/airlines_review__prediction_satisfaction_drivers/analyses/original/analysis.md
wall_seconds: 60.15
---

# Customer Satisfaction Drivers in Airline Reviews

## Executive Summary

This analysis examines what drives customer satisfaction (Overall Rating) across airlines in a dataset of 943 verified and unverified reviews. Five primary service dimensions are evaluated: Seat Comfort, Staff Service, Food & Beverages, Inflight Entertainment, and Value for Money.

## Data Overview

- **Total Reviews:** 943
- **Rating Scale:** Overall Rating ranges from 1-10
- **Feature Scale:** Individual service dimensions rated 1-5

## Primary Satisfaction Drivers

### Strongest Correlation with Overall Satisfaction

**1. Staff Service** (Strongest Driver)
   - Consistently mentioned as critical to satisfaction across all review segments
   - Reviews with high ratings frequently highlight "professional," "friendly," "attentive," and "helpful" cabin crew
   - Examples of positive mentions: "cabin crew truly went above and beyond," "staff extremely helpful," "crew were fantastic"
   - Negative mentions significantly impact ratings: "crew were rude," "crew not attentive," "staff disorganized"
   - **Insight:** Cabin crew quality appears to be the most influential factor differentiating highly satisfied customers from dissatisfied ones

**2. Seat Comfort** (Strong Driver)
   - Long-haul passengers particularly sensitive to seat design and recline functionality
   - Business Class seat comfort generates strong opinions: praise for "comfortable beds," complaints about "hard seats," "cramped," or "uncomfortable"
   - Economy passengers note legroom, recline functionality, and support
   - Regional Business Class seats frequently criticized as "uncomfortable and cramped"
   - **Insight:** Seat design directly impacts satisfaction, especially for premium cabin classes and long flights

**3. Value for Money** (Strong Driver)
   - Clear differentiation between satisfied and dissatisfied customers
   - Customers who feel overpaying for services deliver low ratings despite good service
   - Premium cabin passengers expect premium food, amenities, and service—gaps here drive dissatisfaction
   - Economy passengers more satisfied when extras (free meals, entertainment) exceed expectations
   - **Insight:** Price-to-service ratio significantly influences overall satisfaction perception

### Secondary Drivers

**4. Food & Beverages** (Moderate-to-Strong Driver)
   - Quality and variety consistently mentioned
   - Business Class passengers particularly critical: "mediocre meals," "food below standard," "cold food"
   - Positive mentions: "food was very good," "delicious," "high quality with choices"
   - Quantity issues noted: "small portions," "limited options," running out of certain dishes
   - Vegetarian and special dietary accommodations impact satisfaction
   - **Insight:** Meal service represents a clear differentiator, especially in premium cabins

**5. Inflight Entertainment (IFE)** (Moderate Driver)
   - Becomes more important on longer flights
   - Technical issues (freezing screens, poor connectivity) noted but not primary complaint
   - Movie/content selection mentioned: praise for "excellent selection" or criticism for "limited options"
   - Less central to satisfaction than crew service and comfort
   - **Insight:** IFE serves as a supporting amenity but is rarely the primary satisfaction driver

## Satisfaction Patterns by Key Segments

### By Travel Class

**Business/Premium Cabin:**
- Higher expectations for all dimensions
- Seat comfort and food quality generate strong satisfaction/dissatisfaction
- Staff service excellence is expected baseline
- Amenities (hot towels, slippers, amenity kits) matter significantly
- Value perception critical—premium pricing expectations high

**Economy Class:**
- Staff service remains critical but expectations lower
- Seat comfort still important but space constraints accepted
- Unexpected amenities (free meals, entertainment) boost satisfaction significantly
- Value for money often the primary satisfaction driver
- Generally higher tolerance for basic service

### By Trip Type

**Long-Haul Flights:**
- Seat comfort becomes paramount (sleeping difficulty major complaint)
- Staff service for attentiveness during extended flights highly valued
- Food quality and meal timing critical
- IFE importance increases

**Short-Haul Flights:**
- Efficient, smooth boarding/service appreciated
- Staff friendliness and professionalism still key
- Expectations for extended service lower

## Key Exceptions and Nuances

1. **Cost-Cutting Measures Impact:** Recent reviews note elimination of hot towels, pre-packed meals, and amenity kits—these reductions generate disproportionate dissatisfaction among frequent flyers and premium passengers despite maintained flight operations

2. **Operational Failures Override Service Excellence:** Luggage delays, missed connections, and booking system issues create low satisfaction scores even when cabin crew service is excellent

3. **Aircraft Type Matters:** Newer aircraft (A350, A380) generally rated higher for comfort; specific seat configurations significantly affect reviews

4. **Individual Expectations Vary:** Same flight receives both 10/10 and 1/10 ratings—suggesting passenger expectations and specific service interactions drive perception more than objective service levels

## Summary of Drivers by Relative Importance

| Rank | Driver | Correlation Strength | Notes |
|------|--------|----------------------|-------|
| 1 | Staff Service | Very Strong | Most consistent satisfaction differentiator |
| 2 | Seat Comfort | Strong | Particularly for long-haul/premium |
| 3 | Value for Money | Strong | Price-to-service ratio critical |
| 4 | Food & Beverages | Moderate-Strong | Quality and quantity matter |
| 5 | Inflight Entertainment | Moderate | Supporting factor, not primary driver |

## Recommendations for Improving Satisfaction

1. **Prioritize Cabin Crew Training & Engagement:** Invest heavily in staff professionalism, attentiveness, and warmth—this is the most consistent satisfaction driver

2. **Maintain Premium Seat/Service Standards:** Cost-cutting in premium cabins directly backfires; maintain expected standards for paid premium

3. **Align Price with Service Delivery:** Ensure pricing matches service quality delivered, particularly for economy premium upgrades

4. **Focus on Meal Quality Over Quantity:** Food presentation and quality consistently mentioned; pre-packed meals generate negative sentiment

5. **Address Operational Reliability:** Luggage handling, connection management, and booking system reliability must support flight service quality

---

**Variant:** original  
**Analysis Date:** 2026-06-17
