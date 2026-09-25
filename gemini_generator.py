import google.generativeai as genai
import os

# API key Render Environment la irunthu edukkum da
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_fitness_plan(age, gender, height, weight, goal, activity, bmi):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = f"""
        You are a fitness expert. Create a personalized fitness plan.
        
        User Details:
        - Age: {age}
        - Gender: {gender}
        - Height: {height} cm
        - Weight: {weight} kg
        - BMI: {bmi}
        - Goal: {goal}
        - Activity Level: {activity}

        Give response in clean format with:
        1. Diet Plan (Morning, Afternoon, Night)
        2. Workout Plan (Weekly)
        3. Tips
        
        Keep it simple and motivational. Use emojis.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"Gemini Error: {e}")
        # Fallback plan if API fails da
        return f"""
        ### Personalized Plan for {goal} 💪
        
        **Your BMI: {bmi}**

        **Diet Plan:**
        - Morning: Oats + Eggs + Fruits
        - Afternoon: Brown Rice + Chicken / Dal + Veggies
        - Evening: Green Tea + Nuts
        - Night: Light dinner + Salad

        **Workout Plan (5 days):**
        - Monday: Chest + Triceps
        - Tuesday: Back + Biceps
        - Wednesday: Legs + Shoulders
        - Thursday: Cardio + Core
        - Friday: Full Body + Yoga

        **Tips:**
        - Drink 3L water daily
        - Sleep 7-8 hours
        - Be consistent da! 🔥

        (Note: Gemini API key check pannu da, fallback plan idhu)
        """
