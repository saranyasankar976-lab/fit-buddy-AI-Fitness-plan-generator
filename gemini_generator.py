def generate_fitness_plan(age, gender, height, weight, goal, activity, bmi):
    # Simple fallback plan - no API needed, 100% working
    workout = f"""
    Day 1: Full Body Strength (Push-ups, Squats, Planks)
    Day 2: Cardio - 30 min Walking/Jogging
    Day 3: Upper Body - (Dumbbells if available)
    Day 4: Active Rest - Yoga / Stretching
    Day 5: Lower Body - Lunges, Squats
    Day 6: HIIT - 20 min
    Day 7: Rest & Recovery

    Goal: {goal} | Activity: {activity} | BMI: {bmi}
    """

    nutrition = f"For {goal}: Eat high protein, 2L water daily, avoid junk food. Your BMI is {bmi} - maintain balanced diet."

    recovery = "Sleep 7-8 hours, stretch daily, 1 rest day per week is must."

    return {
        "workout": workout,
        "nutrition": nutrition,
        "recovery": recovery
    }
