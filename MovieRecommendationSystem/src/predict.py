from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "linear_regression.pkl"

print("Loading model from:", MODEL_PATH)

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

model = joblib.load(MODEL_PATH)

def predict_house_price(data: dict):
    df = pd.DataFrame([data])
    return round(float(model.predict(df)[0]), 2)
