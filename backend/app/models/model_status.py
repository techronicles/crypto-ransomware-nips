from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.core.database import Base


class ModelStatus(Base):
    __tablename__ = "model_status"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    dataset = Column(String, nullable=False)
    accuracy = Column(Float, default=0.0)
    precision = Column(Float, default=0.0)
    recall = Column(Float, default=0.0)
    f1_score = Column(Float, default=0.0)
    last_trained = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Loaded")
    prediction_mode = Column(String, default="Mock / Integration Ready")