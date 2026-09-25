import os
from google import genai

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
_client = genai.Client(api_key=GOOGLE_API_KEY) if GOOGLE_API_KEY else None
MODEL_NAME = MODEL_NAME = "gemini-3-flash-preview"


def generate_nutrition_tip_with_flash(goal: str) -> str:
    if _client is None:
        return f"[DEMO MODE] Balanced diet tip for {goal}."

    prompt = f"Give ONE concise nutrition/recovery tip (2-3 sentences) for goal '{goal}'."
    interaction = _client.interactions.create(model=MODEL_NAME, input=prompt)
    return interaction.output_text