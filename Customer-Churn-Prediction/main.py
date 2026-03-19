from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Customer Churn Prediction")

app.include_router(router)