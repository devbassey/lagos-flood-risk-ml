from pathlib import Path
import shutil

# 1. Copy image to brain directory
src_img = Path('outputs/figures/01_documentary_flooding_evidence_lagos.png')
dst_img = Path(r'C:\Users\LENOVO\.gemini\antigravity\brain\dbbda659-ab1c-425a-952f-42069ce27ace\01_documentary_flooding_evidence_lagos.png')
shutil.copy2(src_img, dst_img)
print('Copied photographic plate to brain directory!')

# 2. Update build_native_docx.py to support jpg and jpeg in content-types
docx_script = Path(r'C:\Users\LENOVO\.gemini\antigravity\brain\dbbda659-ab1c-425a-952f-42069ce27ace\scratch\build_native_docx.py')
code = docx_script.read_text(encoding='utf-8')
if 'Extension="jpg"' not in code:
    code = code.replace(
        '<Default Extension="png" ContentType="image/png"/>',
        '<Default Extension="png" ContentType="image/png"/>\n  <Default Extension="jpg" ContentType="image/jpeg"/>\n  <Default Extension="jpeg" ContentType="image/jpeg"/>'
    )
    docx_script.write_text(code, encoding='utf-8')
    print('build_native_docx.py updated with jpg/jpeg OpenXML support!')

# 3. Insert Figure 1.1 into outputs/Final_Project_Report.md
report_path = Path('outputs/Final_Project_Report.md')
report_text = report_path.read_text(encoding='utf-8')

fig_1_1_block = """![Figure 1.1: Ground-Truth Documentary Evidence of Urban Flooding Hazards Across Lagos State](figures/01_documentary_flooding_evidence_lagos.png)

**Detailed Interpretation & Key Findings from Figure 1.1:**
Photographic documentation from verified field archives and institutional sources illustrating the multi-dimensional physical flood mechanisms across metropolitan Lagos:
- **Panel A (Pluvial Flash Flooding in Lekki Residential Corridor - Eti-Osa LGA):** Severe compound inundation along the low-lying Lekki-Epe axis following an intense convective cloudburst in July 2024. Despite upscale real-estate development, pervasive sand-filling of coastal lagoons and paving over natural detention wetlands creates acute surface runoff with nowhere to drain by gravity during high tides. [Source: Field Documentary Record, July 2024]
- **Panel B (Critical Transport Arterial Inundation & Economic Paralysis - Lagos Mainland):** Major municipal transit corridor submerged under bumper-height stormwater during the wet season. High impervious surface cover (>90% asphalt and concrete) converts over 90% of incident rainfall into immediate street runoff, stranding commuters and causing severe commercial paralysis across mainland transit arteries. [Source: Wiki Loves Africa Urban Environmental Archives, 2023]
- **Panel C (Astronomical High-Tide & Coastal Backwater Inundation - Lagos Lagoon Waterfront):** Waterfront community submerged during astronomical syzygy high tide. In coastal zones sitting below 2 m elevation, ocean and lagoon tides rise higher than street storm drains, forcing saline water backwards through outfalls and flooding habitable terrain even in the absence of rain. [Source: Coastal Field Archives, 2010]
- **Panel D (Primary Stormwater Collector Obstruction & Solid Waste Siltation):** Drainage canal severely blocked by solid waste, plastic bottles, and sediment. Urban drainage infrastructure in Lagos frequently loses 60–90% of design conveyance capacity due to illegal refuse dumping and deferred maintenance, converting moderate rain events into severe local disasters. [Source: Urban Environmental Sanitation Archives, 2023]
- **Panel E (Emergency Municipal Drainage Maintenance - Lagos State MEWR):** Emergency response crews from the Lagos State Ministry of the Environment and Water Resources (MEWR) manually desilting and dredging secondary drainage channels to restore hydraulic conveyance during peak rainy season. [Source: Lagos State MEWR, 2023]
- **Panel F (Peri-Urban Wetland Settlement Inundation - Iba Town, Ojo LGA):** Residential inundation in a rapidly expanding peri-urban community in Ojo LGA. Rapid demographic growth in peripheral LGAs forces low-income residents into unpaved, flood-prone marshlands lacking tertiary drainage infrastructure. [Source: Community Vulnerability Documentation, 2023]

---
"""

target_pos = "3. **Coastal & Tidal Backwater Locking**: Storm surges and rising Atlantic and lagoon water levels submerge low-lying coastal zones (**Lagos Island**, **Eti-Osa**, **Apapa**, **Ajeromi/Ifelodun**, **Amuwo Odofin**, **Ojo**, **Badagry**, **Ibeju-Lekki**) and create hydraulic \"backwater locking,\" where high lagoon tailwater prevents terrestrial storm drains from discharging by gravity.\n\n"

if target_pos in report_text and "Figure 1.1:" not in report_text:
    report_text = report_text.replace(target_pos, target_pos + fig_1_1_block + "\n")
    report_path.write_text(report_text, encoding='utf-8')
    print('Inserted Figure 1.1 into outputs/Final_Project_Report.md!')
else:
    print('Target position not found or Figure 1.1 already present.')
