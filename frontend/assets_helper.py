import os
import base64

def get_mascot_base64() -> str:
    """
    Returns base64 encoded string of the NutriAI mascot avatar.
    Guaranteed safe and resilient across multiple path resolutions.
    """
    possible_paths = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "mascot.jpg")),
        os.path.abspath(os.path.join(os.getcwd(), "assets", "mascot.jpg")),
        r"c:\Users\Honey\Desktop\Food & Nutrition Assistant\assets\mascot.jpg"
    ]
    for p in possible_paths:
        if os.path.exists(p):
            try:
                with open(p, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
            except Exception:
                continue
    return ""
