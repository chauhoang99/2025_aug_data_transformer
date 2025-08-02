# main.py

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import io
import json

from registry import registry
import transformations  # Needed to register transformers

app = FastAPI()


class TransformationStep(BaseModel):
    name: str
    params: dict


@app.post("/transform/")
async def transform_data(
    file: UploadFile = File(...),
    pipeline: str = Form(...)
):
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV")

    try:
        steps = json.loads(pipeline)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid pipeline JSON")

    # We can automatically plug the required transformer in
    # Or we also can hard-code which one to use here.
    for step in steps:
        transformer = registry.get(step["name"])
        if not transformer:
            raise HTTPException(
                status_code=400, detail=f"Unknown transformer: {step['name']}")
        try:
            df = transformer(df, **step["params"])
        except KeyError as e:
            raise HTTPException(
                status_code=400, detail=''
            )

    return JSONResponse(content=df.to_dict(orient="records"))


@app.get("/available-transformers/")
def list_transformers():
    return {"available": registry.available_transformers()}
