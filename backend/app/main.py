from fastapi import FastAPI
from app.core.logger import setup_logging, get_logger

setup_logging()

logger = get_logger(__name__)

app = FastAPI(
    title="GSEAnalytiX Backend API",
    description="Energy Analysis",
    version="1.0"
)

logger.info("GSEAnalytiX Backend API Started Successfully!")
