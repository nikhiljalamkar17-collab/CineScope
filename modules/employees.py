import streamlit as st
import plotly.express as px
import pandas as pd
from utils.ui import kpi, top_card, chart_card, filter_start, filter_end

def show(df):
    st.markdown('<h1 style="font-size:45px; font-weight: 900; text-align:center; margin-bottom: 30px;"> Staff<span style="color: #E50914;">Performance</span> </h1>', unsafe_allow_html=True) 

    # ---------------- COLUMN DETECTION ----------------
    df = df.copy()
    df.columns = df.columns.str.strip()

    cat_cols = df.select_dtypes(include='object').columns
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns

    if len(cat_cols) == 0 or len(num_cols) == 0:
        st.error("❌ Dataset structure is invalid. Requires text columns and at least one metric column.")
        return

    # Smart Mappings
    emp_name = cat_cols[0]
    dept_col = "Department" if "Department" in df.columns else cat_cols[1]
    performance_col = num_cols[0]

    # Smart Designation Tracking
    desig_col = next((c for c in cat_cols if "designation" in c.lower() or "role" in c.lower() or "title" in c.lower()), None)
    if not desig_col and len(cat_cols) > 2:
        desig_col = cat_cols[2]

    # Optional columns
    salary_col = next((col for col in num_cols if "salary" in col.lower()), None)

    # ---------------- 3-WAY CASCADING WORKABLE FILTERS ----------------
    filter_start()
    col1, col2, col3 = st.columns(3)

    # 1. Select Department
    available_depts = sorted(df[dept_col].astype(str).unique())
    selected_dept = col1.selectbox("🏢 Department Unit", ["All Departments"] + available_depts)

    # Slice for Designation Dropdown
    temp_df = df.copy()
    if selected_dept != "All Departments":
        temp_df = temp_df[temp_df[dept_col].astype(str) == selected_dept]

    # 2. Select Designation (New Filter Slot)
    if desig_col:
        available_desigs = sorted(temp_df[desig_col].astype(str).unique())
        selected_desig = col2.selectbox("💼 Designation Profile", ["All Designations"] + available_desigs)
        if selected_desig != "All Designations":
            temp_df = temp_df[temp_df[desig_col].astype(str) == selected_desig]
    else:
        col2.markdown("<p style='opacity:0.4; padding-top:25px;'>No Designation Found</p>", unsafe_allow_html=True)
        selected_desig = "All Designations"

    # 3. Focus Employee Dropdown
    available_emps = sorted(temp_df[emp_name].astype(str).unique())
    selected_emp = col3.selectbox("👤 Focus Employee", ["Global Overview"] + available_emps)
    filter_end()

    # --- APPLY FILTER MUTATIONS TO MASTER DATAFRAME ---
    if selected_dept != "All Departments":
        df = df[df[dept_col].astype(str) == selected_dept]
    if desig_col and selected_desig != "All Designations":
        df = df[df[desig_col].astype(str) == selected_desig]
    if selected_emp != "Global Overview":
        df = df[df[emp_name].astype(str) == selected_emp]

    if df.empty:
        st.warning("⚠️ Zero staff records match this specific parameters layout.")
        return

    # ---------------- CONSOLIDATED METRIC DOSSIER CARD ----------------
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    if selected_emp != "Global Overview":
        emp_stats = df.iloc[0]
        desig_label = f" | Role: {emp_stats[desig_col]}" if desig_col else ""
        top_card(
            f"PROFESSIONAL DOSSIER: {selected_emp}", 
            f"{int(emp_stats[performance_col])} SCORE POINTS", 
            f"UNIT: {emp_stats[dept_col]}{desig_label}"
        )
    else:
        top_unit_emp = df.loc[df[performance_col].idxmax()]
        view_label = "GLOBAL TOP PERFORMER" if selected_dept == "All Departments" else f"TOP VALUE DRIVER IN {selected_dept}"
        top_card(
            view_label, 
            str(top_unit_emp[emp_name]), 
            f"Leading operations with {int(top_unit_emp[performance_col])} Matrix Points"
        )

    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

    # ---------------- REFINED PROFESSIONAL KPI STRIP ----------------
    c1, c2, c3 = st.columns(3)
    with c1:
        kpi("Monitored Roster", df.shape[0])
    with c2:
        kpi("Mean Performance Score", f"{round(df[performance_col].mean(), 1)} Pts")
    with c3:
        kpi("Peak Resource Output", f"{int(df[performance_col].max())} Pts")

    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)

    # ---------------- 2-CHART HIGH-IMPACT LAYOUT ----------------
    st.markdown("### 📊 Workforce Performance Intelligence")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # --- CHART 1: NEON GRADIENT HORIZONTAL BAR CHART ---
        # Logic: Horizontal charts keep long employee names perfectly un-crushed and easy to compare side-by-side
        top10 = df.sort_values(performance_col, ascending=False).head(10).copy()
        top10[emp_name] = top10[emp_name].astype(str).str.strip()
        top10[performance_col] = pd.to_numeric(top10[performance_col], errors='coerce')

        fig_bar = px.bar(
            top10,
            x=performance_col,
            y=emp_name,
            orientation='h',
            title="🎯 Top 10 Personnel Roster Rank",
            color=performance_col,
            color_continuous_scale=["#1e3a8a", "#3b82f6", "#b91c1c", "#e50914"], # Deep Cyberpunk Neon Glow
            template="plotly_dark"
        )
        fig_bar.update_traces(
            marker_line_width=0,
            opacity=0.92,
            hovertemplate="<b>Employee:</b> %{y}<br><b>Output Score:</b> %{x} Pts<extra></extra>"
        )
        fig_bar.update_layout(
            coloraxis_showscale=False,
            margin=dict(t=50, b=40, l=10, r=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(title="", showgrid=False, categoryorder='total ascending', tickmode='linear'),
            xaxis=dict(title="Performance Points", showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=False),
            title_font=dict(size=18, family="sans-serif", color="white")
        )
        chart_card(fig_bar)

    with chart_col2:
        # --- CHART 2: PREMIUM BUSINESS CUTOUT DONUT CHART ---
        # Logic: Aggregates weights visually so anyone visiting understands exactly which segment handles the volume
        dept_perf = df.groupby(dept_col)[performance_col].mean().reset_index()
        dept_perf[dept_col] = dept_perf[dept_col].astype(str).str.strip()
        dept_perf[performance_col] = pd.to_numeric(dept_perf[performance_col], errors='coerce')

        fig_donut = px.pie(
            dept_perf,
            names=dept_col,
            values=performance_col,
            hole=0.65,
            title="🏢 Departmental Contribution Density",
            color_discrete_sequence=["#E50914", "#3b82f6", "#10b981", "#f59e0b", "#8b5cf6"],
            template="plotly_dark"
        )
        fig_donut.update_traces(
            textposition="outside",
            textinfo="percent+label",
            marker=dict(line=dict(color="#121212", width=2)),
            hovertemplate="<b>Department:</b> %{label}<br><b>Avg Matrix:</b> %{value:.1f} Pts<extra></extra>"
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
    best_dept = dept_perf.sort_values(performance_col, ascending=False).iloc[0][dept_col]
    st.info(
        f"💡 **Operational Insight:** Roster metrics identify **{best_dept}** as the primary efficiency cluster. "
        f"Personnel under this designation and branch represent the strongest operational thresholds on your dashboard canvas."
    )