import importlib
import streamlit as st
from config.settings import PAGE_TITLE, PAGE_ICON, DEFAULT_CALORIES
from frontend.assets_helper import get_mascot_base64

# Force fresh reload of submodules on each execution
import config.settings
import backend.ai_service
import backend.vision_service
import backend.export_service
import frontend.styles
import frontend.components.sidebar
import frontend.components.chat_view
import frontend.components.vision_view

importlib.reload(config.settings)
importlib.reload(backend.ai_service)
importlib.reload(backend.vision_service)
importlib.reload(backend.export_service)
importlib.reload(frontend.styles)
importlib.reload(frontend.components.sidebar)
importlib.reload(frontend.components.chat_view)
importlib.reload(frontend.components.vision_view)

from frontend.styles import inject_styles
from frontend.components.sidebar import render_sidebar
from frontend.components.chat_view import render_chat_view
from frontend.components.vision_view import render_vision_view

# 1. Page Configuration
st.set_page_config(
    page_title="TastyTalk - Professional AI Nutritionist",
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Active Theme CSS
active_theme = st.session_state.get("app_theme", "emerald")
inject_styles(theme=active_theme)

# 3. Session State Initialization
if "current_view" not in st.session_state or st.session_state.current_view not in ["chat", "vision"]:
    st.session_state.current_view = "chat"
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

# 4. Render Sidebar
sidebar_data = render_sidebar()

# 5. Top Executive Brand Header
mascot_b64 = get_mascot_base64()
mascot_src = f"data:image/jpeg;base64,{mascot_b64}" if mascot_b64 else ""

st.markdown(f"""
<div class="pro-app-header">
    <div class="pro-brand-group">
        <div class="pro-brand-avatar">
            <img src="{mascot_src}" alt="TastyTalk Mascot" />
        </div>
        <div>
            <div class="pro-brand-title">TastyTalk 🥑</div>
            <div class="pro-brand-sub">
                <span class="status-dot-live"></span>
                <span>Certified Clinical AI Nutrition & Culinary System</span>
            </div>
        </div>
    </div>
    <div class="pro-profile-pills">
        <span class="pro-pill">🎯 <strong>{sidebar_data['goal']}</strong></span>
        <span class="pro-pill">🥗 <strong>{sidebar_data['preference']}</strong></span>
        <span class="pro-pill">🔥 <strong>{sidebar_data['calorie_target']} kcal</strong></span>
    </div>
</div>
""", unsafe_allow_html=True)

# 6. Mode Switcher Tabs
tab_chat, tab_vision = st.tabs(["💬 AI Nutritionist Chat", "📸 Food Plate Vision Scanner"])

with tab_chat:
    render_chat_view(
        api_key=sidebar_data["api_key"],
        goal=sidebar_data["goal"],
        preference=sidebar_data["preference"],
        calorie_target=sidebar_data["calorie_target"],
        session_id=sidebar_data["active_session_id"]
    )

with tab_vision:
    render_vision_view(
        api_key=sidebar_data["api_key"],
        goal=sidebar_data["goal"],
        preference=sidebar_data["preference"]
    )
