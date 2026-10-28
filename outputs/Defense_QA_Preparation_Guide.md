# Defense & Technical Interview Q&A Preparation Guide
## Spatio-Temporal Prediction of Flood Risk in Lagos State, Nigeria (2010–2050)

This guide prepares you for academic thesis defenses, stakeholder briefings (LASEMA, Lagos State Ministry of the Environment and Water Resources, NIHSA), and Senior ML / Climate Data Science technical interviews. It covers **15 high-probability technical, methodological, and policy questions** with rigorous, metric-backed answers.

---

### Part 1: Data Engineering, Remote Sensing & Target Label Construction

#### Q1. Your target variable (`flood_occurred`) is compiled from EM-DAT, Dartmouth Flood Observatory, ReliefWeb, FloodList, and Nigerian newspaper archives. How do you defend against reporting bias (e.g., wealthier or denser LGAs getting more media coverage)?
**Answer:**
- **Acknowledge the Positive-Unlabelled (PU) structure:** Media and disaster databases record confirmed positives ($y=1$), while unrecorded LGA-months ($y=0$) are technically *unlabelled* rather than guaranteed dry months.
- **Triangulation across 5 independent sources:** By combining international satellite/humanitarian repositories (DFO, EM-DAT, ReliefWeb/NEMA) with local community reporting (FloodList, Punch, Vanguard, Premium Times) and mapping over **150+ community/neighborhood names** (e.g., *Ajegunle $\rightarrow$ Ajeromi/Ifelodun*, *Ikorodu Majidun $\rightarrow$ Ikorodu*, *Suleja/Isheri $\rightarrow$ Kosofe*) across all 20 LGAs, we minimized single-source urban bias (`423` flood LGA-months across `2010–2025`, or `11.02%` prevalence).
- **Zero target leakage in features:** We deliberately excluded newspaper mention counts or historical LGA flood frequency from the feature vector (`22` purely physical and demographic features) so the model learns physical susceptibility (elevation, water proximity, imperviousness, rainfall) rather than media attention.
- **Empirical check via Leave-One-LGA-Out CV:** When an entire LGA is held out during training (`LeaveOneGroupOut`), Calibrated Monotonic XGBoost still achieves a mean **ROC-AUC of `0.902`** (`PR-AUC = 0.493`), proving that predictions generalize across LGAs via physical terrain and rainfall rather than memorizing LGA-specific reporting rates.

---

#### Q2. CHIRPS has a native spatial resolution of $0.05^\circ$ ($\approx 5.5\text{ km}$). Some urban Lagos LGAs (like Lagos Island, Apapa, Surulere, and Ajeromi/Ifelodun) are smaller than a single $5.5\text{ km}$ pixel. How did you handle sub-pixel extraction?
**Answer:**
- **Area-weighted fractional pixel reducer in Google Earth Engine:** In `02_rainfall_chirps.ipynb`, we used `ee.Reducer.mean()` and `ee.Reducer.max()` at `scale=5566` over exact GADM v4.1 polygons. In Google Earth Engine, polygon reduction uses fractional pixel area weights for every pixel intersecting the polygon boundary rather than centroid-only sampling.
- **Why this works physically:** Synoptic convective rainfall systems in coastal West Africa have correlation lengths of $15\text{–}40\text{ km}$, meaning neighboring compact LGAs around the Lagos Lagoon experience highly correlated monthly rainfall accumulations (`185–240 mm/month`), while local flood divergence is driven by **high-resolution static terrain (`30m` SRTM), water proximity (`30m` JRC), and land-cover (`10m` ESA WorldCover)**—where we have ratusan to thousands of native pixels even inside the smallest LGA (`Lagos Island`).

---

#### Q3. Why was it critical to mask permanent water bodies (`JRC occurrence >= 50%`) before computing SRTM elevation statistics for Lagos LGAs?
**Answer:**
- **The Lagoon Zero-Elevation Bias:** Roughly `22%` of Lagos State's surface area consists of the Lagos Lagoon, Badagry Creek, Lekki Lagoon, and Atlantic estuaries, where radar interferometry (SRTM 30m) records water surface elevation ($0\text{ m}$).
- **Without land masking:** An LGA with high highland elevation on land but a large lagoon footprint would have its `elev_mean_m` artificially dragged toward $0\text{ m}$ and its `pct_low_elev_5m` inflated by open water rather than habitable land.
- **Our solution (`03_elevation_and_water.ipynb`):** We masked SRTM v3 (`USGS/SRTMGL1_003`) using `JRC/GSW1_4/GlobalSurfaceWater` (`occurrence < 50%`) prior to computing `elev_mean_m`, `elev_min_m`, `elev_std_m`, `elev_p10_m`, `pct_low_elev_2m`, `pct_low_elev_5m`, and `slope_mean_deg`. This isolates true terrestrial flood topography.

---

#### Q4. Why did you harmonize two different WorldPop collections (`WorldPop/GP/100m/pop` and `WorldPop/GP/100m/R2025A/v1/pop`) in Notebook 05?
**Answer:**
- The legacy GEE collection (`WorldPop/GP/100m/pop`) ends in `2020`, whereas the newest release (`WorldPop/GP/100m/R2025A/v1/pop`) covers `2015–2030` with updated census and settlement baselines.
- Simply concatenating `2010–2014` from the legacy asset with `2015–2025` from `R2025A` would introduce an artificial step-change discontinuity in `2015`.
- Instead, we extracted the overlapping year (`2015`) from both collections for each LGA, computed an LGA-specific harmonization ratio $r_i = \text{Pop}_{i,2015}^{\text{R2025A}} / \text{Pop}_{i,2015}^{\text{Legacy}}$, and scaled the `2010–2014` series by $r_i$. This preserved the historical spatial growth trajectory from `2010–2014` while aligning seamlessly with the `2015–2025` `R2025A` baseline.

---

#### Q5. Why did you engineer antecedent rainfall (`rain_prev_month_mm`, `rain_2m_cum_mm`) and local z-score anomalies (`rain_anom_z`) instead of relying solely on current-month rainfall (`rain_total_mm`)?
**Answer:**
- **Soil saturation & perched water tables (Compound Flooding):** In Lagos's September–October secondary peak ("Odo Omi" / Ogun River bank overflow), monthly rainfall (`~195 mm`) is often lower than June (`~310 mm`), yet severe flooding occurs because the coastal aquifer and lagoon are already saturated from July–August rains.
- **Empirical proof from SHAP & Mann–Whitney tests:**
  - `rain_2m_cum_mm` achieves the **#1 highest Mann–Whitney $U$ effect size** ($r_{\text{rb}} = 0.654$, $p = 3.07 \times 10^{-83}$) and the **#1 highest TreeSHAP importance** (`mean |SHAP| = 0.7209`), outperforming current-month rainfall (`rain_total_mm`, `mean |SHAP| = 0.2422`) by nearly $3\times$.
  - `rain_anom_z` captures localized extreme events relative to an LGA's own historical climatology (`mean |SHAP| = 0.0884`).

---

### Part 2: Machine Learning Architecture, Validation & Calibration

#### Q6. Why did you use a strict temporal train/test split (`2010–2020` train, `2021–2025` test) plus `TimeSeriesSplit` and `LeaveOneGroupOut` instead of standard 5-fold stratified random cross-validation?
**Answer:**
- **Two leakage modes in spatio-temporal panels:**
  1. **Temporal autocorrelation & synoptic weather leakage:** In a random split, `Lagos Island – July 2022` might be in the training set while `Mainland – July 2022` is in the test set. Since both experienced the exact same July 2022 rainstorm, a random split leaks the storm's label across LGAs and inflates test metrics.
  2. **Future-to-past leakage:** Training on `2024` to predict `2018` violates operational forecasting reality.
- **Our three-tier evaluation design (`07_modelling.ipynb`):**
  - **Out-of-Time Test (`2021–2025`, `1,200` rows):** Evaluates forward generalization into unseen future years where flood frequency shifted from `9.09%` (`2010–2020`) to `15.25%` (`2021–2025`).
  - **5-Fold Expanding-Window `TimeSeriesSplit`:** Prevents look-ahead bias during hyperparameter selection.
  - **20-Fold `LeaveOneGroupOut` Spatial CV:** Trains on 19 LGAs and tests on 1 completely unseen LGA (`ROC-AUC = 0.902`), proving spatial transferability.

---

#### Q7. Why did you enforce monotonic constraints (`monotone_constraints`) on the XGBoost classifier, and how did that affect both historical accuracy and 2050 climate extrapolations?
**Answer:**
- **Problem with unconstrained decision trees:** On finite noisy samples (`2,640` training rows), standard gradient-boosted trees can fit non-physical split inversions—for instance, predicting lower flood probability when `rain_total_mm` increases from `380 mm` to `420 mm` if a single high-rainfall month happened to go unreported. This becomes catastrophic when projecting into `2030–2050` under `SSP5-8.5` with higher rainfall and sea-level rise.
- **Our Constraint Specification:**
  - $+1$ (monotonically non-decreasing): `rain_total_mm`, `rain_max_daily_mm`, `rain_2m_cum_mm`, `rain_anom_z`, `pct_low_elev_2m`, `pct_low_elev_5m`, `pct_built_up`, `pop_density_km2`.
  - $-1$ (monotonically non-increasing): `elev_mean_m`, `elev_p10_m`, `slope_mean_deg`, `dist_water_mean_m`, `pct_mangrove`, `pct_tree_cover`.
- **Result:** Calibrated Monotonic XGBoost achieved the **highest Test ROC-AUC (`0.890`) and Test PR-AUC (`0.460`)** while guaranteeing physically coherent, monotonic response surfaces under `SSP2-4.5` and `SSP5-8.5` climate perturbations.

---

#### Q8. With an `11.02%` positive class rate, ROC-AUC (`0.890`) looks very high while PR-AUC (`0.460`) is numerically lower. Is `0.460` PR-AUC good, and why report both?
**Answer:**
- **Why ROC-AUC can be optimistic under imbalance:** False Positive Rate ($\text{FPR} = \text{FP} / (\text{FP} + \text{TN})$) has a large denominator ($\text{TN} = 1,017$ in the test set), so moderate false alarms do not heavily penalize ROC-AUC.
- **Why PR-AUC (`0.460`) is strong:** The naive baseline for Precision-Recall AUC equals the test positive prevalence (`0.1525` in `2021–2025`, `0.1102` overall). Achieving `PR-AUC = 0.460` (`95% CI: [0.402, 0.534]`) represents a **$3.05\times$ lift over random guessing** and outperforms Logistic Regression (`0.406`) by `+5.4` percentage points (`+13.3%` relative gain).
- Furthermore, at the calibrated threshold (`0.38`), our models achieve **`71.0%–71.8%` Recall** on historical floods, capturing more than 7 out of every 10 flood LGA-months.

---

#### Q9. Why did you apply Platt scaling (`CalibratedClassifierCV(method='sigmoid')`) on top of XGBoost and Random Forest?
**Answer:**
- When class weights (`scale_pos_weight = 10.0` in XGBoost or `class_weight='balanced_subsample'` in Random Forest) are used to boost minority-class sensitivity, raw predicted scores are shifted upward toward $0.5\text{–}0.8$, causing systematic over-prediction of flood probabilities and inflating Brier scores.
- Because our downstream **2050 Composite Flood Risk Index (`FRI`)** directly incorporates the model's predicted wet-season flood probability as its **Hazard (`H`)** pillar, the probabilities must represent well-calibrated empirical frequencies.
- Using 5-fold `TimeSeriesSplit` sigmoid calibration reduced the **Brier Score to `0.1070` (Random Forest) and `0.1092` (XGBoost)** and aligned the calibration reliability curve closely with the $45^\circ$ diagonal (`07_pr_roc_calibration_curves.png`).

---

#### Q10. In your spatial hold-out analysis (`07_spatial_holdout_lga.csv`), why does `Ibeju-Lekki` have a lower PR-AUC (`0.289`) despite having a high ROC-AUC (`0.858`)?
**Answer:**
- **Rapid non-stationary peri-urban transformation:** `Ibeju-Lekki` is the fastest-changing peri-urban corridor in West Africa (Lekki Free Trade Zone, Dangote Refinery, Lekki Deep Sea Port). Between 2010 and 2016 it was sparsely populated coastal scrubland with very few reported floods (`low historical base rate`), whereas post-2019 rapid land reclamation and wetland infilling triggered sudden drainage bottlenecks.
- **Implication:** Because `ESA WorldCover` is a static `2021` snapshot (`21.7%` built-up across its large $653\text{ km}^2$ land area), the LGA-wide built-up average understates localized imperviousness along the Lekki-Epe expressway. This directly motivates our recommendation in Chapter 9.2 to incorporate **annual dynamic imperviousness from Sentinel-2 (`2016–2025`)** and **30m sub-LGA ward grids**.

---

### Part 3: Climate Projections, Sea-Level Rise & Composite Risk Index (`2030–2050`)

#### Q11. Why couldn't you feed raw NASA NEX-GDDP-CMIP6 daily precipitation directly into the trained XGBoost model for `2030–2050` projections?
**Answer:**
- **GCM "Drizzle Effect" & Mean Bias:** Even at $0.25^\circ$ downscaled resolution, Global Climate Models in the Gulf of Guinea exhibit systematic wet/dry biases and produce too many low-intensity drizzle days (`1–3 mm/day`) while underestimating convective cloudburst peaks (`>80 mm/day`) compared to satellite-gauge CHIRPS (`0.05°`).
- **Our Delta-Ratio / Quantile Scaling Pipeline (`08_climate_projections.ipynb`):**
  1. We extracted `103,000+` daily records across **5 CMIP6 GCMs** (`ACCESS-CM2`, `GFDL-ESM4`, `MPI-ESM1-2-HR`, `MRI-ESM2-0`, `UKESM1-0-LL`) for historical reference (`2010–2014`) and future horizons (`2030–2050`, `SSP2-4.5` & `SSP5-8.5`).
  2. For each calendar month $m$, LGA $i$, and scenario $s$, we computed the multi-model ensemble ratio $R_{i,m,s} = \bar{P}^{\text{CMIP6, future}}_{i,m,s} / \bar{P}^{\text{CMIP6, hist}}_{i,m}$ (clipped to $[0.70, 1.60]$ for physical stability) and applied it to the observed CHIRPS baseline climatology (`2010–2025`), alongside an additional $+4\%$ convective extreme intensification factor on `rain_max_daily_mm` per the Clausius–Clapeyron relation ($\approx 7\%\text{ K}^{-1}$).

---

#### Q12. How did you model Sea-Level Rise (SLR) and future urban growth in the `2030–2050` feature perturbations?
**Answer:**
- **Physically coupled topographic shift for SLR:** Rather than adding SLR as a disconnected post-hoc weight, we integrated **IPCC AR6 Gulf of Guinea regional relative sea-level rise** (`+0.15 m` by 2030 and `+0.26 m` by 2050 under `SSP2-4.5`; `+0.18 m` by 2030 and `+0.35 m` by 2050 under `SSP5-8.5`, plus `2 mm/yr` coastal subsidence) directly into the terrain features:
  - Effective elevation above mean sea level decreases by $\Delta\text{SLR}$ (`elev_mean_m`, `elev_min_m`, `elev_p10_m`).
  - Low-elevation land fractions (`pct_low_elev_2m`, `pct_low_elev_5m`) expand proportionally in coastal/lagoon LGAs (`dist_water_mean_m < 3,000 m`).
- **SSP Demographic & Urban Growth:** Population density (`pop_density_km2`) scales by compound annual growth (`2.4%/yr` under `SSP2-4.5`, `3.1%/yr` under `SSP5-8.5` with peri-urban concentration in `Ikorodu`, `Ibeju-Lekki`, `Badagry`, and `Epe`), while `pct_built_up` expands (`+0.35%/yr` to `+0.60%/yr`) at the expense of permeable vegetation (`pct_tree_cover`, `pct_mangrove`).

---

#### Q13. The Composite Flood Risk Index uses weights $\text{FRI} = 100 \times (0.50 H + 0.30 E + 0.20 V)$. Isn't $50\% / 30\% / 20\%$ arbitrary? How do you prove your LGA rankings aren't an artifact of weight selection?
**Answer:**
- **Grounded in the IPCC AR6 Risk Framework:** Hazard ($H$) represents the calibrated wet-season ML flood probability (`50%`), Exposure ($E$) captures normalized population density and urban built-up footprint (`30%`), and Vulnerability ($V$) captures low-lying terrain (`<5m`), water proximity, and wetland loss (`20%`).
- **Rigorous Sensitivity Perturbation (`09_risk_index.ipynb`):** We tested four distinct weight schemes across all 20 LGAs:
  1. **Baseline (`50% H / 30% E / 20% V`)**
  2. **Hazard-Heavy (`70% H / 15% E / 15% V`)** — $\text{Spearman } \rho = 0.9233$ ($p = 6.5 \times 10^{-9}$)
  3. **Exposure-Heavy (`35% H / 45% E / 20% V`)** — $\text{Spearman } \rho = 0.9624$ ($p = 1.2 \times 10^{-11}$)
  4. **Equal Weights (`33.3% H / 33.3% E / 33.3% V`)** — $\text{Spearman } \rho = 0.9910$ ($p = 2.8 \times 10^{-17}$)
- Across all four weight schemes, the top-tier priority LGAs (`Lagos Island`, `Apapa`, `Kosofe`, `Eti-Osa`, `Amuwo Odofin`, `Ajeromi/Ifelodun`) remain invariant.

---

### Part 4: Policy Impact & Operational Deployment

#### Q14. Why does `Alimosho` rank #1 in total flood-exposed population (`280,101` residents/yr by 2050 under SSP5-8.5) even though its Composite FRI (`35.2`, Rank #19) is Moderate?
**Answer:**
- **Risk Rate vs. Absolute Human Exposure:**
  - `Lagos Island` (`FRI = 56.5`, Rank #1) and `Apapa` (`FRI = 56.2`, Rank #2) have the highest *probability and intensity* of flooding per square kilometer due to extreme low elevation (`80%–92%` of land `<5m`) and lagoon encirclement, but smaller residential populations (`~350k–400k`).
  - `Alimosho` sits on higher inland terrain (`elev_mean_m = 34.4 m`), giving it a lower wet-season flood probability (`12.16%` in 2050 SSP5-8.5). However, because `Alimosho` is Lagos's most populous LGA (`>2.3 million` projected residents by 2050), multiplying `2.3M` residents by a `12.16%` pluvial flash-flood hazard yields **`280,101` exposed residents per year**.
- **Policy Takeaway:** Lagos cannot rely on a single metric. **Coastal defense capital expenditure** (sea walls, tidal gates, pumping stations) must target **Top-FRI LGAs** (`Lagos Island`, `Apapa`, `Eti-Osa`, `Kosofe`), whereas **community early-warning alerts, secondary storm-drain desilting, and LASEMA relief staging** must simultaneously cover **high-population inland LGAs** (`Alimosho`, `Kosofe`, `Ajeromi/Ifelodun`, `Mushin`, `Ikorodu`).

---

#### Q15. If LASEMA or the Lagos State Ministry of the Environment wanted to deploy this system into production next month, what would the operational architecture look like?
**Answer:**
1. **Automated Monthly & Sub-Monthly Ingestion Cron:** A lightweight cloud pipeline (GitHub Actions / Cloud Run) querying Google Earth Engine on the 1st and 15th of each month to fetch near-real-time **CHIRPS Prelim / IMERG daily rainfall**, compute rolling 30-day and 60-day cumulative rainfall (`rain_2m_cum_mm`) and anomaly z-scores (`rain_anom_z`), and merge with static LGA terrain/exposure features.
2. **Calibrated Inference Engine:** Score all 20 LGAs (and 37 LCDAs / 377 wards once downscaled) using the serialized `outputs/models/flood_model_bundle.joblib`, applying the calibrated threshold (`0.38`) to classify each LGA into **Green (`<20%`), Amber (`20–38%`), Orange (`38–60%`), or Red (`>60%`)** alert tiers.
3. **Decision-Support Dissemination:** Push automated GeoJSON updates to the **Streamlit Decision-Support Dashboard (`app.py`)** and trigger SMS/WhatsApp early-warning bulletins to LASEMA zonal directors when `rain_2m_cum_mm` crosses the `300 mm` saturation threshold identified by our SHAP dependence analysis.
