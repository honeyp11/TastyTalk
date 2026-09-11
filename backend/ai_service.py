from typing import Generator, List, Dict
from google import genai
from google.genai import types
from config.settings import SUPPORTED_MODELS

def build_nutritionist_system_instruction(
    goal: str = "Healthy Maintenance",
    preference: str = "Vegetarian",
    calorie_target: int = 2000
) -> str:
    """
    Constructs a personalized TastyTalk nutritionist & culinary coach system instruction prompt.
    """
    return f"""
You are TastyTalk, a friendly, certified clinical nutritionist, culinary expert, and empathetic dietary coach!
Your superpower is making healthy nutrition simple, interactive, tasty, and exciting instead of boring or complicated.

User Profile:
- Goal: {goal}
- Dietary Preference: {preference}
- Target Daily Calories: {calorie_target} kcal

Interactive & Easy Communication Style:
1. Greet the user warmly and keep the conversation engaging, fun, and easy to understand (avoid heavy medical jargon unless asked).
2. Always respect their diet ({preference}) and tailor delicious recipes with practical, kitchen-ready ingredients.
3. For meal plans, break them down clearly:
   - Name of the meal with estimated calories and macro split (Protein, Carbs, Fat in grams).
   - Easy cooking tips or quick preparation shortcuts.
4. End your responses with a friendly follow-up question or 2 quick choice options to keep the conversation interactive (e.g. "Would you like me to share a 10-minute recipe for this or make a weekly grocery list?").
5. When recommending alternatives, suggest tasty, satisfying swaps that don't feel like a sacrifice.
"""

def stream_nutrition_advice(
    prompt: str,
    message_history: List[Dict],
    goal: str,
    preference: str,
    calorie_target: int,
    api_key: str
) -> Generator[str, None, None]:
    """
    Streams tokens from Gemini models with automatic fallback cascade.
    """
    client = genai.Client(api_key=api_key)
    system_instruction = build_nutritionist_system_instruction(goal, preference, calorie_target)
    
    # Build conversation contents including recent history (last 10 turns)
    contents = []
    
    # Context preamble (user -> model)
    contents.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=f"[SYSTEM CONTEXT]\n{system_instruction}")]
        )
    )
    contents.append(
        types.Content(
            role="model",
            parts=[types.Part.from_text(text=f"Understood! I am TastyTalk, your personalized food & nutrition coach for {goal}, {preference} diet, and {calorie_target} kcal daily target. How can I assist you today?")]
        )
    )
    
    # Sanitize and strictly enforce alternating user/model turns
    recent_history = message_history[-10:] if len(message_history) > 10 else message_history
    last_role = "model"
    
    for msg in recent_history:
        text = str(msg.get("content", "")).strip()
        # Skip empty strings and error notices
        if not text or text.startswith("❌") or text.startswith("⚠️"):
            continue
            
        role = "user" if msg.get("role") == "user" else "model"
        
        # Enforce alternation: if consecutive same role, skip or combine
        if role == last_role:
            continue
            
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=text)]
            )
        )
        last_role = role
        
    # If the last turn before current prompt was 'user', add a brief acknowledgement so prompt can be 'user'
    if last_role == "user":
        contents.append(
            types.Content(
                role="model",
                parts=[types.Part.from_text(text="I'm listening, please go ahead!")]
            )
        )
        
    # Append current user prompt
    contents.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        )
    )

    
    last_error = None
    success = False
    
    for model_name in SUPPORTED_MODELS:
        try:
            response = client.models.generate_content_stream(
                model=model_name,
                contents=contents
            )
            has_yielded = False
            for chunk in response:
                if chunk.text:
                    has_yielded = True
                    yield chunk.text
            if has_yielded:
                success = True
                break
        except Exception as e:
            last_error = e
            continue
            
    if not success and last_error:
        yield f"\n\n❌ **Error communicating with AI service:** `{str(last_error)}`\n\n*Please verify your Gemini API key has active quota at [Google AI Studio](https://aistudio.google.com/apikey).*"
