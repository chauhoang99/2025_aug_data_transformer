from fastapi import HTTPException


class ColumnNotFound(HTTPException):
    def __init__(self, column_name: str):
        super().__init__(status_code=400,
                         detail=f"Column '{column_name}' not found")


class InvalidCSV(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Invalid CSV")


class InvalidPipelineJSON(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Invalid pipeline JSON")


class UnknownTransformer(HTTPException):
    def __init__(self, transformer_name: str):
        super().__init__(status_code=400,
                         detail=f"Unknown transformer: {transformer_name}")


class InvalidPipelineParam(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Unknown pipeline param, please check again")


class EmptyPipeline(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Pipeline must not be empty")


class PydanticValidationError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=400, detail=f"{message}")
