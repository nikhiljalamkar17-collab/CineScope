import streamlit as st
import plotly.express as px
import pandas as pd
from utils.ui import kpi, top_card, chart_card, filter_start, filter_end

def show(df):

    st.markdown('<h1 style=" font-size:45px; font-weight: 900; text-align:center;"> Inventory<span style="color: #E50914;">Insights</span> </h1>', unsafe_allow_html=True) 

    # ---------------- COLUMN DETECTION ----------------
    cat_cols = df.select_dtypes(include='object').columns
    num_cols = df.select_dtypes(include=['int','float']).columns

    if len(cat_cols) == 0 or len(num_cols) == 0:
        st.error("Dataset not suitable for analysis")
        return

    # Logical assumptions
    item_col = cat_cols[0]     # Item Name
    category_col = cat_cols[1] if len(cat_cols) > 1 else cat_cols[0]
    value_col = num_cols[0]    # Sales / Revenue

    # ---------------- FILTERS ----------------
    filter_start()

    col1, col2 = st.columns(2)

    category_filter = col1.multiselect(
        "Select city",
        df[category_col].unique(),
        help="Filter by food category (Popcorn, Drinks, etc.)"
    )

    item_filter = col2.multiselect(
        "Select Items",
        df[item_col].unique(),
        help="Select specific items"
    )

    filter_end()

    # Apply filters
    if category_filter:
        df = df[df[category_col].isin(category_filter)]

    if item_filter:
        df = df[df[item_col].isin(item_filter)]

    if df.empty:
        st.warning("No data after applying filters")
        return

    # ---------------- TOP ITEM ----------------
    top = df.loc[df[value_col].idxmax()]
    top_card("🍿 Top Selling Item", top[item_col], int(top[value_col]))
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

    # ---------------- KPI ----------------
    c1, c2 = st.columns(2)

    with c1:
        kpi("Total Items", df.shape[0])

    with c2:
        kpi("Total Sales", int(df[value_col].sum()))

    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

    # ---------------- CHARTS ----------------
    st.markdown("### 📦 Inventory & Sales Performance")

    # Clean data first to ensure no nulls break the hierarchy for the treemap
    tree_df = df.dropna(subset=[category_col, item_col, value_col])

    # Dynamic columns setup to hold our 2 selected charts
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # Chart 2: Category Revenue Breakdown (Donut)
        fig_pie = px.pie(
            df,
            names=category_col,
            values=value_col,
            hole=0.5,
            title="Revenue Distribution by Category",
            color_discrete_sequence=px.colors.sequential.YlOrRd,
            template="plotly_dark"
        )
        fig_pie.update_traces(textinfo='percent+label')
        chart_card(fig_pie)

    with chart_col2:
        # Chart 3: Item Concentration (Treemap)
        if not tree_df.empty:
            fig_tree = px.treemap(
                tree_df,
                path=[px.Constant("All Inventory"), category_col, item_col], 
                values=value_col,
                title="Inventory Hierarchy: Sales Weight",
                color=value_col,
                color_continuous_scale="RdGy",
                template="plotly_dark"
            )
            fig_tree.update_traces(marker=dict(cornerradius=5)) 
            chart_card(fig_tree)
        else:
            st.warning("Insufficient data for Treemap")

    # ---------------- INSIGHT ----------------
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    st.info(
        f"Top category contributing most revenue: "
        f"{df.groupby(category_col)[value_col].sum().idxmax()}"
    )
