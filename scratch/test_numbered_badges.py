"""
Test script to verify clean numbered badges on the urban core and clear legend matching.
Numbered LGAs (1 to 10):
1. Agege
2. Ikeja
3. Oshodi/Isolo
4. Mushin
5. Shomolu
6. Surulere
7. Mainland
8. Ajeromi/Ifelodun
9. Apapa
10. Lagos Island
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
URBAN_DICT = dict(URBAN_CORE)

# Fine-tuned centroid positions for perfect badge separation
# (dx, dy) adjustments in meters to prevent any visual overlap
BADGE_OFFSETS = {
    "Agege": (0, 0),
    "Ikeja": (800, 0),
    "Oshodi/Isolo": (-800, 400),
    "Mushin": (0, 0),
    "Shomolu": (600, 200),
    "Surulere": (-400, 0),
    "Mainland": (800, 0),
    "Ajeromi/Ifelodun": (-800, 0),
    "Apapa": (400, -400),
    "Lagos Island": (0, 0),
}

# The remaining 10 spacious LGAs that have full text names directly on map
SPACIOUS_LGAS = [
    ("Badagry", 490298, 712859),
    ("Ojo", 516155, 712500),
    ("Amuwo Odofin", 526000, 710000),
    ("Alimosho", 527167, 731000),
    ("Ifako/Ijaye", 533599, 738500),
    ("Kosofe", 547000, 731000),
    ("Ikorodu", 565000, 734000),
    ("Eti-Osa", 562000, 711000),
    ("Ibeju-Lekki", 595736, 712500),
    ("Epe", 605000, 727000),
]

def plot_numbered_badges_and_labels(ax, lga_df):
    """Plots numbered badges 1-10 on small LGAs, and clean white-haloed names on spacious LGAs."""
    halo = [pe.withStroke(linewidth=3, foreground="white")]
    
    # 1. Plot names for spacious LGAs
    for name, x, y in SPACIOUS_LGAS:
        ax.text(x, y, name, fontsize=9.5, fontweight="bold", color="#1e293b",
                ha="center", va="center", path_effects=halo, zorder=5)
        
    # 2. Plot numbered circle badges for the 10 small LGAs
    for name, num in URBAN_CORE:
        row = lga_df[lga_df["lga"] == name].iloc[0]
        c = row.geometry.centroid
        offset = BADGE_OFFSETS.get(name, (0, 0))
        bx = c.x + offset[0]
        by = c.y + offset[1]
        
        # Badge circle: crisp white circle with dark slate border and shadow effect
        circle = plt.Circle((bx, by), 1400, facecolor="#ffffff", edgecolor="#0f172a", linewidth=1.5, zorder=8)
        ax.add_patch(circle)
        
        # Number inside badge
        ax.text(bx, by, str(num), fontsize=8.5, fontweight="bold", color="#0f172a",
                ha="center", va="center", zorder=9)

print("Setup completed successfully.")
