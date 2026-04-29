from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import SessionLocal
from app.models.blocked_ip import BlockedIP

router = APIRouter()


class BlockIPRequest(BaseModel):
    ipAddress: str
    reason: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("")
def get_blocked_ips(db: Session = Depends(get_db)):
    rows = db.query(BlockedIP).order_by(BlockedIP.id.desc()).all()

    return [
        {
            "id": item.id,
            "ipAddress": item.ip_address,
            "reason": item.reason,
            "blockedAt": item.blocked_at.strftime("%Y-%m-%d %I:%M %p"),
            "mode": item.mode,
            "status": item.status,
        }
        for item in rows
    ]


@router.post("")
def add_blocked_ip(payload: BlockIPRequest, db: Session = Depends(get_db)):
    row = BlockedIP(
        ip_address=payload.ipAddress,
        reason=payload.reason,
        mode="Manual",
        status="Active",
    )

    db.add(row)
    db.commit()
    db.refresh(row)

    return {
        "id": row.id,
        "ipAddress": row.ip_address,
        "reason": row.reason,
        "blockedAt": row.blocked_at.strftime("%Y-%m-%d %I:%M %p"),
        "mode": row.mode,
        "status": row.status,
    }