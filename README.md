# Spatio-Temporal Prediction of Pluvial and Coastal Flood Risk in Lagos State, Nigeria (2010–2050)

**Author:** Utibe Bassey  
**Scope:** 20 Local Government Areas (LGAs) of Lagos State · Historical Study Period: `2010–2025` (3,840 LGA-months) · Climate Projections: `2030–2050` (`SSP2-4.5` & `SSP5-8.5`)

---

## 1. Project Overview

Flooding is one of the most recurrent and costly natural hazards in Lagos State, driven by intense bimodal tropical rainfall, low-lying coastal and lagoon-fringe topography, rapid impervious urbanisation, and rising sea levels.

This repository implements an end-to-end, reproducible **geospatial data engineering, machine learning, and climate risk projection pipeline** at the Local Government Area (LGA) level:
1. **Multi-Source Satellite & Hydrological Feature Engineering (Google Earth Engine)**:
   - **CHIRPS v2.0 Daily Rainfall (`2010–2025`)**: 116,880 daily LGA records aggregated into monthly totals, 1-day and 3-day storm extremes, rainy/heavy-rain day counts, antecedent previous-month rainfall (`rain_prev_month_mm`), 2-month cumulative rainfall, standardised anomalies, and cyclical seasonality (`month_sin`, `month_cos`).
   - **USGS SRTM (30 m) & JRC Global Surface Water (30 m)**: Land-masked elevation statistics (`elev_mean_m`, `elev_median_m`, `low5_share` $<5\text{ m}$, `low10_share` $<10\text{ m}$, `slope_mean_deg`), permanent water fraction (`water_share`), and Euclidean distance to nearest permanent water (`dist_water_mean_km`, `near_water_1km_share`).
   - **ESA WorldCover v200 (10 m) & WorldPop (100 m)**: Impervious built-up land share (`built_share`), wetland/mangrove share (`wetland_mangrove_share`), vegetated share (`veg_share`), and annual resident population & density (`2010–2025`).
2. **Historical Flood Event Log & LGA-Month Target Labels (`2010–2025`)**:
   - Compiled from NEMA, NIHSA Annual Flood Outlooks, LASEMA emergency logs, EM-DAT, the Dartmouth Flood Observatory (DFO) / MODIS Global Flood Database, and verified Nigerian news archives across all 20 LGAs (`423` documented flood LGA-months out of `3,840`, `11.02%`).
3. **Spatio-Temporal Machine Learning & Explainability**:
   - **Temporal Validation**: Strict chronological train/validation split (`2010–2020`, 2,640 rows) with expanding-window `TimeSeriesSplit` cross-validation and held-out future test evaluation (`2021–2025`, 1,200 rows).
   - **Spatial Validation**: 20-fold **Leave-One-LGA-Out (`LeaveOneGroupOut`)** cross-validation to verify generalisation to unseen LGAs (`Mean ROC-AUC = 0.902`).
   - **Models**: Naive & Climatology Baselines, $L_2$-Regularised Logistic Regression, Cost-Sensitive Random Forest, and **Calibrated Monotonic XGBoost** (`Test ROC-AUC = 0.890`, `Test PR-AUC = 0.460`, `Brier Score = 0.109`), explained with **TreeSHAP**.
4. **CMIP6 Climate Projections (`2030–2050`) & Composite Flood Risk Index (FRI)**:
   - Daily precipitation extracted from **5 CMIP6 Global Climate Models** (`ACCESS-CM2`, `GFDL-ESM4`, `MPI-ESM1-2-HR`, `MRI-ESM2-0`, `UKESM1-0-LL`) via `NASA/GDDP-CMIP6`, bias-corrected against CHIRPS, and combined with **IPCC AR6 regional sea-level rise** and **SSP urban growth** under **SSP2-4.5** and **SSP5-8.5**.
   - **Composite Flood Risk Index (FRI, 0–100)** combining Hazard ($H$), Physical/Drainage Vulnerability ($V$), and Human Exposure ($E$), delivered via a standalone **Leaflet interactive HTML map** and a **Streamlit dashboard (`app.py`)**.

---

## 2. Repository Structure

```text
lagos-flood-risk-ml/
├── app.py                                      # Interactive Streamlit Dashboard
├── requirements.txt                            # Reproducible Python dependencies
├── README.md                                   # Project documentation & reproduction guide
├── data/
│   ├── raw/
│   │   ├── gadm41_NGA.gpkg                     # GADM v4.1 Nigeria administrative boundaries
│   │   ├── chirps_chunks/                      # 32 six-month daily CHIRPS GEE downloads
│   │   ├── chirps_daily_lga.csv                # Combined daily CHIRPS rainfall (116,880 rows)
│   │   ├── cmip6_lagos_daily.csv               # 5-GCM CMIP6 daily rainfall (historical, ssp245, ssp585)
│   │   └── flood_events/
│   │       └── flood_events_log.csv            # Curated historical Lagos flood records (2010–2025)
│   └── clean/
│       ├── lagos_lgas.gpkg                     # Cleaned 20 Lagos LGA boundaries (EPSG:4326)
│       ├── rainfall_lga_month.csv              # Monthly & antecedent CHIRPS features (3,840 rows)
│       ├── terrain_water_lga.csv               # SRTM elevation & JRC water distance (20 rows)
│       ├── flood_events_combined.csv           # Combined DFO + curated event log
│       ├── flood_labels_lga_month.csv          # LGA-month flood target labels (3,840 rows)
│       ├── flood_labels_state_month.csv        # State-month flood target labels (192 rows)
│       ├── landcover_lga.csv                   # ESA WorldCover 10m shares per LGA (20 rows)
│       ├── population_lga_year.csv             # WorldPop 100m annual population 2010–2025 (320 rows)
│       ├── master_lga_month.csv                # Master modelling table (3,840 rows × 40 columns)
│       ├── data_dictionary.csv                 # Column-by-column unit & source documentation
│       ├── projections_lga_month_2030_2050.csv # 2030–2050 monthly ensemble flood projections
│       └── flood_risk_index_lga.csv            # Composite Flood Risk Index & exposed population
├── notebooks/
│   ├── 01_lga_boundaries.ipynb                 # Phase 0/2: Extract & verify 20 Lagos LGA polygons
│   ├── 02_rainfall_chirps.ipynb                # Phase 2/3: Daily CHIRPS -> monthly & antecedent features
│   ├── 03_elevation_and_water.ipynb            # Phase 2: SRTM elevation, slope & JRC water distance
│   ├── 04_flood_records.ipynb                  # Phase 2: Historical flood records & LGA-month labelling
│   ├── 05_population_landcover.ipynb           # Phase 2: ESA WorldCover, WorldPop & Master Table assembly
│   ├── 06_eda.ipynb                            # Phase 3: Spatial/seasonal EDA, Mann-Whitney tests & VIF
│   ├── 07_modelling.ipynb                      # Phase 4: Temporal/spatial CV, ML models, calibration & SHAP
│   ├── 08_climate_projections.ipynb            # Phase 5: 5-GCM CMIP6 bias correction, SLR & 2050 projections
│   └── 09_risk_index.ipynb                     # Phase 6: Composite Flood Risk Index & interactive HTML map
└── outputs/
    ├── figures/                                # High-resolution PNG charts from Notebooks 06–09
    ├── maps/
    │   └── lagos_flood_risk_interactive.html   # Standalone interactive Leaflet risk explorer
    ├── models/
    │   └── flood_model_bundle.joblib           # Saved calibrated XGBoost pipeline & metadata
    └── tables/                                 # CSV results tables for report inclusion
```

---

## 3. How to Reproduce the Pipeline

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run Notebooks in Order (`01` → `09`)**:
   - All raw Google Earth Engine downloads (`chirps_daily_lga.csv`, `terrain_water_lga.csv`, `landcover_lga.csv`, `population_lga_year.csv`, and `cmip6_lagos_daily.csv`) are already cached in `data/raw/` and `data/clean/`, so Notebooks `01` to `09` can be rerun offline or re-authenticated against Google Earth Engine (`PROJECT_ID = "lagos-flood-risk"`).
3. **Launch the Interactive Dashboard**:
   ```bash
   streamlit run app.py
   ```
   Or open `outputs/maps/lagos_flood_risk_interactive.html` directly in any web browser.
