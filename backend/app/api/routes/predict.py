from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.traffic_log import TrafficLog
from app.models.alert import Alert
from app.models.blocked_ip import BlockedIP

router = APIRouter()


class PredictRequest(BaseModel):
    sourceIp: str
    destinationIp: str
    protocol: str
    packetSize: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def classify_traffic(protocol: str, packet_size: int):
    protocol_upper = protocol.upper()

    if protocol_upper in ["SMB", "FTP"] and packet_size >= 1000:
        return "Malicious", 0.94, "Crypto-Ransomware Traffic"

    if protocol_upper == "TCP" and packet_size >= 1200:
        return "Suspicious", 0.78, "Suspicious High-Volume TCP Traffic"

    if protocol_upper == "UDP" and packet_size >= 900:
        return "Suspicious", 0.72, "Abnormal UDP Traffic"

    return "Benign", 0.31, "Normal Traffic"


@router.post("")
def predict_traffic(payload: PredictRequest, db: Session = Depends(get_db)):
    prediction, confidence, threat_type = classify_traffic(
        payload.protocol,
        payload.packetSize,
    )

    traffic_log = TrafficLog(
        source_ip=payload.sourceIp,
        destination_ip=payload.destinationIp,
        protocol=payload.protocol.upper(),
        packet_size=payload.packetSize,
        prediction=prediction,
    )

    db.add(traffic_log)
    db.commit()
    db.refresh(traffic_log)

    alert_created = None
    blocked_ip_created = None

    if prediction in ["Suspicious", "Malicious"]:
        alert = Alert(
            source_ip=payload.sourceIp,
            destination_ip=payload.destinationIp,
            threat_type=threat_type,
            severity="High" if prediction == "Malicious" else "Medium",
            status="Blocked" if prediction == "Malicious" else "Monitoring",
        )

        db.add(alert)
        db.commit()
        db.refresh(alert)

        alert_created = {
            "id": alert.id,
            "sourceIp": alert.source_ip,
            "destinationIp": alert.destination_ip,
            "threatType": alert.threat_type,
            "severity": alert.severity,
            "status": alert.status,
        }

    if prediction == "Malicious":
        existing_block = (
            db.query(BlockedIP)
            .filter(BlockedIP.ip_address == payload.sourceIp)
            .first()
        )

        if not existing_block:
            blocked_ip = BlockedIP(
                ip_address=payload.sourceIp,
                reason=threat_type,
                mode="Auto",
                status="Active",
            )

            db.add(blocked_ip)
            db.commit()
            db.refresh(blocked_ip)

            blocked_ip_created = {
                "id": blocked_ip.id,
                "ipAddress": blocked_ip.ip_address,
                "reason": blocked_ip.reason,
                "mode": blocked_ip.mode,
                "status": blocked_ip.status,
            }

    return {
        "trafficLogId": traffic_log.id,
        "prediction": prediction,
        "confidence": confidence,
        "threatType": threat_type,
        "alertCreated": alert_created,
        "blockedIpCreated": blocked_ip_created,
    }