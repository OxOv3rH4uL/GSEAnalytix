from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.schema.error_schema import ErrorResponse
from app.core.logger import get_logger

logger = get_logger(__name__)


def error_response(
    e: Exception,
    status_code: int,
    message : str | None = None
) -> JSONResponse:
    
    error = ErrorResponse(
        error = type(e).__name__,
        message = message if message is not None else str(e)      
    )

    return JSONResponse(
        status_code=status_code,
        content = error.model_dump(mode="json")
    )


async def global_exceptions(
    req : Request,
    e : Exception
) -> JSONResponse:

    logger.error(
        "Exception in %s %s",
        req.url.path,
        req.method,
        exc_info=e
    )

    error = ErrorResponse(
        error="Internal Server Error",
        message = "Unexpected Error"
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content = error.model_dump(mode="json")
    )