from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routes import router
import os

app = FastAPI()
app.include_router(router)

# Health check ku
@app.get("/health")
def health():
    return {"status": "ok"}

# Root path fix - ithu thaan mukkiyam da
@app.get("/", include_in_schema=False)
async def root_redirect():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/form")
