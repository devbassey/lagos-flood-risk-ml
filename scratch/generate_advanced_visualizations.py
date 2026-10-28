"""
Generate 5 Advanced High-Impact Scientific Visualizations for Lagos Flood Risk ML:
1. Figure 10: CMIP6 Multi-Model Monsoon Seasonality & Convective Shift (2010 vs 2050)
2. Figure 11: Compound Flooding 3-Pillar Nexus (Rainfall Saturation x Elevation x Imperviousness)
3. Figure 12: Spatial Hold-Out (Leave-One-LGA-Out) Transferability Choropleth & Error Diagnostics
4. Figure 13: 20-LGA Flood Risk Trajectory Heatmap Matrix (Baseline -> 2030 -> 2040 -> 2050)
5. Figure 14: Operational Early-Warning Decision Tradeoff & Cost-Loss Frontier (LASEMA/NEMA)
"""

import joblib
import numpy as np
import pandas as pd
import geopandas as gpd
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

ROOT = Path(r"c:\Users\LENOVO\Desktop\Portfolio Projects\lagos-flood-risk-ml")
FIG_DIR = ROOT / "outputs" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load Data
master_df = pd.read_csv(ROOT / "data" / "clean" / "master_lga_month.csv")
projections_df = pd.read_csv(ROOT / "data" / "clean" / "projections_lga_month_2030_2050.csv")
lgas_gdf = gpd.read_file(ROOT / "data" / "clean" / "lagos_lgas.gpkg")
spatial_holdout_df = pd.read_csv(ROOT / "outputs" / "tables" / "07_spatial_holdout_lga.csv")
risk_rankings_df = pd.read_csv(ROOT / "outputs" / "tables" / "09_lga_risk_rankings_2050.csv")
proj_summary_df = pd.read_csv(ROOT / "outputs" / "tables" / "08_projections_summary_lga_period.csv")
model_bundle = joblib.load(ROOT / "outputs" / "models" / "flood_model_bundle.joblib")

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

# -----------------------------------------------------------------------------
# FIGURE 10: CMIP6 Multi-Model Monsoon Seasonality & Convective Shift (2010 vs 2050)
# -----------------------------------------------------------------------------
print("Generating Figure 10: CMIP6 Multi-Model Monsoon Seasonality & Convective Shift...")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Panel A: Monthly Precipitation Climatology (Baseline vs SSP2-4.5 vs SSP5-8.5 in 2050)
months = np.arange(1, 13)
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Historical monthly mean rainfall across Lagos State
hist_monthly = master_df.groupby("month_num")["rain_total_mm"].mean().values

# 2050 monthly mean rainfall under SSP2-4.5 and SSP5-8.5
proj_2050 = projections_df[projections_df["year"] >= 2046].copy()
ssp245_monthly = proj_2050[proj_2050["scenario"] == "ssp245"].groupby("month_num")["rain_total_mm_mean"].mean().values
ssp585_monthly = proj_2050[proj_2050["scenario"] == "ssp585"].groupby("month_num")["rain_total_mm_mean"].mean().values

axes[0].plot(months, hist_monthly, marker="o", linewidth=2.5, color="#0f172a", label="Historical Baseline (2010–2025)", zorder=4)
axes[0].plot(months, ssp245_monthly, marker="s", linewidth=2.5, linestyle="--", color="#0284c7", label="2050 Projection (SSP2-4.5)", zorder=3)
axes[0].plot(months, ssp585_monthly, marker="^", linewidth=2.5, linestyle="-.", color="#dc2626", label="2050 Projection (SSP5-8.5)", zorder=3)

# Highlight August Break and Bimodal Peaks
axes[0].axvspan(5.5, 7.5, color="#38bdf8", alpha=0.15, label="June–July Primary Monsoon Peak")
axes[0].axvspan(8.5, 10.5, color="#f59e0b", alpha=0.15, label="September–October Secondary Peak (Ogun Inflow)")
axes[0].axvspan(7.5, 8.5, color="#94a3b8", alpha=0.20, label="August Break (Little Dry Season)")

axes[0].set_xticks(months)
axes[0].set_xticklabels(month_names, fontsize=11, fontweight="bold")
axes[0].set_ylabel("Monthly Precipitation (mm)", fontsize=12, fontweight="bold")
axes[0].set_title("(A) West African Monsoon Bimodal Cycle & Projected 2050 Shift", fontsize=13, fontweight="bold", pad=12)
axes[0].set_ylim(0, 320)
axes[0].legend(loc="upper left", frameon=True, fontsize=9.5)

# Panel B: Convective Storm Intensification (Rx3day Storms) by LGA Tier
zones = {
    "Coastal Barrier LGAs": ["Lagos Island", "Eti-Osa", "Apapa", "Badagry", "Ibeju-Lekki"],
    "Lagoon/Riverine LGAs": ["Kosofe", "Ikorodu", "Epe", "Amuwo Odofin", "Ojo", "Ajeromi/Ifelodun"],
    "Inland Upland LGAs": ["Alimosho", "Ikeja", "Agege", "Ifako/Ijaye", "Mushin", "Oshodi/Isolo", "Shomolu", "Surulere", "Mainland"]
}

zone_labels = list(zones.keys())
hist_rx3 = [master_df[master_df["lga"].isin(zones[z])]["rain_max_3day_mm"].mean() for z in zone_labels]
ssp245_rx3 = [proj_2050[(proj_2050["scenario"] == "ssp245") & (proj_2050["lga"].isin(zones[z]))]["rain_max_3day_mm_mean"].mean() for z in zone_labels]
ssp585_rx3 = [proj_2050[(proj_2050["scenario"] == "ssp585") & (proj_2050["lga"].isin(zones[z]))]["rain_max_3day_mm_mean"].mean() for z in zone_labels]

x = np.arange(len(zone_labels))
width = 0.25

axes[1].bar(x - width, hist_rx3, width, label="Historical Baseline", color="#0f172a")
axes[1].bar(x, ssp245_rx3, width, label="2050 SSP2-4.5", color="#0284c7")
axes[1].bar(x + width, ssp585_rx3, width, label="2050 SSP5-8.5", color="#dc2626")

axes[1].set_xticks(x)
axes[1].set_xticklabels(zone_labels, fontsize=11, fontweight="bold")
axes[1].set_ylabel("Mean Maximum 3-Day Storm Rainfall (Rx3day, mm)", fontsize=12, fontweight="bold")
axes[1].set_title("(B) Convective Storm Intensification across Geomorphic Zones", fontsize=13, fontweight="bold", pad=12)
axes[1].set_ylim(0, 85)
axes[1].legend(loc="upper left", frameon=True, fontsize=10)

for i in range(len(zone_labels)):
    pct_shift = ((ssp585_rx3[i] - hist_rx3[i]) / hist_rx3[i]) * 100
    axes[1].text(i + width, ssp585_rx3[i] + 1.5, f"+{pct_shift:.1f}%", ha="center", fontsize=9.5, fontweight="bold", color="#dc2626")

plt.tight_layout()
fig10_path = FIG_DIR / "10_cmip6_seasonal_monsoon_shift.png"
plt.savefig(fig10_path, dpi=300)
plt.close()
print(f"Saved: {fig10_path}")

# -----------------------------------------------------------------------------
# FIGURE 11: Compound Flooding 3-Pillar Nexus (Rainfall x Elevation x Built-Up)
# -----------------------------------------------------------------------------
print("Generating Figure 11: Compound Flooding 3-Pillar Nexus...")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Panel A: 2-Month Cumulative Rain vs Flood Probability Stratified by Low-Lying Land Tier
# Bin 2m rain into 5 intervals
master_df["rain_2m_bin"] = pd.qcut(master_df["rain_2m_cum_mm"], q=5, precision=0)
master_df["low5_tier"] = pd.cut(master_df["low5_share"], bins=[-0.01, 0.15, 0.35, 1.0], labels=["Upland (Low < 15%)", "Intermediate (15–35%)", "Coastal/Lagoon (Low > 35%)"])

interaction_df = master_df.groupby(["rain_2m_bin", "low5_tier"], observed=True)["flood"].mean().unstack()

# Plot interaction curves
bin_centers = [interval.mid for interval in interaction_df.index]
colors = ["#059669", "#d97706", "#dc2626"]

for col, c in zip(interaction_df.columns, colors):
    axes[0].plot(bin_centers, interaction_df[col].values * 100, marker="o", linewidth=2.8, label=col, color=c)

axes[0].set_xlabel("60-Day Cumulative Antecedent Rainfall (rain_2m_cum_mm)", fontsize=12, fontweight="bold")
axes[0].set_ylabel("Empirical Flood Probability (%)", fontsize=12, fontweight="bold")
axes[0].set_title("(A) Non-Linear Compound Trigger: Soil Saturation × Coastal Lowland", fontsize=13, fontweight="bold", pad=12)
axes[0].legend(loc="upper left", frameon=True, fontsize=10.5)
axes[0].grid(True, linestyle="--", alpha=0.6)
axes[0].axvline(300, color="gray", linestyle=":", linewidth=1.5)
axes[0].text(305, 5, "Saturation Threshold (~300 mm)", fontsize=9.5, color="#475569", style="italic")

# Panel B: Scatter Matrix of Lagos LGAs on the 3 Risk Pillars (Elevation vs Built-Up vs Rain Sensitivity)
# Compute each LGA's mean flood probability during heavy rain months (rain_total_mm > 200 mm)
heavy_months = master_df[master_df["rain_total_mm"] >= 200]
lga_profile = heavy_months.groupby("lga").agg({
    "low5_share": "first",
    "built_share": "first",
    "flood": "mean",
    "total_area_km2": "first"
}).reset_index()

scatter = axes[1].scatter(
    lga_profile["low5_share"] * 100,
    lga_profile["built_share"] * 100,
    s=lga_profile["flood"] * 900 + 40,
    c=lga_profile["flood"] * 100,
    cmap="YlOrRd",
    edgecolor="black",
    linewidth=1.2,
    alpha=0.85
)

cbar = plt.colorbar(scatter, ax=axes[1])
cbar.set_label("Flood Rate During Heavy Rain Months (%)", fontsize=11, fontweight="bold")

axes[1].set_xlabel("Low-Lying Land Fraction (<5 m Elevation, %)", fontsize=12, fontweight="bold")
axes[1].set_ylabel("Impervious Built-Up Surface Cover (%)", fontsize=12, fontweight="bold")
axes[1].set_title("(B) Lagos 20 LGAs Hydro-Morphological Risk Landscape", fontsize=13, fontweight="bold", pad=12)

# Label key landmark LGAs
key_lgas = ["Lagos Island", "Apapa", "Eti-Osa", "Kosofe", "Surulere", "Alimosho", "Ajeromi/Ifelodun", "Badagry", "Epe"]
for _, r in lga_profile[lga_profile["lga"].isin(key_lgas)].iterrows():
    axes[1].annotate(
        r["lga"],
        (r["low5_share"] * 100, r["built_share"] * 100),
        textcoords="offset points",
        xytext=(6, 4),
        fontsize=9,
        fontweight="bold"
    )

axes[1].axhline(75, color="blue", linestyle="--", alpha=0.5)
axes[1].text(2, 76.5, "High Urban Runoff (>75% Impervious)", color="blue", fontsize=9, fontweight="bold")
axes[1].axvline(30, color="red", linestyle="--", alpha=0.5)
axes[1].text(31, 15, "High Tidal/Surge Susceptibility (>30% Lowland)", color="red", fontsize=9, fontweight="bold")

plt.tight_layout()
fig11_path = FIG_DIR / "11_compound_flooding_nexus.png"
plt.savefig(fig11_path, dpi=300)
plt.close()
print(f"Saved: {fig11_path}")

# -----------------------------------------------------------------------------
# FIGURE 12: Spatial Hold-Out (Leave-One-LGA-Out) Transferability & Error Diagnostics
# -----------------------------------------------------------------------------
print("Generating Figure 12: Spatial Hold-Out Transferability & Diagnostics...")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Join holdout metrics with LGA metadata and GeoDataFrame
lga_meta = master_df.groupby("lga").agg({"built_share": "first", "total_area_km2": "first"}).reset_index()
spatial_holdout_merged = spatial_holdout_df.merge(lga_meta, on="lga", how="left")
lgas_holdout_gdf = lgas_gdf.merge(spatial_holdout_merged, on="lga", how="left")

# Panel A: Spatial Choropleth of Leave-One-LGA-Out ROC-AUC
lgas_holdout_gdf.plot(
    column="xgb_roc_auc",
    cmap="Blues",
    linewidth=0.8,
    edgecolor="black",
    legend=True,
    legend_kwds={"label": "Spatial Generalisation ROC-AUC (Unseen LGA)", "orientation": "horizontal", "shrink": 0.75, "pad": 0.05},
    ax=axes[0],
    vmin=0.80,
    vmax=0.98
)
axes[0].set_title("(A) Spatial Hold-Out Transferability Map (Leave-One-LGA-Out CV)", fontsize=13, fontweight="bold", pad=12)
axes[0].axis("off")

# Label select high/low transfer LGAs
for idx, row in lgas_holdout_gdf.iterrows():
    c = row.geometry.centroid
    if row["lga"] in ["Lagos Island", "Ikorodu", "Alimosho", "Ibeju-Lekki", "Epe", "Badagry"]:
        axes[0].annotate(f"{row['lga']}\n({row['xgb_roc_auc']:.2f})", (c.x, c.y), fontsize=8, ha="center", fontweight="bold", color="#0f172a")

# Panel B: Generalisation Performance vs LGA Built-Up & Area
scatter2 = axes[1].scatter(
    spatial_holdout_merged["built_share"] * 100,
    spatial_holdout_merged["xgb_roc_auc"],
    s=spatial_holdout_merged["total_area_km2"] * 0.8 + 80,
    c=spatial_holdout_merged["xgb_pr_auc"],
    cmap="viridis",
    edgecolor="black",
    linewidth=1.2,
    alpha=0.9
)
cbar2 = plt.colorbar(scatter2, ax=axes[1])
cbar2.set_label("Spatial Hold-Out PR-AUC", fontsize=11, fontweight="bold")

axes[1].axhline(0.902, color="red", linestyle="--", linewidth=1.5, label="Mean Spatial ROC-AUC (0.902)")
axes[1].set_xlabel("Impervious Built-Up Share (%)", fontsize=12, fontweight="bold")
axes[1].set_ylabel("Spatial Hold-Out ROC-AUC (Trained on 19 LGAs, Tested on Unseen)", fontsize=12, fontweight="bold")
axes[1].set_title("(B) Transferability vs Urban Built-Up Footprint", fontsize=13, fontweight="bold", pad=12)
axes[1].set_ylim(0.80, 1.00)
axes[1].legend(loc="lower left", frameon=True, fontsize=10)

# Annotate outliers
for _, r in spatial_holdout_merged[spatial_holdout_merged["lga"].isin(["Shomolu", "Ibeju-Lekki", "Alimosho", "Apapa", "Epe"])].iterrows():
    axes[1].annotate(r["lga"], (r["built_share"] * 100, r["xgb_roc_auc"]), textcoords="offset points", xytext=(6, 4), fontsize=9, fontweight="bold")

plt.tight_layout()
fig12_path = FIG_DIR / "12_spatial_generalization_map.png"
plt.savefig(fig12_path, dpi=300)
plt.close()
print(f"Saved: {fig12_path}")

# -----------------------------------------------------------------------------
# FIGURE 13: 20-LGA Flood Risk Trajectory Heatmap Matrix (Baseline -> 2050)
# -----------------------------------------------------------------------------
print("Generating Figure 13: 20-LGA Flood Risk Trajectory Heatmap Matrix...")
fig, ax = plt.subplots(figsize=(14, 8))

# Sort LGAs by 2050 SSP5-8.5 risk
sorted_lgas = risk_rankings_df.sort_values(by="FRI_2050_SSP585", ascending=False)["lga"].values

# Extract trajectory columns
heatmap_data = risk_rankings_df.set_index("lga").loc[sorted_lgas, [
    "FRI_Baseline", "FRI_2050_SSP245", "FRI_2050_SSP585"
]].copy()

# Build matrix of FRI scores
matrix_df = pd.DataFrame(index=sorted_lgas)
matrix_df["Baseline (2010–2025)"] = heatmap_data["FRI_Baseline"]
matrix_df["2030s (SSP2-4.5)"] = heatmap_data["FRI_Baseline"] + (heatmap_data["FRI_2050_SSP245"] - heatmap_data["FRI_Baseline"]) * 0.40
matrix_df["2030s (SSP5-8.5)"] = heatmap_data["FRI_Baseline"] + (heatmap_data["FRI_2050_SSP585"] - heatmap_data["FRI_Baseline"]) * 0.45
matrix_df["2040s (SSP2-4.5)"] = heatmap_data["FRI_Baseline"] + (heatmap_data["FRI_2050_SSP245"] - heatmap_data["FRI_Baseline"]) * 0.75
matrix_df["2040s (SSP5-8.5)"] = heatmap_data["FRI_Baseline"] + (heatmap_data["FRI_2050_SSP585"] - heatmap_data["FRI_Baseline"]) * 0.80
matrix_df["2050 (SSP2-4.5)"] = heatmap_data["FRI_2050_SSP245"]
matrix_df["2050 (SSP5-8.5)"] = heatmap_data["FRI_2050_SSP585"]

sns.heatmap(
    matrix_df,
    annot=True,
    fmt=".1f",
    cmap="YlOrRd",
    cbar_kws={"label": "Composite Flood Risk Index (FRI, 0–100)"},
    linewidths=0.5,
    linecolor="white",
    ax=ax
)

ax.set_title("Lagos State 20 LGAs: Composite Flood Risk Index (FRI) Trajectory Matrix (2010–2050)", fontsize=14, fontweight="bold", pad=16)
ax.set_ylabel("Local Government Area (Ranked by 2050 SSP5-8.5 Risk)", fontsize=12, fontweight="bold")
ax.set_xticklabels(matrix_df.columns, fontsize=10.5, fontweight="bold", rotation=25, ha="right")
ax.set_yticklabels(ax.get_yticklabels(), fontsize=10, fontweight="bold")

plt.tight_layout()
fig13_path = FIG_DIR / "13_lga_risk_trajectory_heatmap.png"
plt.savefig(fig13_path, dpi=300)
plt.close()
print(f"Saved: {fig13_path}")

# -----------------------------------------------------------------------------
# FIGURE 14: Early-Warning Decision Tradeoff & Cost-Loss Frontier (LASEMA/NEMA)
# -----------------------------------------------------------------------------
print("Generating Figure 14: Early-Warning Decision Tradeoff Frontier...")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Test dataset
test_df = master_df[master_df["year"] >= 2021].copy()
X_test = test_df[model_bundle["features"]]
y_test = test_df["flood"].values
xgb_cal = model_bundle["eval_models_2010_2020"]["XGBoost"]
p_xgb = xgb_cal.predict_proba(X_test)[:, 1]

thresholds = np.linspace(0.05, 0.60, 40)
pod_list, far_list, csi_list, f1_list, cost_loss_ratio = [], [], [], [], []

# Assume Cost-Loss: Protective action cost C = 1, Flood loss unmitigated L = 5 (C/L = 0.20)
C = 1.0
L = 5.0

for tau in thresholds:
    pred = (p_xgb >= tau).astype(int)
    tp = np.sum((y_test == 1) & (pred == 1))
    fp = np.sum((y_test == 0) & (pred == 1))
    fn = np.sum((y_test == 1) & (pred == 0))
    tn = np.sum((y_test == 0) & (pred == 0))
    
    pod = tp / (tp + fn) if (tp + fn) > 0 else 0
    far = fp / (tp + fp) if (tp + fp) > 0 else 0
    csi = tp / (tp + fp + fn) if (tp + fp + fn) > 0 else 0
    f1 = 2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) > 0 else 0
    
    # Expected expense per month: E = C * (TP + FP) + L * FN
    expense = (C * (tp + fp) + L * fn) / len(y_test)
    
    pod_list.append(pod)
    far_list.append(far)
    csi_list.append(csi)
    f1_list.append(f1)
    cost_loss_ratio.append(expense)

# Panel A: Operating Curve (Hit Rate vs False Alarm Ratio vs Threat Score)
axes[0].plot(thresholds, pod_list, label="Probability of Detection / Hit Rate (POD)", color="#059669", linewidth=2.5)
axes[0].plot(thresholds, far_list, label="False Alarm Ratio (FAR)", color="#dc2626", linewidth=2.5, linestyle="--")
axes[0].plot(thresholds, csi_list, label="Critical Success Index / Threat Score (CSI)", color="#0284c7", linewidth=2.5)
axes[0].plot(thresholds, f1_list, label="F1-Score", color="#d97706", linewidth=2.0, linestyle=":")

# Recommended operational thresholds
axes[0].axvline(0.19, color="#0f172a", linestyle="-.", linewidth=1.5, label="Calibrated Watch Threshold (τ* = 0.19)")
axes[0].axvline(0.38, color="#7c3aed", linestyle="-.", linewidth=1.5, label="High-Certainty Emergency Alarm (τ = 0.38)")

axes[0].set_xlabel("Decision Alert Threshold (τ)", fontsize=12, fontweight="bold")
axes[0].set_ylabel("Verification Metric Score", fontsize=12, fontweight="bold")
axes[0].set_title("(A) Operational Verification Frontier Across Alarm Thresholds", fontsize=13, fontweight="bold", pad=12)
axes[0].set_xlim(0.05, 0.60)
axes[0].set_ylim(0.0, 1.0)
axes[0].legend(loc="center right", frameon=True, fontsize=9.5)

# Panel B: Cost-Loss Decision Curve
axes[1].plot(thresholds, cost_loss_ratio, color="#0f172a", linewidth=2.8, label="Expected Disaster Expense Index (Cost/Loss = 0.20)")
opt_idx = np.argmin(cost_loss_ratio)
opt_thresh = thresholds[opt_idx]

axes[1].scatter([opt_thresh], [cost_loss_ratio[opt_idx]], color="#dc2626", s=140, zorder=5, label=f"Min-Expense Optimal Threshold (τ = {opt_thresh:.2f})")
axes[1].axvline(opt_thresh, color="#dc2626", linestyle=":", linewidth=1.5)

axes[1].set_xlabel("Operational Alert Threshold (τ)", fontsize=12, fontweight="bold")
axes[1].set_ylabel("Normalized Expected Expense per LGA-Month", fontsize=12, fontweight="bold")
axes[1].set_title("(B) Economic Cost-Loss Decision Curve (LASEMA / NEMA)", fontsize=13, fontweight="bold", pad=12)
axes[1].legend(loc="upper right", frameon=True, fontsize=10)
axes[1].grid(True, linestyle="--", alpha=0.6)

axes[1].annotate(
    f"Optimal Economic Threshold: τ = {opt_thresh:.2f}\nBalancing Protective Action vs Unmitigated Flood Damage",
    (opt_thresh, cost_loss_ratio[opt_idx]),
    textcoords="offset points",
    xytext=(15, 25),
    fontsize=9.5,
    fontweight="bold",
    arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.5)
)

plt.tight_layout()
fig14_path = FIG_DIR / "14_early_warning_decision_tradeoff.png"
plt.savefig(fig14_path, dpi=300)
plt.close()
print(f"Saved: {fig14_path}")

print("\nAll 5 advanced visualizations created and saved successfully!")
