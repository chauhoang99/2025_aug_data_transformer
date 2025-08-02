# main.py

import io
import json

import pandas as pd
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from exception_handler import (
    column_not_found_handler,
    http_exception_handler,
    invalid_csv_handler,
    invalid_pipeline_handler,
    invalid_pipeline_param,
    unknown_transformer_handler,
)
from exceptions import (
    ColumnNotFound,
    InvalidCSV,
    InvalidPipelineJSON,
    InvalidPipelineParam,
    UnknownTransformer,
)
from registry import registry

app = FastAPI()

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(ColumnNotFound, column_not_found_handler)
app.add_exception_handler(InvalidCSV, invalid_csv_handler)
app.add_exception_handler(InvalidPipelineJSON, invalid_pipeline_handler)
app.add_exception_handler(UnknownTransformer, unknown_transformer_handler)
app.add_exception_handler(InvalidPipelineParam, invalid_pipeline_param)


@app.post("/transform/")
async def transform_data(
    file: UploadFile = File(...),
    pipeline: str = Form(...)
):
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    except Exception:
        raise InvalidCSV()

    try:
        steps = json.loads(pipeline)
    except json.JSONDecodeError:
        raise InvalidPipelineJSON()

    # We can automatically plug the required transformer in
    # Or we also can hard-code which one to use here.
    for step in steps:
        transformer = registry.get(step["name"])
        if not transformer:
            raise UnknownTransformer(step['name'])
        try:
            df = transformer(df, **step["params"])
        except TypeError:
            raise InvalidPipelineParam()

    return JSONResponse(content=df.to_dict(orient="records"))


@app.get("/available-transformers/")
def list_transformers():
    return {"available": registry.available_transformers()}
