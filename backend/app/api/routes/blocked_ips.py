from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class BlockIPRequest(BaseModel):
    ipAddress: str
    reason: str


blocked_ips = [
    {
        "id": 1,
        "ipAddress": "192.168.1.12",
        "reason": "Crypto-ransomware traffic detected",
        "blockedAt": "2026-04-27 09:30 AM",
        "mode": "Auto",
        "status": "Active",
    },
    {
        "id": 2,
        "ipAddress": "185.220.101.4",
        "reason": "Possible C2 communication",
        "blockedAt": "2026-04-27 10:05 AM",
        "mode": "Auto",
        "status": "Active",
    },
]


@router.get("")
def get_blocked_ips():
    return blocked_ips


@router.post("")
def add_blocked_ip(payload: BlockIPRequest):
    new_ip = {
        "id": len(blocked_ips) + 1,
        "ipAddress": payload.ipAddress,
        "reason": payload.reason,
        "blockedAt": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
        "mode": "Manual",
        "status": "Active",
    }

    blocked_ips.insert(0, new_ip)
    return new_ip