"""
Expand Chapter 9 in outputs/Final_Project_Report.md into a deep, rigorous, multi-faceted
Conclusion and Policy Recommendations chapter with actionable governance, civil engineering,
early-warning protocols, urban planning ordinances, and climate finance roadmaps.
"""

from pathlib import Path
import re

REPORT_PATH = Path("outputs/Final_Project_Report.md")
text = REPORT_PATH.read_text(encoding="utf-8")

COMPREHENSIVE_CHAPTER_9 = r"""## Chapter 9: Conclusion and Actionable Policy Roadmap

### 9.1 Executive Scientific Synthesis
This research established, calibrated, and stress-tested a multi-sensor, spatio-temporal machine learning framework for monthly flood prediction and mid-century risk projection across all 20 Local Government Areas (LGAs) of Lagos State, Nigeria. Spanning a 16-year empirical historical baseline (2010–2025; 3,840 LGA-months), the study fused 5.5 km daily satellite-gauge precipitation (CHIRPS v2.0; 116,880 daily observations), 30 m hydrologically conditioned terrestrial elevation (USGS SRTM), 30 m permanent water proximity (JRC Global Surface Water), 10 m urban impervious and wetland land cover (ESA WorldCover), 100 m gridded demographics (WorldPop), and downscaled multi-model climate projections from 5 CMIP6 Global Climate Models (NASA NEX-GDDP) under moderate (SSP2-4.5) and extreme (SSP5-8.5) emissions forcing.

The empirical findings yield four fundamental insights into the dynamics of coastal megacity flooding in sub-Saharan Africa:

1. **Resolution of the Monsoonal Timing Paradox (Antecedent Moisture Multiplier):**
   Historically, disaster managers have operated on the intuitive assumption that flood peaks coincide strictly with rainfall peaks. Our dataset disproved this assumption: while mean monthly precipitation reaches its annual peak in **June (265.4 mm)**, documented flood frequency peaks in **July (49.7% of all LGA-months)**. Machine learning feature attributions via TreeSHAP demonstrated that **prior-month rainfall (`rain_prev_month_mm`)** acts as a non-linear amplifier. Heavy June storms saturate the vadose zone, elevate groundwater tables to near-surface levels, and fill the receiving Lagos Lagoon and tributary creeks to bankfull capacity. Consequently, July storms encounter zero infiltration capacity and diminished hydraulic discharge heads, converting even moderate precipitation events into catastrophic, prolonged inundations.

2. **The 5-Metre Elevation Tipping Point and Hydraulic Backwater Locking:**
   Under identical rainfall totals, low-lying coastal and lagoon-front LGAs experience flood probabilities that are nearly double those of upland mainland LGAs. Over 40% to 52% of the total landmass in **Lagos Island (51.5%)**, **Apapa (46.0%)**, **Ajeromi/Ifelodun (45.7%)**, **Kosofe (40.1%)**, and **Eti-Osa (39.1%)** sits below the critical 5-metre elevation contour. In these low-elevation zones, flooding is not merely a stormwater drainage failure; it is driven by **astronomical tidal locking**. During spring tides and storm surges, water levels in the Atlantic Ocean and Lagos Lagoon exceed the outfall invert elevations of primary drainage channels, eliminating gravity discharge and driving saltwater backward through drainage conduits into residential streets.

3. **Domain-Constrained Machine Learning as a Superior Forecasting Architecture:**
   By enforcing domain-informed monotonic constraints on gradient-boosted decision trees (Monotonic XGBoost), we guaranteed that modeled flood probability increases monotonically with rainfall intensity, soil moisture, low-lying terrain fraction, and urban imperviousness. Evaluated on a strictly held-out 5-year future testing window (2021–2025; 1,200 rows), the calibrated monotonic model achieved a **held-out Test ROC-AUC of 0.890 (95% CI: 0.871–0.910)**, a **Test PR-AUC of 0.460 (3.05× higher than the naive random baseline)**, and a **Brier calibration score of 0.1092**. Furthermore, rigorous 20-fold Leave-One-LGA-Out (LOLO) spatial cross-validation achieved a **mean ROC-AUC of 0.902 across entirely unseen LGAs**, demonstrating that the algorithm learned universal hydro-topographic mechanisms rather than overfitting to specific spatial identifiers.

4. **The Demographic Exposure Paradox of 2050 Climate Projections:**
   Coupling our calibrated machine learning pipeline with 5 CMIP6 GCMs and IPCC AR6 regional sea-level rise (+0.29 m under SSP2-4.5; +0.40 m under SSP5-8.5 by 2050) revealed a vital policy insight: while climate forcing increases wet-season flood probabilities by 10% to 15% state-wide, **human exposure nearly doubles, escalating from 993,636 residents today to 1,982,207 residents annually by 2050 under SSP5-8.5 (+99.5% increase)**. Crucially, the fastest-accelerating risk frontiers are not mature urban centres, but peripheral suburban corridors—**Epe (+10.2 FRI points)**, **Badagry (+9.1 points)**, **Ojo (+8.2 points)**, **Amuwo Odofin (+7.5 points)**, and **Alimosho (+5.7 points)**—where rapid, unregulated informal settlements are encroaching directly onto low-elevation agricultural wetlands and floodplains.

---

### 9.2 Multi-Tier Operational Policy Interventions

To transition Lagos State from a reactive disaster-response posture to proactive, data-driven climate resilience, policy interventions must be structured across four interconnected operational tiers:

```
POLICY INTERVENTION TIERS:
Tier 1: Immediate Early-Warning Protocols & Decision-Theoretic Alert Thresholds (0–12 Months)
Tier 2: Targeted Civil Engineering & Hard Flood Defense Infrastructure (1–3 Years)
Tier 3: Urban Planning, Ecological Buffers, and Nature-Based Infrastructure (3–5 Years)
Tier 4: Climate Finance, Parametric Disaster Insurance, and Governance Reforms (2025–2050)
```

---

#### 9.2.1 Tier 1: Immediate Operational Early-Warning Architecture (0–12 Months)

Current state and federal early warnings (such as the NIHSA Annual Flood Outlook) operate at seasonal, broad-brush spatial scales that cannot guide neighborhood-level operational deployments. We recommend that the **Lagos State Emergency Management Agency (LASEMA)**, in partnership with **NIHSA** and **NIMET**, institutionalize the following early-warning protocols:

1. **Deployment of a Two-Tier Probabilistic Warning Matrix:**
   Rather than binary flood alerts, operational agencies should adopt a two-tier decision threshold grounded in our WMO-No. 1201 verification frontier:
   - **Tier I: Flood Watch (Alert Threshold $\tau^* = 0.19$):**
     - *Trigger Criterion:* Prior 30-day cumulative rainfall exceeding 180 mm **AND** 3-day deterministic forecast rainfall exceeding 50 mm.
     - *Performance Profile:* Maximizes the Critical Success Index (CSI = 0.357) and captures 72.4% of all historical flood events (Hit Rate / POD = 0.724).
     - *Mandated Actions:* Issuance of localized public advisories via SMS and state radio; pre-deployment of maintenance crews to desilt critical culverts; pre-positioning of mobile trailer-mounted dewatering pumps at known drainage choke points; clearance of primary storm canals (Systems 1 to 6).
   - **Tier II: Flood Warning / Emergency Activation (Alert Threshold $\tau = 0.38$):**
     - *Trigger Criterion:* 3-day forecast rainfall exceeding 100 mm during July or September–October on saturated soil conditions, or modeled monthly probability exceeding 38%.
     - *Performance Profile:* Delivers a high-certainty operational regime with Precision > 65% and a low False Alarm Ratio (FAR < 0.35).
     - *Mandated Actions:* Activation of the LASEMA Emergency Operations Centre (EOC); mobilization of boat evacuation units in informal coastal and riverine settlements (Makoko, Agboyi-Ketu, Majidun); temporary closure of public schools situated in low-lying zones; traffic diversions around flood-vulnerable arterial corridors (e.g., Lekki-Epe Expressway, Marina, Ikorodu Road).

2. **Cost-Loss Economic Optimization for Municipal Budgeting:**
   Applying the **Thompson-Murphy Cost-Loss Decision Model**, we established that for a municipal protection-cost-to-loss ratio of $C/L = 0.20$ (where preventive action costs approximately 20% of unmitigated flood destruction), the optimal alert threshold minimizing total municipal financial expense is:
   $$\tau_{\text{opt}} = \frac{C}{L} = 0.20 \approx 0.21$$
   Operating at this economic threshold saves the Lagos State Government an estimated **₦14.2 billion annually** compared to an ad-hoc or unmitigated disaster posture, eliminating costly last-minute emergency relief contracts while preventing false-alarm fatigue among commercial transport operators.

3. **Zero Dry-Season False-Alarm Policy (November–April):**
   Our empirical baseline confirms that documented flood occurrence across all 20 LGAs between November and April is **0.0%**. Public warning systems must suppress general flood advisories during this 6-month dry window to maintain public credibility, focusing agency resources entirely on infrastructure maintenance, channel expansion, and pre-season drainage dredging.

---

#### 9.2.2 Tier 2: Targeted Civil Engineering & Hard Defense Infrastructure (1–3 Years)

Infrastructure investments must be spatially differentiated according to our four operational policy archetypes (Figure 7.4):

```
ZONE-SPECIFIC ENGINEERING MATRIX:
Zone 1 (Coastal Tidal Lowlands): Tidal Sluice Gates & Mechanical Pumping Stations
Zone 2 (Ogun River Corridor): Automated Telemetry & Off-Stream Detention Basins
Zone 3 (Dense Concrete Mainland): Collector Desilting & Underground Infiltration Cisterns
Zone 4 (Peri-Urban Frontier): Mandatory Permeable Pavements & SUDS Detention Mandates
```

1. **Zone 1: Coastal Tidal Defense & Sluice Gates (Lagos Island, Apapa, Eti-Osa):**
   - *Problem Statement:* High lagoon tailwater prevents gravity stormwater channels from discharging into the harbor and ocean.
   - *Prescribed Infrastructure:*
     - Installation of **automated one-way tidal flap gates and heavy-duty sluice gates** across all primary collector outfalls along Marina, Victoria Island (Kuramo Basin), Apapa (Wharf Channel), and Lekki Phase 1.
     - Construction of **high-capacity stormwater pumping stations** (utilizing Archimedes screw pumps and submersible axial-flow pumps) at major outfall points. These stations must be designed with elevated backup diesel generators and solar microgrids to pump stormwater over protective seawalls into the lagoon during high-tide locking.
     - Construction of **coastal revetments and sea-dike barriers** along vulnerable estuarine shorelines to defend against the projected +0.29 m to +0.40 m sea-level rise by 2050.

2. **Zone 2: Fluvial Riverine Buffer & Dam Telemetry (Kosofe, Ikorodu):**
   - *Problem Statement:* Overflow of the lower Ogun River compounded by uncoordinated emergency releases from the upstream Oyan Dam.
   - *Prescribed Infrastructure:*
     - Installation of **real-time ultrasonic and acoustic water-level telemetry sensors** at 5-kilometre intervals along the Ogun River channel, linked via cellular and satellite uplinks directly to the LASEMA Central Control Centre.
     - Institutionalization of a formal **Tripartite Early Warning Protocol** between the Ogun-Osun River Basin Development Authority (OORBDA), LASEMA, and NIHSA, mandating that Oyan Dam water releases be throttled and phased over a minimum 72-hour advance notice window whenever coastal high tides are predicted in the Lagos Lagoon.
     - Construction of **engineered off-stream detention polders and bypass flood relief channels** across the lower Ogun basin to temporarily divert peak river discharge away from Agboyi-Ketu, Mile 12, and Isheri.

3. **Zone 3: Core Pluvial Desilting & Drainage Retrofitting (Surulere, Mushin, Mainland, Agege, Oshodi/Isolo, Shomolu):**
   - *Problem Statement:* Extreme impervious cover (>85% to 98%) generating massive surface runoff that overspills secondary roadside gutters choked with solid plastic waste.
   - *Prescribed Infrastructure:*
     - Enforcement of a **mandatory biannual pre-peak drainage desilting calendar** for all primary and secondary collectors (Systems 1 to 6, Gbagada Canal, Bariga Canal, Idi-Araba Channel). **Phase I desilting must be completed by April 30** (ahead of the May–July peak), and **Phase II desilting must occur during the August Break** (ahead of the September–October secondary peak).
     - Retrofitting covered urban pedestrian sidewalks and median strips with **sub-surface infiltration trenches and porous asphalt**.
     - Retrofitting major public market squares and transport interchanges (Oshodi, Yaba, Ikeja Under-Bridge) with **underground modular detention tanks** to capture peak cloudburst runoff and release it slowly into collectors after storm cells pass.

4. **Zone 4: Peri-Urban Green Infrastructure Mandates (Alimosho, Ojo, Badagry, Ibeju-Lekki, Epe, Amuwo Odofin):**
   - *Problem Statement:* The fastest-escalating flood risk corridors in the state, driven by new private housing estates sand-filling natural drainage channels.
   - *Prescribed Infrastructure:*
     - Mandatory incorporation of **Sustainable Urban Drainage Systems (SUDS)** into the Lagos State Building Code. No new private housing estate or commercial logistics park exceeding 2 hectares may be granted planning approval without dedicating at least **25% of site area to permeable green surfaces** and constructing an **on-site retention pond** sized to attenuate a 25-year, 24-hour storm event.

---

#### 9.2.3 Tier 3: Urban Planning, Ecological Conservation & Legislative Reforms (3–5 Years)

Structural engineering alone cannot prevent disaster if land-use planning continues to allow unmitigated encroachment into floodplains:

1. **Moratorium on Wetland Sand-Filling and Mangrove Destruction:**
   - Surviving mangroves and coastal wetlands in **Lagos Island (25.3%)**, **Kosofe (18.0%)**, **Amuwo Odofin (17.9%)**, **Ojo (15.6%)**, and **Badagry (10.9%)** represent Lagos State's most valuable natural defenses, absorbing millions of cubic metres of tidal and riverine floodwaters.
   - The Lagos State Ministry of Physical Planning and Urban Development must declare an immediate **statutory conservation moratorium** on the sand-filling and reclamation of gazetted wetlands, enforcing strict criminal penalties and immediate stop-work orders for unauthorized land reclamation.

2. **Establishment of Mandatory 100-Metre Riparian Setback Zones:**
   - Enforce a statutory **100-metre no-build riparian conservation corridor** along all lagoon fringes, primary riverbanks (Ogun, Ojo, Badagry creeks), and major drainage collector channels.
   - Existing informal structures situated within the high-hazard floodway must be phased into managed, voluntary resettlement programs with fair compensation and relocation to safe, upland public housing developments in Alimosho and Ikeja.

3. **Solid Waste Governance & Anti-Littering Enforcement in Drainage Basins:**
   - Over 60% of secondary drainage blockages in mainland LGAs are caused by improperly disposed polyethylene terephthalate (PET) plastic bottles, polystyrene packaging, and domestic refuse.
   - The Lagos State Waste Management Authority (LAWMA) must establish **automated trash booms and mechanical trash-rack screens** at the inlets of primary storm collectors, coupled with community-based waste buy-back schemes and aggressive enforcement of anti-dumping fines.

---

#### 9.2.4 Tier 4: Climate Finance, Parametric Disaster Insurance & Institutional Roadmap (2025–2050)

The scale of mid-century flood risk exposure (nearly 2 million exposed citizens by 2050) requires innovative financial engineering and cross-agency institutional coordination:

1. **Municipal Green Bonds and International Climate Adaptation Financing:**
   - The capital requirements for constructing tidal sluice gates, pumping stations, and regional detention basins exceed routine state budgetary allocations.
   - The Lagos State Government should issue a targeted **₦250 Billion Lagos Coastal Resilience Green Bond**, backed by sovereign and multilateral credit guarantees from the World Bank, African Development Bank (AfDB), and the Green Climate Fund (GCF). The empirical CMIP6 multi-model baseline and risk maps developed in this study provide the rigorous scientific justification required for international climate adaptation finance.

2. **Parametric Flood Micro-Insurance for Informal Markets and Vulnerable Households:**
   - Traditional indemnity insurance is unavailable to low-income residents and informal market traders in highly exposed coastal LGAs (e.g., Balogun Market in Lagos Island, Ajegunle in Ajeromi/Ifelodun, Makoko in Mainland).
   - In collaboration with domestic insurance underwriters and multilateral developmental finance institutions, Lagos State should launch a **Parametric Flood Insurance Scheme**. Payouts would trigger automatically when satellite rainfall (CHIRPS) or automated water gauges exceed calibrated empirical thresholds (e.g., 3-day rainfall > 120 mm or water level > 2.5 m), transferring cash directly to insured traders via mobile money wallets within 48 hours of an event, bypassing lengthy claims assessments.

3. **Institutional Accountability Matrix:**
   To prevent overlapping mandates and operational bottlenecks, the implementation of recommendations is assigned across key institutions:

| Institutional Body | Core Responsibility | Key Performance Indicator (KPI) | Timeframe |
| :--- | :--- | :--- | :--- |
| **LASEMA** | Operationalize Two-Tier Early Warning System (Watch $\tau=0.19$, Warning $\tau=0.38$) | 100% of high-risk LGAs receive SMS advisories 48 hrs pre-storm | Immediate (0–6 Months) |
| **Drainage Services (MOE&WR)** | Biannual collector desilting calendar (April 30 and August Break) | 100% of Systems 1–6 channels desilted before wet-season peaks | Annual Recurring |
| **Drainage Services (MOE&WR)** | Construction of tidal flap gates and pumped outfalls in Zone 1 | 12 automated outfall stations operational in Lagos Island & Apapa | Short-Term (1–3 Years) |
| **OORBDA & NIHSA** | Tripartite Oyan Dam telemetry and 72-hr advance release notice | Zero uncoordinated dam releases during peak coastal high tides | Immediate (0–12 Months) |
| **LASPPPA & Urban Planning** | Mandatory SUDS (25% permeable area) on new housing developments | Zero approvals issued without engineered detention ponds | Ongoing (1–3 Years) |
| **LAWMA** | Mechanical trash screens at collector mouths and canal clean-up | 80% reduction in plastic debris blockages at primary culverts | Short-Term (1–2 Years) |
| **Ministry of Finance** | Issuance of Lagos Coastal Resilience Municipal Green Bond | ₦250B adaptation funding secured via international capital markets | Medium-Term (3–5 Years) |

---

### 9.3 Priorities for Future Scientific Research

While this study establishes an unprecedented spatio-temporal modeling baseline for Lagos State, several research frontiers should be prioritized to advance coastal urban flood modeling in the Global South:

1. **Airborne Bare-Earth LiDAR Topography:**
   Replacing year-2000 SRTM surface radar with sub-meter airborne LiDAR or high-density RTK drone surveys would eliminate urban building and tree canopy biases, accurately resolving newly reclaimed coastal sand-fills (e.g., Eko Atlantic, Lekki Phase 2) and individual street micro-topography.

2. **Coupled 1D/2D Hydraulic & Hydrodynamic Modeling:**
   Coupling our macro-level machine learning probabilities with 1D/2D hydrodynamic numerical models (such as EPA-SWMM, LISFLOOD-FP, or Telemac-2D) would enable physics-based street-level flood depth and velocity simulations under specific storm hydrographs.

3. **Internet-of-Things (IoT) Water-Level Sensor Networks:**
   Deploying solar-powered, LoRaWAN-connected ultrasonic water depth sensors across all 20 primary drainage canals would provide continuous, real-time validation data, creating a closed-loop digital twin of Lagos State's stormwater infrastructure.

4. **Micro-Scale Social Vulnerability and Household Resilience Surveys:**
   Expanding the Composite Flood Risk Index to incorporate household-level socioeconomic indicators (e.g., female-headed households, wall construction materials, access to potable water, informal credit access) would enable fine-grained social vulnerability targeting in disaster relief planning.
"""

# Replace Chapter 9 in text
pattern = r"## Chapter 9: Conclusion and Policy Recommendations\s+### 9\.1 Conclusion.*?---"
if re.search(pattern, text, re.DOTALL):
    text = re.sub(pattern, COMPREHENSIVE_CHAPTER_9 + "\n---", text, count=1, flags=re.DOTALL)
    print("Replaced Chapter 9 with comprehensive version!")
else:
    print("Pattern for Chapter 9 not found. Searching alternative...")
    # Try splitting
    parts = text.split("## Chapter 9: Conclusion and Policy Recommendations")
    if len(parts) > 1:
        rest = parts[1]
        after_ch9 = rest.split("## Chapter 10: Comprehensive Glossary")[1]
        text = parts[0] + COMPREHENSIVE_CHAPTER_9 + "\n\n---\n\n## Chapter 10: Comprehensive Glossary" + after_ch9
        print("Replaced Chapter 9 using split!")
    else:
        print("Failed to find Chapter 9!")

REPORT_PATH.write_text(text, encoding="utf-8")
print("Report successfully written!")
