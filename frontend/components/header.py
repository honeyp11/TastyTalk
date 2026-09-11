import streamlit as st
from database.connection import is_db_connected

def render_header(goal: str, preference: str, calorie_target: int):
    """
    Renders the rich top header with active profile chips and live DB connectivity status.
    """
    db_status_badge = ""
    if is_db_connected():
        db_status_badge = '<span class="status-badge status-connected">● MongoDB Connected</span>'
    else:
        db_status_badge = '<span class="status-badge status-memory">● In-Memory Mode</span>'
        
    st.markdown(f"""
    <div class="nutri-header">
        <div class="nutri-title-area">
            <h1>TastyTalk 🥑</h1>
            <p>Smart Food & Nutrition Assistant — Delicious & Healthy Diet Guidance</p>
            <div class="profile-chips">
                <span class="profile-chip">🎯 <b>Goal:</b> {goal}</span>
                <span class="profile-chip">🥗 <b>Diet:</b> {preference}</span>
                <span class="profile-chip">🔥 <b>Target:</b> {calorie_target} kcal</span>
            </div>
        </div>
        <div>
            {db_status_badge}
        </div>
    </div>
    """, unsafe_allow_html=True)
