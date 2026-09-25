from pymongo import MongoClient
import os
from datetime import datetime

# MongoDB connection - Render la MONGO_URI set pannanum da
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["fitbuddy_db"]
collection = db["users"]

def save_user_data(name, age, gender, height, weight, goal, activity, bmi):
    try:
        data = {
            "name": name,
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "goal": goal,
            "activity": activity,
            "bmi": bmi,
            "created_at": datetime.now()
        }
        collection.insert_one(data)
        print(f"Saved user: {name}")
        return True
    except Exception as e:
        print(f"DB Error: {e}")
        return False

def get_all_users():
    try:
        users = list(collection.find().sort("created_at", -1))
        return users
    except Exception as e:
        print(f"DB Fetch Error: {e}")
        return []
