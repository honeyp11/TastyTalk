import streamlit as st
try:
    from frontend.assets_helper import get_mascot_base64
except Exception:
    from frontend.styles import get_mascot_base64
from database.session_repo import list_sessions, create_session, delete_session

def render_home_view():
    """
    Renders the centered Dashboard matching the user's CareNex reference screenshot:
    - User Status Top Bar ('Hi, Foodie 👋' + Status pill)
    - Hero Card with 'Ask Your Nutrition Question' + Framed 3D Chef Robot Mascot
    - 'Chat with TastyTalk Now' full-width button
    - '⚡ Quick Starters' Bento grid (Dietary Roadmap, Food Plate Scanner, Macro Targets, 7-Day Plan)
    - '🔥 Trending Topics' chips
    - '🕒 Recent Consultations' History Chat list
    """
    mascot_b64 = get_mascot_base64()
    mascot_src = f"data:image/jpeg;base64,{mascot_b64}" if mascot_b64 else ""

    goal = st.session_state.get("goal", "Healthy Maintenance")
    pref = st.session_state.get("preference", "Vegetarian")
    calories = st.session_state.get("calorie_target", 2000)

    # 1. Top User Header (Matching CareNex Screenshot)
    st.markdown(f"""
    <div class="carenex-user-header">
        <div class="user-greeting-group">
            <div class="user-avatar-circle">🧑‍🍳</div>
            <div>
                <div class="user-title-main">Hi, Foodie 👋</div>
                <div class="user-domain-sub">Domain: Healthy Nutrition & Clinical Dietetics</div>
            </div>
        </div>
        <span class="carenex-status-pill">
            <span class="status-dot"></span>
            TastyTalk Active
        </span>
    </div>
    """, unsafe_allow_html=True)

    # 2. Hero Greeting Card (Matching CareNex Screenshot)
    st.markdown(f"""
    <div class="hero-greeting-card">
        <div class="greeting-text-area">
            <div class="greeting-badge">⚡ TASTYTALK AI NUTRITIONIST</div>
            <div class="greeting-main">Ask Your Nutrition<br>Question</div>
            <div class="greeting-desc">
                Meet TastyTalk! Your personalized AI dietitian for customized meal plans, macro tracking, food plate scans, and clinical recipe guidance.
            </div>
            <div class="greeting-tags">
                <span class="tag-pill">🎯 {goal}</span>
                <span class="tag-pill">🥗 {pref}</span>
                <span class="tag-pill">🔥 {calories} kcal/day</span>
            </div>
        </div>
        <div class="mascot-frame-box">
            <img src="{mascot_src}" alt="TastyTalk Chef Robot" />
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Full-Width "Chat with TastyTalk Now" Button (Matching CareNex)
    if st.button("💬 Chat with TastyTalk Now", key="hero_chat_now", use_container_width=True):
        st.session_state.current_view = "chat"
        st.rerun()

    prompt_to_launch = None

    # 4. "⚡ Quick Starters" Section (Matching CareNex)
    st.markdown("""
    <div class="section-title-row" style="margin-top: 24px;">
        <div class="section-title">⚡ Quick Starters</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="small")
    with c1:
        st.markdown("""
        <div class="bento-card bento-primary">
            <div class="bento-top-row">
                <span class="bento-icon">📖</span>
                <span class="bento-arrow">↗</span>
            </div>
            <div>
                <div class="bento-label">Dietary Roadmap</div>
                <div class="bento-sub">Custom nutrition milestones & advice</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Generate Roadmap ↗", key="bento_roadmap", use_container_width=True):
            prompt_to_launch = f"Create a step-by-step 30-day nutrition roadmap for my goal of {goal} with a {pref} diet and {calories} kcal daily budget."

    with c2:
        st.markdown("""
        <div class="bento-card">
            <div class="bento-top-row">
                <span class="bento-icon">📸</span>
                <span class="bento-arrow">↗</span>
            </div>
            <div>
                <div class="bento-label">Plate Vision Scan</div>
                <div class="bento-sub">AI photo calorie & macro audit</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Scan Food Photo ↗", key="bento_vision", use_container_width=True):
            st.session_state.current_view = "vision"
            st.rerun()

    c3, c4 = st.columns(2, gap="small")
    with c3:
        st.markdown("""
        <div class="bento-card">
            <div class="bento-top-row">
                <span class="bento-icon">⚖️</span>
                <span class="bento-arrow">↗</span>
            </div>
            <div>
                <div class="bento-label">Macro Targets</div>
                <div class="bento-sub">Target Protein, Carbs, Fat ratio</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Calculate Macros ↗", key="bento_macro", use_container_width=True):
            prompt_to_launch = f"Calculate my exact daily macronutrient distribution in grams (Protein, Carbs, Fats) and calorie percentages for a {pref} diet targeting {goal} at {calories} kcal."

    with c4:
        st.markdown("""
        <div class="bento-card">
            <div class="bento-top-row">
                <span class="bento-icon">📋</span>
                <span class="bento-arrow">↗</span>
            </div>
            <div>
                <div class="bento-label">7-Day Plan</div>
                <div class="bento-sub">Structured weekly meal architecture</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create 7-Day Plan ↗", key="bento_plan", use_container_width=True):
            prompt_to_launch = f"Create a structured 7-day meal plan for a {pref} diet tailored to {goal} at {calories} kcal/day. Include breakfast, lunch, dinner, snack ideas and estimated macros."

    # 5. "🔥 Trending Topics" Section
    st.markdown("""
    <div class="section-title-row" style="margin-top: 24px;">
        <div class="section-title">🔥 Trending Topics</div>
        <span class="see-all-link">Quick Consult</span>
    </div>
    """, unsafe_allow_html=True)

    t1, t2, t3 = st.columns(3, gap="small")
    with t1:
        if st.button("🥩 High Protein", key="trend_protein", use_container_width=True):
            prompt_to_launch = f"What are the top 7 highest-protein foods and snacks complying strictly with a {pref} diet?"
        if st.button("⏱️ 16:8 Fasting", key="trend_fasting", use_container_width=True):
            prompt_to_launch = f"How should I structure my 16:8 intermittent fasting eating window for {goal} with a {pref} diet?"
    with t2:
        if st.button("🥑 Low-Carb Keto", key="trend_keto", use_container_width=True):
            prompt_to_launch = f"Give me a satisfying 3-day low-carb keto meal outline suitable for a {pref} lifestyle."
        if st.button("🌱 Superfood Swaps", key="trend_vegan", use_container_width=True):
            prompt_to_launch = f"What are 5 essential nutrient-dense superfood swaps to boost gut health on a {pref} diet?"
    with t3:
        if st.button("⚡ Fat Loss Tips", key="trend_loss", use_container_width=True):
            prompt_to_launch = f"What are 4 science-backed fat loss habits that speed up metabolism without starving?"
        if st.button("🩺 Sugar Control", key="trend_sugar", use_container_width=True):
            prompt_to_launch = f"Provide delicious low glycemic index (GI) meal ideas to keep blood sugar stable throughout the day."

    # Launch session if prompt clicked
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

    # 6. "🕒 Recent Consultations" Section (Matching CareNex)
    st.markdown("""
    <div class="section-title-row" style="margin-top: 24px;">
        <div class="section-title">🕒 Recent Consultations</div>
        <span class="see-all-link">MongoDB History</span>
    </div>
    """, unsafe_allow_html=True)

    sessions = list_sessions()
    if not sessions:
        st.caption("No previous chats recorded yet. Tap any starter card above to begin!")
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
