"""
Streamlit Dashboard: Spatio-Temporal Flood Risk Explorer for Lagos State (2010–2050)
Run with:
    streamlit run app.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Lagos Flood Risk ML Explorer (2010–2050)",
    page_icon="🌊",
    layout="wide",
)

ROOT = Path(__file__).parent
FRI_PATH = ROOT / "data/clean/flood_risk_index_lga.csv"
MASTER_PATH = ROOT / "data/clean/master_lga_month.csv"
PROJ_MONTHLY_PATH = ROOT / "data/clean/projections_lga_month_2030_2050.csv"
MODEL_COMP_PATH = ROOT / "outputs/tables/07_model_comparison_test.csv"
MAP_HTML_PATH = ROOT / "outputs/maps/lagos_flood_risk_interactive.html"

@st.cache_data
def load_data():
    fri = pd.read_csv(FRI_PATH)
    master = pd.read_csv(MASTER_PATH, parse_dates=["month"])
    proj_m = pd.read_csv(PROJ_MONTHLY_PATH, parse_dates=["month"])
    model_comp = pd.read_csv(MODEL_COMP_PATH)
    return fri, master, proj_m, model_comp

fri_df, master_df, proj_m_df, model_comp_df = load_data()

st.title("🌊 Lagos State Flood Risk & Climate Projection Dashboard (2010–2050)")
st.markdown(
    "**Spatio-Temporal Machine Learning Prediction of Pluvial and Coastal Flood Risk across all 20 Lagos State LGAs**  \n"
    "*Powered by CHIRPS Rainfall, SRTM Elevation, JRC Surface Water, ESA WorldCover, WorldPop, Calibrated Monotonic XGBoost, and 5-Model CMIP6 Projections (SSP2-4.5 & SSP5-8.5).*"
)

# Sidebar controls
st.sidebar.header("🔎 Scenario & Time Controls")
period_options = [
    ("Historical", "Baseline (2010-2025)", "Historical Baseline (2010–2025)"),
    ("ssp245", "2030s (2030-2039)", "2030s (2030–2039) · SSP2-4.5 (Moderate)"),
    ("ssp245", "2040s (2040-2049)", "2040s (2040–2049) · SSP2-4.5 (Moderate)"),
    ("ssp245", "2050 (2046-2050)", "2050 (2046–2050) · SSP2-4.5 (Moderate)"),
    ("ssp585", "2030s (2030-2039)", "2030s (2030–2039) · SSP5-8.5 (High Emissions)"),
    ("ssp585", "2040s (2040-2049)", "2040s (2040–2049) · SSP5-8.5 (High Emissions)"),
    ("ssp585", "2050 (2046-2050)", "2050 (2046–2050) · SSP5-8.5 (High Emissions)"),
]
selected_label = st.sidebar.selectbox(
    "Select Climate Scenario & Period",
    [p[2] for p in period_options],
    index=6,
)
sel_scen, sel_period = [(p[0], p[1]) for p in period_options if p[2] == selected_label][0]

lga_list = sorted(fri_df["lga"].unique())
selected_lga = st.sidebar.selectbox("Select LGA for Deep-Dive Profile", lga_list, index=lga_list.index("Eti-Osa"))

sub_fri = fri_df[(fri_df["scenario"] == sel_scen) & (fri_df["period"] == sel_period)].sort_values("lga_rank")
lga_row = sub_fri[sub_fri["lga"] == selected_lga].iloc[0]

# Top KPI row
col1, col2, col3, col4 = st.columns(4)
col1.metric(
    "State Mean Flood Risk Index (FRI)",
    f"{sub_fri['fri_score'].mean():.1f} / 100",
    f"{sub_fri['fri_score'].mean() - fri_df[fri_df['period']=='Baseline (2010-2025)']['fri_score'].mean():+.1f} vs Baseline",
)
col2.metric(
    "State Mean Wet-Season Flood Prob",
    f"{sub_fri['wet_season_prob_pct'].mean():.1f}%",
    f"Range: {sub_fri['wet_season_min_pct'].mean():.1f}%–{sub_fri['wet_season_max_pct'].mean():.1f}%",
)
base_exp_pop = fri_df[fri_df["period"] == "Baseline (2010-2025)"]["exposed_population"].sum()
cur_exp_pop = sub_fri["exposed_population"].sum()
col3.metric(
    "Total Population Exposed to Risk",
    f"{cur_exp_pop:,.0f}",
    f"{((cur_exp_pop - base_exp_pop) / base_exp_pop) * 100:+.1f}% vs Baseline",
)
col4.metric(
    f"{selected_lga} Risk Rank & Tier",
    f"#{int(lga_row['lga_rank'])} ({lga_row['risk_tier']})",
    f"FRI: {lga_row['fri_score']:.1f} ({lga_row['wet_season_prob_pct']:.1f}% wet prob)",
)

tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Interactive Risk Map & LGA Rankings",
    "📍 LGA Deep-Dive & Seasonal Profile",
    "📈 2030–2050 Climate Scenarios",
    "🤖 ML Model Performance & SHAP",
])

with tab1:
    st.subheader("Interactive Lagos LGA Flood Risk Map (2010–2050)")
    if MAP_HTML_PATH.exists():
        components.html(MAP_HTML_PATH.read_text(encoding="utf-8"), height=620, scrolling=False)
    st.subheader(f"All 20 LGAs Ranked for: {selected_label}")
    display_cols = [
        "lga_rank", "lga", "fri_score", "fri_min", "fri_max", "risk_tier",
        "wet_season_prob_pct", "exp_flood_months_yr", "population", "exposed_population",
        "low5_share", "built_share",
    ]
    st.dataframe(sub_fri[display_cols], use_container_width=True, hide_index=True)

with tab2:
    st.subheader(f"LGA Profile: {selected_lga}")
    lga_all_periods = fri_df[fri_df["lga"] == selected_lga]
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Progression Across Scenarios & Decades")
        st.dataframe(
            lga_all_periods[["scenario", "period", "lga_rank", "fri_score", "risk_tier", "wet_season_prob_pct", "population", "exposed_population"]],
            use_container_width=True,
            hide_index=True,
        )
    with c2:
        st.markdown("#### Seasonal Monthly Flood Probability Curve")
        hist_lga = master_df[master_df["lga"] == selected_lga].groupby("month_num")["flood"].mean() * 100
        p245_lga = proj_m_df[(proj_m_df["lga"] == selected_lga) & (proj_m_df["scenario"] == "ssp245") & (proj_m_df["year"] >= 2040)].groupby("month_num")["flood_prob_mean"].mean() * 100
        p585_lga = proj_m_df[(proj_m_df["lga"] == selected_lga) & (proj_m_df["scenario"] == "ssp585") & (proj_m_df["year"] >= 2040)].groupby("month_num")["flood_prob_mean"].mean() * 100

        fig, ax = plt.subplots(figsize=(7, 3.8))
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        ax.plot(range(1, 13), hist_lga.values, marker="o", color="gray", linestyle="--", label="Historical Observed (2010–2025)")
        ax.plot(range(1, 13), p245_lga.values, marker="s", color="steelblue", linewidth=2, label="2040–2050 · SSP2-4.5")
        ax.plot(range(1, 13), p585_lga.values, marker="^", color="crimson", linewidth=2, label="2040–2050 · SSP5-8.5")
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(months)
        ax.set_ylabel("Flood Probability (%)")
        ax.set_title(f"Monthly Flood Risk Seasonality in {selected_lga}")
        ax.legend()
        st.pyplot(fig)

with tab3:
    st.subheader("CMIP6 Climate Projections & Exposed Population (2030–2050)")
    st.image(str(ROOT / "outputs/figures/08_climate_projections_2030_2050.png"), use_container_width=True)
    st.image(str(ROOT / "outputs/figures/09_exposed_population_by_lga.png"), use_container_width=True)

with tab4:
    st.subheader("Supervised ML Model Evaluation (Held-Out Test Period: 2021–2025)")
    st.dataframe(model_comp_df, use_container_width=True, hide_index=True)
    st.image(str(ROOT / "outputs/figures/07_pr_roc_calibration_curves.png"), use_container_width=True)
    st.image(str(ROOT / "outputs/figures/07_feature_importance_and_shap_bar.png"), use_container_width=True)
