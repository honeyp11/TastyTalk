import os
from dotenv import load_dotenv

# Ensure .env is loaded
load_dotenv()

# Application Metadata
APP_NAME = "TastyTalk"
APP_SUBTITLE = "Smart Food & Nutrition Assistant"
PAGE_TITLE = "TastyTalk 🥑 — Food & Nutrition Assistant"
PAGE_ICON = "🥑"
LAYOUT = "wide"

# Database Configuration
DB_NAME = "food_nutrition_db"
DEFAULT_MONGO_URI = "mongodb://localhost:27017/"

# Supported Gemini Models (in priority fallback order)
SUPPORTED_MODELS = [
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-flash-latest"
]

# Health Goals & Dietary Profiles
HEALTH_GOALS = [
    "Weight Loss",
    "Muscle Gain",
    "Healthy Maintenance",
    "Keto / Low-Carb",
    "Diabetic Friendly",
    "Heart Healthy",
    "Intermittent Fasting"
]

DIET_PREFERENCES = [
    "Vegetarian",
    "Vegan",
    "Non-Vegetarian",
    "Eggetarian",
    "Jain",
    "Gluten-Free",
    "High-Protein"
]

MEAL_TYPES = [
    "Breakfast",
    "Morning Snack",
    "Lunch",
    "Evening Snack",
    "Dinner",
    "Post-Workout"
]

DEFAULT_CALORIES = 2000

def resolve_api_key() -> str:
    """
    Scans streamlit session state, streamlit secrets, environment, and .env for Gemini API key.
    Ensures seamless operation on local machines, mobile devices, and Streamlit Community Cloud.
    """
    # 1. Check user override in active session
    try:
        import streamlit as st
        if hasattr(st, "session_state") and "api_key_override" in st.session_state:
            override = str(st.session_state.api_key_override).strip()
            if override:
                return override
    except Exception:
        pass

    candidates = [
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
        "Career_Guidance_Chatbot",
        "AI_API_KEY",
        "GEMINI_KEY"
    ]

    # 2. Check Streamlit Cloud st.secrets
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            for key in candidates:
                if key in st.secrets and str(st.secrets[key]).strip():
                    return str(st.secrets[key]).strip()
    except Exception:
        pass

    # 3. Check os.environ and .env
    for key in candidates:
        val = os.getenv(key)
        if val and val.strip():
            return val.strip()

    return ""

def resolve_mongo_uri() -> str:
    """
    Returns configured MONGO_URI, checking st.secrets, environment, or falling back to local MongoDB.
    """
    # Check Streamlit Cloud st.secrets
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            for key in ["MONGO_URI", "MONGODB_URI"]:
                if key in st.secrets and str(st.secrets[key]).strip():
                    return str(st.secrets[key]).strip()
    except Exception:
        pass

    uri = os.getenv("MONGO_URI") or os.getenv("MONGODB_URI")
    if uri and uri.strip():
        return uri.strip()
    return DEFAULT_MONGO_URI

def resolve_db_name() -> str:
    """
    Returns configured MONGO_DB_NAME with whitespace cleanly stripped.
    """
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            for key in ["MONGO_DB_NAME", "DB_NAME"]:
                if key in st.secrets and str(st.secrets[key]).strip():
                    return str(st.secrets[key]).strip()
    except Exception:
        pass

    val = os.getenv("MONGO_DB_NAME") or os.getenv("DB_NAME")
    if val and val.strip():
        return val.strip()
    return DB_NAME


