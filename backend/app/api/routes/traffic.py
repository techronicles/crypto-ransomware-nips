from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.traffic_log import TrafficLog

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("")
def get_traffic_records(db: Session = Depends(get_db)):
    rows = db.query(TrafficLog).order_by(TrafficLog.id.desc()).all()

    return [
        {
            "id": item.id,
            "timestamp": item.timestamp.strftime("%Y-%m-%d %I:%M %p"),
            "sourceIp": item.source_ip,
            "destinationIp": item.destination_ip,
            "protocol": item.protocol,
            "packetSize": item.packet_size,
            "prediction": item.prediction,
        }
        for item in rows
    ]