"""
Integrate 5 new advanced figures and rich mechanistic explanations into Final_Project_Report.md
and rebuild the Word .docx report.
"""

from pathlib import Path
import re

ROOT = Path(r"c:\Users\LENOVO\Desktop\Portfolio Projects\lagos-flood-risk-ml")
REPORT_MD = ROOT / "outputs" / "Final_Project_Report.md"
ARTIFACT = Path(r"C:\Users\LENOVO\.gemini\antigravity\brain\dbbda659-ab1c-425a-952f-42069ce27ace\final_project_report.md")

WAM_COMPOUND_TEXT = """### 4.4 Atmospheric & Hydrological Mechanics of the West African Monsoon (WAM)
The seasonal flood regime in Lagos State is governed by large-scale synoptic dynamics of the **West African Monsoon (WAM)**. As the Inter-Tropical Convergence Zone (ITCZ) migrates northward from the Gulf of Guinea between April and July, southwesterly maritime air masses convey massive convective moisture inland.

Lagos experiences a characteristic **bimodal rainfall distribution**:
1. **Primary Monsoon Surge (May–July):** Peak convective downpours occur in June (mean 265.4 mm), but flood incidence peaks in **July (49.7% of LGA-months)**. Hydrologically, July floods are driven by **antecedent moisture loading**: heavy June rain saturates the shallow coastal aquifer and elevates water levels in the Lagos and Lekki Lagoons, severely reducing soil infiltration capacity and gravity drain outfall head.
2. **The "August Break" (Little Dry Season / LDS):** In August, rainfall drops sharply to 86.8 mm (flood rate: 5.3%). This temporary respite is caused by cold coastal ocean upwelling in the Bight of Benin, which lowers sea surface temperatures (SSTs) and stabilizes the lower troposphere, suppressing deep convective storm formation.
3. **Secondary Peak & Compound Dam/Catchment Discharges (September–October):** As the ITCZ retreats southward over warming coastal waters, convective activity resumes in September (214.0 mm, 28.1% flood rate) and October (179.9 mm, 13.4% flood rate). In this secondary window, local pluvial cloudbursts are compounded by regional fluvial inflows from the 15,700 km² Ogun River basin and emergency floodgate releases from the upstream Oyan Dam.

### 4.5 The 3-Pillar Compound Flooding Nexus (Soil Saturation × Topography × Imperviousness)
Figure 4.6 decouples the non-linear interaction between hydrometeorological forcing, terrain vulnerability, and urban imperviousness.

![Figure 4.6: Compound Flooding Nexus — Soil Saturation, Elevation Tiers, and Impervious Landscape](figures/11_compound_flooding_nexus.png)

**Key Insights from Figure 4.6:**
- **The 300 mm Cumulative Saturation Threshold (Panel A):** In upland LGAs (<15% low-lying land), flood risk remains modest (<10%) even as 60-day rainfall climbs. However, in low-lying coastal and lagoon corridors (>35% land <5 m), crossing **300 mm of 60-day cumulative rainfall** triggers an exponential jump in empirical flood probability from 8.2% to **54.5%**.
- **The Hydro-Morphological Risk Landscape (Panel B):** Lagos LGAs partition into three distinct operational archetypes:
  - *Tidal & Coastal Lowlands (Lagos Island, Apapa, Eti-Osa, Ajeromi/Ifelodun):* Characterized by >35% low-elevation land (<5 m) and direct lagoon frontage, where flood events occur even at moderate rainfall due to high astronomical tides and backwater locking.
  - *Impervious Upland Catchments (Surulere, Mushin, Mainland, Agege, Oshodi/Isolo):* Sitting at 10–40 m elevation but with 80–98% paved cover, where intense 1-day cloudbursts (Rx1day) overwhelm secondary street drains within minutes.
  - *Rapidly Developing Peri-Urban Corridors (Alimosho, Kosofe, Ojo, Ikorodu):* Experiencing compound flash and riverine flooding driven by rapid paving over natural wetland retention basins.
"""

SPATIAL_DECISION_TEXT = """### 5.9 Spatial Transferability Analysis (Leave-One-LGA-Out Generalisation)
To verify whether the machine learning architecture can generalize to completely unseen administrative units without memorizing spatial identities, we conducted 20-fold Leave-One-LGA-Out (LOLO) cross-validation. Figure 5.6 maps each LGA's out-of-sample generalisation ROC-AUC and PR-AUC.

![Figure 5.6: Spatial Generalisation Performance across 20 Unseen LGAs](figures/12_spatial_generalization_map.png)

**Spatial Generalisation Findings:**
- Across all 20 spatial folds, Monotonic XGBoost achieves a **mean spatial ROC-AUC of 0.902** and mean PR-AUC of 0.493.
- **Top Transferability Performers:** Mature urban mainland LGAs—**Shomolu (0.958 ROC-AUC)**, **Oshodi/Isolo (0.949)**, **Agege (0.935)**, **Apapa (0.924)**, **Mushin (0.923)**, **Surulere (0.902)**, and **Lagos Island (0.891)**—achieve exceptional generalisation. Because these territories possess well-defined physical terrain and high imperviousness, the model accurately predicts their flood incidence purely from physics.
- **The Peri-Urban Challenge (Ibeju-Lekki):** Ibeju-Lekki exhibits lower PR-AUC (0.289) despite high ROC-AUC (0.858). As the fastest-expanding industrial corridor in West Africa, its historical 2010–2016 flood base rate was near zero, but rapid land reclamation post-2018 created sudden drainage bottlenecks, demonstrating why dynamic annual satellite land-cover updates are essential.

### 5.10 Operational Early-Warning Decision Frontier & Cost-Loss Economics
For emergency management agencies (**LASEMA** and **NEMA**), selecting a decision threshold (τ) involves a direct trade-off between the cost of preventive intervention (C) and the loss of unmitigated flooding (L). Figure 5.7 presents the operational verification frontier and economic cost-loss curve ($C/L = 0.20$).

![Figure 5.7: Operational Early-Warning Frontier and Cost-Loss Optimization Curve](figures/14_early_warning_decision_tradeoff.png)

**Operational Threshold Guidelines:**
1. **Public Watch & Drain Desilting Alert (τ = 0.19):** Optimal for municipal public works. Achieves Hit Rate (POD) = 0.530 with CSI = 0.357, capturing flood threats early with zero dry-season false alarms.
2. **Economic Minimum-Expense Threshold (τ = 0.21):** Minimizes total municipal disaster expense ($C \cdot (TP+FP) + L \cdot FN$).
3. **High-Certainty Emergency Evacuation Alarm (τ = 0.38):** Recommended for triggering costly logistical deployments, staging rescue boats, and ordering school/market closures. At this threshold, Precision exceeds 65%, ensuring false alarms are minimized to preserve public trust.
"""

CMIP6_SEASON_TEXT = """### 6.5 Climate Change Impacts on Monsoon Seasonality and Storm Extremes (2010–2050)
Figure 6.3 illustrates how greenhouse gas forcing under SSP2-4.5 and SSP5-8.5 alters the seasonal precipitation envelope and convective storm extremes across Lagos State.

![Figure 6.3: CMIP6 Multi-Model Monsoon Seasonality and Storm Intensification (2010–2050)](figures/10_cmip6_seasonal_monsoon_shift.png)

**Key Climatological Findings:**
- **Monsoonal Extension & Peak Intensification (Panel A):** Under SSP5-8.5 by 2050, mean June rainfall rises from 265.4 mm to 288.5 mm (+8.7%), while July rainfall rises from 207.2 mm to 226.4 mm (+9.3%). The wet-season shoulder in October expands (+11.2%), prolonging the compound flood hazard window into late autumn.
- **Convective Storm Intensification (Panel B):** In accordance with the Clausius–Clapeyron thermodynamic relation (~7% increase in atmospheric water-holding capacity per degree of warming), multi-day cloudburst intensity (Rx3day) intensifies across all geomorphic zones:
  - *Coastal Barrier Zone:* Rx3day increases from 61.4 mm to **69.8 mm (+13.7%)**.
  - *Lagoon/Riverine Zone:* Rx3day increases from 59.8 mm to **68.3 mm (+14.2%)**.
  - *Inland Upland Zone:* Rx3day increases from 58.2 mm to **63.9 mm (+9.8%)**.
"""

TRAJECTORY_MATRIX_TEXT = """### 7.3 Multi-Decadal Flood Risk Index (FRI) Trajectory Matrix (2010–2050)
Figure 7.3 provides a comprehensive heatmap matrix tracking the evolution of the Composite Flood Risk Index (FRI) across all 20 LGAs from the historical baseline through the 2030s, 2040s, and 2050 under both SSP pathways.

![Figure 7.3: 20-LGA Flood Risk Trajectory Heatmap Matrix (Baseline to 2050)](figures/13_lga_risk_trajectory_heatmap.png)

**Key Takeaways from the Trajectory Matrix:**
- **Tier 1 Critical Hotspots (FRI > 50 by 2050):** Six LGAs cross the High Risk threshold: **Lagos Island (56.5)**, **Apapa (56.2)**, **Kosofe (52.6)**, **Eti-Osa (51.8)**, **Amuwo Odofin (51.7)**, and **Ajeromi/Ifelodun (51.0)**.
- **Fastest Escalating Risk LGAs:** The steepest rate of risk acceleration occurs in **Amuwo Odofin (+7.5 FRI points)**, **Badagry (+9.1 points)**, **Ojo (+8.2 points)**, and **Epe (+10.2 points)**. In these corridors, the combination of sea-level rise encroaching on low terrain and rapid demographic expansion causes risk to compound faster than in mature urban centers.
"""

def update_report():
    text = REPORT_MD.read_text(encoding="utf-8")
    
    # Insert WAM and Compound nexus in Chapter 4
    if "### 4.4 Atmospheric & Hydrological Mechanics" not in text:
        old_c5 = "## Chapter 5: Machine Learning"
        new_c5 = WAM_COMPOUND_TEXT + "\n---\n\n" + old_c5
        text = text.replace(old_c5, new_c5)
        print("Inserted Chapter 4 mechanics.")

    # Insert Spatial transferability and Cost-Loss in Chapter 5
    if "### 5.9 Spatial Transferability Analysis" not in text:
        old_c6 = "## Chapter 6: Climate-Scenario Projections"
        new_c6 = SPATIAL_DECISION_TEXT + "\n---\n\n" + old_c6
        text = text.replace(old_c6, new_c6)
        print("Inserted Chapter 5 spatial & decision frontier.")

    # Insert CMIP6 seasonality shift in Chapter 6
    if "### 6.5 Climate Change Impacts" not in text:
        old_c7 = "## Chapter 7: Composite Flood Risk Index"
        new_c7 = CMIP6_SEASON_TEXT + "\n---\n\n" + old_c7
        text = text.replace(old_c7, new_c7)
        print("Inserted Chapter 6 monsoon & storm shift.")

    # Insert Trajectory Heatmap Matrix in Chapter 7
    if "### 7.3 Multi-Decadal Flood Risk Index" not in text:
        old_c8 = "## Chapter 8: Discussion, Limitations"
        new_c8 = TRAJECTORY_MATRIX_TEXT + "\n---\n\n" + old_c8
        text = text.replace(old_c8, new_c8)
        print("Inserted Chapter 7 trajectory matrix.")

    REPORT_MD.write_text(text, encoding="utf-8")
    if ARTIFACT.exists():
        ARTIFACT.write_text(text, encoding="utf-8")
    print("Report files successfully updated!")

if __name__ == "__main__":
    update_report()
