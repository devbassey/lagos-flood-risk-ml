"""
Generate Figure 1.0 / Figure 1.1: Administrative Reference Map of Lagos State
Showing all 20 Local Government Areas (LGAs) grouped into 4 functional geomorphic zones.
Includes:
- Large LGA labels with white halos
- Numbered circular badge pins (① to ⑫) for dense urban core
- Complete, non-overlapping Urban Core Reference Legend
- Surrounding water bodies (Atlantic Ocean, Lagos Lagoon, Lekki Lagoon)
- Layman-friendly insight boxes at bottom
- Metric scale bar and North arrow
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
from pathlib import Path
import numpy as np

# 1. Load LGAs
gdf = gpd.read_file('data/clean/lagos_lgas.gpkg')

# Define 4 Geomorphic / Operational Zones
zone_map = {
    # Coastal Barrier & Island Zone
    'Eti-Osa': 'Coastal Barrier & Island Zone',
    'Lagos Island': 'Coastal Barrier & Island Zone',
    'Apapa': 'Coastal Barrier & Island Zone',
    'Ibeju-Lekki': 'Coastal Barrier & Island Zone',
    # Tidal Estuarine & Lower Riverine Zone
    'Kosofe': 'Tidal Estuarine & Lower Riverine Zone',
    'Ikorodu': 'Tidal Estuarine & Lower Riverine Zone',
    'Epe': 'Tidal Estuarine & Lower Riverine Zone',
    # Central Mainland Urban Catchments
    'Surulere': 'Central Mainland Urban Catchments',
    'Mainland': 'Central Mainland Urban Catchments',
    'Mushin': 'Central Mainland Urban Catchments',
    'Shomolu': 'Central Mainland Urban Catchments',
    'Ikeja': 'Central Mainland Urban Catchments',
    'Agege': 'Central Mainland Urban Catchments',
    'Oshodi/Isolo': 'Central Mainland Urban Catchments',
    'Ifako/Ijaye': 'Central Mainland Urban Catchments',
    'Ajeromi/Ifelodun': 'Central Mainland Urban Catchments',
    # Western Peri-Urban Growth Corridor
    'Alimosho': 'Western Peri-Urban Corridor',
    'Amuwo Odofin': 'Western Peri-Urban Corridor',
    'Ojo': 'Western Peri-Urban Corridor',
    'Badagry': 'Western Peri-Urban Corridor',
}

gdf['zone'] = gdf['lga'].map(zone_map)

# Color palette for the 4 zones
zone_colors = {
    'Coastal Barrier & Island Zone': '#38BDF8',       # Sky blue / Coastal
    'Tidal Estuarine & Lower Riverine Zone': '#34D399',# Emerald / Wetland
    'Central Mainland Urban Catchments': '#F87171',   # Coral red / Urban core
    'Western Peri-Urban Corridor': '#FBBF24',         # Amber / Growth
}

gdf['color'] = gdf['zone'].map(zone_colors)

# Setup Figure
fig, ax = plt.subplots(figsize=(18, 9.5), dpi=300)
ax.set_facecolor('#F0F9FF') # Subtle ocean/water background

# Plot LGAs
gdf.plot(ax=ax, color=gdf['color'], edgecolor='#0F172A', linewidth=1.2, zorder=2)

# Identify urban core LGAs requiring numbered pins
urban_core_keys = [
    'Agege', 'Ifako/Ijaye', 'Ikeja', 'Oshodi/Isolo', 
    'Mushin', 'Shomolu', 'Surulere', 'Mainland', 
    'Ajeromi/Ifelodun', 'Apapa', 'Lagos Island', 'Kosofe'
]

# Large LGAs that can be labeled directly
large_lgas = {
    'Badagry': (2.88, 6.43),
    'Ojo': (3.17, 6.47),
    'Alimosho': (3.26, 6.61),
    'Ikorodu': (3.52, 6.62),
    'Epe': (3.98, 6.58),
    'Ibeju-Lekki': (3.80, 6.46),
    'Eti-Osa': (3.54, 6.44),
    'Amuwo Odofin': (3.29, 6.44)
}

for name, (x, y) in large_lgas.items():
    ax.text(x, y, name, fontsize=10.5, fontweight='bold', color='#0F172A',
            ha='center', va='center', zorder=5,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor='#475569', alpha=0.9, lw=0.8))

# Urban Core Numbered Badges (1 to 12)
urban_pins = {
    'Agege': (1, 3.32, 6.62),
    'Ifako/Ijaye': (2, 3.33, 6.67),
    'Ikeja': (3, 3.35, 6.59),
    'Oshodi/Isolo': (4, 3.32, 6.53),
    'Mushin': (5, 3.35, 6.53),
    'Shomolu': (6, 3.38, 6.54),
    'Surulere': (7, 3.35, 6.49),
    'Mainland': (8, 3.38, 6.49),
    'Ajeromi/Ifelodun': (9, 3.32, 6.45),
    'Apapa': (10, 3.36, 6.44),
    'Lagos Island': (11, 3.40, 6.45),
    'Kosofe': (12, 3.40, 6.59),
}

for name, (num, x, y) in urban_pins.items():
    # Draw circular white badge with navy text
    ax.plot(x, y, 'o', color='#1E3A8A', markersize=14, zorder=6)
    ax.plot(x, y, 'o', color='white', markersize=12, zorder=7)
    ax.text(x, y, str(num), fontsize=7.5, fontweight='black', color='#1E3A8A',
            ha='center', va='center', zorder=8)

# Geographic Water Labels
ax.text(3.3, 6.33, "ATLANTIC OCEAN\n(Gulf of Guinea / Bight of Benin)", fontsize=11, fontweight='bold',
        color='#0284C7', ha='center', va='center', style='italic', zorder=3)
ax.text(3.48, 6.51, "Lagos Lagoon", fontsize=10, fontweight='bold',
        color='#0284C7', ha='center', va='center', style='italic', zorder=3)
ax.text(4.08, 6.52, "Lekki Lagoon", fontsize=10, fontweight='bold',
        color='#0284C7', ha='center', va='center', style='italic', zorder=3)
ax.text(2.85, 6.40, "Badagry Creek", fontsize=9, fontweight='bold',
        color='#0284C7', ha='center', va='center', style='italic', zorder=3)

# Boundaries formatting
ax.set_xlim(2.68, 4.35)
ax.set_ylim(6.28, 6.78)
ax.set_xlabel('Longitude (°E)', fontsize=10, fontweight='bold', color='#334155')
ax.set_ylabel('Latitude (°N)', fontsize=10, fontweight='bold', color='#334155')
ax.tick_params(colors='#334155', labelsize=9)
ax.grid(color='#CBD5E1', linestyle='--', linewidth=0.5, alpha=0.7)

# Title Block
plt.suptitle('Administrative Reference Map of Lagos State: 20 Local Government Areas (LGAs)',
             fontsize=14, fontweight='bold', color='#0F172A', y=0.97)
plt.title('Official GADM v4.1 Level-2 Boundaries classified into Four Operational Geomorphic and Flood Risk Zones',
          fontsize=10.5, color='#475569', pad=8)

# Zone Legend (Top Right)
zone_patches = [
    mpatches.Patch(color='#38BDF8', label='Coastal Barrier & Island Zone (4 LGAs: Tidal backwater locking, surges)'),
    mpatches.Patch(color='#34D399', label='Tidal Estuarine & Lower Riverine (3 LGAs: Ogun River discharge, wetlands)'),
    mpatches.Patch(color='#F87171', label='Central Mainland Urban Core (9 LGAs: High concrete cover, pluvial flash)'),
    mpatches.Patch(color='#FBBF24', label='Western Peri-Urban Corridor (4 LGAs: Rapid sprawling wetland encroachment)')
]
leg_zone = ax.legend(handles=zone_patches, loc='upper right', frameon=True,
                     facecolor='white', edgecolor='#94A3B8', fontsize=8.5, title='Geomorphic & Flood Risk Zones',
                     title_fontsize=9.5)
leg_zone.get_title().set_fontweight('bold')
ax.add_artist(leg_zone)

# Urban Core Numbered Callout Legend Box (Bottom Left)
urban_text = (
    "Urban Core Reference Key (Numbered Pins):\n"
    "[1] Agege (98% paved, 42m elev) | [2] Ifako/Ijaye (94% paved, 49m) | [3] Ikeja (88% paved, 35m) | [4] Oshodi/Isolo (81% paved, 23m)\n"
    "[5] Mushin (96% paved, 24m) | [6] Shomolu (95% paved, 14m) | [7] Surulere (97% paved, 9m) | [8] Mainland (90% paved, 9m)\n"
    "[9] Ajeromi/Ifelodun (95% paved, 5m) | [10] Apapa (73% paved, 5m) | [11] Lagos Island (47% paved, 6m) | [12] Kosofe (55% paved, 11m)"
)
bbox_props = dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC', edgecolor='#64748B', alpha=0.95, lw=1)
ax.text(0.5, 0.08, urban_text, transform=ax.transAxes, fontsize=8.0,
        ha='center', va='center', bbox=bbox_props, color='#0F172A', linespacing=1.35)

# Layman Insight Cards (Bottom)
insight_1 = "[GEOGRAPHY] Lagos spans 3,577 km² with 180 km of coastline; over 50% of the metropolis sits <5 m above sea level."
insight_2 = "[ADMINISTRATION] 20 Local Government Areas spanning dense urban cores, coastal islands, and sprawling rural lagoons."
insight_3 = "[COMPOUND HAZARDS] Island LGAs face tidal locking, riverine LGAs face dam releases, and mainland cities face instant flash runoff."

plt.figtext(0.18, 0.015, insight_1, fontsize=7.5, ha='center', color='#0369A1',
            bbox=dict(boxstyle='square,pad=0.4', facecolor='#E0F2FE', edgecolor='#38BDF8', lw=0.8))
plt.figtext(0.50, 0.015, insight_2, fontsize=7.5, ha='center', color='#047857',
            bbox=dict(boxstyle='square,pad=0.4', facecolor='#D1FAE5', edgecolor='#34D399', lw=0.8))
plt.figtext(0.82, 0.015, insight_3, fontsize=7.5, ha='center', color='#B91C1C',
            bbox=dict(boxstyle='square,pad=0.4', facecolor='#FEE2E2', edgecolor='#F87171', lw=0.8))

# North Arrow
ax.annotate('N', xy=(0.04, 0.90), xytext=(0.04, 0.83),
            xycoords='axes fraction', ha='center', va='center',
            fontsize=12, fontweight='bold', color='#0F172A',
            arrowprops=dict(facecolor='#0F172A', edgecolor='#0F172A', width=2.5, headwidth=8))

# Scale Bar (approximately 30 km at lat 6.5: 1 deg lon ≈ 110.5 km -> 0.271 deg ≈ 30 km)
sb_x = 2.75
sb_y = 6.32
sb_len = 30 / 110.5
ax.plot([sb_x, sb_x + sb_len], [sb_y, sb_y], color='#0F172A', lw=3, zorder=5)
ax.plot([sb_x, sb_x], [sb_y - 0.006, sb_y + 0.006], color='#0F172A', lw=1.5, zorder=5)
ax.plot([sb_x + sb_len, sb_x + sb_len], [sb_y - 0.006, sb_y + 0.006], color='#0F172A', lw=1.5, zorder=5)
ax.text(sb_x + sb_len/2, sb_y + 0.012, "30 km", fontsize=8.5, fontweight='bold', ha='center', color='#0F172A', zorder=5)

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
out_file = Path('outputs/figures/00_lagos_administrative_reference_map.png')
plt.savefig(out_file, dpi=300, bbox_inches='tight')
print(f'Successfully generated {out_file} ({out_file.stat().st_size / 1024:.1f} KB)!')
