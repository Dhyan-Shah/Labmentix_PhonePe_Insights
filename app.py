# ─────────────────────────────────────────────────────────────────────────────
# PhonePe Transaction Insights — Streamlit Dashboard
# Author  : [Your Name]
# Intern  : Labmentix Data Science with AI/ML (6 Months Remote)
# ─────────────────────────────────────────────────────────────────────────────

import warnings
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
warnings.filterwarnings("ignore")

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PhonePe Pulse Dashboard",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* ── Main background ── */
.main .block-container {
    background-color: #f5f0ff;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* ══════════════════════════════════════
   SIDEBAR — everything white
══════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2d0060 0%, #4a0d96 50%, #6b21a8 100%) !important;
    border-right: 3px solid #a855f7;
}

/* ALL text elements inside sidebar → white */
section[data-testid="stSidebar"] *:not(input):not(option) {
    color: #ffffff !important;
}

/* Sidebar selectbox — the visible box itself */
section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
    background-color: #ffffff !important;
    border: 2px solid #a855f7 !important;
    border-radius: 10px !important;
}
/* The selected VALUE text inside selectbox */
section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] span,
section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] div {
    color: #2d0060 !important;
    font-weight: 600 !important;
}
/* Dropdown arrow icon */
section[data-testid="stSidebar"] .stSelectbox svg {
    fill: #2d0060 !important;
}

/* Sidebar multiselect — the visible box */
section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] {
    background-color: #ffffff !important;
    border: 2px solid #a855f7 !important;
    border-radius: 10px !important;
}
/* Multiselect placeholder and typed text */
section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] input {
    color: #2d0060 !important;
}
/* Multiselect selected tags */
section[data-testid="stSidebar"] [data-baseweb="tag"] {
    background-color: #7c3aed !important;
    border-radius: 6px !important;
}
section[data-testid="stSidebar"] [data-baseweb="tag"] span {
    color: #ffffff !important;
}
/* Tag close button */
section[data-testid="stSidebar"] [data-baseweb="tag"] [role="presentation"] {
    color: #ffffff !important;
}

/* Sidebar dividers */
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.3) !important;
}

/* ══════════════════════════════════════
   TABS — all tab text clearly visible
══════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: linear-gradient(90deg, #2d0060, #4a0d96, #6b21a8) !important;
    border-radius: 14px !important;
    padding: 5px !important;
    gap: 4px !important;
    box-shadow: 0 4px 16px rgba(45,0,96,0.35) !important;
}

/* ── Every tab button — force white text ── */
.stTabs [data-baseweb="tab"],
.stTabs [data-baseweb="tab"] *,
.stTabs [data-baseweb="tab"] p,
.stTabs [data-baseweb="tab"] span,
.stTabs [data-baseweb="tab"] div,
button[data-baseweb="tab"],
button[data-baseweb="tab"] p,
button[data-baseweb="tab"] span {
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    border-radius: 10px !important;
    background: transparent !important;
    opacity: 1 !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* ── SELECTED tab — white card, dark purple text ── */
.stTabs [aria-selected="true"],
.stTabs [aria-selected="true"] *,
.stTabs [aria-selected="true"] p,
.stTabs [aria-selected="true"] span,
.stTabs [aria-selected="true"] div,
button[aria-selected="true"],
button[aria-selected="true"] p,
button[aria-selected="true"] span {
    background: #ffffff !important;
    color: #2d0060 !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2) !important;
    font-weight: 700 !important;
    opacity: 1 !important;
    -webkit-text-fill-color: #2d0060 !important;
}

/* ── Hide Streamlit's default underline indicator ── */
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* ── Main content headings ── */
h1 { color: #2d0060 !important; font-weight: 800 !important; }
h2 { color: #4a0d96 !important; font-weight: 700 !important; }
h3 { color: #6b21a8 !important; font-weight: 600 !important; }
p, .stMarkdown p { color: #3b1f6b !important; }
hr { border-color: #a855f7 !important; }

/* ── Metric cards ── */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #4a0d96, #6b21a8) !important;
    border-radius: 16px !important;
    padding: 18px !important;
    border: none !important;
    box-shadow: 0 4px 20px rgba(74,13,150,0.35) !important;
    text-align: center;
}
div[data-testid="metric-container"] label {
    color: #e9d5ff !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 26px !important;
    font-weight: 800 !important;
}

/* ── Charts — white card ── */
.element-container .stPlotlyChart {
    background: #ffffff;
    border-radius: 14px;
    padding: 12px;
    box-shadow: 0 2px 14px rgba(74,13,150,0.1);
    margin-bottom: 8px;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #ede9fe !important;
    color: #2d0060 !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}

/* ── Main area selectbox ── */
.stSelectbox > div > div {
    border: 2px solid #6b21a8 !important;
    border-radius: 8px !important;
    color: #2d0060 !important;
}

/* ── Dataframe ── */
.stDataFrame { border: 1px solid #a855f7; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ── DB CONNECTION ─────────────────────────────────────────────────────────────
@st.cache_resource
def get_engine():
    """Create and cache the SQLAlchemy engine"""
    DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

    return create_engine(DB_URL)

engine = get_engine()

@st.cache_data(ttl=300)
def run(query: str) -> pd.DataFrame:
    """Execute SQL query and return DataFrame (cached for 5 minutes)"""
    return pd.read_sql(query, engine)

def clean_state(df: pd.DataFrame) -> pd.DataFrame:
    """Clean state names: replace hyphens with spaces, title-case"""
    df["state"] = df["state"].str.replace("-", " ").str.title()
    return df

def fmt_inr(value: float) -> str:
    """Format large numbers into readable INR format"""
    if value >= 1e12:
        return f"₹{value/1e12:.2f}T"
    elif value >= 1e9:
        return f"₹{value/1e9:.2f}B"
    elif value >= 1e6:
        return f"₹{value/1e6:.2f}M"
    return f"₹{value:,.0f}"

def fmt_count(value: float) -> str:
    """Format large counts into readable format"""
    if value >= 1e9:
        return f"{value/1e9:.2f}B"
    elif value >= 1e6:
        return f"{value/1e6:.2f}M"
    elif value >= 1e3:
        return f"{value/1e3:.1f}K"
    return f"{value:,.0f}"

# ── LOAD FILTER DATA ──────────────────────────────────────────────────────────
@st.cache_data
def load_filters():
    years    = run("SELECT DISTINCT year    FROM aggregated_transaction ORDER BY year")["year"].tolist()
    quarters = run("SELECT DISTINCT quarter FROM aggregated_transaction ORDER BY quarter")["quarter"].tolist()
    states_df = run("SELECT DISTINCT state FROM aggregated_transaction ORDER BY state")
    states_df = clean_state(states_df)
    states   = ["All States"] + states_df["state"].tolist()
    return years, quarters, states

years, quarters, states = load_filters()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:10px 0 6px;'>
      <div style='font-size:42px;'>💜</div>
      <div style='font-size:18px; font-weight:800; color:#fff; letter-spacing:-0.3px;'>PhonePe Pulse</div>
      <div style='font-size:11px; color:#e9d5ff; margin-bottom:4px;'>Transaction Insights Dashboard</div>
    </div>
    <hr style='border-color:rgba(255,255,255,0.25); margin:8px 0;'>
    <p style='font-size:14px; font-weight:700; color:#e9d5ff; margin-bottom:6px;'>🔍 Filters</p>
    """, unsafe_allow_html=True)

    selected_year = st.selectbox(
        "📅 Select Year",
        options=["All Years"] + years,
        index=0,
    )
    selected_quarter = st.selectbox(
        "📆 Select Quarter",
        options=["All Quarters"] + [f"Q{q}" for q in quarters],
        index=0,
    )
    selected_state = st.selectbox(
        "🗺️ Select State",
        options=states,
        index=0,
    )
    selected_txn_type = st.multiselect(
        "💳 Transaction Type",
        options=["Peer to Peer", "Merchant", "Recharge & Bill Payments",
                 "Financial Services", "Others"],
        default=["Peer to Peer", "Merchant", "Recharge & Bill Payments",
                 "Financial Services", "Others"],
    )

    st.markdown("---")
    st.markdown("### 📊 Dashboard Sections")
    st.markdown(
        "- 🏠 Overview\n"
        "- 💳 Transactions\n"
        "- 👥 Users & Devices\n"
        "- 🛡️ Insurance\n"
        "- 🗺️ Geographic Map\n"
        "- 📈 Business Insights"
    )
    st.markdown("""
    <hr style='border-color:rgba(255,255,255,0.25); margin:12px 0;'>
    <p style='font-size:12px; font-weight:700; color:#e9d5ff; margin-bottom:6px;'>📌 Dashboard Sections</p>
    <p style='font-size:12px; color:#e9d5ff; line-height:2;'>
    🏠 Overview<br>💳 Transactions<br>👥 Users &amp; Devices<br>🛡️ Insurance<br>🗺️ Geographic Map<br>📈 Business Insights
    </p>
    <hr style='border-color:rgba(255,255,255,0.25); margin:12px 0;'>
    <p style='font-size:11px; color:#c4b5fd; text-align:center;'>
    📡 PhonePe Pulse | 2018–2024<br>🔧 Streamlit + PostgreSQL + Plotly
    </p>
    """, unsafe_allow_html=True)

# ── BUILD WHERE CLAUSE ────────────────────────────────────────────────────────
def build_where(year=True, quarter=True, state=True, txn_type=True, prefix="WHERE"):
    conditions = []
    if year    and selected_year    != "All Years":
        conditions.append(f"year = {selected_year}")
    if quarter and selected_quarter != "All Quarters":
        q = int(selected_quarter.replace("Q", ""))
        conditions.append(f"quarter = {q}")
    if state   and selected_state   != "All States":
        raw = selected_state.lower().replace(" ", "-")
        conditions.append(f"state = '{raw}'")
    if txn_type and selected_txn_type:
        types = "', '".join(selected_txn_type)
        conditions.append(f"transaction_type IN ('{types}')")
    if conditions:
        return f"{prefix} " + " AND ".join(conditions)
    return ""

# ── MAIN HEADER ───────────────────────────────────────────────────────────────
st.markdown("""
<div style='background: linear-gradient(135deg, #2d0060 0%, #4a0d96 55%, #6b21a8 100%);
            border-radius: 20px; padding: 30px 40px; margin-bottom: 24px;
            box-shadow: 0 8px 32px rgba(45,0,96,0.4);'>
  <div style='display:flex; align-items:center; gap:16px;'>
    <div style='font-size:3rem;'>💜</div>
    <div>
      <div style='font-size:2rem; font-weight:800; color:#ffffff;
                  font-family:Inter,sans-serif; letter-spacing:-0.5px;'>
        PhonePe Transaction Insights
      </div>
      <div style='font-size:0.9rem; color:#c4b5fd; margin-top:5px; font-family:Inter,sans-serif;'>
        Interactive Analytics Dashboard &nbsp;|&nbsp; Labmentix Data Science Internship &nbsp;|&nbsp; 2018–2024
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Overview",
    "💳 Transactions",
    "👥 Users & Devices",
    "🛡️ Insurance",
    "🗺️ Geographic Map",
    "📈 Business Insights",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("## 🏠 Platform Overview")
    st.markdown("Key metrics and high-level trends across PhonePe's transaction, user, and insurance data.")
    st.markdown("---")

    where_txn = build_where(txn_type=False)
    where_user = build_where(txn_type=False)

    # ── KPI Metrics ──
    kpi_txn = run(f"""
        SELECT SUM(transaction_amount) AS total_amount,
               SUM(transaction_count)  AS total_count
        FROM   aggregated_transaction
        {where_txn}
    """)
    kpi_user = run(f"""
        SELECT SUM(registered_users) AS total_users,
               SUM(app_opens)        AS total_opens
        FROM   map_user
        {where_user.replace('transaction_type', 'state')}
    """)
    kpi_ins = run(f"""
        SELECT SUM(insurance_amount) AS total_ins_amount,
               SUM(insurance_count)  AS total_ins_count
        FROM   aggregated_insurance
        {build_where(txn_type=False)}
    """)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("💰 Total Transaction Amount",
                  fmt_inr(kpi_txn["total_amount"].iloc[0] or 0))
    with col2:
        st.metric("🔢 Total Transactions",
                  fmt_count(kpi_txn["total_count"].iloc[0] or 0))
    with col3:
        st.metric("👥 Registered Users",
                  fmt_count(kpi_user["total_users"].iloc[0] or 0))
    with col4:
        st.metric("📱 App Opens",
                  fmt_count(kpi_user["total_opens"].iloc[0] or 0))
    with col5:
        st.metric("🛡️ Insurance Amount",
                  fmt_inr(kpi_ins["total_ins_amount"].iloc[0] or 0))

    st.markdown("---")

    col_l, col_r = st.columns(2)

    with col_l:
        # Transaction trend
        df_trend = run("""
            SELECT year, quarter,
                   year::text || ' Q' || quarter::text AS period,
                   SUM(transaction_amount) AS total_amount,
                   SUM(transaction_count)  AS total_count
            FROM   aggregated_transaction
            GROUP BY year, quarter
            ORDER BY year, quarter
        """)
        fig = px.line(
            df_trend, x="period", y="total_amount",
            title="📈 Transaction Amount Trend (All Time)",
            labels={"total_amount": "Amount (₹)", "period": "Period"},
            markers=True, line_shape="spline",
        )
        fig.update_traces(line_color="#4a0d96", marker_size=6)
        fig.update_layout(
            plot_bgcolor="rgba(255,255,255,0)",
            paper_bgcolor="rgba(255,255,255,0)",
            font_color="#2d0060",
            xaxis=dict(tickangle=-45, gridcolor="#ede9fe"),
            yaxis=dict(gridcolor="#ede9fe"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        # Transaction type donut
        df_type = run(f"""
            SELECT transaction_type,
                   SUM(transaction_count)  AS total_count,
                   SUM(transaction_amount) AS total_amount
            FROM   aggregated_transaction
            {build_where(txn_type=False)}
            GROUP BY transaction_type
            ORDER BY total_count DESC
        """)
        fig2 = px.pie(
            df_type, names="transaction_type", values="total_count",
            title="💳 Transaction Count by Type",
            hole=0.45,
            color_discrete_sequence=["#c77dff","#9d4edd","#7b2d8b","#5a189a","#3c096c"],
        )
        fig2.update_traces(textposition="inside", textinfo="percent+label")
        fig2.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#2d0060", showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)

    # YoY growth bar
    df_yoy = run("""
        SELECT year, SUM(transaction_amount) AS total_amount
        FROM   aggregated_transaction
        GROUP BY year ORDER BY year
    """)
    df_yoy["prev"]       = df_yoy["total_amount"].shift(1)
    df_yoy["yoy_growth"] = ((df_yoy["total_amount"] - df_yoy["prev"]) / df_yoy["prev"] * 100).round(2)
    df_yoy = df_yoy.dropna()

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=df_yoy["year"].astype(str), y=df_yoy["yoy_growth"],
        marker_color=["#10b981" if x > 0 else "#ef4444" for x in df_yoy["yoy_growth"]],
        text=[f"{x:.1f}%" for x in df_yoy["yoy_growth"]], textposition="outside",
        name="YoY Growth %"
    ))
    fig3.update_layout(
        title="📊 Year-over-Year Transaction Growth (%)",
        xaxis_title="Year", yaxis_title="Growth (%)",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color="#2d0060",
        xaxis=dict(gridcolor="#ede9fe"), yaxis=dict(gridcolor="#ede9fe"),
    )
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — TRANSACTIONS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("## 💳 Transaction Analysis")
    st.markdown("Deep dive into transaction amounts, counts, and patterns across states, districts, and pincodes.")
    st.markdown("---")

    where = build_where()

    col_l, col_r = st.columns(2)

    with col_l:
        # Top 10 states by amount
        df_state = run(f"""
            SELECT state, SUM(transaction_amount) AS total_amount,
                   SUM(transaction_count) AS total_count
            FROM   aggregated_transaction
            {build_where(txn_type=False)}
            GROUP BY state ORDER BY total_amount DESC LIMIT 10
        """)
        df_state = clean_state(df_state)
        fig = px.bar(
            df_state, x="total_amount", y="state", orientation="h",
            title="🏆 Top 10 States by Transaction Amount",
            labels={"total_amount": "Amount (₹)", "state": "State"},
            color="total_amount", color_continuous_scale="Purples",
            text=df_state["total_amount"].apply(fmt_inr),
        )
        fig.update_layout(
            yaxis={"categoryorder": "total ascending"},
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#2d0060", coloraxis_showscale=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        # Transaction type stacked area
        df_type_yr = run(f"""
            SELECT year, transaction_type,
                   SUM(transaction_amount) AS total_amount
            FROM   aggregated_transaction
            {build_where(quarter=False, state=False, txn_type=False)}
            GROUP BY year, transaction_type ORDER BY year
        """)
        fig2 = px.area(
            df_type_yr, x="year", y="total_amount", color="transaction_type",
            title="📈 Transaction Type Growth by Year",
            labels={"total_amount": "Amount (₹)", "year": "Year", "transaction_type": "Type"},
            line_shape="spline",
            color_discrete_sequence=["#c77dff","#9d4edd","#7b2d8b","#5a189a","#3c096c"],
        )
        fig2.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#2d0060", xaxis=dict(tickmode="linear"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    col_l2, col_r2 = st.columns(2)

    with col_l2:
        # Top 10 districts
        df_dist = run(f"""
            SELECT state, district,
                   SUM(transaction_amount) AS total_amount,
                   SUM(transaction_count)  AS total_count
            FROM   map_transaction
            {build_where(txn_type=False)}
            GROUP BY state, district
            ORDER BY total_amount DESC LIMIT 10
        """)
        df_dist = clean_state(df_dist)
        df_dist["district"] = df_dist["district"].str.title()
        df_dist["label"]    = df_dist["district"] + " (" + df_dist["state"] + ")"
        fig3 = px.bar(
            df_dist, x="total_amount", y="label", orientation="h",
            title="🏙️ Top 10 Districts by Transaction Amount",
            labels={"total_amount": "Amount (₹)", "label": "District"},
            color="total_amount", color_continuous_scale="Purples",
            text=df_dist["total_amount"].apply(fmt_inr),
        )
        fig3.update_layout(
            yaxis={"categoryorder": "total ascending"},
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#2d0060", coloraxis_showscale=False,
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col_r2:
        # Quarterly seasonality
        df_qtr = run(f"""
            SELECT quarter, SUM(transaction_amount) AS total_amount,
                   SUM(transaction_count) AS total_count
            FROM   aggregated_transaction
            {build_where(quarter=False, txn_type=False)}
            GROUP BY quarter ORDER BY quarter
        """)
        df_qtr["quarter_label"] = ["Q1 (Jan-Mar)", "Q2 (Apr-Jun)",
                                    "Q3 (Jul-Sep)", "Q4 (Oct-Dec)"]
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=df_qtr["quarter_label"], y=df_qtr["total_amount"],
            marker_color=["#7b2d8b","#9d4edd","#c77dff","#e040fb"],
            name="Amount", text=df_qtr["total_amount"].apply(fmt_inr),
            textposition="outside",
        ))
        fig4.add_trace(go.Scatter(
            x=df_qtr["quarter_label"], y=df_qtr["total_count"],
            name="Count", yaxis="y2", mode="lines+markers",
            line=dict(color="#f59e0b", width=2), marker=dict(size=10),
        ))
        fig4.update_layout(
            title="📅 Quarterly Seasonality Pattern",
            yaxis=dict(title="Amount (₹)", gridcolor="#ede9fe"),
            yaxis2=dict(title="Count", overlaying="y", side="right"),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#2d0060", legend=dict(x=0.01, y=0.99),
        )
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # Top 10 pincodes
    df_pin = run(f"""
        SELECT entity_name AS pincode, state,
               SUM(transaction_amount) AS total_amount,
               SUM(transaction_count)  AS total_count
        FROM   top_transaction
        WHERE  entity_type = 'pincode'
        {build_where(txn_type=False, prefix='AND')}
        GROUP BY entity_name, state
        ORDER BY total_amount DESC LIMIT 10
    """)
    df_pin = clean_state(df_pin)
    fig5 = px.bar(
        df_pin, x="pincode", y="total_amount", color="state",
        title="📍 Top 10 Pincodes by Transaction Amount",
        labels={"total_amount": "Amount (₹)", "pincode": "Pincode"},
        text=df_pin["total_amount"].apply(fmt_inr),
        color_discrete_sequence=px.colors.sequential.Purples_r,
    )
    fig5.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color="#2d0060", xaxis_tickangle=-30,
    )
    st.plotly_chart(fig5, use_container_width=True)

    # Raw data table
    with st.expander("📋 View Raw Transaction Data"):
        df_raw = run(f"""
            SELECT state, year, quarter, transaction_type,
                   transaction_count, transaction_amount
            FROM   aggregated_transaction
            {build_where()}
            ORDER BY transaction_amount DESC
            LIMIT 100
        """)
        df_raw = clean_state(df_raw)
        st.dataframe(df_raw, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — USERS & DEVICES
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("## 👥 Users & Device Analysis")
    st.markdown("Explore registered users, app engagement, and device brand preferences across states.")
    st.markdown("---")

    col_l, col_r = st.columns(2)

    with col_l:
        # Top 10 states by registered users
        df_users = run(f"""
            SELECT state, SUM(registered_users) AS total_users,
                   SUM(app_opens) AS total_opens
            FROM   map_user
            {build_where(txn_type=False)}
            GROUP BY state ORDER BY total_users DESC LIMIT 10
        """)
        df_users = clean_state(df_users)
        fig = px.bar(
            df_users, x="total_users", y="state", orientation="h",
            title="👥 Top 10 States by Registered Users",
            labels={"total_users": "Registered Users", "state": "State"},
            color="total_users", color_continuous_scale="Purples",
            text=df_users["total_users"].apply(fmt_count),
        )
        fig.update_layout(
            yaxis={"categoryorder": "total ascending"},
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#2d0060", coloraxis_showscale=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        # Top device brands
        df_brand = run(f"""
            SELECT brand, SUM(user_count) AS total_users
            FROM   aggregated_user
            WHERE  brand != 'Others'
            {build_where(txn_type=False, prefix='AND')}
            GROUP BY brand ORDER BY total_users DESC LIMIT 12
        """)
        fig2 = px.bar(
            df_brand, x="total_users", y="brand", orientation="h",
            title="📱 Top 12 Device Brands by User Count",
            labels={"total_users": "Total Users", "brand": "Brand"},
            color="total_users", color_continuous_scale="Purples",
            text=df_brand["total_users"].apply(fmt_count),
        )
        fig2.update_layout(
            yaxis={"categoryorder": "total ascending"},
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#2d0060", coloraxis_showscale=False,
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    col_l2, col_r2 = st.columns(2)

    with col_l2:
        # Engagement scatter
        df_eng = run(f"""
            SELECT state,
                   SUM(registered_users) AS total_users,
                   SUM(app_opens)        AS total_opens,
                   ROUND((SUM(app_opens)::numeric /
                          NULLIF(SUM(registered_users),0)), 2) AS engagement_ratio
            FROM   map_user
            {build_where(txn_type=False)}
            GROUP BY state ORDER BY total_users DESC
        """)
        df_eng = clean_state(df_eng)
        fig3 = px.scatter(
            df_eng, x="total_users", y="total_opens",
            size="engagement_ratio", color="engagement_ratio",
            hover_name="state", color_continuous_scale="Purples",
            title="📊 App Opens vs Registered Users (Engagement Ratio)",
            labels={"total_users": "Registered Users", "total_opens": "App Opens",
                    "engagement_ratio": "Engagement Ratio"},
        )
        fig3.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#2d0060",
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col_r2:
        # User registration trend
        df_reg = run("""
            SELECT year, quarter,
                   year::text || ' Q' || quarter::text AS period,
                   SUM(registered_users) AS total_registered,
                   SUM(app_opens)        AS total_opens
            FROM   map_user
            GROUP BY year, quarter ORDER BY year, quarter
        """)
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=df_reg["period"], y=df_reg["total_registered"],
            name="Registered Users", mode="lines+markers",
            line=dict(color="#4a0d96", width=2), marker=dict(size=7),
        ))
        fig4.add_trace(go.Scatter(
            x=df_reg["period"], y=df_reg["total_opens"],
            name="App Opens", mode="lines+markers",
            line=dict(color="#f59e0b", width=2), marker=dict(size=7),
        ))
        fig4.update_layout(
            title="📈 User Registrations vs App Opens Trend",
            xaxis_title="Year-Quarter", yaxis_title="Count",
            xaxis_tickangle=-45, legend=dict(x=0.01, y=0.99),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#2d0060",
            xaxis=dict(gridcolor="#ede9fe"), yaxis=dict(gridcolor="#ede9fe"),
        )
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # Top districts by registered users
    df_dist_u = run(f"""
        SELECT state, district, SUM(registered_users) AS total_registered
        FROM   map_user
        {build_where(txn_type=False)}
        GROUP BY state, district
        ORDER BY total_registered DESC LIMIT 15
    """)
    df_dist_u = clean_state(df_dist_u)
    df_dist_u["district"] = df_dist_u["district"].str.title()
    df_dist_u["label"]    = df_dist_u["district"] + " (" + df_dist_u["state"] + ")"
    fig5 = px.bar(
        df_dist_u, x="total_registered", y="label", orientation="h",
        title="🏙️ Top 15 Districts by Registered Users",
        labels={"total_registered": "Registered Users", "label": "District"},
        color="total_registered", color_continuous_scale="Purples",
        text=df_dist_u["total_registered"].apply(fmt_count),
    )
    fig5.update_layout(
        yaxis={"categoryorder": "total ascending"}, height=500,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color="#2d0060", coloraxis_showscale=False,
    )
    st.plotly_chart(fig5, use_container_width=True)

    with st.expander("📋 View Engagement Data by State"):
        st.dataframe(df_eng.sort_values("engagement_ratio", ascending=False),
                     use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — INSURANCE
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("## 🛡️ Insurance Analysis")
    st.markdown("Analyze PhonePe's insurance segment growth, state-level penetration, and market opportunities.")
    st.markdown("---")

    # KPIs
    kpi_ins2 = run(f"""
        SELECT SUM(insurance_amount) AS total_amount,
               SUM(insurance_count)  AS total_count
        FROM   aggregated_insurance
        {build_where(txn_type=False)}
    """)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🛡️ Total Insurance Amount",
                  fmt_inr(kpi_ins2["total_amount"].iloc[0] or 0))
    with col2:
        st.metric("🔢 Total Insurance Policies",
                  fmt_count(kpi_ins2["total_count"].iloc[0] or 0))
    with col3:
        avg_val = ((kpi_ins2["total_amount"].iloc[0] or 0) /
                   max(kpi_ins2["total_count"].iloc[0] or 1, 1))
        st.metric("💰 Avg Policy Value", fmt_inr(avg_val))

    st.markdown("---")
    col_l, col_r = st.columns(2)

    with col_l:
        # Insurance growth over time
        df_ins_trend = run("""
            SELECT year, quarter,
                   year::text || ' Q' || quarter::text AS period,
                   SUM(insurance_amount) AS total_amount,
                   SUM(insurance_count)  AS total_count
            FROM   aggregated_insurance
            GROUP BY year, quarter ORDER BY year, quarter
        """)
        fig = px.area(
            df_ins_trend, x="period", y="total_amount",
            title="📈 Insurance Amount Growth Over Time",
            labels={"total_amount": "Insurance Amount (₹)", "period": "Year-Quarter"},
            line_shape="spline",
        )
        fig.update_traces(fill="tozeroy", line_color="#10b981",
                          fillcolor="rgba(16,185,129,0.15)")
        fig.update_layout(
            xaxis_tickangle=-45,
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#2d0060",
            xaxis=dict(gridcolor="#ede9fe"), yaxis=dict(gridcolor="#ede9fe"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        # Top states by insurance amount
        df_ins_state = run(f"""
            SELECT state, SUM(insurance_amount) AS total_amount,
                   SUM(insurance_count) AS total_count
            FROM   aggregated_insurance
            {build_where(txn_type=False)}
            GROUP BY state ORDER BY total_amount DESC LIMIT 10
        """)
        df_ins_state = clean_state(df_ins_state)
        fig2 = px.bar(
            df_ins_state, x="total_amount", y="state", orientation="h",
            title="🏆 Top 10 States by Insurance Amount",
            labels={"total_amount": "Amount (₹)", "state": "State"},
            color="total_amount", color_continuous_scale="Greens",
            text=df_ins_state["total_amount"].apply(fmt_inr),
        )
        fig2.update_layout(
            yaxis={"categoryorder": "total ascending"},
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#2d0060", coloraxis_showscale=False,
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # Gap analysis — Transaction vs Insurance
    df_gap = run(f"""
        WITH txn AS (
            SELECT state, SUM(transaction_amount) AS txn_amount
            FROM   aggregated_transaction
            {build_where(txn_type=False)}
            GROUP BY state
        ),
        ins AS (
            SELECT state, SUM(insurance_amount) AS ins_amount
            FROM   aggregated_insurance
            {build_where(txn_type=False)}
            GROUP BY state
        )
        SELECT t.state, t.txn_amount,
               COALESCE(i.ins_amount, 0) AS ins_amount,
               ROUND((COALESCE(i.ins_amount,0)/NULLIF(t.txn_amount,0)*100)::numeric,4)
               AS ins_penetration_pct
        FROM   txn t LEFT JOIN ins i ON t.state = i.state
        ORDER  BY t.txn_amount DESC LIMIT 12
    """)
    df_gap = clean_state(df_gap)

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(name="Transaction Amount", x=df_gap["state"],
                          y=df_gap["txn_amount"], marker_color="#9d4edd"))
    fig3.add_trace(go.Bar(name="Insurance Amount", x=df_gap["state"],
                          y=df_gap["ins_amount"], marker_color="#10b981"))
    fig3.update_layout(
        barmode="group",
        title="⚖️ Transaction vs Insurance Amount — Gap Analysis (Top 12 States)",
        xaxis_title="State", yaxis_title="Amount (₹)", xaxis_tickangle=-30,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color="#2d0060", legend=dict(x=0.01, y=0.99),
        yaxis=dict(gridcolor="#ede9fe"),
    )
    st.plotly_chart(fig3, use_container_width=True)

    col_l3, col_r3 = st.columns(2)
    with col_l3:
        # Insurance treemap
        df_tree = run(f"""
            SELECT state, SUM(insurance_amount) AS total_amount
            FROM   map_insurance
            {build_where(txn_type=False)}
            GROUP BY state ORDER BY total_amount DESC
        """)
        df_tree = clean_state(df_tree)
        fig4 = px.treemap(
            df_tree, path=["state"], values="total_amount",
            color="total_amount", color_continuous_scale="Greens",
            title="🗺️ Insurance Amount by State (Treemap)",
        )
        fig4.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#2d0060",
        )
        st.plotly_chart(fig4, use_container_width=True)

    with col_r3:
        # Penetration table
        st.markdown("#### 📊 Insurance Penetration % by State")
        st.dataframe(
            df_gap[["state", "txn_amount", "ins_amount", "ins_penetration_pct"]]
            .rename(columns={
                "state": "State",
                "txn_amount": "Txn Amount (₹)",
                "ins_amount": "Insurance Amount (₹)",
                "ins_penetration_pct": "Penetration %"
            })
            .sort_values("Penetration %", ascending=False)
            .reset_index(drop=True),
            use_container_width=True, height=400,
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — GEOGRAPHIC MAP
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("## 🗺️ Geographic Map Analysis")
    st.markdown("Visualize transaction, user, and insurance data across India's states on an interactive choropleth map.")
    st.markdown("---")

    map_metric = st.selectbox(
        "📊 Select Metric to Map",
        ["Transaction Amount", "Transaction Count", "Registered Users", "Insurance Amount"],
    )

    @st.cache_data
    def load_geojson():
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        try:
            return requests.get(url, timeout=10).json()
        except Exception:
            return None

    india_geojson = load_geojson()

    state_name_map = {
        "andaman-&-nicobar-islands": "Andaman & Nicobar Island",
        "andhra-pradesh": "Andhra Pradesh",
        "arunachal-pradesh": "Arunachal Pradesh",
        "assam": "Assam", "bihar": "Bihar",
        "chandigarh": "Chandigarh", "chhattisgarh": "Chhattisgarh",
        "dadra-&-nagar-haveli-&-daman-&-diu": "Dadra and Nagar Haveli and Daman and Diu",
        "delhi": "Delhi", "goa": "Goa", "gujarat": "Gujarat",
        "haryana": "Haryana", "himachal-pradesh": "Himachal Pradesh",
        "jammu-&-kashmir": "Jammu & Kashmir",
        "jharkhand": "Jharkhand", "karnataka": "Karnataka",
        "kerala": "Kerala", "ladakh": "Ladakh",
        "lakshadweep": "Lakshadweep", "madhya-pradesh": "Madhya Pradesh",
        "maharashtra": "Maharashtra", "manipur": "Manipur",
        "meghalaya": "Meghalaya", "mizoram": "Mizoram",
        "nagaland": "Nagaland", "odisha": "Odisha",
        "puducherry": "Puducherry", "punjab": "Punjab",
        "rajasthan": "Rajasthan", "sikkim": "Sikkim",
        "tamil-nadu": "Tamil Nadu", "telangana": "Telangana",
        "tripura": "Tripura", "uttar-pradesh": "Uttar Pradesh",
        "uttarakhand": "Uttarakhand", "west-bengal": "West Bengal",
    }

    if india_geojson:
        if map_metric == "Transaction Amount":
            df_map = run(f"""
                SELECT state, SUM(transaction_amount) AS value
                FROM   aggregated_transaction
                {build_where(txn_type=False)}
                GROUP BY state
            """)
            color_scale, label = "Purples", "Transaction Amount (₹)"
        elif map_metric == "Transaction Count":
            df_map = run(f"""
                SELECT state, SUM(transaction_count) AS value
                FROM   aggregated_transaction
                {build_where(txn_type=False)}
                GROUP BY state
            """)
            color_scale, label = "Blues", "Transaction Count"
        elif map_metric == "Registered Users":
            df_map = run(f"""
                SELECT state, SUM(registered_users) AS value
                FROM   map_user
                {build_where(txn_type=False)}
                GROUP BY state
            """)
            color_scale, label = "Greens", "Registered Users"
        else:
            df_map = run(f"""
                SELECT state, SUM(insurance_amount) AS value
                FROM   aggregated_insurance
                {build_where(txn_type=False)}
                GROUP BY state
            """)
            color_scale, label = "YlOrRd", "Insurance Amount (₹)"

        df_map["state_mapped"] = df_map["state"].map(state_name_map)
        df_map = df_map.dropna(subset=["state_mapped"])

        fig_map = px.choropleth(
            df_map,
            geojson=india_geojson,
            featureidkey="properties.ST_NM",
            locations="state_mapped",
            color="value",
            color_continuous_scale=color_scale,
            title=f"🗺️ India Map — {map_metric} by State",
            labels={"value": label, "state_mapped": "State"},
            hover_data=["value"],
        )
        fig_map.update_geos(fitbounds="locations", visible=False)
        fig_map.update_layout(
            margin=dict(l=0, r=0, t=40, b=0), height=600,
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#2d0060",
        )
        st.plotly_chart(fig_map, use_container_width=True)

        st.markdown("#### 📊 State Rankings Table")
        df_map_display = df_map[["state_mapped", "value"]].rename(
            columns={"state_mapped": "State", "value": map_metric}
        ).sort_values(map_metric, ascending=False).reset_index(drop=True)
        st.dataframe(df_map_display, use_container_width=True)
    else:
        st.warning("⚠️ Could not load India GeoJSON. Check your internet connection.")
        st.info("The map requires an internet connection to load India's state boundaries.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — BUSINESS INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown("## 📈 Business Insights & Case Studies")
    st.markdown("Key findings from the 5 business case studies with strategic recommendations.")
    st.markdown("---")

    insight_tabs = st.tabs([
        "CS1: Transaction Dynamics",
        "CS2: Device & Engagement",
        "CS3: Insurance Penetration",
        "CS4: Market Expansion",
        "CS5: User Registration",
    ])

    # ── CS1 ──
    with insight_tabs[0]:
        st.markdown("### 🏦 Case Study 1: Decoding Transaction Dynamics")
        col_l, col_r = st.columns(2)
        with col_l:
            df_cs1 = run("""
                SELECT state, SUM(transaction_amount) AS total_amount
                FROM   aggregated_transaction GROUP BY state
                ORDER BY total_amount DESC LIMIT 10
            """)
            df_cs1 = clean_state(df_cs1)
            fig = px.bar(df_cs1, x="total_amount", y="state", orientation="h",
                         color="total_amount", color_continuous_scale="Purples",
                         title="Top 10 States by Transaction Amount",
                         labels={"total_amount": "Amount (₹)", "state": "State"})
            fig.update_layout(yaxis={"categoryorder": "total ascending"},
                               plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               font_color="#2d0060", coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
        with col_r:
            st.markdown("#### 💡 Key Findings")
            st.success("✅ Maharashtra, Karnataka & Telangana drive 60%+ of value")
            st.success("✅ Merchant payments growing fastest — overtaking P2P")
            st.success("✅ Q4 is peak season (festive + year-end bonuses)")
            st.warning("⚠️ Northern states underperform vs population size")
            st.warning("⚠️ Financial Services still <5% of total volume")
            st.markdown("#### 🎯 Recommendations")
            st.info("1. Launch premium products in Maharashtra & Karnataka first")
            st.info("2. Accelerate merchant onboarding with zero-MDR incentives")
            st.info("3. Plan festive campaigns for Q3-Q4 with higher budgets")
            st.info("4. Develop vernacular UX for northern states")

    # ── CS2 ──
    with insight_tabs[1]:
        st.markdown("### 📱 Case Study 2: Device Dominance & User Engagement")
        col_l, col_r = st.columns(2)
        with col_l:
            df_cs2 = run("""
                SELECT brand, SUM(user_count) AS total_users
                FROM   aggregated_user WHERE brand != 'Others'
                GROUP BY brand ORDER BY total_users DESC LIMIT 10
            """)
            fig = px.pie(df_cs2, names="brand", values="total_users",
                         title="Device Brand Distribution",
                         hole=0.4,
                         color_discrete_sequence=px.colors.sequential.Purples_r)
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               font_color="#2d0060")
            st.plotly_chart(fig, use_container_width=True)
        with col_r:
            st.markdown("#### 💡 Key Findings")
            st.success("✅ Xiaomi dominates — 30%+ of PhonePe users")
            st.success("✅ Samsung & Vivo together cover another ~35%")
            st.success("✅ Apple growing — premium user segment emerging")
            st.warning("⚠️ Most users on budget devices (≤4GB RAM)")
            st.warning("⚠️ Large states like UP have low engagement ratios")
            st.markdown("#### 🎯 Recommendations")
            st.info("1. Prioritize Xiaomi, Samsung, Vivo in QA testing")
            st.info("2. Introduce 'Lite Mode' for sub-4GB RAM devices")
            st.info("3. Re-engagement campaigns in low-engagement states")
            st.info("4. Use high-engagement states (Goa, Chandigarh) as beta markets")

    # ── CS3 ──
    with insight_tabs[2]:
        st.markdown("### 🛡️ Case Study 3: Insurance Penetration & Growth")
        col_l, col_r = st.columns(2)
        with col_l:
            df_cs3 = run("""
                SELECT year::text || ' Q' || quarter::text AS period,
                       SUM(insurance_amount) AS total_amount
                FROM   aggregated_insurance
                GROUP BY year, quarter ORDER BY year, quarter
            """)
            fig = px.area(df_cs3, x="period", y="total_amount",
                          title="Insurance Growth Trajectory",
                          labels={"total_amount": "Amount (₹)", "period": "Period"},
                          line_shape="spline")
            fig.update_traces(fill="tozeroy", line_color="#10b981",
                              fillcolor="rgba(16,185,129,0.15)")
            fig.update_layout(xaxis_tickangle=-45,
                               plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               font_color="#2d0060")
            st.plotly_chart(fig, use_container_width=True)
        with col_r:
            st.markdown("#### 💡 Key Findings")
            st.success("✅ Exponential insurance growth since 2022")
            st.success("✅ Q4 is peak for insurance (tax-saving season)")
            st.warning("⚠️ Penetration <1% in every state — massive gap")
            st.warning("⚠️ North-eastern states nearly untouched")
            st.markdown("#### 🎯 Recommendations")
            st.info("1. Scale insurer partnerships immediately")
            st.info("2. In-app nudges post-payment transactions")
            st.info("3. 80C tax-saving campaigns Oct-Dec every year")
            st.info("4. Micro-insurance (₹1/day) for rural & NE states")

    # ── CS4 ──
    with insight_tabs[3]:
        st.markdown("### 🗺️ Case Study 4: Transaction Analysis for Market Expansion")
        col_l, col_r = st.columns(2)
        with col_l:
            df_cs4 = run("""
                SELECT state, district,
                       SUM(transaction_amount) AS total_amount,
                       SUM(transaction_count)  AS total_count,
                       ROUND((SUM(transaction_amount)::numeric /
                              NULLIF(SUM(transaction_count),0)), 2) AS avg_val
                FROM   map_transaction
                GROUP BY state, district
                ORDER BY total_amount DESC LIMIT 20
            """)
            df_cs4 = clean_state(df_cs4)
            df_cs4["district"] = df_cs4["district"].str.title()
            fig = px.scatter(df_cs4, x="total_count", y="total_amount",
                             size="avg_val", color="state",
                             hover_name="district",
                             title="Top 20 Districts — Amount vs Count vs Avg Value",
                             labels={"total_count": "Count", "total_amount": "Amount (₹)"})
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               font_color="#2d0060")
            st.plotly_chart(fig, use_container_width=True)
        with col_r:
            st.markdown("#### 💡 Key Findings")
            st.success("✅ Bengaluru Urban & Mumbai are top districts by far")
            st.success("✅ Clear Pareto effect — top 10 pincodes drive huge volume")
            st.warning("⚠️ Many districts: high count but low avg value")
            st.warning("⚠️ Low-activity districts lack digital infrastructure")
            st.markdown("#### 🎯 Recommendations")
            st.info("1. Dedicated RMs for top 50 pincodes nationally")
            st.info("2. BNPL / UPI Credit for high-count low-value districts")
            st.info("3. Offline agent networks for low-activity districts")
            st.info("4. Double merchant incentives in high-growth states")

    # ── CS5 ──
    with insight_tabs[4]:
        st.markdown("### 👥 Case Study 5: User Registration Analysis")
        col_l, col_r = st.columns(2)
        with col_l:
            df_cs5 = run("""
                SELECT year::text || ' Q' || quarter::text AS period,
                       SUM(registered_users) AS registered,
                       SUM(app_opens)        AS opens
                FROM   map_user
                GROUP BY year, quarter ORDER BY year, quarter
            """)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_cs5["period"], y=df_cs5["registered"],
                                     name="Registered Users", mode="lines+markers",
                                     line=dict(color="#4a0d96", width=2)))
            fig.add_trace(go.Scatter(x=df_cs5["period"], y=df_cs5["opens"],
                                     name="App Opens", mode="lines+markers",
                                     line=dict(color="#f59e0b", width=2)))
            fig.update_layout(title="Registrations vs App Opens — Engagement Gap",
                               xaxis_tickangle=-45,
                               plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               font_color="#2d0060")
            st.plotly_chart(fig, use_container_width=True)
        with col_r:
            st.markdown("#### 💡 Key Findings")
            st.success("✅ Maharashtra & Karnataka lead registrations every quarter")
            st.success("✅ Small urban states (Goa, Chandigarh) have best engagement")
            st.warning("⚠️ Registration-to-activation gap is widening over time")
            st.warning("⚠️ Urban saturation risk — rural expansion needed")
            st.markdown("#### 🎯 Recommendations")
            st.info("1. 48-hour activation funnel with auto re-engagement")
            st.info("2. Weekly state-level engagement ratio alerts")
            st.info("3. 'PhonePe for Bharat' rural expansion program")
            st.info("4. Post-festive activation campaigns in January")

    st.markdown("---")
    st.markdown("### 🏁 Overall Strategic Priority Order")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("""
        <div style='background:#1e1e3a;border:1px solid #5a189a;border-radius:12px;padding:16px;text-align:center'>
        <h2>🔑</h2><b style='color:#c77dff'>Re-engage</b><br>
        <small style='color:#9d9db4'>Dormant registered users<br>Immediate revenue</small>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background:#1e1e3a;border:1px solid #5a189a;border-radius:12px;padding:16px;text-align:center'>
        <h2>🏪</h2><b style='color:#c77dff'>Merchants</b><br>
        <small style='color:#9d9db4'>Fastest growing segment<br>Accelerate onboarding</small>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='background:#1e1e3a;border:1px solid #5a189a;border-radius:12px;padding:16px;text-align:center'>
        <h2>🛡️</h2><b style='color:#c77dff'>Insurance</b><br>
        <small style='color:#9d9db4'>Highest margin opportunity<br>Scale cross-sell</small>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div style='background:#1e1e3a;border:1px solid #5a189a;border-radius:12px;padding:16px;text-align:center'>
        <h2>🌾</h2><b style='color:#c77dff'>Rural</b><br>
        <small style='color:#9d9db4'>PhonePe for Bharat<br>Long-term scale</small>
        </div>""", unsafe_allow_html=True)
    with col5:
        st.markdown("""
        <div style='background:#1e1e3a;border:1px solid #5a189a;border-radius:12px;padding:16px;text-align:center'>
        <h2>📱</h2><b style='color:#c77dff'>App Perf</b><br>
        <small style='color:#9d9db4'>Device optimization<br>Improve retention</small>
        </div>""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#9d9db4; padding:10px;'>
    💜 PhonePe Transaction Insights Dashboard |
    Built with Streamlit + PostgreSQL + Plotly |
    Labmentix Data Science Internship
</div>
""", unsafe_allow_html=True)