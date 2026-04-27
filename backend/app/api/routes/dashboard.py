from fastapi import APIRouter

router = APIRouter()


@router.get("/summary")
def get_dashboard_summary():
    return {
        "totalTraffic": 99995,
        "suspiciousTraffic": 285,
        "blockedIps": 7,
        "activeAlerts": 4,
        "modelAccuracy": 94.6,
        "systemStatus": "Running",
        "backendStatus": "Online",
        "databaseStatus": "Mock Mode",
        "detectionEngine": "Running",
        "preventionMode": "Log Only"
    }