import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routes import router
from database import init_db

app = FastAPI(title="FitBuddy")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB safely
try:
    init_db()
except Exception as e:
    print(f"DB init warning: {e}")

app.include_router(router)

# Mount static only if exists - ithu than main fix da!
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
else:
    print(f"Static folder not found at {STATIC_DIR}, skipping mount")

@app.get("/health")
def health():
    return {"status": "ok"}
