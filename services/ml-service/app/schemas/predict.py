from pydantic import BaseModel


class PredictRequest(BaseModel):
    feature1: float
    feature2: float
    feature3: float


class PredictResponse(BaseModel):
    prediction: float
    model_version: str
    duration_ms: float
