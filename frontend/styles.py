import os
import base64
import streamlit as st
from frontend.assets_helper import get_mascot_base64

GLOBAL_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Overall Dark Cyberpunk / Obsidian App Canvas */
    .stApp {
        background: radial-gradient(circle at 50% 0%, rgba(16, 185, 129, 0.12) 0%, transparent 60%),
                    radial-gradient(circle at 100% 100%, rgba(6, 182, 212, 0.08) 0%, transparent 50%),
                    #070a13;
        color: #f1f5f9;
    }

    /* Mobile-App Centered Layout (Like the Reference Screenshots) */
    .main .block-container {
        max-width: 680px !important;
        margin: 0 auto !important;
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
    }

    /* Hide default Streamlit clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Top App Bar */
    .top-app-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 4px 16px 4px;
        margin-bottom: 12px;
    }

    .brand-group {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .brand-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 1.35rem;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, #ffffff 40%, #a7f3d0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .online-indicator {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(16, 185, 129, 0.12);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.4px;
        text-transform: uppercase;
    }

    .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: #10b981;
        box-shadow: 0 0 8px #10b981;
    }

    /* 3D Mascot Hero Card (Reference Image 1 & 2) */
    .hero-greeting-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.16) 0%, rgba(6, 182, 212, 0.1) 60%, rgba(13, 18, 30, 0.7) 100%);
        border: 1px solid rgba(16, 185, 129, 0.35);
        border-radius: 24px;
        padding: 24px 26px;
        margin-bottom: 24px;
        backdrop-filter: blur(20px);
        box-shadow: 0 16px 36px -10px rgba(0, 0, 0, 0.6), 0 0 24px rgba(16, 185, 129, 0.15);
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
    }

    .greeting-text-area {
        flex: 1;
        z-index: 2;
    }

    .greeting-sub {
        color: #6ee7b7;
        font-size: 0.88rem;
        font-weight: 600;
        margin-bottom: 4px;
    }

    .greeting-main {
        font-family: 'Outfit', sans-serif;
        font-size: 1.85rem;
        font-weight: 800;
        line-height: 1.2;
        color: #ffffff;
        margin: 0 0 12px 0;
    }

    .greeting-tags {
        display: flex;
        gap: 6px;
        flex-wrap: wrap;
    }

    .tag-pill {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.14);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        color: #e2e8f0;
    }

    /* Floating Mascot Animation */
    @keyframes floatMascot {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-8px) rotate(1.5deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }

    .mascot-avatar-hero {
        width: 105px;
        height: 105px;
        border-radius: 50%;
        overflow: hidden;
        border: 3px solid #10b981;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.4);
        animation: floatMascot 4s ease-in-out infinite;
        flex-shrink: 0;
        background: #090d16;
        margin-left: 12px;
    }

    .mascot-avatar-hero img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* Bento Grid Action Cards (Reference Image 1) */
    .section-title-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
        margin-top: 8px;
    }

    .section-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #f1f5f9;
        margin: 0;
    }

    .see-all-link {
        color: #10b981;
        font-size: 0.82rem;
        font-weight: 600;
        text-decoration: none;
        cursor: pointer;
    }

    .bento-card {
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 20px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 130px;
        position: relative;
        cursor: pointer;
    }

    .bento-card:hover {
        background: rgba(16, 185, 129, 0.08);
        border-color: rgba(16, 185, 129, 0.45);
        transform: translateY(-4px);
        box-shadow: 0 12px 28px -6px rgba(16, 185, 129, 0.25);
    }

    .bento-primary {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.25) 0%, rgba(5, 150, 105, 0.12) 100%);
        border: 1px solid rgba(16, 185, 129, 0.4);
    }

    .bento-top-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }

    .bento-icon {
        font-size: 1.5rem;
    }

    .bento-arrow {
        color: #10b981;
        font-size: 1.15rem;
        font-weight: 700;
        transition: transform 0.2s ease;
    }

    .bento-card:hover .bento-arrow {
        transform: translate(2px, -2px);
    }

    .bento-label {
        font-size: 1rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 10px;
        line-height: 1.25;
    }

    .bento-sub {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 2px;
    }

    /* Health Overview Gauge Card (Reference Image 3) */
    .health-gauge-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 18px 22px;
        margin: 20px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
    }

    .gauge-metrics {
        display: flex;
        gap: 16px;
        flex-wrap: wrap;
    }

    .metric-item {
        display: flex;
        flex-direction: column;
    }

    .metric-label {
        font-size: 0.72rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
    }

    .metric-val {
        font-size: 1.15rem;
        font-weight: 800;
        color: #34d399;
    }

    .score-badge-circle {
        width: 74px;
        height: 74px;
        border-radius: 50%;
        border: 4px solid #10b981;
        box-shadow: 0 0 16px rgba(16, 185, 129, 0.35);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        background: rgba(16, 185, 129, 0.1);
    }

    .score-num {
        font-size: 1.3rem;
        font-weight: 800;
        color: #ffffff;
        line-height: 1;
    }

    .score-denom {
        font-size: 0.65rem;
        color: #6ee7b7;
        font-weight: 600;
    }

    /* History Chat List (Reference Image 1 & 2) */
    .history-row {
        background: rgba(255, 255, 255, 0.025);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 12px 16px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.2s ease;
    }

    .history-row:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(16, 185, 129, 0.3);
        transform: translateX(3px);
    }

    .history-left {
        display: flex;
        align-items: center;
        gap: 12px;
        min-width: 0;
    }

    .history-avatar {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: rgba(16, 185, 129, 0.15);
        border: 1.5px solid #10b981;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
    }

    .history-info {
        min-width: 0;
    }

    .history-title {
        font-weight: 700;
        font-size: 0.92rem;
        color: #f1f5f9;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .history-meta {
        font-size: 0.74rem;
        color: #64748b;
    }

    .history-right {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-shrink: 0;
    }

    .history-time {
        font-size: 0.75rem;
        color: #64748b;
    }

    .history-chevron {
        color: #10b981;
        font-size: 0.95rem;
        font-weight: 700;
    }

    /* Floating Bottom Dock (Reference Image 1 & 2) */
    .floating-dock {
        position: fixed;
        bottom: 18px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(11, 16, 28, 0.88);
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.7), 0 0 20px rgba(16, 185, 129, 0.15);
        backdrop-filter: blur(20px);
        border-radius: 36px;
        padding: 6px 14px;
        display: flex;
        align-items: center;
        gap: 8px;
        z-index: 9999;
        max-width: 440px;
        width: 90%;
        justify-content: space-around;
    }

    /* Styled Chat Bubbles (Reference Image 2 GammaBot style) */
    .user-bubble-box {
        background: #151d30;
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 18px 18px 4px 18px;
        padding: 12px 18px;
        color: #f8fafc;
        max-width: 82%;
        margin-left: auto;
        margin-bottom: 14px;
        font-size: 0.93rem;
        line-height: 1.45;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    .bot-bubble-box {
        background: linear-gradient(135deg, #059669 0%, #047857 50%, #065f46 100%);
        border: 1px solid rgba(52, 211, 153, 0.4);
        border-radius: 18px 18px 18px 4px;
        padding: 16px 20px;
        color: #ffffff;
        max-width: 88%;
        margin-right: auto;
        margin-bottom: 16px;
        font-size: 0.94rem;
        line-height: 1.5;
        box-shadow: 0 8px 24px -4px rgba(16, 185, 129, 0.35);
    }

    .bot-bubble-box table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
        font-size: 0.85rem;
    }

    .bot-bubble-box th, .bot-bubble-box td {
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 6px 10px;
        text-align: left;
    }

    .bot-bubble-box th {
        background: rgba(0, 0, 0, 0.25);
    }

    /* Suggestion Chips */
    .suggestion-chips-row {
        display: flex;
        gap: 8px;
        overflow-x: auto;
        padding-bottom: 8px;
        margin-bottom: 12px;
        scrollbar-width: none;
    }
    .suggestion-chips-row::-webkit-scrollbar {
        display: none;
    }

    /* Buttons override */
    .stButton>button {
        border-radius: 14px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }

    button[kind="primary"] {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.35) !important;
    }

    button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.5) !important;
    }

    /* Mobile Responsive Optimizations (< 768px) */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 0.6rem !important;
            padding-right: 0.6rem !important;
            padding-top: 0.4rem !important;
            padding-bottom: 5.5rem !important;
        }

        /* Top Bar navigation keeping columns strictly side-by-side */
        .chat-top-bar-wrapper [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            align-items: center !important;
            gap: 4px !important;
        }
        .chat-top-bar-wrapper [data-testid="column"] {
            min-width: 0 !important;
        }
        .chat-top-bar-wrapper button {
            padding: 6px 4px !important;
            font-size: 0.8rem !important;
        }

        /* Dock container keeping buttons strictly side-by-side on mobile */
        .dock-container [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 6px !important;
        }
        .dock-container [data-testid="column"] {
            min-width: 0 !important;
            flex: 1 1 0 !important;
        }
        .dock-container .stButton>button {
            padding: 9px 4px !important;
            font-size: 0.8rem !important;
            white-space: nowrap !important;
        }

        /* Hero card responsiveness */
        .hero-greeting-card {
            padding: 16px 18px !important;
            margin-bottom: 16px !important;
        }
        .greeting-main {
            font-size: 1.4rem !important;
        }
        .mascot-avatar-hero {
            width: 74px !important;
            height: 74px !important;
            margin-left: 8px !important;
        }

        /* Chat bubbles on mobile */
        .user-bubble-box {
            max-width: 90% !important;
            padding: 10px 14px !important;
            font-size: 0.88rem !important;
            margin-bottom: 10px !important;
        }
        .bot-bubble-box {
            max-width: 95% !important;
            padding: 12px 14px !important;
            font-size: 0.89rem !important;
            margin-bottom: 12px !important;
        }

        /* Fix chat input pinning on mobile */
        [data-testid="stChatInput"] {
            bottom: 12px !important;
        }
        [data-testid="stChatInput"] textarea {
            font-size: 0.9rem !important;
        }
    }
</style>
"""

def inject_styles():
    """Injects high-end mobile-app styled CSS into Streamlit."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
