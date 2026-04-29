from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.model_status import ModelStatus

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/status")
def get_model_status(db: Session = Depends(get_db)):
    model = db.query(ModelStatus).order_by(ModelStatus.id.desc()).first()

    if not model:
        raise HTTPException(
            status_code=404,
            detail="Model status not found"
        )

    return {
        "modelName": model.model_name,
        "version": model.version,
        "dataset": model.dataset,
        "accuracy": model.accuracy,
        "precision": model.precision,
        "recall": model.recall,
        "f1Score": model.f1_score,
        "lastTrained": model.last_trained.strftime("%Y-%m-%d"),
        "status": model.status,
        "predictionMode": model.prediction_mode,
    }