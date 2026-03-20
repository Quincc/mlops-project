from sqlalchemy.ext.asyncio import AsyncSession

from app.models.prediction_log import PredictionLog


async def create_prediction_log(
    db: AsyncSession,
    feature1: float,
    feature2: float,
    feature3: float,
    prediction: float,
    model_version: str,
    duration_ms: float,
) -> PredictionLog:
    item = PredictionLog(
        feature1=feature1,
        feature2=feature2,
        feature3=feature3,
        prediction=prediction,
        model_version=model_version,
        duration_ms=duration_ms,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item
