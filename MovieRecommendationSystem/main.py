from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.predict import predict_house_price

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request):
    form = await request.form()

    input_data = {
        "median_income": float(form["median_income"]),
        "housing_median_age": float(form["housing_median_age"]),
        "total_rooms": float(form["total_rooms"]),
        "total_bedrooms": float(form["total_bedrooms"]),
        "population": float(form["population"]),
        "households": float(form["households"]),
        "longitude": float(form["longitude"]),
        "latitude": float(form["latitude"]),
        "ocean_proximity_INLAND": int(form["inland"]),
        "ocean_proximity_ISLAND": int(form["island"]),
        "ocean_proximity_NEAR BAY": int(form["near_bay"]),
        "ocean_proximity_NEAR OCEAN": int(form["near_ocean"])
    }

    result = predict_house_price(input_data)

    return templates.TemplateResponse(
        "predict.html",
        {"request": request, "prediction": result}
    )
