# Portfolio Case Study & LinkedIn Launch Kit
## Spatio-Temporal Prediction of Flood Risk in Lagos State, Nigeria (2010–2050)

This document contains ready-to-publish copy for:
1. **Personal Website / GitHub Portfolio Case Study** (long-form technical showcase)
2. **LinkedIn Post Option A: Technical ML & Geospatial Engineering Focus** (aimed at Senior ML Engineers, Hiring Managers, and Climate Data Scientists)
3. **LinkedIn Post Option B: Urban Resilience, Climate Impact & Policy Focus** (aimed at Urban Planners, Development Banks, Government Leaders, and Civic Tech)

---

## 1. Personal Website / Portfolio Case Study

### Title
**Spatio-Temporal Flood Risk Prediction & 2050 Climate Impact Modelling for Lagos State, Nigeria**

### Subtitle
*Combining 16 years of satellite remote sensing (CHIRPS, SRTM, JRC Surface Water, ESA WorldCover, WorldPop), Calibrated Monotonic Gradient Boosting, and 5-GCM CMIP6 climate projections to map flood hazard and human exposure across Lagos's 20 Local Government Areas.*

### Executive Summary
Lagos State is Africa's largest coastal megacity ($\approx 16\text{–}22\text{ million}$ residents), squeezed onto a low-lying barrier-lagoon complex where nearly half of several urban LGAs sit less than $5\text{ m}$ above mean sea level. Every wet season, compound pluvial, fluvial, and coastal flooding disrupts millions of lives and causes an estimated **US\$4 billion** in annual economic damages.

I designed and built an end-to-end **Spatio-Temporal Machine Learning & Climate Risk Decision-Support System** across all **20 Local Government Areas (LGAs)** spanning **3,840 historical LGA-months (`2010–2025`)** and projecting future flood risk through **`2030–2050`** under **IPCC AR6 `SSP2-4.5` and `SSP5-8.5`** pathways.

### System Architecture & Engineering Highlights
1. **Multi-Sensor Satellite Data Engineering (Google Earth Engine):**
   - **Precipitation (`CHIRPS v2.0`, `5.5 km` daily):** Engineered monthly totals, maximum 1-day cloudburst intensity, rainy-day counts, heavy rain days ($\ge 20\text{ mm}$), **60-day antecedent cumulative rainfall (`rain_2m_cum_mm`)** to capture soil/aquifer saturation, and **LGA-specific monthly z-score anomalies (`rain_anom_z`)**.
   - **Land-Masked Topography (`SRTM 30m` + `JRC Global Surface Water 30m`):** Masked permanent lagoon and estuarine water bodies (`occurrence >= 50%`) prior to extracting elevation percentiles (`p10`, `mean`, `std`), slope, and low-elevation land fractions (`<2m`, `<5m`) so open lagoon water would not distort terrestrial elevation metrics.
   - **Dynamic Exposure (`WorldPop 100m` + `ESA WorldCover 10m`):** Harmonized `2010–2014` and `2015–2025` `R2025A` population grids using per-LGA overlap scaling ratios alongside 10m impervious built-up and mangrove buffer fractions.
2. **Leakage-Free Spatio-Temporal Validation & Monotonic ML:**
   - Evaluated **Logistic Regression, Random Forest, LightGBM, and Monotonic XGBoost** using a strict out-of-time split (`2010–2020` train vs. `2021–2025` test), **5-fold `TimeSeriesSplit` CV**, and **20-fold `LeaveOneGroupOut` spatial hold-out CV**.
   - Enforced **domain-informed monotonic constraints (`+1/-1`)** on XGBoost so flood probability strictly increases with rainfall, low elevation, and imperviousness and decreases with elevation, slope, distance to water, and mangrove cover.
   - Applied **Platt sigmoid probability calibration** (`Brier Score = 0.1070–0.1092`) and **1,000-iteration bootstrap 95% confidence intervals**.
3. **CMIP6 Multi-Model Downscaling & 2050 Composite Risk Index (`FRI`):**
   - Processed **103,000+ daily records** across **5 CMIP6 Global Climate Models** (`ACCESS-CM2`, `GFDL-ESM4`, `MPI-ESM1-2-HR`, `MRI-ESM2-0`, `UKESM1-0-LL`) via NASA NEX-GDDP-CMIP6, applying delta-ratio bias correction against CHIRPS, IPCC AR6 Gulf of Guinea sea-level rise (`+0.26 m` to `+0.35 m`), and SSP demographic projections.
   - Constructed the **IPCC AR6 Composite Flood Risk Index** ($\text{FRI} = 0.50 H + 0.30 E + 0.20 V$), verified via rank-stability sensitivity testing ($\text{Spearman } \rho = 0.92\text{–}0.99$).

### Key Quantitative Results

| Metric / Finding | Value | Technical Significance |
| :--- | :--- | :--- |
| **Historical Panel Size** | `3,840` LGA-months (`2010–2025`) | `423` documented flood LGA-months (`11.02%` positive rate) |
| **Out-of-Time Test ROC-AUC (`2021–2025`)** | **`0.890`** (`95% CI: [0.871, 0.910]`) | Calibrated Monotonic XGBoost on unseen future years |
| **Out-of-Time Test PR-AUC (`2021–2025`)** | **`0.460`** (`95% CI: [0.402, 0.534]`) | **$3.05\times$ lift** over naive baseline; `+13.3%` over Logistic Regression |
| **20-Fold Spatial Hold-Out (`LeaveOneGroupOut`)** | **`0.902` ROC-AUC** (`0.493` PR-AUC) | Generalizes accurately to completely unseen LGAs |
| **#1 Physical Driver (TreeSHAP)** | `rain_2m_cum_mm` (`|SHAP| = 0.7209`) | 60-day cumulative rainfall is nearly **$3\times$ more predictive** than current-month rain alone |
| **2050 Annual Flood-Exposed Population** | **`1.98 Million / yr`** (`SSP5-8.5`) | Nearly **doubles (`+99.5%`)** from `993,636/yr` in the historical baseline |
| **Top 5 Highest-Risk LGAs (`2050 SSP5-8.5`)** | `Lagos Island` (`56.5`), `Apapa` (`56.2`), `Kosofe` (`52.6`), `Eti-Osa` (`51.8`), `Amuwo Odofin` (`51.7`) | **11 of 20 LGAs** enter the High Risk (`FRI >= 45`) tier by 2050 |

### Deliverables Built
- **9 End-to-End Reproducible Jupyter Notebooks** (`notebooks/01` through `09`)
- **4-Tab Interactive Streamlit Decision-Support Dashboard** (`app.py`) with a live *What-If Policy Simulator*
- **Standalone Multi-Layer Folium/Leaflet HTML Map** (`outputs/maps/lagos_flood_risk_interactive.html`)
- **Complete 10-Chapter Technical Report (`.docx` & `.md`)** & **15-Slide Executive Presentation Deck (`.pptx`)**

---

## 2. LinkedIn Launch Post — Option A (Technical ML & Data Science Focus)

> **Suggested Visual Attachments:**
> 1. `outputs/figures/09_flood_risk_index_maps_2050.png` (3-panel 2050 Flood Risk Index map)
> 2. `outputs/figures/07_shap_beeswarm_summary.png` (TreeSHAP feature attribution plot)
> 3. `outputs/figures/07_pr_roc_calibration_curves.png` (ROC, PR, and Calibration curves)

**Post Copy:**

How do you predict urban flood risk across Africa’s largest coastal megacity—and project how climate change and sea-level rise will reshape that risk by 2050? 🌊🛰️📈

Over the past few weeks, I built an end-to-end **Spatio-Temporal Flood Risk Machine Learning & Climate Projection System for Lagos State, Nigeria** across all 20 Local Government Areas (`2010–2050`).

Instead of treating flood prediction as a static GIS overlay or a leaky random train/test split, I engineered a physical-statistical pipeline grounded in satellite remote sensing and climate science:

🔹 **Multi-Sensor Feature Engineering (Google Earth Engine):**
Fused 16 years (`3,840` LGA-months) of daily **CHIRPS (`5.5 km`)** precipitation, **SRTM (`30 m`)** digital elevation masked with **JRC Global Surface Water (`30 m`)** (so the Lagos Lagoon doesn't bias land elevation toward 0m!), **ESA WorldCover (`10 m`)** imperviousness/mangroves, and harmonized **WorldPop (`100 m`)** demographic series.

🔹 **What Actually Drives Flooding in Lagos? (TreeSHAP Insight):**
Current-month rainfall alone isn't the #1 predictor. **60-day cumulative antecedent rainfall (`rain_2m_cum_mm`, `mean |SHAP| = 0.721`)** is nearly **3x more predictive** than single-month rainfall (`0.242`). In Lagos, compound flooding peaks when intense cloudbursts hit an already-saturated coastal water table and swollen lagoon system.

🔹 **Rigorous Spatio-Temporal Validation & Monotonic Constraints:**
- Strict out-of-time test split (`2010–2020` train $\rightarrow$ `2021–2025` test) + 5-fold `TimeSeriesSplit` CV + 20-fold `LeaveOneGroupOut` spatial CV.
- Enforced **domain-informed monotonic constraints (`+1/-1`)** in XGBoost + Platt sigmoid calibration so the model never learns non-physical tree inversions when extrapolating to future climate regimes.
- **Results:** `0.890` Test ROC-AUC (`95% CI: [0.871, 0.910]`), `0.460` Test PR-AUC (`3.05x` over naive baseline), `0.107` Brier Score, and **`0.902` ROC-AUC on unseen LGAs** in spatial hold-out testing.

🔹 **2030–2050 CMIP6 Climate & Sea-Level Rise Projections:**
Downscaled `103,000+` daily records across **5 CMIP6 GCMs** (`ACCESS-CM2`, `GFDL-ESM4`, `MPI-ESM1-2-HR`, `MRI-ESM2-0`, `UKESM1-0-LL`) under `SSP2-4.5` and `SSP5-8.5`, coupled with IPCC AR6 Gulf of Guinea sea-level rise (`+0.26m` to `+0.35m`).
- By 2050 (`SSP5-8.5`), annual flood-exposed population in Lagos nearly doubles from **`993k` to `1.98 Million` residents/year (`+99.5%`)**.
- **Top 5 Highest-Risk LGAs (2050 FRI):** `Lagos Island` (`56.5`), `Apapa` (`56.2`), `Kosofe` (`52.6`), `Eti-Osa` (`51.8`), and `Amuwo Odofin` (`51.7`).

The project includes a 9-notebook reproducible pipeline, an interactive Folium web map, and a 4-tab **Streamlit Decision-Support Dashboard** with a live What-If simulator for testing drainage upgrades and mangrove restoration.

#MachineLearning #ClimateDataScience #Geospatial #XGBoost #GoogleEarthEngine #ExplainableAI #Lagos #FloodRisk #Python #Streamlit

---

## 3. LinkedIn Launch Post — Option B (Policy, Urban Resilience & Impact Focus)

> **Suggested Visual Attachments:**
> 1. `outputs/figures/09_exposed_population_by_lga.png` (Exposed Population by LGA: Baseline vs 2050)
> 2. `outputs/figures/09_flood_risk_index_maps_2050.png` (2050 Flood Risk Index Choropleth)

**Post Copy:**

By 2050, nearly **2 million Lagos residents per year** could face wet-season flooding—almost double the historical baseline (`+99.5%`). 🌍🏙️⚠️

Lagos loses an estimated **US$4 billion annually** to flooding. Yet urban resilience planners often face a critical dilemma: *Where should we build coastal sea walls and tidal pumping stations, and where should we prioritize community early warning and secondary storm-drain desilting?*

Using 16 years of satellite observations (`2010–2025`), machine learning, and 5-model CMIP6 climate projections (`2030–2050`), I built a **Spatio-Temporal Flood Risk Index & Decision-Support Tool** for all 20 Local Government Areas (LGAs) in Lagos State.

**3 Key Takeaways for Lagos Urban Resilience:**

1️⃣ **11 of 20 LGAs will reach "High Risk" status by 2050 (`SSP5-8.5`):**
Coastal and lagoon-front LGAs—led by **Lagos Island (`FRI 56.5`), Apapa (`56.2`), Kosofe (`52.6`), Eti-Osa (`51.8`), and Amuwo Odofin (`51.7`)**—face a compound squeeze from intense monsoonal cloudbursts and `+0.26m to +0.35m` of Gulf of Guinea sea-level rise.

2️⃣ **High Hazard Rate $\neq$ Highest Human Exposure:**
While `Lagos Island` and `Apapa` face the highest *probability* of flooding per square kilometer, **Alimosho (`280,101` exposed residents/yr), Kosofe (`247,534`), and Ajeromi/Ifelodun (`188,167`)** account for the largest *human headcount* at risk due to rapid population growth and impervious surface expansion. Coastal defense capex and inland emergency relief must be planned together.

3️⃣ **Early Warning Needs a 60-Day Memory:**
Our explainable AI (`TreeSHAP`) analysis revealed that **2-month cumulative rainfall (`>300 mm` over 60 days)** is nearly **3x more predictive** of severe Lagos flooding than single-month rainfall alone. Watching multi-week soil and lagoon saturation—especially ahead of the September–October Ogun River overflow peak—can give emergency agencies weeks of advance warning.

I’ve packaged the entire system into an interactive **Streamlit Decision-Support Dashboard** where planners can test how storm-drain expansion, green infrastructure, and mangrove conservation in Badagry, Ikorodu, Epe, and Ojo can bend the 2050 risk curve.

#UrbanResilience #Lagos #ClimateAdaptation #DisasterRiskReduction #GIS #DataScience #PublicPolicy #Nigeria #SustainableCities
