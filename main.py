from fastapi import FastAPI
from routes import router

app = FastAPI(title="Fit Buddy AI")

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}
