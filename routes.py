import os
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from models import UserInput, FeedbackRequest
from gemini_generator import generate_workout_gemini
from gemini_flash_generator import generate_nutrition_tip_with_flash
from updated_plan import update_workout_plan
import database as db

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# / - Home route: shows the input form
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

# /generate-workout - Plan Generator
@router.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    goal: str = Form(...),
    level: str = Form(...)
):
    user_input = UserInput(name=name, age=age, gender=gender, goal=goal, level=level)
    
    workout_plan = generate_workout_gemini(user_input)
    nutrition_tip = generate_nutrition_tip_with_flash(user_input)
    
    # Save to DB
    db.save_user_data(user_input, workout_plan)

    return templates.TemplateResponse(request, "result.html", {
        "workout": workout_plan,
        "nutrition": nutrition_tip,
        "user": user_input
    })
