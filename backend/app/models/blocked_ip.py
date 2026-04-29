from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base


class BlockedIP(Base):
    __tablename__ = "blocked_ips"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, nullable=False, unique=True)
    reason = Column(String, nullable=False)
    blocked_at = Column(DateTime, default=datetime.utcnow)
    mode = Column(String, default="Manual")
    status = Column(String, default="Active")