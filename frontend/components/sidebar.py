import streamlit as st
from config.settings import (
    HEALTH_GOALS,
    DIET_PREFERENCES,
    DEFAULT_CALORIES,
    resolve_api_key,
)
from database.connection import is_db_connected
from database.session_repo import list_sessions, create_session, delete_session
try:
    from frontend.assets_helper import get_mascot_base64
except Exception:
    from frontend.styles import get_mascot_base64

def render_sidebar():
    """
    Renders the sidebar navigation, 3D mascot avatar, view switcher,
    session history, profile settings, and API configuration.
    """
    with st.sidebar:
        # Mascot Avatar Banner in Sidebar
        mascot_b64 = get_mascot_base64()
        mascot_src = f"data:image/jpeg;base64,{mascot_b64}" if mascot_b64 else ""

        st.markdown(f"""
        <div class="sidebar-mascot-container">
            <img src="{mascot_src}" class="sidebar-mascot-img" alt="TastyTalk Mascot" />
            <div>
                <div style="font-weight: 800; font-size: 1.15rem; color: #34d399;">TastyTalk 🥑</div>
                <div style="font-size: 0.78rem; color: #94a3b8;">Smart Food & Nutrition AI</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Main Navigation Switcher
        st.markdown("#### 🧭 Navigation")
        view_options = {
            "🏠 Home Dashboard": "home",
            "💬 TastyTalk Chat": "chat",
            "📸 Food Vision Scanner": "vision",
            "👋 Welcome Screen": "welcome"
        }
        
        # Determine current view index
        current_view = st.session_state.get("current_view", "home")
        view_labels = list(view_options.keys())
        default_index = 0
        for idx, lbl in enumerate(view_labels):
            if view_options[lbl] == current_view:
                default_index = idx
                break
                
        selected_label = st.radio(
            "Navigate",
            view_labels,
            index=default_index,
            label_visibility="collapsed"
        )
        st.session_state.current_view = view_options[selected_label]

        # Theme Selector (Image 1, 2, 3 Aesthetics)
        st.markdown("---")
        st.markdown("#### 🎨 Visual Theme")
        theme_map = {
            "🥑 Cyber Emerald (Image 1)": "emerald",
            "💜 Electric Violet (Image 3)": "violet",
            "🌿 Mint Glass (Image 2)": "mint"
        }
        curr_theme_code = st.session_state.get("app_theme", "emerald")
        theme_idx = 0
        for i, val in enumerate(theme_map.values()):
            if val == curr_theme_code:
                theme_idx = i
                break
        selected_theme_label = st.selectbox(
            "Theme",
            list(theme_map.keys()),
            index=theme_idx,
            label_visibility="collapsed"
        )
        new_theme = theme_map[selected_theme_label]
        if new_theme != st.session_state.get("app_theme"):
            st.session_state.app_theme = new_theme
            st.rerun()

        st.markdown("---")


        # Action: New Consultation Button
        if st.button("➕ New Consultation", use_container_width=True, type="primary"):
            new_id = create_session(
                goal=st.session_state.get("goal", "Healthy Maintenance"),
                preference=st.session_state.get("preference", "Vegetarian"),
                calorie_target=st.session_state.get("calorie_target", DEFAULT_CALORIES),
                title="New Consultation"
            )
            st.session_state.active_session_id = new_id
            st.session_state.messages = []
            st.session_state.current_view = "chat"
            st.rerun()

        st.markdown("---")

        # Database History / Sessions List
        db_online = is_db_connected()
        if db_online:
            st.markdown("#### 🕒 Recent Consultations")
            sessions = list_sessions()
            
            if not sessions:
                st.caption("No consultations recorded.")
            else:
                for s in sessions[:6]:
                    s_id = s.get("session_id")
                    title = s.get("title", "Consultation")
                    is_active = (s_id == st.session_state.get("active_session_id"))
                    
                    col_btn, col_del = st.columns([0.82, 0.18])
                    with col_btn:
                        label = f"👉 {title}" if is_active else title
                        if st.button(label, key=f"side_sess_{s_id}", use_container_width=True):
                            st.session_state.active_session_id = s_id
                            st.session_state.current_view = "chat"
                            st.rerun()
                    with col_del:
                        if st.button("✕", key=f"side_del_{s_id}", help="Delete consultation"):
                            delete_session(s_id)
                            if st.session_state.get("active_session_id") == s_id:
                                st.session_state.active_session_id = None
                                st.session_state.messages = []
                            st.rerun()
                            
            st.markdown("---")

        # Profile Preferences
        st.markdown("#### 🎯 Personal Profile")
        
        goal_idx = 0
        if "goal" in st.session_state and st.session_state.goal in HEALTH_GOALS:
            goal_idx = HEALTH_GOALS.index(st.session_state.goal)
            
        goal = st.selectbox("Health Goal", HEALTH_GOALS, index=goal_idx, key="goal_select")
        st.session_state.goal = goal

        pref_idx = 0
        if "preference" in st.session_state and st.session_state.preference in DIET_PREFERENCES:
            pref_idx = DIET_PREFERENCES.index(st.session_state.preference)
            
        preference = st.selectbox("Dietary Preference", DIET_PREFERENCES, index=pref_idx, key="pref_select")
        st.session_state.preference = preference

        calorie_target = st.number_input(
            "Target Calories (kcal/day)",
            min_value=1000,
            max_value=5000,
            value=st.session_state.get("calorie_target", DEFAULT_CALORIES),
            step=50,
            key="cal_target"
        )
        st.session_state.calorie_target = calorie_target

        st.markdown("---")

        # API Key Configuration
        st.markdown("#### 🔑 AI Engine Config")
        default_key = resolve_api_key()
        api_key = st.text_input(
            "Gemini API Key",
            value=default_key,
            type="password",
            placeholder="AIzaSy...",
            help="Configured via .env or entered here."
        )

        st.markdown("---")
        # System Diagnostic
        db_online = is_db_connected()
        if db_online:
            st.caption("🟢 MongoDB: **Connected** (`food_nutrition_db`)")
        else:
            st.caption("🟡 Cloud Mode: **Active** (In-Memory Session)")


    return {
        "api_key": api_key,
        "goal": goal,
        "preference": preference,
        "calorie_target": calorie_target,
        "active_session_id": st.session_state.get("active_session_id"),
        "current_view": st.session_state.get("current_view", "home")
    }
