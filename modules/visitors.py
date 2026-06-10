import streamlit as st
import plotly.express as px
import pandas as pd
from utils.ui import kpi, chart_card, filter_start, filter_end

def show(df):
    st.markdown('<h1 style="font-size:45px; font-weight: 900; text-align:center; margin-bottom: 30px;"> Audience<span style="color: #E50914;">Intelligence</span> </h1>', unsafe_allow_html=True) 

    # ---------------- GLOBAL DATA PREPARATION ----------------
    df = df.copy()
    df.columns = df.columns.str.strip()
    
    # Matching your utils/loader.py output keys perfectly
    visitor_col = "Tickets_Booked" if "Tickets_Booked" in df.columns else "Tickets Booked"
    name_col = "Visitors Name"
    theater_col = "Theater Name"

    # Fallback checks to prevent crashes if column keys mismatch
    if theater_col not in df.columns:
        # Fallback to look for lowercase if needed
        theater_col = next((c for c in df.columns if "theater" in c.lower() or "theatre" in c.lower()), df.columns[1])
    if name_col not in df.columns:
        name_col = df.columns[0]
    if visitor_col not in df.columns:
        num_cols = df.select_dtypes(include=['int64', 'float64']).columns
        visitor_col = num_cols[0] if len(num_cols) > 0 else df.columns[-1]

    # ---------------- SINGLE CLEAN FILTER CONFIGURATION ----------------
    filter_start()
    
    # One clean multiselect box that perfectly binds to both charts
    theater_options = sorted(df[theater_col].astype(str).unique())
    selected_theater = st.multiselect("🏢 Select Theater Location", theater_options, placeholder="All Theaters")
    
    filter_end()

    # --- APPLY FILTER STATE ---
    if selected_theater:
        df = df[df[theater_col].astype(str).isin(selected_theater)]

    if df.empty:
        st.warning("⚠️ Zero metrics found for this specific query parameters.")
        return

    # ---------------- MONITORING STATUS HEADLINE ----------------
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 25px;">
            <h2 style="color: #E50914; margin: 0; font-size: 20px; font-weight: 700; letter-spacing: 1px;">GLOBAL AUDIENCE MONITORING STATUS</h2>
        </div>
    """, unsafe_allow_html=True)

    # ---------------- REFINED PROFESSIONAL KPI STRIP ----------------
    c1, c2, c3 = st.columns(3)
    with c1:
        kpi("Aggregated Visits", f"{int(df[visitor_col].sum()):,}")
    with c2:
        kpi("Peak Single Activity", f"{int(df[visitor_col].max()):,}")
    with c3:
        kpi("Visitor Rating", "⭐⭐⭐⭐")

    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)

    # ---------------- HIGH-TECH INTERACTIVE MASTER CHARTS ----------------
    st.markdown("### 📊 Enterprise Audience Metrics")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # --- CHART 1: GRADIENT GLOW VERTICAL BAR ---
        top_chart_data = df.sort_values(visitor_col, ascending=False).head(10)
        fig_bar = px.bar(
            top_chart_data,
            x=name_col,
            y=visitor_col,
            title="🎯 Top Visitor Traffic Footprint",
            color=visitor_col,
            color_continuous_scale=["#3a0709", "#800c11", "#e50914", "#ff4d5a"], 
            template="plotly_dark"
        )
        
        fig_bar.update_traces(
            marker_line_width=0, 
            opacity=0.95,
            hovertemplate="<b>Visitor:</b> %{x}<br><b>Footfall:</b> %{y:,}<extra></extra>"
        )
        fig_bar.update_layout(
            coloraxis_showscale=False,
            margin=dict(t=50, b=40, l=40, r=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="", showgrid=False, tickangle=-15),
            yaxis=dict(title="Footfall Count", showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=False),
            title_font=dict(size=18, family="sans-serif", color="white")
        )
        chart_card(fig_bar)

    with chart_col2:
        # --- CHART 2: PREMIUM DONUT MIX ---
        pie_data = df.groupby(theater_col)[visitor_col].sum().reset_index()
        fig_pie = px.pie(
            pie_data,
            names=theater_col,
            values=visitor_col,
            hole=0.6, 
            title="🏢 Theater Volume Contribution Share",
            color_discrete_sequence=["#E50914", "#B00710", "#78050B", "#ff4d5a", "#4A0205"], 
            template="plotly_dark"
        )
        
        fig_pie.update_traces(
            textposition="outside", 
            textinfo="percent+label",
            marker=dict(line=dict(color="#121212", width=2)),
            hovertemplate="<b>Theater:</b> %{label}<br><b>Total Visits:</b> %{value:,}<br><b>Share:</b> %{percent}<extra></extra>"
        )
        fig_pie.update_layout(
            margin=dict(t=50, b=40, l=30, r=30),
            showlegend=False, 
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            title_font=dict(size=18, family="sans-serif", color="white")
        )
        chart_card(fig_pie)

    # ---------------- SMART CONTEXTUAL INSIGHT ----------------
    st.markdown("<br>", unsafe_allow_html=True)
    top_global = df.sort_values(visitor_col, ascending=False).iloc[0]
    st.info(f"💡 **Global Intel:** High-density node detected. Prime driver is **{top_global[name_col]}** at **{top_global[theater_col]}** with an execution footprint of **{int(top_global[visitor_col]):,}**.")