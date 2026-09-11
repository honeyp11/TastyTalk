import streamlit as st
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
    update_session_title,
    get_session
)
try:
    from frontend.assets_helper import get_mascot_base64
except Exception:
    from frontend.styles import get_mascot_base64

def render_chat_view(
    api_key: str,
    goal: str,
    preference: str,
    calorie_target: int,
    session_id: str
):
    """
    Renders the mobile-styled AI Chat interface matching Reference Images 1 & 2.
    """
    pref = preference  # Safe alias
    mascot_b64 = get_mascot_base64()
    mascot_src = f"data:image/jpeg;base64,{mascot_b64}" if mascot_b64 else ""

    # Load history from DB
    if "loaded_session_id" not in st.session_state or st.session_state.loaded_session_id != session_id:
        if session_id:
            db_msgs = get_session_messages(session_id)
            st.session_state.messages = db_msgs
        else:
            st.session_state.messages = []
        st.session_state.loaded_session_id = session_id

    # 1. Top Navigation Bar (< Back | Ai Chat | Export)
    st.markdown("<div class='chat-top-bar-wrapper'>", unsafe_allow_html=True)
    c_back, c_title, c_tool = st.columns([0.24, 0.52, 0.24], gap="small")
    with c_back:
        if st.button("‹ Back", key="chat_back_btn", use_container_width=True):
            st.session_state.current_view = "home"
            st.rerun()
    with c_title:
        st.markdown("""
        <div style="text-align: center; padding-top: 2px;">
            <div style="font-weight: 800; font-size: 1.12rem; color: #ffffff; line-height: 1.2;">TastyTalk 🥑</div>
            <div style="font-size: 0.72rem; color: #34d399;">● Online Food AI</div>
        </div>
        """, unsafe_allow_html=True)
    with c_tool:
        with st.popover("📥 Export", use_container_width=True):
            st.caption("Download Consultation")
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
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 6px 0 14px 0;'>", unsafe_allow_html=True)

    # 2. Inline Mobile API Key Setup if Missing
    if not api_key:
        st.markdown("""
        <div style="background: rgba(239, 68, 68, 0.12); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 16px; padding: 12px 16px; margin-bottom: 14px;">
            <div style="font-weight: 700; font-size: 0.92rem; color: #fca5a5; margin-bottom: 3px;">🔑 Gemini API Key Needed</div>
            <div style="font-size: 0.78rem; color: #cbd5e1; margin-bottom: 8px;">
                Enter your Google Gemini API key below to enable chat responses on this device:
            </div>
        </div>
        """, unsafe_allow_html=True)
        inline_key = st.text_input(
            "Paste Gemini API Key",
            type="password",
            placeholder="AIzaSy...",
            key="inline_mobile_key_input",
            label_visibility="collapsed"
        )
        if inline_key and inline_key.strip():
            st.session_state.api_key_override = inline_key.strip()
            st.rerun()

    # Check for initial prompt passed from home cards
    prompt_to_send = None
    if "initial_prompt" in st.session_state and st.session_state.initial_prompt:
        prompt_to_send = st.session_state.initial_prompt
        st.session_state.initial_prompt = None

    # Empty State Starter Chips
    if len(st.session_state.messages) == 0 and not prompt_to_send:
        st.markdown(f"""
        <div style="text-align: center; padding: 18px 10px;">
            <div style="width: 65px; height: 65px; border-radius: 50%; overflow: hidden; border: 2.5px solid #10b981; margin: 0 auto 10px auto; box-shadow: 0 0 18px rgba(16,185,129,0.3);">
                <img src="{mascot_src}" style="width: 100%; height: 100%; object-fit: cover;" />
            </div>
            <div style="font-weight: 700; font-size: 1.22rem; color: #ffffff;">Ask TastyTalk Anything! 🥑</div>
            <div style="font-size: 0.84rem; color: #94a3b8; max-width: 380px; margin: 4px auto 14px auto;">
                Get clinical nutrition breakdowns, custom recipes, and meal plans tailored to your {preference} diet!
            </div>
        </div>
        """, unsafe_allow_html=True)

        sc1, sc2 = st.columns(2, gap="small")
        with sc1:
            if st.button("🍕 Healthy Pizza Idea ↗", use_container_width=True):
                prompt_to_send = f"Give me a mouth-watering, high-protein, low-calorie pizza or flatbread recipe complying with a {preference} diet."
            if st.button("🍳 5-Min Protein Snacks ↗", use_container_width=True):
                prompt_to_send = f"Suggest 3 quick 5-minute high-protein snacks strictly adhering to a {preference} diet."
        with sc2:
            if st.button("📋 7-Day Meal Architecture ↗", use_container_width=True):
                prompt_to_send = f"Create a structured 7-day meal plan for a {preference} diet focused on {goal} with a target of {calorie_target} kcal/day. Include delicious variety and calorie breakdown."
            if st.button("⚖️ Smart Macro Breakdown ↗", use_container_width=True):
                prompt_to_send = f"Calculate the exact daily grams of Protein, Carbs, and Fats for my goal of {goal} at {calorie_target} kcal."

    # Render Styled Conversation Bubbles
    for msg in st.session_state.messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role == "user":
            st.markdown(f"""
            <div class="user-bubble-box">
                <div style="font-size: 0.72rem; color: #94a3b8; margin-bottom: 2px; font-weight: 600;">You</div>
                {content}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bot-bubble-box">
                <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 6px;">
                    <span style="font-size: 1rem;">🥑</span>
                    <span style="font-size: 0.8rem; font-weight: 800; letter-spacing: 0.4px;">TastyTalk</span>
                </div>
                <div>{content}</div>
            </div>
            """, unsafe_allow_html=True)

    # Quick Suggestion Chips (Compact collapsible expander to prevent taking full mobile screen)
    if len(st.session_state.messages) > 0 and not prompt_to_send:
        with st.expander("💡 Quick Follow-ups & Suggestions", expanded=False):
            chip1, chip2 = st.columns(2, gap="small")
            with chip1:
                if st.button("🛒 Weekly Grocery List", key="sugg_groc", use_container_width=True):
                    prompt_to_send = "Generate a categorized weekly grocery shopping list based on the recommended meal plan above."
                if st.button("🍰 Guilt-Free Sweet Treats", key="sugg_sweet", use_container_width=True):
                    prompt_to_send = f"Give me 2 healthy, high-protein dessert or sweet treat ideas under 200 calories for a {preference} diet."
            with chip2:
                if st.button("🔄 Healthier Food Swaps", key="sugg_swap", use_container_width=True):
                    prompt_to_send = "What are 5 healthy low-calorie substitutes for popular snack cravings?"
                if st.button("⏱️ Intermittent Fasting Window", key="sugg_fast", use_container_width=True):
                    prompt_to_send = "How should I structure my 16:8 intermittent fasting window with these meals?"

    # Chat Input Bar
    if user_input := st.chat_input("Ask TastyTalk: 'What can I cook with oats?', 'Healthy dinner ideas?'..."):
        prompt_to_send = user_input


    # Streaming Execution & MongoDB Auto-Save
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

        # Add user query
        st.session_state.messages.append({"role": "user", "content": prompt_to_send})
        save_message(session_id, "user", prompt_to_send)

        st.markdown(f"""
        <div class="user-bubble-box">
            <div style="font-size: 0.72rem; color: #94a3b8; margin-bottom: 2px; font-weight: 600;">You</div>
            {prompt_to_send}
        </div>
        """, unsafe_allow_html=True)

        # Stream assistant response
        if not api_key:
            err_msg = "⚠️ **Gemini API Key missing!** Please enter your key in the sidebar or `.env` file."
            st.error(err_msg)
            st.session_state.messages.append({"role": "assistant", "content": err_msg})
            save_message(session_id, "assistant", err_msg)
        else:
            bot_placeholder = st.empty()
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
                    bot_placeholder.markdown(f"""
                    <div class="bot-bubble-box">
                        <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 6px;">
                            <span style="font-size: 1rem;">🥑</span>
                            <span style="font-size: 0.8rem; font-weight: 800;">TastyTalk</span>
                        </div>
                        <div>{stream_text}▌</div>
                    </div>
                    """, unsafe_allow_html=True)

                bot_placeholder.markdown(f"""
                <div class="bot-bubble-box">
                    <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 6px;">
                        <span style="font-size: 1rem;">🥑</span>
                        <span style="font-size: 0.8rem; font-weight: 800;">TastyTalk</span>
                    </div>
                    <div>{stream_text}</div>
                </div>
                """, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": stream_text})
                save_message(session_id, "assistant", stream_text)

            except Exception as e:
                err = f"❌ **Error:** `{str(e)}`"
                bot_placeholder.error(err)
                st.session_state.messages.append({"role": "assistant", "content": err})
                save_message(session_id, "assistant", err)

        st.rerun()
