import json
import time

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.predict import PredictRequest, PredictResponse
from app.services.model import predict_score, MODEL_VERSION
from app.services.prediction_log import create_prediction_log

router = APIRouter(prefix='/api/v1', tags=['prediction'])


@router.post('/predict', response_model=PredictResponse)
async def predict(payload: PredictRequest, request: Request, db: AsyncSession = Depends(get_db)) -> PredictResponse:
    started_at = time.perf_counter()
    request.app.state.metrics['requests_total'].inc()

    prediction = predict_score(payload.feature1, payload.feature2, payload.feature3)
    duration = time.perf_counter() - started_at

    request.app.state.metrics['prediction_latency'].observe(duration)
    request.app.state.metrics['prediction_value'].set(prediction)

    await create_prediction_log(
        db=db,
        feature1=payload.feature1,
        feature2=payload.feature2,
        feature3=payload.feature3,
        prediction=prediction,
        model_version=MODEL_VERSION,
        duration_ms=duration * 1000,
    )

    request.app.state.logger.info(json.dumps({
        'event': 'prediction',
        'input': payload.model_dump(),
        'output': {'prediction': prediction},
        'model_version': MODEL_VERSION,
        'duration_ms': round(duration * 1000, 3),
    }))

    return PredictResponse(prediction=prediction, model_version=MODEL_VERSION, duration_ms=duration * 1000)
