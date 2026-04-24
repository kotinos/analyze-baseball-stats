from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

_SRC = Path(__file__).resolve().parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from baseball_stats.mock_data import generate_players
from baseball_stats.transforms import enrich_player_stats, top_high_value

_PREMIUM_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
    .stApp {
        background: radial-gradient(1200px 800px at 20% -10%, #14332a 0%, #0a0e14 55%, #050608 100%);
        color: #e8edf5;
    }
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #0f141c 0%, #0a0e14 100%);
        border-right: 1px solid rgba(0, 212, 170, 0.15);
    }
    .block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 1200px; }
    h1, h2, h3 {
        font-family: 'Bebas Neue', sans-serif !important;
        letter-spacing: 0.04em;
        font-weight: 400 !important;
    }
    h1 { font-size: 3.2rem !important; color: #f4f7fb !important; margin-bottom: 0.2rem !important; }
    h2 { font-size: 2rem !important; color: #9fe7d6 !important; margin-top: 1.8rem !important; }
    .subtle {
        font-family: 'Inter', sans-serif;
        color: #9aa7bd;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    div[data-testid="stMetricValue"] { color: #00d4aa !important; font-weight: 700 !important; }
    .leader-wrap {
        border: 1px solid rgba(0, 212, 170, 0.25);
        border-radius: 14px;
        padding: 0.75rem 0.75rem 0.5rem;
        background: linear-gradient(145deg, rgba(18, 28, 36, 0.95), rgba(8, 12, 18, 0.92));
        box-shadow: 0 18px 50px rgba(0, 0, 0, 0.45);
    }
    .leader-wrap table { font-family: 'Inter', sans-serif !important; color: #e8edf5 !important; }
    .stPlotlyChart { border-radius: 14px; overflow: hidden; border: 1px solid rgba(0, 212, 170, 0.18); }
</style>
"""


def _style_leaderboard(df: pd.DataFrame) -> str:
    display_df = df[
        ["Name", "OBP", "Value", "Salary", "Hits", "Walks", "AtBats"]
    ].copy()
    styler = (
        display_df.style.format(
            {
                "OBP": "{:.3f}",
                "Value": "{:.4f}",
                "Salary": "${:,.0f}",
                "Hits": "{:.0f}",
                "Walks": "{:.0f}",
                "AtBats": "{:.0f}",
            },
            na_rep="—",
        )
        .background_gradient(subset=["Value", "OBP"], cmap="Greens", low=0.15, high=0.95)
        .hide(axis="index")
    )
    return styler.to_html()


def main() -> None:
    st.markdown(_PREMIUM_CSS, unsafe_allow_html=True)

    st.title("Plate Value Command")
    st.markdown(
        '<p class="subtle">Moneyball-style signal: OBP per $1M salary surfaces '
        "undervalued bats without touching a CSV.</p>",
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.header("Room controls")
        seed = st.number_input("Mock seed", min_value=0, max_value=10_000, value=42, step=1)
        st.caption("Change the seed to reshuffle synthetic counting stats.")

    players = generate_players(seed=int(seed))
    enriched = enrich_player_stats(players)
    leaders = top_high_value(enriched, n=5)

    median_value = float(enriched["Value"].median(skipna=True))
    median_obp = float(enriched["OBP"].median(skipna=True))

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("League median OBP", f"{median_obp:.3f}")
    with c2:
        st.metric("League median value", f"{median_value:.4f}")
    with c3:
        st.metric("Players tracked", f"{len(enriched)}")

    st.subheader("Top 5 high-value profiles")
    st.markdown(
        '<div class="leader-wrap">'
        + _style_leaderboard(leaders)
        + "</div>",
        unsafe_allow_html=True,
    )

    st.subheader("Payroll vs. on-base")
    scatter = px.scatter(
        enriched,
        x="Salary",
        y="OBP",
        hover_name="Name",
        hover_data={
            "Salary": ":$,.0f",
            "OBP": ":.3f",
            "Value": ":.4f",
            "Hits": True,
            "Walks": True,
            "AtBats": True,
        },
        color="Value",
        color_continuous_scale=["#1f2937", "#0f766e", "#34d399", "#bef264"],
    )
    scatter.update_traces(
        marker=dict(size=13, line=dict(width=1, color="rgba(255,255,255,0.35)"), opacity=0.92),
    )
    scatter.update_layout(
        template="plotly_dark",
        margin=dict(l=8, r=8, t=48, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(12,18,24,0.55)",
        font=dict(family="Inter", color="#e8edf5"),
        xaxis_title="Salary ($)",
        yaxis_title="On-base percentage",
        coloraxis_colorbar=dict(
            title="OBP / $1M",
            tickformat=".3f",
        ),
        height=520,
    )
    scatter.update_xaxes(showgrid=True, gridcolor="rgba(148,163,184,0.12)")
    scatter.update_yaxes(showgrid=True, gridcolor="rgba(148,163,184,0.12)")
    st.plotly_chart(scatter, use_container_width=True)


if __name__ == "__main__":
    main()
