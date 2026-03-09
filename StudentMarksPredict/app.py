from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pickle
import os
import numpy as np

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Load model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model", "student_marks_model.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.post("/predict", response_class=HTMLResponse)
def predict(
    request: Request,
    science: int = Form(...),
    english: int = Form(...),
    history: int = Form(...),
    maths: int = Form(...)
):
    import pandas as pd

    data = pd.DataFrame(
        [[science, english, history, maths]],
        columns=['Science', 'English', 'History', 'Maths']
    )

    prediction = model.predict(data)[0]

    return templates.TemplateResponse(
        "predict.html",
        {
            "request": request,
            "prediction": round(prediction, 2)
        }
    )
