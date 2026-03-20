from contextlib import asynccontextmanager
import logging
import time

from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

from app.api.routes import router
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

REQUESTS_TOTAL = Counter('ml_service_requests_total', 'Total requests to predict endpoint')
PREDICTION_LATENCY = Histogram('ml_service_prediction_latency_seconds', 'Prediction latency in seconds')
PREDICTION_VALUE = Gauge('ml_service_prediction_value', 'Last prediction value')


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)
app.state.logger = logger
app.state.metrics = {
    'requests_total': REQUESTS_TOTAL,
    'prediction_latency': PREDICTION_LATENCY,
    'prediction_value': PREDICTION_VALUE,
}
app.include_router(router)


@app.get('/health')
async def health() -> dict[str, str]:
    return {'status': 'ok'}


@app.get('/metrics')
async def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
