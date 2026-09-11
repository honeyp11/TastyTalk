from typing import Optional
from PIL import Image
from google import genai
from google.genai import types
from config.settings import SUPPORTED_MODELS

def analyze_food_image(
    image: Image.Image,
    goal: str,
    preference: str,
    api_key: str
) -> str:
    """
    Analyzes a food plate or nutrition label image using Gemini Multimodal Vision,
    estimating calories, macros, ingredients, and health score.
    """
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
You are an expert AI Food & Nutrition Vision Analyst.
User Context:
- Goal: {goal}
- Dietary Preference: {preference}

Please analyze this food image carefully and output the analysis in this structured format:

### 🍽️ Detected Food Items & Portions
- List each identified item with approximate weight or portion size.

### 📊 Estimated Nutritional Breakdown
| Metric | Estimated Amount |
| :--- | :--- |
| **Total Calories** | ~X kcal |
| **Protein** | ~X g |
| **Carbohydrates** | ~X g |
| **Fat** | ~X g |
| **Fiber** | ~X g |

### 🥗 Alignment with Goal ({goal})
- Evaluate whether this meal supports their goal of {goal} and matches their {preference} diet.

### 💡 Nutritionist Tips & Health Score
- **Health Rating**: X / 10
- Actionable tips to improve this meal's nutritional density (e.g., adding greens, reducing refined oils).
"""
    
    last_error = None
    for model_name in SUPPORTED_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[
                    image,
                    prompt
                ]
            )
            if response.text:
                return response.text
        except Exception as e:
            last_error = e
            continue
            
    return f"❌ **Error analyzing food image:** `{str(last_error)}`"
