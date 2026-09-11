import streamlit as st
from config.settings import (
    HEALTH_GOALS,
    DIET_PREFERENCES,
    DEFAULT_CALORIES,
    resolve_api_key,
)
from database.connection import is_db_connected
from database.session_repo import list_sessions, create_session, delete_session
from frontend.assets_helper import get_mascot_base64

def render_sidebar():
    """
    Renders an executive sidebar drawer:
    - App branding & status
    - Mode navigation (AI Nutrition Chat vs Food Vision Scanner)
    - Theme selector (Cyber Emerald, Electric Violet, Mint Glass)
    - Session history with MongoDB synchronization
    - Profile preferences (Goal, Diet, Calories)
    - API configuration
    """
    with st.sidebar:
        # Mascot Avatar Banner in Sidebar
        mascot_b64 = get_mascot_base64()
        mascot_src = f"data:image/jpeg;base64,{mascot_b64}" if mascot_b64 else ""

        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; padding: 6px 0 16px 0; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 16px;">
            <div style="width: 44px; height: 44px; border-radius: 12px; overflow: hidden; border: 2px solid #10b981; flex-shrink: 0; background: #080d1a;">
                <img src="{mascot_src}" style="width: 100%; height: 100%; object-fit: cover;" alt="TastyTalk Mascot" />
            </div>
            <div>
                <div style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.15rem; color: #ffffff; line-height: 1.2;">TastyTalk 🥑</div>
                <div style="font-size: 0.74rem; color: #34d399; font-weight: 600;">Clinical AI Nutritionist</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Mode Navigation Switcher
        st.markdown("#### 🧭 Workspace Mode")
        view_options = {
            "💬 AI Nutrition Chat": "chat",
            "📸 Food Plate Scanner": "vision"
        }
        
        current_view = st.session_state.get("current_view", "chat")
        if current_view not in ["chat", "vision"]:
            current_view = "chat"
            st.session_state.current_view = "chat"

        view_labels = list(view_options.keys())
        default_index = 0
        for idx, lbl in enumerate(view_labels):
            if view_options[lbl] == current_view:
                default_index = idx
                break
                
        selected_label = st.radio(
            "Select Mode",
            view_labels,
            index=default_index,
            label_visibility="collapsed"
        )
        st.session_state.current_view = view_options[selected_label]

        # Action: New Consultation Button
        if st.button("➕ New Consultation", use_container_width=True, type="primary"):
            new_id = create_session(
                goal=st.session_state.get("goal", "Healthy Maintenance"),
                preference=st.session_state.get("preference", "Vegetarian"),
                calorie_target=st.session_state.get("calorie_target", DEFAULT_CALORIES),
                title="New Consultation"
            )
            st.session_state.active_session_id = new_id
            st.session_state.loaded_session_id = new_id
            st.session_state.messages = []
            st.session_state.current_view = "chat"
            st.rerun()

        st.markdown("---")

        # Database History / Sessions List
        db_online = is_db_connected()
        st.markdown("#### 🕒 Consultation History")
        sessions = list_sessions()
        
        if not sessions:
            st.caption("No previous consultations.")
        else:
            for s in sessions[:8]:
                s_id = s.get("session_id")
                title = s.get("title", "Consultation")
                is_active = (s_id == st.session_state.get("active_session_id"))
                
                col_btn, col_del = st.columns([0.84, 0.16])
                with col_btn:
                    label = f"👉 {title}" if is_active else title
                    if st.button(label, key=f"side_sess_{s_id}", use_container_width=True):
                        st.session_state.active_session_id = s_id
                        st.session_state.loaded_session_id = s_id
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
        st.markdown("#### 🎯 Dietary Profile")
        
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
            "Daily Budget (kcal)",
            min_value=1000,
            max_value=5000,
            value=st.session_state.get("calorie_target", DEFAULT_CALORIES),
            step=50,
            key="cal_target"
        )
        st.session_state.calorie_target = calorie_target

        st.markdown("---")

        # Visual Theme Switcher
        st.markdown("#### 🎨 Color Accent")
        theme_map = {
            "🥑 Cyber Emerald": "emerald",
            "💜 Electric Violet": "violet",
            "🌿 Mint Glass": "mint"
        }
        curr_theme_code = st.session_state.get("app_theme", "emerald")
        theme_idx = 0
        for i, val in enumerate(theme_map.values()):
            if val == curr_theme_code:
                theme_idx = i
                break
        selected_theme_label = st.selectbox(
            "Accent Theme",
            list(theme_map.keys()),
            index=theme_idx,
            label_visibility="collapsed"
        )
        new_theme = theme_map[selected_theme_label]
        if new_theme != st.session_state.get("app_theme"):
            st.session_state.app_theme = new_theme
            st.rerun()

        st.markdown("---")

        # API Key Configuration
        st.markdown("#### 🔑 AI Credentials")
        default_key = resolve_api_key()
        api_key = st.text_input(
            "Gemini API Key",
            value=default_key,
            type="password",
            placeholder="AIzaSy...",
            help="Your key is stored securely in session."
        )

        st.markdown("---")
        # System Diagnostic
        if db_online:
            st.caption("🟢 MongoDB: **Connected**")
        else:
            st.caption("🟡 Cloud Fallback: **In-Memory Active**")

    return {
        "api_key": api_key,
        "goal": goal,
        "preference": preference,
        "calorie_target": calorie_target,
        "active_session_id": st.session_state.get("active_session_id"),
        "current_view": st.session_state.get("current_view", "chat")
    }
