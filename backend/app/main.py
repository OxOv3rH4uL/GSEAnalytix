from fastapi import FastAPI
from app.core.logger import setup_logging, get_logger
from app.api.routers.projects_router import project_router as project
from app.api.routers.device_router import device_router as devices
from app.core.exceptions_handler import global_exceptions
setup_logging()

logger = get_logger(__name__)

app = FastAPI(
    title="GSEAnalytiX Backend API",
    description="Energy Analysis",
    version="1.0"
)

app.add_exception_handler(
    Exception,
    global_exceptions
)

app.include_router(
    project,
    prefix="/api"
)

app.include_router(
    devices,
    prefix="/api"
)


logger.info("GSEAnalytiX Backend API Started Successfully!")

@app.get("/ping")
def checking():
    return {"message" : "pong"}
