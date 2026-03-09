from fastapi import FastAPI
import pickle

app = FastAPI()

model = pickle.load(open("sales_model.pkl","rb"))

@app.get("/")
def home():
    return {"message":"Sales Prediction API"}

@app.get("/predict/{day}")
def predict(day:int):
    prediction = model.predict([[day]])
    return {"Predicted Sales": float(prediction[0])}