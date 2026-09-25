import sqlite3
import os

DB_NAME = "fit_buddy.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  age INTEGER,
                  gender TEXT,
                  height REAL,
                  weight REAL,
                  goal TEXT,
                  activity TEXT,
                  bmi REAL,
                  plan TEXT)''')
    conn.commit()
    conn.close()

def save_user_data(name, age, gender, height, weight, goal, activity, bmi, plan):
    init_db()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO users (name, age, gender, height, weight, goal, activity, bmi, plan) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (name, age, gender, height, weight, goal, activity, bmi, plan))
    conn.commit()
    conn.close()

def get_all_users():
    init_db()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users ORDER BY id DESC")
    users = c.fetchall()
    conn.close()
    return users

# Start la DB create pannuthu
init_db()
