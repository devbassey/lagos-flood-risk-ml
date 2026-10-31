"""
Test Redesign of Map 03: Concrete Jungle vs Nature's Sponge.
Fixes:
1. Vertical Stack (2, 1) layout matching Lagos State's 5:1 aspect ratio perfectly.
2. Zero label clutter on map: clean polygons, subtle haloed text for major regions.
3. Clean Callout bracket for the Urban Core.
4. Rich, beautiful Layman Cards below each map showing Top 5 rankings in plain English.
5. Large, legible, high-contrast typography.
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

# Load data
lgas_gdf = gpd.read_file(ROOT / "data" / "clean" / "lagos_lgas.gpkg")
master_df = pd.read_csv(ROOT / "data" / "clean" / "master_lga_month.csv")
risk_df = pd.read_csv(ROOT / "outputs" / "tables" / "09_lga_risk_rankings_2050.csv")

lga_stats = master_df.groupby("lga").agg({
    "built_share": "first",
    "wetland_mangrove_share": "first",
}).reset_index()

lga_stats["built_pct"] = lga_stats["built_share"] * 100
lga_stats["mangrove_pct"] = lga_stats["wetland_mangrove_share"] * 100

lga_full = lgas_gdf.merge(lga_stats, on="lga", how="left").merge(risk_df, on="lga", how="left")
lga_proj = lga_full.to_crs(epsg=32631)

# Sort rankings for layman cards
top_built = lga_proj.sort_values("built_pct", ascending=False).head(5)
top_nature = lga_proj.sort_values("mangrove_pct", ascending=False).head(5)

# Create 2-row vertical layout: figsize=(17, 13)
fig = plt.figure(figsize=(17, 13))

# Layout grid:
# Top header: y = 0.94 to 0.99
# Subplot 1 (Map A - Built): y = 0.54 to 0.90
# Subplot 2 (Map B - Nature): y = 0.14 to 0.50
# Bottom layman banner: y = 0.02 to 0.11

gs = fig.add_gridspec(2, 1, height_ratios=[1, 1], top=0.91, bottom=0.13, left=0.04, right=0.96, hspace=0.32)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

fig.suptitle(
    "Concrete Jungle vs. Nature's Sponge: City Pavement vs. Mangrove Buffers",
    fontsize=18, fontweight="bold", y=0.97, color="#0f172a"
)
fig.text(
    0.5, 0.935,
    "How paving over nature causes flooding: Rain cannot soak into concrete (Red), while natural wetlands (Green) act as protective flood sponges.",
    fontsize=12, ha="center", color="#475569"
)

def add_clean_compass(ax):
    ax.annotate('N', xy=(0.97, 0.88), xytext=(0.97, 0.74),
                xycoords='axes fraction', textcoords='axes fraction',
                ha='center', va='bottom', fontsize=12, fontweight='bold', color="#0f172a",
                arrowprops=dict(facecolor='#0f172a', edgecolor='#0f172a', width=2, headwidth=6))

def plot_clean_major_labels(ax):
    """Labels only the large spacious anchor regions with subtle white-stroked text."""
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

# -----------------------------------------------------------------------------
# Panel A: Built-Up Pavement Footprint
# -----------------------------------------------------------------------------
divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("bottom", size="4%", pad=0.25)
lga_proj.plot(
    column="built_pct",
    cmap="OrRd",
    edgecolor="#334155",
    linewidth=0.9,
    legend=True,
    cax=cax1,
    legend_kwds={"label": "Impervious Concrete & Pavement Cover (% of Land Area): Yellow = Low Pavement (<40%)  |  Dark Red = Extreme Concrete Jungle (>90%)", "orientation": "horizontal"},
    ax=ax1,
    vmin=0,
    vmax=100
)
ax1.set_title("(A) Concrete Jungle: Paved Roads, Buildings & Roofs (Zero Infiltration)", fontsize=13, fontweight="bold", pad=8, color="#0f172a", loc="left")
ax1.axis("off")
add_clean_compass(ax1)
plot_clean_major_labels(ax1)

# Point to urban core with a clean pointer line and callout box
ax1.annotate(
    "DENSE URBAN CORE\n(Surulere, Mushin, Ajeromi, Agege)\n95% to 98% Concrete Pavement",
    xy=(538000, 720000), xytext=(538000, 706000),
    fontsize=9.5, fontweight="bold", color="#7f1d1d", ha="center",
    arrowprops=dict(arrowstyle="->", color="#7f1d1d", lw=1.5),
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#fef2f2", edgecolor="#f87171", lw=1.2)
)

# Overlay Top 5 ranking card on the top right
card1_text = (
    "TOP 5 CONCRETE JUNGLES (Highest Runoff Risk):\n"
    " 1. Surulere: 98.3% Paved (Zero Absorption)\n"
    " 2. Ajeromi/Ifelodun: 97.4% Paved\n"
    " 3. Mushin: 96.9% Paved\n"
    " 4. Agege: 95.8% Paved\n"
    " 5. Lagos Mainland: 95.2% Paved\n"
    " -> 100% of rainwater immediately rushes into streets!"
)
ax1.text(
    0.02, 0.88, card1_text, transform=ax1.transAxes,
    fontsize=8.5, va="top", ha="left", color="#7f1d1d", fontweight="medium",
    bbox=dict(boxstyle="round,pad=0.5", facecolor="#fff1f2", edgecolor="#fca5a5", lw=1.1)
)

# -----------------------------------------------------------------------------
# Panel B: Wetland and Mangrove Protective Natural Retention Buffers
# -----------------------------------------------------------------------------
divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes("bottom", size="4%", pad=0.25)
lga_proj.plot(
    column="mangrove_pct",
    cmap="YlGn",
    edgecolor="#334155",
    linewidth=0.9,
    legend=True,
    cax=cax2,
    legend_kwds={"label": "Natural Wetland & Mangrove Retention Buffer (% of Land Area): Cream = <2% Wetlands  |  Dark Green = Strong Natural Sponge (>15%)", "orientation": "horizontal"},
    ax=ax2,
    vmin=0,
    vmax=28
)
ax2.set_title("(B) Nature's Sponge: Surviving Wetlands & Mangrove Forests (Natural Water Storage)", fontsize=13, fontweight="bold", pad=8, color="#0f172a", loc="left")
ax2.axis("off")
add_clean_compass(ax2)
plot_clean_major_labels(ax2)

# Point to Kosofe and Lagos Island wetlands
ax2.annotate(
    "KEY NATURAL SPONGES\nKosofe (18.0%) & Lagos Island (25.3%)\nCrucial floodwater buffer zones",
    xy=(546000, 725000), xytext=(546000, 706000),
    fontsize=9.5, fontweight="bold", color="#14532d", ha="center",
    arrowprops=dict(arrowstyle="->", color="#14532d", lw=1.5),
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#f0fdf4", edgecolor="#4ade80", lw=1.2)
)

card2_text = (
    "TOP 5 NATURAL SPONGE BUFFERS:\n"
    " 1. Lagos Island: 25.3% Wetlands & Mangroves\n"
    " 2. Kosofe: 18.0% Wetlands (Ogun River buffer)\n"
    " 3. Amuwo Odofin: 17.9% Wetlands\n"
    " 4. Ojo: 15.6% Mangroves\n"
    " 5. Badagry: 10.9% Wetlands\n"
    " -> Absorbs millions of litres of floodwater naturally!"
)
ax2.text(
    0.02, 0.88, card2_text, transform=ax2.transAxes,
    fontsize=8.5, va="top", ha="left", color="#14532d", fontweight="medium",
    bbox=dict(boxstyle="round,pad=0.5", facecolor="#f0fdf4", edgecolor="#86efac", lw=1.1)
)

# -----------------------------------------------------------------------------
# Bottom Layman Infographic Cards
# -----------------------------------------------------------------------------
card_w = 0.29
ys = 0.05
xs = [0.04, 0.355, 0.67]

points = [
    ("[THE CONCRETE JUNGLE] Zero Ground Infiltration",
     "In core mainland LGAs (Surulere, Mushin, Ajeromi, Agege), over 95% of land is covered\nby concrete and roofs. Rain cannot soak into the ground, creating instant flash floods."),
    ("[NATURE'S SPONGE] Protecting Natural Floodwaters",
     "Wetlands and mangroves act like gigantic natural sponges. Where they survive (Kosofe,\nAmuwo Odofin, Badagry), they soak up excess water and prevent severe neighborhood damage."),
    ("[KEY TAKEAWAY] Nature is Cheaper than Concrete",
     "Every square metre of wetland reclaimed by sand-filling increases flood risks downstream.\nEnforcing wetland conservation and permeable paving is Lagos's most cost-effective defense.")
]

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

test_path = FIG_DIR / "map_03_landcover_mangrove_buffers.png"
plt.savefig(str(test_path), dpi=300)
plt.close()
print("Saved redesigned Map 03 successfully!")
