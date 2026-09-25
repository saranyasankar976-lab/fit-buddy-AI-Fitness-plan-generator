# FitBuddy – AI Fitness Plan Generator (Gemini Models)

A FastAPI web app that generates personalized 7-day workout plans and
nutrition tips using Google's Gemini 1.5 Pro (workouts + feedback revisions)
and Gemini Flash (nutrition tips), backed by SQLite via SQLAlchemy.

## Project structure
```
fitbuddy/
├── app/
│   ├── main.py                    # FastAPI app entrypoint
│   ├── routes.py                  # All route handlers
│   ├── models.py                  # Pydantic schemas (UserInput, FeedbackRequest)
│   ├── database.py                # SQLAlchemy models + save/get/update functions
│   ├── gemini_generator.py        # generate_workout_gemini() -> Gemini 1.5 Pro
│   ├── gemini_flash_generator.py  # generate_nutrition_tip_with_flash() -> Gemini Flash
│   └── updated_plan.py            # update_workout_plan() -> Gemini 1.5 Pro
├── templates/
│   ├── index.html                 # Input form
│   ├── result.html                # Plan + tip + feedback form
│   └── all_users.html             # Admin dashboard
├── static/images/                 # Put a background image here if you want one
├── requirements.txt
├── .env.example
└── README.md
```

## Step-by-step setup

**1. Get a Gemini API key**
Go to https://aistudio.google.com/app/apikey and create a free API key.

**2. Create and activate a virtual environment**
```bash
python -m venv fitbuddy-env
# Windows:
fitbuddy-env\Scripts\activate
# macOS/Linux:
source fitbuddy-env/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure your API key**
```bash
cp .env.example .env
# then edit .env and paste your real key:
# GOOGLE_API_KEY=AIza...
```

**5. Run the server**
```bash
uvicorn app.main:app --reload
```

**6. Open the app**
- App: http://127.0.0.1:8000
- API docs (Swagger): http://127.0.0.1:8000/docs

## How it works (matches the 4 scenarios)

1. **Generate a plan** — fill the form on `/` with name, user ID, age, weight,
   goal, and intensity → `POST /generate-workout` → Gemini 1.5 Pro builds the
   7-day plan, Gemini Flash builds the nutrition tip, both are saved to SQLite
   and shown on `result.html`.
2. **Give feedback** — from the result page, submit feedback (e.g. "more
   cardio") → `POST /submit-feedback` → the original plan + your feedback are
   sent back to Gemini 1.5 Pro, which returns a revised plan (the original is
   kept in the DB, not overwritten).
3. **Nutrition tip** — regenerated any time a plan is created or updated,
   tailored to the user's goal.
4. **Admin view** — `GET /view-all-users` lists every user with their
   original and updated plans side by side, with a delete option.

## Notes
- If `GOOGLE_API_KEY` isn't set, the app still runs end-to-end using
  placeholder "[DEMO MODE]" text instead of calling Gemini — useful for
  testing the FastAPI/DB/template wiring without burning API quota.
- The SQLite file `fitbuddy.db` is created automatically on first run.
- This build follows the exact module layout in the project brief
  (Milestones 1–5): model selection → core functions → routes.py →
  frontend templates → local deployment.
