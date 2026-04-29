from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.traffic_log import TrafficLog
from app.models.blocked_ip import BlockedIP
from app.models.alert import Alert

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    total_traffic = db.query(TrafficLog).count()

    suspicious_traffic = (
        db.query(TrafficLog)
        .filter(TrafficLog.prediction != "Benign")
        .count()
    )

    blocked_ips = (
        db.query(BlockedIP)
        .filter(BlockedIP.status == "Active")
        .count()
    )

    active_alerts = (
        db.query(Alert)
        .filter(Alert.status != "Resolved")
        .count()
    )

    return {
        "totalTraffic": total_traffic,
        "suspiciousTraffic": suspicious_traffic,
        "blockedIps": blocked_ips,
        "activeAlerts": active_alerts,
        "modelAccuracy": 94.6,
        "systemStatus": "Running",
        "backendStatus": "Online",
        "databaseStatus": "Connected",
        "detectionEngine": "Running",
        "preventionMode": "Log Only",
    }