import streamlit as st
import pandas as pd
import os

def show(logo_base64=None):
    # Hide sidebar, strip top padding, and run at a native 100% viewport resolution
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none !important;
            }
            [data-testid="collapsedSidebarButton"] {
                display: none !important;
            }
            /* Removes the default padding gaps at the very top of the window framework */
            .block-container {
                padding-top: 0rem !important;
                padding-bottom: 1rem !important;
            }
            /* Clean form padding adjustment */
            div[data-testid="stForm"] {
                padding: 20px !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Balanced 3-column layout to center the login interface on high-res monitors
    _, welcome_container, _ = st.columns([0.8, 1.6, 0.8])
    
    with welcome_container:
        # Pull the logo up as high as possible
        st.markdown("<div style='margin-top: 0px;'></div>", unsafe_allow_html=True)
        
        # 🎯 1. High-Fidelity Balanced Logo Placement (Zero margins)
        if logo_base64:
            st.markdown(f"""
                <div style="text-align: center; margin-bottom: 0px; padding-bottom: 0px;">
                    <img src="data:image/png;base64,{logo_base64}" style="width: 450px; height: 450px; object-fit: contain; margin: 0px; padding: 0px;">
                </div>
            """, unsafe_allow_html=True)
        
        # 📜 2. Condensed Sub-Headline & Short Descriptive Pitch
        st.markdown("""
            <div style="text-align: center; margin-top: -110px; margin-bottom: 25px; padding-top: 0px;">
                <p style="font-size: 13px; color: #E50914; letter-spacing: 5px; font-weight: 700; text-transform: uppercase; margin: 0px 0px 8px 0px;">
                    Enterprise Intelligence System
                </p>
                <p style="font-size: 14px; color: #888; line-height: 1.5; max-width: 500px; margin: 0 auto;">
                    Welcome to your operational command hub. Step inside to unlock real-time movie economics, concessions inventory, and multi-site venue performance.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # 🔑 3. Professional Clean Login Input Card
        with st.form("cinescope_login_form"):
            st.markdown("<p style='font-size: 11px; color: #777; font-weight: 700; letter-spacing: 1px; margin-bottom: 6px;'>USER IDENTITY</p>", unsafe_allow_html=True)
            username = st.text_input("Username", label_visibility="collapsed", placeholder="Enter your official handle (e.g., admin)")
            
            st.markdown("<p style='font-size: 11px; color: #777; font-weight: 700; letter-spacing: 1px; margin-bottom: 6px; margin-top: 16px;'>SECURITY PIN</p>", unsafe_allow_html=True)
            password = st.text_input("Password", label_visibility="collapsed", type="password", placeholder="••••••••••••")
            
            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
            submit_btn = st.form_submit_button("ENTER SYSTEM", use_container_width=True)
            
            if submit_btn:
                try:
                    # 🔐 1. Hardcoded quick master login bypass (Always handy for testing)
                    if username == "admin" and password == "admin123":
                        st.session_state.authenticated = True
                        st.rerun()
                    
                    else:
                        # 📁 2. Resolve your local Excel data track file layout paths
                        base_path = os.path.dirname(os.path.dirname(__file__))
                        data_path = os.path.join(base_path, "data", "data.xlsx")
                        
                        if not os.path.exists(data_path):
                            st.error(f"❌ Excel File missing at path: {data_path}")
                        else:
                            # 📊 3. Read your 'Employee Data' sheet tab directly
                            emp_df = pd.read_excel(data_path, sheet_name="Employee Data")
                            
                            # 🔍 4. Match input entries to your sheet column fields 
                            # (Verify these column headers match your spreadsheet exactly!)
                            valid_user = emp_df[
                                (emp_df['Employee_Name'].astype(str) == username) & 
                                (emp_df['Password'].astype(str) == password)
                            ]
                            
                            if not valid_user.empty:
                                st.session_state.authenticated = True
                                st.rerun()
                            else:
                                st.error("❌ Authentication Refused. Invalid access credentials.")
                                
                except Exception as e:
                    st.error(f"⚠️ Security Gateway Offline: {str(e)}")