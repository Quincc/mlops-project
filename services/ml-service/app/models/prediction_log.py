from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PredictionLog(Base):
    __tablename__ = 'prediction_log'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    feature1: Mapped[float] = mapped_column(Float, nullable=False)
    feature2: Mapped[float] = mapped_column(Float, nullable=False)
    feature3: Mapped[float] = mapped_column(Float, nullable=False)
    prediction: Mapped[float] = mapped_column(Float, nullable=False)
    model_version: Mapped[str] = mapped_column(String(50), nullable=False)
    duration_ms: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
