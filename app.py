import streamlit as st
import base64
import os
from utils.loader import load_all_data
from utils import ui 

# 1. Page Configuration Setup
st.set_page_config(page_title="CineScope | Enterprise", layout="wide", page_icon="🎬")

# 2. Global Asset Styles Ingestion
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.error("CSS file not found.")

def get_base64_image(image_path):
    if not os.path.exists(image_path): return None
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_path = os.path.join("data", "logo.png")
logo_base64 = get_base64_image(logo_path)

# 3. Modular Functional Component Imports
from modules import movies, visitors, theaters, employees, food, login_page, homepage

# 4. Central Runtime Routing States
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "page" not in st.session_state:
    st.session_state.page = "Home"

def nav(page_name):
    st.session_state.page = page_name

# 5. Immersive Gateway Security Shield
if not st.session_state.authenticated:
    login_page.show(logo_base64)
    st.stop() 

# 6. Database Engine Compilation (Executes only if authenticated)
data = load_all_data()

# 7. Navigation Control Environment (Sidebar)
with st.sidebar:
    if logo_base64:
        st.markdown(f"""
            <div style="text-align: center; margin-top: -125px; margin-bottom: -125px;">
                <img src="data:image/png;base64,{logo_base64}" style="width: 350px; height: 350px;">
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<h1 style="font-size:45px; font-weight:900; text-align:center;">CINE<span style="color:#E50914;">SCOPE</span></h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    if st.button("🏠 Home", use_container_width=True): nav("Home")
    st.caption("EXPLORE")
    if st.button("🎥 Movies", use_container_width=True): nav("Movies")
    if st.button("🍿 Inventory", use_container_width=True): nav("Food")
    if st.button("👥 Audience", use_container_width=True): nav("Visitors")
    if st.button("🏢 Theaters", use_container_width=True): nav("Theaters")
    if st.button("👨‍💼 Staff", use_container_width=True): nav("Employees")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚪 Log Out System", use_container_width=True, type="secondary"):
        st.session_state.authenticated = False
        st.session_state.page = "Home"
        st.rerun()

# 8. Main Sub-System Workspace Router
if st.session_state.page == "Home":
    homepage.show(data, nav)
else:
    # Forces live operational status tracking on internal sub-pages
    ui.system_live()
    
    if st.session_state.page == "Movies": movies.show(data["movies"])
    elif st.session_state.page == "Food": food.show(data["food"])
    elif st.session_state.page == "Visitors": visitors.show(data["visitors"])
    elif st.session_state.page == "Theaters": theaters.show(data["theaters"])
    elif st.session_state.page == "Employees": employees.show(data["employees"])