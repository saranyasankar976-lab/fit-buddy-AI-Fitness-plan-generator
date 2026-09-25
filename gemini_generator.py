import os
from google import genai

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
_client = genai.Client(api_key=GOOGLE_API_KEY) if GOOGLE_API_KEY else None
MODEL_NAME = "gemini-3-flash-preview"


def generate_workout_gemini(goal: str, intensity: str, age: int, weight: float) -> str:
    if _client is None:
        return _fallback_plan(goal, intensity)

    prompt = f"""
You are a certified fitness coach. Create a personalized 7-day workout plan.

User profile:
- Age: {age}
- Weight: {weight} kg
- Fitness goal: {goal}
- Preferred workout intensity: {intensity}

Format the response as:
Day 1: <focus>
  Warm-up (5-10 mins): ...
  Main workout: exercise - sets x reps
  Cooldown: ...
(repeat Day 1 to Day 7)
""".strip()

    interaction = _client.interactions.create(model=MODEL_NAME, input=prompt)
    return interaction.output_text


def _fallback_plan(goal: str, intensity: str) -> str:
    return f"[DEMO MODE] 7-day plan placeholder for goal='{goal}', intensity='{intensity}'."