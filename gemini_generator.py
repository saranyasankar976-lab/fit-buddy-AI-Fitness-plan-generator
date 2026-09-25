import os

def generate_fitness_plan(age, gender, height, weight, goal, activity, bmi):
    # Gemini try pannuthu, illa na dummy plan kuduthu
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""Create a 7-day workout plan for:
            Age: {age}, Gender: {gender}, Height: {height}cm, Weight: {weight}kg, BMI: {bmi}
            Goal: {goal}, Activity: {activity}
            Give workout, diet tip, recovery tip in simple format."""
            response = model.generate_content(prompt)
            text = response.text
            return {
                "workout": text,
                "nutrition": "High protein, drink 3L water daily, eat balanced meals.",
                "recovery": "Sleep 8 hours, stretch daily, rest on Sunday."
            }
    except Exception as e:
        print(f"Gemini error: {e}")

    # API key illa na ithu work aagum da - fallback plan
    if goal == "weight loss":
        workout = f"""Day 1: Cardio 30min + Full body
Day 2: HIIT 20min + Abs
Day 3: Cardio 40min
Day 4: Strength - Upper body
Day 5: Cardio 30min + Core
Day 6: Strength - Lower body + Cardio 20min
Day 7: Rest + Stretching
(BMI {bmi} ku etha plan)"""
    elif goal == "muscle gain":
        workout = f"""Day 1: Chest + Triceps
Day 2: Back + Biceps
Day 3: Legs + Shoulder
Day 4: Chest + Core
Day 5: Back + Legs
Day 6: Full body strength
Day 7: Rest
(BMI {bmi} ku muscle gain plan)"""
    else:
        workout = f"""Day 1: Full body 45min
Day 2: Cardio + Yoga 30min
Day 3: Strength training
Day 4: HIIT 25min
Day 5: Core + Flexibility
Day 6: Mixed cardio 40min
Day 7: Active recovery"""

    return {
        "workout": workout,
        "nutrition": f"Goal {goal} ku: Protein 1.2g per kg bodyweight, Calories maintain pannu, Water 3L",
        "recovery": "Sleep 7-8 hrs, Foam rolling, Walk daily 8k steps"
    }
