import json, os
FILE = "data.json"
def save_user_data(name, age, gender, height, weight, goal, activity, bmi, plan):
    data = []
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                data = json.load(f)
        except: data = []
    data.append({"name": name, "age": age, "bmi": bmi, "goal": goal})
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)
