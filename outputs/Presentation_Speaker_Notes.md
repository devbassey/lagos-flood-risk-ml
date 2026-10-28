# Presentation Deck & Slide-by-Slide Speaker Notes (14 Slides)

## Slide 1: Spatio-Temporal Prediction of Pluvial & Coastal Flood Risk in Lagos State
**Subtitle:** *A Machine Learning Approach (2010–2025) with CMIP6 Climate-Scenario Projections to 2050*

**Key Points on Slide:**
- Author: Utibe Bassey
- Data Stack: CHIRPS v2.0 Daily · USGS SRTM 30m · JRC Water 30m · ESA WorldCover 10m · WorldPop 100m · NEX-GDDP-CMIP6
- Deliverables: Master LGA-Month Dataset · Calibrated ML Pipeline · Composite Flood Risk Index · Interactive Map & Streamlit App

**Verbal Speaker Script:**
> Good day everyone. My presentation covers the Spatio-Temporal Prediction of Pluvial and Coastal Flood Risk in Lagos State, Nigeria, using satellite earth observation, machine learning, and CMIP6 climate projections to 2050. Across 9 reproducible notebooks, we built a 3,840-row LGA-by-month dataset covering all 20 LGAs from 2010 to 2025, validated our models temporally and spatially, and projected flood risk and population exposure to 2050.

---

## Slide 2: 1. Problem Statement & Motivation
**Subtitle:** *Why Lagos State Needs LGA-Level Spatio-Temporal Flood Forecasting & 2050 Risk Projections*

**Key Points on Slide:**
- Compound Flood Hazard: Lagos faces three interacting mechanisms—intense convective pluvial downpours, Ogun River / lagoon floodplain overflow, and Atlantic tidal backwater locking.
- Current Forecasting Gap: Existing national outlooks (e.g., NIHSA Annual Flood Outlook) provide broad seasonal classifications, but lack monthly probability predictions at individual LGA granularity.
- Rapid Demographic & Climate Shifts: Unplanned wetland reclamation, surging population density, intensifying extreme storms, and sea-level rise are rapidly shifting the baseline.
- Project Goal: Build an open, data-driven early-warning and long-term planning tool that predicts WHEN and WHERE Lagos floods today (2010–2025) and projects how risk evolves by 2030, 2040, and 2050.

**Verbal Speaker Script:**
> Lagos is uniquely vulnerable because low-lying barrier islands and lagoon margins meet extreme urban imperviousness. While annual outlooks exist, planners and emergency agencies like LASEMA lack a quantitative model that predicts monthly flood probabilities per LGA and quantifies how climate change and urban expansion will alter exposure by 2050.

---

## Slide 3: 2. Research Aim, Objectives & Literature Gap
**Subtitle:** *Bridging Static GIS Susceptibility Mapping and Dynamic Machine Learning Climate Projections*

**Key Points on Slide:**
- Limitation of Past Studies: Most Nigerian flood studies rely on static GIS Multi-Criteria / AHP weighting (subjective weights, cannot predict monthly timing or ingest daily CMIP6 series).
- Objective 1 & 2 (Data & EDA): Fuse multi-satellite observations (CHIRPS, SRTM, JRC, WorldCover, WorldPop) with documented flood records (2010–2025) and test physical drivers statistically.
- Objective 3 (Machine Learning): Compare Logistic Regression, Random Forest, and Monotonic XGBoost under strict chronological (2010–2020 vs 2021–2025) and spatial (Leave-One-LGA-Out) validation.
- Objective 4 & 5 (2050 Projections & FRI): Bias-correct 5 CMIP6 GCMs, integrate IPCC AR6 sea-level rise & urban growth, and rank all 20 LGAs on a Composite Flood Risk Index (FRI).

**Verbal Speaker Script:**
> Our literature review identified a clear methodological gap: traditional GIS-AHP maps in Nigeria are static in time and use subjective weights. By combining satellite time series with calibrated machine learning and physical monotonicity constraints, we can predict monthly flood probabilities and project them under IPCC AR6 scenarios.

---

## Slide 4: 3. End-to-End Geospatial & ML Data Engineering Pipeline
**Subtitle:** *Nine Reproducible Notebooks Transforming Satellite Collections into Decision Support*

**Key Points on Slide:**
- Notebooks 01–02 (Boundaries & Rainfall): GADM v4.1 20 LGAs; CHIRPS daily rain aggregated into monthly total, 1-day/3-day/7-day rolling peaks, rainy/heavy days, and lag-1 month antecedent rain.
- Notebook 03 (Topography & Hydrology): JRC permanent water mask applied FIRST so lagoon water (0m) does not bias SRTM land elevation; Euclidean distance to water computed in UTM Zone 31N.
- Notebook 04 (Target Labels): Combines DFO/MODIS Global Flood Database with 75 multi-LGA documented events (NEMA, NIHSA, LASEMA, EM-DAT, verified news) via a 150-place gazetteer.
- Notebook 05 (Exposure & Master Table): Extracts ESA WorldCover 10m (`built_share`, `wetland_mangrove_share`) and harmonised WorldPop 100m (2010–2025) into `master_lga_month.csv`.

**Verbal Speaker Script:**
> Every data engineering step was designed to avoid common geospatial biases. For example, in Notebook 03 we masked out permanent lagoon and ocean water pixels using JRC Global Surface Water before measuring SRTM land elevation. In Notebook 02, we added antecedent previous-month rainfall to capture water-table saturation.

---

## Slide 5: 4. Exploratory Analysis: Bimodal Seasonality & Antecedent Rain
**Subtitle:** *Why July Floods More Often Than June Despite Lower Average Monthly Rainfall*

**Key Points on Slide:**
- Bimodal Wet Season: Rainfall peaks in June (265.4 mm mean, 39.1% flood rate) and July (207.2 mm, 49.7% flood rate), dips in August (86.8 mm, 5.3%), and peaks again in Sept–Oct (28.1% & 13.4%).
- The Antecedent Moisture Effect: July has the highest flood probability (49.7%) because June's heavy rains saturate the soil, fill drainage canals, and elevate lagoon levels.
- Dry Season Floor: From November to April, documented flood occurrence is 0.0% across all 20 LGAs.
- Inter-Annual Peaks: Major flood years (2011, 2012, 2017, 2018, 2020, 2021, 2022, 2024, 2025) align with extreme convective storms and wet anomalies.

**Verbal Speaker Script:**
> Looking at Figure 4.1 on the right, notice a crucial physical insight: average rainfall is highest in June (265 mm), yet flood probability peaks in July at nearly 50%. That happens because of antecedent rainfall from the previous month—soils and the Lagos Lagoon are already full when July storms arrive.

---

## Slide 6: 5. Spatial Flood Archetypes Across the 20 Lagos LGAs
**Subtitle:** *Three Distinct Hydro-Topographic Flood Regimes Identified by Satellite Data*

**Key Points on Slide:**
- Archetype 1 — Coastal & Barrier-Island LGAs (Eti-Osa 35 floods, Lagos Island 28, Apapa 23, Ajeromi/Ifelodun 23): Mean land elevation 4.8–5.8m, with 39%–52% of land lying below 5m.
- Archetype 2 — Ogun River & Lagoon Floodplain LGAs (Kosofe 33 floods, Ikorodu 30 floods): Combine low-lying wetland margins (18% wetland in Kosofe) with upstream river & Oyan Dam inflows.
- Archetype 3 — High-Imperviousness Mainland LGAs (Surulere 26, Mainland 25, Mushin 20, Alimosho 19, Ikeja 18): 82%–98% paved built-up cover turns intense 1-day and 3-day storms into flash runoff.

**Verbal Speaker Script:**
> Our spatial choropleths reveal three distinct flood archetypes in Lagos: low-lying coastal islands below 5 metres elevation, riverine floodplain corridors in Kosofe and Ikorodu, and heavily paved mainland LGAs where built-up surfaces exceed 85 to 98 percent.

---

## Slide 7: 6. Statistical Hypothesis Testing & Hydro-Topographic Interactions
**Subtitle:** *Mann–Whitney U Tests & Non-Linear Amplification Between Rainfall and Elevation*

**Key Points on Slide:**
- Highly Significant Separation (p < 1e-100): Flood months have a median 2-month cumulative rainfall of 464.5 mm vs 201.2 mm in non-flood months (rank-biserial r = +0.752).
- Current-Month & 3-Day Storm Extremes: Median monthly rain is 244.0 mm on flood months vs 90.2 mm on non-flood months (r = +0.718); max 3-day storm is 69.2 mm vs 32.6 mm (r = +0.648).
- Terrain × Rainfall Interaction (Right Chart): Under 100–200 mm of monthly rain, low-lying LGAs (<8m) flood at nearly double the rate (16.5%) of upland LGAs (>20m, 8.8%).
- Extreme Wet Months (>300 mm): Flood probability reaches 66.4% in low-lying coastal LGAs and 60.4% in mid-elevation lagoon LGAs.

**Verbal Speaker Script:**
> Mann-Whitney U tests confirm that two-month cumulative rainfall, monthly rainfall, and 3-day storm intensity are statistically significant at p < 10^-100. The heatmap on the right shows that under identical rainfall, low-lying coastal LGAs below 8m flood at nearly twice the rate of upland LGAs.

---

## Slide 8: 7. Machine Learning Design & Held-Out Test Performance (2021–2025)
**Subtitle:** *Strict Temporal Split, Monotonic Constraints & 20-Fold Leave-One-LGA-Out Spatial Validation*

**Key Points on Slide:**
- Leakage-Free Validation: Trained & tuned on 2010–2020 (2,640 rows) using 5-fold expanding-window TimeSeriesSplit; tested strictly on future unseen years 2021–2025 (1,200 rows).
- Top Ranking Discrimination (Calibrated Monotonic XGBoost): Achieves Test ROC-AUC = 0.890 [0.871, 0.910] and Test PR-AUC = 0.460 [0.402, 0.534] (3.05x the Naive Baseline).
- Top Early-Warning Sensitivity (Cost-Sensitive Random Forest): Achieves Test F1 = 0.562, Recall = 71.8%, and Brier Calibration Score = 0.1070.
- 20-Fold Spatial Hold-Out (Leave-One-LGA-Out): Mean ROC-AUC of 0.902 across unseen LGAs (Shomolu 0.958, Oshodi 0.949, Agege 0.935, Alimosho 0.924, Apapa 0.924, Kosofe 0.900).

**Verbal Speaker Script:**
> To prevent data leakage, we trained strictly on 2010–2020 and evaluated on 2021–2025. Calibrated Monotonic XGBoost achieved a 0.890 Test ROC-AUC and 0.460 PR-AUC—over 3 times the naive baseline—and a 0.902 mean ROC-AUC when predicting completely unseen LGAs in Leave-One-LGA-Out cross-validation.

---

## Slide 9: 8. Model Explainability: TreeSHAP & Multi-Model Feature Importance
**Subtitle:** *Transparent Physical Rules Governing Flood Predictions Across Lagos State*

**Key Points on Slide:**
- Physical Monotonicity Enforced: XGBoost is constrained so higher rainfall, higher `low5_share`, or higher `built_share` can never paradoxically lower predicted flood probability.
- Top Temporal Drivers (SHAP): Seasonal phase (`month_cos`, `month_sin`), `rain_total_mm`, `rainy_days`, `rain_prev_month_mm` (antecedent wetness), and `rain_max_3day_mm` govern WHEN floods occur.
- Top Spatial Drivers (SHAP): `elev_mean_m`, `low5_share` (<5m land), `dist_water_mean_km`, `wetland_mangrove_share`, and `built_share` govern WHICH LGAs flood under a given storm.
- Cross-Model Agreement: Logistic Regression, Random Forest, and XGBoost agree on the top physical predictors.

**Verbal Speaker Script:**
> Using TreeSHAP, we opened the black box to verify what drives predictions. In the beeswarm plot on the right, high current-month rain, high previous-month rain, and high 3-day storm totals push flood log-odds strongly upward, while low elevation and high low5_share separate vulnerable coastal LGAs from upland ones.

---

## Slide 10: 9. Climate-Scenario Projections to 2050 (CMIP6 + SLR + Urban Growth)
**Subtitle:** *5-GCM Ensemble (`NASA/GDDP-CMIP6`) Under Moderate (SSP2-4.5) and High (SSP5-8.5) Emissions*

**Key Points on Slide:**
- 5-Model CMIP6 Ensemble: Extracted >103,000 daily records across ACCESS-CM2, GFDL-ESM4, MPI-ESM1-2-HR, MRI-ESM2-0, and UKESM1-0-LL via Google Earth Engine.
- Quantile Delta Scaling: Bias-corrected each GCM against 2010–2025 CHIRPS LGA climatology to preserve local spatial gradients and GCM extreme storm intensification.
- Compound Future Drivers: Integrated IPCC AR6 regional sea-level rise (+0.29m in SSP2-4.5; +0.40m in SSP5-8.5 by 2050) and SSP demographic & impervious built-up expansion.
- Trajectory to 2050: State mean wet-season flood probability rises from 20.18% (Baseline) to 22.30% (SSP2-4.5) and 22.68% (SSP5-8.5), with coastal & peri-urban LGAs seeing the sharpest jumps.

**Verbal Speaker Script:**
> For Phase 5, we pulled daily precipitation from 5 CMIP6 Global Climate Models on Earth Engine, bias-corrected them against our CHIRPS baseline, and added IPCC AR6 sea-level rise and urban expansion. Notice how the uncertainty fan across the 5 climate models is explicitly reported, with SSP5-8.5 diverging higher after 2040.

---

## Slide 11: 10. Composite Flood Risk Index (FRI) & Exposed Population to 2050
**Subtitle:** *Combining Hazard (0.45), Physical/Drainage Vulnerability (0.30), and Human Exposure (0.25)*

**Key Points on Slide:**
- IPCC AR6 Risk Formulation: FRI (0–100) combines model wet-season hazard probability (45%), terrain/impervious vulnerability (30%), and population exposure (25%).
- Robustness Verified: Weight sensitivity analysis across 4 weighting schemes confirms Spearman rank correlation rho = 0.92 to 0.99.
- Highest-Risk LGAs in 2050 (SSP5-8.5): #1 Lagos Island (56.5), #2 Apapa (56.2), #3 Kosofe (52.6), #4 Eti-Osa (51.8), #5 Amuwo Odofin (51.7), #6 Ajeromi/Ifelodun (51.0), #7 Mainland (49.7).
- Nearly 2 Million Residents Exposed Annually by 2050: State exposed population doubles from 993,636 (Baseline) to 1.75M (+75.8% in SSP2-4.5) and 1.98M (+99.5% in SSP5-8.5).

**Verbal Speaker Script:**
> When we combine Hazard, Vulnerability, and Exposure into the Composite Flood Risk Index, we see a dramatic escalation across Lagos State by 2050. Most importantly, the number of residents annually exposed to wet-season flood risk nearly doubles from 994,000 in the baseline to 1.98 million under SSP5-8.5.

---

## Slide 12: 11. Interactive Decision-Support Map & Streamlit Dashboard
**Subtitle:** *Standalone Leaflet HTML Explorer (`outputs/maps/`) and Live Streamlit App (`app.py`)*

**Key Points on Slide:**
- Interactive Leaflet HTML Map (`lagos_flood_risk_interactive.html`): Opens in any browser without a server; lets planners toggle across Baseline, 2030s, 2040s, and 2050 (SSP2-4.5 & SSP5-8.5).
- Streamlit Planning Dashboard (`app.py`): Four interactive tabs—(1) Interactive Map & Rankings, (2) LGA Deep-Dive & Monthly Seasonality Curve, (3) 2030–2050 Scenarios, (4) ML Metrics & SHAP.
- Largest Exposed Populations by 2050: Amuwo Odofin (266k), Badagry (227k), Eti-Osa (212k), Ojo (205k), Kosofe (136k), Apapa (129k), Alimosho (121k), and Ikorodu (119k).
- Fastest Risk Escalation (+FRI Points): Epe (+10.2), Badagry (+9.1), Ojo (+8.2), Ibeju-Lekki (+8.0), and Amuwo Odofin (+7.5) due to rapid coastal urbanisation.

**Verbal Speaker Script:**
> To make our results immediately actionable for non-technical planners, we built both a standalone Leaflet HTML map and a 4-tab Streamlit application. Planners can click any LGA, compare its seasonal flood curve between today and 2050, and inspect its exposed population.

---

## Slide 13: 12. Limitations & Methodological Transparency
**Subtitle:** *Honest Scientific Assessment of Data, Resolution, and Modelling Constraints*

**Key Points on Slide:**
- 1. Reporting Bias in Documentary Records: Media and agency logs cover major commercial corridors (Lekki, VI, Ikeja, Lagos Island) and recent years (2017–2025) more densely than peripheral settlements.
- 2. Satellite Rainfall Resolution (5.5 km): CHIRPS captures regional monsoon storms accurately but cannot resolve sub-kilometre convective micro-bursts across compact LGAs (e.g., Ajeromi, Mushin).
- 3. SRTM Canopy/Building Bias: SRTM (30m, year 2000) measures surface height rather than bare-earth LiDAR and predates post-2000 coastal sand-filling (e.g., Eko Atlantic, Lekki phases).
- 4. Unscheduled Dam Releases & Drain Blockages: Upstream Oyan Dam operations and local solid-waste blockages of street drains are unobserved in satellite data.

**Verbal Speaker Script:**
> Every rigorous machine learning study must state its limitations transparently. First, a label of 0 means no documented flood report, not guaranteed dry streets. Second, CHIRPS is 5.5 km resolution and SRTM is a year-2000 surface model. Finally, our 2050 projections hold drainage capacity fixed at current levels to show what happens without adaptation.

---

## Slide 14: 13. Actionable Policy & Engineering Recommendations
**Subtitle:** *Five Evidence-Based Interventions for LASEMA, NIHSA & Lagos Ministry of Environment*

**Key Points on Slide:**
- 1. Two-Tier Early Warning Trigger (LASEMA): Issue targeted LGA flood watches when prior 30-day rain exceeds 180 mm AND 3-day forecast rain exceeds 50 mm (calibrated model threshold tau* = 0.19).
- 2. Tidal Flap Gates & Pumped Outfalls (Lagos Island, Apapa, Eti-Osa, Ajeromi, Amuwo Odofin): Protect <5m coastal land against +0.29–0.40m sea-level rise and lagoon backwater locking.
- 3. Ogun River Floodplain Setbacks & Dam Telemetry (Kosofe & Ikorodu): Protect remaining wetlands (18% in Kosofe) and link Oyan Dam release schedules directly to community alerts.
- 4. Mandate Permeable SUDS in Expanding Corridors (Ibeju-Lekki, Ojo, Badagry, Ikorodu, Alimosho) & Biannual Pre-Peak Desilting (before May 1 and during the August Break).

**Verbal Speaker Script:**
> In conclusion, our findings translate directly into five actionable policies for Lagos State: a two-tier antecedent-plus-forecast early warning trigger, tidal flap gates for coastal LGAs below 5 metres, automated Oyan Dam telemetry for Kosofe and Ikorodu, permeable drainage mandates in fast-growing corridors, and biannual channel desilting before May and during the August Break. Thank you, and I welcome your questions.

---
