from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import os

from app.model_load import model
from app.mongodb import collection
from app.logger import logger

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@router.post("/predict", response_class=HTMLResponse)
def predict(
    request: Request,
    gender: int = Form(...),
    senior_citizen: int = Form(...),
    partner: int = Form(...),
    dependents: int = Form(...),
    tenure: int = Form(...),
    monthly_charges: float = Form(...),
    total_charges: float = Form(...)
):

    # Data for model
    data = pd.DataFrame([[ 
        gender, senior_citizen, partner, dependents,
        tenure, monthly_charges, total_charges
    ]], columns=[
        'gender','SeniorCitizen','Partner','Dependents','tenure',
        'MonthlyCharges','TotalCharges'
    ])

    pred = model.predict(data)[0]
    prob = model.predict_proba(data)[0][1]

    if pred == 1:
        result = f" Customer Will Leave ({round(prob*100,2)}%)"
    else:
        result = f" Customer Will Stay ({round((1-prob)*100,2)}%)"

    logger.info(f"Prediction: {pred}, Prob: {prob}")

    # Save to MongoDB
    collection.insert_one({
        "gender": gender,
        "tenure": tenure,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
        "prediction": int(pred),
        "probability": float(prob)
    })

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": result}
    )