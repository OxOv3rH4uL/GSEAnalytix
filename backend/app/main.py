from fastapi import FastAPI
from app.core.logger import setup_logging, get_logger
from app.api.routers.projects_router import project_router as project
setup_logging()

logger = get_logger(__name__)

app = FastAPI(
    title="GSEAnalytiX Backend API",
    description="Energy Analysis",
    version="1.0"
)

app.include_router(
    project,
    prefix="/api"
)


logger.info("GSEAnalytiX Backend API Started Successfully!")

@app.get("/ping")
def checking():
    return {"message" : "pong"}
