from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from database import save_user_data, get_all_users
from gemini_generator import generate_fitness_plan

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate")
async def generate_plan(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    height: float = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    activity: str = Form(...)
):
    bmi = round(weight / ((height/100) ** 2), 2)
    plan = generate_fitness_plan(age, gender, height, weight, goal, activity, bmi)
    save_user_data(name, age, gender, height, weight, goal, activity, bmi, plan)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "name": name,
        "bmi": bmi,
        "plan": plan,
        "goal": goal
    })
