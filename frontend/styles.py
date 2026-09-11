import streamlit as st
from frontend.assets_helper import get_mascot_base64

def get_theme_css(theme: str = "emerald") -> str:
    """
    Generates professional, enterprise-grade dark UI CSS:
    - emerald: Cyber Emerald / Vibrant Green (GammaBot / Pro Health aesthetic)
    - violet: Electric Violet / Deep Purple (Perplexity / Linear aesthetic)
    - mint: Fresh Teal / Clean Mint Glass (Clinical modern aesthetic)
    """
    if theme == "violet":
        primary_color = "#8b5cf6"
        primary_gradient = "linear-gradient(135deg, #8b5cf6 0%, #7c3aed 50%, #6d28d9 100%)"
        primary_glow = "rgba(139, 92, 246, 0.35)"
        accent_color = "#a855f7"
        bg_canvas = """
            radial-gradient(circle at 50% 0%, rgba(139, 92, 246, 0.12) 0%, transparent 50%),
            radial-gradient(circle at 100% 100%, rgba(236, 72, 153, 0.05) 0%, transparent 40%),
            #070611
        """
        card_bg = "rgba(22, 18, 42, 0.7)"
        card_border = "rgba(139, 92, 246, 0.22)"
        bot_bubble_bg = "linear-gradient(145deg, rgba(30, 24, 58, 0.9) 0%, rgba(20, 16, 42, 0.95) 100%)"
        bot_bubble_border = "rgba(168, 85, 247, 0.4)"
        user_bubble_bg = "linear-gradient(145deg, #2d1f4d 0%, #1f1537 100%)"
    elif theme == "mint":
        primary_color = "#14b8a6"
        primary_gradient = "linear-gradient(135deg, #14b8a6 0%, #0d9488 50%, #0f766e 100%)"
        primary_glow = "rgba(20, 184, 166, 0.35)"
        accent_color = "#2dd4bf"
        bg_canvas = """
            radial-gradient(circle at 50% 0%, rgba(20, 184, 166, 0.12) 0%, transparent 50%),
            radial-gradient(circle at 100% 100%, rgba(56, 189, 248, 0.05) 0%, transparent 40%),
            #040d12
        """
        card_bg = "rgba(10, 28, 32, 0.7)"
        card_border = "rgba(20, 184, 166, 0.22)"
        bot_bubble_bg = "linear-gradient(145deg, rgba(14, 38, 44, 0.9) 0%, rgba(8, 24, 28, 0.95) 100%)"
        bot_bubble_border = "rgba(45, 212, 191, 0.4)"
        user_bubble_bg = "linear-gradient(145deg, #134e4a 0%, #0c3330 100%)"
    else:  # default: emerald
        primary_color = "#10b981"
        primary_gradient = "linear-gradient(135deg, #10b981 0%, #059669 50%, #047857 100%)"
        primary_glow = "rgba(16, 185, 129, 0.35)"
        accent_color = "#34d399"
        bg_canvas = """
            radial-gradient(circle at 50% 0%, rgba(16, 185, 129, 0.12) 0%, transparent 50%),
            radial-gradient(circle at 100% 100%, rgba(6, 182, 212, 0.05) 0%, transparent 40%),
            #060a12
        """
        card_bg = "rgba(12, 20, 32, 0.7)"
        card_border = "rgba(16, 185, 129, 0.2)"
        bot_bubble_bg = "linear-gradient(145deg, rgba(14, 26, 42, 0.9) 0%, rgba(9, 17, 28, 0.95) 100%)"
        bot_bubble_border = "rgba(52, 211, 153, 0.38)"
        user_bubble_bg = "linear-gradient(145deg, #0d2822 0%, #071915 100%)"

    return f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    /* Global Dark Canvas */
    .stApp {{
        background: {bg_canvas} !important;
        color: #f1f5f9;
    }}

    #MainMenu, footer, header {{visibility: hidden;}}

    /* Main Spacious & Professional Container */
    .main .block-container {{
        max-width: 960px !important;
        width: 100% !important;
        margin: 0 auto !important;
        padding: 1.5rem 1.2rem 4rem 1.2rem !important;
    }}

    @media (max-width: 768px) {{
        .main .block-container {{
            padding: 1rem 0.6rem 3.5rem 0.6rem !important;
        }}
    }}

    /* Top Executive App Bar */
    .pro-app-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 20px;
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 20px;
        backdrop-filter: blur(16px);
        margin-bottom: 22px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.6), 0 0 20px {primary_glow};
    }}

    .pro-brand-group {{
        display: flex;
        align-items: center;
        gap: 14px;
    }}

    .pro-brand-avatar {{
        width: 48px;
        height: 48px;
        border-radius: 14px;
        overflow: hidden;
        border: 2px solid {primary_color};
        box-shadow: 0 0 15px {primary_glow};
        background: #090e1a;
        flex-shrink: 0;
    }}

    .pro-brand-avatar img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}

    .pro-brand-title {{
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 1.35rem;
        color: #ffffff;
        letter-spacing: -0.3px;
        line-height: 1.2;
    }}

    .pro-brand-sub {{
        font-size: 0.78rem;
        color: #94a3b8;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-top: 2px;
    }}

    .status-dot-live {{
        width: 8px;
        height: 8px;
        background: {accent_color};
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px {accent_color};
        animation: pulseDot 2s infinite;
    }}

    @keyframes pulseDot {{
        0% {{ transform: scale(0.9); opacity: 0.7; }}
        50% {{ transform: scale(1.2); opacity: 1; }}
        100% {{ transform: scale(0.9); opacity: 0.7; }}
    }}

    .pro-profile-pills {{
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
    }}

    .pro-pill {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 5px 12px;
        font-size: 0.76rem;
        font-weight: 600;
        color: #cbd5e1;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }}

    .pro-pill strong {{
        color: {accent_color};
    }}

    /* Welcome Hero Banner */
    .pro-hero-banner {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 22px;
        padding: 26px 28px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(16px);
        box-shadow: 0 12px 35px -8px rgba(0, 0, 0, 0.5), 0 0 25px {primary_glow};
    }}

    .pro-hero-badge {{
        display: inline-block;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid {primary_glow};
        color: {accent_color};
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 0.6px;
        padding: 4px 12px;
        border-radius: 20px;
        margin-bottom: 12px;
        text-transform: uppercase;
    }}

    .pro-hero-title {{
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 1.85rem;
        color: #ffffff;
        line-height: 1.25;
        margin-bottom: 10px;
    }}

    .pro-hero-gradient-text {{
        background: {primary_gradient};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .pro-hero-desc {{
        font-size: 0.92rem;
        color: #94a3b8;
        line-height: 1.55;
        max-width: 680px;
        margin-bottom: 0;
    }}

    /* Quick Starters Bento Grid */
    .starter-section-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
        margin-top: 10px;
    }}

    .starter-section-title {{
        font-family: 'Outfit', sans-serif;
        font-size: 1.12rem;
        font-weight: 700;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .starter-card {{
        background: {card_bg};
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 18px 20px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 110px;
        backdrop-filter: blur(12px);
    }}

    .starter-card:hover {{
        border-color: {primary_color};
        transform: translateY(-3px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.6), 0 0 18px {primary_glow};
    }}

    .starter-top-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }}

    .starter-icon {{
        font-size: 1.5rem;
    }}

    .starter-arrow {{
        color: {accent_color};
        font-weight: 800;
        font-size: 1.15rem;
        transition: transform 0.2s;
    }}

    .starter-card:hover .starter-arrow {{
        transform: translate(3px, -3px);
    }}

    .starter-label {{
        font-size: 0.96rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 3px;
    }}

    .starter-sub {{
        font-size: 0.78rem;
        color: #94a3b8;
        line-height: 1.35;
    }}

    /* Trending Topic Chips Row */
    .trending-chips-wrap {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 14px;
        margin-bottom: 24px;
    }}

    .trending-chip-item {{
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #e2e8f0;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        cursor: pointer;
        transition: all 0.2s ease;
    }}

    .trending-chip-item:hover {{
        background: rgba(255, 255, 255, 0.08);
        border-color: {primary_color};
        color: #ffffff;
        transform: translateY(-1px);
    }}

    /* Chat Messages Layout */
    .chat-container-wrap {{
        display: flex;
        flex-direction: column;
        gap: 16px;
        margin-bottom: 24px;
    }}

    /* User Message Bubble */
    .user-bubble {{
        align-self: flex-end;
        background: {user_bubble_bg};
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px 18px 4px 18px;
        padding: 14px 18px;
        color: #f8fafc;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
        position: relative;
    }}

    .user-bubble-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
        font-size: 0.74rem;
        font-weight: 700;
        color: {accent_color};
    }}

    .user-bubble-body {{
        font-size: 0.92rem;
        line-height: 1.5;
    }}

    /* Bot Message Bubble */
    .bot-bubble {{
        align-self: flex-start;
        background: {bot_bubble_bg};
        border: 1px solid {bot_bubble_border};
        border-radius: 18px 18px 18px 4px;
        padding: 18px 22px;
        color: #f8fafc;
        max-width: 92%;
        margin-right: auto;
        box-shadow: 0 8px 30px -6px rgba(0, 0, 0, 0.5), 0 0 15px {primary_glow};
        backdrop-filter: blur(16px);
        position: relative;
    }}

    .bot-bubble-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }}

    .bot-brand-tag {{
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 800;
        font-size: 0.88rem;
        color: #ffffff;
    }}

    .bot-brand-pill {{
        background: {primary_gradient};
        color: #ffffff;
        font-size: 0.68rem;
        font-weight: 800;
        padding: 2px 8px;
        border-radius: 12px;
        letter-spacing: 0.4px;
    }}

    .bubble-time {{
        font-size: 0.7rem;
        color: #94a3b8;
    }}

    .bot-bubble-body {{
        font-size: 0.93rem;
        line-height: 1.6;
    }}

    .bot-bubble-body p {{
        margin-bottom: 0.8rem;
    }}

    .bot-bubble-body strong {{
        color: {accent_color};
    }}

    .bot-bubble-body ul, .bot-bubble-body ol {{
        margin-left: 1.2rem;
        margin-bottom: 0.8rem;
    }}

    .bot-bubble-body table {{
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0;
        font-size: 0.86rem;
    }}

    .bot-bubble-body th, .bot-bubble-body td {{
        padding: 8px 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: left;
    }}

    .bot-bubble-body th {{
        background: rgba(255, 255, 255, 0.06);
        color: {accent_color};
    }}

    /* Global Input & Button Overrides */
    .stButton>button {{
        border-radius: 14px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }}

    button[kind="primary"] {{
        background: {primary_gradient} !important;
        border: none !important;
        box-shadow: 0 4px 14px {primary_glow} !important;
        color: #ffffff !important;
    }}

    button[kind="primary"]:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px {primary_glow} !important;
    }}

    button[kind="secondary"] {{
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #e2e8f0 !important;
    }}

    button[kind="secondary"]:hover {{
        background: rgba(255, 255, 255, 0.09) !important;
        border-color: {primary_color} !important;
        color: #ffffff !important;
    }}

    [data-testid="stChatInput"] {{
        margin-top: 14px !important;
    }}

    [data-testid="stChatInput"] textarea {{
        font-size: 0.92rem !important;
        border-radius: 16px !important;
        background: rgba(14, 20, 32, 0.95) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: #ffffff !important;
    }}

    [data-testid="stChatInput"] textarea:focus {{
        border-color: {primary_color} !important;
        box-shadow: 0 0 15px {primary_glow} !important;
    }}

    /* Custom Navigation Tabs */
    .view-switcher-bar {{
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 12px;
    }}

    /* Sidebar Clean Styling */
    [data-testid="stSidebar"] {{
        background: #090e18 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }}

    [data-testid="stSidebar"] .stButton>button {{
        border-radius: 12px !important;
        font-size: 0.84rem !important;
    }}
</style>
"""

def inject_styles(theme: str = "emerald"):
    """Injects high-end, responsive professional CSS into Streamlit."""
    css = get_theme_css(theme)
    st.markdown(css, unsafe_allow_html=True)
