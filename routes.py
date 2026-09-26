"""
routes.py
Core operational layer of FitBuddy — bridges the frontend templates,
the AI generation modules (Gemini Pro & Flash), and the SQLite database.
"""

import os
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.models import UserInput, FeedbackRequest
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan
from app import database as db

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)


# ---------------------------------------------------------------- #
# / — Home route: shows the input form
# ---------------------------------------------------------------- #
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {})


# ---------------------------------------------------------------- #
# /generate-workout — Plan Generator
# ---------------------------------------------------------------- #
@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    user = UserInput(
        username=username, user_id=user_id, age=age,
        weight=weight, goal=goal, intensity=intensity,
    )

    workout_plan = generate_workout_gemini(user.goal, user.intensity, user.age, user.weight)
    nutrition_tip = generate_nutrition_tip_with_flash(user.goal)

    db.save_user(user)
    db.save_plan(user.user_id, workout_plan, nutrition_tip)

    return templates.TemplateResponse(request, "result.html", {
        "username": user.username,
        "user_id": user.user_id,
        "age": user.age,
        "weight": user.weight,
        "goal": user.goal,
        "intensity": user.intensity,
        "workout_plan": workout_plan,
        "nutrition_tip": nutrition_tip,
        "updated": False,
    })


# ---------------------------------------------------------------- #
# /submit-feedback — Update Plan with Feedback
# ---------------------------------------------------------------- #
@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
):
    fb = FeedbackRequest(user_id=user_id, feedback=feedback)

    original_plan = db.get_original_plan(fb.user_id)
    user = db.get_user(fb.user_id)

    if not original_plan or not user:
        return templates.TemplateResponse(request, "result.html", {
            "error": f"No existing plan found for user_id '{fb.user_id}'. Generate a plan first.",
        })

    revised_plan = update_workout_plan(original_plan, fb.feedback)
    db.update_plan(fb.user_id, revised_plan)

    nutrition_tip = generate_nutrition_tip_with_flash(user.goal)

    return templates.TemplateResponse(request, "result.html", {
        "username": user.username,
        "user_id": user.user_id,
        "age": user.age,
        "weight": user.weight,
        "goal": user.goal,
        "intensity": user.intensity,
        "workout_plan": revised_plan,
        "original_plan": original_plan,
        "nutrition_tip": nutrition_tip,
        "updated": True,
        "feedback": fb.feedback,
    })


# ---------------------------------------------------------------- #
# /view-all-users — Admin dashboard
# ---------------------------------------------------------------- #
@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    users = db.get_all_users()
    plans = db.get_all_plans()
    plans_by_user = {p.user_id: p for p in plans}

    rows = []
    for u in users:
        p = plans_by_user.get(u.user_id)
        rows.append({
            "user": u,
            "original_plan": p.original_plan if p else None,
            "updated_plan": p.updated_plan if p else None,
            "nutrition_tip": p.nutrition_tip if p else None,
        })

    return templates.TemplateResponse(request, "all_users.html", {"rows": rows})


# ---------------------------------------------------------------- #
# /delete-user/{user_id} — Admin: remove a user + their plan
# ---------------------------------------------------------------- #
@router.post("/delete-user/{user_id}")
def delete_user(user_id: str):
    db.delete_user(user_id)
    return RedirectResponse(url="/view-all-users", status_code=303)
