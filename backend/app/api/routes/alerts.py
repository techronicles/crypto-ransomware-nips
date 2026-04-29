from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import SessionLocal
from app.models.alert import Alert

router = APIRouter()


class AlertStatusUpdate(BaseModel):
    status: str


ALLOWED_STATUSES = [
    "Monitoring",
    "Reviewed",
    "Blocked",
    "Resolved",
    "False Positive",
]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def format_alert(item: Alert):
    return {
        "id": item.id,
        "timestamp": item.timestamp.strftime("%Y-%m-%d %I:%M %p"),
        "sourceIp": item.source_ip,
        "destinationIp": item.destination_ip,
        "threatType": item.threat_type,
        "severity": item.severity,
        "status": item.status,
    }


@router.get("")
def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).order_by(Alert.id.desc()).all()
    return [format_alert(item) for item in alerts]


@router.patch("/{alert_id}/status")
def update_alert_status(
    alert_id: int,
    payload: AlertStatusUpdate,
    db: Session = Depends(get_db),
):
    if payload.status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Allowed statuses: {ALLOWED_STATUSES}",
        )

    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found",
        )

    alert.status = payload.status
    db.commit()
    db.refresh(alert)

    return format_alert(alert)