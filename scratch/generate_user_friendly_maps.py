"""
Generate 5 User-Friendly, Layman-Accessible, Publication-Grade Spatial Maps for Lagos Flood Risk ML.
Solves label distortion by:
1. Using clean, non-overlapping labels for large LGAs.
2. Using numbered callout badges (1-10) for the dense urban core with a dedicated Urban Core Reference Bar.
3. Adding Layman Quick-Guide Infographic Cards explaining the map in simple, plain English without problematic emojis.
4. Using intuitive, high-contrast color ramps with qualitative guideposts (Safe -> Danger).
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

ROOT = Path(r"C:\Users\LENOVO\Desktop\Portfolio Projects\lagos-flood-risk-ml").resolve()
FIG_DIR = (ROOT / "outputs" / "figures").resolve()
FIG_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load data
lgas_gdf = gpd.read_file(ROOT / "data" / "clean" / "lagos_lgas.gpkg")
master_df = pd.read_csv(ROOT / "data" / "clean" / "master_lga_month.csv")
risk_df = pd.read_csv(ROOT / "outputs" / "tables" / "09_lga_risk_rankings_2050.csv")

# Compute LGA summary statistics
lga_stats = master_df.groupby("lga").agg({
    "elev_mean_m": "first",
    "low5_share": "first",
    "low10_share": "first",
    "dist_water_mean_km": "first",
    "near_water_1km_share": "first",
    "built_share": "first",
    "wetland_mangrove_share": "first",
    "veg_share": "first",
    "rain_total_mm": "mean",
    "rain_max_daily_mm": "mean",
    "rain_max_3day_mm": "mean",
    "total_area_km2": "first",
    "land_area_km2": "first",
    "pop_density_km2": "last"
}).reset_index()

lga_stats["mean_annual_rain_mm"] = lga_stats["rain_total_mm"] * 12
lga_full = lgas_gdf.merge(lga_stats, on="lga", how="left").merge(risk_df, on="lga", how="left")
lga_proj = lga_full.to_crs(epsg=32631)

# Categorize LGAs: Urban Core (10 small congested LGAs) vs Peripheral / Large LGAs (10 spacious LGAs)
URBAN_CORE_NAMES = [
    "Agege", "Ikeja", "Oshodi/Isolo", "Mushin", "Shomolu",
    "Surulere", "Mainland", "Ajeromi/Ifelodun", "Apapa", "Lagos Island"
]

URBAN_CORE_DICT = {name: i+1 for i, name in enumerate(URBAN_CORE_NAMES)}

def add_clean_north_arrow(ax, x=0.96, y=0.92):
    ax.annotate('N', xy=(x, y), xytext=(x, y - 0.07),
                xycoords='axes fraction', textcoords='axes fraction',
                ha='center', va='bottom', fontsize=11, fontweight='bold',
                arrowprops=dict(facecolor='#0f172a', edgecolor='#0f172a', width=2, headwidth=6))

def annotate_map_cleanly(ax, gdf, value_col, format_str, unit_str="", is_zone_map=False):
    """
    Annotates large LGAs with text boxes and urban core LGAs with numbered circles.
    Also returns a formatted string table for the urban core key.
    """
    urban_key_items = []
    
    # Custom offset nudges for large LGAs to optimize cartographic balance
    nudges = {
        "Badagry": (0, 0),
        "Ojo": (0, -2000),
        "Amuwo Odofin": (-3000, -3500),
        "Alimosho": (0, 2000),
        "Ifako/Ijaye": (0, 2500),
        "Kosofe": (3000, 2000),
        "Ikorodu": (0, 2000),
        "Eti-Osa": (0, -2500),
        "Ibeju-Lekki": (0, -1500),
        "Epe": (0, 2000),
    }
    
    for _, r in gdf.iterrows():
        name = r["lga"]
        c = r.geometry.centroid
        val = r[value_col]
        
        if name in URBAN_CORE_DICT:
            num = URBAN_CORE_DICT[name]
            # Plot numbered circle badge
            ax.scatter(c.x, c.y, s=150, color="#ffffff", edgecolors="#0f172a", linewidth=1.5, zorder=6)
            ax.text(c.x, c.y, str(num), fontsize=8, fontweight="bold", ha="center", va="center", color="#0f172a", zorder=7)
            
            # Record for urban key
            if is_zone_map:
                urban_key_items.append((num, f"{name}: {val}"))
            elif isinstance(val, (int, float, np.floating, np.integer)):
                urban_key_items.append((num, f"{name} ({format_str.format(val)}{unit_str})"))
            else:
                urban_key_items.append((num, f"{name} ({val})"))
        else:
            # Large LGA: plot clean text box
            nudge = nudges.get(name, (0, 0))
            if is_zone_map:
                txt = f"{name}\n{val}"
            elif isinstance(val, (int, float, np.floating, np.integer)):
                txt = f"{name}\n{format_str.format(val)}{unit_str}"
            else:
                txt = f"{name}\n{val}"
                
            ax.annotate(
                txt,
                (c.x + nudge[0], c.y + nudge[1]),
                fontsize=7.8,
                ha="center",
                va="center",
                fontweight="bold",
                color="#0f172a",
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#ffffff", alpha=0.90, edgecolor="#94a3b8", linewidth=0.8),
                zorder=5
            )
            
    return urban_key_items

def add_urban_core_legend(ax, key_items, title="Urban Core (Numbered 1 to 10)"):
    """Adds a neat, multi-column urban core reference box in the Atlantic Ocean whitespace."""
    key_items.sort(key=lambda x: x[0])
    row1 = "  |  ".join([f"[{k[0]}] {k[1]}" for k in key_items[:5]])
    row2 = "  |  ".join([f"[{k[0]}] {k[1]}" for k in key_items[5:]])
    box_text = f"Urban Core Reference ({title}):\n{row1}\n{row2}"
    
    ax.text(
        0.50, 0.04, box_text,
        transform=ax.transAxes,
        fontsize=7.2,
        ha="center",
        va="bottom",
        fontweight="medium",
        color="#1e293b",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#f8fafc", alpha=0.94, edgecolor="#cbd5e1", linewidth=0.9),
        zorder=8
    )

def add_layman_infographic_banner(fig, points):
    """
    Adds a clean, beautifully styled 3-part Layman Quick-Guide card at the bottom of the figure.
    points: list of 3 tuples (header_text, body_text)
    """
    card_colors = ["#f0fdf4", "#eff6ff", "#fef2f2"]
    border_colors = ["#86efac", "#93c5fd", "#fca5a5"]
    text_colors = ["#14532d", "#1e3a8a", "#7f1d1d"]
    
    xs = [0.03, 0.36, 0.69]
    widths = [0.28, 0.28, 0.28]
    
    for i, (title, body) in enumerate(points):
        full_text = f"{title}\n{body}"
        fig.text(
            xs[i] + widths[i]/2, 0.055, full_text,
            fontsize=8.0,
            ha="center",
            va="center",
            color=text_colors[i],
            bbox=dict(boxstyle="round,pad=0.5", facecolor=card_colors[i], edgecolor=border_colors[i], linewidth=1.1)
        )

# =============================================================================
# MAP 01: Topography & Inundation Surge Vulnerability
# =============================================================================
print("Generating Map 01 (Layman-Friendly): Topography & Ocean Flood Zones...")
fig, axes = plt.subplots(1, 2, figsize=(19, 10.5))
fig.subplots_adjust(top=0.88, bottom=0.15, left=0.03, right=0.97, wspace=0.08)

fig.suptitle(
    "How Flat is Lagos? Land Elevation & Ocean Flood Danger Zones",
    fontsize=16, fontweight="bold", y=0.97, color="#0f172a"
)
fig.text(
    0.5, 0.935,
    "Why low height traps water: Areas below 5 metres (Blue) suffer when ocean tides block city stormwater drains.",
    fontsize=10.5, ha="center", color="#475569"
)

# Panel A: Terrestrial Elevation
divider0 = make_axes_locatable(axes[0])
cax0 = divider0.append_axes("bottom", size="3.5%", pad=0.38)
lga_proj.plot(
    column="elev_mean_m",
    cmap="terrain",
    edgecolor="#334155",
    linewidth=0.8,
    legend=True,
    cax=cax0,
    legend_kwds={"label": "Height Above Sea Level (Metres): Green = Sea Level (2–5m) | Brown = High Hills (30–45m)", "orientation": "horizontal"},
    ax=axes[0],
    vmin=2.0,
    vmax=48.0
)
axes[0].set_title("(A) Land Elevation Above Sea Level (Where is Lagos High vs. Flat?)", fontsize=12, fontweight="bold", pad=10, color="#1e293b")
axes[0].axis("off")
add_clean_north_arrow(axes[0])
key_a = annotate_map_cleanly(axes[0], lga_proj, "elev_mean_m", "{:.1f}", "m")
add_urban_core_legend(axes[0], key_a, "Elevation in Metres")

# Panel B: Low-Lying Coastal & Tidal Surge Exposure (<5m)
divider1 = make_axes_locatable(axes[1])
cax1 = divider1.append_axes("bottom", size="3.5%", pad=0.38)
lga_proj["low5_pct"] = lga_proj["low5_share"] * 100
lga_proj.plot(
    column="low5_pct",
    cmap="Blues",
    edgecolor="#1e293b",
    linewidth=0.8,
    legend=True,
    cax=cax1,
    legend_kwds={"label": "Share of Land Sunk Below 5m: White (<10% Safe) | Dark Blue (>40% Severe Ocean/Tidal Flood Danger)", "orientation": "horizontal"},
    ax=axes[1],
    vmin=0.0,
    vmax=55.0
)
axes[1].set_title("(B) Ocean Flood Danger Zones: Percentage of Land Below 5 Metres", fontsize=12, fontweight="bold", pad=10, color="#1e293b")
axes[1].axis("off")
add_clean_north_arrow(axes[1])
key_b = annotate_map_cleanly(axes[1], lga_proj, "low5_pct", "{:.1f}", "%")
add_urban_core_legend(axes[1], key_b, "Land Sunk Below 5 Metres")

add_layman_infographic_banner(fig, [
    ("[SAFE HIGH GROUND] Upland Lagos (Agege, Ifako, Ikeja, Alimosho)",
     "Sit 20 to 45 metres above sea level. Rain flows away naturally downhill into canals.\nLow flood risk unless secondary roadside street gutters are choked with trash."),
    ("[TIDAL TRAP ZONES] Coastal Islands (Lagos Island, Apapa, Eti-Osa)",
     "Over 40% to 52% of land sits below 5 metres. When high tides enter the lagoon,\nocean water pushes BACK into drains, trapping rainwater on city streets."),
    ("[KEY TAKEAWAY] Water Cannot Flow Uphill",
     "Lowland coastal communities cannot be saved by gutter desilting alone;\nthey require mechanical pump stations, sea dikes, and one-way tidal gates.")
])

map1_path = FIG_DIR / "map_01_topography_inundation_zones.png"
plt.savefig(str(map1_path), dpi=300)
plt.close()
print(f"Saved: {map1_path}")

# =============================================================================
# MAP 02: Spatial Rainfall Climatology & Convective Storm Hotspots
# =============================================================================
print("Generating Map 02 (Layman-Friendly): Spatial Rainfall Climatology...")
fig, axes = plt.subplots(1, 2, figsize=(19, 10.5))
fig.subplots_adjust(top=0.88, bottom=0.15, left=0.03, right=0.97, wspace=0.08)

fig.suptitle(
    "Where Does It Rain Heaviest in Lagos? Annual Rain & Cloudburst Storms",
    fontsize=16, fontweight="bold", y=0.97, color="#0f172a"
)
fig.text(
    0.5, 0.935,
    "Tracking rainfall across Lagos: Rain increases from West to East, while intense 1-day downpours hit coastal areas hardest.",
    fontsize=10.5, ha="center", color="#475569"
)

# Panel A: Mean Annual Rainfall
divider0 = make_axes_locatable(axes[0])
cax0 = divider0.append_axes("bottom", size="3.5%", pad=0.38)
lga_proj.plot(
    column="mean_annual_rain_mm",
    cmap="YlGnBu",
    edgecolor="#1e293b",
    linewidth=0.8,
    legend=True,
    cax=cax0,
    legend_kwds={"label": "Average Yearly Rain (mm): Yellow = Moderate (~1,400 mm) | Dark Blue = Very Heavy (>1,750 mm)", "orientation": "horizontal"},
    ax=axes[0],
    vmin=1380,
    vmax=1800
)
axes[0].set_title("(A) Yearly Total Rainfall (West-to-East Monsoonal Gradient)", fontsize=12, fontweight="bold", pad=10, color="#1e293b")
axes[0].axis("off")
add_clean_north_arrow(axes[0])
key_2a = annotate_map_cleanly(axes[0], lga_proj, "mean_annual_rain_mm", "{:.0f}", "mm")
add_urban_core_legend(axes[0], key_2a, "Annual Rain (mm)")

# Panel B: Convective Storm Cloudburst Intensity
divider1 = make_axes_locatable(axes[1])
cax1 = divider1.append_axes("bottom", size="3.5%", pad=0.38)
lga_proj.plot(
    column="rain_max_daily_mm",
    cmap="PuBuGn",
    edgecolor="#1e293b",
    linewidth=0.8,
    legend=True,
    cax=cax1,
    legend_kwds={"label": "Heaviest 1-Day Cloudburst (mm): Light Mint = Typical Storm (~24mm) | Dark Cyan = Extreme Downpour (>30mm)", "orientation": "horizontal"},
    ax=axes[1],
    vmin=22.0,
    vmax=32.0
)
axes[1].set_title("(B) Cloudburst Storm Intensity: Heaviest Single-Day Downpours", fontsize=12, fontweight="bold", pad=10, color="#1e293b")
axes[1].axis("off")
add_clean_north_arrow(axes[1])
key_2b = annotate_map_cleanly(axes[1], lga_proj, "rain_max_daily_mm", "{:.1f}", "mm")
add_urban_core_legend(axes[1], key_2b, "Max 1-Day Rain (mm)")

add_layman_infographic_banner(fig, [
    ("[WEST-TO-EAST RAIN BELT] Wetter Towards Epe & Islands",
     "Badagry in the west receives ~1,394 mm of rain annually, while Epe and the central\nislands receive nearly 400 mm more (~1,779 mm) due to moist coastal storm fronts."),
    ("[SUDDEN CLOUDBURSTS] High-Volume 24-Hour Downpours",
     "Single-day storms regularly dump 80 to 115 mm of rain in a few hours,\noverwhelming street drainage canals long before water can flow into the lagoon."),
    ("[KEY TAKEAWAY] Season vs. Day Flooding",
     "Total annual rain decides how soaked and full soils become by July;\nsudden 1-day convective cloudbursts decide which streets flash-flood today.")
])

map2_path = FIG_DIR / "map_02_spatial_rainfall_gradients.png"
plt.savefig(str(map2_path), dpi=300)
plt.close()
print(f"Saved: {map2_path}")

# =============================================================================
# MAP 03: Land Cover, Imperviousness & Mangrove Buffers
# =============================================================================
print("Generating Map 03 (Layman-Friendly): Concrete Jungle vs Nature's Sponge...")
fig, axes = plt.subplots(1, 2, figsize=(19, 10.5))
fig.subplots_adjust(top=0.88, bottom=0.15, left=0.03, right=0.97, wspace=0.08)

fig.suptitle(
    "Concrete Jungle vs. Nature's Sponge: City Pavement vs. Mangrove Buffers",
    fontsize=16, fontweight="bold", y=0.97, color="#0f172a"
)
fig.text(
    0.5, 0.935,
    "How paving over nature makes floods worse: 95%+ concrete in the city vs. natural wetlands that soak up floodwater.",
    fontsize=10.5, ha="center", color="#475569"
)

# Panel A: Urban Impervious Built-Up Footprint
divider0 = make_axes_locatable(axes[0])
cax0 = divider0.append_axes("bottom", size="3.5%", pad=0.38)
lga_proj["built_pct"] = lga_proj["built_share"] * 100
lga_proj.plot(
    column="built_pct",
    cmap="OrRd",
    edgecolor="#1e293b",
    linewidth=0.8,
    legend=True,
    cax=cax0,
    legend_kwds={"label": "Paved Concrete & Roof Cover (%): Yellow = Green/Suburban (<40%) | Deep Red = Total Concrete Jungle (>90%)", "orientation": "horizontal"},
    ax=axes[0],
    vmin=0,
    vmax=100
)
axes[0].set_title("(A) Concrete Footprint: Paved Roads, Buildings & Roofs (%)", fontsize=12, fontweight="bold", pad=10, color="#1e293b")
axes[0].axis("off")
add_clean_north_arrow(axes[0])
key_3a = annotate_map_cleanly(axes[0], lga_proj, "built_pct", "{:.0f}", "%")
add_urban_core_legend(axes[0], key_3a, "Built Concrete Cover %")

# Panel B: Wetland and Mangrove Protective Natural Retention Buffers
divider1 = make_axes_locatable(axes[1])
cax1 = divider1.append_axes("bottom", size="3.5%", pad=0.38)
lga_proj["mangrove_pct"] = lga_proj["wetland_mangrove_share"] * 100
lga_proj.plot(
    column="mangrove_pct",
    cmap="YlGn",
    edgecolor="#1e293b",
    linewidth=0.8,
    legend=True,
    cax=cax1,
    legend_kwds={"label": "Natural Wetland & Mangrove Buffer (%): Cream = No Wetlands Left (<2%) | Dark Green = Strong Sponge (>15%)", "orientation": "horizontal"},
    ax=axes[1],
    vmin=0,
    vmax=28
)
axes[1].set_title("(B) Nature's Sponge: Surviving Wetlands & Mangrove Forests (%)", fontsize=12, fontweight="bold", pad=10, color="#1e293b")
axes[1].axis("off")
add_clean_north_arrow(axes[1])
key_3b = annotate_map_cleanly(axes[1], lga_proj, "mangrove_pct", "{:.1f}", "%")
add_urban_core_legend(axes[1], key_3b, "Wetland / Mangrove %")

add_layman_infographic_banner(fig, [
    ("[CONCRETE JUNGLE] 95%+ Paved (Surulere, Mushin, Ajeromi)",
     "Over 95% of the land is covered in concrete, asphalt, and roofs. Zero rain\nsoaks into the ground; 100% of rainwater rushes into roads instantly as flash runoff."),
    ("[NATURE'S SPONGE] Protective Wetlands (Kosofe, Lagos Island)",
     "Mangroves and wetlands in Kosofe (18%) and Lagos Island (25%) act as giant natural\nsponges, absorbing millions of litres of floodwaters before they reach homes."),
    ("[KEY TAKEAWAY] Nature is Cheaper than Concrete",
     "Concrete turns rain into street torrents. Protecting remaining wetlands and\nmandating permeable paving in new developments is Lagos's most affordable flood defense.")
])

map3_path = FIG_DIR / "map_03_landcover_mangrove_buffers.png"
plt.savefig(str(map3_path), dpi=300)
plt.close()
print(f"Saved: {map3_path}")

# =============================================================================
# MAP 04: Climate Change & Sea-Level Rise Risk Escalation (2010 to 2050)
# =============================================================================
print("Generating Map 04 (Layman-Friendly): Climate Risk Escalation to 2050...")
fig, axes = plt.subplots(1, 2, figsize=(19, 10.5))
fig.subplots_adjust(top=0.88, bottom=0.15, left=0.03, right=0.97, wspace=0.08)

fig.suptitle(
    "Where is Flood Risk Growing Fastest by 2050? Climate & Population Shifts",
    fontsize=16, fontweight="bold", y=0.97, color="#0f172a"
)
fig.text(
    0.5, 0.935,
    "The expanding danger zone: How rising sea levels and suburban sprawl push the fastest risk growth into outward corridors.",
    fontsize=10.5, ha="center", color="#475569"
)

# Panel A: Net Increase in Composite Flood Risk Index (Delta FRI under SSP5-8.5)
divider0 = make_axes_locatable(axes[0])
cax0 = divider0.append_axes("bottom", size="3.5%", pad=0.38)
lga_proj.plot(
    column="FRI_Change_SSP585",
    cmap="YlOrRd",
    edgecolor="#1e293b",
    linewidth=0.8,
    legend=True,
    cax=cax0,
    legend_kwds={"label": "Increase in Flood Risk Score by 2050 (Points): Yellow = Low Rise (+2 to +4) | Dark Red = Severe Surge (+8 to +10 pts)", "orientation": "horizontal"},
    ax=axes[0],
    vmin=2.0,
    vmax=11.0
)
axes[0].set_title("(A) Future Danger Growth: Increase in Flood Risk Score by 2050", fontsize=12, fontweight="bold", pad=10, color="#1e293b")
axes[0].axis("off")
add_clean_north_arrow(axes[0])
key_4a = annotate_map_cleanly(axes[0], lga_proj, "FRI_Change_SSP585", "+{:.1f}", " pts")
add_urban_core_legend(axes[0], key_4a, "Risk Score Increase (+pts)")

# Panel B: Projected Net Increase in Flood-Exposed Population by 2050
lga_proj["Delta_Exposed_Pop"] = lga_proj["Exposed_Pop_2050_SSP585"] - lga_proj["Exposed_Pop_Baseline"]
divider1 = make_axes_locatable(axes[1])
cax1 = divider1.append_axes("bottom", size="3.5%", pad=0.38)
lga_proj.plot(
    column="Delta_Exposed_Pop",
    cmap="Reds",
    edgecolor="#1e293b",
    linewidth=0.8,
    legend=True,
    cax=cax1,
    legend_kwds={"label": "New Residents Exposed to Wet-Season Floods: Pink = <20k New People | Deep Maroon = 100k to 160k More People in Danger", "orientation": "horizontal"},
    ax=axes[1],
    vmin=0,
    vmax=170000
)
axes[1].set_title("(B) People in Harm's Way: New Residents Exposed to Floods by 2050", fontsize=12, fontweight="bold", pad=10, color="#1e293b")
axes[1].axis("off")
add_clean_north_arrow(axes[1])

# Format urban core population items in thousands
urban_key_4b = []
for _, r in lga_proj.iterrows():
    name = r["lga"]
    val = r["Delta_Exposed_Pop"]
    if name in URBAN_CORE_DICT:
        num = URBAN_CORE_DICT[name]
        urban_key_4b.append((num, f"{name} (+{val/1000:.0f}k people)"))
    else:
        nudges = {"Badagry": (0, 0), "Ojo": (0, -2000), "Amuwo Odofin": (-3000, -3500), "Alimosho": (0, 2000),
                  "Ifako/Ijaye": (0, 2500), "Kosofe": (3000, 2000), "Ikorodu": (0, 2000), "Eti-Osa": (0, -2500),
                  "Ibeju-Lekki": (0, -1500), "Epe": (0, 2000)}
        nudge = nudges.get(name, (0, 0))
        c = r.geometry.centroid
        axes[1].annotate(
            f"{name}\n+{val/1000:.0f}k people",
            (c.x + nudge[0], c.y + nudge[1]),
            fontsize=7.8,
            ha="center",
            va="center",
            fontweight="bold",
            color="#0f172a",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#ffffff", alpha=0.90, edgecolor="#94a3b8", linewidth=0.8),
            zorder=5
        )

add_urban_core_legend(axes[1], urban_key_4b, "New Exposed People by 2050")

add_layman_infographic_banner(fig, [
    ("[FASTEST RISK GROWTH] Expanding Suburbs (Epe, Badagry, Ojo)",
     "Risk climbs fastest in peripheral corridors: Epe (+10.2 pts), Badagry (+9.1 pts),\nand Ojo (+8.2 pts) driven by rising sea levels (+0.29–0.40m) and monsoons."),
    ("[DOUBLING POPULATION EXPOSURE] From 1M to 2M People",
     "Rapid demographic growth in floodplains nearly doubles the number of exposed\nLagos residents from 993,000 today to 1,982,000 people annually by 2050."),
    ("[KEY TAKEAWAY] Build Drainage Before Houses",
     "Today's calm rural outskirts will become tomorrow's flood hotspots if new housing\nestates pave over natural floodplains without drainage master plans.")
])

map4_path = FIG_DIR / "map_04_climate_risk_escalation_delta.png"
plt.savefig(str(map4_path), dpi=300)
plt.close()
print(f"Saved: {map4_path}")

# =============================================================================
# MAP 05: Operational Policy Intervention Zoning Map
# =============================================================================
print("Generating Map 05 (Layman-Friendly): Policy Action Zoning...")
fig, ax = plt.subplots(figsize=(18, 10.5))
fig.subplots_adjust(top=0.90, bottom=0.18, left=0.03, right=0.97)

fig.suptitle(
    "What Should the Government Do? 4 Practical Action Zones for Lagos State",
    fontsize=16, fontweight="bold", y=0.97, color="#0f172a"
)
fig.text(
    0.5, 0.938,
    "Tailored engineering solutions for LASEMA, NIHSA, and Ministry of Environment based on each area's specific physical geography.",
    fontsize=10.5, ha="center", color="#475569"
)

def assign_layman_zone(row):
    lga = row["lga"]
    if lga in ["Lagos Island", "Apapa", "Eti-Osa"]:
        return "Zone 1: Sea Walls & Sluice Gates (Ocean/Island Lowlands)"
    elif lga in ["Kosofe", "Ikorodu"]:
        return "Zone 2: River Buffers & Dam Warnings (Ogun River Corridor)"
    elif lga in ["Surulere", "Mushin", "Mainland", "Agege", "Oshodi/Isolo", "Shomolu"]:
        return "Zone 3: Drain Clearing & Porous Paving (Dense Concrete Mainland)"
    else:
        return "Zone 4: Green Drainage Rules (Expanding Suburban Frontiers)"

lga_proj["layman_zone"] = lga_proj.apply(assign_layman_zone, axis=1)

layman_palette = {
    "Zone 1: Sea Walls & Sluice Gates (Ocean/Island Lowlands)": "#0284c7",       # Ocean Blue
    "Zone 2: River Buffers & Dam Warnings (Ogun River Corridor)": "#10b981",    # Emerald Green
    "Zone 3: Drain Clearing & Porous Paving (Dense Concrete Mainland)": "#f59e0b", # Amber Gold
    "Zone 4: Green Drainage Rules (Expanding Suburban Frontiers)": "#8b5cf6"    # Violet Purple
}

lga_proj["zone_color"] = lga_proj["layman_zone"].map(layman_palette)

lga_proj.plot(
    color=lga_proj["zone_color"],
    edgecolor="#0f172a",
    linewidth=1.1,
    ax=ax
)
ax.axis("off")
add_clean_north_arrow(ax, x=0.96, y=0.90)

# Annotate Map 5 cleanly
key_5 = []
nudges_5 = {
    "Badagry": (0, 0),
    "Ojo": (0, -2000),
    "Amuwo Odofin": (-3000, -3500),
    "Alimosho": (0, 2000),
    "Ifako/Ijaye": (0, 2500),
    "Kosofe": (3000, 2000),
    "Ikorodu": (0, 2000),
    "Eti-Osa": (0, -2500),
    "Ibeju-Lekki": (0, -1500),
    "Epe": (0, 2000),
}

for _, r in lga_proj.iterrows():
    name = r["lga"]
    c = r.geometry.centroid
    rank = r["Rank_2050_SSP585"]
    zone_short = r["layman_zone"].split(":")[0]
    
    if name in URBAN_CORE_DICT:
        num = URBAN_CORE_DICT[name]
        ax.scatter(c.x, c.y, s=160, color="#ffffff", edgecolors="#0f172a", linewidth=1.5, zorder=6)
        ax.text(c.x, c.y, str(num), fontsize=8.5, fontweight="bold", ha="center", va="center", color="#0f172a", zorder=7)
        key_5.append((num, f"{name}: {zone_short} (Risk #{rank})"))
    else:
        nudge = nudges_5.get(name, (0, 0))
        ax.annotate(
            f"{name}\n{zone_short} (Risk #{rank})",
            (c.x + nudge[0], c.y + nudge[1]),
            fontsize=8.5,
            ha="center",
            va="center",
            fontweight="bold",
            color="#0f172a",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffffff", alpha=0.92, edgecolor="#64748b", linewidth=0.9),
            zorder=5
        )

# Add Urban Core Key in Ocean
key_5.sort(key=lambda x: x[0])
row1 = "  |  ".join([f"[{k[0]}] {k[1]}" for k in key_5[:5]])
row2 = "  |  ".join([f"[{k[0]}] {k[1]}" for k in key_5[5:]])
box_text = f"Urban Core LGAs (Numbered 1 to 10):\n{row1}\n{row2}"

ax.text(
    0.50, 0.05, box_text,
    transform=ax.transAxes,
    fontsize=8.2,
    ha="center",
    va="bottom",
    fontweight="medium",
    color="#1e293b",
    bbox=dict(boxstyle="round,pad=0.5", facecolor="#f8fafc", alpha=0.95, edgecolor="#cbd5e1", linewidth=1.0),
    zorder=8
)

# Custom Legend
legend_patches = [
    mpatches.Patch(color=color, label=zone)
    for zone, color in layman_palette.items()
]
ax.legend(
    handles=legend_patches,
    loc="upper right",
    frameon=True,
    facecolor="#ffffff",
    edgecolor="#cbd5e1",
    fontsize=9.5,
    title="Priority Policy & Engineering Archetype",
    title_fontsize=10.5
)

add_layman_infographic_banner(fig, [
    ("[ZONE 1] Ocean Sluice Gates (Islands & Coast)",
     "Install tidal one-way flap gates and pump stations in Lagos Island, Apapa, and Eti-Osa.\nStops high ocean tides from flowing backward into street gutters during storms."),
    ("[ZONE 2] River Buffers (Ogun River Corridor)",
     "Enforce 50m green buffer zones in Kosofe and Ikorodu; install real-time river gauges;\ncoordinate early emergency warnings whenever Oyan Dam prepares to release water."),
    ("[ZONE 3] Clean Gutters (Concrete Mainland)",
     "Clear solid plastic waste from secondary drains twice a year (before May 1 and August);\nmandate porous, permeable concrete in public parking lots and sidewalks.")
])

map5_path = FIG_DIR / "map_05_policy_intervention_zoning.png"
plt.savefig(str(map5_path), dpi=300)
plt.close()
print(f"Saved: {map5_path}")

print("All 5 user-friendly maps generated successfully!")
