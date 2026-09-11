import streamlit as st
from PIL import Image
from backend.vision_service import analyze_food_image
from database.session_repo import log_meal, create_session
from config.settings import MEAL_TYPES

def render_vision_view(api_key: str, goal: str, preference: str):
    """
    Renders the Search by Image / AI Plate Scanner matching Reference Image 1.
    """
    # Top Bar with Back Button
    c_back, c_title = st.columns([0.22, 0.78])
    with c_back:
        if st.button("‹ Back", key="vis_back_btn", use_container_width=True):
            st.session_state.current_view = "home"
            st.rerun()
    with c_title:
        st.markdown("""
        <div style="padding-top: 4px;">
            <div style="font-weight: 800; font-size: 1.15rem; color: #ffffff;">Search by Image</div>
            <div style="font-size: 0.75rem; color: #34d399;">● AI Food Vision Scanner</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 8px 0 18px 0;'>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload meal or nutrition label",
        type=["jpg", "jpeg", "png", "webp"],
        help="Supports JPG, PNG, WEBP"
    )

    meal_type = st.selectbox("Meal Category", MEAL_TYPES, index=2)

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Plate Preview", use_container_width=True)

        if st.button("⚡ Scan & Analyze Nutrition Breakdown", type="primary", use_container_width=True):
            if not api_key:
                st.error("⚠️ Please enter your Gemini API Key in the sidebar.")
            else:
                with st.spinner("🔍 Estimating portions, calories, and macros..."):
                    result = analyze_food_image(
                        image=image,
                        goal=goal,
                        preference=preference,
                        api_key=api_key
                    )
                    st.session_state.last_vision_result = result
                    st.session_state.last_vision_meal_type = meal_type

    if "last_vision_result" in st.session_state and st.session_state.last_vision_result:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="bot-bubble-box" style="max-width: 100%;">
            <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 6px;">
                <span style="font-size: 1.1rem;">🥑</span>
                <span style="font-weight: 800; font-size: 0.95rem;">AI Vision Analysis Report</span>
            </div>
            <div>{st.session_state.last_vision_result}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("💾 Save Meal to MongoDB History", use_container_width=True):
            sess_id = st.session_state.get("active_session_id")
            if not sess_id:
                sess_id = create_session(goal=goal, preference=preference, title="Food Vision Meal")
                st.session_state.active_session_id = sess_id
            
            log_meal(
                session_id=sess_id,
                meal_type=st.session_state.get("last_vision_meal_type", "Meal"),
                items="Scanned Plate Analysis",
                calories=500
            )
            st.success("✅ Meal successfully saved to your MongoDB nutrition records!")
    elif uploaded_file is None:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.02); border: 2px dashed rgba(255,255,255,0.1); border-radius: 20px; padding: 40px 20px; text-align: center; margin-top: 15px;">
            <div style="font-size: 3rem; margin-bottom: 10px;">📸</div>
            <div style="font-weight: 700; color: #ffffff; font-size: 1.05rem;">Snap or Upload Your Meal</div>
            <div style="color: #64748b; font-size: 0.85rem; margin-top: 4px;">
                TastyTalk Vision will identify food items, calculate calories, and break down macros.
            </div>
        </div>
        """, unsafe_allow_html=True)
