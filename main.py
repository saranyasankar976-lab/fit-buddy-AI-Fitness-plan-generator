"""
main.py
FitBuddy application entrypoint.
Run with:  uvicorn app.main:app --reload
Then visit http://127.0.0.1:8000  (and /docs for the API explorer)
"""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()  # loads GOOGLE_API_KEY from a .env file if present

from routes import router
from app.database import init_db

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = FastAPI(title="FitBuddy - AI Fitness Plan Generator")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(router)


@app.on_event("startup")
def on_startup():
    init_db()
