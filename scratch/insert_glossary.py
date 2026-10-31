"""
Script to insert a Comprehensive Technical and Layman-Friendly Glossary into outputs/Final_Project_Report.md.
Also adds a concise List of Acronyms and Abbreviations right after the Abstract.
"""

from pathlib import Path
import re

REPORT_PATH = Path("outputs/Final_Project_Report.md")
text = REPORT_PATH.read_text(encoding="utf-8")

# 1. Executive Acronyms List to place right after Abstract (before Chapter 1)
EXECUTIVE_ACRONYMS = """
---

## Executive List of Acronyms and Abbreviations

| Acronym / Abbreviation | Full Name / Description | Primary Application in this Report |
| :--- | :--- | :--- |
| **API** | Antecedent Precipitation Index | Quantifies prior soil moisture accumulation (30-day and 60-day lag) |
| **BSS** | Brier Skill Score | Measures probabilistic forecast skill relative to historical climatology |
| **CHIRPS** | Climate Hazards Group InfraRed Precipitation with Stations | 5.5 km daily satellite-gauge rainfall dataset (16 years, 116,880 observations) |
| **CMIP6** | Coupled Model Intercomparison Project Phase 6 | Multi-model climate simulation standard underpinning IPCC Sixth Assessment |
| **CSI** | Critical Success Index (Threat Score) | WMO-standard verification metric balancing detection against false alarms |
| **DEM** | Digital Elevation Model | USGS SRTM 30m gridded terrestrial land surface elevation |
| **ESA** | European Space Agency | Source of 10m WorldCover impervious and wetland land-cover classification |
| **EVT / GEV** | Extreme Value Theory / Generalized Extreme Value | Statistical distribution used to model multi-decadal storm return levels |
| **FAR** | False Alarm Ratio | Proportion of issued flood alarms that did not materialize in documented floods |
| **FRI** | Composite Flood Risk Index | Unified 0–100 score integrating Hazard, Vulnerability, and Exposure |
| **GCM** | General Circulation Model / Global Climate Model | 3D numerical models simulating Earth's atmospheric and oceanic physics |
| **GEE** | Google Earth Engine | Cloud-native geospatial processing platform used for satellite extractions |
| **IPCC** | Intergovernmental Panel on Climate Change | United Nations body assessing climate change science, impacts, and options |
| **JRC GSW** | Joint Research Centre Global Surface Water | 30m global record used to mask water bodies and calculate water proximity |
| **LASEMA** | Lagos State Emergency Management Agency | Primary state emergency responder responsible for flood alerts and rescues |
| **LGA** | Local Government Area | Administrative unit of study in Lagos State (20 official LGAs) |
| **LOLO** | Leave-One-LGA-Out Cross-Validation | 20-fold spatial generalisation test verifying model transferability |
| **NEX-GDDP** | NASA Earth Exchange Global Daily Downscaled Projections | 25 km bias-corrected daily climate series downscaled for Lagos State |
| **NIHSA** | Nigeria Hydrological Services Agency | Federal agency issuing the national Annual Flood Outlook (AFO) |
| **NIMET** | Nigerian Meteorological Agency | Federal meteorological agency providing seasonal climate predictions |
| **POD** | Probability of Detection (Hit Rate / Recall) | Proportion of actual historical flood events successfully flagged |
| **PR-AUC** | Precision-Recall Area Under Curve | Performance metric evaluating predictive skill on imbalanced binary data |
| **ROC-AUC** | Receiver Operating Characteristic Area Under Curve | Diagnostic metric evaluating discrimination across all classification thresholds |
| **Rx1day** | Maximum 1-Day Precipitation | Heaviest single-day rainfall total in a calendar month (cloudburst intensity) |
| **SHAP** | SHapley Additive exPlanations | Game-theoretic method explaining individual feature contributions in ML |
| **SLR** | Sea-Level Rise | IPCC AR6 projected regional oceanic rise (+0.29m to +0.40m by 2050) |
| **SSP** | Shared Socioeconomic Pathways | IPCC climate forcing pathways (SSP2-4.5 Moderate; SSP5-8.5 High) |
| **SUDS** | Sustainable Urban Drainage Systems | Engineering approach mimicking natural drainage via permeable paving and ponds |
| **WAM** | West African Monsoon | Dominant tropical wind system generating Lagos's bimodal rainy seasons |
| **WMO** | World Meteorological Organization | UN specialised agency establishing international meteorological standards |
| **XGBoost** | eXtreme Gradient Boosting | Gradient-boosted decision tree library configured with monotonic constraints |

"""

# 2. Comprehensive Glossary to add as Chapter 10 (before References)
FULL_GLOSSARY = r"""
---

## Chapter 10: Comprehensive Glossary of Technical Terms, Acronyms, and Concepts

This glossary provides formal technical definitions, underlying mathematical formulations, and plain-English layman explanations for the key concepts spanning remote sensing, hydrology, machine learning, and climate science used throughout this report.

```
GLOSSARY DOMAIN INDEX:
Section 10.1: Institutional Bodies and Remote Sensing Earth Observation Datasets
Section 10.2: Hydrology, Urban Geomorphology, and Drainage Engineering
Section 10.3: Machine Learning, Statistical Calibration, and Model Verification
Section 10.4: Climate Change Scenarios, Extreme Value Theory, and Risk Formulations
```

---

### 10.1 Institutional Bodies and Earth Observation Platforms

#### 1. CHIRPS (Climate Hazards Group InfraRed Precipitation with Stations)
* **Technical Definition:** A quasi-global (50°S–50°N), 0.05° (~5.5 km) high-resolution gridded daily rainfall dataset produced by the USGS Earth Resources Observation and Science (EROS) Center and the Climate Hazards Center at UC Santa Barbara. CHIRPS blends cold cloud duration (CCD) satellite infrared observations with calibrated in-situ ground weather station measurements.
* **Layman Explanation:** A high-tech "weather map in the sky" that combines daily satellite cloud images with real ground rain gauges to estimate exactly how many millimeters of rain fell over each neighborhood in Lagos every day since 1981.
* **Project Context:** Used as the primary historical rainfall engine across all 20 LGAs over 16 years (2010–2025; 116,880 daily observations).

#### 2. SRTM (Shuttle Radar Topography Mission)
* **Technical Definition:** A digital elevation dataset acquired in February 2000 by a modified radar system flown aboard the Space Shuttle Endeavour (mission STS-99). Provides global 1-arc-second (~30 m) digital elevation data referenced to the WGS84 ellipsoid and EGM96 geoid.
* **Layman Explanation:** A satellite radar scan that mapped the physical height of the Earth's surface. In our project, it tells us which parts of Lagos are high ground (hills) and which are low-lying basins sitting near sea level.
* **Project Context:** Masked with permanent water bodies to isolate terrestrial elevation. Revealed that over 40% to 52% of land in coastal island LGAs sits less than 5 metres above sea level.

#### 3. JRC GSW (Joint Research Centre Global Surface Water)
* **Technical Definition:** A 30 m resolution global database developed by the European Commission's Joint Research Centre mapping the spatial and temporal distribution of surface water over 38 years using 4.5+ million Landsat satellite scenes.
* **Layman Explanation:** A satellite dataset that tracks where water permanently exists on Earth. It allowed us to accurately mask out the Lagos Lagoon and ocean so they do not distort land elevation measurements.
* **Project Context:** Used to compute Euclidean distance to permanent water bodies (`dist_water_mean_km`) and the share of land within 1 km of water (`near_water_1km_share`).

#### 4. ESA WorldCover (European Space Agency WorldCover 10m)
* **Technical Definition:** A 10 m resolution global land-cover map generated from Sentinel-1 radar and Sentinel-2 optical imagery by a consortium led by VITO Remote Sensing under the European Space Agency.
* **Layman Explanation:** A detailed satellite land-use map that classifies every 10-meter square in Lagos as concrete buildings, roads, water, grassland, or mangrove wetlands.
* **Project Context:** Quantified impervious urban surfaces (`built_share`) and surviving mangrove retention buffers (`wetland_mangrove_share`).

#### 5. WorldPop
* **Technical Definition:** An open-access spatial demographic dataset producing high-resolution (3-arc-second / ~100 m) gridded population distribution estimates using random forest dasymetric disaggregation informed by census counts and geospatial building covariates.
* **Layman Explanation:** A computer model that estimates how many human beings live in each 100-meter block of land across Lagos, providing reliable demographic numbers between national census years.
* **Project Context:** Provided annual population counts and density estimates used to calculate human exposure to flooding.

#### 6. GADM (Database of Global Administrative Areas)
* **Technical Definition:** A high-resolution spatial database of administrative boundaries across all countries at multiple sub-national tiers (Level 0: Country; Level 1: State/Province; Level 2: Local Government Area/District).
* **Layman Explanation:** Official digital boundary maps that trace the exact borders between the 20 Local Government Areas in Lagos State.

#### 7. NIHSA (Nigeria Hydrological Services Agency)
* **Technical Definition:** The apex federal agency under the Federal Ministry of Water Resources and Sanitation mandated to assess, evaluate, and forecast Nigeria's water resources, responsible for publishing the official national Annual Flood Outlook (AFO).
* **Layman Explanation:** The Nigerian government agency responsible for monitoring rivers, dams, and flood risks nationwide.

#### 8. LASEMA (Lagos State Emergency Management Agency)
* **Technical Definition:** The dedicated emergency management and disaster-response authority established under the Lagos State Emergency Management Agency Law of 2008, responsible for disaster mitigation, search and rescue, and flood relief operations.
* **Layman Explanation:** Lagos State's "first responders" who clear flood disaster zones, rescue stranded citizens, and coordinate emergency evacuations during major storms.

#### 9. WMO (World Meteorological Organization)
* **Technical Definition:** A specialized agency of the United Nations dedicated to international cooperation and standardization in meteorology, operational hydrology, and climate science.
* **Layman Explanation:** The global authority that sets scientific standards for measuring weather forecasts, rainfall records, and flood warnings.

---

### 10.2 Hydrology, Urban Geomorphology, and Drainage Engineering

#### 10. Pluvial Flooding (Surface Runoff / Flash Flooding)
* **Technical Definition:** Inundation caused directly by extreme atmospheric precipitation exceeding the local infiltration capacity of the soil and the hydraulic discharge capacity of surface drainage networks, occurring independently of overflowing watercourses.
* **Layman Explanation:** "Street gutter flooding." When rain falls faster than concrete city gutters can drain it away, turning streets and roads into fast-moving rivers.
* **Project Context:** Common in dense mainland LGAs (Surulere, Mushin, Agege) where concrete cover exceeds 95%.

#### 11. Fluvial Flooding (Riverine Inundation)
* **Technical Definition:** Flooding that occurs when the volumetric discharge of a natural river, stream, or channel exceeds its bankfull conveyance capacity, causing water to overtop its banks and inundate adjacent floodplains.
* **Layman Explanation:** "River overflow." When heavy upstream rains fill major rivers (like the Ogun River) until they burst their banks and flood surrounding communities.
* **Project Context:** Concentrated in the lower Ogun River floodplain (Kosofe and Ikorodu), especially when compounded by water releases from the upstream Oyan Dam.

#### 12. Coastal Surge and Tidal Backwater Locking
* **Technical Definition:** Inundation driven by astronomical high tides, meteorological storm surges, and mean sea-level rise along coastal boundaries. "Tidal backwater locking" refers to the hydraulic phenomenon where elevated tailwater levels in the receiving water body (ocean or lagoon) eliminate the positive hydrostatic head gradient of terrestrial drainage channels, preventing gravity outflow and forcing water to back up into urban collector networks.
* **Layman Explanation:** When the ocean tide rises higher than the street drains, water cannot flow out into the lagoon. In fact, sea water flows *backward* up through the storm drains and bubbles up onto city roads even after rain stops.
* **Project Context:** Affects coastal island and estuarine LGAs (Lagos Island, Apapa, Eti-Osa) where land lies below 5 metres.

#### 13. Compound Flooding
* **Technical Definition:** The simultaneous or sequential co-occurrence of multiple flood drivers (e.g., intense convective precipitation, saturated catchment soil moisture, river discharge, and coastal/lagoon high tides) whose joint interaction generates extreme impact exceeding that of each individual driver in isolation.
* **Layman Explanation:** A "triple disaster." When heavy local rain, overflowing rivers from upstream, and high ocean tides all hit Lagos on the exact same day, causing massive, prolonged flooding.

#### 14. Antecedent Soil Moisture & Precipitation Index (API)
* **Technical Definition:** The residual moisture content stored in the unsaturated soil vadose zone prior to a precipitation event, resulting from cumulative rainfall over previous days or months minus evapotranspiration and deep percolation. Governs the soil moisture deficit and determines the fraction of new rainfall converted into surface runoff.
* **Layman Explanation:** How "soggy" the ground already is before a new storm starts. If a sponge is already soaked full of water, any new water poured on it will spill straight off onto the table.
* **Project Context:** Explains why Lagos floods most frequently in July (49.7% flood rate) even though June receives more rainfall: June rains soak the soil full, leaving zero absorption capacity for July storms.

#### 15. Convective Cloudburst (Rx1day Extreme)
* **Technical Definition:** A sudden, high-intensity, short-duration convective precipitation event delivering high volumetric rainfall rates (often >25–35 mm/hour or >75–120 mm/24 hours) associated with cumulonimbus cell development along tropical squall lines.
* **Layman Explanation:** A sudden, violent tropical rain dump where the sky opens up and pours torrential rain for a few hours, instantly overwhelming street drains.
* **Project Context:** Captured via `rain_max_daily_mm` (Rx1day) and `rain_max_3day_mm` in our machine learning feature stack.

#### 16. Little Dry Season (LDS) / "August Break"
* **Technical Definition:** A climatological phenomenon characteristic of the coastal Guinea Coast of West Africa during July/August, characterized by a temporary suppression of convective precipitation caused by ocean upwelling, sea surface temperature cooling in the northern Gulf of Guinea, and atmospheric stability, creating a distinct bimodal monsoonal curve.
* **Layman Explanation:** The 2-to-3 week lull in rainfall during August where rain temporarily drops before returning in September and October.
* **Project Context:** Rainfall in Lagos drops from 207.2 mm in July down to 86.8 mm in August, reducing flood occurrence to 5.3%.

#### 17. Runoff Coefficient ($C$) and Impervious Built Cover (`built_share`)
* **Technical Definition:** In the Rational Formula for peak urban discharge ($Q = C \cdot I \cdot A$), the dimensionless runoff coefficient $C$ represents the proportion of rainfall converted into direct surface runoff (ranging from $C \approx 0.15$ on natural forest to $C > 0.85–0.95$ on asphalt and concrete).
* **Layman Explanation:** The percentage of rain that turns into flowing street runoff instead of soaking into the soil. Concrete has a runoff coefficient near 1.0 (100% runoff), while grass and wetlands absorb most rain.
* **Project Context:** Inner metropolitan LGAs (Surulere, Mushin, Agege) exceed 95% impervious cover, driving instant flash flooding.

#### 18. Sustainable Urban Drainage Systems (SUDS)
* **Technical Definition:** A sequence of water management practices and engineering facilities designed to align urban stormwater drainage with natural hydrological cycles by promoting retention, infiltration, detention, and biological treatment (e.g., permeable pavements, bioswales, rain gardens, and retention basins).
* **Layman Explanation:** Eco-friendly building rules—like porous parking lots that let rain soak through the gravel, and neighborhood retention ponds that store floodwater safely.

#### 19. Tidal Flap Gate / Sluice Gate
* **Technical Definition:** A passive, one-way check valve installed at the ocean or lagoon outfall of an urban stormwater channel. Opens under positive terrestrial head pressure to allow stormwater to discharge, but closes automatically when ocean tidal levels exceed the canal water level, preventing saltwater intrusion and tidal backflow.
* **Layman Explanation:** A giant one-way door on a drainage canal. It lets rainwater flow out into the ocean, but automatically slams shut when the ocean tide rises so seawater cannot flow backward into city streets.

---

### 10.3 Machine Learning, Statistical Calibration, and Verification

#### 20. Supervised Machine Learning
* **Technical Definition:** A paradigm in machine learning where an algorithm learns a mapping function $f: X \rightarrow Y$ from input feature vectors $X$ to target ground-truth labels $Y$ using empirical risk minimization.
* **Layman Explanation:** Teaching a computer algorithm by showing it historical examples: "Here is the weather and terrain in Lagos in June 2018 (inputs), and here is whether it flooded or not (outcome). Learn the mathematical pattern so you can predict future floods."

#### 21. XGBoost (eXtreme Gradient Boosting)
* **Technical Definition:** A scalable, distributed gradient-boosted decision tree algorithm that minimizes a regularized objective function combining convex loss and tree-complexity penalties using second-order Taylor approximations.
* **Layman Explanation:** A powerful ensemble of hundreds of decision trees that learn step-by-step from each other's mistakes to make accurate predictions.

#### 22. Monotonic Constraints
* **Technical Definition:** A structural constraint enforced during tree splitting requiring that the model prediction must be a non-decreasing (or non-increasing) monotonic function of a specific feature: $\frac{\partial \hat{y}}{\partial x_j} \ge 0$.
* **Layman Explanation:** Forcing the AI to obey common sense: "More rain can NEVER decrease flood risk; it can only increase it or keep it the same." This prevents the computer from making non-physical predictions when projecting into the future.
* **Project Context:** Enforced on `rain_total_mm`, `rain_max_daily_mm`, `rain_max_3day_mm`, `rain_prev_month_mm`, `low5_share`, and `built_share`.

#### 23. Receiver Operating Characteristic — Area Under Curve (ROC-AUC)
* **Technical Definition:** The integral of the True Positive Rate (Sensitivity) plotted against the False Positive Rate ($1 - \text{Specificity}$) across all classification thresholds $\tau \in [0, 1]$. Represents the probability that the model ranks a randomly chosen positive instance higher than a randomly chosen negative instance.
* **Layman Explanation:** A report card grade from 0.5 (pure guesswork / coin toss) to 1.0 (perfect prediction) measuring how well the AI distinguishes between flood months and dry months.
* **Project Context:** Our calibrated XGBoost achieved a held-out test ROC-AUC of **0.890** (an "A" grade).

#### 24. Precision-Recall Area Under Curve (PR-AUC)
* **Technical Definition:** The area under the curve plotting Precision ($\frac{TP}{TP + FP}$) against Recall ($\frac{TP}{TP + FN}$). Unlike ROC-AUC, PR-AUC does not credit true negatives and is the gold standard for rare-event, imbalanced classification tasks.
* **Layman Explanation:** A much tougher test than ROC-AUC when floods are rare. It specifically checks: "When the model issues a flood alarm, is it usually right? And does it catch all the actual disasters?"
* **Project Context:** Test PR-AUC was **0.460**—more than 3 times higher than the naive random baseline (0.151).

#### 25. Brier Score (BS) and Brier Skill Score (BSS)
* **Technical Definition:** The mean squared error of probabilistic predictions:
  $$BS = \frac{1}{N}\sum_{i=1}^{N}(p_i - y_i)^2$$
  Decomposed via Sanders-Murphy into Reliability ($REL$), Resolution ($RES$), and Climatology Uncertainty ($UNC$):
  $$BS = REL - RES + UNC$$
  The Brier Skill Score measures improvement over climatology:
  $$BSS = 1 - \frac{BS}{BS_{\text{clim}}}$$
* **Layman Explanation:** Checks whether probability numbers are honest. If the model says there is an 80% chance of rain, does it actually flood 80% of the time? A lower Brier Score means more honest, reliable probabilities.
* **Project Context:** Test Brier Score was **0.1092**, delivering a positive Brier Skill Score of $+0.147$ over climatological baseline guessing.

#### 26. Critical Success Index (CSI / Threat Score)
* **Technical Definition:** The ratio of successful event hits to the total number of hits, misses, and false alarms:
  $$CSI = \frac{TP}{TP + FP + FN}$$
* **Layman Explanation:** The international weather agency standard for measuring warning accuracy. Penalizes both missed floods and cried-wolf false alarms.
* **Project Context:** Reached its peak operational efficiency of $0.357$ at decision threshold $\tau^* = 0.19$.

#### 27. TreeSHAP (SHapley Additive exPlanations)
* **Technical Definition:** A game-theoretic method for explaining tree ensemble model outputs by calculating the unique Shapley marginal contribution of each input feature across all possible feature subsets:
  $$\hat{f}(x) = \phi_0 + \sum_{j=1}^{M}\phi_j(x)$$
* **Layman Explanation:** The "black-box opener." It mathematically breaks down each individual flood prediction to tell decision-makers: "This month's flood alarm was caused 40% by heavy 3-day rainfall, 30% by saturated soil from last month, and 30% by low elevation."

#### 28. Leave-One-LGA-Out (LOLO) Spatial Generalisation
* **Technical Definition:** A 20-fold spatial cross-validation scheme where the model is iteratively trained on 19 LGAs and evaluated on the 1 single held-out LGA, repeated across all 20 LGAs.
* **Layman Explanation:** The ultimate honesty test: "Can the AI accurately predict floods in an LGA it has never seen before?" Proves that the model learned real physics rather than just memorizing town names.
* **Project Context:** Achieved a mean spatial ROC-AUC of **0.902**, proving high transferability.

#### 29. Moran's I (Spatial Autocorrelation)
* **Technical Definition:** A global inferential statistic measuring spatial clustering or dispersion of a continuous variable or regression residual across geographic units based on a spatial weight matrix $W$:
  $$I = \frac{N}{S_0} \frac{\sum_{i}\sum_{j} w_{ij}(z_i - \bar{z})(z_j - \bar{z})}{\sum_{i}(z_i - \bar{z})^2}$$
* **Layman Explanation:** A test that checks whether prediction errors clump together in neighboring towns. If Moran's I is near zero, it proves that errors are random and the model has not missed any regional geographic factor.
* **Project Context:** Residual Moran's I on the test set was $+0.041$ ($p = 0.284$, statistically indistinguishable from zero), confirming spatial independence.

#### 30. Cost-Loss Ratio ($C/L$)
* **Technical Definition:** An economic decision-theory framework evaluating the monetary trade-off between the proactive cost of preventive action ($C$, e.g., deploying emergency pumps or clearing drains) and the unmitigated disaster loss ($L$, e.g., damaged infrastructure and property destruction). Under cost-loss optimization, the optimal alert threshold $\tau_{\text{opt}}$ occurs where $\tau = C/L$.
* **Layman Explanation:** Comparing the price of an umbrella against the cost of getting your suit ruined. For a typical municipal ratio of $C/L = 0.20$, the cheapest strategy is to take action whenever flood probability exceeds 21%.

---

### 10.4 Climate Change Projections, Extreme Value Theory, and Risk

#### 31. CMIP6 (Coupled Model Intercomparison Project Phase 6)
* **Technical Definition:** The sixth collaborative framework of global climate modeling centers coordinating standardized numerical climate experiments under the World Climate Research Programme (WCRP), serving as the foundational modeling basis for the IPCC Sixth Assessment Report (AR6).
* **Layman Explanation:** The premier global scientific effort where the world's leading supercomputer climate modeling centers run standardized simulations of future global weather patterns up to the year 2100.
* **Project Context:** We downscaled daily precipitation from 5 major CMIP6 models: ACCESS-CM2, CNRM-ESM2-1, EC-EARTH3, MPI-ESM1-2-HR, and MRI-ESM2-0.

#### 32. Shared Socioeconomic Pathways (SSPs)
* **Technical Definition:** Scenarios of projected global socioeconomic developments and greenhouse gas concentration trajectories through 2100 adopted by the IPCC:
  * **SSP2-4.5 ("Middle of the Road"):** Intermediate greenhouse gas mitigation where carbon emissions hover around current levels before declining after 2050, resulting in an additional radiative forcing of $+4.5\text{ W/m}^2$ by 2100.
  * **SSP5-8.5 ("Fossil-Fueled Development"):** High-emissions, fossil-fuel intensive economic development characterized by rapid energy consumption, leading to $+8.5\text{ W/m}^2$ radiative forcing by 2100.
* **Layman Explanation:** Two contrasting visions of our planet's future:
  * **SSP2-4.5**: The realistic "middle course," where countries gradually adopt green energy and emissions slowly stabilize.
  * **SSP5-8.5**: The "business-as-usual / worst-case" scenario, where humanity continues burning high amounts of oil, coal, and gas without major environmental policies.

#### 33. Hawkins-Sutton Uncertainty Partitioning
* **Technical Definition:** A variance decomposition methodology formulated by Hawkins and Sutton (2009) that separates the total projection variance in climate model predictions into three distinct orthogonal components:
  1. **Internal Variability ($V$):** Unforced chaotic atmospheric-ocean fluctuations (e.g., ENSO).
  2. **Model Uncertainty ($M$):** Structural differences in how different climate models simulate physical processes.
  3. **Scenario Uncertainty ($S$):** Divergence between socioeconomic emissions trajectories.
* **Layman Explanation:** A mathematical technique that answers: "When future climate predictions differ, is it because of natural random weather swings, differences between supercomputer models, or because we don't know how much fossil fuel humans will burn?"
* **Project Context:** Proved that for the 2030–2050 planning horizon in Lagos, **model differences account for >99.9% of uncertainty**, proving that using an ensemble of 5 different models is essential.

#### 34. Generalized Extreme Value (GEV) Distribution & Return Period
* **Technical Definition:** A three-parameter family of continuous probability distributions (combining Gumbel, Fréchet, and Weibull families) used in Extreme Value Theory (EVT) to model the block maxima (e.g., annual maximum daily precipitation, Rx1day):
  $$F(x; \mu, \sigma, \xi) = \exp\left\{-\left[1 + \xi\left(\frac{x - \mu}{\sigma}\right)\right]^{-1/\xi}\right\}$$
  The "Return Period" ($T$) is the inverse of the annual exceedance probability ($T = 1/P$), representing the average recurrence interval between storms exceeding a given threshold.
* **Layman Explanation:** A statistical method that models rare, once-in-a-generation catastrophic storms. A "50-year storm" doesn't mean it happens only once every 50 years; it means there is a 2% chance of it hitting in any given year.
* **Project Context:** Proved that an 86.4 mm 1-day storm has a 50-year return level state-wide, but triggers a **100% flood occurrence rate** in coastal barrier LGAs.

#### 35. Relative Sea-Level Rise (RSLR)
* **Technical Definition:** The net change in ocean surface height relative to the adjacent coastal terrestrial land surface, combining global eustatic sea-level changes (thermal expansion and ice sheet melt) with local vertical land motion (subsidence or tectonic uplift).
* **Layman Explanation:** The actual rise of the ocean water against the Lagos shoreline, taking into account melting polar ice caps and the sinking of low-lying reclaimed sandy soil.
* **Project Context:** Under IPCC AR6 projections, relative sea-level rise along the Lagos coast is projected to reach **+0.29 metres under SSP2-4.5** and **+0.40 metres under SSP5-8.5 by 2050**.

#### 36. Composite Flood Risk Index (FRI)
* **Technical Definition:** An integrated dimensionless risk metric (scaled 0–100) formulated in accordance with the UNDRR/IPCC risk framework ($R = H \times V \times E$):
  $$FRI = \left(w_H \cdot H_{\text{norm}} + w_V \cdot V_{\text{norm}} + w_E \cdot E_{\text{norm}}\right) \times 100$$
  where $H$ is the modeled monthly flood hazard probability, $V$ is physical vulnerability (low elevation and high imperviousness), and $E$ is demographic exposure (population density).
* **Layman Explanation:** A single, easy-to-read "risk score" from 0 (very low risk) to 100 (extreme disaster danger) that combines:
  1. **Hazard**: How likely it is to flood.
  2. **Vulnerability**: How flat, paved, and prone to trapping water the ground is.
  3. **Exposure**: How many thousands of human beings live in the danger zone.
* **Project Context:** Rises from a historical baseline score of **38.8 to 44.0 by 2050**, with peripheral growth LGAs (Epe, Badagry, Ojo) experiencing the sharpest increases (+8 to +10.2 points).

#### 37. Population Exposure (Exposed Headcount)
* **Technical Definition:** The estimated absolute number of permanent human residents residing within geographic zones subject to wet-season flood hazard:
  $$E_{\text{pop}} = \sum_{l \in \text{LGAs}} P_l(t) \cdot \bar{p}_{\text{wet}, l}(t)$$
  where $P_l(t)$ is the projected population of LGA $l$ in year $t$, and $\bar{p}_{\text{wet}, l}(t)$ is the mean wet-season monthly flood probability.
* **Layman Explanation:** The total number of men, women, and children living in neighborhoods where streets, homes, or businesses are predicted to flood during the rainy season.
* **Project Context:** Projected to double from **993,636 residents today to 1,982,207 residents by 2050 under SSP5-8.5**, driven primarily by demographic growth pushing people into unzoned floodplains.

"""

# Insert EXECUTIVE_ACRONYMS right after Abstract
abstract_pattern = r"(## Abstract\n\n.*?\n\n---)"
if re.search(abstract_pattern, text, re.DOTALL):
    text = re.sub(abstract_pattern, r"\1" + EXECUTIVE_ACRONYMS, text, count=1, flags=re.DOTALL)
    print("Inserted Executive Acronyms after Abstract!")
else:
    print("Could not find Abstract pattern!")

# Insert Chapter 10 Glossary right before References
if "## Chapter 10: References" in text:
    text = text.replace("## Chapter 10: References", FULL_GLOSSARY + "\n## Chapter 11: References")
    print("Inserted Chapter 10 Glossary and renumbered References to Chapter 11!")
elif "## Chapter 11: References" in text:
    # Already renumbered or updated
    print("Chapter 11: References already present. Updating Glossary...")
    parts = text.split("## Chapter 10: Comprehensive Glossary")
    if len(parts) > 1:
        before = parts[0]
        after = parts[1].split("## Chapter 11: References")[1]
        text = before + FULL_GLOSSARY.strip() + "\n\n## Chapter 11: References" + after
    else:
        text = text.replace("## Chapter 11: References", FULL_GLOSSARY + "\n## Chapter 11: References")
else:
    print("Could not find References chapter!")

REPORT_PATH.write_text(text, encoding="utf-8")
print("Report successfully updated with comprehensive glossary!")
