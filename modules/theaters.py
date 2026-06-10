import streamlit as st
import plotly.express as px
import pandas as pd
from utils.ui import kpi, top_card, chart_card, filter_start, filter_end

def show(df):
    st.markdown('<h1 style="font-size:45px; font-weight: 900; text-align:center; margin-bottom: 30px;"> Theater<span style="color: #E50914;">Performance</span> </h1>', unsafe_allow_html=True) 

    # ---------------- CLEAN COLUMN NAMES ----------------
    df = df.copy()
    df.columns = df.columns.str.strip()

    # ---------------- DETECT COLUMNS SAFELY ----------------
    cat_cols = df.select_dtypes(include='object').columns
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns

    if len(cat_cols) == 0 or len(num_cols) == 0:
        st.error("❌ Dataset structure is invalid. Requires at least two Text columns and one Numeric column.")
        return

    # 🔥 SMART DETECTION
    theater_col = None
    location_col = None

    for col in cat_cols:
        col_lower = col.lower()
        if any(x in col_lower for x in ["theater", "theatre", "cinema", "chain"]):
            theater_col = col
        elif any(x in col_lower for x in ["city", "location"]):
            location_col = col

    # Fallbacks (guaranteed working)
    if theater_col is None:
        theater_col = cat_cols[0]
    if location_col is None:
        location_col = cat_cols[1] if len(cat_cols) > 1 else cat_cols[0]

    revenue_col = num_cols[0]

    # ---------------- CLEAN DATA ----------------
    df = df[[theater_col, location_col, revenue_col]].dropna()

    # ---------------- AGGREGATE ----------------
    agg_df = df.groupby([theater_col, location_col])[revenue_col].sum().reset_index()

    if agg_df.empty:
        st.warning("No usable data available.")
        return

    # ---------------- WORKABLE CASCADING FILTERS ----------------
    filter_start()
    col1, col2 = st.columns(2)

    location_filter = col1.multiselect(
        "📍 Select City / Location",
        sorted(agg_df[location_col].unique()),
        placeholder="All Cities"
    )

    theater_filter = col2.multiselect(
        "🏢 Select Theater Chain",
        sorted(agg_df[theater_col].unique()),
        placeholder="All Theaters"
    )
    filter_end()

    # Apply filters dynamically
    if location_filter:
        agg_df = agg_df[agg_df[location_col].isin(location_filter)]
    if theater_filter:
        agg_df = agg_df[agg_df[theater_col].isin(theater_filter)]

    if agg_df.empty:
        st.warning("⚠️ No metrics found for this specific configuration.")
        return

    # ---------------- TOP THEATER PROFILE CARD ----------------
    top = agg_df.loc[agg_df[revenue_col].idxmax()]
    top_card(
        "🏆 Top Performing Location",
        f"{top[theater_col]} ({top[location_col]})",
        int(top[revenue_col])
    )
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

    # ---------------- REFINED PROFESSIONAL KPI STRIP ----------------
    c1, c2 = st.columns(2)
    with c1:
        kpi("Active Locations", agg_df[theater_col].nunique())
    with c2:
        kpi("Aggregated Revenue", f"₹ {int(agg_df[revenue_col].sum()):,}")

    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)

# ---------------- 2-CHART MASTER STRATEGIC VIEW ----------------
    st.markdown("### 📊 Enterprise Theater Analytics")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # --- CHART 1: DYNAMIC GRADIENT HORIZONTAL BAR ---
        # Safeguard: Force columns to correct types and take top 10 rows
        top10 = agg_df.sort_values(revenue_col, ascending=False).head(10).copy()
        top10[theater_col] = top10[theater_col].astype(str).str.strip()
        top10[revenue_col] = pd.to_numeric(top10[revenue_col], errors='coerce')

        fig_bar = px.bar(
            top10,
            x=revenue_col,
            y=theater_col,
            orientation='h',
            title="🎯 Top 10 Branches by Revenue Gross",
            color=revenue_col,
            # Continuous gradient scaling from deep blue to cinematic red
            color_continuous_scale=["#1e3a8a", "#3b82f6", "#b91c1c", "#e50914"],
            template="plotly_dark"
        )
        
        # Clean up individual bar attributes
        fig_bar.update_traces(
            marker_line_width=0,
            opacity=0.9,
            hovertemplate="<b>Theater:</b> %{y}<br><b>Gross:</b> ₹%{x:,}<extra></extra>"
        )
        
        # Layout tuning for high-end scannability
        fig_bar.update_layout(
            coloraxis_showscale=False,
            margin=dict(t=50, b=40, l=10, r=20), # Tightened margins for breathing room
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(title="", showgrid=False, categoryorder='total ascending', tickmode='linear'),
            xaxis=dict(title="Revenue (₹)", showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=False),
            title_font=dict(size=18, family="sans-serif", color="white")
        )
        
        # Render using Streamlit's native responsive container with custom config toolbar hidden
        with st.container():
            chart_card(fig_bar)

    with chart_col2:
        # --- CHART 2: PREMIUM HIGH-CONTRAST DONUT ---
        # Safeguard: Group and cast elements cleanly
        city_perf = agg_df.groupby(location_col)[revenue_col].sum().reset_index()
        city_perf[location_col] = city_perf[location_col].astype(str).str.strip()
        city_perf[revenue_col] = pd.to_numeric(city_perf[revenue_col], errors='coerce')
        
        fig_donut = px.pie(
            city_perf,
            names=location_col,
            values=revenue_col,
            hole=0.6, # Sleek corporate cut-out look
            title="🌍 Regional Market Share Distribution",
            # Distinct, highly visible operational colors
            color_discrete_sequence=["#E50914", "#3b82f6", "#10b981", "#f59e0b", "#8b5cf6"],
            template="plotly_dark"
        )
        
        # Pull text labels completely outward to eliminate ugly inner-slice clustering
        fig_donut.update_traces(
            textposition="outside",
            textinfo="percent+label",
            marker=dict(line=dict(color="#121212", width=2)), # Thick clean separation lines
            hovertemplate="<b>City:</b> %{label}<br><b>Total Gross:</b> ₹%{value:,}<br><b>Share:</b> %{percent}<extra></extra>"
        )
        
        fig_donut.update_layout(
            margin=dict(t=50, b=40, l=40, r=40),
            showlegend=False, # Hidden since text labels look much cleaner pointing directly to slices
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            title_font=dict(size=18, family="sans-serif", color="white")
        )
        
        with st.container():
            chart_card(fig_donut)

    # ---------------- SMART CONTEXTUAL INSIGHT ----------------
    st.markdown("<br>", unsafe_allow_html=True)
    best_city = city_perf.sort_values(revenue_col, ascending=False).iloc[0][location_col]
    st.info(
        f"💡 **Operational Insight:** Regional diagnostic shows **{best_city}** as the highest revenue-generating market hub. "
        f"Allocated cinema infrastructures inside this perimeter dominate your active dashboard matrices."
    )   
