import sys
from pathlib import Path

ROOT = Path(r"c:\Users\LENOVO\Desktop\Portfolio Projects\lagos-flood-risk-ml")
ARTIFACT = Path(r"C:\Users\LENOVO\.gemini\antigravity\brain\dbbda659-ab1c-425a-952f-42069ce27ace\final_project_report.md")
REPORT_MD = ROOT / "outputs" / "Final_Project_Report.md"

DATA_TOOLS_MD = """### 3.2 Comprehensive Data Sources & Satellite Assets Inventory
Table 3.1 synthesises all primary datasets, satellite Earth observation collections, and disaster archives integrated into the master feature store.

| Dataset Name | Source / Provider | Earth Engine Snippet / Path | Native Spatial Resolution | Native Temporal Resolution | Temporal Range Used | Key Variables Extracted | Primary Use in Project |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **GADM Administrative Boundaries v4.1** | GADM / UC Davis | `data/raw/gadm41_NGA.gpkg` | Vector (Level 2) | Static (2022) | 2022 | 20 Lagos LGA administrative boundaries & polygon geometries | Spatial clipping, zonal reducers, spatial join |
| **CHIRPS Daily Precipitation v2.0** | UCSB Climate Hazards Group / USGS | `UCSB-CHG/CHIRPS/DAILY` | $0.05^\\circ$ ($\\approx 5.5\\text{ km}$) | Daily ($06:00\\text{ UTC}$) | `2010-01-01` to `2025-12-31` | `rain_total_mm`, `rain_max_daily_mm`, `rain_max_3day_mm`, `rainy_days`, `rain_2m_cum_mm`, `rain_anom_z` | Hydrometeorological hazard features |
| **USGS SRTM Digital Elevation v3** | NASA / USGS JPL | `USGS/SRTMGL1_003` | $1\\text{ arc-second}$ ($\\approx 30\\text{ m}$) | Static (Feb 2000) | 2000 | `elev_mean_m`, `elev_median_m`, `elev_min_m`, `elev_std_m`, `low5_share`, `low10_share`, `slope_mean_deg` | Topographic susceptibility & surge exposure |
| **JRC Global Surface Water v1.4** | European Commission Joint Research Centre | `JRC/GSW1_4/GlobalSurfaceWater` | $30\\text{ m}$ | Multi-decadal summary (`1984–2021`) | 1984–2021 | `water_occurrence_pct`, permanent water mask ($\\ge 50\\%$), `dist_water_mean_km`, `near_water_1km_share` | Water masking of DEM & proximity features |
| **ESA WorldCover 10m 2021 v200** | European Space Agency (ESA) | `ESA/WorldCover/v200` | $10\\text{ m}$ | Annual (2021) | 2021 | Built-up (`built_share`), Tree cover (`veg_share`), Mangroves & Wetlands (`wetland_mangrove_share`), Bare land (`bare_share`) | Imperviousness, drainage capacity, nature buffers |
| **WorldPop Unconstrained Gridded Pop** | WorldPop / Univ. Southampton | `WorldPop/GP/100m/pop` & `.../R2025A/v1/pop` | $100\\text{ m}$ (1 hectare) | Annual | `2010–2025` | `population`, `pop_density_km2`, annual growth rate | Human exposure & vulnerable population estimation |
| **Historical Flood Events Log & Archives** | NEMA, NIHSA, LASEMA, EM-DAT, DFO, News | `data/raw/flood_events/flood_events_log.csv` & `GLOBAL_FLOOD_DB` | Community / LGA text & vector polygons | Monthly event-level | `2010–2025` | Event dates, impacted LGAs, communities, severity, source citations | Ground-truth supervised binary target label (`flood`) |
| **NASA NEX-GDDP-CMIP6** | NASA Ames Research Center | `NASA/GDDP-CMIP6` | $0.25^\\circ$ ($\\approx 25\\text{ km}$) | Daily | `2010–2014` (Hist) & `2030–2050` (Future) | Daily precipitation (`pr`) across 5 GCMs (`ACCESS-CM2`, `GFDL-ESM4`, `MPI-ESM1-2-HR`, `MRI-ESM2-0`, `UKESM1-0-LL`) | Climate projections under SSP2-4.5 & SSP5-8.5 |
| **IPCC AR6 Sea-Level Rise Projections** | IPCC Working Group I | IPCC AR6 Sea Level Projection Tool (Gulf of Guinea) | Regional coastal gauge ($1^\\circ$) | Decadal | 2030, 2040, 2050 | Median regional relative sea-level rise ($\\Delta\\text{SLR}$: $+0.11\\text{–}0.40\\text{ m}$) | Coastal elevation depression & low-land expansion |

---

### 3.3 Computational Tools, Software Stack & Engineering Environment
Table 3.2 details the complete software environment, programming languages, analytical libraries, and cloud infrastructure used to develop, train, validate, and deploy the system.

| Category | Tool / Library Name | Environment / Version | Primary Role & Capabilities | Project Utilization |
| :--- | :--- | :---: | :--- | :--- |
| **Programming Language** | **Python** | `3.13.9` (64-bit) | Core development, data pipelines, model training, and web dashboard execution | Standard language across all 9 notebooks, CLI scripts, and web apps |
| **Cloud Geospatial Engine** | **Google Earth Engine (GEE)** | `earthengine-api` `1.4.3` | Cloud-scale planetary Earth observation computing and zonal reducers | Extracted CHIRPS daily sums, SRTM elevation, JRC water, WorldCover, WorldPop, and CMIP6 grids |
| **Geospatial & Vector Analytics** | **GeoPandas & Fiona** | `geopandas` `1.0.1` | Vector spatial processing, GeoPackage I/O, coordinate reprojections | Managed LGA boundaries (`EPSG:4326` and `EPSG:32631`), geometric unions, spatial joins |
| **Geometric Operations** | **Shapely & PyProj** | `shapely` `2.0.6`, `pyproj` `3.7.0` | Planar geometry calculations, spatial filtering, UTM reprojection | Verified topological validity of polygons and geodesic distance calculations |
| **Numerical & Tabular Data** | **Pandas & NumPy** | `pandas` `2.2.3`, `numpy` `2.1.3` | High-performance tabular transformation, rolling windows, array algebra | Feature store assembly, antecedent lag computation, QDM bias correction scaling |
| **Scientific Computing** | **SciPy** | `scipy` `1.14.1` | Non-parametric hypothesis testing and statistical distributions | Two-sided Mann–Whitney $U$ tests, rank-biserial effect sizes, Spearman correlations |
| **Machine Learning Core** | **Scikit-Learn** | `scikit-learn` `1.5.2` | Preprocessing, cross-validation iterators, metrics, probability calibration | `StandardScaler`, `TimeSeriesSplit`, `LeaveOneGroupOut`, `CalibratedClassifierCV`, PR/ROC AUC |
| **Gradient Boosting** | **XGBoost** | `xgboost` `2.1.3` | Scalable gradient boosted decision trees with domain monotonic constraints | Monotonic classification, hyperparameter tuning, fast inference |
| **Random Forests** | **Scikit-Learn Ensemble** | `scikit-learn` `1.5.2` | Balanced subsampled random forests with out-of-bag validation | Cost-sensitive baseline and non-linear ensemble comparison |
| **Explainable AI (XAI)** | **SHAP** | `shap` `0.46.0` | Cooperative game-theoretic feature attributions (TreeSHAP) | Local and global feature importance, beeswarm summary plots, partial dependence analysis |
| **Interactive Web Dashboard** | **Streamlit** | `streamlit` `1.40.1` | Reactive web application framework for data science and model deployment | Multi-tab decision-support dashboard (`app.py`) with real-time What-If scenario simulation |
| **Interactive Cartography** | **Folium / Leaflet.js** | `folium` `0.18.0` | Client-side interactive slippy maps, GeoJSON overlays, choropleths | Multi-layer interactive flood risk map (`outputs/maps/lagos_flood_risk_interactive.html`) |
| **Static Visualizations** | **Matplotlib & Seaborn** | `matplotlib` `3.9.2`, `seaborn` `0.13.2` | Publication-ready figures, ROC/PR curves, confusion matrices, heatmaps | Generated 11 high-resolution figures in `outputs/figures/` (300 DPI) |
| **Model Serialization** | **Joblib** | `joblib` `1.4.2` | Compressed binary persistence of fitted pipelines and calibrated models | Saved `outputs/models/flood_model_bundle.joblib` for headless production inference |
| **Office Document Generation** | **Standard Zipfile + OpenXML** | Python Standard Library | Zero-dependency native packaging of Word (`.docx`) and PowerPoint (`.pptx`) | Automated synthesis of formatted Word project report and 15-slide PowerPoint deck |
| **Cloud & Local Runtime** | **Anaconda / Windows 11** | Conda Environment | Isolated reproducible dependency management | Dedicated execution environment ensuring zero package conflicts |

---
"""

def update_file(path: Path):
    text = path.read_text(encoding="utf-8")
    
    # Check if already present
    if "### 3.2 Comprehensive Data Sources & Satellite Assets Inventory" in text:
        print(f"Already updated: {path}")
        return

    # Renumber old sections
    old_target = "### 3.2 Spatial Units and Topographic Masking"
    new_target = "### 3.4 Spatial Units and Topographic Masking"
    
    if old_target not in text:
        print(f"Error: Could not find target in {path}")
        return
        
    text = text.replace("### 3.6 Summary Profile", "### 3.8 Summary Profile")
    text = text.replace("### 3.5 Target Variable Construction", "### 3.7 Target Variable Construction")
    text = text.replace("### 3.4 Land Cover and Harmonised", "### 3.6 Land Cover and Harmonised")
    text = text.replace("### 3.3 Daily-to-Monthly", "### 3.5 Daily-to-Monthly")
    text = text.replace(old_target, DATA_TOOLS_MD + "\n" + new_target)
    
    path.write_text(text, encoding="utf-8")
    print(f"Successfully updated: {path}")

if __name__ == "__main__":
    update_file(REPORT_MD)
    if ARTIFACT.exists():
        update_file(ARTIFACT)
