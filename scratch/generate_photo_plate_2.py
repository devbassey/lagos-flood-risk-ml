import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path

pdir = Path('outputs/figures/photos')
fig, axes = plt.subplots(2, 3, figsize=(18, 11), dpi=300)

panels = [
    ('photo_08_broken_down_car_flood.jpg', '(A) Vehicular Inundation & Engine Hydro-Locking\nMajor Roadway Storm Inundation: Commuter Breakdown & Transit Paralysis\n[Source: Urban Environmental Documentation, 2023]'),
    ('photo_07_street_flood_deep.jpg', '(B) Deep Residential Street Submergence (Peak June Monsoon)\nPluvial Cloudburst Runoff: Complete Loss of Sidewalk & Roadway Access\n[Source: Field Documentary Archive, June 2019]'),
    ('photo_09_lekki_flooding_residential_2024.jpg', '(C) Compound Waterlogging in Lekki Coastal Estates (Eti-Osa LGA)\nTidal Locking & Paved Runoff: Prolonged Compound Inundation (July 2024)\n[Source: Field Documentary Record, July 2024]'),
    ('photo_10_no_proper_drainage_unpaved.jpg', '(D) Absence of Engineered Drainage Channels in Dense Settlement\nUnpaved Neighborhood: Stormwater Stagnation Creating Health Hazards\n[Source: Local Infrastructure Vulnerability Survey, 2023]'),
    ('photo_11_swamp_lekki_conservation.jpg', '(E) Coastal Wetland Sponge Function (Lekki Conservation Reserve)\nNatural Retention: Mangrove & Swamp Buffer Absorbing Surge Volumes\n[Source: Ecological Field Survey, Eti-Osa Wetland Reserve, 2023]'),
    ('photo_12_feeder_road_mazamaza.jpg', '(F) Peri-Urban Arterial Feeder Road Inundation (Mazamaza / Amuwo Odofin)\nTransport Corridor Degradation: Heavy Waterlogging Halting Commerce\n[Source: Commercial Corridor Infrastructure Record, 2019]')
]

for ax, (fname, title) in zip(axes.flat, panels):
    img = Image.open(pdir / fname)
    # Convert RGBA/P to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')
    ax.imshow(img)
    ax.set_title(title, fontsize=10, fontweight='bold', pad=8, color='#0F172A', linespacing=1.2)
    ax.axis('off')

plt.suptitle('Socio-Economic, Transport Paralysis and Infrastructure Impacts of Recurrent Lagos Floods\nPhotographic documentation of commuter vehicular stalls, residential compound waterlogging, drainage deficits, and natural wetland sponge buffers.',
             fontsize=14, fontweight='bold', color='#1E3A8A', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.94])

out_path = Path('outputs/figures/02_socioeconomic_and_infrastructure_impacts_lagos.png')
plt.savefig(out_path, dpi=300, bbox_inches='tight')

# Optimize size
with Image.open(out_path) as img:
    if img.size[0] > 3000:
        new_w = 3000
        new_h = int(img.size[1] * (3000 / img.size[0]))
        img_res = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        img_res.save(out_path, 'PNG', optimize=True)

print(f'Saved and optimized Plate 2: {out_path} ({out_path.stat().st_size / 1024:.1f} KB)')
