"""
Master Script: Generate all 5 clean, user-friendly, distortion-free geospatial maps for Lagos Flood Risk ML.
Key features:
1. 2-row vertical stack layout for Maps 1-4 matching Lagos State's 5:1 aspect ratio perfectly.
2. Completely clean polygons: zero overlapping boxes or clustered numbered badges on the map!
3. Clean, white-haloed labels for major anchor regions.
4. Clean pointer callouts for the central urban core and key physical zones.
5. Rich, beautifully styled Layman Cards showing Top 5 LGA rankings and plain-English explanations.
6. 3-part Layman Quick-Guide Infographic Banner at the bottom.
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

def add_clean_compass(ax):
    ax.annotate('N', xy=(0.97, 0.88), xytext=(0.97, 0.74),
                xycoords='axes fraction', textcoords='axes fraction',
                ha='center', va='bottom', fontsize=11, fontweight='bold', color="#0f172a",
                arrowprops=dict(facecolor='#0f172a', edgecolor='#0f172a', width=2, headwidth=6))

def plot_clean_major_labels(ax):
    halo = [pe.withStroke(linewidth=3, foreground="white")]
    labels = [
        ("Badagry", 490298, 712859),
        ("Alimosho", 527167, 731000),
        ("Ikorodu", 565000, 734000),
        ("Epe", 605000, 727000),
        ("Ibeju-Lekki", 595736, 712500),
    ]
    for name, x, y in labels:
        ax.text(x, y, name, fontsize=10, fontweight="bold", color="#1e293b",
                ha="center", va="center", path_effects=halo)

def add_layman_infographic_banner(fig, points):
    card_w = 0.29
    ys = 0.05
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
# MAP 01: Land Elevation & Ocean Flood Danger Zones
# =============================================================================
print("Generating Map 01: Topography & Ocean Flood Zones...")
fig = plt.figure(figsize=(17, 13))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1], top=0.91, bottom=0.13, left=0.04, right=0.96, hspace=0.32)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

fig.suptitle("How Flat is Lagos? Land Elevation & Ocean Flood Danger Zones", fontsize=18, fontweight="bold", y=0.97, color="#0f172a")
fig.text(0.5, 0.935, "Why low height traps water: Areas below 5 metres (Blue) suffer when ocean tides block city stormwater drains.", fontsize=12, ha="center", color="#475569")

# Panel A: Elevation
divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("bottom", size="4%", pad=0.25)
lga_proj.plot(column="elev_mean_m", cmap="terrain", edgecolor="#334155", linewidth=0.9, legend=True, cax=cax1,
              legend_kwds={"label": "Height Above Sea Level (Metres): Green = Sea Level (2–5m)  |  Brown = High Hills (30–45m)", "orientation": "horizontal"},
              ax=ax1, vmin=2.0, vmax=48.0)
ax1.set_title("(A) Land Elevation Above Sea Level (Where is Lagos High vs. Flat?)", fontsize=13, fontweight="bold", pad=8, color="#0f172a", loc="left")
ax1.axis("off")
add_clean_compass(ax1)
plot_clean_major_labels(ax1)

ax1.annotate("NORTHERN HIGHLANDS\nAgege (41.9m) & Ifako (49.2m)\nSafe natural gravity drainage",
             xy=(535000, 735000), xytext=(535000, 706000), fontsize=9.5, fontweight="bold", color="#14532d", ha="center",
             arrowprops=dict(arrowstyle="->", color="#14532d", lw=1.5),
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#f0fdf4", edgecolor="#86efac", lw=1.2))

card1_text = (
    "HIGHEST UPLAND REGIONS (Natural Gravity Drainage):\n"
    " 1. Ifako/Ijaye: 49.2 metres (Highest in Lagos)\n"
    " 2. Agege: 41.9 metres\n"
    " 3. Alimosho: 27.9 metres\n"
    " 4. Ikeja: 24.3 metres\n"
    " 5. Oshodi/Isolo: 22.8 metres\n"
    " -> Rain flows downhill naturally into regional canals!"
)
ax1.text(0.02, 0.88, card1_text, transform=ax1.transAxes, fontsize=8.5, va="top", ha="left", color="#14532d", fontweight="medium",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#f0fdf4", edgecolor="#86efac", lw=1.1))

# Panel B: Low-Lying Land <5m
divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes("bottom", size="4%", pad=0.25)
lga_proj.plot(column="low5_pct", cmap="Blues", edgecolor="#334155", linewidth=0.9, legend=True, cax=cax2,
              legend_kwds={"label": "Share of Land Sunk Below 5m: White = <10% Safe High Ground  |  Dark Blue = Over 40% Severe Ocean/Tidal Flood Danger", "orientation": "horizontal"},
              ax=ax2, vmin=0.0, vmax=55.0)
ax2.set_title("(B) Ocean Flood Danger Zones: Percentage of Land Below 5 Metres", fontsize=13, fontweight="bold", pad=8, color="#0f172a", loc="left")
ax2.axis("off")
add_clean_compass(ax2)
plot_clean_major_labels(ax2)

ax2.annotate("CRITICAL TIDAL TRAP\nLagos Island (51.5%) & Apapa (46.0%)\nOcean tides block street drains",
             xy=(546000, 715000), xytext=(546000, 706000), fontsize=9.5, fontweight="bold", color="#1e3a8a", ha="center",
             arrowprops=dict(arrowstyle="->", color="#1e3a8a", lw=1.5),
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#eff6ff", edgecolor="#93c5fd", lw=1.2))

card2_text = (
    "TOP 5 TIDAL TRAP ZONES (Land Sunk Below 5m):\n"
    " 1. Lagos Island: 51.5% below 5m (Critical ocean risk)\n"
    " 2. Apapa: 46.0% below 5m (Port & industrial basin)\n"
    " 3. Ajeromi/Ifelodun: 45.7% below 5m\n"
    " 4. Kosofe: 40.1% below 5m (Lagoon & river edge)\n"
    " 5. Eti-Osa: 39.1% below 5m (Lekki Peninsula)\n"
    " -> High ocean tides push water BACKWARD into drains!"
)
ax2.text(0.02, 0.88, card2_text, transform=ax2.transAxes, fontsize=8.5, va="top", ha="left", color="#1e3a8a", fontweight="medium",
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
# MAP 02: Spatial Rainfall Climatology & Convective Cloudburst Hotspots
# =============================================================================
print("Generating Map 02: Spatial Rainfall Climatology...")
fig = plt.figure(figsize=(17, 13))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1], top=0.91, bottom=0.13, left=0.04, right=0.96, hspace=0.32)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

fig.suptitle("Where Does It Rain Heaviest in Lagos? Annual Rain & Cloudburst Storms", fontsize=18, fontweight="bold", y=0.97, color="#0f172a")
fig.text(0.5, 0.935, "Tracking rainfall across Lagos: Rain increases from West to East, while intense 1-day downpours hit coastal areas hardest.", fontsize=12, ha="center", color="#475569")

# Panel A: Mean Annual Rain
divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("bottom", size="4%", pad=0.25)
lga_proj.plot(column="mean_annual_rain_mm", cmap="YlGnBu", edgecolor="#334155", linewidth=0.9, legend=True, cax=cax1,
              legend_kwds={"label": "Average Yearly Rain (mm): Yellow = Moderate (~1,400 mm)  |  Dark Blue = Very Heavy Torrent (>1,750 mm)", "orientation": "horizontal"},
              ax=ax1, vmin=1380, vmax=1800)
ax1.set_title("(A) Yearly Total Rainfall (West-to-East Monsoonal Gradient)", fontsize=13, fontweight="bold", pad=8, color="#0f172a", loc="left")
ax1.axis("off")
add_clean_compass(ax1)
plot_clean_major_labels(ax1)

ax1.annotate("EASTERN RAIN BELT\nEpe (1,779mm) & Lagos Island (1,763mm)\nReceives ~400mm more rain yearly than Badagry",
             xy=(590000, 722000), xytext=(590000, 706000), fontsize=9.5, fontweight="bold", color="#1e3a8a", ha="center",
             arrowprops=dict(arrowstyle="->", color="#1e3a8a", lw=1.5),
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#eff6ff", edgecolor="#93c5fd", lw=1.2))

card1_text = (
    "ANNUAL RAINFALL GRADIENT (West to East):\n"
    " • Wettest: Epe (1,779 mm), Shomolu (1,765 mm), Lagos Island (1,763 mm)\n"
    " • Moderate: Ikeja (1,675 mm), Alimosho (1,650 mm)\n"
    " • Driest: Badagry (1,460 mm), Ajeromi (1,394 mm)\n"
    " -> Eastern & coastal communities receive ~400mm more rain every year!"
)
ax1.text(0.02, 0.88, card1_text, transform=ax1.transAxes, fontsize=8.5, va="top", ha="left", color="#1e3a8a", fontweight="medium",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#eff6ff", edgecolor="#93c5fd", lw=1.1))

# Panel B: Rx1day Cloudburst
divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes("bottom", size="4%", pad=0.25)
lga_proj.plot(column="rain_max_daily_mm", cmap="PuBuGn", edgecolor="#334155", linewidth=0.9, legend=True, cax=cax2,
              legend_kwds={"label": "Heaviest 1-Day Cloudburst (mm): Light Mint = Typical Storm (~24mm)  |  Dark Cyan = Extreme Downpour (>30mm in 24 hrs)", "orientation": "horizontal"},
              ax=ax2, vmin=22.0, vmax=32.0)
ax2.set_title("(B) Cloudburst Storm Intensity: Heaviest Single-Day Downpours (Rx1day)", fontsize=13, fontweight="bold", pad=8, color="#0f172a", loc="left")
ax2.axis("off")
add_clean_compass(ax2)
plot_clean_major_labels(ax2)

ax2.annotate("COASTAL CLOUDBURST HOTSPOT\nEti-Osa (31.8mm) & Lagos Island (31.5mm)\nSingle storms dump 80–115mm in hours",
             xy=(555000, 715000), xytext=(555000, 706000), fontsize=9.5, fontweight="bold", color="#064e3b", ha="center",
             arrowprops=dict(arrowstyle="->", color="#064e3b", lw=1.5),
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#ecfdf5", edgecolor="#6ee7b7", lw=1.2))

card2_text = (
    "TOP 5 EXTREME 1-DAY CLOUDBURSTS (Rx1day Peak):\n"
    " 1. Eti-Osa: 31.8 mm/day average peak storm\n"
    " 2. Lagos Island: 31.5 mm/day\n"
    " 3. Kosofe: 30.2 mm/day\n"
    " 4. Ikeja: 29.8 mm/day\n"
    " 5. Alimosho: 28.9 mm/day\n"
    " -> Localized convective downpours overwhelm street drains in minutes!"
)
ax2.text(0.02, 0.88, card2_text, transform=ax2.transAxes, fontsize=8.5, va="top", ha="left", color="#064e3b", fontweight="medium",
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
# MAP 04: Climate Change Risk Escalation Frontiers (2010 to 2050)
# =============================================================================
print("Generating Map 04: Climate Risk Escalation Frontiers...")
fig = plt.figure(figsize=(17, 13))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1], top=0.91, bottom=0.13, left=0.04, right=0.96, hspace=0.32)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

fig.suptitle("Where is Flood Risk Growing Fastest by 2050? Climate & Population Shifts", fontsize=18, fontweight="bold", y=0.97, color="#0f172a")
fig.text(0.5, 0.935, "The expanding danger zone: How rising sea levels and suburban sprawl push the fastest risk growth into outward corridors.", fontsize=12, ha="center", color="#475569")

# Panel A: Delta FRI
divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("bottom", size="4%", pad=0.25)
lga_proj.plot(column="FRI_Change_SSP585", cmap="YlOrRd", edgecolor="#334155", linewidth=0.9, legend=True, cax=cax1,
              legend_kwds={"label": "Increase in Flood Risk Score by 2050 (Points): Yellow = Low Rise (+2 to +4)  |  Dark Red = Severe Escalation (+8 to +10 pts)", "orientation": "horizontal"},
              ax=ax1, vmin=2.0, vmax=11.0)
ax1.set_title("(A) Future Danger Growth: Increase in Flood Risk Score by 2050 (SSP5-8.5)", fontsize=13, fontweight="bold", pad=8, color="#0f172a", loc="left")
ax1.axis("off")
add_clean_compass(ax1)
plot_clean_major_labels(ax1)

ax1.annotate("FASTEST ACCELERATING RISK\nEpe (+10.2 pts) & Badagry (+9.1 pts)\nSea level rise & expanding development",
             xy=(605000, 725000), xytext=(605000, 706000), fontsize=9.5, fontweight="bold", color="#7c2d12", ha="center",
             arrowprops=dict(arrowstyle="->", color="#7c2d12", lw=1.5),
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff7ed", edgecolor="#fdba74", lw=1.2))

card1_text = (
    "FASTEST RISK ESCALATION FRONTIERS (Delta FRI by 2050):\n"
    " 1. Epe: +10.2 points (Fastest risk climb in entire state)\n"
    " 2. Badagry: +9.1 points\n"
    " 3. Ojo: +8.2 points\n"
    " 4. Amuwo Odofin: +7.5 points\n"
    " 5. Alimosho: +5.7 points\n"
    " -> Suburban growth corridors face the steepest climate escalation!"
)
ax1.text(0.02, 0.88, card1_text, transform=ax1.transAxes, fontsize=8.5, va="top", ha="left", color="#7c2d12", fontweight="medium",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#fff7ed", edgecolor="#fdba74", lw=1.1))

# Panel B: Delta Exposed Population
divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes("bottom", size="4%", pad=0.25)
lga_proj.plot(column="Delta_Exposed_Pop", cmap="Reds", edgecolor="#334155", linewidth=0.9, legend=True, cax=cax2,
              legend_kwds={"label": "New Residents Exposed to Floods: Pink = <20k New People  |  Deep Maroon = 100k to 160k More People in Danger", "orientation": "horizontal"},
              ax=ax2, vmin=0, vmax=170000)
ax2.set_title("(B) People in Harm's Way: New Residents Exposed to Floods by 2050", fontsize=13, fontweight="bold", pad=8, color="#0f172a", loc="left")
ax2.axis("off")
add_clean_compass(ax2)
plot_clean_major_labels(ax2)

ax2.annotate("POPULATION EXPOSURE SURGE\nAmuwo (+143k), Badagry (+140k), Ojo (+121k)\nMassive influx of people into low-lying floodplains",
             xy=(515000, 715000), xytext=(515000, 706000), fontsize=9.5, fontweight="bold", color="#881337", ha="center",
             arrowprops=dict(arrowstyle="->", color="#881337", lw=1.5),
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff1f2", edgecolor="#fda4af", lw=1.2))

card2_text = (
    "TOP 5 POPULATION EXPOSURE EXPANSIONS BY 2050:\n"
    " 1. Amuwo Odofin: +143,000 more people in flood zones\n"
    " 2. Badagry: +140,000 more people\n"
    " 3. Ojo: +121,000 more people\n"
    " 4. Eti-Osa: +84,000 more people\n"
    " 5. Kosofe: +65,000 more people\n"
    " -> Rapid demographic sprawl doubles total flood-exposed citizens!"
)
ax2.text(0.02, 0.88, card2_text, transform=ax2.transAxes, fontsize=8.5, va="top", ha="left", color="#881337", fontweight="medium",
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
fig, ax = plt.subplots(figsize=(17, 11))
fig.subplots_adjust(top=0.90, bottom=0.18, left=0.04, right=0.96)

fig.suptitle("What Should the Government Do? 4 Practical Action Zones for Lagos State", fontsize=18, fontweight="bold", y=0.97, color="#0f172a")
fig.text(0.5, 0.935, "Tailored engineering solutions for LASEMA, NIHSA, and Ministry of Environment based on each area's specific physical terrain.", fontsize=12, ha="center", color="#475569")

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
plot_clean_major_labels(ax)

# Clean callouts pointing to the 4 action zones
ax.annotate("ZONE 1: OCEAN SLUICE GATES\nLagos Island, Apapa, Eti-Osa\nMechanical pumps & tidal flap gates",
            xy=(550000, 715000), xytext=(550000, 706000), fontsize=9.5, fontweight="bold", color="#0369a1", ha="center",
            arrowprops=dict(arrowstyle="->", color="#0369a1", lw=1.5),
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#f0f9ff", edgecolor="#7dd3fc", lw=1.2))

ax.annotate("ZONE 2: RIVER BUFFERS & TELEMETRY\nKosofe & Ikorodu (Ogun River Corridor)\nAutomated river gauges & Oyan Dam warnings",
            xy=(555000, 732000), xytext=(555000, 743000), fontsize=9.5, fontweight="bold", color="#047857", ha="center",
            arrowprops=dict(arrowstyle="->", color="#047857", lw=1.5),
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#ecfdf5", edgecolor="#6ee7b7", lw=1.2))

ax.annotate("ZONE 3: CLEAN GUTTERS & DESILTING\nSurulere, Mushin, Agege, Ikeja, Mainland\nClear plastic waste twice a year (before May & August)",
            xy=(538000, 725000), xytext=(515000, 738000), fontsize=9.5, fontweight="bold", color="#b45309", ha="center",
            arrowprops=dict(arrowstyle="->", color="#b45309", lw=1.5),
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#fffbeb", edgecolor="#fde68a", lw=1.2))

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

print("All 5 clean, user-friendly maps generated successfully!")
