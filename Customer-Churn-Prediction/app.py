from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pandas as pd
import pickle

app = FastAPI()

templates = Jinja2Templates(directory="templates")

model = pickle.load(open("model/churn.pkl","rb"))

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/predict", response_class=HTMLResponse)
def predict(request: Request,
            gender:int,
            SeniorCitizen:int,
            Partner:int,
            Dependents:int,
            tenure:int,
            MonthlyCharges:float,
            TotalCharges:float):

    data = pd.DataFrame([[gender,SeniorCitizen,Partner,Dependents,tenure,
                          0,0,0,0,0,0,0,0,0,0,0,0,
                          MonthlyCharges,TotalCharges]],
        columns=['gender','SeniorCitizen','Partner','Dependents','tenure',
                 'PhoneService','MultipleLines','InternetService','OnlineSecurity',
                 'OnlineBackup','DeviceProtection','TechSupport','StreamingTV',
                 'StreamingMovies','Contract','PaperlessBilling','PaymentMethod',
                 'MonthlyCharges','TotalCharges'])

    pred = model.predict(data)[0]

    result = "Customer Will Leave" if pred==1 else "Customer Will Stay"

    return templates.TemplateResponse(
        "index.html",
        {"request":request,"result":result}
    )