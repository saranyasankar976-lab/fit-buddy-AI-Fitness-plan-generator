from gemini_generator import generate_workout_gemini

def generate_fitness_plan(age, gender, height, weight, goal):
    try:
        prompt = f"Create fitness plan for Age:{age}, Gender:{gender}, Height:{height}cm, Weight:{weight}kg, Goal:{goal}. Give workout, diet, tips."
        result = generate_workout_gemini(prompt)
        return result
    except Exception as e:
        return f"## FitBuddy Plan - {goal}\n\nAge: {age}, Gender: {gender}\nHeight: {height}cm, Weight: {weight}kg\n\n**Workout:**\nMon: Chest & Triceps\nTue: Back & Biceps\nWed: Legs\nThu: Shoulders\nFri: Full Body HIIT\nSat: Yoga\nSun: Rest\n\n**Diet:**\nMorning: Warm water + Almonds\nBreakfast: Oats/Idli/Dosa\nLunch: Rice + Dal + Veggies + Curd\nEvening: Fruits/Green tea\nDinner: 2 Chapati + Veg curry"