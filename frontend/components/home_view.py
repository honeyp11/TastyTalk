import streamlit as st
try:
    from frontend.assets_helper import get_mascot_base64
except Exception:
    from frontend.styles import get_mascot_base64
from database.session_repo import list_sessions, create_session, delete_session

def render_home_view():
    """
    Renders the mobile-app styled Home Dashboard matching Reference Image 1 & 3:
    - Top App Bar with Online indicator
    - 3D Mascot Hero Card ("Ask Your Food Question")
    - Bento Grid Action Cards (Chat with Bot, Search by Image, Macro Split, 7-Day Plan)
    - Trending Topics / Dietary Needs Chips
    - Health Overview Energy & Calorie Score Card
    - History Chat list with timestamps and chevrons
    """
    mascot_b64 = get_mascot_base64()
    mascot_src = f"data:image/jpeg;base64,{mascot_b64}" if mascot_b64 else ""

    goal = st.session_state.get("goal", "Healthy Maintenance")
    pref = st.session_state.get("preference", "Vegetarian")
    calories = st.session_state.get("calorie_target", 2000)

    # 1. Top App Bar (Reference Image 1 & 3)
    st.markdown(f"""
    <div class="top-app-bar">
        <div class="brand-group">
            <span style="font-size: 1.4rem;">🥑</span>
            <div>
                <div class="brand-title">TastyTalk</div>
                <div style="font-size: 0.72rem; color: #64748b; margin-top: -2px;">Personal Nutrition Coach</div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
            <span class="online-indicator">
                <span class="status-dot"></span>
                Online
            </span>
            <div style="width: 34px; height: 34px; border-radius: 50%; background: #131d31; border: 1.5px solid #10b981; display: flex; align-items: center; justify-content: center; font-size: 0.95rem;">
                🧑‍🍳
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Hero Mascot Card ("Welcome! Ask Your Question" - Matching Image 1 Screen 2)
    st.markdown(f"""
    <div class="hero-greeting-card">
        <div class="greeting-text-area">
            <div class="greeting-sub">Welcome, Foodie! 👋</div>
            <div class="greeting-main">Ask Your Nutrition Question</div>
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

    prompt_to_launch = None

    # 3. Bento Grid Action Cards (Matching Image 1 Screen 2 & Image 3 Screen 2)
    st.markdown("""
    <div class="section-title-row">
        <div class="section-title">Explore Features</div>
    </div>
    """, unsafe_allow_html=True)

    bento_c1, bento_c2 = st.columns(2, gap="small")
    with bento_c1:
        st.markdown("""
        <div class="bento-card bento-primary">
            <div class="bento-top-row">
                <span class="bento-icon">💬</span>
                <span class="bento-arrow">↗</span>
            </div>
            <div>
                <div class="bento-label">Chat with Bot</div>
                <div class="bento-sub">Smart Diet & Recipe AI</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Chatting ↗", key="bento_chat_btn", use_container_width=True):
            st.session_state.current_view = "chat"
            st.rerun()

    with bento_c2:
        st.markdown("""
        <div class="bento-card">
            <div class="bento-top-row">
                <span class="bento-icon">📸</span>
                <span class="bento-arrow">↗</span>
            </div>
            <div>
                <div class="bento-label">Search by Image</div>
                <div class="bento-sub">Food Plate & Macro Vision</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Scan Food Plate ↗", key="bento_vision_btn", use_container_width=True):
            st.session_state.current_view = "vision"
            st.rerun()

    bento_c3, bento_c4 = st.columns(2, gap="small")
    with bento_c3:
        st.markdown("""
        <div class="bento-card">
            <div class="bento-top-row">
                <span class="bento-icon">⚖️</span>
                <span class="bento-arrow">↗</span>
            </div>
            <div>
                <div class="bento-label">Macro Targets</div>
                <div class="bento-sub">Optimal Protein / Carb Split</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Calculate Macros ↗", key="bento_macro_btn", use_container_width=True):
            prompt_to_launch = f"Calculate my exact daily macronutrient distribution in grams (Protein, Carbs, Fats) and calorie breakdown for a {pref} diet targeting {goal} at {calories} kcal/day."

    with bento_c4:
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
        if st.button("Create 7-Day Plan ↗", key="bento_plan_btn", use_container_width=True):
            prompt_to_launch = f"Create a comprehensive 7-day meal plan for a {pref} diet tailored to {goal} at {calories} kcal/day. Include breakfast, lunch, dinner, snack ideas and estimated macros."

    # 4. Trending Topics Pills (Matching Reference Image 1 Screen 2)
    st.markdown("""
    <div class="section-title-row" style="margin-top: 18px;">
        <div class="section-title">Trending Topics</div>
        <span class="see-all-link">Quick Consult</span>
    </div>
    """, unsafe_allow_html=True)

    topic_c1, topic_c2, topic_c3 = st.columns(3, gap="small")
    with topic_c1:
        if st.button("🥩 High Protein", key="trend_protein", use_container_width=True):
            prompt_to_launch = f"What are the top 7 highest-protein foods and snacks complying strictly with a {pref} diet?"
        if st.button("⏱️ 16:8 Fasting", key="trend_fasting", use_container_width=True):
            prompt_to_launch = f"How should I structure my 16:8 intermittent fasting eating window for {goal} with a {pref} diet?"
    with topic_c2:
        if st.button("🥑 Low-Carb Keto", key="trend_keto", use_container_width=True):
            prompt_to_launch = f"Give me a satisfying 3-day low-carb keto meal outline suitable for a {pref} lifestyle."
        if st.button("🌱 Superfoods Swap", key="trend_vegan", use_container_width=True):
            prompt_to_launch = f"What are 5 essential nutrient-dense superfood swaps to boost gut health on a {pref} diet?"
    with topic_c3:
        if st.button("⚡ Fat Loss Tips", key="trend_loss", use_container_width=True):
            prompt_to_launch = f"What are 4 science-backed fat loss habits that speed up metabolism without starving?"
        if st.button("🩺 Sugar Control", key="trend_sugar", use_container_width=True):
            prompt_to_launch = f"Provide delicious low glycemic index (GI) meal ideas to keep blood sugar stable throughout the day."

    # Launch session if prompt was clicked from Bento cards or Trending topics
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

    # 5. Health Overview Gauge Card (Matching Reference Image 2 Screen 1)
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
                <span class="metric-label">Target Goal</span>
                <span class="metric-val" style="font-size: 1rem; color: #67e8f9;">{goal}</span>
            </div>
        </div>
        <div class="score-badge-circle">
            <span class="score-num">88</span>
            <span class="score-denom">SCORE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 6. History Chat Section (Matching Reference Image 1 & 3)
    st.markdown("""
    <div class="section-title-row">
        <div class="section-title">History Chat</div>
        <span class="see-all-link">Recent Sessions</span>
    </div>
    """, unsafe_allow_html=True)

    sessions = list_sessions()
    if not sessions:
        st.caption("No previous chats recorded yet. Tap any action card above to start!")
    else:
        for s in sessions[:5]:
            s_id = s.get("session_id")
            title = s.get("title", "Nutrition Consultation")
            updated = s.get("updated_at")
            time_str = updated.strftime("%H:%M") if updated else "12:00"
            
            c_row, c_act = st.columns([0.82, 0.18], gap="small")
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
                if st.button("Open ›", key=f"hist_open_{s_id}", use_container_width=True):
                    st.session_state.active_session_id = s_id
                    st.session_state.current_view = "chat"
                    st.rerun()
