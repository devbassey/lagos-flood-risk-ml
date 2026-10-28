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
> Lagos State is home to over 15 to 20 million people squeezed onto a fragile barrier-lagoon complex where roughly half of several urban LGAs sit less than 5 metres above sea level. Every rainy season, compound flooding causes billions of Naira in damage and severe social disruption. While NIHSA provides national annual outlooks, decision-makers lack an open, monthly predictive model that can guide operational early warnings and mid-century urban resilience capex.

---

## Slide 3: 2. End-to-End System Architecture
**Subtitle:** *Nine Modular Jupyter Notebooks from Multi-Sensor Earth Observation to Deployed Decision Support*

**Key Points on Slide:**
- Notebooks 01–03: Vector boundary harmonization (GADM v4.1, 20 LGAs); CHIRPS daily precipitation aggregation (5,844 days); SRTM 30m elevation masked by JRC surface water (occurrence >= 50%) to isolate terrestrial elevation.
- Notebooks 04–05: 75 multi-LGA historical flood logs (2010–2025, 423 positive LGA-months = 11.02%); ESA WorldCover 10m land cover; WorldPop 100m spliced demographics; master_lga_month.csv (3,840 rows × 40 columns).
- Notebooks 06–07: Exploratory data analysis; Mann–Whitney U non-parametric tests; temporal split (2010–2020 train vs 2021–2025 test); 20-fold Leave-One-LGA-Out spatial CV; calibrated monotonic XGBoost; TreeSHAP explainability.
- Notebooks 08–09: NASA NEX-GDDP-CMIP6 5-GCM daily downscaling (103,000+ records) under SSP2-4.5 and SSP5-8.5; IPCC AR6 sea-level rise (+0.29–0.40m); composite Flood Risk Index (FRI); interactive Leaflet map & Streamlit dashboard.

**Verbal Speaker Script:**
> This slide summarizes our end-to-end 9-notebook architecture. We ingested satellite Earth observation data at native resolutions—5.5 km CHIRPS precipitation, 30m SRTM digital elevation, 30m JRC surface water, 10m ESA WorldCover, and 100m WorldPop demographics. Crucially, we applied JRC water masking to SRTM elevation so the Lagos Lagoon does not artificially depress land elevation to 0 metres, and built a curated 16-year flood record across 150 local community gazetteers.

---

## Slide 4: 3. Spatio-Temporal EDA: Seasonality & Inter-Annual Trends
**Subtitle:** *Bimodal Monsoonal Curve, Antecedent Rainfall Lag, and the August Break (2010–2025)*

**Key Points on Slide:**
- Bi-Modal Seasonality: Lagos exhibits two wet-season peaks driven by the West African Monsoon—a primary surge in May–July and a secondary resurgence in September–October.
- Antecedent Moisture Multiplier: While June has the highest monthly rainfall (265.4 mm), flood frequency peaks in July (49.7% of all LGA-months) because soils, drainage canals, and the lagoon are already saturated from June.
- Dry Season Baseline: From November through April, recorded flood occurrence drops to 0.0% across all 20 LGAs.

**Verbal Speaker Script:**
> Looking at our exploratory data analysis in Slide 4, Figure 4.1 illustrates the bimodal seasonality of Lagos rainfall. Notice the critical hydrological insight: monthly rainfall peaks in June at 265.4 mm, but flood occurrence peaks in July at nearly 50% of LGAs. Why? Because June rains saturate the soil and fill the lagoon, leaving zero infiltration capacity for July storms. August brings the Little Dry Season break, followed by a secondary flood peak in September and October as upstream Ogun River water flows into the state.

---

## Slide 5: 4. Spatio-Temporal EDA: Physical Geography of the 20 LGAs
**Subtitle:** *Choropleths of Low-Lying Coastal Land, Water Proximity, Impervious Cover & Historical Floods*

**Key Points on Slide:**
- Coastal & Tidal Hotspots: Eti-Osa (35 flood months), Lagos Island (28), Apapa (23), and Ajeromi/Ifelodun (23) combine extreme low elevation (40%–52% of land <5m) with direct lagoon and ocean frontage.
- Riverine & Lagoon Floodplain: Kosofe (33 flood months) and Ikorodu (30) sit along the lower Ogun River corridor, where river overflow compounds heavy rainfall.
- Impervious Mainland Runoff: Core mainland LGAs (Surulere, Mushin, Mainland, Agege, Oshodi/Isolo) have up to 98% impervious built-up cover, triggering rapid pluvial street flash-floods.

**Verbal Speaker Script:**
> Slide 5 maps the physical geography of Lagos's 20 LGAs. In Panel 1, historical flooding concentrates heavily in coastal and lagoon-front LGAs: Eti-Osa leads with 35 documented flood months, followed by Kosofe with 33, Ikorodu with 30, and Lagos Island with 28. Panels 2 through 4 explain why: coastal LGAs have up to 52% of land below 5 metres, while mainland LGAs like Surulere and Mushin exceed 95% impervious concrete cover, preventing any natural stormwater infiltration.

---

## Slide 6: 5. Compound Flooding Nexus & Saturation Thresholds
**Subtitle:** *How Antecedent Rainfall, Low Elevation, and Urban Imperviousness Interact Non-Linearly*

**Key Points on Slide:**
- Soil Saturation Multiplier (Panel A): In low-lying coastal/lagoon LGAs (<5m elevation), exceeding 300 mm of 60-day rainfall (rain_2m_cum_mm) causes empirical flood probability to jump nearly 7-fold from 8.2% to 54.5%.
- Upland Runoff Independence: In upland LGAs (>20m), flood occurrence is driven by high imperviousness (>80%) and 1-day storm cloudbursts (Rx1day) overwhelming secondary street drains.
- Tidal Backwater Locking: High water in the Lagos Lagoon prevents gravity drainage channels from discharging, converting localized rainstorms into prolonged neighborhood inundations.

**Verbal Speaker Script:**
> Slide 6 presents our analysis of compound flooding mechanics in Lagos. Panel A shows that crossing 300 mm of cumulative 60-day rainfall acts as a critical tipping point in coastal and lagoon LGAs, jumping flood probability to 54.5%. Panel B separates the 20 LGAs into three clear operational archetypes: tidal lowlands, paved upland catchments, and rapidly expanding peri-urban zones.

---

## Slide 7: 6. Non-Parametric Hypothesis Testing & Physical Interactions
**Subtitle:** *Mann–Whitney U Tests (r_rb up to +0.752) and Non-Linear Elevation × Rainfall Matrix*

**Key Points on Slide:**
- Mann–Whitney U Statistical Tests: Comparing 423 flood months against 3,417 non-flood months reveals that antecedent cumulative rainfall (rain_2m_cum_mm) exhibits the single highest effect size (+0.752).
- Non-Linear Terrain Interaction: As shown in Figure 4.4, low-elevation LGAs (<8m) experience high flood rates (35%–62%) whenever monthly rainfall exceeds 200 mm.
- Upland Flash Resilience: Upland LGAs (>20m elevation) require rainfall exceeding 300 mm combined with extreme 3-day cloudbursts before widespread flooding occurs.

**Verbal Speaker Script:**
> In Slide 7, we present the statistical validation of our feature set. Because hydrological data is heavily skewed, we used two-sided Mann–Whitney U tests. Notice that 60-day antecedent rainfall achieves a massive effect size of plus 0.752, outranking current-month rainfall alone. The interaction heatmap in Figure 4.4 demonstrates that coastal LGAs flood at nearly double the rate of upland LGAs under identical rainfall volumes.

---

## Slide 8: 7. Leakage-Free Validation Architecture & Monotonic ML
**Subtitle:** *Out-of-Time Testing (2021–2025), TimeSeriesSplit, and Domain Monotonic Constraints*

**Key Points on Slide:**
- Strict Out-of-Time Hold-Out: The model is trained strictly on 2010–2020 and evaluated on 2021–2025. All scalers, hyperparameters, calibrators, and decision thresholds are fit exclusively on training data.
- Leave-One-LGA-Out (LOLO) Spatial CV: Evaluates spatial generalisation by training on 19 LGAs and testing on the held-out LGA across 20 distinct spatial folds.
- Domain Monotonic Constraints (+1 / -1): Enforced on XGBoost so predicted flood risk strictly increases with rainfall, low elevation, and built-up cover, and strictly decreases with elevation, slope, and water distance.
- Sigmoid Probability Calibration: Platt scaling aligns predicted probabilities with empirical event frequencies, lowering the Brier score to 0.1070–0.1092.

**Verbal Speaker Script:**
> Slide 8 outlines our modeling and validation design. To prevent temporal data leakage, we split our panel strictly into a 2010–2020 training set and an out-of-time 2021–2025 test set. We used 5-fold expanding-window TimeSeriesSplit for hyperparameter tuning. Crucially, we enforced domain monotonic constraints on XGBoost: flood risk must physically increase with rainfall and imperviousness, and decrease with elevation. This mathematical guarantee prevents decision trees from learning erratic, non-physical splits when extrapolating to 2050 climate scenarios.

---

## Slide 9: 8. Model Evaluation on Held-Out Test Set (2021–2025)
**Subtitle:** *Benchmark Comparison: Climatology, Logistic Regression, Random Forest & Calibrated XGBoost*

**Key Points on Slide:**
- Predictive Superiority: Calibrated Monotonic XGBoost achieves the highest Test ROC-AUC (0.890) and highest Test PR-AUC (0.460, 95% CI: [0.402, 0.534]).
- High Recall Benchmark: Cost-sensitive Random Forest achieves 71.8% Recall on historical flood months with a Test F1-score of 0.562.
- Calibrated Probabilities: As seen in Figure 5.1 (right panel), calibrated probabilities track the ideal 45-degree diagonal closely, ensuring reliable risk index inputs.

**Verbal Speaker Script:**
> Slide 9 displays our quantitative results on the held-out 2021–2025 test period. Calibrated Monotonic XGBoost achieves a Test ROC-AUC of 0.890 and a PR-AUC of 0.460, representing a 3.05-fold lift over the naive baseline. Cost-sensitive Random Forest achieves 71.8% recall on actual flood events. The reliability diagram in Figure 5.1 confirms that our calibrated probabilities closely mirror true empirical flood frequencies.

---

## Slide 10: 9. WMO-No. 1201 Verification & Residual Spatial Independence
**Subtitle:** *Decomposed Brier Score & Global Moran's I Proving Zero Residual Spatial Bias*

**Key Points on Slide:**
- WMO Forecast Verification: Evaluated under WMO-No. 1201 guidelines on the held-out 2021–2025 period. Random Forest achieves BSS = +16.5% and CSI = 0.390; Monotonic XGBoost achieves BSS = +14.8% with the lowest False Alarm Ratio (0.478).
- Spatial Residual Independence: Raw flood labels exhibit positive spatial clustering (Moran's I = +0.028, z = 1.99). Our model predictions reproduce this footprint (I = +0.127, p = 0.012).
- Zero Spatial Confounding: Model prediction residuals (e = y - p) have a Moran's I of -0.0482 (p = 0.603), proving that our hydro-topographic features completely account for spatial autocorrelation.

**Verbal Speaker Script:**
> Slide 10 benchmarks our models against World Meteorological Organization standard WMO-No. 1201. Random Forest delivers a Brier Skill Score of +16.5% and a Critical Success Index of 0.390, while XGBoost achieves the lowest false alarm ratio of 47.8%. In Panel B, Global Moran's I on model residuals is -0.048 with p = 0.603, proving that our model errors are spatially independent with zero spatial confounding.

---

## Slide 11: 10. Spatial Transferability Map (Leave-One-LGA-Out CV)
**Subtitle:** *Generalisation Performance when Trained on 19 LGAs and Tested on 1 Unseen Territory*

**Key Points on Slide:**
- Zero Spatial Leakage: Each LGA was completely held out in turn during training, evaluating whether the model can predict flood history in an unseen territory solely from its physical attributes.
- High Transfer in Mature Cores: Shomolu (0.958), Oshodi/Isolo (0.949), Agege (0.935), Apapa (0.924), and Mushin (0.923) achieve remarkable generalisation skill.
- The Peri-Urban Challenge: Ibeju-Lekki exhibits lower PR-AUC (0.289) due to post-2018 industrial transformation (Dangote Refinery, Lekki Deep Sea Port) shifting its baseline rapidly.

**Verbal Speaker Script:**
> Slide 11 demonstrates spatial generalisation across all 20 LGAs using Leave-One-LGA-Out cross-validation. The model achieves an outstanding mean ROC-AUC of 0.902 across unseen LGAs. Transferability is highest in mature built-up corridors like Shomolu and Oshodi, while rapidly developing corridors like Ibeju-Lekki underscore the need for annual satellite land-cover monitoring.

---

## Slide 12: 11. Model Explainability: TreeSHAP Feature Attributions
**Subtitle:** *Why 60-Day Antecedent Rainfall and Low Elevation Govern Lagos Flood Probability*

**Key Points on Slide:**
- Dominance of Antecedent Rainfall: TreeSHAP reveals that rain_2m_cum_mm is nearly 3x more impactful than current-month rainfall alone, explaining the July peak.
- Terrain & Imperviousness Thresholds: High low5_share (<5m elevation) and high built_share (>80%) push log-odds of flooding sharply upward.
- Protective Nature Buffers: High wetland_mangrove_share and distance from permanent water (dist_water_mean_km) exert negative SHAP forces, acting as natural flood attenuation buffers.

**Verbal Speaker Script:**
> Slide 12 opens the black box using TreeSHAP game-theoretic explainability. The beeswarm plot demonstrates that 60-day cumulative rainfall is by far the single most decisive driver—nearly three times more influential than current-month rainfall alone. Low-lying terrain and urban imperviousness strongly push predictions toward flooding, while wetlands and mangrove buffers pull predictions back downward.

---

## Slide 13: 12. CMIP6 Monsoon Seasonality Shifts & Convective Extremes
**Subtitle:** *Projected Shifts in West African Monsoon Cycles & 3-Day Storm Intensity by 2050*

**Key Points on Slide:**
- Monsoon Seasonality Expansion: Under SSP5-8.5 by 2050, mean June rainfall rises to 288.5 mm (+8.7%) and July rises to 226.4 mm (+9.3%), with the October secondary shoulder expanding by +11.2%.
- Clausius–Clapeyron Intensification: Atmospheric warming increases convective cloudburst intensity (~7% / K). Mean 3-day extreme storms (Rx3day) rise from 61.4 mm to 69.8 mm in coastal LGAs and from 59.8 mm to 68.3 mm in lagoon corridors.
- Compounding Sea-Level Rise: This rainfall surge coincides with +0.29m (SSP2-4.5) to +0.40m (SSP5-8.5) of coastal sea-level rise and 2 mm/yr coastal subsidence.

**Verbal Speaker Script:**
> Slide 13 examines the physical shifts in the West African Monsoon projected by our 5-GCM CMIP6 ensemble. In Panel A, both June and July rainfall peaks expand by ~9%, while the October season lengthens. In Panel B, thermodynamic warming increases maximum 3-day storm intensity by 10% to 14% across all geomorphic zones, compounding coastal sea-level rise.

---

## Slide 14: 13. 2030–2050 Climate Projections: 5 GCMs & Sea-Level Rise
**Subtitle:** *NEX-GDDP-CMIP6 Ensemble, Quantile Delta Mapping, and IPCC AR6 Gulf of Guinea SLR*

**Key Points on Slide:**
- GCM Bias Correction: Delta-ratio quantile scaling against 2010–2025 CHIRPS baseline preserves spatial rainfall gradients and multi-model uncertainty envelopes.
- Sea-Level Rise Coupling: Regional SLR (+0.29m under SSP2-4.5; +0.40m under SSP5-8.5 by 2050) depresses effective land elevation and expands low-lying area.
- Flood Hazard Growth: State-wide wet-season flood probability increases from 20.18% in the baseline period to 22.30% (SSP2-4.5) and 22.68% (SSP5-8.5) by 2050.

**Verbal Speaker Script:**
> In Slide 14, we project flood hazard through 2050 across a 5-GCM CMIP6 ensemble downscaled with Quantile Delta Mapping. We coupled regional sea-level rise—reaching plus 29 centimetres under SSP2-4.5 and plus 40 centimetres under SSP5-8.5—directly into our digital elevation model. State-wide wet-season flood probability rises from 20.18% historically to 22.68% by 2050, adding an average of nearly 2.5 additional flood weeks per LGA per year.

---

## Slide 15: 14. Multi-Decadal Flood Risk Index Trajectory Matrix (2010–2050)
**Subtitle:** *Tracking the Composite Flood Risk Index (FRI) across All 20 LGAs through Mid-Century*

**Key Points on Slide:**
- Tier 1 Persistent Hotspots: Lagos Island (56.5), Apapa (56.2), Kosofe (52.6), Eti-Osa (51.8), Amuwo Odofin (51.7), and Ajeromi/Ifelodun (51.0) anchor the high-risk category by 2050.
- Fastest Escalating Corridors: The steepest increases in FRI occur in Amuwo Odofin (+7.5), Ojo (+8.2), Badagry (+9.1), and Epe (+10.2), driven by rapid wetland conversion combined with rising sea levels.
- Multi-Epoch Planning: Provides urban planners with a transparent roadmap of how risk unfolds in the 2030s, 2040s, and 2050 under both moderate and high-emissions pathways.

**Verbal Speaker Script:**
> Slide 15 presents our comprehensive 20-LGA multi-decadal risk trajectory matrix. Six LGAs cross into the High-Risk category (FRI > 50) by 2050 under SSP5-8.5. Importantly, the matrix highlights rapidly escalating corridors like Amuwo Odofin, Badagry, and Epe, where rapid demographic growth and wetland paving accelerate risk faster than in mature city centers.

---

## Slide 16: 15. Composite Flood Risk Index (FRI) Spatial Shift to 2050
**Subtitle:** *Combining Hazard (H), Vulnerability (V), and Exposure (E) across Scenarios*

**Key Points on Slide:**
- IPCC AR6 Formulation: FRI = 100 × (0.45 Hazard + 0.30 Vulnerability + 0.25 Exposure), integrating calibrated ML probability, low-elevation terrain, and gridded population.
- Weight Sensitivity Verification: Testing four weighting schemes confirmed Spearman rank correlations of 0.92 to 0.99, proving LGA rankings are robust to weight selection.
- Spatial Risk Expansion: By 2050 under SSP5-8.5, high flood risk (FRI >= 45) spreads from the coastal core into peripheral LGAs like Ojo and Badagry.

**Verbal Speaker Script:**
> Slide 16 maps our Composite Flood Risk Index from baseline to 2050 under SSP2-4.5 and SSP5-8.5. Following IPCC AR6 guidelines, FRI weights Hazard at 45%, Physical Vulnerability at 30%, and Human Exposure at 25%. Sensitivity analysis confirmed rank stability across all alternative weights with Spearman correlations above 0.92. Notice how high risk expands westward along Badagry Creek and eastward into the Lekki peninsula by mid-century.

---

## Slide 17: 16. Population Exposed to Flood Risk: Baseline vs 2050
**Subtitle:** *Exposed Population Nearly Doubles from 0.99 Million to 1.98 Million Residents/Year*

**Key Points on Slide:**
- Doubling of Human Exposure: Rapid urban demographic expansion amplifies climate impacts, nearly doubling exposed residents from 993,636 to 1,982,207 by 2050 under SSP5-8.5.
- Fastest Growing Exposure: Amuwo Odofin (+117% exposed residents), Badagry (+162%), Ojo (+144%), and Ikorodu (+98%) experience massive exposure spikes as populations move into floodplains.
- Alimosho Exposure Paradox: While Alimosho has a moderate FRI score (39.2), its massive population (over 2 million by 2050) means over 120,000 residents will be exposed annually.

**Verbal Speaker Script:**
> Slide 17 delivers one of our most critical policy findings: total human exposure. While hazard rates increase by 10 to 15%, population growth causes total exposed residents to nearly double from 993,000 today to 1.98 million people per year by 2050 under SSP5-8.5. Corridors like Amuwo Odofin, Badagry, and Ojo see exposure climb by 117% to 162%.

---

## Slide 18: 17. Operational Early-Warning Frontier & Cost-Loss Optimization
**Subtitle:** *Economic Decision Support for LASEMA & NIHSA Alert Threshold Tuning*

**Key Points on Slide:**
- Operational Trade-Off Curve (Panel A): Shows how Probability of Detection (POD), False Alarm Ratio (FAR), and Critical Success Index (CSI) evolve across alert thresholds (0.05 to 0.60).
- Cost-Loss Economic Curve (Panel B): Balances preventive protection cost (C) against unmitigated disaster loss (L). For a standard municipal ratio (C/L = 0.20), the minimum-expense threshold occurs at tau = 0.21.
- Multi-Tier Emergency Protocol: Recommends tau = 0.19 for public works drainage desilting and community advisory notices, and tau = 0.38 for mobilizing emergency boat evacuations and school closures.

**Verbal Speaker Script:**
> Slide 18 provides concrete economic decision-support for operational emergency management. Panel A plots the verification frontier across decision thresholds. Panel B applies cost-loss decision theory to find the optimal threshold (tau = 0.21) that minimizes total municipal disaster expense. We recommend a two-tier alert protocol: tau = 0.19 for drainage advisories, and tau = 0.38 for high-certainty emergency deployments.

---

## Slide 19: 18. Limitations & Methodological Transparency
**Subtitle:** *Honest Scientific Assessment of Data, Resolution, and Modelling Constraints*

**Key Points on Slide:**
- 1. Reporting Bias in Documentary Records: Media and agency logs cover major commercial corridors (Lekki, VI, Ikeja, Lagos Island) and recent years (2017–2025) more densely than peripheral settlements.
- 2. Satellite Rainfall Resolution (5.5 km): CHIRPS captures regional monsoon storms accurately but cannot resolve sub-kilometre convective micro-bursts across compact LGAs (e.g., Ajeromi, Mushin).
- 3. SRTM Canopy/Building Bias: SRTM (30m, year 2000) measures surface height rather than bare-earth LiDAR and predates post-2000 coastal sand-filling (e.g., Eko Atlantic, Lekki phases).
- 4. Unscheduled Dam Releases & Drain Blockages: Upstream Oyan Dam operations and local solid-waste blockages of street drains are unobserved in satellite data.

**Verbal Speaker Script:**
> Every rigorous machine learning study must state its limitations transparently. First, a label of 0 means no documented flood report, not guaranteed dry streets. Second, CHIRPS is 5.5 km resolution and SRTM is a year-2000 surface model. Finally, our 2050 projections hold drainage capacity fixed at current levels to show what happens without adaptation.

---

## Slide 20: 19. Actionable Policy & Engineering Recommendations
**Subtitle:** *Five Evidence-Based Interventions for LASEMA, NIHSA & Lagos Ministry of Environment*

**Key Points on Slide:**
- 1. Two-Tier Early Warning Trigger (LASEMA): Issue targeted LGA flood watches when prior 30-day rain exceeds 180 mm AND 3-day forecast rain exceeds 50 mm (calibrated model threshold tau* = 0.19).
- 2. Tidal Flap Gates & Pumped Outfalls (Lagos Island, Apapa, Eti-Osa, Ajeromi, Amuwo Odofin): Protect <5m coastal land against +0.29–0.40m sea-level rise and lagoon backwater locking.
- 3. Ogun River Floodplain Setbacks & Dam Telemetry (Kosofe & Ikorodu): Protect remaining wetlands (18% in Kosofe) and link Oyan Dam release schedules directly to community alerts.
- 4. Mandate Permeable SUDS in Expanding Corridors (Ibeju-Lekki, Ojo, Badagry, Ikorodu, Alimosho) & Biannual Pre-Peak Desilting (before May 1 and during the August Break).

**Verbal Speaker Script:**
> In conclusion, our findings translate directly into five actionable policies for Lagos State: a two-tier antecedent-plus-forecast early warning trigger, tidal flap gates for coastal LGAs below 5 metres, automated Oyan Dam telemetry for Kosofe and Ikorodu, permeable drainage mandates in fast-growing corridors, and biannual channel desilting before May and during the August Break. Thank you, and I welcome your questions.

---
