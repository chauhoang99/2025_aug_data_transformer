from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from exceptions import (
    ColumnNotFound,
    InvalidCSV,
    InvalidPipelineJSON,
    UnknownTransformer,
    InvalidPipelineParam
)


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


async def column_not_found_handler(request: Request, exc: ColumnNotFound):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


async def invalid_csv_handler(request: Request, exc: InvalidCSV):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


async def invalid_pipeline_handler(request: Request, exc: InvalidPipelineJSON):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


async def unknown_transformer_handler(request: Request, exc: UnknownTransformer):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


async def invalid_pipeline_param(request: Request, exc: InvalidPipelineParam):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
