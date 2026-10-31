"""
Integrate 5 new advanced map figures and explanations into Final_Project_Report.md,
clean formatting, and rebuild the native Word document report.
"""

from pathlib import Path
import re

ROOT = Path(r"c:\Users\LENOVO\Desktop\Portfolio Projects\lagos-flood-risk-ml")
REPORT_MD = ROOT / "outputs" / "Final_Project_Report.md"
ARTIFACT = Path(r"C:\Users\LENOVO\.gemini\antigravity\brain\dbbda659-ab1c-425a-952f-42069ce27ace\final_project_report.md")

text = REPORT_MD.read_text(encoding="utf-8")

# 1. Insert Map 01, Map 02, Map 03 in Chapter 4 right after Figure 4.2
MAPS_CH4_TEXT = """### 4.2.1 High-Resolution Topographic Relief and Coastal Surge Inundation Zones (<5m Land)
Figure 4.2a provides a dedicated dual-panel cartographic analysis of Lagos State's digital elevation relief and critical coastal lowlands.

![Figure 4.2a: Terrestrial Topography and Coastal & Estuarine Surge Inundation Vulnerability (<5m Land)](figures/map_01_topography_inundation_zones.png)

**Detailed Interpretation & Key Findings from Figure 4.2a:**
- **Panel A (Terrestrial Elevation & Topographic Relief):** Depicts mean land elevation derived from USGS SRTM 30m, masked using JRC Global Surface Water (occurrence >= 50%) to eliminate lagoon and estuarine open water distortion. Terrestrial elevation ranges from <5 m along the southern barrier-lagoon complex to over 40–50 m in northern inland LGAs (**Agege** at 41.9 m, **Ifako/Ijaye** at 49.2 m, and **Alimosho** at 27.9 m).
- **Panel B (Low-Lying Coastal & Estuarine Surge Inundation Zones):** Isolates the percentage of land area sitting below the critical 5-metre contour. Over 40% to 52% of total land area in **Lagos Island (51.5%)**, **Apapa (46.0%)**, **Ajeromi/Ifelodun (45.7%)**, **Kosofe (40.1%)**, and **Eti-Osa (39.1%)** lies below 5 m. This leaves these metropolitan hubs directly vulnerable to astronomical high tides, storm surge backflows, and hydraulic gravity-drain locking whenever heavy rainfall coincides with high lagoon water levels.

### 4.2.2 Synoptic Precipitation Gradient and Convective Cloudburst Extremes (Rx1day)
Figure 4.2b maps the spatial distribution of mean annual precipitation and short-duration storm intensity across the 20 LGAs.

![Figure 4.2b: Synoptic Precipitation Gradient and Convective Cloudburst Extremes across Lagos State](figures/map_02_spatial_rainfall_gradients.png)

**Detailed Interpretation & Key Findings from Figure 4.2b:**
- **Panel A (Synoptic Rainfall Climatology Gradient):** 16-year CHIRPS v2.0 satellite-gauge precipitation records reveal a pronounced regional gradient ranging from 1,394 mm/year in southwestern coastal corridors (**Ajeromi/Ifelodun**, **Badagry** at 1,460 mm) to over 1,760–1,780 mm/year along the central and eastern lagoon axis (**Lagos Island** at 1,763 mm, **Shomolu** at 1,765 mm, **Epe** at 1,779 mm).
- **Panel B (Convective Cloudburst Intensity - Rx1day):** Mean monthly maximum 1-day storm precipitation highlights local cloudburst hotspots where convective monsoonal cells dump 28–32 mm within a single 24-hour window. These sudden localized downpours routinely overwhelm tertiary urban street drainage regardless of regional annual totals, triggering acute pluvial flash floods in **Alimosho**, **Ikeja**, and **Kosofe**.

### 4.2.3 Urban Impervious Built-Up Surfaces and Wetland/Mangrove Ecological Buffers
Figure 4.2c illustrates the ecological contrast between artificial impervious surfaces and natural wetland retention buffers.

![Figure 4.2c: Urban Impervious Built-Up Surfaces and Wetland/Mangrove Ecological Retention Buffers](figures/map_03_landcover_mangrove_buffers.png)

**Detailed Interpretation & Key Findings from Figure 4.2c:**
- **Panel A (Urban Impervious Footprint):** High-resolution ESA WorldCover 10m mapping shows that inner metropolitan LGAs—**Agege (98.3%)**, **Surulere (97.0%)**, **Mushin (96.5%)**, **Shomolu (95.4%)**, **Ajeromi/Ifelodun (95.3%)**, and **Ifako/Ijaye (94.4%)**—are almost completely paved over. Impervious concrete and asphalt prevent groundwater infiltration, generating catastrophic surface runoff volumes ($C > 0.85$).
- **Panel B (Wetland & Mangrove Protective Natural Retention Buffers):** Identifies remaining ecological defenses. While urban core LGAs have <1% natural wetlands, outer coastal and riverine LGAs—**Lagos Island (25.3%)**, **Kosofe (18.0%)**, **Amuwo Odofin (17.9%)**, **Ojo (15.6%)**, **Badagry (10.9%)**, and **Epe (8.6%)**—rely heavily on mangrove belts to absorb tidal swells. Deforestation and wetland reclamation in these corridors directly strip away flood attenuation capacity."""

# Insert in Chapter 4 right before ### 4.3
if "### 4.2.1 High-Resolution Topographic Relief" not in text:
    old_target = "### 4.3 Non-Parametric Hypothesis Testing"
    text = text.replace(old_target, MAPS_CH4_TEXT + "\n\n" + old_target)
    print("Inserted Maps 01, 02, 03 into Chapter 4.")

# 2. Insert Map 04 in Chapter 6 right after Figure 6.1
MAP_CH6_TEXT = """### 6.2.1 Spatial Frontiers of Climate Risk Escalation (Delta FRI & Headcount Growth to 2050)
Figure 6.1a maps where climate change and sea-level rise accelerate risk fastest across Lagos State.

![Figure 6.1a: Spatial Frontiers of Climate Risk Escalation and Human Exposure Expansion (2010 to 2050)](figures/map_04_climate_risk_escalation_delta.png)

**Detailed Interpretation & Key Findings from Figure 6.1a:**
- **Panel A (Climate Change Risk Escalation Frontier - Delta FRI):** Maps the net increase in Composite Flood Risk Index from baseline to 2050 under SSP5-8.5. While island LGAs remain highest in absolute risk, the *fastest accelerating risk frontiers* emerge in peripheral corridors: **Epe (+10.2 FRI points)**, **Badagry (+9.1 points)**, **Ojo (+8.2 points)**, **Amuwo Odofin (+7.5 points)**, and **Alimosho (+5.7 points)**. In these territories, rising sea levels and expanding paved surfaces outpace drainage capacity.
- **Panel B (Net Growth in Flood-Exposed Residents):** Quantifies where the doubling of exposed population concentrates. Sprawling peri-urban corridors add massive headcounts directly into vulnerable zones: **Alimosho (+56,000 net exposed residents/yr)**, **Kosofe (+65,000)**, **Amuwo Odofin (+143,000)**, **Badagry (+140,000)**, **Ojo (+121,000)**, and **Eti-Osa (+84,000)**."""

if "### 6.2.1 Spatial Frontiers of Climate Risk Escalation" not in text:
    old_target6 = "### 6.3 Extreme Value Theory"
    text = text.replace(old_target6, MAP_CH6_TEXT + "\n\n" + old_target6)
    print("Inserted Map 04 into Chapter 6.")

# 3. Insert Map 05 in Chapter 7 right after Figure 7.3
MAP_CH7_TEXT = """### 7.4 Spatial Policy Intervention & Operational Resilience Action Zoning
Figure 7.4 translates our predictive machine learning models and 2050 climate projections into an operational, multi-tier spatial zoning framework for **LASEMA**, **NIHSA**, and the **Lagos State Ministry of the Environment and Water Resources**.

![Figure 7.4: Lagos State Operational Flood Resilience and Policy Intervention Zoning Map](figures/map_05_policy_intervention_zoning.png)

**Detailed Interpretation & Key Findings from Figure 7.4:**
The 20 LGAs partition into four distinct operational policy zones, each requiring tailored structural and early-warning interventions:
- **Zone 1: Coastal Tidal Defense & Sluice Gates (Lagos Island, Apapa, Eti-Osa):** 
  - *Vulnerability Profile:* Extreme low elevation (>39% land <5 m), direct ocean/lagoon frontage, hydraulic backwater locking during high tide.
  - *Operational Mandate:* Construct automated tidal flap gates and high-capacity stormwater pumping stations at outfall mouths; build elevated sea-dike walls along vulnerable shorelines.
- **Zone 2: Fluvial Riverine Buffer & Dam Telemetry (Kosofe, Ikorodu):**
  - *Vulnerability Profile:* Lower Ogun River floodplain, compound flooding from upstream Oyan Dam releases during July and September–October.
  - *Operational Mandate:* Enforce strict 500-metre conservation buffer setbacks along the Agboyi-Ketu, Isheri, and Majidun wetland corridors; integrate real-time acoustic water-level telemetry with LASEMA emergency alerts.
- **Zone 3: Core Pluvial Desilting & Pavement Retrofit (Surulere, Mushin, Mainland, Agege, Oshodi/Isolo, Shomolu):**
  - *Vulnerability Profile:* Extreme impervious built-up cover (>85–98%), pluvial street flash flooding from short convective cloudbursts.
  - *Operational Mandate:* Implement mandatory biannual pre-peak collector desilting (Phase I before May 1, Phase II in August); retrofit roads with permeable asphalt and infiltration basins.
- **Zone 4: Peri-Urban SUDS & Permeable Mandates (Alimosho, Ojo, Badagry, Ibeju-Lekki, Epe, Amuwo Odofin, Ifako/Ijaye, Ikeja):**
  - *Vulnerability Profile:* Fastest risk acceleration (Delta FRI up to +10.2 points), massive population influx into natural retention basins.
  - *Operational Mandate:* Mandate Sustainable Urban Drainage Systems (SUDS)—requiring 25% permeable green footprints and on-site detention basins for all new private residential estate approvals."""

if "### 7.4 Spatial Policy Intervention & Operational Resilience" not in text:
    old_target7 = "## Chapter 8: Discussion"
    text = text.replace(old_target7, MAP_CH7_TEXT + "\n\n---\n\n" + old_target7)
    print("Inserted Map 05 into Chapter 7.")

REPORT_MD.write_text(text, encoding="utf-8")
if ARTIFACT.exists():
    ARTIFACT.write_text(text, encoding="utf-8")
print("Report successfully updated with all 5 new map visualizations!")
