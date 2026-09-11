import streamlit as st
try:
    from frontend.assets_helper import get_mascot_base64
except Exception:
    from frontend.styles import get_mascot_base64

def render_welcome_view():
    """
    Renders the Splash / Welcome Screen matching Image 1 (Screen 1) and Image 3 (Screen 1):
    - 3D Floating NutriBot Mascot with neon halo
    - Headline: 'Meet TastyTalk! Solution for Nutrition'
    - Feature summary pills
    - Prominent 'Get Started' action button
    """
    mascot_b64 = get_mascot_base64()
    mascot_src = f"data:image/jpeg;base64,{mascot_b64}" if mascot_b64 else ""

    st.markdown(f"""
    <div class="welcome-container">
        <!-- Floating 3D Mascot -->
        <div class="welcome-mascot-wrapper">
            <div class="welcome-mascot-halo"></div>
            <div class="welcome-mascot-avatar">
                <img src="{mascot_src}" alt="TastyTalk 3D Mascot" />
            </div>
        </div>

        <!-- App Branding & Title -->
        <div class="welcome-badge">🥑 Next-Gen AI Nutritionist</div>
        <h1 class="welcome-headline">Meet TastyTalk!<br><span class="welcome-gradient-text">Solution for Healthy Diet</span></h1>
        
        <p class="welcome-description">
            Ask any food question and receive instant clinical nutrition breakdowns, custom recipes, and food plate scans powered by AI.
        </p>

        <!-- Feature Highlights Pills -->
        <div class="welcome-features-row">
            <span class="welcome-chip">⚡ Instant Diet Plans</span>
            <span class="welcome-chip">📸 Food Plate Vision</span>
            <span class="welcome-chip">🥗 Macro Tracking</span>
            <span class="welcome-chip">💾 Cloud History</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Big Prominent "Get Started" Button (Matching Reference Screen 1)
    st.markdown("<div style='margin-top: 22px;'>", unsafe_allow_html=True)
    c_left, c_mid, c_right = st.columns([0.1, 0.8, 0.1])
    with c_mid:
        if st.button("🚀 Get Started", key="welcome_get_started", use_container_width=True, type="primary"):
            st.session_state.current_view = "home"
            st.rerun()

        if st.button("💬 Start Chatting Directly →", key="welcome_quick_chat", use_container_width=True):
            st.session_state.current_view = "chat"
            st.rerun()

    st.markdown("""
    <div style="text-align: center; margin-top: 18px; font-size: 0.76rem; color: #64748b;">
        Powered by Google Gemini 3.6 • MongoDB Multi-Session Persistence
    </div>
    </div>
    """, unsafe_allow_html=True)
