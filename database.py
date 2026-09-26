import json
import os

FILE = "data.json"

def save_user_data(name, age, gender, height, weight, goal, activity, bmi, plan):
    data = []
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                data = json.load(f)
        except:
            data = []
    data.append({
        "name": name,
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "goal": goal,
        "activity": activity,
        "bmi": bmi
    })
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_all_users():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []
