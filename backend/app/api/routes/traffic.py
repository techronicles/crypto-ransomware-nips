from fastapi import APIRouter

router = APIRouter()


@router.get("")
def get_traffic_records():
    return [
        {
            "id": 1,
            "timestamp": "2026-04-27 09:31 AM",
            "sourceIp": "192.168.1.20",
            "destinationIp": "8.8.8.8",
            "protocol": "TCP",
            "packetSize": 512,
            "prediction": "Benign",
        },
        {
            "id": 2,
            "timestamp": "2026-04-27 09:36 AM",
            "sourceIp": "192.168.1.12",
            "destinationIp": "10.0.0.5",
            "protocol": "SMB",
            "packetSize": 1480,
            "prediction": "Malicious",
        },
        {
            "id": 3,
            "timestamp": "2026-04-27 09:42 AM",
            "sourceIp": "192.168.1.34",
            "destinationIp": "185.220.101.4",
            "protocol": "TCP",
            "packetSize": 960,
            "prediction": "Suspicious",
        },
    ]