import os
import base64
import streamlit as st
from frontend.assets_helper import get_mascot_base64

def get_theme_css(theme: str = "emerald") -> str:
    """
    Generates CSS tailored to the selected theme:
    - emerald: Cyber Emerald / Teal Neon (CareNex & GammaBot Style)
    - violet: Electric Violet / Neon Purple (Personal AI Style)
    - mint: Mint Glassmorphism (Health AI Style)
    """
    if theme == "violet":
        primary_color = "#8b5cf6"
        primary_gradient = "linear-gradient(135deg, #8b5cf6 0%, #7c3aed 50%, #6d28d9 100%)"
        primary_glow = "rgba(139, 92, 246, 0.4)"
        accent_color = "#a855f7"
        bg_radial = """
            radial-gradient(circle at 50% 0%, rgba(139, 92, 246, 0.16) 0%, transparent 60%),
            radial-gradient(circle at 100% 100%, rgba(236, 72, 153, 0.08) 0%, transparent 50%),
            #080713
        """
        bot_bubble_bg = "linear-gradient(135deg, #7c3aed 0%, #6d28d9 50%, #5b21b6 100%)"
        bot_bubble_border = "rgba(168, 85, 247, 0.45)"
        bot_bubble_shadow = "0 8px 24px -4px rgba(139, 92, 246, 0.4)"
        dock_active_color = "#a855f7"
    elif theme == "mint":
        primary_color = "#14b8a6"
        primary_gradient = "linear-gradient(135deg, #14b8a6 0%, #0d9488 50%, #0f766e 100%)"
        primary_glow = "rgba(20, 184, 166, 0.4)"
        accent_color = "#2dd4bf"
        bg_radial = """
            radial-gradient(circle at 50% 0%, rgba(20, 184, 166, 0.14) 0%, transparent 60%),
            radial-gradient(circle at 100% 100%, rgba(56, 189, 248, 0.08) 0%, transparent 50%),
            #071118
        """
        bot_bubble_bg = "linear-gradient(135deg, #0d9488 0%, #0f766e 50%, #115e59 100%)"
        bot_bubble_border = "rgba(45, 212, 191, 0.4)"
        bot_bubble_shadow = "0 8px 24px -4px rgba(20, 184, 166, 0.35)"
        dock_active_color = "#2dd4bf"
    else:  # default: emerald
        primary_color = "#10b981"
        primary_gradient = "linear-gradient(135deg, #10b981 0%, #059669 50%, #047857 100%)"
        primary_glow = "rgba(16, 185, 129, 0.4)"
        accent_color = "#34d399"
        bg_radial = """
            radial-gradient(circle at 50% 0%, rgba(16, 185, 129, 0.14) 0%, transparent 60%),
            radial-gradient(circle at 100% 100%, rgba(6, 182, 212, 0.08) 0%, transparent 50%),
            #070a13
        """
        bot_bubble_bg = "linear-gradient(135deg, #059669 0%, #047857 50%, #065f46 100%)"
        bot_bubble_border = "rgba(52, 211, 153, 0.4)"
        bot_bubble_shadow = "0 8px 24px -4px rgba(16, 185, 129, 0.35)"
        dock_active_color = "#10b981"

    return f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    /* Dynamic Cyber Canvas */
    .stApp {{
        background: {bg_radial} !important;
        color: #f1f5f9;
    }}

    /* Centered Dashboard Layout matching CareNex Reference */
    .main .block-container {{
        max-width: 980px !important;
        margin: 0 auto !important;
        padding-top: 1.5rem !important;
        padding-bottom: 5rem !important;
    }}

    #MainMenu, footer, header {{visibility: hidden;}}

    /* Top User Status Bar (Matching CareNex Screenshot) */
    .carenex-user-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        padding: 0 4px;
    }}

    .user-greeting-group {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .user-avatar-circle {{
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.25) 0%, rgba(6, 182, 212, 0.1) 100%);
        border: 2px solid {primary_color};
        box-shadow: 0 0 14px {primary_glow};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }}

    .user-title-main {{
        font-family: 'Outfit', sans-serif;
        font-size: 1.28rem;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.2;
    }}

    .user-domain-sub {{
        font-size: 0.76rem;
        color: #94a3b8;
        margin-top: 2px;
    }}

    .carenex-status-pill {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.1);
        color: {accent_color};
        border: 1px solid rgba(16, 185, 129, 0.35);
        padding: 5px 14px;
        border-radius: 24px;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.4px;
    }}

    /* Hero Banner Card (CareNex Exact Match) */
    .hero-greeting-card {{
        background: linear-gradient(135deg, rgba(13, 22, 38, 0.88) 0%, rgba(9, 14, 26, 0.96) 100%);
        border: 1px solid rgba(16, 185, 129, 0.35);
        border-radius: 24px;
        padding: 28px 32px;
        margin-bottom: 14px;
        box-shadow: 0 20px 45px -12px rgba(0, 0, 0, 0.7), 0 0 30px rgba(16, 185, 129, 0.12);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 24px;
        position: relative;
        overflow: hidden;
    }}

    .greeting-text-area {{
        flex: 1;
        z-index: 2;
    }}

    .greeting-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        color: {accent_color};
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}

    .greeting-main {{
        font-family: 'Outfit', sans-serif;
        font-size: 2.3rem;
        font-weight: 800;
        line-height: 1.15;
        color: #ffffff;
        margin: 0 0 10px 0;
        letter-spacing: -0.5px;
    }}

    .greeting-desc {{
        font-size: 0.92rem;
        color: #94a3b8;
        line-height: 1.55;
        max-width: 520px;
        margin-bottom: 14px;
    }}

    .greeting-tags {{
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }}

    .tag-pill {{
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 4px 11px;
        border-radius: 20px;
        font-size: 0.74rem;
        font-weight: 600;
        color: #cbd5e1;
    }}

    /* Mascot Framed Box on Right (CareNex Screenshot) */
    .mascot-frame-box {{
        width: 175px;
        height: 155px;
        border-radius: 20px;
        border: 1.5px solid rgba(16, 185, 129, 0.4);
        background: radial-gradient(circle at center, rgba(16, 185, 129, 0.12) 0%, rgba(7, 10, 19, 0.8) 100%);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5), 0 0 25px rgba(16, 185, 129, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        flex-shrink: 0;
        animation: floatMascot 4s ease-in-out infinite;
    }}

    .mascot-frame-box img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}

    @keyframes floatMascot {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-7px); }}
        100% {{ transform: translateY(0px); }}
    }}

    /* Section Headers */
    .section-title-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
        margin-top: 10px;
    }}

    .section-title {{
        font-family: 'Outfit', sans-serif;
        font-size: 1.25rem;
        font-weight: 800;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .see-all-link {{
        color: {accent_color};
        font-size: 0.82rem;
        font-weight: 600;
    }}

    /* Bento Grid Action Cards (CareNex & Image 1) */
    .bento-card {{
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 18px 20px;
        transition: all 0.25s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 110px;
        margin-bottom: 6px;
    }}

    .bento-card:hover {{
        background: rgba(255, 255, 255, 0.06);
        border-color: {primary_glow};
        transform: translateY(-2px);
    }}

    .bento-primary {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.03) 100%);
        border: 1px solid {primary_glow};
    }}

    .bento-top-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    .bento-icon {{
        font-size: 1.45rem;
    }}

    .bento-arrow {{
        color: {accent_color};
        font-size: 1.15rem;
        font-weight: 700;
    }}

    .bento-label {{
        font-size: 1.02rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 8px;
        line-height: 1.25;
    }}

    .bento-sub {{
        font-size: 0.76rem;
        color: #94a3b8;
        margin-top: 2px;
    }}

    /* History Chat Rows */
    .history-row {{
        background: rgba(255, 255, 255, 0.025);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 12px 16px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}

    .history-left {{
        display: flex;
        align-items: center;
        gap: 12px;
        min-width: 0;
    }}

    .history-avatar {{
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.06);
        border: 1.5px solid {primary_color};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.05rem;
        flex-shrink: 0;
    }}

    .history-info {{
        min-width: 0;
    }}

    .history-title {{
        font-weight: 700;
        font-size: 0.92rem;
        color: #f1f5f9;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    .history-meta {{
        font-size: 0.74rem;
        color: #64748b;
    }}

    /* Message Bubbles */
    .user-bubble-box {{
        background: #141c2d;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px 18px 4px 18px;
        padding: 12px 18px;
        color: #f8fafc;
        max-width: 82%;
        margin-left: auto;
        margin-bottom: 12px;
        font-size: 0.93rem;
        line-height: 1.5;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    }}

    .bot-bubble-box {{
        background: {bot_bubble_bg};
        border: 1px solid {bot_bubble_border};
        border-radius: 18px 18px 18px 4px;
        padding: 16px 20px;
        color: #ffffff;
        max-width: 88%;
        margin-right: auto;
        margin-bottom: 14px;
        font-size: 0.94rem;
        line-height: 1.55;
        box-shadow: {bot_bubble_shadow};
    }}

    .bot-bubble-box table {{
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
        font-size: 0.85rem;
    }}

    .bot-bubble-box th, .bot-bubble-box td {{
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 6px 10px;
        text-align: left;
    }}

    .bot-bubble-box th {{
        background: rgba(0, 0, 0, 0.25);
    }}

    /* Buttons Override */
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

    /* Mobile Responsive Optimizations (< 768px) */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding-left: 0.6rem !important;
            padding-right: 0.6rem !important;
            padding-top: 0.4rem !important;
            padding-bottom: 5.5rem !important;
        }}

        .hero-greeting-card {{
            padding: 18px 20px !important;
            flex-direction: column !important;
            text-align: left !important;
        }}

        .greeting-main {{
            font-size: 1.6rem !important;
        }}

        .mascot-frame-box {{
            width: 100% !important;
            height: 130px !important;
        }}

        .chat-top-bar-wrapper [data-testid="stHorizontalBlock"],
        .dock-container [data-testid="stHorizontalBlock"] {{
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 4px !important;
        }}

        .dock-container [data-testid="column"] {{
            min-width: 0 !important;
            flex: 1 1 0 !important;
        }}

        .dock-container .stButton>button {{
            padding: 8px 2px !important;
            font-size: 0.78rem !important;
            white-space: nowrap !important;
        }}

        .user-bubble-box {{
            max-width: 90% !important;
        }}
        .bot-bubble-box {{
            max-width: 95% !important;
        }}
    }}
</style>
"""

def inject_styles(theme: str = "emerald"):
    """Injects high-end mobile-app styled CSS into Streamlit according to active theme."""
    css = get_theme_css(theme)
    st.markdown(css, unsafe_allow_html=True)
