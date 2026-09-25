import os
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# ithu thaan fix da - app. eduthutom
from database import get_db
from models import User
from utils import generate_fitness_plan

router = APIRouter()

# ithu thaan 2nd fix da - oru dirname mattum
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

# Templates folder check pannurom
if not os.path.exists(TEMPLATE_DIR):
    # velila irukka try pannurom
    alt_path = os.path.join(os.path.dirname(BASE_DIR), "templates")
    if os.path.exists(alt_path):
        TEMPLATE_DIR = alt_path

print(f"Using templates from: {TEMPLATE_DIR}")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate", response_class=HTMLResponse)
async def generate_plan(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    height: int = Form(...),
    weight: int = Form(...),
    goal: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        user = User(name=name, age=age, gender=gender, height=height, weight=weight, goal=goal)
        db.add(user)
        db.commit()

        plan = generate_fitness_plan(age, gender, height, weight, goal)
        
        return templates.TemplateResponse("result.html", {
            "request": request, 
            "user": user,
            "plan": plan
        })
    except Exception as e:
        print(f"Error generating plan: {e}")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"Error: {str(e)}"
        })
