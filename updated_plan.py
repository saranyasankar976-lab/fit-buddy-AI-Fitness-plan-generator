import os
from google import genai

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
_client = genai.Client(api_key=GOOGLE_API_KEY) if GOOGLE_API_KEY else None
MODEL_NAME = "gemini-3-flash-preview"


def update_workout_plan(original_plan: str, feedback: str) -> str:
    if _client is None:
        return f"[DEMO MODE] Updated plan (feedback: {feedback})\n\n{original_plan}"

    prompt = f"""
Here is a user's current 7-day workout plan:

{original_plan}

Feedback: "{feedback}"

Revise the plan to incorporate this feedback, keeping the Day 1-7 structure.
""".strip()

    interaction = _client.interactions.create(model=MODEL_NAME, input=prompt)
    return interaction.output_text