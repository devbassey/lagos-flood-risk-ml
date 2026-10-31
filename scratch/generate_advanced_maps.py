"""
Generate 5 Advanced Spatial Map Visualizations for Lagos Flood Risk ML:
1. Map 01: Topography & Inundation Surge Vulnerability (Elevation & Land <5m)
2. Map 02: Spatial Rainfall Climatology & Convective Storm Hotspots (Mean Annual Rain & Rx1day)
3. Map 03: Land Cover, Urban Imperviousness & Wetland/Mangrove Buffers
4. Map 04: Climate Change & Sea-Level Rise Risk Escalation Frontiers (Delta FRI & Delta Exposed Population 2010->2050)
5. Map 05: Operational Resilience & Policy Intervention Spatial Zoning Map (Action Archetypes for Lagos State)

Also update the interactive HTML Leaflet map with expanded layers.
"""

import numpy as np
import pandas as pd
import geopandas as gpd
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.axes_grid1 import make_axes_locatable

ROOT = Path(r"c:\Users\LENOVO\Desktop\Portfolio Projects\lagos-flood-risk-ml")
FIG_DIR = ROOT / "outputs" / "figures"
MAP_DIR = ROOT / "outputs" / "maps"
FIG_DIR.mkdir(parents=True, exist_ok=True)
MAP_DIR.mkdir(parents=True, exist_ok=True)

# Load geospatial and tabular data
lgas_gdf = gpd.read_file(ROOT / "data" / "clean" / "lagos_lgas.gpkg")
master_df = pd.read_csv(ROOT / "data" / "clean" / "master_lga_month.csv")
risk_df = pd.read_csv(ROOT / "outputs" / "tables" / "09_lga_risk_rankings_2050.csv")

# Compute LGA-level summary stats from master_df
lga_stats = master_df.groupby("lga").agg({
    "elev_mean_m": "first",
    "low5_share": "first",
    "low10_share": "first",
    "dist_water_mean_km": "first",
    "near_water_1km_share": "first",
    "built_share": "first",
    "wetland_mangrove_share": "first",
    "veg_share": "first",
    "rain_total_mm": "mean",  # monthly mean
    "rain_max_daily_mm": "mean",
    "rain_max_3day_mm": "mean",
    "total_area_km2": "first",
    "land_area_km2": "first",
    "pop_density_km2": "last"
}).reset_index()

# Convert monthly mean rain to annual mean rain
lga_stats["mean_annual_rain_mm"] = lga_stats["rain_total_mm"] * 12

# Merge with risk rankings
lga_full = lgas_gdf.merge(lga_stats, on="lga", how="left").merge(risk_df, on="lga", how="left")

# Reproject to UTM Zone 31N (EPSG:32631) for accurate metric cartography
lga_proj = lga_full.to_crs(epsg=32631)

def add_north_arrow(ax, x=0.94, y=0.90, size=22):
    ax.annotate('N', xy=(x, y), xytext=(x, y - 0.08),
                xycoords='axes fraction', textcoords='axes fraction',
                ha='center', va='bottom', fontsize=12, fontweight='bold',
                arrowprops=dict(facecolor='black', edgecolor='black', width=2.5, headwidth=8))

# -----------------------------------------------------------------------------
# MAP 1: Topography, Elevation Relief & Coastal Surge Vulnerability
# -----------------------------------------------------------------------------
print("Generating Map 01: Topography & Inundation Surge Vulnerability...")
fig, axes = plt.subplots(1, 2, figsize=(18, 7.5))

# Panel A: Mean Elevation above Sea Level (m)
divider0 = make_axes_locatable(axes[0])
cax0 = divider0.append_axes("bottom", size="4%", pad=0.35)
lga_proj.plot(
    column="elev_mean_m",
    cmap="terrain",
    edgecolor="#1e293b",
    linewidth=0.9,
    legend=True,
    cax=cax0,
    legend_kwds={"label": "Mean Terrestrial Elevation (SRTM 30m, metres above sea level)", "orientation": "horizontal"},
    ax=axes[0],
    vmin=2.0,
    vmax=52.0
)
axes[0].set_title("(A) Lagos State Terrestrial Elevation & Topographic Relief", fontsize=13, fontweight="bold", pad=12)
axes[0].axis("off")
add_north_arrow(axes[0])

# Annotate elevations
for _, r in lga_proj.iterrows():
    c = r.geometry.centroid
    name = r["lga"]
    elev = r["elev_mean_m"]
    if name in ["Lagos Island", "Apapa", "Eti-Osa", "Kosofe", "Ikeja", "Alimosho", "Ifako/Ijaye", "Badagry", "Epe", "Ikorodu"]:
        axes[0].annotate(f"{name}\n{elev:.1f}m", (c.x, c.y), fontsize=8.5, ha="center", va="center",
                         fontweight="bold", color="#0f172a",
                         bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.75, edgecolor="none"))

# Panel B: Low-Lying Coastal & Tidal Surge Exposure (<5m)
divider1 = make_axes_locatable(axes[1])
cax1 = divider1.append_axes("bottom", size="4%", pad=0.35)
lga_proj["low5_pct"] = lga_proj["low5_share"] * 100
lga_proj.plot(
    column="low5_pct",
    cmap="Blues",
    edgecolor="#0f172a",
    linewidth=0.9,
    legend=True,
    cax=cax1,
    legend_kwds={"label": "Land Area Below 5m Elevation (% of LGA Land)", "orientation": "horizontal"},
    ax=axes[1],
    vmin=0.0,
    vmax=55.0
)
axes[1].set_title("(B) Coastal & Estuarine Surge Inundation Vulnerability (<5m Land)", fontsize=13, fontweight="bold", pad=12)
axes[1].axis("off")
add_north_arrow(axes[1])

for _, r in lga_proj.iterrows():
    c = r.geometry.centroid
    name = r["lga"]
    pct = r["low5_pct"]
    if pct >= 25.0:
        axes[1].annotate(f"{name}\n{pct:.1f}%", (c.x, c.y), fontsize=8.5, ha="center", va="center",
                         fontweight="bold", color="#1e3a8a",
                         bbox=dict(boxstyle="round,pad=0.2", facecolor="#eff6ff", alpha=0.85, edgecolor="#93c5fd"))

plt.tight_layout()
map1_path = FIG_DIR / "map_01_topography_inundation_zones.png"
plt.savefig(map1_path, dpi=300)
plt.close()
print(f"Saved: {map1_path}")

# -----------------------------------------------------------------------------
# MAP 2: Spatial Rainfall Climatology & Convective Storm Hotspots
# -----------------------------------------------------------------------------
print("Generating Map 02: Spatial Rainfall Climatology & Storm Hotspots...")
fig, axes = plt.subplots(1, 2, figsize=(18, 7.5))

# Panel A: Mean Annual Rainfall (mm/year)
divider0 = make_axes_locatable(axes[0])
cax0 = divider0.append_axes("bottom", size="4%", pad=0.35)
lga_proj.plot(
    column="mean_annual_rain_mm",
    cmap="YlGnBu",
    edgecolor="#0f172a",
    linewidth=0.9,
    legend=True,
    cax=cax0,
    legend_kwds={"label": "Mean Annual Precipitation (CHIRPS v2.0, mm/year)", "orientation": "horizontal"},
    ax=axes[0],
    vmin=1380,
    vmax=1800
)
axes[0].set_title("(A) Synoptic Rainfall Climatology Gradient Across Lagos State", fontsize=13, fontweight="bold", pad=12)
axes[0].axis("off")
add_north_arrow(axes[0])

for _, r in lga_proj.iterrows():
    c = r.geometry.centroid
    name = r["lga"]
    val = r["mean_annual_rain_mm"]
    if name in ["Badagry", "Amuwo Odofin", "Lagos Island", "Surulere", "Eti-Osa", "Epe", "Ikorodu"]:
        axes[0].annotate(f"{name}\n{val:.0f}mm", (c.x, c.y), fontsize=8.5, ha="center", va="center",
                         fontweight="bold", color="#0f172a",
                         bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8, edgecolor="none"))

# Panel B: Convective Storm Cloudburst Intensity (Rx1day)
divider1 = make_axes_locatable(axes[1])
cax1 = divider1.append_axes("bottom", size="4%", pad=0.35)
lga_proj.plot(
    column="rain_max_daily_mm",
    cmap="PuBuGn",
    edgecolor="#0f172a",
    linewidth=0.9,
    legend=True,
    cax=cax1,
    legend_kwds={"label": "Mean Monthly Maximum Daily Rainfall (Rx1day Cloudburst, mm)", "orientation": "horizontal"},
    ax=axes[1],
    vmin=22.0,
    vmax=32.0
)
axes[1].set_title("(B) Convective Storm Cloudburst Intensity (Rx1day)", fontsize=13, fontweight="bold", pad=12)
axes[1].axis("off")
add_north_arrow(axes[1])

for _, r in lga_proj.iterrows():
    c = r.geometry.centroid
    name = r["lga"]
    val = r["rain_max_daily_mm"]
    if name in ["Lagos Island", "Eti-Osa", "Kosofe", "Alimosho", "Ikorodu", "Epe", "Badagry"]:
        axes[1].annotate(f"{name}\n{val:.1f}mm", (c.x, c.y), fontsize=8.5, ha="center", va="center",
                         fontweight="bold", color="#064e3b",
                         bbox=dict(boxstyle="round,pad=0.2", facecolor="#ecfdf5", alpha=0.85, edgecolor="#6ee7b7"))

plt.tight_layout()
map2_path = FIG_DIR / "map_02_spatial_rainfall_gradients.png"
plt.savefig(map2_path, dpi=300)
plt.close()
print(f"Saved: {map2_path}")

# -----------------------------------------------------------------------------
# MAP 3: Land Cover, Imperviousness & Mangrove Nature Buffer Deficits
# -----------------------------------------------------------------------------
print("Generating Map 03: Land Cover, Imperviousness & Mangrove Buffers...")
fig, axes = plt.subplots(1, 2, figsize=(18, 7.5))

# Panel A: Urban Impervious Built-Up Footprint (%)
divider0 = make_axes_locatable(axes[0])
cax0 = divider0.append_axes("bottom", size="4%", pad=0.35)
lga_proj["built_pct"] = lga_proj["built_share"] * 100
lga_proj.plot(
    column="built_pct",
    cmap="OrRd",
    edgecolor="#0f172a",
    linewidth=0.9,
    legend=True,
    cax=cax0,
    legend_kwds={"label": "Impervious Built-Up Surface Cover (% of LGA Land)", "orientation": "horizontal"},
    ax=axes[0],
    vmin=0,
    vmax=100
)
axes[0].set_title("(A) Urban Imperviousness Footprint (ESA WorldCover 10m)", fontsize=13, fontweight="bold", pad=12)
axes[0].axis("off")
add_north_arrow(axes[0])

for _, r in lga_proj.iterrows():
    c = r.geometry.centroid
    name = r["lga"]
    val = r["built_pct"]
    if val >= 85.0:
        axes[0].annotate(f"{name}\n{val:.0f}%", (c.x, c.y), fontsize=8.5, ha="center", va="center",
                         fontweight="bold", color="#7f1d1d",
                         bbox=dict(boxstyle="round,pad=0.2", facecolor="#fef2f2", alpha=0.85, edgecolor="#fca5a5"))

# Panel B: Wetland and Mangrove Protective Natural Retention Buffers (%)
divider1 = make_axes_locatable(axes[1])
cax1 = divider1.append_axes("bottom", size="4%", pad=0.35)
lga_proj["mangrove_pct"] = lga_proj["wetland_mangrove_share"] * 100
lga_proj.plot(
    column="mangrove_pct",
    cmap="YlGn",
    edgecolor="#0f172a",
    linewidth=0.9,
    legend=True,
    cax=cax1,
    legend_kwds={"label": "Mangrove & Wetland Retention Buffer (% of LGA Land)", "orientation": "horizontal"},
    ax=axes[1],
    vmin=0,
    vmax=30
)
axes[1].set_title("(B) Wetland & Mangrove Protective Retention Buffers", fontsize=13, fontweight="bold", pad=12)
axes[1].axis("off")
add_north_arrow(axes[1])

for _, r in lga_proj.iterrows():
    c = r.geometry.centroid
    name = r["lga"]
    val = r["mangrove_pct"]
    if val >= 5.0:
        axes[1].annotate(f"{name}\n{val:.1f}%", (c.x, c.y), fontsize=8.5, ha="center", va="center",
                         fontweight="bold", color="#14532d",
                         bbox=dict(boxstyle="round,pad=0.2", facecolor="#f0fdf4", alpha=0.85, edgecolor="#86efac"))

plt.tight_layout()
map3_path = FIG_DIR / "map_03_landcover_mangrove_buffers.png"
plt.savefig(map3_path, dpi=300)
plt.close()
print(f"Saved: {map3_path}")

# -----------------------------------------------------------------------------
# MAP 4: Climate Change & Sea-Level Rise Risk Escalation Frontiers (2010 to 2050)
# -----------------------------------------------------------------------------
print("Generating Map 04: Climate Risk Escalation Delta (2010 -> 2050)...")
fig, axes = plt.subplots(1, 2, figsize=(18, 7.5))

# Panel A: Net Increase in Composite Flood Risk Index (Delta FRI under SSP5-8.5)
divider0 = make_axes_locatable(axes[0])
cax0 = divider0.append_axes("bottom", size="4%", pad=0.35)
lga_proj.plot(
    column="FRI_Change_SSP585",
    cmap="inferno",
    edgecolor="#0f172a",
    linewidth=0.9,
    legend=True,
    cax=cax0,
    legend_kwds={"label": "Projected Increase in Flood Risk Index (Delta FRI, 2010–2025 to 2050 SSP5-8.5)", "orientation": "horizontal"},
    ax=axes[0],
    vmin=2.0,
    vmax=11.0
)
axes[0].set_title("(A) Climate Change Risk Escalation Frontier (Delta FRI to 2050)", fontsize=13, fontweight="bold", pad=12)
axes[0].axis("off")
add_north_arrow(axes[0])

for _, r in lga_proj.iterrows():
    c = r.geometry.centroid
    name = r["lga"]
    val = r["FRI_Change_SSP585"]
    if val >= 6.0:
        axes[0].annotate(f"{name}\n+{val:.1f} FRI", (c.x, c.y), fontsize=8.5, ha="center", va="center",
                         fontweight="bold", color="#ffffff",
                         bbox=dict(boxstyle="round,pad=0.2", facecolor="#7c2d12", alpha=0.85, edgecolor="#fdba74"))

# Panel B: Projected Net Increase in Flood-Exposed Population by 2050 (SSP5-8.5)
lga_proj["Delta_Exposed_Pop"] = lga_proj["Exposed_Pop_2050_SSP585"] - lga_proj["Exposed_Pop_Baseline"]
divider1 = make_axes_locatable(axes[1])
cax1 = divider1.append_axes("bottom", size="4%", pad=0.35)
lga_proj.plot(
    column="Delta_Exposed_Pop",
    cmap="Reds",
    edgecolor="#0f172a",
    linewidth=0.9,
    legend=True,
    cax=cax1,
    legend_kwds={"label": "Net Growth in Annual Flood-Exposed Residents by 2050 (Persons/Year)", "orientation": "horizontal"},
    ax=axes[1],
    vmin=0,
    vmax=180000
)
axes[1].set_title("(B) Human Exposure Expansion (Net Growth in Exposed Residents)", fontsize=13, fontweight="bold", pad=12)
axes[1].axis("off")
add_north_arrow(axes[1])

for _, r in lga_proj.iterrows():
    c = r.geometry.centroid
    name = r["lga"]
    val = r["Delta_Exposed_Pop"]
    if val >= 50000:
        axes[1].annotate(f"{name}\n+{val/1000:.0f}k people", (c.x, c.y), fontsize=8.5, ha="center", va="center",
                         fontweight="bold", color="#7f1d1d",
                         bbox=dict(boxstyle="round,pad=0.2", facecolor="#fff1f2", alpha=0.9, edgecolor="#fda4af"))

plt.tight_layout()
map4_path = FIG_DIR / "map_04_climate_risk_escalation_delta.png"
plt.savefig(map4_path, dpi=300)
plt.close()
print(f"Saved: {map4_path}")

# -----------------------------------------------------------------------------
# MAP 5: Lagos State Policy Intervention & Resilience Action Zoning Map
# -----------------------------------------------------------------------------
print("Generating Map 05: Operational Policy Intervention Zoning Map...")
fig, ax = plt.subplots(figsize=(14, 8))

# Define Policy Intervention Archetypes:
# Zone 1: Coastal Tidal Defense & Sluice Gates (Lagos Island, Apapa, Eti-Osa)
# Zone 2: Fluvial Riverine Retention & Dam Early Warning (Kosofe, Ikorodu)
# Zone 3: High-Density Pluvial Drainage Desilting & Pavement Retrofitting (Surulere, Mushin, Mainland, Agege, Oshodi/Isolo, Shomolu)
# Zone 4: Peri-Urban Green Infrastructure & SUDS Mandate (Alimosho, Ojo, Badagry, Ibeju-Lekki, Epe, Amuwo Odofin, Ifako/Ijaye, Ikeja)

def assign_policy_zone(row):
    lga = row["lga"]
    if lga in ["Lagos Island", "Apapa", "Eti-Osa"]:
        return "Zone 1: Coastal Tidal Defense & Sluice Gates"
    elif lga in ["Kosofe", "Ikorodu"]:
        return "Zone 2: Fluvial Riverine Buffer & Dam Telemetry"
    elif lga in ["Surulere", "Mushin", "Mainland", "Agege", "Oshodi/Isolo", "Shomolu"]:
        return "Zone 3: Core Pluvial Desilting & Pavement Retrofit"
    else:
        return "Zone 4: Peri-Urban SUDS & Permeable Mandates"

lga_proj["policy_zone"] = lga_proj.apply(assign_policy_zone, axis=1)

zone_palette = {
    "Zone 1: Coastal Tidal Defense & Sluice Gates": "#0284c7",          # Ocean Blue
    "Zone 2: Fluvial Riverine Buffer & Dam Telemetry": "#10b981",        # Emerald Green
    "Zone 3: Core Pluvial Desilting & Pavement Retrofit": "#f59e0b",     # Amber Orange
    "Zone 4: Peri-Urban SUDS & Permeable Mandates": "#8b5cf6"           # Violet Purple
}

lga_proj["zone_color"] = lga_proj["policy_zone"].map(zone_palette)

lga_proj.plot(
    color=lga_proj["zone_color"],
    edgecolor="#0f172a",
    linewidth=1.2,
    ax=ax
)

# Label all 20 LGAs with zone-styled text
for _, r in lga_proj.iterrows():
    c = r.geometry.centroid
    name = r["lga"]
    rank = r["Rank_2050_SSP585"]
    fri = r["FRI_2050_SSP585"]
    ax.annotate(f"{name}\n#{rank} (FRI {fri:.1f})", (c.x, c.y), fontsize=8.5, ha="center", va="center",
                fontweight="bold", color="#0f172a",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.85, edgecolor="#64748b"))

# Create legend
legend_patches = [
    mpatches.Patch(color=color, label=zone)
    for zone, color in zone_palette.items()
]
ax.legend(handles=legend_patches, loc="lower right", frameon=True, fontsize=10.5, title="Operational Resilience Zones (LASEMA / Ministry of Environment)", title_fontsize=11.5)

ax.set_title("Lagos State Operational Flood Resilience & Policy Intervention Zoning Map", fontsize=14, fontweight="bold", pad=16)
ax.axis("off")
add_north_arrow(ax, x=0.96, y=0.92)

plt.tight_layout()
map5_path = FIG_DIR / "map_05_policy_intervention_zoning.png"
plt.savefig(map5_path, dpi=300)
plt.close()
print(f"Saved: {map5_path}")

# -----------------------------------------------------------------------------
# 6. ENHANCE INTERACTIVE FOLIUM HTML WEB MAP WITH EXPANDED LAYERS
# -----------------------------------------------------------------------------
print("Updating Interactive Leaflet HTML Map with Expanded Layers...")
import folium
from folium import plugins

# Base map centered on Lagos State
m = folium.Map(location=[6.5244, 3.3792], zoom_start=10, tiles="CartoDB positron")

# Convert lga_full back to WGS84 for GeoJSON
lga_wgs84 = lga_full.to_crs(epsg=4326)

# Feature Group 1: 2050 SSP5-8.5 Risk (Default)
fg_2050 = folium.FeatureGroup(name="2050 Flood Risk Index (SSP5-8.5)", show=True)
def style_fri_2050(feature):
    val = feature["properties"]["FRI_2050_SSP585"]
    if val >= 50:
        c = "#7f1d1d"
    elif val >= 45:
        c = "#dc2626"
    elif val >= 35:
        c = "#f59e0b"
    else:
        c = "#10b981"
    return {"fillColor": c, "color": "#0f172a", "weight": 1.5, "fillOpacity": 0.65}

folium.GeoJson(
    lga_wgs84,
    style_function=style_fri_2050,
    tooltip=folium.GeoJsonTooltip(
        fields=["lga", "FRI_2050_SSP585", "Rank_2050_SSP585", "Exposed_Pop_2050_SSP585", "elev_mean_m", "built_share"],
        aliases=["LGA:", "2050 FRI (SSP5-8.5):", "2050 Rank:", "Exposed Residents:", "Mean Elevation (m):", "Built-Up Share:"],
        localize=True
    )
).add_to(fg_2050)
fg_2050.add_to(m)

# Feature Group 2: Baseline FRI
fg_base = folium.FeatureGroup(name="Baseline Flood Risk Index (2010–2025)", show=False)
def style_fri_base(feature):
    val = feature["properties"]["FRI_Baseline"]
    if val >= 50:
        c = "#7f1d1d"
    elif val >= 45:
        c = "#dc2626"
    elif val >= 35:
        c = "#f59e0b"
    else:
        c = "#10b981"
    return {"fillColor": c, "color": "#0f172a", "weight": 1.5, "fillOpacity": 0.65}

folium.GeoJson(
    lga_wgs84,
    style_function=style_fri_base,
    tooltip=folium.GeoJsonTooltip(
        fields=["lga", "FRI_Baseline", "Rank_Baseline", "Exposed_Pop_Baseline"],
        aliases=["LGA:", "Baseline FRI:", "Baseline Rank:", "Baseline Exposed Pop:"],
        localize=True
    )
).add_to(fg_base)
fg_base.add_to(m)

# Feature Group 3: Low-Lying Land (<5m Surge Zone)
fg_surge = folium.FeatureGroup(name="Low-Lying Land Fraction (<5m Surge Exposure)", show=False)
def style_surge(feature):
    val = feature["properties"]["low5_share"] * 100
    if val >= 40:
        c = "#1e3a8a"
    elif val >= 25:
        c = "#2563eb"
    elif val >= 10:
        c = "#60a5fa"
    else:
        c = "#eff6ff"
    return {"fillColor": c, "color": "#0f172a", "weight": 1.5, "fillOpacity": 0.65}

folium.GeoJson(
    lga_wgs84,
    style_function=style_surge,
    tooltip=folium.GeoJsonTooltip(
        fields=["lga", "low5_share", "dist_water_mean_km"],
        aliases=["LGA:", "Land <5m Share:", "Dist to Water (km):"],
        localize=True
    )
).add_to(fg_surge)
fg_surge.add_to(m)

# Feature Group 4: Urban Impervious Built-Up Footprint
fg_built = folium.FeatureGroup(name="Urban Impervious Built-Up Share (%)", show=False)
def style_built(feature):
    val = feature["properties"]["built_share"] * 100
    if val >= 85:
        c = "#7f1d1d"
    elif val >= 60:
        c = "#ea580c"
    elif val >= 30:
        c = "#f59e0b"
    else:
        c = "#fef08a"
    return {"fillColor": c, "color": "#0f172a", "weight": 1.5, "fillOpacity": 0.65}

folium.GeoJson(
    lga_wgs84,
    style_function=style_built,
    tooltip=folium.GeoJsonTooltip(
        fields=["lga", "built_share", "pop_density_km2"],
        aliases=["LGA:", "Built-Up Footprint:", "Pop Density (/km²):"],
        localize=True
    )
).add_to(fg_built)
fg_built.add_to(m)

folium.LayerControl(collapsed=False).add_to(m)
plugins.Fullscreen().add_to(m)

interactive_html = MAP_DIR / "lagos_flood_risk_interactive.html"
m.save(interactive_html)
print(f"Saved expanded interactive web map: {interactive_html}")

print("\nAll 5 advanced map visualizations and enhanced web map generated successfully!")
