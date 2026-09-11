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
    Scans environment and .env for Gemini API key under multiple common alias names.
    """
    candidates = [
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
        "Career_Guidance_Chatbot",
        "AI_API_KEY"
    ]
    for key in candidates:
        val = os.getenv(key)
        if val and val.strip():
            return val.strip()
    return ""

def resolve_mongo_uri() -> str:
    """
    Returns configured MONGO_URI, falling back to local MongoDB instance.
    """
    uri = os.getenv("MONGO_URI") or os.getenv("MONGODB_URI")
    if uri and uri.strip():
        return uri.strip()
    return DEFAULT_MONGO_URI
