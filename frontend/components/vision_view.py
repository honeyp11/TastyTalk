import streamlit as st
from PIL import Image
from backend.vision_service import analyze_food_image
from database.session_repo import log_meal, create_session
from config.settings import MEAL_TYPES

def render_vision_view(api_key: str, goal: str, preference: str):
    """
    Renders an executive AI Food Vision Plate Scanner:
    - Photo upload for meals or nutrition panels
    - Instant portion estimation, calorie breakdown, and macronutrient analysis
    - One-click save to MongoDB health records
    """
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <div style="font-family: 'Outfit', sans-serif; font-size: 1.35rem; font-weight: 800; color: #ffffff;">
            📸 AI Food Plate Vision Scanner
        </div>
        <div style="font-size: 0.82rem; color: #94a3b8; margin-top: 2px;">
            Upload an image of your plate, snack, or grocery nutrition facts label for instant AI analysis.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c_upload, c_meta = st.columns([0.7, 0.3], gap="medium")
    with c_upload:
        uploaded_file = st.file_uploader(
            "Upload meal photo (JPG, PNG, WEBP)",
            type=["jpg", "jpeg", "png", "webp"],
            help="High clarity photos work best"
        )
    with c_meta:
        meal_type = st.selectbox("Meal Category", MEAL_TYPES, index=2)
        st.markdown("<br>", unsafe_allow_html=True)

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        c_img, c_res = st.columns([0.45, 0.55], gap="medium")
        with c_img:
            st.image(image, caption="Uploaded Plate Preview", use_container_width=True)

        with c_res:
            if st.button("⚡ Scan & Analyze Nutrition Breakdown", type="primary", use_container_width=True):
                if not api_key:
                    st.error("⚠️ Please enter your Gemini API Key in the sidebar or above.")
                else:
                    with st.spinner("🔍 Estimating portions, ingredients, calories, and macros..."):
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
        <div class="bot-bubble" style="max-width: 100%;">
            <div class="bot-bubble-header">
                <div class="bot-brand-tag">
                    <span>🥑 AI Plate Analysis</span>
                    <span class="bot-brand-pill">Nutrition Report</span>
                </div>
            </div>
            <div class="bot-bubble-body">
        """, unsafe_allow_html=True)
        st.markdown(st.session_state.last_vision_result)
        st.markdown("</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
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
        <div style="background: rgba(255,255,255,0.02); border: 2px dashed rgba(255,255,255,0.1); border-radius: 20px; padding: 48px 24px; text-align: center; margin-top: 15px;">
            <div style="font-size: 3.2rem; margin-bottom: 12px;">🥗 📸</div>
            <div style="font-weight: 700; color: #ffffff; font-size: 1.15rem;">Snap or Upload Any Meal</div>
            <div style="color: #94a3b8; font-size: 0.88rem; max-width: 480px; margin: 6px auto 0 auto; line-height: 1.5;">
                TastyTalk Vision estimates portion weights, total calories, protein, carbs, fats, and gives clinical tips for healthier swaps.
            </div>
        </div>
        """, unsafe_allow_html=True)
