from app.core.database import SessionLocal
from app.models.alert import Alert
from app.models.blocked_ip import BlockedIP
from app.models.traffic_log import TrafficLog
from app.models.model_status import ModelStatus

db = SessionLocal()

try:
    # Clear old seed data first
    db.query(Alert).delete()
    db.query(BlockedIP).delete()
    db.query(TrafficLog).delete()
    db.query(ModelStatus).delete()
    db.commit()

    alerts = [
        Alert(
            source_ip="192.168.1.12",
            destination_ip="10.0.0.5",
            threat_type="Crypto-Ransomware Traffic",
            severity="High",
            status="Blocked",
        ),
        Alert(
            source_ip="192.168.1.34",
            destination_ip="10.0.0.8",
            threat_type="Suspicious SMB Activity",
            severity="Medium",
            status="Monitoring",
        ),
        Alert(
            source_ip="192.168.1.50",
            destination_ip="185.220.101.4",
            threat_type="Possible C2 Communication",
            severity="High",
            status="Blocked",
        ),
    ]

    blocked_ips = [
        BlockedIP(
            ip_address="192.168.1.12",
            reason="Crypto-ransomware traffic detected",
            mode="Auto",
            status="Active",
        ),
        BlockedIP(
            ip_address="185.220.101.4",
            reason="Possible C2 communication",
            mode="Auto",
            status="Active",
        ),
    ]

    traffic_logs = [
        TrafficLog(
            source_ip="192.168.1.20",
            destination_ip="8.8.8.8",
            protocol="TCP",
            packet_size=512,
            prediction="Benign",
        ),
        TrafficLog(
            source_ip="192.168.1.12",
            destination_ip="10.0.0.5",
            protocol="SMB",
            packet_size=1480,
            prediction="Malicious",
        ),
        TrafficLog(
            source_ip="192.168.1.34",
            destination_ip="185.220.101.4",
            protocol="TCP",
            packet_size=960,
            prediction="Suspicious",
        ),
        TrafficLog(
            source_ip="192.168.1.55",
            destination_ip="1.1.1.1",
            protocol="UDP",
            packet_size=420,
            prediction="Benign",
        ),
        TrafficLog(
            source_ip="192.168.1.90",
            destination_ip="10.0.0.12",
            protocol="TCP",
            packet_size=1300,
            prediction="Malicious",
        ),
    ]

    model_status = ModelStatus(
        model_name="Random Forest Classifier",
        version="v1.0.0",
        dataset="UGRansom",
        accuracy=94.6,
        precision=93.8,
        recall=95.1,
        f1_score=94.4,
        status="Loaded",
        prediction_mode="Mock / Integration Ready",
    )

    db.add_all(alerts)
    db.add_all(blocked_ips)
    db.add_all(traffic_logs)
    db.add(model_status)

    db.commit()
    print("Seed completed successfully")

except Exception as e:
    db.rollback()
    print("Seed failed:", e)

finally:
    db.close()