from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from database import SessionLocal, LifeData

app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Score Logic
def calculate_score(study, sleep, screen, workout, morning):
    score = 0

    if study >= 5:
        score += 30
    elif study >= 3:
        score += 20
    else:
        score += 10

    if 7 <= sleep <= 8:
        score += 20
    else:
        score += 10

    if screen <= 3:
        score += 20
    else:
        score += 10

    if workout == "yes":
        score += 15

    if morning == "yes":
        score += 15

    return score

# Suggestion
def get_suggestion(score, workout, morning):
    if score > 80:
        return "🔥 Excellent! You are living a balanced life."
    elif score > 50:
        msg = "👍 Good, but improve consistency. "
        if workout == "no":
            msg += "Start exercising. "
        if morning == "no":
            msg += "Build a morning routine."
        return msg
    else:
        return "⚠️ Focus on discipline: study more, reduce screen time, stay active."

# Workout Plan
def get_workout_plan(workout, score):
    if workout == "no":
        return [
            "Start with 10 min walking 🚶",
            "Do 10 push-ups 💪",
            "Stretch for 5 mins 🧘"
        ]
    
    elif score < 50:
        return [
            "15 min cardio 🏃",
            "Basic strength training",
            "Light yoga 🧘"
        ] 
    
    else:
        return [
            "30 min gym workout 🏋️",
            "Strength + cardio mix",
            "End with stretching"
        ]

# Home
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Analyze
@app.post("/", response_class=HTMLResponse)
def analyze(request: Request,
            study: int = Form(...),
            sleep: int = Form(...),
            screen: int = Form(...),
            workout: str = Form(...),
            morning: str = Form(...)):

    score = calculate_score(study, sleep, screen, workout, morning)
    suggestion = get_suggestion(score, workout, morning)
    workout_plan = get_workout_plan(workout, score)

    # Save to DB
    db = SessionLocal()
    data = LifeData(
        study=study,
        sleep=sleep,
        screen=screen,
        workout=workout,
        morning=morning
    )
    db.add(data)
    db.commit()
    db.close()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "score": score,
        "suggestion": suggestion,
        "workout_plan": workout_plan
    })
