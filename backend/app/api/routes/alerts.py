from fastapi import APIRouter

router = APIRouter()


@router.get("")
def get_alerts():
    return [
        {
            "id": 1,
            "timestamp": "2026-04-27 09:30 AM",
            "sourceIp": "192.168.1.12",
            "destinationIp": "10.0.0.5",
            "threatType": "Crypto-Ransomware Traffic",
            "severity": "High",
            "status": "Blocked",
        },
        {
            "id": 2,
            "timestamp": "2026-04-27 09:45 AM",
            "sourceIp": "192.168.1.34",
            "destinationIp": "10.0.0.8",
            "threatType": "Suspicious SMB Activity",
            "severity": "Medium",
            "status": "Monitoring",
        },
        {
            "id": 3,
            "timestamp": "2026-04-27 10:05 AM",
            "sourceIp": "192.168.1.50",
            "destinationIp": "185.220.101.4",
            "threatType": "Possible C2 Communication",
            "severity": "High",
            "status": "Blocked",
        },
    ]