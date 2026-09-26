# FitBuddy - AI Fitness Plan Generator using Gemini Models

## ABSTRACT:
FitBuddy is an AI-powered fitness app that generates personalized 7-day workout plans using Google Gemini 1.5 Pro.

## FILES & FUNCTION:
**File:** gemini_generator.py
**Function:** generate_workout_gemini()
**Logic:** Takes UserInput Pydantic model -> calls Gemini SDK -> returns 7-day plan

**File:** routes.py / app.py
Uses Jinja2Templates(directory="templates") and TemplateResponse with {{ username }}, {{ workout_plan }}

## TECH STACK:
- Frontend: HTML, CSS, Flexbox, Roboto font
- Backend: FastAPI, Uvicorn
- AI: Google Generative AI SDK, GOOGLE_API_KEY in .env
- DB: SQLAlchemy

## ACCESS:
- Local: uvicorn main:app --reload -> http://127.0.0.1:8000 & /docs
- Live: Render link (View Demo button)

## CONCLUSION:
All Epics 1 to 5 are implemented at 90% (To Be Reviewed)
