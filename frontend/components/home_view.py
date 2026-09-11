import streamlit as st
try:
    from frontend.assets_helper import get_mascot_base64
except Exception:
    from frontend.styles import get_mascot_base64
from database.session_repo import list_sessions, create_session, delete_session
from database.connection import is_db_connected

def render_home_view():
    """
    Renders the mobile-app styled Home Dashboard matching the user's reference images:
    - 3D Mascot Hero Card ("How may I help you today?")
    - Bento Grid Action Cards with ↗ arrows
    - Health Overview Energy & Calorie Gauge Card
    - History Chat list with timestamps and chevrons
    """
    mascot_b64 = get_mascot_base64()
    mascot_src = f"data:image/jpeg;base64,{mascot_b64}" if mascot_b64 else ""

    goal = st.session_state.get("goal", "Healthy Maintenance")
    pref = st.session_state.get("preference", "Vegetarian")
    calories = st.session_state.get("calorie_target", 2000)

    # 1. Top App Bar (Reference Image 1 & 2)
    st.markdown(f"""
    <div class="top-app-bar">
        <div class="brand-group">
            <span style="font-size: 1.4rem;">🥑</span>
            <span class="brand-title">TastyTalk</span>
        </div>
        <div>
            <span class="online-indicator">
                <span class="status-dot"></span>
                Online
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Hero Mascot Card ("What delicious food are we exploring today?")
    st.markdown(f"""
    <div class="hero-greeting-card">
        <div class="greeting-text-area">
            <div class="greeting-sub">Hey Foodie! 👋</div>
            <div class="greeting-main">What tasty food are we exploring today?</div>
            <div class="greeting-tags">
                <span class="tag-pill">🎯 {goal}</span>
                <span class="tag-pill">🥗 {pref}</span>
                <span class="tag-pill">🔥 {calories} kcal</span>
            </div>
        </div>
        <div class="mascot-avatar-hero">
            <img src="{mascot_src}" alt="TastyTalk 3D Mascot" />
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Bento Grid Action Cards (Reference Image 1 & 2)
    st.markdown("""
    <div class="section-title-row">
        <div class="section-title">Quick Actions</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)

    prompt_to_launch = None

    with c1:
        st.markdown("""
        <div class="bento-card bento-primary">
            <div class="bento-top-row">
                <span class="bento-icon">💬</span>
                <span class="bento-arrow">↗</span>
            </div>
            <div>
                <div class="bento-label">Chat with TastyTalk</div>
                <div class="bento-sub">Interactive Diet & Recipe Coach</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Consultation ↗", key="bento_chat", use_container_width=True):
            st.session_state.current_view = "chat"
            st.rerun()

    with c2:
        st.markdown("""
        <div class="bento-card">
            <div class="bento-top-row">
                <span class="bento-icon">📸</span>
                <span class="bento-arrow">↗</span>
            </div>
            <div>
                <div class="bento-label">Search by Image</div>
                <div class="bento-sub">AI Plate & Macro Scanner</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Scan Food Photo ↗", key="bento_vision", use_container_width=True):
            st.session_state.current_view = "vision"
            st.rerun()

    with c3:
        st.markdown("""
        <div class="bento-card">
            <div class="bento-top-row">
                <span class="bento-icon">⚖️</span>
                <span class="bento-arrow">↗</span>
            </div>
            <div>
                <div class="bento-label">Macro Split</div>
                <div class="bento-sub">Protein, Carbs, Fat Targets</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Calculate Macros ↗", key="bento_macro", use_container_width=True):
            prompt_to_launch = f"Calculate the optimal macronutrient distribution (Protein, Carbs, Fat in grams and percentages) for my goal of {goal} with a daily budget of {calories} calories."

    with c4:
        st.markdown("""
        <div class="bento-card">
            <div class="bento-top-row">
                <span class="bento-icon">📋</span>
                <span class="bento-arrow">↗</span>
            </div>
            <div>
                <div class="bento-label">7-Day Plan</div>
                <div class="bento-sub">Structured Weekly Menu</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Generate 7-Day Plan ↗", key="bento_plan", use_container_width=True):
            prompt_to_launch = f"Generate a comprehensive 7-day meal plan for a {pref} diet targeting {calories} kcal/day for {goal}. Provide exact meal timings, ingredients, and macro split table."

    if prompt_to_launch:
        new_id = create_session(
            goal=goal,
            preference=pref,
            calorie_target=calories,
            title=prompt_to_launch[:35]
        )
        st.session_state.active_session_id = new_id
        st.session_state.initial_prompt = prompt_to_launch
        st.session_state.current_view = "chat"
        st.rerun()

    # 4. Health Overview Gauge Card (Reference Image 3)
    st.markdown(f"""
    <div class="health-gauge-card">
        <div class="gauge-metrics">
            <div class="metric-item">
                <span class="metric-label">Daily Budget</span>
                <span class="metric-val">{calories} kcal</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">Diet Pattern</span>
                <span class="metric-val" style="font-size: 1rem; color: #a7f3d0;">{pref}</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">Target Focus</span>
                <span class="metric-val" style="font-size: 1rem; color: #67e8f9;">{goal}</span>
            </div>
        </div>
        <div class="score-badge-circle">
            <span class="score-num">88</span>
            <span class="score-denom">SCORE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 5. History Chat Section (Reference Image 1 & 2)
    st.markdown("""
    <div class="section-title-row">
        <div class="section-title">History Chat</div>
        <span class="see-all-link">Recent Consultations</span>
    </div>
    """, unsafe_allow_html=True)

    sessions = list_sessions()
    if not sessions:
        st.caption("No conversations recorded yet. Tap any action card above to start!")
    else:
        for s in sessions[:5]:
            s_id = s.get("session_id")
            title = s.get("title", "Nutrition Consultation")
            updated = s.get("updated_at")
            time_str = updated.strftime("%H:%M") if updated else "12:00"
            
            c_row, c_act = st.columns([0.82, 0.18])
            with c_row:
                st.markdown(f"""
                <div class="history-row">
                    <div class="history-left">
                        <div class="history-avatar">🥑</div>
                        <div class="history-info">
                            <div class="history-title">{title}</div>
                            <div class="history-meta">{s.get('message_count', 0)} messages • {time_str}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with c_act:
                if st.button("Open >", key=f"hist_open_{s_id}", use_container_width=True):
                    st.session_state.active_session_id = s_id
                    st.session_state.current_view = "chat"
                    st.rerun()
