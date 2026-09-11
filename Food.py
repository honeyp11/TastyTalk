import importlib
import streamlit as st
from config.settings import PAGE_TITLE, PAGE_ICON, LAYOUT, DEFAULT_CALORIES

# Force fresh reload of submodules on each execution
import config.settings
import backend.ai_service
import backend.vision_service
import backend.export_service
import frontend.styles
import frontend.components.sidebar
import frontend.components.home_view
import frontend.components.chat_view
import frontend.components.vision_view

importlib.reload(config.settings)
importlib.reload(backend.ai_service)
importlib.reload(backend.vision_service)
importlib.reload(backend.export_service)
importlib.reload(frontend.styles)
importlib.reload(frontend.components.sidebar)
importlib.reload(frontend.components.home_view)
importlib.reload(frontend.components.chat_view)
importlib.reload(frontend.components.vision_view)

from frontend.styles import inject_styles
from frontend.components.sidebar import render_sidebar
from frontend.components.home_view import render_home_view
from frontend.components.chat_view import render_chat_view
from frontend.components.vision_view import render_vision_view

# 1. Page Configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

# 2. Inject Modern Dark Glassmorphism CSS
inject_styles()

# 3. Session State Initialization
if "current_view" not in st.session_state:
    st.session_state.current_view = "home"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "active_session_id" not in st.session_state:
    st.session_state.active_session_id = None
if "goal" not in st.session_state:
    st.session_state.goal = "Healthy Maintenance"
if "preference" not in st.session_state:
    st.session_state.preference = "Vegetarian"
if "calorie_target" not in st.session_state:
    st.session_state.calorie_target = DEFAULT_CALORIES

# 4. Render Sidebar (Profile Controls, API Config, MongoDB History)
sidebar_data = render_sidebar()

# 5. Active View Routing
active_view = sidebar_data.get("current_view", "home")

if active_view == "home":
    render_home_view()
elif active_view == "chat":
    render_chat_view(
        api_key=sidebar_data["api_key"],
        goal=sidebar_data["goal"],
        preference=sidebar_data["preference"],
        calorie_target=sidebar_data["calorie_target"],
        session_id=sidebar_data["active_session_id"]
    )
elif active_view == "vision":
    render_vision_view(
        api_key=sidebar_data["api_key"],
        goal=sidebar_data["goal"],
        preference=sidebar_data["preference"]
    )

# 6. Bottom Navigation Dock (Rendered on Home & Vision screens)
if active_view != "chat":
    st.markdown("<br><div class='dock-container'>", unsafe_allow_html=True)
    dock_c1, dock_c2, dock_c3 = st.columns(3, gap="small")
    with dock_c1:
        if st.button("🏠 Home", key="dock_home", use_container_width=True, type="primary" if active_view == "home" else "secondary"):
            st.session_state.current_view = "home"
            st.rerun()
    with dock_c2:
        if st.button("💬 Chat", key="dock_chat", use_container_width=True, type="primary" if active_view == "chat" else "secondary"):
            st.session_state.current_view = "chat"
            st.rerun()
    with dock_c3:
        if st.button("📸 Vision Scan", key="dock_vis", use_container_width=True, type="primary" if active_view == "vision" else "secondary"):
            st.session_state.current_view = "vision"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

