from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import router
import os

app = FastAPI(title="Fit Buddy")

app.include_router(router)

# Static folder iruntha mount pannuthu
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/health")
def health():
    return {"status": "ok"}
