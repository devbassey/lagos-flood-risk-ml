from pathlib import Path
import shutil, re

# 1. Copy figures to brain directory
brain_dir = Path(r"C:\Users\LENOVO\.gemini\antigravity\brain\dbbda659-ab1c-425a-952f-42069ce27ace")

fig_00 = Path("outputs/figures/00_lagos_administrative_reference_map.png")
fig_02 = Path("outputs/figures/02_socioeconomic_and_infrastructure_impacts_lagos.png")

if fig_00.exists():
    shutil.copy2(fig_00, brain_dir / fig_00.name)
    print(f"Copied {fig_00.name} to brain!")

if fig_02.exists():
    shutil.copy2(fig_02, brain_dir / fig_02.name)
    print(f"Copied {fig_02.name} to brain!")

# 2. Update outputs/Final_Project_Report.md
report_path = Path("outputs/Final_Project_Report.md")
text = report_path.read_text(encoding="utf-8")

# Prepare blocks for Figure 1.1, Figure 1.2, Figure 1.3
fig_1_1_map_block = """![Figure 1.1: Administrative Reference Map of Lagos State: 20 Local Government Areas (LGAs) and Geomorphic Flood Risk Zones](figures/00_lagos_administrative_reference_map.png)

**Detailed Interpretation & Key Findings from Figure 1.1:**
An administrative and geographic reference map of Lagos State establishing the spatial units of analysis used across all machine learning models, hazard choropleths, and climate projections:
- **Spatial Coverage & Geography:** Depicts all 20 official Local Government Areas (LGAs) derived from GADM v4.1 Level-2 administrative geometries, spanning 3,577 km² along 180 km of Atlantic coastline (Bight of Benin / Gulf of Guinea). Surrounding marine and estuarine water bodies—including the Atlantic Ocean to the south, the expansive 400+ km² Lagos Lagoon in the center, Lekki Lagoon to the east, and Badagry Creek to the west—define the natural boundary conditions for urban drainage.
- **Four Operational Geomorphic & Hazard Zones:**
  - **Coastal Barrier & Island Zone (Sky Blue - 4 LGAs: Eti-Osa, Lagos Island, Apapa, Ibeju-Lekki):** Characterized by low mean elevations (<6 m) and sand barrier spits bounded between the Atlantic Ocean and coastal lagoons. These LGAs face severe compound flood hazards from astronomical high tides, meteorological storm surges, and direct sea-level rise backwater locking.
  - **Tidal Estuarine & Lower Riverine Zone (Emerald Green - 3 LGAs: Kosofe, Ikorodu, Epe):** Situated along the margins of the Lagos and Lekki Lagoons and the lower Ogun River floodplain. Flood events are heavily driven by upstream river discharge from Oyo and Ogun States, water releases from Oyan Dam, and multi-week wetland soil saturation.
  - **Central Mainland Urban Catchments (Coral Red - 9 LGAs: Surulere, Mainland, Mushin, Shomolu, Ikeja, Agege, Oshodi/Isolo, Ifako/Ijaye, Ajeromi/Ifelodun):** High-density urban centers characterized by extreme impervious built-up surface cover (81% to 98% asphalt, concrete, and roofing). Pluvial flash flooding occurs within minutes of intense convective cloudbursts due to zero infiltration capacity and overloaded secondary gutters.
  - **Western Peri-Urban Growth Corridor (Amber - 4 LGAs: Alimosho, Amuwo Odofin, Ojo, Badagry):** Rapidly expanding peripheral settlements experiencing massive population influx. Paving over natural freshwater swamps and sand-filling wetland retention basins creates acute flash and waterlogging hazards in formerly rural corridors.
- **Urban Core Reference Key (Numbered Circular Pins ① to ⑫):** To preserve map legibility and prevent text collision across the congested mainland core, numbered circular badges pin each municipality: `[1] Agege (98% paved, 42 m elev)`, `[2] Ifako/Ijaye (94% paved, 49 m)`, `[3] Ikeja (88% paved, 35 m)`, `[4] Oshodi/Isolo (81% paved, 23 m)`, `[5] Mushin (96% paved, 24 m)`, `[6] Shomolu (95% paved, 14 m)`, `[7] Surulere (97% paved, 9 m)`, `[8] Mainland (90% paved, 9 m)`, `[9] Ajeromi/Ifelodun (95% paved, 5 m)`, `[10] Apapa (73% paved, 5 m)`, `[11] Lagos Island (47% paved, 6 m)`, and `[12] Kosofe (55% paved, 11 m)`.

---
"""

# Replace existing Figure 1.1 photographic plate with Figure 1.2, and add Figure 1.3
# First, remove old Figure 1.1 block if present
old_fig_pattern = r"!\[Figure 1\.1: Ground-Truth Documentary Evidence.*?---\n"
text = re.sub(old_fig_pattern, "", text, flags=re.DOTALL)

# Now construct the comprehensive three-figure introductory suite
intro_figures_suite = fig_1_1_map_block + """![Figure 1.2: Ground-Truth Documentary Evidence of Urban Flooding Mechanisms Across Lagos State](figures/01_documentary_flooding_evidence_lagos.png)

**Detailed Interpretation & Key Findings from Figure 1.2:**
Photographic documentation from verified field archives and institutional sources illustrating the multi-dimensional physical flood mechanisms operating across metropolitan Lagos:
- **Panel A (Pluvial Flash Flooding in Lekki Residential Corridor - Eti-Osa LGA):** Severe compound inundation along the low-lying Lekki-Epe axis following an intense convective cloudburst in July 2024. Despite upscale real-estate development, pervasive sand-filling of coastal lagoons and paving over natural detention wetlands creates acute surface runoff with nowhere to drain by gravity during high tides. [Source: Field Documentary Record, July 2024]
- **Panel B (Critical Transport Arterial Inundation & Economic Paralysis - Lagos Mainland):** Major municipal transit corridor submerged under bumper-height stormwater during the wet season. High impervious surface cover (>90% asphalt and concrete) converts over 90% of incident rainfall into immediate street runoff, stranding commuters and causing severe commercial paralysis across mainland transit arteries. [Source: Wiki Loves Africa Urban Environmental Archives, 2023]
- **Panel C (Astronomical High-Tide & Coastal Backwater Inundation - Lagos Lagoon Waterfront):** Waterfront community submerged during astronomical syzygy high tide. In coastal zones sitting below 2 m elevation, ocean and lagoon tides rise higher than street storm drains, forcing saline water backwards through outfalls and flooding habitable terrain even in the absence of rain. [Source: Coastal Field Archives, 2010]
- **Panel D (Primary Stormwater Collector Obstruction & Solid Waste Siltation):** Drainage canal severely blocked by solid waste, plastic bottles, and sediment. Urban drainage infrastructure in Lagos frequently loses 60–90% of design conveyance capacity due to illegal refuse dumping and deferred maintenance, converting moderate rain events into severe local disasters. [Source: Urban Environmental Sanitation Archives, 2023]
- **Panel E (Emergency Municipal Drainage Maintenance - Lagos State MEWR):** Emergency response crews from the Lagos State Ministry of the Environment and Water Resources (MEWR) manually desilting and dredging secondary drainage channels to restore hydraulic conveyance during peak rainy season. [Source: Lagos State MEWR, 2023]
- **Panel F (Peri-Urban Wetland Settlement Inundation - Iba Town, Ojo LGA):** Residential inundation in a rapidly expanding peri-urban community in Ojo LGA. Rapid demographic growth in peripheral LGAs forces low-income residents into unpaved, flood-prone marshlands lacking tertiary drainage infrastructure. [Source: Community Vulnerability Documentation, 2023]

---

![Figure 1.3: Socio-Economic, Transport Paralysis and Infrastructure Impacts of Recurrent Lagos Floods](figures/02_socioeconomic_and_infrastructure_impacts_lagos.png)

**Detailed Interpretation & Key Findings from Figure 1.3:**
Photographic documentation from verified ground surveys demonstrating the severe human, vehicular, and environmental impacts of recurrent flooding across Lagos State:
- **Panel A (Vehicular Inundation & Engine Hydro-Locking on Arterial Roads):** Commuter vehicle completely stalled and abandoned in deep floodwaters along a major metropolitan transit route following an afternoon cloudburst. Flood depths exceeding 40 cm enter vehicular exhaust systems and air intakes, causing widespread engine hydro-locking, electrical short circuits, and multi-hour traffic gridlock across metropolitan bridges. [Source: Urban Environmental Documentation, April 2023]
- **Panel B (Deep Residential Street Submergence during Peak June Monsoon):** Residential access corridor submerged under waist-high stormwater. The complete submergence of road curbs, pedestrian sidewalks, and perimeter fencing cuts off neighborhood access, isolates homes, and forces residents to wade through contaminated waters carrying microbial pathogens and vector-borne disease risks. [Source: Field Documentary Archive, June 2019]
- **Panel C (Compound Waterlogging in Lekki Coastal Estates - Eti-Osa LGA):** Prolonged flood pooling within private compounds and access streets in Lekki Phase 1 during July 2024. Because coastal groundwater tables lie within 0.5 metres of the surface and tidal gates remain locked, floodwaters persist for 48 to 72 hours following storm cessation, causing severe structural degradation to residential foundations and perimeter walls. [Source: Field Documentary Record, July 2024]
- **Panel D (Absence of Engineered Drainage Channels in Dense Unpaved Settlements):** Unpaved residential street in an informal mainland settlement where the total absence of engineered concrete gutters forces surface runoff to pool into massive stagnant lagoons, breeding mosquitoes and blocking emergency vehicular ingress. [Source: Local Infrastructure Vulnerability Survey, July 2023]
- **Panel E (Coastal Wetland Sponge Function - Lekki Conservation Reserve):** Surviving natural mangrove wetland and swamp forest in the Lekki Conservation Reserve absorbing millions of litres of stormwater overflow. This natural retention basin attenuates peak storm runoff volumes and buffers surrounding urban developments, illustrating why protecting remaining coastal wetlands is vastly cheaper than constructing concrete sea walls. [Source: Ecological Field Survey, Eti-Osa Wetland Reserve, 2023]
- **Panel F (Peri-Urban Commercial Feeder Road Degradation - Mazamaza / Amuwo Odofin):** Major commercial feeder road connecting the Badagry International Expressway and Mazamaza markets heavily eroded and submerged by stormwater. Persistent seasonal flooding rapidly disintegrates road asphalt into deep gullies, paralyzing cross-border logistics and market commerce. [Source: Commercial Corridor Infrastructure Record, 2019]

---
"""

# Insert the three-figure suite right after Section 1.1 description of the 3 physical mechanisms
insertion_marker = '3. **Coastal & Tidal Backwater Locking**: Storm surges and rising Atlantic and lagoon water levels submerge low-lying coastal zones (**Lagos Island**, **Eti-Osa**, **Apapa**, **Ajeromi/Ifelodun**, **Amuwo Odofin**, **Ojo**, **Badagry**, **Ibeju-Lekki**) and create hydraulic "backwater locking," where high lagoon tailwater prevents terrestrial storm drains from discharging by gravity.\n\n'

if insertion_marker in text:
    text = text.replace(insertion_marker, insertion_marker + intro_figures_suite + "\n")
    report_path.write_text(text, encoding="utf-8")
    print("outputs/Final_Project_Report.md successfully updated with Figures 1.1, 1.2, and 1.3!")
else:
    print("Insertion marker not found!")
