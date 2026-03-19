import os
import pickle
from app.logger import logger

# Get project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Model path
model_path = os.path.join(BASE_DIR, "model", "churn_pipeline.pkl")

try:
    logger.info("Loading ML model...")

    #  Load once
    with open(model_path, "rb") as f:
        pipeline = pickle.load(f)

    # Extract model
    model = pipeline["model"]

    logger.info("Model loaded successfully ")

except Exception as e:
    logger.error(f"Error loading model: {e}")
    raise e