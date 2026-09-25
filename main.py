from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import router
import database

app = FastAPI(title="Fit Buddy")

# DB create pannuthu
database.init_db()

# Routes add pannuthu
app.include_router(router)

# Templates and static
# app.mount("/static", StaticFiles(directory="static"), name="static")  # static folder iruntha mattum
