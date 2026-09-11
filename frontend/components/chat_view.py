import streamlit as st
import datetime
from backend.ai_service import stream_nutrition_advice
from backend.export_service import (
    export_session_as_pdf,
    export_session_as_markdown,
    export_session_as_text
)
from database.session_repo import (
    create_session,
    save_message,
    get_session_messages,
    update_session_title
)
from frontend.assets_helper import get_mascot_base64

def render_chat_view(
    api_key: str,
    goal: str,
    preference: str,
    calorie_target: int,
    session_id: str
):
    """
    Renders an executive, professional AI Nutritionist Chat workspace:
    - Clean top action bar with Live Status, New Chat, and Export options
    - Interactive Quick-Starter cards and Trending Chips for 1-click chatting
    - Streaming, formatted consultation responses with follow-up suggestion chips
    - MongoDB persistent chat history sync
    """
    mascot_b64 = get_mascot_base64()
    mascot_src = f"data:image/jpeg;base64,{mascot_b64}" if mascot_b64 else ""

    # Load session history if switched
    if "loaded_session_id" not in st.session_state or st.session_state.loaded_session_id != session_id:
        if session_id:
            db_msgs = get_session_messages(session_id)
            st.session_state.messages = db_msgs
        else:
            st.session_state.messages = []
        st.session_state.loaded_session_id = session_id

    # 1. Top Navigation & Action Header
    c_left, c_right = st.columns([0.65, 0.35])
    with c_left:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
            <div style="font-family: 'Outfit', sans-serif; font-size: 1.35rem; font-weight: 800; color: #ffffff;">
                TastyTalk 🥑
            </div>
            <span class="pro-pill" style="border-color: rgba(52, 211, 153, 0.4);">
                <span class="status-dot-live"></span>
                <strong>Clinical Nutritionist</strong>
            </span>
        </div>
        <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 12px;">
            Tailored for <strong>{goal}</strong> • <strong>{preference}</strong> • <strong>{calorie_target} kcal/day</strong>
        </div>
        """, unsafe_allow_html=True)
    with c_right:
        c_new, c_exp = st.columns([0.48, 0.52])
        with c_new:
            if st.button("➕ New Chat", key="chat_new_btn", use_container_width=True):
                new_id = create_session(
                    goal=goal,
                    preference=preference,
                    calorie_target=calorie_target,
                    title="New Consultation"
                )
                st.session_state.active_session_id = new_id
                st.session_state.loaded_session_id = new_id
                st.session_state.messages = []
                st.rerun()
        with c_exp:
            with st.popover("📥 Export", use_container_width=True):
                st.caption("Download Consultation Log")
                current_msgs = st.session_state.get("messages", [])
                pdf_bytes = export_session_as_pdf(current_msgs, goal, preference, calorie_target)
                st.download_button(
                    "📄 PDF Document",
                    data=pdf_bytes,
                    file_name="TastyTalk_Consultation.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                md_text = export_session_as_markdown(current_msgs, goal, preference, calorie_target)
                st.download_button(
                    "📝 Markdown (.md)",
                    data=md_text,
                    file_name="TastyTalk_Consultation.md",
                    mime="text/markdown",
                    use_container_width=True
                )

    st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 6px 0 16px 0;'>", unsafe_allow_html=True)

    # 2. Missing API Key Alert / Quick Input
    if not api_key:
        st.warning("⚠️ **Gemini API Key Needed:** Please enter your Google Gemini API key in the sidebar to start chatting.")
        inline_key = st.text_input("Or enter API Key here:", type="password", placeholder="AIzaSy...", key="inline_chat_key")
        if inline_key and inline_key.strip():
            st.session_state.api_key_override = inline_key.strip()
            st.rerun()

    # Track prompt to execute
    prompt_to_send = None

    # Check for initial prompt passed from other cards
    if "initial_prompt" in st.session_state and st.session_state.initial_prompt:
        prompt_to_send = st.session_state.initial_prompt
        st.session_state.initial_prompt = None

    # 3. Empty State: Inviting Hero & Quick-Starters (Matching Reference Aesthetic)
    if len(st.session_state.messages) == 0 and not prompt_to_send:
        st.markdown(f"""
        <div class="pro-hero-banner">
            <span class="pro-hero-badge">AI Nutrition & Culinary Intelligence</span>
            <h1 class="pro-hero-title">How can I assist your <span class="pro-hero-gradient-text">health journey</span> today?</h1>
            <p class="pro-hero-desc">
                Ask about personalized meal plans, clinical nutrition breakdowns, macro ratios, or quick healthy recipes tailored strictly to your dietary goals.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="starter-section-header">
            <div class="starter-section-title">⚡ Quick Consultation Starters</div>
            <div style="font-size: 0.78rem; color: #94a3b8;">Click any card to start instantly</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="medium")
        with col1:
            st.markdown("""
            <div class="starter-card">
                <div class="starter-top-row">
                    <span class="starter-icon">📖</span>
                    <span class="starter-arrow">↗</span>
                </div>
                <div>
                    <div class="starter-label">Custom Dietary Roadmap</div>
                    <div class="starter-sub">30-day nutrition strategy & milestones</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Generate Roadmap ↗", key="btn_quick_roadmap", use_container_width=True):
                prompt_to_send = f"Create a step-by-step 30-day nutrition roadmap for my goal of {goal} with a {preference} diet and {calorie_target} kcal daily budget."

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("""
            <div class="starter-card">
                <div class="starter-top-row">
                    <span class="starter-icon">⚖️</span>
                    <span class="starter-arrow">↗</span>
                </div>
                <div>
                    <div class="starter-label">Macronutrient Targets</div>
                    <div class="starter-sub">Target Protein, Carbs & Fats in exact grams</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Calculate Macros ↗", key="btn_quick_macros", use_container_width=True):
                prompt_to_send = f"Calculate my exact daily macronutrient distribution in grams (Protein, Carbs, Fats) and calorie percentages for a {preference} diet targeting {goal} at {calorie_target} kcal."

        with col2:
            st.markdown("""
            <div class="starter-card">
                <div class="starter-top-row">
                    <span class="starter-icon">📋</span>
                    <span class="starter-arrow">↗</span>
                </div>
                <div>
                    <div class="starter-label">7-Day Structured Meal Plan</div>
                    <div class="starter-sub">Daily breakfast, lunch, dinner & snack breakdown</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Create 7-Day Plan ↗", key="btn_quick_plan", use_container_width=True):
                prompt_to_send = f"Create a structured 7-day meal plan for a {preference} diet tailored to {goal} at {calorie_target} kcal/day. Include delicious variety and estimated calories."

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("""
            <div class="starter-card">
                <div class="starter-top-row">
                    <span class="starter-icon">🍳</span>
                    <span class="starter-arrow">↗</span>
                </div>
                <div>
                    <div class="starter-label">15-Minute High-Protein Meals</div>
                    <div class="starter-sub">Fast, nutrient-dense recipes for busy days</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Suggest Quick Meals ↗", key="btn_quick_meals", use_container_width=True):
                prompt_to_send = f"Suggest 3 quick 15-minute high-protein recipes strictly complying with a {preference} diet for {goal}."

        # Trending Topic Chips
        st.markdown("<br><div style='font-size: 0.82rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px;'>🔥 Trending Nutrition Queries:</div>", unsafe_allow_html=True)
        t1, t2, t3, t4 = st.columns(4, gap="small")
        with t1:
            if st.button("🥗 30g Protein Breakfast", key="trend_1", use_container_width=True):
                prompt_to_send = f"What are 3 delicious {preference} breakfast ideas that deliver at least 30g of clean protein?"
        with t2:
            if st.button("🥑 16:8 Intermittent Fasting", key="trend_2", use_container_width=True):
                prompt_to_send = f"How should I structure my meals and calorie distribution within a 16:8 intermittent fasting window for {goal}?"
        with t3:
            if st.button("🍰 Low-Calorie Sweet Treats", key="trend_3", use_container_width=True):
                prompt_to_send = f"Give me 2 healthy, high-protein dessert recipes under 200 calories for a {preference} diet."
        with t4:
            if st.button("🛒 Essential Grocery List", key="trend_4", use_container_width=True):
                prompt_to_send = f"Generate a categorized weekly grocery list of staple ingredients for a {preference} diet aiming for {goal}."

    # 4. Render Conversation Messages
    if len(st.session_state.messages) > 0:
        for idx, msg in enumerate(st.session_state.messages):
            role = msg.get("role", "user")
            content = msg.get("content", "")
            time_str = msg.get("time", datetime.datetime.now().strftime("%I:%M %p"))

            if role == "user":
                st.markdown(f"""
                <div class="user-bubble">
                    <div class="user-bubble-header">
                        <span>🧑‍💻 You</span>
                        <span>{time_str}</span>
                    </div>
                    <div class="user-bubble-body">{content}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="bot-bubble">
                    <div class="bot-bubble-header">
                        <div class="bot-brand-tag">
                            <span>🥑 TastyTalk AI</span>
                            <span class="bot-brand-pill">Nutritionist</span>
                        </div>
                        <span class="bubble-time">{time_str}</span>
                    </div>
                    <div class="bot-bubble-body">
                """, unsafe_allow_html=True)
                # Streamlit markdown handles code, tables, bold formatting cleanly
                st.markdown(content)
                st.markdown("</div></div>", unsafe_allow_html=True)

        # Quick Follow-Up Chips Row above Chat Bar
        if not prompt_to_send:
            st.markdown("<div style='margin-top: 14px; margin-bottom: 4px; font-size: 0.78rem; font-weight: 700; color: #94a3b8;'>💡 Quick Follow-Ups:</div>", unsafe_allow_html=True)
            fc1, fc2, fc3, fc4 = st.columns(4, gap="small")
            with fc1:
                if st.button("🛒 Get Grocery List", key="fu_groc", use_container_width=True):
                    prompt_to_send = "Based on the advice above, generate a categorized weekly grocery shopping list."
            with fc2:
                if st.button("⏱️ 10-Min Recipe", key="fu_rec", use_container_width=True):
                    prompt_to_send = "Provide a step-by-step 10-minute recipe with simple cooking instructions."
            with fc3:
                if st.button("🔄 Healthy Food Swaps", key="fu_swap", use_container_width=True):
                    prompt_to_send = "What are 4 healthy, low-calorie swaps for common snacks or comfort foods?"
            with fc4:
                if st.button("⚖️ Calculate Macros", key="fu_macro", use_container_width=True):
                    prompt_to_send = "What is the exact macronutrient breakdown (protein, carbs, fats in grams) for this?"

    # 5. Bottom Chat Input
    user_input = st.chat_input("Ask TastyTalk: 'What should I eat post-workout?', 'Calculate macros for weight loss'...")
    if user_input:
        prompt_to_send = user_input

    # 6. Execute Streaming Response & MongoDB Persistence
    if prompt_to_send:
        if not session_id:
            session_id = create_session(
                goal=goal,
                preference=preference,
                calorie_target=calorie_target,
                title=prompt_to_send[:35]
            )
            st.session_state.active_session_id = session_id
            st.session_state.loaded_session_id = session_id
        elif len(st.session_state.messages) == 0:
            update_session_title(session_id, prompt_to_send[:35])

        # Record and show user query
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        st.session_state.messages.append({"role": "user", "content": prompt_to_send, "time": time_now})
        save_message(session_id, "user", prompt_to_send)

        st.markdown(f"""
        <div class="user-bubble">
            <div class="user-bubble-header">
                <span>🧑‍💻 You</span>
                <span>{time_now}</span>
            </div>
            <div class="user-bubble-body">{prompt_to_send}</div>
        </div>
        """, unsafe_allow_html=True)

        if not api_key:
            err_msg = "⚠️ **Gemini API Key missing!** Please enter your key in the sidebar or `.env` file."
            st.error(err_msg)
            st.session_state.messages.append({"role": "assistant", "content": err_msg, "time": time_now})
            save_message(session_id, "assistant", err_msg)
        else:
            bot_card = st.empty()
            stream_text = ""
            try:
                for chunk in stream_nutrition_advice(
                    prompt=prompt_to_send,
                    message_history=st.session_state.messages[:-1],
                    goal=goal,
                    preference=preference,
                    calorie_target=calorie_target,
                    api_key=api_key
                ):
                    stream_text += chunk
                    bot_card.markdown(f"""
                    <div class="bot-bubble">
                        <div class="bot-bubble-header">
                            <div class="bot-brand-tag">
                                <span>🥑 TastyTalk AI</span>
                                <span class="bot-brand-pill">Nutritionist</span>
                            </div>
                            <span class="bubble-time">Typing...</span>
                        </div>
                        <div class="bot-bubble-body">
                    """, unsafe_allow_html=True)
                    bot_card.markdown(stream_text + "▌")
                    bot_card.markdown("</div></div>", unsafe_allow_html=True)

                bot_card.markdown(f"""
                <div class="bot-bubble">
                    <div class="bot-bubble-header">
                        <div class="bot-brand-tag">
                            <span>🥑 TastyTalk AI</span>
                            <span class="bot-brand-pill">Nutritionist</span>
                        </div>
                        <span class="bubble-time">{datetime.datetime.now().strftime("%I:%M %p")}</span>
                    </div>
                    <div class="bot-bubble-body">
                """, unsafe_allow_html=True)
                bot_card.markdown(stream_text)
                bot_card.markdown("</div></div>", unsafe_allow_html=True)

                st.session_state.messages.append({"role": "assistant", "content": stream_text, "time": time_now})
                save_message(session_id, "assistant", stream_text)

            except Exception as e:
                err = f"❌ **Error:** `{str(e)}`"
                bot_card.error(err)
                st.session_state.messages.append({"role": "assistant", "content": err, "time": time_now})
                save_message(session_id, "assistant", err)

        st.rerun()
