import streamlit as st

def kpi(label, value):
    # Added flex-direction and min-height to ensure the nameplate looks balanced
    st.markdown(f"""
        <div class="kpi-card" style="min-height: 120px; display: flex; flex-direction: column; justify-content: center;">
            <p style="margin:0; font-size:14px; font-weight: 600; opacity: 0.8; text-transform: uppercase; letter-spacing: 1.5px; line-height: 1.2;">
                {label}
            </p>
            <h2 style="margin: 10px 0 0 0; font-size: 32px; color: #E50914; font-weight: 800;">
                {value}
            </h2>
        </div>
    """, unsafe_allow_html=True)

def system_live():
    # Styled to be a full-width bar at the top of the content area
    st.markdown("""
        <div class="system-status" style="display: flex; justify-content: space-between; padding: 10px 30px; 
                    background: rgba(229, 9, 20, 0.05); border-radius: 50px; 
                    border: 1px solid rgba(229, 9, 20, 0.2); margin-bottom: 30px;">
            <span style="color: #E50914; font-size: 12px; font-weight: 700;">● SYSTEM LIVE</span>
            <span style="color: #E50914; font-size: 12px; font-weight: 700;">ACTIVE</span>
        </div>
    """, unsafe_allow_html=True)

def top_card(title, main_val, sub_val):
    st.markdown(f"""
        <div class="top-card">
            <h4 style="margin:0; opacity:0.8; font-weight:400;">{title}</h4>
            <h1 style="margin:10px 0; font-size:45px; font-weight:700;">{main_val}</h1>
            <p style="margin:0; font-size:16px; background:rgba(255,255,255,0.15); 
               display:inline-block; padding:4px 15px; border-radius:30px;">{sub_val}</p>
        </div>
    """, unsafe_allow_html=True)

def chart_card(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="white",
        hovermode="x unified",
        margin=dict(l=10, r=10, t=50, b=10)
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

def nav_gateway(icon, title, desc):
    return f"""
        <div class="glass-nav-card">
            <h1 style="font-size: 50px; margin-bottom: 15px;">{icon}</h1>
            <h3 style="margin-bottom: 10px;">{title}</h3>
            <p style="font-size: 14px; opacity: 0.6; line-height: 1.6;">{desc}</p>
        </div>
    """

def filter_start():
    st.markdown('<div class="filter-box">', unsafe_allow_html=True)

def filter_end():
    st.markdown('</div>', unsafe_allow_html=True)