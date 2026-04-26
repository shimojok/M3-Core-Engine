import streamlit as st
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

st.set_page_config(page_title="M3-Core-Engine Dashboard", layout="wide")
st.title("🌍 MBT55 GHG Abatement Simulator")
st.markdown("**M3-Core-Engine | IPCC Tier 2 | 5.1億トン削減目標**")

# パラメータ読み込み
with open("src/parameters_optimized.json") as f:
    params = json.load(f)

# 基本数値（notebookから抽出）
GHG_PER_UNIT_YEAR = 9299  # tCO2e/unit/yr
TARGET_GHG = 510_000_000   # tCO2e/yr
DAC_LOW, DAC_HIGH = 300, 600
MBT55_COST = 2.90  # USD/tCO2e

# スライダー
col1, col2 = st.columns(2)
with col1:
    units = st.slider("MBT55発酵機台数", 0, 100000, 54850, step=100)
    ghg = units * GHG_PER_UNIT_YEAR / 1e6
    st.metric("年間GHG削減量 (Mt CO₂e)", f"{ghg:.1f}")
    st.metric("目標達成率", f"{ghg / (TARGET_GHG/1e6) * 100:.1f}%")

with col2:
    st.metric("MBT55 コスト ($/tCO₂e)", f"${MBT55_COST:.2f}")
    st.metric("DAC コスト ($/tCO₂e)", f"${DAC_LOW}〜${DAC_HIGH}")
    st.metric("MBT55の優位性", f"{DAC_LOW/MBT55_COST:.0f}x〜{DAC_HIGH/MBT55_COST:.0f}x 安価")

st.info(f"**パラメータ最適化**: Nelder-Mead + L-BFGS-B | H₂制約: {params['_metadata']['h2_constraint_satisfied']} | 分解率24h: {params['_metadata']['decomposition_rate_24h']*100:.0f}%")
