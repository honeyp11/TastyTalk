import os
import base64
import streamlit as st
from frontend.assets_helper import get_mascot_base64

def get_theme_css(theme: str = "emerald") -> str:
    """
    Generates CSS tailored to the selected theme:
    - emerald: Cyber Emerald / Teal Neon (Image 1 - GammaBot Style)
    - violet: Electric Violet / Neon Purple (Image 3 - Personal AI Style)
    - mint: Mint Glassmorphism (Image 2 - Health AI Style)
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

    /* Mobile App Centered Shell */
    .main .block-container {{
        max-width: 680px !important;
        margin: 0 auto !important;
        padding-top: 1rem !important;
        padding-bottom: 5.5rem !important;
    }}

    #MainMenu, footer, header {{visibility: hidden;}}

    /* Welcome / Splash Screen (Reference Image 1 & 3 Screen 1) */
    .welcome-container {{
        text-align: center;
        padding: 30px 15px 10px 15px;
    }}

    .welcome-mascot-wrapper {{
        position: relative;
        width: 140px;
        height: 140px;
        margin: 0 auto 20px auto;
    }}

    .welcome-mascot-halo {{
        position: absolute;
        top: -10px;
        left: -10px;
        right: -10px;
        bottom: -10px;
        border-radius: 50%;
        background: radial-gradient(circle, {primary_glow} 0%, transparent 70%);
        animation: pulseHalo 3s ease-in-out infinite;
    }}

    @keyframes pulseHalo {{
        0% {{ transform: scale(0.95); opacity: 0.6; }}
        50% {{ transform: scale(1.15); opacity: 1; }}
        100% {{ transform: scale(0.95); opacity: 0.6; }}
    }}

    .welcome-mascot-avatar {{
        width: 130px;
        height: 130px;
        border-radius: 50%;
        overflow: hidden;
        border: 3.5px solid {primary_color};
        box-shadow: 0 0 35px {primary_glow};
        animation: floatMascot 4s ease-in-out infinite;
        position: relative;
        z-index: 2;
        background: #090d16;
        margin: 0 auto;
    }}

    .welcome-mascot-avatar img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}

    .welcome-badge {{
        display: inline-block;
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: {accent_color};
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.6px;
        text-transform: uppercase;
        padding: 4px 14px;
        border-radius: 20px;
        margin-bottom: 12px;
    }}

    .welcome-headline {{
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 2.2rem;
        line-height: 1.15;
        color: #ffffff;
        margin: 0 0 10px 0;
    }}

    .welcome-gradient-text {{
        background: linear-gradient(135deg, #ffffff 30%, {accent_color} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .welcome-description {{
        font-size: 0.92rem;
        color: #94a3b8;
        max-width: 440px;
        margin: 0 auto 20px auto;
        line-height: 1.5;
    }}

    .welcome-features-row {{
        display: flex;
        justify-content: center;
        gap: 8px;
        flex-wrap: wrap;
        margin-bottom: 10px;
    }}

    .welcome-chip {{
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.76rem;
        font-weight: 600;
        color: #e2e8f0;
    }}

    /* Top App Bar */
    .top-app-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 4px 14px 4px;
        margin-bottom: 8px;
    }}

    .brand-group {{
        display: flex;
        align-items: center;
        gap: 10px;
    }}

    .brand-title {{
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 1.35rem;
        letter-spacing: -0.5px;
        color: #ffffff;
    }}

    .online-indicator {{
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(255, 255, 255, 0.06);
        color: {accent_color};
        border: 1px solid {primary_glow};
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
    }}

    .status-dot {{
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: {primary_color};
        box-shadow: 0 0 8px {primary_color};
    }}

    /* Hero Greeting Card (Reference Image 1 & 3 Screen 2) */
    .hero-greeting-card {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%);
        border: 1px solid {primary_glow};
        border-radius: 24px;
        padding: 22px 24px;
        margin-bottom: 20px;
        backdrop-filter: blur(20px);
        box-shadow: 0 16px 36px -10px rgba(0, 0, 0, 0.6), 0 0 24px rgba(255, 255, 255, 0.05);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}

    .greeting-sub {{
        color: {accent_color};
        font-size: 0.88rem;
        font-weight: 600;
        margin-bottom: 4px;
    }}

    .greeting-main {{
        font-family: 'Outfit', sans-serif;
        font-size: 1.7rem;
        font-weight: 800;
        line-height: 1.2;
        color: #ffffff;
        margin: 0 0 10px 0;
    }}

    .greeting-tags {{
        display: flex;
        gap: 6px;
        flex-wrap: wrap;
    }}

    .tag-pill {{
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 3px 9px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        color: #cbd5e1;
    }}

    @keyframes floatMascot {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-7px); }}
        100% {{ transform: translateY(0px); }}
    }}

    .mascot-avatar-hero {{
        width: 95px;
        height: 95px;
        border-radius: 50%;
        overflow: hidden;
        border: 2.5px solid {primary_color};
        box-shadow: 0 0 22px {primary_glow};
        animation: floatMascot 4s ease-in-out infinite;
        flex-shrink: 0;
        background: #090d16;
        margin-left: 10px;
    }}

    .mascot-avatar-hero img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}

    /* Bento Grid Action Cards (Reference Image 1 & 3 Screen 2) */
    .section-title-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        margin-top: 6px;
    }}

    .section-title {{
        font-size: 1.02rem;
        font-weight: 700;
        color: #f1f5f9;
        margin: 0;
    }}

    .see-all-link {{
        color: {accent_color};
        font-size: 0.8rem;
        font-weight: 600;
    }}

    .bento-card {{
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 16px 18px;
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
        font-size: 1.4rem;
    }}

    .bento-arrow {{
        color: {accent_color};
        font-size: 1.1rem;
        font-weight: 700;
    }}

    .bento-label {{
        font-size: 0.95rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 8px;
        line-height: 1.25;
    }}

    .bento-sub {{
        font-size: 0.72rem;
        color: #94a3b8;
        margin-top: 2px;
    }}

    /* Health Overview Gauge Card (Reference Image 2 Screen 1) */
    .health-gauge-card {{
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 16px 20px;
        margin: 18px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
    }}

    .gauge-metrics {{
        display: flex;
        gap: 16px;
        flex-wrap: wrap;
    }}

    .metric-item {{
        display: flex;
        flex-direction: column;
    }}

    .metric-label {{
        font-size: 0.7rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
    }}

    .metric-val {{
        font-size: 1.1rem;
        font-weight: 800;
        color: {accent_color};
    }}

    .score-badge-circle {{
        width: 68px;
        height: 68px;
        border-radius: 50%;
        border: 3.5px solid {primary_color};
        box-shadow: 0 0 16px {primary_glow};
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        background: rgba(0, 0, 0, 0.25);
    }}

    .score-num {{
        font-size: 1.25rem;
        font-weight: 800;
        color: #ffffff;
        line-height: 1;
    }}

    .score-denom {{
        font-size: 0.62rem;
        color: {accent_color};
        font-weight: 600;
    }}

    /* History Chat Rows */
    .history-row {{
        background: rgba(255, 255, 255, 0.025);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 10px 14px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}

    .history-left {{
        display: flex;
        align-items: center;
        gap: 10px;
        min-width: 0;
    }}

    .history-avatar {{
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.06);
        border: 1.5px solid {primary_color};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        flex-shrink: 0;
    }}

    .history-info {{
        min-width: 0;
    }}

    .history-title {{
        font-weight: 700;
        font-size: 0.88rem;
        color: #f1f5f9;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    .history-meta {{
        font-size: 0.72rem;
        color: #64748b;
    }}

    /* Message Bubbles (Matching Reference Image 1 & 3 Screen 3) */
    .user-bubble-box {{
        background: #141c2d;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px 18px 4px 18px;
        padding: 12px 16px;
        color: #f8fafc;
        max-width: 82%;
        margin-left: auto;
        margin-bottom: 12px;
        font-size: 0.92rem;
        line-height: 1.45;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    }}

    .bot-bubble-box {{
        background: {bot_bubble_bg};
        border: 1px solid {bot_bubble_border};
        border-radius: 18px 18px 18px 4px;
        padding: 15px 18px;
        color: #ffffff;
        max-width: 88%;
        margin-right: auto;
        margin-bottom: 14px;
        font-size: 0.93rem;
        line-height: 1.5;
        box-shadow: {bot_bubble_shadow};
    }}

    .bot-bubble-box table {{
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
        font-size: 0.84rem;
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

        .chat-top-bar-wrapper [data-testid="stHorizontalBlock"] {{
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            align-items: center !important;
            gap: 4px !important;
        }}
        .chat-top-bar-wrapper [data-testid="column"] {{
            min-width: 0 !important;
        }}

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

        .hero-greeting-card {{
            padding: 16px 18px !important;
            margin-bottom: 16px !important;
        }}
        .greeting-main {{
            font-size: 1.35rem !important;
        }}
        .mascot-avatar-hero {{
            width: 72px !important;
            height: 72px !important;
        }}

        .user-bubble-box {{
            max-width: 90% !important;
            padding: 10px 14px !important;
            font-size: 0.88rem !important;
            margin-bottom: 10px !important;
        }}
        .bot-bubble-box {{
            max-width: 95% !important;
            padding: 12px 14px !important;
            font-size: 0.89rem !important;
            margin-bottom: 12px !important;
        }}

        [data-testid="stChatInput"] {{
            bottom: 10px !important;
        }}
    }}
</style>
"""

def inject_styles(theme: str = "emerald"):
    """Injects high-end mobile-app styled CSS into Streamlit according to active theme."""
    css = get_theme_css(theme)
    st.markdown(css, unsafe_allow_html=True)
