from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from starlette.requests import Request


@dataclass(frozen=True)
class FoodProfile:
    calories: int
    protein_g: float
    carbs_g: float
    fat_g: float


FOOD_DB: Dict[str, FoodProfile] = {
    "chicken": FoodProfile(calories=240, protein_g=45, carbs_g=0, fat_g=5),
    "rice": FoodProfile(calories=210, protein_g=4, carbs_g=46, fat_g=0.5),
    "egg": FoodProfile(calories=78, protein_g=6, carbs_g=0.6, fat_g=5),
    "broccoli": FoodProfile(calories=55, protein_g=4, carbs_g=11, fat_g=0.5),
    "salmon": FoodProfile(calories=208, protein_g=22, carbs_g=0, fat_g=13),
    "oats": FoodProfile(calories=150, protein_g=5, carbs_g=27, fat_g=3),
    "banana": FoodProfile(calories=105, protein_g=1.3, carbs_g=27, fat_g=0.3),
    "yogurt": FoodProfile(calories=120, protein_g=10, carbs_g=17, fat_g=1.5),
    "beans": FoodProfile(calories=130, protein_g=8.5, carbs_g=24, fat_g=0.5),
    "avocado": FoodProfile(calories=160, protein_g=2, carbs_g=9, fat_g=15),
}


class AnalyzeRequest(BaseModel):
    meals: List[str] = Field(..., min_length=1)


class AnalysisResult(BaseModel):
    calories: int
    protein_g: float
    carbs_g: float
    fat_g: float
    detected_foods: List[str]
    suggestions: List[str]


def analyze_meals(meals: List[str]) -> AnalysisResult:
    totals = {"calories": 0, "protein_g": 0.0, "carbs_g": 0.0, "fat_g": 0.0}
    detected: List[str] = []

    for meal in meals:
        lowered = meal.lower()
        for food, profile in FOOD_DB.items():
            if food in lowered:
                detected.append(food)
                totals["calories"] += profile.calories
                totals["protein_g"] += profile.protein_g
                totals["carbs_g"] += profile.carbs_g
                totals["fat_g"] += profile.fat_g

    unique_detected = sorted(set(detected))
    suggestions: List[str] = []

    if totals["protein_g"] < 80:
        suggestions.append("Consider adding lean protein (e.g., chicken, yogurt, beans).")
    if totals["carbs_g"] < 130:
        suggestions.append("Carbohydrates are low; add complex carbs like oats or rice.")
    if totals["fat_g"] < 35:
        suggestions.append("Healthy fats are low; add avocado or salmon.")
    if totals["calories"] < 1600:
        suggestions.append("Total calories look low for most adults; increase meal portions.")
    if not unique_detected:
        suggestions.append("No known foods detected. Try naming ingredients explicitly.")

    return AnalysisResult(
        calories=int(totals["calories"]),
        protein_g=round(totals["protein_g"], 1),
        carbs_g=round(totals["carbs_g"], 1),
        fat_g=round(totals["fat_g"], 1),
        detected_foods=unique_detected,
        suggestions=suggestions,
    )


app = FastAPI(title="GPTNutri")

base_dir = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=base_dir / "static"), name="static")
templates = Jinja2Templates(directory=str(base_dir / "templates"))


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html", {})


@app.post("/api/analyze", response_model=AnalysisResult)
def analyze(payload: AnalyzeRequest) -> AnalysisResult:
    return analyze_meals(payload.meals)
