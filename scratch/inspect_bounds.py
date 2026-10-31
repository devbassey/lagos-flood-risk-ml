import geopandas as gpd
from pathlib import Path

gdf = gpd.read_file('data/clean/lagos_lgas.gpkg').to_crs(epsg=32631)
print("Bounds:", gdf.total_bounds)
for idx, row in gdf.iterrows():
    c = row.geometry.centroid
    print(f"{row['lga']}: centroid ({c.x:.0f}, {c.y:.0f}), area={row.geometry.area/1e6:.1f} km2")
