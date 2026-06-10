import streamlit as st
import plotly.express as px
import pandas as pd
from utils import ui

def show(data, nav_func):
    # --- PREMIUM HERO HEADER ---
    st.markdown("""
        <div class="premium-hero">
            <h1>CINE<span style="color:#E50914;">SCOPE</span></h1>
            <p style="font-size:20px; color:#999; letter-spacing:5px; margin-top:5px;">ENTERPRISE INTELLIGENCE SYSTEM</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align:center; color:#A03D04; font-size:18px;'>SELECT OPERATIONAL GATEWAY</h2>", unsafe_allow_html=True)
    
    # --- NAVIGATION GATEWAYS: ROW 1 ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(ui.nav_gateway("🎬", "Content Studio", "Box Office ROI and Industry Analysis."), unsafe_allow_html=True)
        if st.button("Enter Studio", key="mov_gate"): nav_func("Movies")
    with c2:
        st.markdown(ui.nav_gateway("🍿", "Retail Center", "Inventory and Concession Sales."), unsafe_allow_html=True)
        if st.button("Enter Retail", key="food_gate"): nav_func("Food")
    with c3:
        st.markdown(ui.nav_gateway("🏢", "Theaters", "Site Performance and Location ROI."), unsafe_allow_html=True)
        if st.button("Enter Assets", key="theat_gate"): nav_func("Theaters")

    # --- NAVIGATION GATEWAYS: ROW 2 ---
    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown(ui.nav_gateway("👥", "Visitor Hub", "Footfall Patterns and Audience."), unsafe_allow_html=True)
        if st.button("Enter Audience", key="visit_gate"): nav_func("Visitors")
    with c5:
        st.markdown(ui.nav_gateway("👨‍💼", "Workforce", "KPI Tracking and Team Stats."), unsafe_allow_html=True)
        if st.button("Enter Management", key="emp_gate"): nav_func("Employees")
    with c6:
        st.markdown(ui.nav_gateway("⚙️", "Settings", "System Configuration."), unsafe_allow_html=True)
        st.button("Restricted", key="lock_gate", disabled=True)

     