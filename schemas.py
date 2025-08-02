from typing import List, Dict, Any
from pydantic import BaseModel, RootModel, model_validator
from exceptions import EmptyPipeline

class TransformationStep(BaseModel):
    name: str
    params: Dict[str, Any]

class TransformationPipeline(RootModel):
    root: List[TransformationStep]

    @model_validator(mode='before')
    @classmethod
    def validate_pipeline(cls, value):
        if not value:
            raise EmptyPipeline()
        return value
