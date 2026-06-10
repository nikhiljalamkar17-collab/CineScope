import streamlit as st
import plotly.express as px
import pandas as pd
from utils.ui import kpi, top_card, chart_card, filter_start, filter_end

# ---------------- FORMAT FUNCTION ----------------
def format_currency(x):
    if abs(x) >= 1e7:
        return f"₹ {x/1e7:.2f} Cr"
    elif abs(x) >= 1e5:
        return f"₹ {x/1e5:.2f} L"
    else:
        return f"₹ {int(x)}"


def show(df):
 
    st.markdown('<h1 style=" font-size:45px; font-weight: 900; text-align:center;"> Movies<span style="color: #E50914;">Intelligence</span> </h1>', unsafe_allow_html=True) 

    # ---------------- CLEAN ----------------
    df = df.copy()
    df.columns = df.columns.str.strip()

    # ---------------- COLUMN DETECTION ----------------
    cat_cols = df.select_dtypes(include='object').columns
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns

    movie_col = cat_cols[0]
    genre_col = next((c for c in cat_cols if "genre" in c.lower()), cat_cols[0])
    year_col = next((c for c in df.columns if "year" in c.lower()), None)
    industry_col = next((c for c in cat_cols if "industry" in c.lower()), None)

    revenue_col = num_cols[0]
    cost_col = num_cols[1]

    # ---------------- METRICS ----------------
    df["Profit"] = df[revenue_col] - df[cost_col]
    df["Profit_Display"] = df["Profit"].abs()
    df["Profit_Type"] = df["Profit"].apply(lambda x: "Profit" if x >= 0 else "Loss")

    df["ROI"] = (df["Profit"] / df[cost_col]).replace([float('inf'), -float('inf')], 0)
    df["Profit_Margin"] = (df["Profit"] / df[revenue_col]).replace([float('inf'), -float('inf')], 0)

    df["Verdict"] = df["Profit"].apply(lambda x: "Hit" if x > 0 else "Flop")

    # ---------------- ADVANCED SMART FILTERS ----------------
    filter_start()

    original_df = df.copy()

    # -------- CLEAN FILTER COLUMNS --------
    for col in cat_cols:
        original_df[col] = original_df[col].astype(str)

    c1, c2, c3, c4 = st.columns(4)

    # =========================================================
    # GENRE FILTER
    # =========================================================
    genre_options = sorted(
        original_df[genre_col]
        .dropna()
        .astype(str)
        .unique()
    )

    genre_filter = c1.multiselect(
        "🎭 Select Genre",
        genre_options,
        placeholder="Choose Genre"
    )

    filtered_df = original_df.copy()

    if genre_filter:
        filtered_df = filtered_df[
            filtered_df[genre_col].isin(genre_filter)
        ]

    # =========================================================
    # MOVIE FILTER
    # =========================================================
    movie_options = sorted(
        filtered_df[movie_col]
        .dropna()
        .astype(str)
        .unique()
    )

    movie_filter = c2.multiselect(
        "🎬 Select Movies",
        movie_options,
        placeholder="Choose Movies"
    )

    if movie_filter:
        filtered_df = filtered_df[
            filtered_df[movie_col].isin(movie_filter)
        ]

    # =========================================================
    # YEAR FILTER
    # =========================================================
    if year_col:

        year_options = sorted(
            filtered_df[year_col]
            .dropna()
            .astype(str)
            .unique()
        )

        year_filter = c3.multiselect(
            "📅 Select Year",
            year_options,
            placeholder="Choose Year"
        )

        if year_filter:
            filtered_df = filtered_df[
                filtered_df[year_col]
                .astype(str)
                .isin(year_filter)
            ]

    else:
        year_filter = []

    # =========================================================
    # INDUSTRY FILTER
    # =========================================================
    if industry_col:

        industry_options = sorted(
            filtered_df[industry_col]
            .dropna()
            .astype(str)
            .unique()
        )

        industry_filter = c4.multiselect(
            "🌍 Select Industry",
            industry_options,
            placeholder="Choose Industry"
        )

        if industry_filter:
            filtered_df = filtered_df[
                filtered_df[industry_col]
                .astype(str)
                .isin(industry_filter)
            ]

    else:
        industry_filter = []

    filter_end()

    # =========================================================
    # FINAL FILTERED DATA
    # =========================================================
    df = filtered_df.copy()

    # =========================================================
    # EMPTY CHECK
    # =========================================================
    if df.empty:
        st.warning("⚠️ No data available for selected filters")
        return

    # ---------------- TOP MOVIE (ENHANCED) ----------------
    top = df.loc[df["Profit"].idxmax()]

    performance_tag = "🔥 Blockbuster" if top["ROI"] > 1 else "⚖️ Average"

    top_card(
        "🎬 Top Performing Movie",
        f"{top[movie_col]} ({top[genre_col]})",
        f"{format_currency(top['Profit'])} | ROI: {round(top['ROI']*100,1)}% | {performance_tag}"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------- KPI ----------------
    total_profit = df["Profit"].sum()
    avg_roi = df["ROI"].mean() * 100
    hit_ratio = (df["Verdict"] == "Hit").mean() * 100

    c1, c2 = st.columns(2)

    with c1:
        kpi("Total Movies", df.shape[0])

    with c2:
        kpi("Total Revenue", format_currency(df[revenue_col].sum()))
    # ---------------- CHARTS ----------------
# ---------------- 2-CHART MASTER STRATEGIC VIEW ----------------
    st.markdown("### 📊 Enterprise Movie Analytics")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # --- CHART 1: NEON GRADIENT HORIZONTAL EARNINGS BAR ---
        # Logic: Horizontal bars keep genre names perfectly readable. 
        # The chart naturally groups profitable genres separate from losing genres.
        genre_profit = df.groupby(genre_col)["Profit"].sum().reset_index()
        genre_profit = genre_profit.sort_values("Profit", ascending=False)
        
        # Ensure data types are cast properly to prevent Plotly canvas crashes
        genre_profit[genre_col] = genre_profit[genre_col].astype(str).str.strip()
        genre_profit["Profit"] = pd.to_numeric(genre_profit["Profit"], errors='coerce')

        fig_bar = px.bar(
            genre_profit,
            x="Profit",
            y=genre_col,
            orientation='h',
            title="🎯 Net Financial Yield by Genre",
            color="Profit",
            # Smooth transition from corporate deep blue to cinematic red
            color_continuous_scale=["#1e3a8a", "#3b82f6", "#b91c1c", "#e50914"],
            template="plotly_dark"
        )
        
        # UI Polish: Custom clean tooltips and spacing adjustments
        fig_bar.update_traces(
            marker_line_width=0,
            opacity=0.92,
            hovertemplate="<b>Genre:</b> %{y}<br><b>Net Yield:</b> ₹%{x:,}<extra></extra>"
        )
        fig_bar.update_layout(
            coloraxis_showscale=False,
            margin=dict(t=50, b=40, l=10, r=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(title="", showgrid=False, categoryorder='total ascending', tickmode='linear'),
            xaxis=dict(title="Net Earnings (₹)", showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=False),
            title_font=dict(size=18, family="sans-serif", color="white")
        )
        chart_card(fig_bar)

    with chart_col2:
        # --- CHART 2: PREMIUM BUSINESS CUTOUT DONUT CHART ---
        # Logic: Clean division of regional industry data with outside pointers to avoid crowding.
        if industry_col:
            pie_data = df.groupby(industry_col)[revenue_col].sum().reset_index()
            names_param = industry_col
            title_text = "🌍 Regional Market Share Distribution"
            hover_label = "Industry"
        else:
            pie_data = df.groupby("Verdict")[revenue_col].sum().reset_index()
            names_param = "Verdict"
            title_text = "🎬 Operational Success Ratio Mix"
            hover_label = "Status"

        # Explicit type casting for safety
        pie_data[names_param] = pie_data[names_param].astype(str).str.strip()
        pie_data[revenue_col] = pd.to_numeric(pie_data[revenue_col], errors='coerce')

        fig_donut = px.pie(
            pie_data,
            names=names_param,
            values=revenue_col,
            hole=0.65, # Modern deeper donut hole
            title=title_text,
            color_discrete_sequence=["#E50914", "#3b82f6", "#10b981", "#f59e0b", "#8b5cf6"],
            template="plotly_dark"
        )
        
        # Pull text labels outside to maximize visual breathing room
        fig_donut.update_traces(
            textposition="outside",
            textinfo="percent+label",
            marker=dict(line=dict(color="#121212", width=2)),
            hovertemplate=f"<b>{hover_label}:</b> %{{label}}<br><b>Gross Revenue:</b> ₹%{{value:,}}<br><b>Share:</b> %{{percent}}<extra></extra>"
        )
        fig_donut.update_layout(
            margin=dict(t=50, b=40, l=30, r=30),
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            title_font=dict(size=18, family="sans-serif", color="white")
        )
        chart_card(fig_donut)

    # ---------------- SMART CONTEXTUAL INSIGHT ----------------
    st.markdown("<br>", unsafe_allow_html=True)
    best_genre = df.groupby(genre_col)["Profit"].sum().idxmax()
    worst_genre = df.groupby(genre_col)["Profit"].sum().idxmin()

    st.success(
        f"💡 **Operational Insight:** Portfolio diagnostics identify **{best_genre}** as your highest absolute yield driver, "
        f"while **{worst_genre}** experiences the heaviest capital drag under current selection parameters."
    )
