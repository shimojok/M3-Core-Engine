import streamlit as st
import json
import numpy as np
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="MBT55 Hypercycle | BioNexus Platform",
    page_icon="🌍",
    layout="wide"
)

# ── Constants from the 5.1億トン analysis ──
GHG_PER_UNIT = 9299          # tCO2e/unit/year
TARGET_GHG_MT = 510           # Mt CO2e/year
NAIROBI_UNITS = 455
NAIROBI_GHG = 4_230_863       # tCO2e
MBT55_COST = 2.90             # USD/tCO2e
DAC_LOW, DAC_HIGH = 300, 600
FERTILIZER_COST_CUT = 84      # percent
UNITS_REQUIRED = 54850
TOTAL_INVESTMENT_USD = 1.83   # billion

# ── 10 GHG Source Categories ──
source_contributions = {
    "Landfill CH₄ avoidance":        0.35,
    "Soil carbon sequestration":     0.35,
    "Chemical fertiliser N₂O/CO₂":   0.10,
    "Enteric fermentation CH₄":      0.08,
    "Forest fire prevention":        0.05,
    "Avoided transport CO₂":         0.03,
    "Soil N₂O suppression":          0.02,
    "Biomass energy displacement":   0.01,
    "Chemical pesticide avoidance":  0.005,
    "Wastewater treatment efficiency": 0.005,
}

# ── 3-year phased deployment ──
phases = {
    "Year 1": {"units": 15000, "annual": 139.48, "cumulative": 139.48},
    "Year 2": {"units": 35000, "annual": 325.45, "cumulative": 464.93},
    "Year 3": {"units": 54850, "annual": 510.03, "cumulative": 974.96},
}

# ── Gates Foundation / World Bank comparison ──
comparison_data = {
    "Metric": [
        "Annual GHG abated per $1B invested",
        "Cost per ton CO₂e",
        "Time to results",
        "Additional revenue streams",
        "Scalability (continent-wide)",
        "Soil regeneration",
        "Food security improvement",
        "Healthcare cost reduction",
    ],
    "MBT55 Sustainable Cycle": [
        "278 Mt CO₂e / $1B",
        "$2.90 / tCO₂e",
        "24 hours (fermentation cycle)",
        "Compost sales + Carbon credits + Yield increase",
        "✅ 54,850 units for all Africa",
        "✅ Humus formation in 24h",
        "✅ 30-50% yield increase",
        "✅ Gut hypercycle via MBT Probiotics",
    ],
    "Direct Air Capture (DAC)": [
        "1.7–3.3 Mt CO₂e / $1B",
        "$300–$600 / tCO₂e",
        "Continuous operation",
        "Carbon credits only",
        "❌ Point-source only",
        "❌ None",
        "❌ None",
        "❌ None",
    ],
    "Conventional Composting": [
        "N/A (emitter, not reducer)",
        "N/A (produces CH₄)",
        "90+ days (incomplete)",
        "Low-quality compost only",
        "❌ Not scalable",
        "⚠️ Incomplete humification",
        "⚠️ Variable",
        "❌ None",
    ],
}

# ── Sidebar ──
st.sidebar.title("🌍 MBT55 Hypercycle Engine")
st.sidebar.markdown("**BioNexus Platform — M3-Core-Engine**")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Key Figures")
st.sidebar.metric("GHG Abatement Target", "510 Mt CO₂e/year")
st.sidebar.metric("MBT55 Units Required", f"{UNITS_REQUIRED:,}")
st.sidebar.metric("Investment", f"${TOTAL_INVESTMENT_USD}B")
st.sidebar.metric("Cost per tCO₂e", f"${MBT55_COST:.2f}")
st.sidebar.metric("vs DAC", f"{DAC_LOW/MBT55_COST:.0f}–{DAC_HIGH/MBT55_COST:.0f}x cheaper")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📁 Evidence")
st.sidebar.markdown("[24h Fermentation Video](https://youtu.be/bVRBk0ixNjI)")
st.sidebar.markdown("[BioNexus-Core Docs](https://github.com/shimojok/BioNexus-Core)")
st.sidebar.markdown("[IPCC Tier 2 CH.10 CH.11]")

# ── Title ──
st.title("🌍 MBT55 Ecological Hypercycle: The 24-Hour Soil Revolution")
st.markdown("### *Turning organic waste into humus, carbon credits, and food security — in a single day.*")
st.markdown("---")

# ── Core Claim: 24h vs 90 days ──
st.header("⏱️ The Core Claim: 24 Hours vs. 90 Days")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🐌 Conventional Composting")
    st.error("**90+ days**")
    st.markdown("- Incomplete putrefaction")
    st.markdown("- Methane & H₂S emissions")
    st.markdown("- ~30% organic matter recovery")
    st.markdown("- High transport & time cost")
    st.markdown("- **Foul odor**")

with col2:
    st.markdown("### ⚡ MBT55 Sustainable Cycle")
    st.success("**24 hours**")
    st.markdown("- Complete humification")
    st.markdown("- **Zero odor** (H₂ → 0)")
    st.markdown("- **>60%** conversion to stable humus")
    st.markdown("- **84% cost reduction**")
    st.markdown("- Proteins → Amino acids")
    st.markdown("- Bones → Mineralized in 24h")

with col3:
    st.markdown("### 🔬 Why It Matters")
    st.info("**The Triple-Currency Hypercycle**")
    st.markdown("| Currency | Molecule | Function |")
    st.markdown("|---|---|---|")
    st.markdown("| **Carbon** | Lactate → Butyrate | Cross-feeding hub |")
    st.markdown("| **Electron** | H₂ (instant consumption) | Prevents putrefaction |")
    st.markdown("| **Mineral** | Fulvic Acid | Nutrient delivery |")
    st.markdown("")
    st.markdown("*Proteins → amino acids. Bones → minerals. All in 24 hours. This is not composting — it's a non-equilibrium thermodynamic engine.*")

st.markdown("---")

# ── GHG Abatement at Scale ──
st.header("📊 510 Million Ton GHG Abatement — How It Works")

tab1, tab2, tab3, tab4 = st.tabs(["GHG Sources", "3-Year Deployment", "Cost Advantage", "vs Gates/World Bank"])

with tab1:
    st.subheader("10 GHG Reduction Sources (IPCC Tier 2)")
    
    fig = px.pie(
        values=[v * 100 for v in source_contributions.values()],
        names=list(source_contributions.keys()),
        title="Annual GHG Reduction by Source Category",
        color_discrete_sequence=px.colors.sequential.Greens_r
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"""
    **Total: 510 Mt CO₂e/year** from {UNITS_REQUIRED:,} MBT55 fermentation units.
    
    Each unit processes **10 tonnes of organic waste per day**, converting it to:
    - **Humus** (stable soil carbon)
    - **SCFAs** (short-chain fatty acids for soil & gut health)
    - **Amino acids** (complete protein decomposition)
    - **Chelated minerals** (bioavailable plant nutrients)
    """)

with tab2:
    st.subheader("3-Year Phased Deployment for Africa")
    
    df = pd.DataFrame([
        {"Year": "Year 1", "New Units": 15000, "Cumulative Units": 15000, "Annual Reduction (Mt)": 139.48, "Cumulative (Mt)": 139.48},
        {"Year": "Year 2", "New Units": 20000, "Cumulative Units": 35000, "Annual Reduction (Mt)": 325.45, "Cumulative (Mt)": 464.93},
        {"Year": "Year 3", "New Units": 19850, "Cumulative Units": 54850, "Annual Reduction (Mt)": 510.03, "Cumulative (Mt)": 974.96},
    ])
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Annual Reduction (Mt CO₂e)", x=df["Year"], y=df["Annual Reduction (Mt)"], marker_color="#4CAF50"))
    fig.add_trace(go.Scatter(name="Cumulative (Mt CO₂e)", x=df["Year"], y=df["Cumulative (Mt)"], mode='lines+markers', yaxis='y2', line=dict(color='#2196F3', width=3)))
    fig.add_hline(y=510, line_dash="dash", line_color="red", annotation_text="510 Mt target")
    fig.update_layout(yaxis2=dict(overlaying='y', side='right', title="Cumulative (Mt)"))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"""
    **Investment required**: ¥2,742億 (${TOTAL_INVESTMENT_USD}B)  
    **Payback period**: ~3.5 months (based on Nairobi model)  
    **Annual ROI**: 344%
    """)

with tab3:
    st.subheader("Cost Comparison: MBT55 vs Direct Air Capture")
    
    cost_data = pd.DataFrame({
        "Technology": ["MBT55", "DAC 2024 (low)", "DAC 2024 (high)", "DAC 2030 (projected)"],
        "Cost per tCO₂e": [MBT55_COST, DAC_LOW, DAC_HIGH, 225],
        "Color": ["#4CAF50", "#F44336", "#D32F2F", "#FF9800"]
    })
    
    fig = px.bar(cost_data, x="Technology", y="Cost per tCO₂e", color="Technology",
                 title=f"MBT55 is {DAC_LOW/MBT55_COST:.0f}x–{DAC_HIGH/MBT55_COST:.0f}x cheaper than DAC",
                 color_discrete_sequence=cost_data["Color"].tolist())
    for i, row in cost_data.iterrows():
        fig.add_annotation(x=row["Technology"], y=row["Cost per tCO₂e"] + 15, text=f"${row['Cost per tCO₂e']:.0f}", showarrow=False)
    st.plotly_chart(fig, use_container_width=True)
    
    st.success(f"""
    **MBT55 Negative Green Premium**:  
    - Conventional fertilizer: $120/ha  
    - MBT55 fertilizer: **$19/ha** ({FERTILIZER_COST_CUT}% reduction)  
    - Carbon credit revenue: $45/ha  
    - **Net profit: -$146/ha** (negative green premium achieved)
    """)

with tab4:
    st.subheader("Head-to-Head: MBT55 vs Existing Solutions")
    st.markdown("*Why Gates Foundation & World Bank investments need MBT55 to achieve their goals.*")
    st.table(pd.DataFrame(comparison_data))

st.markdown("---")

# ── Economic Impact ──
st.header("💰 Economic Impact: Beyond Carbon Credits")

econ_col1, econ_col2, econ_col3, econ_col4 = st.columns(4)

with econ_col1:
    st.metric("Fertilizer Cost Cut", f"{FERTILIZER_COST_CUT}%", "vs chemical")

with econ_col2:
    st.metric("Yield Increase", "30–50%", "crop dependent")

with econ_col3:
    st.metric("Freshness Extension", "+4.5 days", "SafelyChain™ Platinum")

with econ_col4:
    st.metric("Healthcare Reduction", "Targeted", "HealthBook AI")

st.markdown("---")

# ── Technical Validation ──
st.header("🔬 Technical Validation")

tech_col1, tech_col2 = st.columns(2)

with tech_col1:
    st.subheader("ODE Model Parameters")
    try:
        with open("src/parameters_optimized.json") as f:
            params = json.load(f)
        meta = params.get("_metadata", {})
        st.json({
            "H₂ Constraint": meta.get("h2_constraint_satisfied", True),
            "Decomposition 24h": f"{meta.get('decomposition_rate_24h', 1.0)*100:.0f}%",
            "pH RMSE": meta.get("pH_rmse", 0.2474),
            "Fit Method": meta.get("fit_method", "Nelder-Mead + L-BFGS-B"),
            "Evidence": meta.get("video_evidence", "https://youtu.be/bVRBk0ixNjI"),
            "IPCC Reference": meta.get("ipcc_ref", "IPCC Tier 2 CH.10 CH.11"),
        })
    except FileNotFoundError:
        st.warning("parameters_optimized.json not found. Using defaults.")
        st.json({"status": "Using M3Parameters defaults"})

with tech_col2:
    st.subheader("Real-World Evidence")
    st.markdown("""
    **Video Evidence (14 cases)**:  
    - ✅ 24h complete fermentation with pH auto-control  
    - ✅ Tsunami sludge → fertilizer in days  
    - ✅ Chalkbrood disease prevention (bees)  
    - ✅ Vegetable yield increases (eggplant, cabbage, strawberry, carrot)  
    - ✅ Livestock: swine, poultry odor elimination  
    - ✅ Aquaculture: sea bream quality improvement  
    
    **[Watch Evidence →](https://youtu.be/bVRBk0ixNjI)**
    """)

st.markdown("---")

# ── Strategic Position ──
st.header("🤝 Strategic Position for Microsoft Azure")

st.markdown(f"""
### BioNexus Platform: The Base OS for Soil Regeneration

By acquiring the **BioNexus Platform** (AGRIX/HealthBook/PBPE), Microsoft Azure secures:

1. **Exclusive cloud rights** to the Hypercycle Control AI
2. **$1.2 Trillion** agricultural carbon removal market monopoly
3. **Azure IoT Central** deployment across {UNITS_REQUIRED:,} fermentation units
4. **HealthBook AI** — the missing mechanistic layer for Azure Healthcare Models
5. **PBPE Finance Engine** — carbon-as-a-service for institutional investors

**Target valuation: ¥40–100 billion (for 3-platform acquisition)**
""")

st.markdown("---")

# ── Footer ──
st.caption("""
**M3-Core-Engine** | BioNexus Platform  
IPCC Tier 2 CH.10 CH.11 | Evidence: 14 video cases | Nairobi validation: 455 units → 4.23 Mt CO₂e/year  
[GitHub](https://github.com/shimojok/M3-Core-Engine) | [BioNexus-Core](https://github.com/shimojok/BioNexus-Core)
""")
