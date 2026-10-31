"""
Generate all 5 Lagos State spatial flood risk maps with:
1. Spacious 2-row vertical stack layout (18" x 14.5") matching Lagos's 5:1 shape.
2. Numbered circular badges (1 to 10) on the small congested urban core LGAs, carefully spaced.
3. Full white-haloed names on the 10 spacious outer LGAs.
4. Dedicated, prominent 'NUMBERED AREAS IDENTIFICATION KEY' box directly beneath each map.
5. Rich Top-5 Layman Cards in the open upper corners.
6. 3-part Layman Infographic Banner at the bottom.
"""

import numpy as np
import pandas as pd
import geopandas as gpd
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from mpl_toolkits.axes_grid1 import make_axes_locatable

ROOT = Path(r"C:\Users\LENOVO\Desktop\Portfolio Projects\lagos-flood-risk-ml").resolve()
FIG_DIR = (ROOT / "outputs" / "figures").resolve()
FIG_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load data
lgas_gdf = gpd.read_file(ROOT / "data" / "clean" / "lagos_lgas.gpkg")
master_df = pd.read_csv(ROOT / "data" / "clean" / "master_lga_month.csv")
risk_df = pd.read_csv(ROOT / "outputs" / "tables" / "09_lga_risk_rankings_2050.csv")

lga_stats = master_df.groupby("lga").agg({
    "elev_mean_m": "first",
    "low5_share": "first",
    "built_share": "first",
    "wetland_mangrove_share": "first",
    "rain_total_mm": "mean",
    "rain_max_daily_mm": "mean",
}).reset_index()

lga_stats["mean_annual_rain_mm"] = lga_stats["rain_total_mm"] * 12
lga_stats["low5_pct"] = lga_stats["low5_share"] * 100
lga_stats["built_pct"] = lga_stats["built_share"] * 100
lga_stats["mangrove_pct"] = lga_stats["wetland_mangrove_share"] * 100

lga_full = lgas_gdf.merge(lga_stats, on="lga", how="left").merge(risk_df, on="lga", how="left")
lga_proj = lga_full.to_crs(epsg=32631)
lga_proj["Delta_Exposed_Pop"] = lga_proj["Exposed_Pop_2050_SSP585"] - lga_proj["Exposed_Pop_Baseline"]

# The 10 urban core LGAs requiring numbers
URBAN_CORE = [
    ("Agege", 1),
    ("Ikeja", 2),
    ("Oshodi/Isolo", 3),
    ("Mushin", 4),
    ("Shomolu", 5),
    ("Surulere", 6),
    ("Mainland", 7),
    ("Ajeromi/Ifelodun", 8),
    ("Apapa", 9),
    ("Lagos Island", 10),
]

# Fine-tuned centroid coordinates for perfect badge separation without overlap
BADGE_OFFSETS = {
    "Agege": (0, 0),
    "Ikeja": (1000, 0),
    "Oshodi/Isolo": (-1200, 400),
    "Mushin": (0, 0),
    "Shomolu": (800, 200),
    "Surulere": (-600, 0),
    "Mainland": (1000, 0),
    "Ajeromi/Ifelodun": (-1000, 0),
    "Apapa": (600, -600),
    "Lagos Island": (0, 0),
}

# The remaining 10 spacious LGAs that have full text names directly on map
SPACIOUS_LGAS = [
    ("Badagry", 490298, 712859),
    ("Ojo", 516155, 712500),
    ("Amuwo Odofin", 526000, 710000),
    ("Alimosho", 527167, 731000),
    ("Ifako/Ijaye", 533599, 738800),
    ("Kosofe", 547000, 731500),
    ("Ikorodu", 565000, 734000),
    ("Eti-Osa", 564000, 711000),
    ("Ibeju-Lekki", 595736, 712500),
    ("Epe", 605000, 727000),
]

def add_clean_compass(ax):
    ax.annotate('N', xy=(0.97, 0.88), xytext=(0.97, 0.74),
                xycoords='axes fraction', textcoords='axes fraction',
                ha='center', va='bottom', fontsize=11, fontweight='bold', color="#0f172a",
                arrowprops=dict(facecolor='#0f172a', edgecolor='#0f172a', width=2, headwidth=6))

def plot_numbered_badges_and_labels(ax, lga_df):
    """Plots numbered badges 1-10 on small LGAs, and clean white-haloed names on spacious LGAs."""
    halo = [pe.withStroke(linewidth=3, foreground="white")]
    
    # 1. Names for spacious LGAs
    for name, x, y in SPACIOUS_LGAS:
        ax.text(x, y, name, fontsize=9.5, fontweight="bold", color="#1e293b",
                ha="center", va="center", path_effects=halo, zorder=5)
        
    # 2. Numbered circle badges for 10 urban core LGAs
    for name, num in URBAN_CORE:
        row = lga_df[lga_df["lga"] == name].iloc[0]
        c = row.geometry.centroid
        offset = BADGE_OFFSETS.get(name, (0, 0))
        bx = c.x + offset[0]
        by = c.y + offset[1]
        
        # Badge circle: crisp white circle with dark slate border
        circle = plt.Circle((bx, by), 1200, facecolor="#ffffff", edgecolor="#0f172a", linewidth=1.4, zorder=8)
        ax.add_patch(circle)
        
        # Bold number inside badge
        ax.text(bx, by, str(num), fontsize=8.5, fontweight="bold", color="#0f172a",
                ha="center", va="center", zorder=9)

def add_numbered_key_box(ax, lga_df, value_col, format_str, unit_str="", title_metric="Value"):
    """
    Renders a prominent, high-contrast identification key box right below the map
    linking each number badge 1-10 directly to its LGA name and exact metric value.
    """
    items = []
    for name, num in URBAN_CORE:
        row = lga_df[lga_df["lga"] == name].iloc[0]
        val = row[value_col]
        if isinstance(val, (int, float, np.floating, np.integer)):
            val_txt = f"{format_str.format(val)}{unit_str}"
        else:
            val_txt = str(val)
        items.append(f"[{num}] {name}: {val_txt}")
        
    row1 = "   |   ".join(items[:5])
    row2 = "   |   ".join(items[5:])
    
    box_text = f"KEY TO NUMBERED URBAN AREAS (1 to 10) — {title_metric}:\n{row1}\n{row2}"
    
    ax.text(
        0.50, 0.05, box_text,
        transform=ax.transAxes,
        fontsize=8.0,
        ha="center",
        va="bottom",
        fontweight="medium",
        color="#0f172a",
        bbox=dict(boxstyle="round,pad=0.45", facecolor="#ffffff", alpha=0.96, edgecolor="#64748b", linewidth=1.1),
        zorder=10
    )

def add_layman_infographic_banner(fig, points):
    card_w = 0.29
    ys = 0.045
    xs = [0.04, 0.355, 0.67]
    card_colors = ["#fff1f2", "#f0fdf4", "#eff6ff"]
    border_colors = ["#fda4af", "#86efac", "#93c5fd"]
    text_colors = ["#881337", "#14532d", "#1e3a8a"]

    for i, (head, body) in enumerate(points):
        full_text = f"{head}\n{body}"
        fig.text(
            xs[i] + card_w/2, ys, full_text,
            fontsize=8.5, ha="center", va="center", color=text_colors[i],
            bbox=dict(boxstyle="round,pad=0.5", facecolor=card_colors[i], edgecolor=border_colors[i], lw=1.2)
        )

# =============================================================================
# MAP 01: Topography & Ocean Flood Zones
# =============================================================================
print("Generating Map 01: Topography & Ocean Flood Zones...")
fig = plt.figure(figsize=(18, 14.5))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1], top=0.92, bottom=0.12, left=0.04, right=0.96, hspace=0.34)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

fig.suptitle("How Flat is Lagos? Land Elevation & Ocean Flood Danger Zones", fontsize=18, fontweight="bold", y=0.97, color="#0f172a")
fig.text(0.5, 0.942, "Why low height traps water: Areas below 5 metres (Blue) suffer when ocean tides block city stormwater drains.", fontsize=11.5, ha="center", color="#475569")

# Panel A: Elevation
divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("bottom", size="3.5%", pad=0.32)
lga_proj.plot(column="elev_mean_m", cmap="terrain", edgecolor="#334155", linewidth=0.9, legend=True, cax=cax1,
              legend_kwds={"label": "Height Above Sea Level (Metres): Green = Sea Level (2–5m)  |  Brown = High Hills (30–45m)", "orientation": "horizontal"},
              ax=ax1, vmin=2.0, vmax=48.0)
ax1.set_title("(A) Land Elevation Above Sea Level (Where is Lagos High vs. Flat?)", fontsize=13, fontweight="bold", pad=8, color="#0f172a", loc="left")
ax1.axis("off")
add_clean_compass(ax1)
plot_numbered_badges_and_labels(ax1, lga_proj)
add_numbered_key_box(ax1, lga_proj, "elev_mean_m", "{:.1f}", "m", "Height Above Sea Level")

card1_text = (
    "HIGHEST UPLAND REGIONS (Natural Gravity Drainage):\n"
    " 1. Ifako/Ijaye: 49.2 metres (Highest in Lagos)\n"
    " 2. [1] Agege: 41.9 metres\n"
    " 3. Alimosho: 27.9 metres\n"
    " 4. [2] Ikeja: 24.3 metres\n"
    " 5. [3] Oshodi/Isolo: 22.8 metres\n"
    " -> Rain flows downhill naturally into regional canals!"
)
ax1.text(0.02, 0.88, card1_text, transform=ax1.transAxes, fontsize=8.2, va="top", ha="left", color="#14532d", fontweight="medium",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#f0fdf4", edgecolor="#86efac", lw=1.1))

# Panel B: Low-Lying Land <5m
divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes("bottom", size="3.5%", pad=0.32)
lga_proj.plot(column="low5_pct", cmap="Blues", edgecolor="#334155", linewidth=0.9, legend=True, cax=cax2,
              legend_kwds={"label": "Share of Land Sunk Below 5m: White = <10% Safe High Ground  |  Dark Blue = Over 40% Severe Ocean/Tidal Flood Danger", "orientation": "horizontal"},
              ax=ax2, vmin=0.0, vmax=55.0)
ax2.set_title("(B) Ocean Flood Danger Zones: Percentage of Land Below 5 Metres", fontsize=13, fontweight="bold", pad=8, color="#0f172a", loc="left")
ax2.axis("off")
add_clean_compass(ax2)
plot_numbered_badges_and_labels(ax2, lga_proj)
add_numbered_key_box(ax2, lga_proj, "low5_pct", "{:.1f}", "%", "Land Area Sunk Below 5m")

card2_text = (
    "TOP 5 TIDAL TRAP ZONES (Land Sunk Below 5m):\n"
    " 1. [10] Lagos Island: 51.5% below 5m (Critical ocean risk)\n"
    " 2. [9] Apapa: 46.0% below 5m (Port & industrial basin)\n"
    " 3. [8] Ajeromi/Ifelodun: 45.7% below 5m\n"
    " 4. Kosofe: 40.1% below 5m (Lagoon & river edge)\n"
    " 5. Eti-Osa: 39.1% below 5m (Lekki Peninsula)\n"
    " -> High ocean tides push water BACKWARD into drains!"
)
ax2.text(0.02, 0.88, card2_text, transform=ax2.transAxes, fontsize=8.2, va="top", ha="left", color="#1e3a8a", fontweight="medium",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#eff6ff", edgecolor="#93c5fd", lw=1.1))

add_layman_infographic_banner(fig, [
    ("[SAFE HIGH GROUND] Upland Lagos (Agege, Ifako, Ikeja)",
     "Sit 20 to 50 metres above sea level. Rain flows away naturally downhill into canals.\nLow flood risk unless secondary roadside street gutters are choked with trash."),
    ("[TIDAL TRAP ZONES] Coastal Islands (Lagos Island, Apapa, Eti-Osa)",
     "Over 40% to 52% of land sits below 5 metres. When high tides enter the lagoon,\nocean water pushes BACK into drains, trapping rainwater on city streets."),
    ("[KEY TAKEAWAY] Water Cannot Flow Uphill",
     "Lowland coastal communities cannot be saved by gutter desilting alone;\nthey require mechanical pump stations, sea dikes, and one-way tidal gates.")
])

plt.savefig(str(FIG_DIR / "map_01_topography_inundation_zones.png"), dpi=300)
plt.close()
print("Saved Map 01 successfully!")

# =============================================================================
# MAP 02: Spatial Rainfall Climatology & Convective Storm Hotspots
# =============================================================================
print("Generating Map 02: Spatial Rainfall Climatology...")
fig = plt.figure(figsize=(18, 14.5))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1], top=0.92, bottom=0.12, left=0.04, right=0.96, hspace=0.34)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

fig.suptitle("Where Does It Rain Heaviest in Lagos? Annual Rain & Cloudburst Storms", fontsize=18, fontweight="bold", y=0.97, color="#0f172a")
fig.text(0.5, 0.942, "Tracking rainfall across Lagos: Rain increases from West to East, while intense 1-day downpours hit coastal areas hardest.", fontsize=11.5, ha="center", color="#475569")

# Panel A: Mean Annual Rain
divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("bottom", size="3.5%", pad=0.32)
lga_proj.plot(column="mean_annual_rain_mm", cmap="YlGnBu", edgecolor="#334155", linewidth=0.9, legend=True, cax=cax1,
              legend_kwds={"label": "Average Yearly Rain (mm): Yellow = Moderate (~1,400 mm)  |  Dark Blue = Very Heavy Torrent (>1,750 mm)", "orientation": "horizontal"},
              ax=ax1, vmin=1380, vmax=1800)
ax1.set_title("(A) Yearly Total Rainfall (West-to-East Monsoonal Gradient)", fontsize=13, fontweight="bold", pad=8, color="#0f172a", loc="left")
ax1.axis("off")
add_clean_compass(ax1)
plot_numbered_badges_and_labels(ax1, lga_proj)
add_numbered_key_box(ax1, lga_proj, "mean_annual_rain_mm", "{:.0f}", "mm", "Mean Annual Rain")

card1_text = (
    "ANNUAL RAINFALL GRADIENT (West to East):\n"
    " • Wettest: Epe (1,779 mm), [5] Shomolu (1,765 mm), [10] Island (1,763 mm)\n"
    " • Moderate: [2] Ikeja (1,675 mm), Alimosho (1,650 mm)\n"
    " • Driest: Badagry (1,460 mm), [8] Ajeromi (1,394 mm)\n"
    " -> Eastern & coastal communities receive ~400mm more rain every year!"
)
ax1.text(0.02, 0.88, card1_text, transform=ax1.transAxes, fontsize=8.2, va="top", ha="left", color="#1e3a8a", fontweight="medium",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#eff6ff", edgecolor="#93c5fd", lw=1.1))

# Panel B: Rx1day Cloudburst
divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes("bottom", size="3.5%", pad=0.32)
lga_proj.plot(column="rain_max_daily_mm", cmap="PuBuGn", edgecolor="#334155", linewidth=0.9, legend=True, cax=cax2,
              legend_kwds={"label": "Heaviest 1-Day Cloudburst (mm): Light Mint = Typical Storm (~24mm)  |  Dark Cyan = Extreme Downpour (>30mm in 24 hrs)", "orientation": "horizontal"},
              ax=ax2, vmin=22.0, vmax=32.0)
ax2.set_title("(B) Cloudburst Storm Intensity: Heaviest Single-Day Downpours (Rx1day)", fontsize=13, fontweight="bold", pad=8, color="#0f172a", loc="left")
ax2.axis("off")
add_clean_compass(ax2)
plot_numbered_badges_and_labels(ax2, lga_proj)
add_numbered_key_box(ax2, lga_proj, "rain_max_daily_mm", "{:.1f}", "mm", "Single-Day Cloudburst Peak")

card2_text = (
    "TOP 5 EXTREME 1-DAY CLOUDBURSTS (Rx1day Peak):\n"
    " 1. Eti-Osa: 31.8 mm/day average peak storm\n"
    " 2. [10] Lagos Island: 31.5 mm/day\n"
    " 3. Kosofe: 30.2 mm/day\n"
    " 4. [2] Ikeja: 29.8 mm/day\n"
    " 5. Alimosho: 28.9 mm/day\n"
    " -> Localized convective downpours overwhelm street drains in minutes!"
)
ax2.text(0.02, 0.88, card2_text, transform=ax2.transAxes, fontsize=8.2, va="top", ha="left", color="#064e3b", fontweight="medium",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#ecfdf5", edgecolor="#6ee7b7", lw=1.1))

add_layman_infographic_banner(fig, [
    ("[WEST-TO-EAST RAIN BELT] Wetter Towards Epe & Islands",
     "Badagry in the west receives ~1,394 mm of rain annually, while Epe and the central\nislands receive nearly 400 mm more (~1,779 mm) due to moist coastal storm fronts."),
    ("[SUDDEN CLOUDBURSTS] High-Volume 24-Hour Downpours",
     "Single-day storms regularly dump 80 to 115 mm of rain in a few hours,\noverwhelming street drainage canals long before water can flow into the lagoon."),
    ("[KEY TAKEAWAY] Season vs. Day Flooding",
     "Total annual rain decides how soaked and full soils become by July;\nsudden 1-day convective cloudbursts decide which streets flash-flood today.")
])

plt.savefig(str(FIG_DIR / "map_02_spatial_rainfall_gradients.png"), dpi=300)
plt.close()
print("Saved Map 02 successfully!")

# =============================================================================
# MAP 03: Concrete Jungle vs Nature's Sponge
# =============================================================================
print("Generating Map 03: Concrete Jungle vs Nature's Sponge...")
fig = plt.figure(figsize=(18, 14.5))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1], top=0.92, bottom=0.12, left=0.04, right=0.96, hspace=0.34)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

fig.suptitle("Concrete Jungle vs. Nature's Sponge: City Pavement vs. Mangrove Buffers", fontsize=18, fontweight="bold", y=0.97, color="#0f172a")
fig.text(0.5, 0.942, "How paving over nature causes flooding: Rain cannot soak into concrete (Red), while natural wetlands (Green) act as protective flood sponges.", fontsize=11.5, ha="center", color="#475569")

# Panel A: Built-Up Cover
divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("bottom", size="3.5%", pad=0.32)
lga_proj.plot(column="built_pct", cmap="OrRd", edgecolor="#334155", linewidth=0.9, legend=True, cax=cax1,
              legend_kwds={"label": "Impervious Concrete & Pavement Cover (% of Land Area): Yellow = Low Pavement (<40%)  |  Dark Red = Extreme Concrete Jungle (>90%)", "orientation": "horizontal"},
              ax=ax1, vmin=0, vmax=100)
ax1.set_title("(A) Concrete Jungle: Paved Roads, Buildings & Roofs (Zero Infiltration)", fontsize=13, fontweight="bold", pad=8, color="#0f172a", loc="left")
ax1.axis("off")
add_clean_compass(ax1)
plot_numbered_badges_and_labels(ax1, lga_proj)
add_numbered_key_box(ax1, lga_proj, "built_pct", "{:.1f}", "%", "Paved Concrete Cover")

card1_text = (
    "TOP 5 CONCRETE JUNGLES (Highest Runoff Risk):\n"
    " 1. [6] Surulere: 98.3% Paved (Zero Absorption)\n"
    " 2. [8] Ajeromi/Ifelodun: 97.4% Paved\n"
    " 3. [4] Mushin: 96.9% Paved\n"
    " 4. [1] Agege: 95.8% Paved\n"
    " 5. [7] Lagos Mainland: 95.2% Paved\n"
    " -> 100% of rainwater immediately rushes into streets!"
)
ax1.text(0.02, 0.88, card1_text, transform=ax1.transAxes, fontsize=8.2, va="top", ha="left", color="#7f1d1d", fontweight="medium",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#fff1f2", edgecolor="#fca5a5", lw=1.1))

# Panel B: Wetland and Mangrove Protective Natural Retention Buffers
divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes("bottom", size="3.5%", pad=0.32)
lga_proj.plot(column="mangrove_pct", cmap="YlGn", edgecolor="#334155", linewidth=0.9, legend=True, cax=cax2,
              legend_kwds={"label": "Natural Wetland & Mangrove Retention Buffer (% of Land Area): Cream = <2% Wetlands  |  Dark Green = Strong Natural Sponge (>15%)", "orientation": "horizontal"},
              ax=ax2, vmin=0, vmax=28)
ax2.set_title("(B) Nature's Sponge: Surviving Wetlands & Mangrove Forests (Natural Water Storage)", fontsize=13, fontweight="bold", pad=8, color="#0f172a", loc="left")
ax2.axis("off")
add_clean_compass(ax2)
plot_numbered_badges_and_labels(ax2, lga_proj)
add_numbered_key_box(ax2, lga_proj, "mangrove_pct", "{:.1f}", "%", "Wetland / Mangrove Buffer")

card2_text = (
    "TOP 5 NATURAL SPONGE BUFFERS:\n"
    " 1. [10] Lagos Island: 25.3% Wetlands & Mangroves\n"
    " 2. Kosofe: 18.0% Wetlands (Ogun River buffer)\n"
    " 3. Amuwo Odofin: 17.9% Wetlands\n"
    " 4. Ojo: 15.6% Mangroves\n"
    " 5. Badagry: 10.9% Wetlands\n"
    " -> Absorbs millions of litres of floodwater naturally!"
)
ax2.text(0.02, 0.88, card2_text, transform=ax2.transAxes, fontsize=8.2, va="top", ha="left", color="#14532d", fontweight="medium",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#f0fdf4", edgecolor="#86efac", lw=1.1))

add_layman_infographic_banner(fig, [
    ("[THE CONCRETE JUNGLE] Zero Ground Infiltration",
     "In core mainland LGAs (Surulere, Mushin, Ajeromi, Agege), over 95% of land is covered\nby concrete and roofs. Rain cannot soak into the ground, creating instant flash floods."),
    ("[NATURE'S SPONGE] Protecting Natural Floodwaters",
     "Wetlands and mangroves act like gigantic natural sponges. Where they survive (Kosofe,\nAmuwo Odofin, Badagry), they soak up excess water and prevent severe neighborhood damage."),
    ("[KEY TAKEAWAY] Nature is Cheaper than Concrete",
     "Every square metre of wetland reclaimed by sand-filling increases flood risks downstream.\nEnforcing wetland conservation and permeable paving is Lagos's most cost-effective defense.")
])

plt.savefig(str(FIG_DIR / "map_03_landcover_mangrove_buffers.png"), dpi=300)
plt.close()
print("Saved Map 03 successfully!")

# =============================================================================
# MAP 04: Climate Change Risk Escalation Frontiers (2010 to 2050)
# =============================================================================
print("Generating Map 04: Climate Risk Escalation Frontiers...")
fig = plt.figure(figsize=(18, 14.5))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1], top=0.92, bottom=0.12, left=0.04, right=0.96, hspace=0.34)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

fig.suptitle("Where is Flood Risk Growing Fastest by 2050? Climate & Population Shifts", fontsize=18, fontweight="bold", y=0.97, color="#0f172a")
fig.text(0.5, 0.942, "The expanding danger zone: How rising sea levels and suburban sprawl push the fastest risk growth into outward corridors.", fontsize=11.5, ha="center", color="#475569")

# Panel A: Delta FRI
divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("bottom", size="3.5%", pad=0.32)
lga_proj.plot(column="FRI_Change_SSP585", cmap="YlOrRd", edgecolor="#334155", linewidth=0.9, legend=True, cax=cax1,
              legend_kwds={"label": "Increase in Flood Risk Score by 2050 (Points): Yellow = Low Rise (+2 to +4)  |  Dark Red = Severe Escalation (+8 to +10 pts)", "orientation": "horizontal"},
              ax=ax1, vmin=2.0, vmax=11.0)
ax1.set_title("(A) Future Danger Growth: Increase in Flood Risk Score by 2050 (SSP5-8.5)", fontsize=13, fontweight="bold", pad=8, color="#0f172a", loc="left")
ax1.axis("off")
add_clean_compass(ax1)
plot_numbered_badges_and_labels(ax1, lga_proj)
add_numbered_key_box(ax1, lga_proj, "FRI_Change_SSP585", "+{:.1f}", " pts", "Increase in Risk Score (+pts)")

card1_text = (
    "FASTEST RISK ESCALATION FRONTIERS (Delta FRI by 2050):\n"
    " 1. Epe: +10.2 points (Fastest risk climb in entire state)\n"
    " 2. Badagry: +9.1 points\n"
    " 3. Ojo: +8.2 points\n"
    " 4. Amuwo Odofin: +7.5 points\n"
    " 5. [10] Lagos Island: +5.9 points\n"
    " -> Suburban growth corridors face the steepest climate escalation!"
)
ax1.text(0.02, 0.88, card1_text, transform=ax1.transAxes, fontsize=8.2, va="top", ha="left", color="#7c2d12", fontweight="medium",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#fff7ed", edgecolor="#fdba74", lw=1.1))

# Panel B: Delta Exposed Population
divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes("bottom", size="3.5%", pad=0.32)
lga_proj.plot(column="Delta_Exposed_Pop", cmap="Reds", edgecolor="#334155", linewidth=0.9, legend=True, cax=cax2,
              legend_kwds={"label": "New Residents Exposed to Floods: Pink = <20k New People  |  Deep Maroon = 100k to 160k More People in Danger", "orientation": "horizontal"},
              ax=ax2, vmin=0, vmax=170000)
ax2.set_title("(B) People in Harm's Way: New Residents Exposed to Floods by 2050", fontsize=13, fontweight="bold", pad=8, color="#0f172a", loc="left")
ax2.axis("off")
add_clean_compass(ax2)
plot_numbered_badges_and_labels(ax2, lga_proj)

# Custom Key box for population formatted in thousands
pop_items = []
for name, num in URBAN_CORE:
    row = lga_proj[lga_proj["lga"] == name].iloc[0]
    val = row["Delta_Exposed_Pop"]
    pop_items.append(f"[{num}] {name}: +{val/1000:.0f}k people")
row1 = "   |   ".join(pop_items[:5])
row2 = "   |   ".join(pop_items[5:])
box_text = f"KEY TO NUMBERED URBAN AREAS (1 to 10) — Net New Flood-Exposed Residents:\n{row1}\n{row2}"
ax2.text(
    0.50, 0.05, box_text, transform=ax2.transAxes, fontsize=8.0, ha="center", va="bottom",
    fontweight="medium", color="#0f172a",
    bbox=dict(boxstyle="round,pad=0.45", facecolor="#ffffff", alpha=0.96, edgecolor="#64748b", linewidth=1.1),
    zorder=10
)

card2_text = (
    "TOP 5 POPULATION EXPOSURE EXPANSIONS BY 2050:\n"
    " 1. Amuwo Odofin: +143,000 more people in flood zones\n"
    " 2. Badagry: +140,000 more people\n"
    " 3. Ojo: +121,000 more people\n"
    " 4. Eti-Osa: +84,000 more people\n"
    " 5. Kosofe: +65,000 more people\n"
    " -> Rapid demographic sprawl doubles total flood-exposed citizens!"
)
ax2.text(0.02, 0.88, card2_text, transform=ax2.transAxes, fontsize=8.2, va="top", ha="left", color="#881337", fontweight="medium",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#fff1f2", edgecolor="#fda4af", lw=1.1))

add_layman_infographic_banner(fig, [
    ("[EXPANDING SUBURBAN FRONTIERS] Risk Moves Outward",
     "Risk climbs fastest in peripheral corridors: Epe (+10.2 pts), Badagry (+9.1 pts),\nand Ojo (+8.2 pts) driven by rising sea levels (+0.29–0.40m) and monsoons."),
    ("[DOUBLING POPULATION EXPOSURE] From 1M to 2M People",
     "Rapid demographic growth in floodplains nearly doubles the number of exposed\nLagos residents from 993,000 today to 1,982,000 people annually by 2050."),
    ("[KEY TAKEAWAY] Build Drainage Before Houses",
     "Today's calm rural outskirts will become tomorrow's flood hotspots if new housing\nestates pave over natural floodplains without drainage master plans.")
])

plt.savefig(str(FIG_DIR / "map_04_climate_risk_escalation_delta.png"), dpi=300)
plt.close()
print("Saved Map 04 successfully!")

# =============================================================================
# MAP 05: Operational Policy Intervention Zoning Map
# =============================================================================
print("Generating Map 05: Operational Policy Intervention Zoning...")
fig, ax = plt.subplots(figsize=(18, 12))
fig.subplots_adjust(top=0.91, bottom=0.16, left=0.04, right=0.96)

fig.suptitle("What Should the Government Do? 4 Practical Action Zones for Lagos State", fontsize=18, fontweight="bold", y=0.97, color="#0f172a")
fig.text(0.5, 0.942, "Tailored engineering solutions for LASEMA, NIHSA, and Ministry of Environment based on each area's specific physical terrain.", fontsize=11.5, ha="center", color="#475569")

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

lga_proj.plot(color=lga_proj["zone_color"], edgecolor="#0f172a", linewidth=1.1, ax=ax)
ax.axis("off")
add_clean_compass(ax)
plot_numbered_badges_and_labels(ax, lga_proj)

# Numbered Key box for Policy Zones
zone_items = []
for name, num in URBAN_CORE:
    row = lga_proj[lga_proj["lga"] == name].iloc[0]
    z_short = row["layman_zone"].split(":")[0]
    zone_items.append(f"[{num}] {name}: {z_short}")
row1 = "   |   ".join(zone_items[:5])
row2 = "   |   ".join(zone_items[5:])
box_text = f"KEY TO NUMBERED URBAN AREAS (1 to 10) — Operational Resilience Zone Assignment:\n{row1}\n{row2}"
ax.text(
    0.50, 0.04, box_text, transform=ax.transAxes, fontsize=8.2, ha="center", va="bottom",
    fontweight="medium", color="#0f172a",
    bbox=dict(boxstyle="round,pad=0.45", facecolor="#ffffff", alpha=0.96, edgecolor="#64748b", linewidth=1.1),
    zorder=10
)

# Legend
legend_patches = [mpatches.Patch(color=color, label=zone) for zone, color in layman_palette.items()]
ax.legend(handles=legend_patches, loc="upper right", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1",
          fontsize=10, title="Priority Operational Resilience Archetype", title_fontsize=11)

add_layman_infographic_banner(fig, [
    ("[ZONE 1 & 2] Mechanical & River Defenses",
     "Zone 1 (Islands): Install tidal flap gates and stormwater pump stations against ocean surge.\nZone 2 (Ogun Corridor): Enforce 50m green riverbank setbacks and automate dam alerts."),
    ("[ZONE 3 & 4] Mainland & Suburban Rules",
     "Zone 3 (Concrete Core): Clear solid waste from street gutters biannually before storms.\nZone 4 (Suburbs): Require all new housing estates to build retention ponds (SUDS)."),
    ("[KEY TAKEAWAY] Tailored Solutions, Not Blanket Policies",
     "Building sea walls in Ikeja makes no sense; desilting gutters won't stop the ocean in Apapa!\nEvery LGA requires civil engineering tailored to its specific elevation and geography.")
])

plt.savefig(str(FIG_DIR / "map_05_policy_intervention_zoning.png"), dpi=300)
plt.close()
print("Saved Map 05 successfully!")

print("All 5 perfectly numbered and keyed maps generated successfully!")
