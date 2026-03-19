from app.logger import logger


def log_prediction(result: str) -> None:
    logger.info("Prediction API called")
    logger.info(f"Prediction result: {result}")