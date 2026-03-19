from pathlib import Path
from dotenv import load_dotenv
import os
from app.logger import logger

# Project root is the parent of the directory containing this file
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def _require(key: str) -> str:
    """Fetch a required env var or raise early with a clear message."""
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(
            f"Missing required environment variable: '{key}'. "
            f"Check your .env file at {BASE_DIR / '.env'}"
        )
    return value


MONGO_URL = _require("MONGO_URL")
DB_NAME   = _require("DB_NAME")

logger.info(f"DB_NAME loaded: {DB_NAME}")
logger.info(f"MONGO_URL loaded: {'*' * 10}")